import time 
from TeleBot import app
from typing import List
from strings import get_command
from TeleBot.core import custom_filter
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.log import loggable


DEL_COMMAND = get_command("DEL_COMMAND")
PURGE_COMMAND = get_command("PURGE_COMMAND")

@app.on_message(custom_filter.command(DEL_COMMAND))
@admins_stuff("can_delete_messages",bot=True)
@loggable
async def _del(client, message,lang):
    replied = message.reply_to_message
    chat_id = message.chat.id
    if not replied:
        await message.reply_text(lang.purge1)
        return

    await client.delete_messages(chat_id, replied.id)
    await message.delete()     
    return lang.purge2.format(message.from_user.mention if message.from_user else 'Anon') 


@app.on_message(custom_filter.command(PURGE_COMMAND))
@admins_stuff("can_delete_messages", bot=True)
@loggable
async def _purge(client, message, lang):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text(lang.purge4)
        return

    start_time = time.time()
    purge_message_ids = await get_message_ids_to_purge(replied, message)
    chat_id = message.chat.id
    await delete_messages_in_batches(client, chat_id, purge_message_ids)

    elapsed_time = time.time() - start_time
    await message.reply_text(lang.purge5.format(f"{elapsed_time : 0.2f}"))
    return lang.purge3.format(message.from_user.mention if message.from_user else 'Anon')

async def get_message_ids_to_purge(start_message, end_message) -> List[int]:
    start_id = start_message.message_id
    end_id = end_message.message_id

    if start_id > end_id:
        return []

    message_ids = [start_id]
    for message_id in range(start_id + 1, end_id):
        message_ids.append(message_id)

    return message_ids

async def delete_messages_in_batches(client, chat_id, message_ids):
    batch_size = 100
    total_messages = len(message_ids)
    for i in range(0, total_messages, batch_size):
        batch = message_ids[i : i + batch_size]
        await client.delete_messages(chat_id=chat_id, message_ids=batch, revoke=True)


__commands__ = []
__mod_name__ = "𝙿ᴜʀɢᴇ"
__alt_names__ = ["purges","purging"]

__help__ = """
**⸢ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ɢʀᴏᴜᴘ.⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
๏ /del | /delete : ᴅᴇʟᴇᴛᴇ ᴀ sɪɴɢʟᴇ ᴍᴇssᴀɢᴇ.
๏ /purge : ᴅᴇʟᴇᴛᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴍᴇssᴀɢᴇs.
═───────◇───────═
"""

