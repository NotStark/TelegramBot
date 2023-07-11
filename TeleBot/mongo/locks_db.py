from TeleBot.mongo import db

lockdb = db.locks

lock_types = {
    'all': "ᴀʟʟ", 'channel': 'ᴄʜᴀɴɴᴇʟ', 'audio': 'ᴀᴜᴅɪᴏ', 'bot': 'ʙᴏᴛ', 'button': 'ʙᴜᴛᴛᴏɴ',
    'command': 'ᴄᴏᴍᴍᴀɴᴅ', 'document': 'ᴅᴏᴄᴜᴍᴇɴᴛ', 'forward': 'ғᴏʀᴡᴀʀᴅ', 'forwardbot': 'ғᴏʀᴡᴀʀᴅ ʙᴏᴛ',
    'forwardchannel': 'ғᴏʀᴡᴀʀᴅ ᴄʜᴀɴɴᴇʟ', 'forwarduser': 'ғᴏʀᴡᴀʀᴅ ᴜsᴇʀ', 'game': 'ɢᴀᴍᴇ',
    'gif': 'ɢɪғ', 'inline': 'ɪɴʟɪɴᴇ', 'photo': 'ᴘʜᴏᴛᴏ', 'poll': 'ᴘᴏʟʟ', 'text': 'ᴛᴇxᴛ',
    'url': 'ᴜʀʟ', 'video': 'ᴠɪᴅᴇᴏ', 'voice': 'ᴠᴏɪᴄᴇ', 'sticker': 'sᴛɪᴄᴋᴇʀ'
}


async def add_lock(chat_id: int, lock_type: str):
    await lockdb.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"locks": lock_type}},
        upsert=True
    )


async def rm_lock(chat_id: int, lock_type: str):
    await lockdb.update_one(
        {"chat_id": chat_id},
        {"$pull": {"locks": lock_type}}
    )


async def get_locks(chat_id: int) -> list:
    chat = await lockdb.find_one({"chat_id": chat_id})
    return chat.get("locks", []) if chat else []


async def get_all_lock_status(chat_id: int):
    chat = await lockdb.find_one({"chat_id": chat_id})
    to_return = {}
    
    locks = chat.get('locks', []) if chat else []
    
    to_return = {
        x: ('🔒', 'unlock') if x in locks else ('', 'lock')
        for x in lock_types.keys()
    }
    
    return to_return