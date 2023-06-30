from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.api.auth import intern_or_teacher_only
from backend.api.schemas import chat as schemas
from backend.api.queries import chat as queries
from backend.api.queries.users import get_user
from backend.models import User
from backend.settings import LimitOffsetPage, LimitOffsetParams
from backend.api.errors.errors import not_found
from backend.ws import ws_manager


router = APIRouter(prefix='/chat')


async def ws_intern_or_teacher_only(token: str, db: Session = Depends(get_db)):
    return await intern_or_teacher_only(token, db)


def current_recipient(recipient_id: int, db: Session = Depends(get_db)):
    recipient = get_user(db, recipient_id)
    if recipient is None:
        raise not_found()
    return recipient


def current_chatters(
    db: Session = Depends(get_db),
    sender: User = Depends(intern_or_teacher_only),
    recipient: User = Depends(current_recipient),
):
    intern, teacher = sender, recipient
    if intern.is_teacher:
        intern, teacher = recipient, sender
    if not queries.users_are_suitable(db, teacher=teacher, intern=intern):
        raise not_found()

    return sender, recipient


@router.get('/{recipient_id}', response_model=LimitOffsetPage[schemas.Message])
def get_messages(
    chatters: tuple[User, User] = Depends(current_chatters),
    params: LimitOffsetParams = Depends(),
    db: Session = Depends(get_db),
):
    return queries.get_messages(db, *chatters, params)


@router.post('/{recipient_id}', response_model=schemas.Message)
async def send_message(
    data: schemas.SendMessage,
    chatters: tuple[User, User] = Depends(current_chatters),
    db: Session = Depends(get_db),
):
    result = queries.create_message(db, *chatters, data.message)
    response_data = schemas.Message.from_orm(result)
    dict_ = response_data.dict()
    dict_['created_at'] = str(dict_['created_at'])
    await ws_manager.broadcast(dict_, chatters[1:])
    return response_data


@router.websocket('/ws/{token}')
async def connect_to_chat(
    websocket: WebSocket,
    user: User = Depends(ws_intern_or_teacher_only),
):
    await ws_manager.connect(user, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json({'pong': True})
    except WebSocketDisconnect:
        await ws_manager.disconnect(user)
