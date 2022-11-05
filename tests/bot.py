from aiogram import Dispatcher
from aiogram import types
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.filters import CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


class TestCallbackData(CallbackData, prefix="test_callback_data"):
    id: int
    name: str


dp = Dispatcher(storage=MemoryStorage())


class States(StatesGroup):
    state = State()
    state_1 = State()


@dp.message(Command(commands=["start"]))
async def command_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer("Hello, new user!")


@dp.message(States.state)
async def message_handler_with_state(message: types.Message, state: FSMContext) -> None:
    await message.reply("Hello, from state!")


@dp.message(States.state_1)
async def message_handler_with_state_data(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(f'Info from state data: {data["info"]}')


@dp.callback_query(TestCallbackData.filter())
async def callback_query_handler(
    callback_query: types.CallbackQuery, callback_data: TestCallbackData, state: FSMContext
) -> None:
    name = callback_data.name
    await callback_query.message.answer(f"Hello, {name}")


@dp.callback_query(States.state, TestCallbackData.filter())
async def callback_query_handler_with_state(
    callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext
) -> None:
    await callback_query.answer("Hello, from state!")


@dp.message(Command(commands="foo"))
async def foo_command_handler(m: types.Message, command: CommandObject):
    if command.args == "fail":
        try:
            return await m.answer("try to don't failed")
        except TelegramAPIError:
            return await m.answer("sorry, i'm failed")
    else:
        await m.answer("success")


@dp.message()
async def message_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer(message.text)
