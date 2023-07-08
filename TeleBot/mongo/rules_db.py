from TeleBot.mongo import db

rulesdb = db.rules

async def is_rules(chat_id: int) -> bool:
    chat = await rulesdb.find_one({"chat_id": chat_id})
    return bool(chat)

async def set_rules(chat_id: int, rules: str):
    await rulesdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"rules": rules}},
        upsert=True
    )

async def clear_rules(chat_id: int):
    await rulesdb.delete_one({"chat_id": chat_id})

async def get_rules(chat_id: int):
    chat = await rulesdb.find_one({"chat_id": chat_id})
    return chat.get("rules") if chat else None