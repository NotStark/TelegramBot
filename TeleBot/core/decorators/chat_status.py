from typing import Any
from pyrogram.types import Message
from TeleBot import app, BOT_ID
from pyrogram.enums import ChatType
from functions import wraps
from TeleBot.core.functions import get_admins, is_invincible
from .lang import get_chat_lang
from ..functions import remove_markdown, handle_exception


async def is_bot_admin(chat_id: int, permission: Any = None) -> bool:
    if permission is None and BOT_ID in await get_admins(chat_id):
        return True
    else:
        chat_member = await app.get_chat_member(chat_id, BOT_ID)
        privileges = (
            chat_member.privileges.__dict__
            if chat_member.privileges is not None
            else {}
        )
        return permission in privileges and privileges[permission]


async def is_user_admin(chat_id: int, user_id: int, permission: Any = None) -> bool:
    if await is_invincible(user_id) or user_id == chat_id:
        return True
    elif permission is None and user_id in await get_admins(chat_id):
        return True
    else:
        chat_member = await app.get_chat_member(chat_id, user_id)
        privileges = (
            chat_member.privileges.__dict__
            if chat_member.privileges is not None
            else {}
        )
        return permission in privileges and privileges[permission]


def admins_stuff(permission: Any = None, bot: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, update):
            if isinstance(update, Message):
                chat_id = update.chat.id
                user_id = (
                    update.sender_chat.id if update.sender_chat else update.from_user.id
                )
                chat_title = update.chat.title
                chat_type = update.chat.type
                alert = False
            else:
                chat_id = update.message.chat.id
                chat_title = update.message.chat.title
                user_id = update.from_user.id
                chat_type = update.message.chat.type
                alert = True

            lang = await get_chat_lang(chat_id)

            async def answer(txt, alert):
                if alert is False:
                    await update.reply(txt)
                else:
                    await update.answer(await remove_markdown(txt), show_alert=True)

            if chat_type == ChatType.PRIVATE:
                await answer(lang.other7, alert)
                return
            if not await is_user_admin(chat_id, user_id, permission=permission):
                if permission is None:
                    txt = lang.other2.format(chat_title)
                    await answer(txt, alert)
                else:
                    txt = lang.other3.format(permission, chat_title)
                    await answer(txt, alert)

                return
            if bot and not await is_bot_admin(chat_id, permission=permission):
                if permission is None:
                    txt = lang.other4.format(chat_title)
                    await answer(txt, alert)
                else:
                    txt = lang.other5.format(permission, chat_title)
                    await answer(txt, alert)
                return

            await handle_exception(client, update, chat_id, alert, lang)

        return wrapper

    return decorator
