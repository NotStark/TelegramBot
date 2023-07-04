from lang import get_string
from pyrogram.types import Message
from functools import wraps
from TeleBot.mongo.lang_db import get_lang

def language(func):
    @wraps(func)
    async def wrapper(client, update):
        chat_id = update.chat.id if isinstance(update,Message) else update.message.chat.id
        try:
            language = await get_lang(chat_id)
            language = get_string(language)
        except:
            language = get_string("en")
        return await func(client, update, language)

    return wrapper
