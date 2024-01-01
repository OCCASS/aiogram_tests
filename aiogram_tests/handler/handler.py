from typing import Callable, Any
from typing import Iterable
from typing import List

from aiogram import types
from aiogram.filters import Filter
from aiogram.filters import StateFilter
from aiogram.fsm.state import State

from .base import RequestHandler


class TelegramEventObserverHandler(RequestHandler):
    def __init__(
        self,
        callback: Callable,
        *filters: Filter,
        state: State | str | None = None,
        state_data: dict[str, Any] | None = None,
        dp_middlewares: Iterable | None = None,
        exclude_observer_methods: Iterable | None = None,
        **kwargs,
    ):
        super().__init__(dp_middlewares, exclude_observer_methods, **kwargs)

        self._callback = callback
        self._filters: List = list(filters)
        self._state: State | str | None = state
        self._state_data: dict[str, Any] | None = state_data

        if self._state_data is None:
            self._state_data = {}

        if self._filters is None:
            self._filters = []

        if not isinstance(self._state_data, dict):
            raise ValueError("state_data is not a dict")

    async def __call__(self, *args, **kwargs):
        if self._state:
            self._filters.append(StateFilter(self._state))

        self.register_handler()

        if self._state:
            state = self.dp.fsm.get_context(
                self.bot, user_id=12345678, chat_id=12345678
            )
            await state.set_state(self._state)
            await state.update_data(**self._state_data)

        await self.feed_update(*args, **kwargs)

    def register_handler(self) -> None:
        """
        Register TelegramEventObserver in dispatcher
        """

        raise NotImplementedError

    async def feed_update(self, *args, **kwargs) -> None:
        """
        Feed dispatcher updates
        """

        raise NotImplementedError


class MessageHandler(TelegramEventObserverHandler):
    def __init__(
        self,
        callback: Callable,
        *filters: Filter,
        state: State | str | None = None,
        state_data: dict[str, Any] | None = None,
        dp_middlewares: Iterable | None = None,
        exclude_observer_methods: Iterable | None = None,
        **kwargs,
    ):
        super().__init__(
            callback,
            *filters,
            state=state,
            state_data=state_data,
            dp_middlewares=dp_middlewares,
            exclude_observer_methods=exclude_observer_methods,
            **kwargs,
        )

    def register_handler(self) -> None:
        self.dp.message.register(self._callback, *self._filters)

    async def feed_update(self, message: types.Message, *args, **kwargs) -> None:
        await self.dp.feed_update(
            self.bot, types.Update(update_id=12345678, message=message)
        )


class CallbackQueryHandler(TelegramEventObserverHandler):
    def __init__(
        self,
        callback: Callable,
        *filters: Filter,
        state: State | str | None = None,
        state_data: dict[str, Any] | None = None,
        dp_middlewares: Iterable | None = None,
        exclude_observer_methods: Iterable | None = None,
        **kwargs,
    ):
        super().__init__(
            callback,
            *filters,
            state=state,
            state_data=state_data,
            dp_middlewares=dp_middlewares,
            exclude_observer_methods=exclude_observer_methods,
            **kwargs,
        )

    def register_handler(self) -> None:
        self.dp.callback_query.register(self._callback, *self._filters)

    async def feed_update(
        self, callback_query: types.CallbackQuery, *args, **kwargs
    ) -> None:
        await self.dp.feed_update(
            self.bot, types.Update(update_id=12345678, callback_query=callback_query)
        )


class MyChatMemberHandler(TelegramEventObserverHandler):
    def __init__(
        self,
        callback: Callable,
        *filters: Filter,
        state: State | str | None = None,
        state_data: dict[str, Any] | None = None,
        dp_middlewares: Iterable | None = None,
        exclude_observer_methods: Iterable | None = None,
        **kwargs,
    ):
        super().__init__(
            callback,
            *filters,
            state=state,
            state_data=state_data,
            dp_middlewares=dp_middlewares,
            exclude_observer_methods=exclude_observer_methods,
            **kwargs,
        )

    def register_handler(self) -> None:
        self.dp.my_chat_member.register(self._callback, *self._filters)

    async def feed_update(
        self, my_chat_member: types.ChatMemberUpdated, *args, **kwargs
    ) -> None:
        await self.dp.feed_update(
            self.bot, types.Update(update_id=12345678, my_chat_member=my_chat_member)
        )
