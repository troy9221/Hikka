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
    def __init__(self, target):self.target=target
    def create_module(self, spec):return importlib.import_module(self.target)
    def exec_module(self, module):pass

class _AliasFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.startswith('hikkatl.'):
            real='telethon'+fullname[len('hikkatl'):]
            spec=importlib.util.find_spec(real)
            if spec is not None:
                return importlib.util.spec_from_loader(fullname,_AliasLoader(real),is_package=spec.submodule_search_locations is not None)
        return None

def install():
    if getattr(telethon,'_hikka_compat_installed',False):return
    telethon._hikka_compat_installed=True
    sys.meta_path.insert(0,_AliasFinder())
    for name,module in list(sys.modules.items()):
        if name=='telethon' or name.startswith('telethon.'):
            sys.modules['hikkatl'+name[len('telethon'):]]=module
    original_parse=html.parse
    html.CUSTOM_EMOJIS=True
    def parse(text):
        if html.CUSTOM_EMOJIS:
            text=re.sub(r'<emoji\s+document_id=["\'](\d+)["\']\s*>',r'<tg-emoji emoji-id="\1">',text or '')
            text=text.replace('</emoji>','</tg-emoji>')
        else:
            text=re.sub(r'</?emoji\b[^>]*>','',text or '')
        return original_parse(text)
    html.parse=parse
