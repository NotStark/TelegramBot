from TeleBot.mongo import db

chatsdb = db.chats

async def get_served_chats() -> list:
    chats = await usersdb.find({"chat_id": {"$lt": 0}}).to_list(length=None)
    return [chat["chat_id"] for chat in chats]

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    return bool(chat)

async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def remove_served_chat(chat_id: int):
    return await chatsdb.delete_one({"chat_id": chat_id})
