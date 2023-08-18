from typing import Optional
from pyrogram.types import Message
from TeleBot import app
from pyrogram.enums import ChatType
from functools import wraps
from TeleBot.mongo.lang_db import get_chat_lang
from pyrogram.errors import ChatWriteForbidden
from ..functions import is_bot_admin , is_user_admin


def admins_stuff(permission: Optional[str] = None, bot: bool = False , user : bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, update):
            from TeleBot.core.functions import remove_markdown
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
            if user and not await is_user_admin(
                chat_id, user_id, permission=permission
            ):
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

            
            try:
                await func(client, update , lang)
            except ChatWriteForbidden:
                await app.leave_chat(chat_id)
            except Exception as e:
                try:
                    txt = str(e.MESSAGE)
                except AttributeError:
                    txt = str(e)
                if alert is False:
                    await update.reply(txt)
                else:
                    await update.answer(txt,show_alert=True)
                raise e

        return wrapper

    return decorator
