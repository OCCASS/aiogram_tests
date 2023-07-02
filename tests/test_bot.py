import pytest
from aiogram.filters import Command
from aiogram.methods import AnswerCallbackQuery
from aiogram.methods import SendMessage

from .bot import callback_query_handler
from .bot import callback_query_handler_with_state
from .bot import command_handler
from .bot import dp
from .bot import foo_command_handler
from .bot import message_handler
from .bot import message_handler_with_state
from .bot import message_handler_with_state_data
from .bot import States
from .bot import TestCallbackData
from aiogram_tests.requester import MockedRequester
from aiogram_tests.handler import CallbackQueryHandler
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import CALLBACK_QUERY
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_message_handler():
    requester = MockedRequester(request_handler=MessageHandler(message_handler, auto_mock_success=True))
    calls = await requester.query(MESSAGE.as_object(text="Hello!"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello!"


@pytest.mark.asyncio
async def test_command_handler():
    requester = MockedRequester(request_handler=MessageHandler(command_handler, Command(commands=["start"])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello, new user!"


@pytest.mark.asyncio
async def test_message_handler_with_state():
    requester = MockedRequester(request_handler=MessageHandler(message_handler_with_state, state=States.state))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="Hello, bot!"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello, from state!"


@pytest.mark.asyncio
async def test_callback_query_handler():
    requester = MockedRequester(request_handler=CallbackQueryHandler(callback_query_handler, TestCallbackData.filter()))
    requester.add_result_for(AnswerCallbackQuery, ok=True)
    requester.add_result_for(SendMessage, ok=True)

    callback_query = CALLBACK_QUERY.as_object(
        data=TestCallbackData(id=1, name="John").pack(), message=MESSAGE.as_object(text="Hello world!")
    )
    calls = await requester.query(callback_query)

    answer_text = calls.send_message.fetchone().text
    assert answer_text == "Hello, John"

    requester.add_result_for(AnswerCallbackQuery, ok=True)
    requester.add_result_for(SendMessage, ok=True)
    callback_query = CALLBACK_QUERY.as_object(
        data=TestCallbackData(id=1, name="Mike").pack(), message=MESSAGE.as_object(text="Hello world!")
    )
    calls = await requester.query(callback_query)

    answer_text = calls.send_message.fetchone().text
    assert answer_text == "Hello, Mike"


@pytest.mark.asyncio
async def test_callback_query_handler_with_state():
    requester = MockedRequester(
        request_handler=CallbackQueryHandler(callback_query_handler_with_state, TestCallbackData.filter())
    )

    requester.add_result_for(AnswerCallbackQuery, ok=True)
    requester.add_result_for(SendMessage, ok=True)

    callback_query = CALLBACK_QUERY.as_object(data=TestCallbackData(id=1, name="John").pack())
    calls = await requester.query(callback_query)

    answer_text = calls.answer_callback_query.fetchone().text
    assert answer_text == "Hello, from state!"


@pytest.mark.asyncio
async def test_handler_with_state_data():
    requester = MockedRequester(
        request_handler=MessageHandler(
            message_handler_with_state_data, state=States.state_1, state_data={"info": "this is message handler"}
        )
    )

    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Info from state data: this is message handler"


@pytest.mark.asyncio
async def test_handler_with_fail():
    requester = MockedRequester(request_handler=MessageHandler(foo_command_handler, dp=dp))

    requester.add_result_for(SendMessage, ok=False, description="Have no rights to send a message", error_code=401)
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/foo fail"))
    answer_message = calls.send_message.pop()
    assert answer_message.text == "sorry, i'm failed"
    answer_message = calls.send_message.pop()
    assert answer_message.text == "try to don't failed"
    assert calls.send_message.fetchone() is None

    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/foo"))
    answer_message = calls.send_message.pop()
    assert answer_message.text == "success"
