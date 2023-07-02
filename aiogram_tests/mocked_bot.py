from collections import deque
from typing import AsyncGenerator
from typing import Deque
from typing import Optional
from typing import Type
from typing import Union

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Request
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType
from aiogram.types import ResponseParameters
from aiogram.types import UNSET
from aiogram.types import User


DEFAULT_AUTO_MOCK_SUCCESS = True


class MockedSession(BaseSession):
    def __init__(self):
        super().__init__()
        self.responses: Deque[Response[TelegramType]] = deque()
        self.requests: Deque[Request] = deque()
        self.closed = True

    def add_result(self, response: Response[TelegramType]) -> Response[TelegramType]:
        self.responses.appendleft(response)
        return response

    def get_request(self) -> Union[Request, None]:
        if self.requests:
            return self.requests[-1]

        return None

    async def close(self):
        self.closed = True

    async def make_request(
        self, bot: Bot, method: TelegramMethod[TelegramType], timeout: Optional[int] = UNSET
    ) -> TelegramType:
        self.closed = False
        self.requests.append(method.build_request(bot))
        response: Response[TelegramType] = self.responses.pop()
        self.check_response(method=method, status_code=response.error_code, content=response.json())
        return response.result  # type: ignore

    async def stream_content(
        self, url: str, timeout: int, chunk_size: int
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        yield b""


class MockedBot(Bot):
    def __init__(self, auto_mock_success: bool = DEFAULT_AUTO_MOCK_SUCCESS, **kwargs):
        super().__init__(kwargs.pop("token", "42:TEST"), session=MockedSession(), **kwargs)
        self.session = MockedSession()
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name="FirstName",
            last_name="LastName",
            username="username",
            language_code="ru",
        )
        self.auto_mock_success = auto_mock_success

    def add_result_for(
        self,
        method: Type[TelegramMethod[TelegramType]],
        ok: bool,
        result: TelegramType = None,
        description: Optional[str] = None,
        error_code: int = 200,
        migrate_to_chat_id: Optional[int] = None,
        retry_after: Optional[int] = None,
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

    async def __call__(self, method: TelegramMethod, request_timeout: Optional[int] = None):
        if self.auto_mock_success:
            self.add_result_for(method.__class__, ok=True)
        return await super().__call__(method, request_timeout)

    def get_request(self) -> Request:
        return self.session.get_request()
