# Aiogram Tests

***aiogram_tests*** is a testing library for bots written on <a href="https://github.com/aiogram/aiogram">aiogram</a>

## 📚 Simple examples

### Simple handler test

#### Simple bot:

```python
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext

# Please, keep your bot tokens on environments, this code only example
bot = Bot('123456789:AABBCCDDEEFFaabbccddeeff-1234567890')
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message, state: FSMContext) -> None:
    await message.answer(message.text)


if __name__ == '__main__':
    dp.run_polling(bot)


```

#### Test cases:

```python
import pytest

from bot import echo

from aiogram_tests import Requester
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_echo():
    request = Requester(request_handler=MessageHandler(echo))
    calls = await request.query(message=MESSAGE.as_object(text="Hello, Bot!"))
    answer_message = calls.send_messsage.fetchone()
    assert answer_message.text == "Hello, Bot!"

```

### ▶️ <a href='https://github.com/aiogram-tests/aiogram_tests/tree/master/examples'>More</a> examples

