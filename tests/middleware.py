from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class TestMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
    ):
        return await handler(event, data)
