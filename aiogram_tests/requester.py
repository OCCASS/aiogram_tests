from aiogram.utils.helper import Helper
from aiogram.utils.helper import Item

from .exceptions import MethodIsNotCalledError
from .handler.base import RequestHandler
from .utils import camel_case2snake_case


class RequestType(Helper):
    @classmethod
    def get_from_lowercase(cls, lower_case: str):
        for item in cls.all():
            if item == lower_case.upper():
                return item

        return None

    ADD_STICKER_TO_SET = Item()
    ANSWER_CALLBACK_QUERY = Item()
    ANSWER_INLINE_QUERY = Item()
    ANSWER_PRE_CHECKOUT_QUERY = Item()
    ANSWER_SHIPPING_QUERY = Item()
    ANSWER_WEB_APP_QUERY = Item()
    APPROVE_CHAT_JOIN_REQUEST = Item()
    BAN_CHAT_MEMBER = Item()
    BAN_CHAT_SENDER_CHAT = Item()
    CHECK_AUTH_WIDGET = Item()
    COPY_MESSAGE = Item()
    CREATE_CHAT_INVITE_LINK = Item()
    CREATE_INVOICE_LINK = Item()
    CREATE_NEW_STICKER_SET = Item()
    DECLINE_CHAT_JOIN_REQUEST = Item()
    DELETE_CHAT_PHOTO = Item()
    DELETE_CHAT_STICKER_SET = Item()
    DELETE_MESSAGE = Item()
    DELETE_MY_COMMANDS = Item()
    DELETE_STICKER_FROM_SET = Item()
    DELETE_WEBHOOK = Item()
    DOWNLOAD_FILE = Item()
    DOWNLOAD_FILE_BY_ID = Item()
    EDIT_CHAT_INVITE_LINK = Item()
    EDIT_MESSAGE_CAPTION = Item()
    EDIT_MESSAGE_LIVE_LOCATION = Item()
    EDIT_MESSAGE_MEDIA = Item()
    EDIT_MESSAGE_REPLY_MARKUP = Item()
    EDIT_MESSAGE_TEXT = Item()
    EXPORT_CHAT_INVITE_LINK = Item()
    FORWARD_MESSAGE = Item()
    GET = Item()
    GET_CHAT = Item()
    GET_CHAT_ADMINISTRATORS = Item()
    GET_CHAT_MEMBER = Item()
    GET_CHAT_MEMBER_COUNT = Item()
    GET_CHAT_MEMBERS_COUNT = Item()
    GET_CHAT_MENU_BUTTON = Item()
    GET_CURRENT = Item()
    GET_CUSTOM_EMOJI_STICKERS = Item()
    GET_FILE = Item()
    GET_FILE_URL = Item()
    GET_GAME_HIGH_SCORES = Item()
    GET_ME = Item()
    GET_MY_COMMANDS = Item()
    GET_MY_DEFAULT_ADMINISTRATOR_RIGHTS = Item()
    GET_NEW_SESSION = Item()
    GET_SESSION = Item()
    GET_STICKER_SET = Item()
    GET_UPDATES = Item()
    GET_USER_PROFILE_PHOTOS = Item()
    GET_WEBHOOK_INFO = Item()
    KICK_CHAT_MEMBER = Item()
    LEAVE_CHAT = Item()
    PIN_CHAT_MESSAGE = Item()
    PROMOTE_CHAT_MEMBER = Item()
    REQUEST = Item()
    REQUEST_TIMEOUT = Item()
    RESTRICT_CHAT_MEMBER = Item()
    REVOKE_CHAT_INVITE_LINK = Item()
    SEND_ANIMATION = Item()
    SEND_AUDIO = Item()
    SEND_CHAT_ACTION = Item()
    SEND_CONTACT = Item()
    SEND_DICE = Item()
    SEND_DOCUMENT = Item()
    SEND_FILE = Item()
    SEND_GAME = Item()
    SEND_INVOICE = Item()
    SEND_LOCATION = Item()
    SEND_MEDIA_GROUP = Item()
    SEND_MESSAGE = Item()
    SEND_PHOTO = Item()
    SEND_POLL = Item()
    SEND_STICKER = Item()
    SEND_VENUE = Item()
    SEND_VIDEO = Item()
    SEND_VIDEO_NOTE = Item()
    SEND_VOICE = Item()
    SET_CHAT_ADMINISTRATOR_CUSTOM_TITLE = Item()
    SET_CHAT_DESCRIPTION = Item()
    SET_CHAT_MENU_BUTTON = Item()
    SET_CHAT_PERMISSIONS = Item()
    SET_CHAT_PHOTO = Item()
    SET_CHAT_STICKER_SET = Item()
    SET_CHAT_TITLE = Item()
    SET_CURRENT = Item()
    SET_GAME_SCORE = Item()
    SET_MY_COMMANDS = Item()
    SET_MY_DEFAULT_ADMINISTRATOR_RIGHTS = Item()
    SET_PASSPORT_DATA_ERRORS = Item()
    SET_STICKER_POSITION_IN_SET = Item()
    SET_STICKER_SET_THUMB = Item()
    SET_WEBHOOK = Item()
    STOP_MESSAGE_LIVE_LOCATION = Item()
    STOP_POLL = Item()
    UNBAN_CHAT_MEMBER = Item()
    UNBAN_CHAT_SENDER_CHAT = Item()
    UNPIN_ALL_CHAT_MESSAGES = Item()
    UNPIN_CHAT_MESSAGE = Item()
    UPLOAD_STICKER_FILE = Item()


class CallsList(list):
    def fetchone(self):
        if len(self) > 0:
            return self[-1]
        else:
            return None

    def fetchall(self):
        return self


class Calls:
    def _get_attributes(self):
        res = []
        for item in dir(self):
            if item.startswith("_") or item.endswith("_"):
                continue

            if not callable(getattr(self, item)):
                res.append(item)

        return tuple(res)

    def __getattr__(self, item):
        if item in dir(self):
            return getattr(self, item)
        else:
            raise MethodIsNotCalledError(
                "method '%s' is not called by bot, so you cant to get this attribute. Called methods: %s"
                % (item, self._get_attributes())
            )


class MockedBot:
    def __init__(self, request_handler: RequestHandler):
        self._handler: RequestHandler = request_handler

    async def query(self, *args, **kwargs) -> Calls:
        try:
            await self._handler(*args, **kwargs)
        except TypeError as e:
            raise AttributeError("incorrect argument name. %s" % e)

        requests = self._handler.bot.session.requests
        result = {}
        for r in requests:
            method_name = camel_case2snake_case(r.method)

            if method_name not in result:
                result[method_name] = CallsList()

            result[method_name].append(self._dict_to_obj(r.data))

        return self._generate_result_obj(result)

    @staticmethod
    def _dict_to_obj(data: dict):
        GeneratedResponse = type("GeneratedResponse", (), data)
        return GeneratedResponse()

    @staticmethod
    def _generate_result_obj(data: dict):
        GeneratedCalls = type("GeneratedCalls", (Calls,), data)
        return GeneratedCalls()
