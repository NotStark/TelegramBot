from TeleBot.mongo import db

approvedb = db.approve


async def approve_user(chat_id: int, user_id: int):
    await approvedb.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"user_ids": user_id}},
        upsert=True
    )


async def is_approved(chat_id: int, user_id: int) -> bool:
    chat = await approvedb.find_one({"chat_id": chat_id})
    if chat:
        return user_id in chat.get("user_ids", [])
    return False


async def disapprove_user(chat_id: int, user_id: int):
    await approvedb.update_one(
        {"chat_id": chat_id},
        {"$pull": {"user_ids": user_id}}
    )


async def disapprove_all(chat_id: int):
    await approvedb.delete_one({"chat_id": chat_id})


async def approved_users(chat_id: int) -> list:
    chat = await approvedb.find_one({"chat_id": chat_id})
    return chat.get("user_ids", []) if chat else []
