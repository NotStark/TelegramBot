from TeleBot.mongo import db
from strings import get_string

langdb = db.language
langm = {}


async def get_lang(chat_id: int) -> str:
    mode = langm.get(chat_id)
    if not mode:
        lang = await langdb.find_one({"chat_id": chat_id})
        if not lang:
            langm[chat_id] = "en"
            return "en"
        langm[chat_id] = lang["lang"]
        return lang["lang"]
    return mode


async def set_lang(chat_id: int, lang: str):
    langm[chat_id] = lang
    await langdb.update_one(
        {"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True
    )


async def get_chat_lang(chat_id: int):
    try:
        language = await get_lang(chat_id)
    except:
        language = "en"
    return get_string(language)