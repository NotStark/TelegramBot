from typing import Any
from pyrogram.types import Message
from pyrogram.enums import ChatType
from functools import wraps
from ..user_manager import is_bot_admin , is_user_admin
from .lang import get_chat_lang
from ..functions import remove_markdown, handle_exception



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
            if user and not await is_user_admin(chat_id, user_id, permission=permission):
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

            await handle_exception(func , client, update, chat_id, alert, lang)

        return wrapper

    return decorator
