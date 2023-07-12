
from TeleBot import app
from pyrogram import filters
from strings import get_command
from pyrogram.enums import ChatMemberStatus
from TeleBot.core import custom_filter
from TeleBot.mongo.notes_db import (
    save_note,
    clear_note,
    get_notes_list,
    remove_all_notes,
    is_note_exist,
)
from TeleBot.core.functions import get_note_tpye, send_note_message, connected
from TeleBot.core.decorators.lang import language
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

SAVE_COMMAND = get_command("SAVE_COMMAND")
CLEAR_COMMAND = get_command("CLEAR_COMMAND")
NOTES_COMMAND = get_command("NOTES_COMMAND")
RMALLNOTES_COMMAND = get_command("RMALLNOTES_COMMAND")
GET_COMMAND = get_command("GET_COMMAND")


@app.on_message(custom_filter.command(SAVE_COMMAND))
@language
async def _save(client, message, lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=True
    )
    if not chat:
        return

    if message.reply_to_message is None or len(message.command) < 2:
        await message.reply(lang.note1)
        return

    note_name, content, text, data_type = await get_note_tpye(message)
    if data_type is None:
        await message.reply(lang.note2)
        return
    if await is_note_exist(chat.id, note_name):
        await message.reply(lang.note2.format(note_name))
        return
    await save_note(chat.id, note_name, content, text, data_type)
    await message.reply(lang.note4.format(note_name))


@app.on_message(custom_filter.command(CLEAR_COMMAND))
@language
async def _clear(client, message, lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=True
    )
    if not chat:
        return
    if len(message.command) < 2:
        return await message.reply(lang.note5)
    note_name = message.command[1].lower()
    result = await clear_note(chat.id, note_name)
    if result is False:
        return await message.reply(lang.note6)
    await message.reply(lang.note7.format(note_name))


@app.on_message(custom_filter.command(NOTES_COMMAND))
@language
async def _save(client, message,lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=False
    )
    if not chat:
        return
    notes_name = await get_notes_list(chat.id)
    if not notes_name:
        return await message.reply(lang.note8.format(chat.title))
    msg = lang.note9
    for note_name in notes_name:
        msg += f"\n‣ `{note_name}`"
    await message.reply(msg)


@app.on_message(custom_filter.command(RMALLNOTES_COMMAND))
@language
async def _rmallnotes(client, message,lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=True
    )
    if not chat:
        return
    notes_name = await get_notes_list(chat.id)
    if not notes_name:
        await message.reply(lang.note8.format(chat.title))
        return

    return await message.reply(
        lang.note9.format(chat.title),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(lang.btn37, callback_data=f"stopallnotes_{chat.id}"),
                    InlineKeyboardButton(
                        lang.btn38,
                        callback_data=f"admin_close_{user.id if user else 0}",
                    ),
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("^stopallnotes_"))
@language
async def _stopallnotes(client, query,lang):
    chat_id = int(query.data.split("_")[1])
    user = await client.get_chat_member(chat_id, query.from_user.id)
    if user.status != ChatMemberStatus.OWNER:
        return await query.answer(lang.note11)
    await remove_all_notes(chat_id)
    return await query.message.edit(lang.note12)


@app.on_message(filters.regex(r"^#[^\s]+"))
@language
async def _hashnote(client, message,lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=False
    )
    if not chat:
        return
    chat_id = chat.id
    if not message.from_user:
        return
    note_name = message.text.split()[0].replace("#", "")
    if await is_note_exist(chat_id, note_name):
        await send_note_message(message, note_name, chat_id)


@app.on_message(custom_filter.command(GET_COMMAND))
@language
async def _getnote(client, message,lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=False
    )
    if not chat:
        return
    chat_id = chat.id
    if len(message.command) < 2:
        return await message.reply(lang.note13)
    note_name = message.command[1].lower()
    if await is_note_exist(chat_id, note_name):
        await send_note_message(message, note_name, chat_id)
    else:
        await message.reply(lang.note14)


__commands__ = SAVE_COMMAND + CLEAR_COMMAND + NOTES_COMMAND + RMALLNOTES_COMMAND
__mod_name__ = "𝙽ᴏᴛᴇs"


__help__ = """
**⸢ᴍᴀᴋᴇ ɴᴏᴛᴇs⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 
═───────◇───────═
๏ /get <notename>: ɢᴇᴛ ᴛʜᴇ ɴᴏᴛᴇ ᴡɪᴛʜ this ɴᴏᴛᴇɴᴀᴍᴇ.
๏ #<notename>*:* same as /get.
๏ /notes or /saved: ʟɪsᴛ ᴀʟʟ sᴀᴠᴇᴅ ɴᴏᴛᴇs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.

「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /save <notename> <notedata>: ꜱᴀᴠᴇꜱ ɴᴏᴛᴇᴅᴀᴛᴀ ᴀꜱ ᴀ ɴᴏᴛᴇ ᴡɪᴛʜ ɴᴀᴍᴇ ɴᴏᴛᴇɴᴀᴍᴇ
๏ /clear <notename>: ᴄʟᴇᴀʀ ɴᴏᴛᴇ ᴡɪᴛʜ ᴛʜɪꜱ ɴᴀᴍᴇ

「𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬」
๏ /removeallnotes: ʀᴇᴍᴏᴠᴇꜱ ᴀʟʟ ɴᴏᴛᴇꜱ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ
ɴᴏᴛᴇ: ɴᴏᴛᴇꜱ ᴀʟꜱᴏ ꜱᴜᴘᴘᴏʀᴛ ᴍᴀʀᴋᴅᴏᴡɴ formatters like: {first}, {last} ᴇᴛᴄ.. ᴀɴᴅ ʙᴜᴛᴛᴏɴꜱ.

๏ ᴄʜᴇᴄᴋ /markdownhelp ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ!
═───────◇───────═
"""
