from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType

from .exceptions import MethodIsNotCalledError
from .handler.base import RequestHandler
from .utils import camel_case2snake_case


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
            method_name = camel_case2snake_case(r.__api_method__)

            if method_name not in result:
                result[method_name] = CallsList()

            result[method_name].append(self._dict_to_obj(r.dict()))

        return self._generate_result_obj(result)

    def add_result_for(
        self,
        method: TelegramMethod[TelegramType],
        ok: bool,
        result: TelegramType | None = None,
        description: str | None = None,
        error_code: int = 200,
        migrate_to_chat_id: int | None = None,
        retry_after: int | None = None,
    ) -> Response[TelegramType]:
        response = self._handler.add_result_for(
            method=method,
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            migrate_to_chat_id=migrate_to_chat_id,
            retry_after=retry_after,
        )
        return response

    @staticmethod
    def _dict_to_obj(data: dict):
        GeneratedResponse = type("GeneratedResponse", (), data)
        return GeneratedResponse()

    @staticmethod
    def _generate_result_obj(data: dict):
        GeneratedCalls = type("GeneratedCalls", (Calls,), data)
        return GeneratedCalls()
