from typing import Any, Tuple
from pyrogram.types import Message
from pyrogram.enums import ChatType
from TeleBot import app, BOT_ID
from TeleBot.mongo.connection_db import get_connected_chat
from TeleBot.helpers.functions import get_admins, is_invincible


async def is_admin(message: Message, permission: Any = None, check_bot: bool = False) -> Tuple[bool, int]:
    chat = message.chat
    user_id = message.sender_chat.id if message.sender_chat else message.from_user_id

    if chat.type == ChatType.PRIVATE:
        chat_id = await get_connected_chat(user_id)
        if not chat_id:
            await message.reply("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴀꜱ ᴍᴀᴅᴇ ᴜᴘ ꜰᴏʀ ɢʀᴏᴜᴘꜱ ɴᴏᴛ ꜰᴏʀ ᴘʀɪᴠᴀᴛᴇ")
            return False, 0
    else:
        chat_id = chat.id

    if permission is None:
        admins = await get_admins(chat_id)
        if check_bot and BOT_ID not in admins:
            return False, chat_id
        if user_id not in admins and not await is_invincible(user_id):
            return False, chat_id
    else:
        if check_bot:
            chat_member = await app.get_chat_member(chat_id, BOT_ID)
            privileges = chat_member.privileges.__dict__ if chat_member.privileges is not None else {}
            if permission not in privileges or not privileges[permission]:
                return False, chat_id
            
        if await is_invincible(user_id):
            return True, chat_id
        chat_member = await app.get_chat_member(chat_id, user_id)
        privileges = chat_member.privileges.__dict__ if chat_member.privileges is not None else {}
        if permission not in privileges or not privileges[permission]:
            return False, chat_id

    return True, chat_id

