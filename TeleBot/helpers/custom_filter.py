import re
from config import HANDLERS
from typing import Union, List
from pyrogram import  filters
from pyrogram.enums import ChatType
from TeleBot.helpers.functions import disable_action


def command(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = HANDLERS, disable: bool = True, group_only : bool  = False):
    commands = commands if isinstance(commands, list) else [commands]
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]

    async def handler(flt, client, message):
        text = message.text or message.caption
        message.command = None

        if not text:
            return False
        text = text.lower()

        pattern = r"^(?:{})({})(?:@[^\s]+)?(?:\s|$)".format("|".join(re.escape(prefix) for prefix in prefixes), "|".join(map(re.escape, commands)))
        match = re.search(pattern, text)

        if match:
            command = match.group(1)
            args = text[match.end():].strip().split()
            message.command = [command] + args
            
            if group_only and message.chat.type == ChatType.PRIVATE:
                await message.reply("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴀꜱ ᴍᴀᴅᴇ ᴜᴘ ꜰᴏʀ ɢʀᴏᴜᴘ ɴᴏᴛ ꜰᴏʀ ᴘʀɪᴠᴀᴛᴇ")
                return False
            
            if disable :
                result = await disable_action(message, command)
                if result is False:
                    return False

            return True

        return False

    return filters.create(handler, "CommandFilter", commands=commands, prefixes=prefixes)