from typing import Iterable, Any
from typing import List

from aiogram import BaseMiddleware
from aiogram import Dispatcher
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType

from aiogram_tests.mocked_bot import MockedBot


class RequestHandler:
    def __init__(
        self,
        dp_middlewares: Iterable[BaseMiddleware] | None = None,
        exclude_observer_methods: Iterable[str] | None = None,
        dp: Dispatcher | None = None,
        **kwargs: Any,
    ):
        self.bot = MockedBot()
        if dp is None:
            dp = Dispatcher(storage=MemoryStorage())
        self.dp = dp

        if dp_middlewares is None:
            dp_middlewares = ()

        if exclude_observer_methods is None:
            exclude_observer_methods = []

        dispatcher_methods = self._get_dispatcher_event_observers()
        available_methods = tuple(
            set(dispatcher_methods) - set(exclude_observer_methods)
        )
        self._register_middlewares(available_methods, tuple(dp_middlewares))

    def _get_dispatcher_event_observers(self) -> List[str]:
        """
        Returns a names for bot event observers, like message, callback_query etc.
        """

        result = []
        for name in dir(self.dp):
            if isinstance(getattr(self.dp, name), TelegramEventObserver):
                result.append(name)

        return result

    def _register_middlewares(
        self, event_observer: Iterable, middlewares: Iterable
    ) -> None:
        for eo_name in event_observer:
            for m in middlewares:
                eo_obj = getattr(self.dp, eo_name)
                eo_obj.middleware.register(m)

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError

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
        response = self.bot.add_result_for(
            method=method,
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            migrate_to_chat_id=migrate_to_chat_id,
            retry_after=retry_after,
        )
        return response
