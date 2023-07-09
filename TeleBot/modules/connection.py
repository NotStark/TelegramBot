from TeleBot import app
from pyrogram import filters, errors, enums
from strings import get_command
from TeleBot.mongo.connection_db import (
    allow_connect,
    is_connection_allowed,
    get_connected_chat,
    disconnect_chat,
    connect_chat,
)
from TeleBot.core.functions import get_admins
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TeleBot.core import custom_filter
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.log import loggable
from TeleBot.core.decorators.lang import language
from  TeleBot.core.functions import remove_markdown


ALLOWCONNECT_COMMAND = get_command("ALLOWCONNECT_COMMAND")
CONNECTION_COMMAND = get_command("CONNECTION_COMMAND")
DISCONNECT_COMMAND = get_command("DISCONNECT_COMMAND")
HELPCONNECT_COMMAND = get_command("HELPCONNECT_COMMAND")
CONNECT_COMMAND = get_command("CONNECT_COMMAND")

@app.on_message(custom_filter.command(ALLOWCONNECT_COMMAND))
@admins_stuff(user=True,bot=False)
@loggable
async def _allow_connect(client, message,lang):
    chat = message.chat
    user = message.from_user.mention if message.from_user else 'Anon'
    if len(message.command) < 2:
        result = is_connection_allowed(chat.id)
        if not result:
            await message.reply(
                lang.connect1
            )
        else:
            await message.reply(
                lang.connect2
            )
        return
    arg = message.command[1].lower()
    if arg == "on":
        await allow_connect(chat.id, True)
        await message.reply(lang.connect3)
        return lang.connect5.format("ᴛʀᴜᴇ",user)
    elif arg == "off":
        await allow_connect(chat.id, False)
        await message.reply(lang.connect4)
        return lang.connect5.format("ғᴀʟsᴇ",user)
    else:
        await message.reply(lang.connect6)
        return 


@app.on_message(custom_filter.command(CONNECTION_COMMAND))
@language
async def _connection(client, message,lang):
    if message.chat.type != enums.ChatType.PRIVATE:
        return await message.reply(lang.other13)
    user_id = message.from_user.id
    connected_chat = await get_connected_chat(user_id)
    if connected_chat:
        chat_title = (await client.get_chat(connected_chat)).title
        await message.reply(lang.connect7.format(chat_title))
    else:
        await message.reply(lang.connect8)


@app.on_message(custom_filter.command(DISCONNECT_COMMAND))
@language
async def _disconnect(client, message,lang):
    user_id = message.from_user.id
    if not await disconnect_chat(user_id):
        await message.reply(lang.connect8)
    else:
        await message.reply(lang.connect9)


@app.on_message(custom_filter.command(HELPCONNECT_COMMAND))
@language
async def help_connect(client, message,lang):
    """
    TODO
    """


@app.on_message(custom_filter.command(CONNECT_COMMAND))
@language
async def _connect(client, message,lang):
    if message.sender_chat:
        return
    if len(message.command) < 2:
        return await message.reply(lang.connect10)
    chat_id = message.command[1]
    try:
        chat_id = int(chat_id)
    except ValueError:
        return await message.reply(lang.connect11)
    try:
        chat = await client.get_chat(chat_id)
    except errors.BadRequest as e:
        if e.MESSAGE == "CHAT_ID_INVALID":
            return await message.reply(lang.connect12)
        return await message.reply(e.MESSAGE)
    user_id = message.from_user.id
    await message.reply(
        lang.connect13.format(chat.title),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang.btn17,
                        callback_data=f"connect_admin_{chat_id}_{user_id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        lang.btn18,
                        callback_data=f"connect_user_{chat_id}_{user_id}",
                    )
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("^connect_"))
@language
async def _connectCb(client, query,lang):
    callback_type, chat_id, user_id = query.data.split("_")[1:]
    from_user = query.from_user
    if from_user.id != int(user_id):
        return await query.answer(lang.other6, show_alert=True)
    chat = await client.get_chat(int(chat_id))
    if callback_type == "admin":
        if from_user.id not in await get_admins(chat.id):
            return await query.answer(
                lang.connect14
            )
        await connect_chat(int(user_id), chat_id)
        return await query.message.edit(
            lang.connect15.format(chat.title)
        )
    if callback_type == "user":
        result = await is_connection_allowed(chat.id)
        if not result:
            await query.answer(
                await remove_markdown(lang.connect16.format(chat.title)),
                show_alert=True,
            )
            return
        await connect_chat(int(user_id), chat.id)
        return await query.message.edit(
            lang.connect17.format(chat.title)
        )

__commands__ = (
    ALLOWCONNECT_COMMAND +
    CONNECTION_COMMAND +
    DISCONNECT_COMMAND +
    HELPCONNECT_COMMAND +
    CONNECT_COMMAND 
   )

__mod_name__ = "𝙲ᴏɴɴᴇᴄᴛɪᴏɴ"
__alt_name__ = ["connect","connections"]


__help__ = """
**⸢ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ ᴄʜᴀᴛ ᴛᴏ ᴀ ɢʀᴏᴜᴘ ᴅᴏ /helpconnect ᴛᴏ ᴋɴᴏᴡ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ ᴄᴏᴍᴍᴀɴᴅꜱ⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
๏ /connect: ᴄᴏɴɴᴇᴄᴛꜱ ᴛᴏ ᴄʜᴀᴛ (ᴄᴀɴ ʙᴇ ᴅᴏɴᴇ ɪɴ ᴀ ɢʀᴏᴜᴘ ʙʏ /connect ᴏʀ /connect <chat id> ɪɴ ᴘᴍ)
๏ /connection: ʟɪꜱᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀᴛꜱ
๏ /disconnect: ᴅɪꜱᴄᴏɴɴᴇᴄᴛ ғʀᴏᴍ ᴀ ᴄʜᴀᴛ
๏ /helpconnect: ʟɪꜱᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴛʜᴀᴛ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ʀᴇᴍᴏᴛᴇʟʏ

「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
❂ /allowconnect <yes/no>: ᴀʟʟᴏᴡ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴀ ᴄʜᴀᴛ
═───────◇───────═
"""
