from strings import get_string
from pyrogram.types import Message
from functools import wraps
from TeleBot.mongo.lang_db import get_lang
from .chat_status import handle_exception


def language(func):
    @wraps(func)
    async def wrapper(client, update):
        chat_id = update.chat.id if isinstance(update, Message) else update.message.chat.id
        alert = False if isinstance(update, Message) else True
        language = await get_chat_lang(chat_id)
        return await handle_exception(func, client, update, chat_id, alert, language)

    return wrapper


async def get_chat_lang(chat_id: int):
    try:
        language = await get_lang(chat_id)
    except:
        language = "en"
    return get_string(language)
