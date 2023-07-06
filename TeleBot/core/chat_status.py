from typing import Any, Tuple
from pyrogram.types import Message
from pyrogram.enums import ChatType
from TeleBot import app, BOT_ID
from TeleBot.core.functions import get_admins, is_invincible
from TeleBot.mongo.connection_db import get_connected_chat


async def is_bot_admin(chat_id: int, permission: Any = None) -> bool:
    if permission is None and BOT_ID in await get_admins(chat_id):
        return True
    else:
        chat_member = await app.get_chat_member(chat_id, BOT_ID)
        privileges = chat_member.privileges.__dict__ if chat_member.privileges is not None else {}
        return permission in privileges and privileges[permission]


async def is_user_admin(chat_id: int, user_id: int, permission: Any = None) -> bool:
    print(chat_id,user_id)
    if await is_invincible(user_id) or user_id == chat_id:
        return True
    elif permission is None and user_id in await get_admins(chat_id):
        return True
    else:
        chat_member = await app.get_chat_member(chat_id, BOT_ID)
        privileges = chat_member.privileges.__dict__ if chat_member.privileges is not None else {}
        return permission in privileges and privileges[permission]


async def do_admins_stuff(message: Message, lang: dict, permission: Any = None, check_bot: bool = False) -> Tuple[bool, int]:
    chat = message.chat
    user_id = message.sender_chat.id if message.sender_chat else message.from_user.id

    if chat.type == ChatType.PRIVATE:
        chat_id = await get_connected_chat(user_id)
        if not chat_id:
            await message.reply(lang.other1)
            return False, 0
        chat_title = (await app.get_chat(chat_id)).title
    else:
        chat_id = chat.id
        chat_title = chat.title

    if not await is_user_admin(chat_id, user_id, permission=permission):
        if permission is None:
            await message.reply(lang.other2.format(chat_title))
        else:
            await message.reply(lang.other3.format(permission, chat_title))
        return False, 0

    if check_bot and not await is_bot_admin(chat_id, permission=permission):
        if permission is None:
            await message.reply(lang.other4.format(chat_title))
        else:
            await message.reply(lang.other5.format(permission, chat_title))
        return False, 0

    return True, chat_id
