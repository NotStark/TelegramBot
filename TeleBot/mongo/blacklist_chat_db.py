from TeleBot.mongo import db

blchatdb = db.blacklistchat

async def add_blacklist_chat(chat_id: int):
    chat = await blchatdb.find_one({"chat_id": chat_id})
    if not chat:
        return await blchatdb.insert_one({"chat_id": chat_id})

async def remove_blacklist_chat(chat_id: int):
    chat = await blchatdb.find_one({"chat_id": chat_id})
    if chat:
        return await blchatdb.delete_one({"chat_id": chat_id})

async def is_blacklisted(chat_id: int) -> bool:
    return await blchatdb.find_one({"chat_id": chat_id}) is not None

async def get_blacklist_chat() -> list:
    return [chat async for chat in blchatdb.find({"chat_id": {"$lt": 0}})]
