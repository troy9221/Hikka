# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/troy9221/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import logging

from aiogram.types import CallbackQuery
from aiogram.types import InlineQuery as AiogramInlineQuery
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.types import Message as AiogramMessage

from .. import utils

logger = logging.getLogger(__name__)


class InlineMessage:
    """Aiogram message, sent via inline bot"""

    def __init__(
        self,
        inline_manager: "InlineManager",  # type: ignore  # noqa: F821
        unit_id: str,
        inline_message_id: str,
    ):
        self.inline_message_id = inline_message_id
        self.unit_id = unit_id
        self.inline_manager = inline_manager
        self._units = inline_manager._units
        self.form = (
            {"id": unit_id, **self._units[unit_id]} if unit_id in self._units else {}
        )

    async def edit(self, *args, **kwargs) -> "InlineMessage":
        if "unit_id" in kwargs:
            kwargs.pop("unit_id")

        if "inline_message_id" in kwargs:
            kwargs.pop("inline_message_id")

        return await self.inline_manager._edit_unit(
            *args,
            unit_id=self.unit_id,
            inline_message_id=self.inline_message_id,
            **kwargs,
        )

    async def delete(self) -> bool:
        return await self.inline_manager._delete_unit_message(
            self,
            unit_id=self.unit_id,
        )

    async def unload(self) -> bool:
        return await self.inline_manager._unload_unit(unit_id=self.unit_id)


class BotInlineMessage:
    """Aiogram message, sent through inline bot itself"""

    def __init__(
        self,
        inline_manager: "InlineManager",  # type: ignore  # noqa: F821
        unit_id: str,
        chat_id: int,
        message_id: int,
    ):
        self.chat_id = chat_id
        self.unit_id = unit_id
        self.inline_manager = inline_manager
        self.message_id = message_id
        self._units = inline_manager._units
        self.form = (
            {"id": unit_id, **self._units[unit_id]} if unit_id in self._units else {}
        )

    async def edit(self, *args, **kwargs) -> "BotMessage":
        if "unit_id" in kwargs:
            kwargs.pop("unit_id")

        if "message_id" in kwargs:
            kwargs.pop("message_id")

        if "chat_id" in kwargs:
            kwargs.pop("chat_id")

        return await self.inline_manager._edit_unit(
            *args,
            unit_id=self.unit_id,
            chat_id=self.chat_id,
            message_id=self.message_id,
            **kwargs,
        )

    async def delete(self) -> bool:
        return await self.inline_manager._delete_unit_message(
            self,
            unit_id=self.unit_id,
            chat_id=self.chat_id,
            message_id=self.message_id,
        )

    async def unload(self, *args, **kwargs) -> bool:
        if "unit_id" in kwargs:
            kwargs.pop("unit_id")

        return await self.inline_manager._unload_unit(
            *args,
            unit_id=self.unit_id,
            **kwargs,
        )


class InlineCall(InlineMessage):
    """Wrapper around aiogram 3.x `CallbackQuery` for inline messages"""

    def __init__(
        self,
        call: CallbackQuery,
        inline_manager: "InlineManager",  # type: ignore  # noqa: F821
        unit_id: str,
    ):
        # Copy attributes from the original callback query
        self.id = getattr(call, "id", None)
        self.from_user = getattr(call, "from_user", None)
        self.message = getattr(call, "message", None)
        self.inline_message_id = getattr(call, "inline_message_id", None)
        self.chat_instance = getattr(call, "chat_instance", None)
        self.data = getattr(call, "data", None)
        self.game_short_name = getattr(call, "game_short_name", None)

        self.original_call = call

        InlineMessage.__init__(
            self,
            inline_manager,
            unit_id,
            getattr(call, "inline_message_id", None),
        )

    async def answer(self, *args, **kwargs):
        """Proxy to original callback query answer"""
        return await self.original_call.answer(*args, **kwargs)


class BotInlineCall(BotInlineMessage):
    """Wrapper around aiogram 3.x `CallbackQuery` for bot messages"""

    def __init__(
        self,
        call: CallbackQuery,
        inline_manager: "InlineManager",  # type: ignore  # noqa: F821
        unit_id: str,
    ):
        # Copy attributes from the original callback query
        self.id = getattr(call, "id", None)
        self.from_user = getattr(call, "from_user", None)
        self.message = getattr(call, "message", None)
        self.chat = getattr(call.message, "chat", None) if call.message else None
        self.chat_instance = getattr(call, "chat_instance", None)
        self.data = getattr(call, "data", None)
        self.game_short_name = getattr(call, "game_short_name", None)

        self.original_call = call

        BotInlineMessage.__init__(
            self,
            inline_manager,
            unit_id,
            call.message.chat.id if call.message else None,
            call.message.message_id if call.message else None,
        )

    async def answer(self, *args, **kwargs):
        """Proxy to original callback query answer"""
        return await self.original_call.answer(*args, **kwargs)


class InlineUnit:
    """InlineManager extension type. For internal use only"""

    def __init__(self):
        """Made just for type specification"""


class BotMessage:
    """Wrapper around aiogram 3.x Message"""

    def __init__(self):
        pass


class InlineQuery:
    """Wrapper around aiogram 3.x InlineQuery"""

    def __init__(self, inline_query: AiogramInlineQuery):
        self.id = getattr(inline_query, "id", None)
        self.from_user = getattr(inline_query, "from_user", None)
        self.query = getattr(inline_query, "query", None)
        self.offset = getattr(inline_query, "offset", None)
        self.chat_type = getattr(inline_query, "chat_type", None)
        self.location = getattr(inline_query, "location", None)

        self.inline_query = inline_query
        self.args = (
            self.inline_query.query.split(maxsplit=1)[1]
            if len(self.inline_query.query.split()) > 1
            else ""
        )

    async def answer(self, results, *args, **kwargs):
        """Proxy to original inline query answer"""
        return await self.inline_query.answer(results, *args, **kwargs)

    @staticmethod
    def _get_res(title: str, description: str, thumb_url: str) -> list:
        return [
            InlineQueryResultArticle(
                id=utils.rand(20),
                title=title,
                description=description,
                input_message_content=InputTextMessageContent(
                    message_text="😶‍🌫️ <i>There is nothing here...</i>",
                    parse_mode="HTML",
                ),
                thumbnail_url=thumb_url,
                thumbnail_width=128,
                thumbnail_height=128,
            )
        ]

    async def e400(self):
        await self.answer(
            self._get_res(
                "🚫 400",
                (
                    "Bad request. You need to pass right arguments, follow module's"
                    " documentation"
                ),
                "https://img.icons8.com/color/344/swearing-male--v1.png",
            ),
            cache_time=0,
        )

    async def e403(self):
        await self.answer(
            self._get_res(
                "🚫 403",
                "You have no permissions to access this result",
                "https://img.icons8.com/external-wanicon-flat-wanicon/344/external-forbidden-new-normal-wanicon-flat-wanicon.png",
            ),
            cache_time=0,
        )

    async def e404(self):
        await self.answer(
            self._get_res(
                "🚫 404",
                "No results found",
                "https://img.icons8.com/external-justicon-flat-justicon/344/external-404-error-responsive-web-design-justicon-flat-justicon.png",
            ),
            cache_time=0,
        )

    async def e426(self):
        await self.answer(
            self._get_res(
                "🚫 426",
                "You need to update Hikka before sending this request",
                "https://img.icons8.com/fluency/344/approve-and-update.png",
            ),
            cache_time=0,
        )

    async def e500(self):
        await self.answer(
            self._get_res(
                "🚫 500",
                "Internal userbot error while processing request. More info in logs",
                "https://img.icons8.com/external-vitaliy-gorbachev-flat-vitaly-gorbachev/344/external-error-internet-security-vitaliy-gorbachev-flat-vitaly-gorbachev.png",
            ),
            cache_time=0,
        )
