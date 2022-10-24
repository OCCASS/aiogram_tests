import pytest
from aiogram import types
from pydantic import ValidationError

import aiogram_pytest.types.dataset as dataset
from aiogram_pytest.types.dataset import DatasetItem


def test_as_object():
    dataset_item = DatasetItem({"firstArg": 1, "secondArg": 2})
    assert dataset_item.as_object() == {"firstArg": 1, "secondArg": 2}
    assert dataset_item.as_object(firstArg=3) == {"firstArg": 3, "secondArg": 2}
    assert dataset_item.as_object(thirdArg=3) == {"firstArg": 1, "secondArg": 2, "thirdArg": 3}


def test_as_object_converting():
    dataset_item = DatasetItem(
        {
            "id": 12345678,
            "is_bot": False,
            "first_name": "FirstName",
            "last_name": "LastName",
            "username": "username",
        },
        model=types.User,
    )
    assert dataset_item.as_object() == types.User(
        id=12345678, is_bot=False, first_name="FirstName", last_name="LastName", username="username"
    )
    assert dataset_item.as_object(first_name="EditedFirstName") == types.User(
        id=12345678, is_bot=False, first_name="EditedFirstName", last_name="LastName", username="username"
    )
    assert dataset_item.as_object(language_code="ru") == types.User(
        id=12345678,
        is_bot=False,
        first_name="EditedFirstName",
        last_name="LastName",
        username="username",
        language_code="ru",
    )


def test_as_object_converting_with_nesting():
    dataset_item = DatasetItem(
        {
            "message_id": 11223,
            "from": {
                "id": 12345678,
                "is_bot": False,
                "first_name": "FirstName",
                "last_name": "LastName",
                "username": "username",
            },
            "chat": {
                "id": 12345678,
                "first_name": "FirstName",
                "last_name": "LastName",
                "username": "username",
                "type": "private",
            },
            "date": 1508709711,
            "text": "Hi, world!",
        },
        model=types.Message,
    )
    assert (
        dataset_item.as_object().to_python()
        == types.Message(
            message_id=11223,
            from_user=types.User(
                id=12345678, is_bot=False, first_name="FirstName", last_name="LastName", username="username"
            ),
            chat=types.Chat(
                id=12345678,
                first_name="FirstName",
                last_name="LastName",
                username="username",
                type=types.ChatType.PRIVATE,
            ),
            date=1508709711,
            text="Hi, world!",
        ).to_python()
    )


def test_converting_all_dataset_items_to_model():
    all_items = (getattr(dataset, name) for name in dir(dataset))
    for item in all_items:
        if not isinstance(item, DatasetItem):
            continue

        with pytest.raises(ValidationError):
            item.as_object()
