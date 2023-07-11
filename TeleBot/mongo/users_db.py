from TeleBot.mongo import db

usersdb = db.users

async def get_served_users() -> list:
    chats = await usersdb.find({"user_id": {"$gt": 0}}).to_list(length=None)
    return [chat["user_id"] for chat in chats]

async def is_served_user(chat_id: int) -> bool:
    chat = await usersdb.find_one({"user_id": chat_id})
    return bool(chat)


async def add_served_user(user_id: int, username: str):
    await usersdb.update_one(
        {"user_id": user_id},
        {"$set": {"username": username}},
        upsert=True
    )

async def remove_served_user(chat_id: int):
    await usersdb.delete_one({"user_id": chat_id})
