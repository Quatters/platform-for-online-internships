from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from backend.api.schemas.users import User
from backend.api.queries.users import get_user_by_email
from backend.api.schemas.users import TokenData
from backend.database import get_db
from backend.settings import AUTH
from backend.api.errors.errors import no_permission
from backend.api.utils import crypt_context


oauth2 = OAuth2PasswordBearer(tokenUrl=AUTH['TOKEN_URL'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


def passwords_match(plain_password: str, hashed_password: str):
    return crypt_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not passwords_match(password, user.password):
        return False
    return user


def create_access_token(data: dict):
    return jwt.encode(
        claims={
            **data.copy(),
            'exp': datetime.utcnow() + timedelta(minutes=AUTH['TOKEN_EXPIRE_MINUTES'])
        },
        key=AUTH['SECRET_KEY'],
        algorithm=AUTH['ALGORITHM'],
    )


async def get_current_user_data(token: Annotated[str, Depends(oauth2)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, AUTH['SECRET_KEY'], algorithms=[AUTH['ALGORITHM']])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2)], db: Session = Depends(get_db)):
    user = await get_current_user_data(token, db)
    return User.from_orm(user)


async def admin_only(token: Annotated[str, Depends(oauth2)], db: Session = Depends(get_db)):
    user = await get_current_user(token, db)
    if user.is_admin:
        return user
    raise no_permission()


async def admin_or_teacher_only(token: Annotated[str, Depends(oauth2)], db: Session = Depends(get_db)):
    user = await get_current_user(token, db)
    if user.is_admin or user.is_teacher:
        return user
    raise no_permission()


async def intern_only(token: Annotated[str, Depends(oauth2)], db: Session = Depends(get_db)):
    user = await get_current_user(token, db)
    if user.is_admin or user.is_teacher:
        raise no_permission()
    return user
