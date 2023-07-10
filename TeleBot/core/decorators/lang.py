from TeleBot import app
from pyrogram.types import Message
from functools import wraps
from TeleBot.mongo.lang_db import get_chat_lang
from pyrogram.errors import ChatWriteForbidden


def language(func):
    @wraps(func)
    async def wrapper(client, update):
        chat_id = update.chat.id if isinstance(update, Message) else update.message.chat.id
        alert = False if isinstance(update, Message) else True
        language = await get_chat_lang(chat_id)
        try:
            await func(client, update , language)
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



