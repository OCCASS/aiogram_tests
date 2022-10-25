import pytest
from aiogram.filters import Command
from test_bot import callback_query_handler
from test_bot import callback_query_handler_with_state
from test_bot import command_handler
from test_bot import message_handler
from test_bot import message_handler_with_state
from test_bot import message_handler_with_state_data
from test_bot import States
from test_bot import TestCallbackData

from aiogram_tests import Requester
from aiogram_tests.handler import CallbackQueryHandler
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import CALLBACK_QUERY
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_message_handler():
    requester = Requester(request_handler=MessageHandler(message_handler))
    calls = await requester.query(MESSAGE.as_object(text="Hello!"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello!"


@pytest.mark.asyncio
async def test_command_handler():
    requester = Requester(request_handler=MessageHandler(command_handler, Command(commands=["start"])))
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello, new user!"


@pytest.mark.asyncio
async def test_message_handler_with_state():
    requester = Requester(request_handler=MessageHandler(message_handler_with_state, state=States.state))
    calls = await requester.query(MESSAGE.as_object(text="Hello, bot!"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Hello, from state!"


@pytest.mark.asyncio
async def test_callback_query_handler():
    requester = Requester(request_handler=CallbackQueryHandler(callback_query_handler, TestCallbackData.filter()))

    callback_query = CALLBACK_QUERY.as_object(
        data=TestCallbackData(id=1, name="John").pack(), message=MESSAGE.as_object(text="Hello world!")
    )
    calls = await requester.query(callback_query)

    answer_text = calls.send_message.fetchone().text
    assert answer_text == "Hello, John"

    callback_query = CALLBACK_QUERY.as_object(
        data=TestCallbackData(id=1, name="Mike").pack(), message=MESSAGE.as_object(text="Hello world!")
    )
    calls = await requester.query(callback_query)

    answer_text = calls.send_message.fetchone().text
    assert answer_text == "Hello, Mike"


@pytest.mark.asyncio
async def test_callback_query_handler_with_state():
    requester = Requester(
        request_handler=CallbackQueryHandler(callback_query_handler_with_state, TestCallbackData.filter())
    )

    callback_query = CALLBACK_QUERY.as_object(data=TestCallbackData(id=1, name="John").pack())
    calls = await requester.query(callback_query)

    answer_text = calls.answer_callback_query.fetchone().text
    assert answer_text == "Hello, from state!"


@pytest.mark.asyncio
async def test_handler_with_state_data():
    requester = Requester(
        request_handler=MessageHandler(
            message_handler_with_state_data, state=States.state_1, state_data={"info": "this is message handler"}
        )
    )

    calls = await requester.query(MESSAGE.as_object())
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Info from state data: this is message handler"
