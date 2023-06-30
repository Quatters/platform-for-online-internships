import asyncio
import contextlib
from typing import Iterable
from fastapi import WebSocket
from backend.models import User


class WebSocketManager:
    def __init__(self):
        self._connections: dict[int, WebSocket] = {}

    async def connect(self, user: User, ws: WebSocket):
        await ws.accept()
        self._connections[user.id] = ws

    # async def disconnect(self, *users: User):
    #     for user in users:
    #         with contextlib.suppress(KeyError):
    #             await self._connections[user.id].close()
    #             del self._connections[user.id]

    async def broadcast(self, json: dict, users: Iterable[User]):
        for user in users:
            ws = self._connections.get(user.id);
            if ws is not None:
                await ws.send_json(json)

    async def disconnect_all(self):  # nocv
        for ws in self._connections.values():
            await ws.close();
        self._connections = {}

    def __del__(self):  # nocv
        with contextlib.suppress(Exception):
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.disconnect_all())
            else:
                loop.run_until_complete(self.disconnect_all())


ws_manager = WebSocketManager()
