import logging
import aiohttp
import asyncio
import warnings

from logging import LogRecord, Formatter
from typing import Callable

from .webhooks import create_webhook

class WebhookHandler(logging.Handler):
    def __init__(self, *, webhook_url: str, session: aiohttp.ClientSession):
        self.formatter = Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        self.__webhook = create_webhook(webhook_url, session)
        self.hook_url = webhook_url
        self.handle_webhook_func = self._default_handle
        self.force_debug = False
        self.level = logging.NOTSET
        self.is_locked = False
        self._warned_no_level_set = False
        self.ignore_warnings = False

    def handle(self, record: LogRecord) -> str:
        if self.level == logging.NOTSET and self._warned_no_level_set is False and self.ignore_warnings is False:
            warnings.warn("No Logging Level has been set. Please set one using handler.setLevel")
            self._warned_no_level_set = True

        asyncio.create_task(self.handle_webhook_func(record))
        return record

    async def _default_handle(self, record: LogRecord):
        text = "```json\n{}\n```".format(self.formatter.format(record))
        if self.is_locked is True:
            return
        if self.level == logging.DEBUG and self.force_debug is False:
            self.is_locked = True
            raise ValueError((
                "Cannot Send Webhook: You have set the logging level to DEBUG. This is disadvised due to spam and ratelimits."
                " Please use a higher level of debugging such as INFO. If you still want to use DEBUG, please set your handler's"
                " force_debug attribute to True. Example: handler.force_debug = True"
            ))
        return await self.__webhook.send(text)


    def setCustomHandle(self, func: Callable):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Custom Handle must be a coroutine")

        self.handle_webhook_func = func