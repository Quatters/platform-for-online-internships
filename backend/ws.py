import asyncio
import contextlib
import orjson
from typing import Iterable
from fastapi import WebSocket
from backend.models import User


class WebSocketManager:  # nocv
    def __init__(self):
        self._connections: dict[int, WebSocket] = {}

    async def connect(self, user: User, ws: WebSocket):
        await ws.accept()
        self._connections[user.id] = ws

    async def disconnect(self, *users: User):
        for user in users:
            with contextlib.suppress(KeyError):
                del self._connections[user.id]

    async def broadcast(self, message: str | bytes | dict, users: Iterable[User]):
        send_func_name = 'send_bytes'
        if isinstance(message, str):
            send_func_name = 'send_text'
        elif isinstance(message, dict):
            send_func_name = 'send_bytes'
            message = orjson.dumps(message)
        for user in users:
            ws = self._connections.get(user.id)
            if ws is not None:
                try:
                    await getattr(ws, send_func_name)(message)
                except RuntimeError:
                    await self.disconnect(user)

    async def disconnect_all(self):
        for ws in self._connections.values():
            await ws.close()
        self._connections = {}

    def __del__(self):
        with contextlib.suppress(Exception):
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.disconnect_all())
            else:
                loop.run_until_complete(self.disconnect_all())


ws_manager = WebSocketManager()
