from TeleBot.mongo import db
from typing import List, Tuple


blacklistdb = db.blacklist


async def add_blacklist(chat_id: int, words: List[str]):
    chat = await blacklistdb.find_one({"chat_id": chat_id})
    failed = []
    if chat:
        l = chat['words']
        for x in words:
            if x not in l:
                l.appen(x)
            else:
                failed.append(x)
        await blacklistdb.update_one({"chat_id": chat_id}, {"$set": {"words": l}})
        return failed
    await blacklistdb.insert_one({"chat_id": chat_id, 'words': words, 'mode': {'mode' : 1 , 'until' : None}})
    return failed


async def rm_blacklist(chat_id: int, words: List[str]) -> int:
    chat = await blacklistdb.find_one({"chat_id": chat_id})
    success = 0
    if chat:
        l = chat.get("words", [])
        for word in words:
            if word in l:
                l.remove(word)
                success += 1
        await blacklistdb.update_one({"chat_id": chat_id}, {"$set": {"words": l}})
    return success


async def set_blacklist_mode(chat_id: int, details: Tuple[int, int]) -> None:
    chat = await blacklistdb.find_one({"chat_id": chat_id})
    if not chat:
        await add_blacklist(chat_id, words=[])
    await blacklistdb.update_one({"chat_id": chat_id}, {"$set": {'mode': {'mode': details[0], 'until': details[1]}}}, upsert=True)


async def get_blacklist_mode(chat_id: int) -> Tuple[int, int]:
    chat = await blacklistdb.find_one({"chat_id": chat_id})
    if not chat:
        return 1, 0
    mode = chat.get("mode", {})
    return mode.get("mode", 1), mode.get("until", 0)


async def get_emoji(chat_id: int, mode_id: int) -> str:
    mode, until = await get_blacklist_mode(chat_id)
    return "✅" if mode == mode_id else ""


async def is_blacklisted(chat_id: int, word: str) -> bool:
    chat = await blacklistdb.find_one({"chat_id": chat_id})
    if chat:
        l = chat.get("words", [])
        return word in l
    return False


async def get_blacklist(chat_id: int) -> List[str]:
    chat = await blacklistdb.find_one({"chat_id": chat_id})
    if chat:
        return chat.get("words", [])
    return []


async def un_blacklistall(chat_id: int) -> None:
    await blacklistdb.delete_one({"chat_id": chat_id})


async def get_time_emoji(chat_id , until , mode_id):
    mode, until = await get_blacklist_mode(chat_id)
    if mode and mode == mode_id and until == until:
        return "✅"
    else :
        return ""

