import re
from config import HANDLERS
from typing import Union, List
from pyrogram import  filters
from TeleBot.mongo.disable_db import get_disabled_commands, get_disable_delete
from pyrogram.errors import MessageDeleteForbidden


async def disable_action(message, command):
    chat_id = message.chat.id
    sender_id = message.sender_chat.id if message.sender_chat else message.from_user.id

    if await is_invincible(sender_id):
        return True
    
    disable_cmds = await get_disabled_commands(chat_id)
    
    if command in disable_cmds:
        if await get_disable_delete(chat_id):
            admins = await get_admins(chat_id)
            if sender_id not in admins and sender_id != chat_id:
                try:
                    await message.delete()
                except MessageDeleteForbidden:
                    pass
                else:
                    return False
                
            return False
        else:
            return False
    
    return True

def command(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = HANDLERS, disable: bool = True ):
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
            
            if disable :
                result = await disable_action(message, command)
                if result is False:
                    return False

            return True

        return False

    return filters.create(handler, "CommandFilter", commands=commands, prefixes=prefixes)


from .functions import is_invincible