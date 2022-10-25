import pytest

from aiogram_tests.exceptions import MethodIsNotCalledError
from aiogram_tests.handler import MessageHandler
from aiogram_tests.requester import Calls
from aiogram_tests.requester import CallsList
from aiogram_tests.requester import Requester
from aiogram_tests.types.dataset import MESSAGE


def test_calls_list():
    calls_list = CallsList([1, 2, 3, 4, 5, 6, 7, 8])
    assert calls_list.fetchone() == 8
    assert calls_list.fetchall() == [1, 2, 3, 4, 5, 6, 7, 8]


def test_calls():
    GeneratedCalls = type("GeneratedCalls", (Calls,), {"send_message": "Message"})
    generated_calls = GeneratedCalls()
    assert generated_calls.send_message == "Message"
    with pytest.raises(MethodIsNotCalledError):
        _ = generated_calls.callback_query


@pytest.mark.asyncio
async def test_requester():
    async def callback(*args, **kwargs):
        pass

    request_handler = MessageHandler(callback)
    requester = Requester(request_handler=request_handler)
    calls = await requester.query(message=MESSAGE.as_object(text="Hello world!"))
    assert isinstance(calls, Calls)
    with pytest.raises(MethodIsNotCalledError):
        _ = calls.send_message

    with pytest.raises(AttributeError):
        await requester.query(callback_query=MESSAGE.as_object(text="Hello world!"))
