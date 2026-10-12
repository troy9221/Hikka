"""Expose maintained Telethon under the legacy Hikka import name.

Aliases keep external modules and native modules on the same TL class objects.
No session keys are copied and no additional Telegram login is created.
"""

import importlib
import importlib.abc
import importlib.util
import re
import sys
import telethon
from telethon.extensions import html


class _AliasLoader(importlib.abc.Loader):
    def __init__(self, target):
        self.target = target

    def create_module(self, spec):
        return importlib.import_module(self.target)

    def exec_module(self, module):
        pass


class _AliasFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.startswith("hikkatl."):
            real = "telethon" + fullname[len("hikkatl") :]
            spec = importlib.util.find_spec(real)
            if spec is not None:
                return importlib.util.spec_from_loader(
                    fullname,
                    _AliasLoader(real),
                    is_package=spec.submodule_search_locations is not None,
                )
        return None


def _forum_request(base, fields):
    # Telegram moved forum methods from channels to messages and renamed channel to peer.
    class LegacyForumRequest(base):
        def __init__(self, *args, **kwargs):
            if len(args) > len(fields):
                raise TypeError("Too many positional arguments")
            for name, value in zip(fields, args):
                if name in kwargs:
                    raise TypeError("Duplicate argument: " + name)
                kwargs[name] = value
            if "channel" in kwargs:
                kwargs["peer"] = kwargs.pop("channel")
            from telethon.tl.types import InputChannel, InputPeerChannel

            if isinstance(kwargs.get("peer"), InputChannel):
                value = kwargs["peer"]
                kwargs["peer"] = InputPeerChannel(value.channel_id, value.access_hash)
            super().__init__(**kwargs)

    LegacyForumRequest.__name__ = base.__name__
    return LegacyForumRequest


def install():
    if getattr(telethon, "_hikka_compat_installed", False):
        return
    telethon._hikka_compat_installed = True
    sys.meta_path.insert(0, _AliasFinder())
    for name, module in list(sys.modules.items()):
        if name == "telethon" or name.startswith("telethon."):
            sys.modules["hikkatl" + name[len("telethon") :]] = module
    from telethon.tl.functions import channels, messages

    forum_fields = {
        "CreateForumTopicRequest": (
            "channel",
            "title",
            "icon_color",
            "icon_emoji_id",
            "random_id",
            "send_as",
        ),
        "DeleteTopicHistoryRequest": ("channel", "top_msg_id"),
        "EditForumTopicRequest": (
            "channel",
            "topic_id",
            "title",
            "icon_emoji_id",
            "closed",
            "hidden",
        ),
        "GetForumTopicsRequest": (
            "channel",
            "offset_date",
            "offset_id",
            "offset_topic",
            "limit",
            "q",
        ),
        "GetForumTopicsByIDRequest": ("channel", "topics"),
        "ReorderPinnedForumTopicsRequest": ("channel", "order", "force"),
        "UpdatePinnedForumTopicRequest": ("channel", "topic_id", "pinned"),
    }
    for name, fields in forum_fields.items():
        if not hasattr(channels, name):
            setattr(channels, name, _forum_request(getattr(messages, name), fields))
    original_parse = html.parse
    html.CUSTOM_EMOJIS = True

    def parse(text):
        if html.CUSTOM_EMOJIS:
            text = re.sub(
                r'<emoji\s+document_id=["\'](\d+)["\']\s*>',
                r'<tg-emoji emoji-id="\1">',
                text or "",
            )
            text = text.replace("</emoji>", "</tg-emoji>")
        else:
            text = re.sub(r"</?emoji\b[^>]*>", "", text or "")
        return original_parse(text)

    html.parse = parse
