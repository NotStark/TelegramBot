from TeleBot.mongo import db

logchannel = db.log_channel
logchannels = {}


async def set_log(chat_id: int, channel_id: int):
    chat = await logchannel.find_one({"chat_id": chat_id})
    if not chat:
        await logchannel.insert_one({"chat_id": chat_id, "channel_id": channel_id})
    else:
        await logchannel.update_one({"chat_id": chat_id}, {"$set": {"channel_id": channel_id}})
    logchannels[chat_id] = channel_id


async def unset_log(chat_id: int):
    result = await logchannel.delete_one({"chat_id": chat_id})
    if result.deleted_count > 0:
        logchannels.pop(chat_id, None)
        return True, logchannels.get(chat_id)
    return False, None


async def get_log_channel(chat_id: int):
    channel = logchannels.get(chat_id)
    if channel is not None:
        return channel

    chat = await logchannel.find_one({"chat_id": chat_id})
    channel_id = chat['channel_id'] if chat else None
    logchannels[chat_id] = channel_id
    return channel_id
