import re
import config
from TeleBot import app
from cachetools import TTLCache
from pyrogram.enums import ChatMembersFilter
from time import perf_counter
from pyrogram import enums 
from .user_manager import is_user_admin
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






async def connected(message, user_id: int, lang, need_admin=True):
    if message.chat.type == enums.ChatType.PRIVATE:
        connected_chat = await get_connected_chat(user_id)
        if not connected_chat:
            return None

        if need_admin and not await is_user_admin(connected_chat, user_id):
            await message.reply(lang.admin34)
            return None

        chat = await app.get_chat(connected_chat)
        if not await is_connection_allowed(connected_chat) and not await is_invincible(user_id):
            await message.reply(lang.admin35)
            await disconnect_chat(user_id)
            return None

        return chat

    elif need_admin and not await is_user_admin(user_id):
        await message.reply(lang.admin34)
        return None

    return message.chat


          

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
