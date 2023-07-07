from pyrogram import filters, errors, enums
from TeleBot import app
from strings import get_command
from TeleBot.core.extractions import extract_user_id
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TeleBot.mongo.approve_db import *
from TeleBot.core.decorators.chat_status import is_user_admin
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.log import loggable
from TeleBot.core.functions import get_admins, connected
from TeleBot.core.custom_filter import command

APPROVE_COMMAND = get_command("APPROVE_COMMAND")
DISAPPROVE_COMMAND = get_command("DISAPPROVE_COMMAND")
APPROVED_COMMAND = get_command("APPROVED_COMMAND")
APPROVAL_COMMAND = get_command("APPROVAL_COMMAND")
DISAPPROVEALL_COMMAND = get_command("DISAPPROVEALL_COMMAND")


@app.on_message(command(commands=APPROVE_COMMAND))
@language
@loggable
async def _approve(client, message, lang):
    user = message.from_user if message.from_user else None
    chat = await connected(
        message,
        message.sender_chat.id if message.sender_chat else message.from_user.id,
        lang,
        need_admin=True,
    )
    if not chat:
        return
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text(lang.admin1)
    if user_id in await get_admins(chat.id):
        await message.reply_text(lang.approve1)
        return
    check_user = await is_approved(chat.id, user_id)
    member = await client.get_chat_member(chat.id, user_id)
    if check_user:
        await message.reply_text(lang.approve2.format(member.user.mention, chat.title))
        return
    await approve_user(chat.id, user_id)
    await message.reply_text(lang.approve3.format(member.user.mention, chat.title))
    return lang.approve16.format(member.user.mention, user.mention if user else "Anon")


@app.on_message(command(commands=DISAPPROVE_COMMAND))
@language
@loggable
async def _disapprove(client, message, lang):
    chat = await connected(
        message,
        message.sender_chat.id if message.sender_chat else message.from_user.id,
        lang,
        need_admin=True,
    )
    if not chat:
        return
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text(lang.admin1)

    if user_id in await get_admins(chat.id):
        return await message.reply_text(lang.approve4)
    check_user = await is_approved(chat.id, user_id)
    member = await client.get_chat_member(chat.id, user_id)
    if not check_user:
        await message.reply_text(lang.approve5.format(member.user.mention))
        return
    await disapprove_user(chat.id, user_id)
    await message.reply_text(
        lang.approve6.format(member.user.mention, message.chat.title)
    )
    return lang.approve17.format(member.user.mention, message.from_user.mention if message.from_user else "Anon")



@app.on_message(command(commands=APPROVED_COMMAND))
@language
async def _approvedlist(client, message, lang):
    chat = await connected(
        message,
        message.sender_chat.id if message.sender_chat else message.from_user.id,
        lang,
        need_admin=True,
    )
    if not chat:
        return
    list1 = await approved_users(chat.id)
    if not list1:
        await message.reply_text(lang.approve7)
        return
    text = lang.approve8
    for i in list1:
        try:
            member = await client.get_chat_member(chat.id, int(i))
            text += f"⦾ {member.user.mention}\n"
        except:
            pass
    await message.reply_text(text)


@app.on_message(command(commands=APPROVAL_COMMAND))
@language
async def _approval(client, message, lang):
    chat = await connected(
        message,
        message.sender_chat.id if message.sender_chat else message.from_user.id,
        lang,
        need_admin=True,
    )
    if not chat:
        return
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply_text(lang.admin1)
    try:
        m = await client.get_chat_member(chat.id, user_id)
    except errors.BabRequest as e:
        return await message.reply(e.MESSAGE)
    check_user = await is_approved(chat.id, user_id)
    if check_user:
        return await message.reply_text(lang.approve9.format(m.user.mention))
    return await message.reply_text(lang.approve10.format(m.user.mention))


@app.on_message(command(commands=DISAPPROVEALL_COMMAND) & filters.group)
@language
async def _disappall(client, message, lang):
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat = await connected(message, user_id, lang, need_admin=True)
    if not chat:
        return
    m = await client.get_chat_member(chat.id, user_id)
    if m.status != enums.ChatMemberStatus.OWNER:
        return await message.reply_text(lang.approve11)
    list1 = await approved_users(chat.id)
    if list1 is None:
        return await message.reply_text(lang.approve12)
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.btn11, callback_data=f"unaproveall_{user_id}_{chat.id}"
                )
            ],
            [
                InlineKeyboardButton(
                    lang.btn9, callback_data=f"admin_close_{user_id}_{chat.id}"
                )
            ],
        ]
    )
    await message.reply_text(
        lang.approve13,
        reply_markup=btn,
    )


@app.on_callback_query(filters.regex("^unaproveall_"))
@language
@loggable
async def _unappall(client, query, lang):
    user_id = query.from_user.id
    chat_id = int(query.data.split("_")[2])
    if user_id != int(query.data.split("_")[1]):
        await query.answer(lang.approve14, show_alert=True)
        return
    await disapprove_all(chat_id)
    await query.message.edit_text(lang.approve15)
    return lang.approve18


__commands__ = (
    APPROVE_COMMAND
    + DISAPPROVE_COMMAND
    + APPROVED_COMMAND
    + APPROVAL_COMMAND
    + DISAPPROVEALL_COMMAND
)
__mod_name__ = "𝙰ᴘᴘʀᴏᴠᴇ"
__alt_names__ = ["approvals", "approve"]


__help__ = """
**⸢sᴏᴍᴇᴛɪᴍᴇs, ʏᴏᴜ ᴍɪɢʜᴛ ᴛʀᴜsᴛ ᴀ ᴜsᴇʀ ɴᴏᴛ ᴛᴏ sᴇɴᴅ ᴜɴᴡᴀɴᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ.
ᴍᴀʏʙᴇ ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴛᴏ ᴍᴀᴋᴇ ᴛʜᴇᴍ ᴀᴅᴍɪɴ, ʙᴜᴛ ʏᴏᴜ ᴍɪɢʜᴛ ʙᴇ ᴏᴋ ᴡɪᴛʜ blacklists, and antiflood not applying to them.
ᴛʜᴀᴛ's ᴡʜᴀᴛ ᴀᴘᴘʀᴏᴠᴀʟs ᴀʀᴇ ғᴏʀ - ᴀᴘᴘʀᴏᴠᴇ ᴏғ ᴛʀᴜsᴛᴡᴏʀᴛʜʏ ᴜsᴇʀs ᴛᴏ ᴀʟʟᴏᴡ ᴛʜᴇᴍ ᴛᴏ sᴇɴᴅ ⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
 
๏ /approve <ᴜsᴇʀ>: ᴀᴘᴘʀᴏᴠᴇ ᴛʜᴇ ᴜsᴇʀ, ʟᴏᴄᴋs ᴀɴᴛɪғʟᴏᴏᴅ ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛs ᴡᴏɴ'ᴛ ᴀᴘᴘʟʏ ᴛᴏ ᴛʜᴇᴍ ᴀɴʏᴍᴏʀᴇ.
๏ /disapprove <ᴜsᴇʀ>: ᴅɪsᴀᴘᴘʀᴏᴠᴇ ᴛʜᴇ ᴜsᴇʀ, ᴛʜᴇʏ ᴡɪʟʟ ɴᴏᴡ ʙᴇ sᴜʙᴊᴇᴄᴛ ᴛᴏ ʟᴏᴄᴋs ᴀɴᴛɪғʟᴏᴏᴅ ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛs again.
๏ /approved: List the approved users of a chat.
๏ /approval <ᴜsᴇʀ>: ᴄʜᴇᴄᴋ ᴛʜᴇ ᴀᴘᴘʀᴏᴠᴀʟ sᴛᴀᴛᴜs ᴏғ ᴀ ᴜsᴇʀ.
๏ /disapproveall: ᴅɪsᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴜsᴇʀs ᴏғ ᴀ ᴄʜᴀᴛ, ᴛʜɪs ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ.
═───────◇───────═
"""
