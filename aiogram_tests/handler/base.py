from typing import Iterable
from typing import List

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Chat
from aiogram.types import User

from aiogram_tests.mocked_bot import MockedBot
from aiogram_tests.types.dataset import CHAT
from aiogram_tests.types.dataset import USER


class RequestHandler:
    def __init__(
        self,
        dp_middlewares: Iterable = None,
        dp_filters: Iterable = None,
        exclude_observer_methods: Iterable = None,
        **kwargs,
    ):
        self.bot = MockedBot()
        self.dp = Dispatcher(storage=MemoryStorage())

        if dp_middlewares is None:
            dp_middlewares = ()

        if dp_filters is None:
            dp_filters = ()

        if exclude_observer_methods is None:
            exclude_observer_methods = []

        dispatcher_methods = self._get_dispatcher_event_observers()
        available_methods = tuple(set(dispatcher_methods) - set(exclude_observer_methods))
        self._register_middlewares(available_methods, tuple(dp_middlewares))
        self._register_filters(available_methods, tuple(dp_filters))

        Bot.set_current(self.bot)
        User.set_current(USER.as_object())
        Chat.set_current(CHAT.as_object())

    def _get_dispatcher_event_observers(self) -> List[str]:
        """
        Returns a names for bot event observers, like message, callback_query etc.
        """

        result = []
        for name in dir(self.bot):
            if isinstance(getattr(self.bot, name), TelegramEventObserver):
                result.append(name)

        return result

    def _register_middlewares(self, event_observer: Iterable, middlewares: Iterable) -> None:
        for eo_name in event_observer:
            for m in middlewares:
                eo_obj = getattr(self.bot, eo_name)
                eo_obj.middleware.register(m)

    def _register_filters(self, event_observer: Iterable, filters: Iterable) -> None:
        for eo_name in event_observer:
            for f in filters:
                eo_obj = getattr(self.bot, eo_name)
                eo_obj.middleware.register(f)

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError
