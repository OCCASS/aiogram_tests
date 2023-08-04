from collections import deque
from typing import AsyncGenerator, Dict, Any, TYPE_CHECKING, cast
from typing import Deque
from typing import Optional

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType
from aiogram.types import ResponseParameters, UNSET_PARSE_MODE
from aiogram.types import User


class MockedSession(BaseSession):
    def __init__(self):
        super(MockedSession, self).__init__()
        self.responses: Deque[Response[TelegramType]] = deque()
        self.requests: Deque[TelegramMethod[TelegramType]] = deque()
        self.closed = True

    def add_result(self, response: Response[TelegramType]) -> Response[TelegramType]:
        self.responses.appendleft(response)
        return response

    def get_request(self) -> TelegramMethod[TelegramType]:
        return self.requests.pop()

    async def close(self):
        self.closed = True

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: Optional[int] = UNSET_PARSE_MODE,
    ) -> TelegramType:
        self.closed = False
        self.requests.append(method)
        response: Response[TelegramType] = self.responses.pop()
        self.check_response(
            bot=bot,
            method=method,
            status_code=cast(int, response.error_code),
            content=response.model_dump_json(),
        )
        return response.result  # type: ignore

    async def stream_content(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        yield b""


class MockedBot(Bot):
    if TYPE_CHECKING:
        session: MockedSession

    def __init__(self, **kwargs):
        super(MockedBot, self).__init__(
            kwargs.pop("token", "42:TEST"), session=MockedSession(), **kwargs
        )
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name="FirstName",
            last_name="LastName",
            username="username",
            language_code="ru",
        )

    def add_result_for(
        self,
        method: TelegramMethod[TelegramType],
        ok: bool,
        result: TelegramType | None = None,
        description: str | None = None,
        error_code: int = 200,
        migrate_to_chat_id: int | None = None,
        retry_after: int | None = None,
    ) -> Response[TelegramType]:
        response = Response[method.__returning__](  # type: ignore
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            parameters=ResponseParameters(
                migrate_to_chat_id=migrate_to_chat_id,
                retry_after=retry_after,
            ),
        )
        self.session.add_result(response)
        return response

    async def __call__(
        self,
        method: TelegramMethod[TelegramType],
        request_timeout: Optional[int] = None,
    ):
        self.add_result_for(method, ok=True)
        return await super().__call__(method, request_timeout)

    def get_request(self) -> TelegramMethod[TelegramType]:
        return self.session.get_request()
