import re
from config import HANDLERS
from typing import Union, List
from pyrogram import  filters
from TeleBot import BOT_USERNAME as username
from .functions import disable_action


def nncommand(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = HANDLERS, disable: bool = True ):
    commands = commands if isinstance(commands, list) else [commands]
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]

    async def handler(flt, client, message):
        text = message.text or message.caption
        message.command = None

        if not text:
            return False
        text = text.lower()
        print(flt.commands,flt.prefixes)

        pattern = r"^(?:{})({})(?:@[^\s]+)?(?:\s|$)".format("|".join(re.escape(prefix) for prefix in prefixes), "|".join(map(re.escape, commands)))
        match = re.search(pattern, text)

        if match:
            command = match.group(1)
            args = text[match.end():].strip().split()
            message.command = [command] + args
            
            if disable :
                result = await disable_action(message, command)
                if result is False:
                    return False

            return True

        return False

    return filters.create(handler, "CommandFilter", commands=commands, prefixes=prefixes)




def command(commands: Union[str, List[str]],prefixes: Union[str, List[str]] = HANDLERS, disable : bool : True, case_sensitive: bool = False):
    """
    https://github.com/pyrogram/pyrogram/blob/efac17198b5fcaec1c2628c4bba0c288a4d617d4/pyrogram/filters.py#L750
    """
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

    async def handler(flt, client, message):
        text = message.text or message.caption
        message.command = None

        if not text:
            return False

        for prefix in flt.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix):]

            for cmd in flt.commands:
                if not re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
                                flags=re.IGNORECASE if not flt.case_sensitive else 0):
                    continue

                without_command = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1,
                                         flags=re.IGNORECASE if not flt.case_sensitive else 0)

                message.command = [cmd] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in command_re.finditer(without_command)
                ]
                if disable :
                    result = await disable_action(message, command)
                    if result is False:
                        return False

                return True

        return False

    commands = commands if isinstance(commands, list) else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return filters.create(
        handler,
        "CommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )
