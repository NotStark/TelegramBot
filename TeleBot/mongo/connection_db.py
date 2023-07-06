from TeleBot.mongo import db
from TeleBot.mongo.chats_db import chatsdb
from TeleBot import app

connectiondb = db.connections
connections = {}


async def allow_connect(chat_id: int, allow: bool):
    await chatsdb.update_one({"chat_id": chat_id}, {"$set": {"allow_connection": allow}}, upsert=True)


async def is_connection_allowed(chat_id: int):
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if chat and "allow_connection" in chat:
        return chat["allow_connection"]
    return False


async def connect_chat(user_id: int, chat_id: int):
    connections[user_id] = chat_id
    await connectiondb.update_one(
        {"user_id": user_id},
        {"$set": {"chat_id": chat_id, "connection": True}},
        upsert=True
    )


async def disconnect_chat(user_id: int) -> bool:
    connections.pop(user_id, None)
    result = await connectiondb.update_one(
        {"user_id": user_id},
        {"$set": {"connection": False}}
    )
    return result.modified_count > 0


async def get_connected_chat(user_id: int):
    chat = connections.get(user_id)
    if chat is not None:
        return chat

    user = await connectiondb.find_one({"user_id": user_id})
    chat_id = user['chat_id'] if user else None
    connections[user_id] = chat_id
    return chat_id
