import pytest
from aiogram.filters import StateFilter

from .middleware import TestMiddleware
from aiogram_tests.handler import MessageHandler
from aiogram_tests.handler import RequestHandler


def test_request_handler_initialization():
    RequestHandler((), ())


def test_request_handler_dp_middlewares():
    r_h = RequestHandler(dp_middlewares=(TestMiddleware(),))
    middlewares_count = len(r_h.dp.message.middleware)
    assert middlewares_count == 1

    r_h = RequestHandler(dp_middlewares=(TestMiddleware(), TestMiddleware()))
    middlewares_count = len(r_h.dp.message.middleware)
    assert middlewares_count == 2


@pytest.mark.asyncio
async def test_telegram_observ_handler():
    async def callback(*args, **kwargs):
        pass

    t_h = MessageHandler(callback)
    await t_h(None)
    handlers_count = len(t_h.dp.message.handlers)
    assert handlers_count == 1

    t_h = MessageHandler(callback, StateFilter(None))
    await t_h(None)
    handlers_count = len(t_h.dp.message.handlers)
    assert handlers_count == 1
