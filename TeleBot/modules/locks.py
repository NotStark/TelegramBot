from TeleBot import app
from pyrogram import filters
from strings import get_command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from itertools import zip_longest
from TeleBot.core.filter_groups import lock_watcher
from TeleBot.core.functions import prevent_approved
from pyrogram.enums import MessageEntityType
from TeleBot.core import custom_filter
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.log import loggable
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.mongo.locks_db import add_lock, rm_lock , get_locks , get_all_lock_status , lock_types


LOCK_COMMAND = get_command("LOCK_COMMAND")


async def get_buttons(chat_id, user_id):
    dic = await get_all_lock_status(chat_id)
    buttons = []
    rows = zip_longest(*[iter(lock_types.keys())] * 3, fillvalue='')
    for row in rows:
        row_buttons = []
        for option in row:
            status, lockunlock = dic[option]
            row_buttons.append(InlineKeyboardButton(f"{lock_types[option]} {status}", callback_data=f"{lockunlock}_{option}_{user_id}"))
        buttons.append(row_buttons)
    buttons.append([InlineKeyboardButton("ᴄʟᴏꜱᴇ",callback_data=f"admin_close_{user_id}")])
    return InlineKeyboardMarkup(buttons)




@app.on_message(custom_filter.command(commands=LOCK_COMMAND))
@admins_stuff(user=True,bot=False)
async def _lock(client,message,lang):
    user_id = message.from_user.id if message.from_user else 0
    chat_id = message.chat.id
    btns = await get_buttons(chat_id , user_id)
    await message.reply_text(lang.lock1,reply_markup=btns)


@app.on_callback_query(filters.regex("^lock_") | filters.regex("^unlock_"))
@language
@loggable
async def _lockCb(client,query,lang):
    lock_type,user_id = query.data.split("_")[1:]
    chat_id = query.message.chat.id
    if query.from_user.id != int(user_id) :
        return await query.answer(lang.other6,show_alert=True)
    if query.data.startswith("lock_"):
        LOCK = True
        await query.answer(lang.lock2)
        await add_lock(chat_id,lock_type)
        btns = await get_buttons(chat_id , user_id)
    if query.data.startswith("unlock_"):
        LOCK = False
        await query.answer(lang.lock3)
        await rm_lock(chat_id,lock_type)
        btns = await get_buttons(chat_id , user_id)
    await query.message.edit_reply_markup(btns)
    return lang.lock4.format(lock_type,query.from_user.mention) if LOCK else lang.lock5.format(lock_type,query.from_user.mention)
    



@app.on_message(filters.group, group=lock_watcher)
async def _lock_watcher(client, message):
    chat_id = message.chat.id
    ignore = await prevent_approved(message)
    if ignore:
        return

    locks = await get_locks(chat_id)
    if not locks:
        return

    try:
        if 'all' in locks:
            await message.delete()
        if message.sender_chat and 'channel' in locks:
            await message.delete()
        if message.audio and 'audio' in locks:
            await message.delete()
        if message.photo and 'photo' in locks:
            await message.delete()
        if message.document and 'document' in locks:
            await message.delete()
        if message.video and 'video' in locks:
            await message.delete()
        if message.sticker and 'sticker' in locks:
            await message.delete()
        if message.from_user.is_bot and 'bot' in locks:
            await message.delete()
        if message.reply_markup and 'button' in locks:
            await message.delete()
        if message.command and 'command' in locks:
            await message.delete()
        if message.voice and 'voice' in locks:
            await message.delete()
        if message.forward and 'forward' in locks:
            await message.delete()
        if message.forward_from and message.forward_from.is_bot and 'forwardbot' in locks:
            await message.delete()
        if message.forward_from and not message.forward_from.is_bot and 'forwarduser' in locks:
             await message.delete()
        if message.forward_from_chat and 'forwardchannel' in locks:
            await message.delete()
        if message.game and 'game' in locks:
            await message.delete()
        if message.animation and 'gif' in locks:
            await message.delete()
        if message.via_bot and 'inline' in locks:
            await message.delete()
        if message.poll and 'poll' in locks:
            await message.delete()
        if message.text and 'text' in locks:
            await message.delete()
        if message.entities or message.caption_entities:
            iterate = message.entities or message.caption_entities
            for entities in  iterate:
                if entities.type == MessageEntityType.URL and 'url' in locks:
                    await message.delete()  
    except Exception as e:
       return

__commands__ = LOCK_COMMAND
__mod_name__ = "𝙻ᴏᴄᴋꜱ"
__alt_names__ = ["lock"]

__help__ = """
**⸢ʟᴏᴄᴋ sᴏᴍᴇᴛʜɪɴɢ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 
═───────◇───────═
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /locks : ᴛᴏ ʟᴏᴄᴋ.
═───────◇───────═
"""
