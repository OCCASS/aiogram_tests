from typing import Callable
from typing import Dict
from typing import Generator
from typing import Iterable
from typing import List
from typing import Union

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.filters import Filter
from aiogram.filters import StateFilter
from aiogram.fsm.state import State
from aiogram.fsm.storage.memory import MemoryStorage

from .mocked_bot import MockedBot
from .types.dataset import CHAT
from .types.dataset import USER


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
        types.User.set_current(USER.as_object())
        types.Chat.set_current(CHAT.as_object())

    def _get_dispatcher_event_observers(self) -> Generator[str]:
        """
        Returns a names for bot event observers, like message, callback_query etc.
        """

        result = (name for name in dir(self.bot) if isinstance(getattr(self.bot, name), TelegramEventObserver))
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


class TelegramEventObserverHandler(RequestHandler):
    def __init__(
        self,
        callback: Callable,
        *filters: Filter,
        state: Union[State, str, None] = None,
        state_data: Dict = None,
        dp_middlewares: Iterable = None,
        exclude_observer_methods: Iterable = None,
        **kwargs,
    ):
        super().__init__(dp_middlewares, (), exclude_observer_methods)

        self._callback = callback
        self._filters: List = list(filters)
        self._state: Union[State, str, None] = state
        self._state_data: Dict = state_data

        if self._state_data is None:
            self._state_data = {}

        if self._filters is None:
            self._filters = []

        if not isinstance(self._state_data, dict):
            raise ValueError("state_data is not a dict")

    def __call__(self, *args, **kwargs):
        if self._state:
            self._filters.append(StateFilter(self._state))

        self.register_handler()

        if self._state:
            state = self.dp.fsm.get_context(self.bot, user_id=12345678, chat_id=12345678)
            await state.set_state(self._state)
            await state.update_data(**self._state_data)

        self.feed_update(*args, **kwargs)

    def register_handler(self) -> None:
        """
        Register TelegramEventObserver in dispatcher
        """

        raise NotImplementedError

    def feed_update(self, *args, **kwargs) -> None:
        """
        Feed dispatcher updates
        """

        raise NotImplementedError


class MessageHandler(TelegramEventObserverHandler):
    def register_handler(self) -> None:
        self.dp.message.register(self._callback, *self._filters)

    def feed_update(self, message: types.Message, *args, **kwargs) -> None:
        self.dp.feed_update(self.bot, types.Update(update_id=12345678, message=message))


class CallbackQueryHandler(TelegramEventObserverHandler):
    def register_handler(self) -> None:
        self.dp.callback_query.register(self._callback, *self._filters)

    def feed_update(self, callback_query: types.CallbackQuery, *args, **kwargs) -> None:
        self.dp.feed_update(self.bot, types.Update(update_id=12345678, callback_query=callback_query))
