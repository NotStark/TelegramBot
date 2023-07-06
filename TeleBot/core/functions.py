import config
import re
from TeleBot import app
from typing import Callable, Union
from pyrogram import Client
from TeleBot.mongo.disable_db import get_disabled_commands, get_disable_delete
from cachetools import TTLCache
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import ChatWriteForbidden, MessageDeleteForbidden
from time import perf_counter
from pyrogram import enums, types
from TeleBot.mongo.connection_db import get_connected_chat,is_connection_allowed, disconnect_chat


async def is_invincible(user_id : int) -> bool:
  INVINCIBLES  = config.SUDO_USERS + config.DEV_USERS 
  return user_id in INVINCIBLES


admin_cache = TTLCache(maxsize=610, ttl=60*10,timer=perf_counter)  

async def get_admins(chat_id : int):
    if chat_id in admin_cache:
        return admin_cache[chat_id]
    admins = [member.user.id async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS) ]  
    admin_cache[chat_id] =  admins
    return admins


async def get_readable_time(seconds: int) -> str:
    time_string = ""
    if seconds < 0:
        raise ValueError("Input value must be non-negative")

    if seconds < 60:
        time_string = f"{round(seconds)}s"
    else:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            time_string += f"{round(days)}days, "
        if hours > 0:
            time_string += f"{round(hours)}h:"
        time_string += f"{round(minutes)}m:{round(seconds):02d}s"

    return time_string


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


async def connected(message,user_id : int,lang , need_admin = True ):
    chat = message.chat
    if chat.type == enums.ChatType.PRIVATE :
        connected_chat = await get_connected_chat(user_id)
        if not connected_chat:
            return False
        if need_admin is True:
            if await is_invincible(user_id) or user_id in await get_admins(chat.id):
                return connected_chat
            await message.reply(lang.admin34)
        else:
            if await is_connection_allowed(connected_chat):
                return connected_chat
            else:
                if not await is_invincible(user_id):
                    await message.reply(lang.admin35)
                    await disconnect_chat(user_id)
                else:
                    return connected_chat
    else:
        return False
    


async def handle_exception(func: Callable,client : Client, update : Union[types.Message,types.CallbackQuery],chat_id : int , alert : bool, lang):
    try:
        await func(client, update , lang)
    except ChatWriteForbidden:
        await app.leave_chat(chat_id)
    except Exception as e:
        txt = None
        try:
             txt = str(e.MESSAGE)
        except AttributeError:
            txt = str(e)
        if alert is False:
            await update.reply(txt)
        else:
            await update.answer(txt,show_alert=True)
        raise e
    

async def remove_markdown(text: str) -> str:
    patterns = [
        r'\*\*(.*?)\*\*',  
        r'__(.*?)__',      
        r'\*(.*?)\*',      
        r'_(.*?)_',       
        r'`(.*?)`',        
        r'\[(.*?)\]\((.*?)\)', 
        r'~~(.*?)~~',      
        r'\[(.*?)\]\[(.*?)\]',  
        r'\!\[(.*?)\]\((.*?)\)',  
    ]
    for pattern in patterns:
        text = re.sub(pattern, r'\1', text)
    return text
