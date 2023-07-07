from pyrogram import filters, errors, enums
from TeleBot import app
from TeleBot.helpers.extractions import extract_user_id
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TeleBot.mongo.approve_db import *
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.lang import language
from TeleBot.core.functions import get_admins
from TeleBot.core.custom_filters import command


@app.on_message(command(commands="approve"))
@admins_stuff()
async def _approve(client, message, lang):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text(
            lang.admin1
        )
    if user_id in await get_admins(chat_id):
        return await message.reply_text(
            lang.approve1
        )
    check_user = await isApproved(chat_id, user_id)
    member = await client.get_chat_member(chat_id, user_id)
    if check_user:
        return await message.reply_text(
            lang.approve2.format(member.user.mention)
        )
    await approve_user(chat_id, user_id)
    return await message.reply_text(
        lang.approve3.format(member.user.mention,message.chat.title)
    )


@app.on_message(command(commands="disapprove"))
@admins_stuff()
async def _disapprove(client, message, lang):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text(
           lang.admin1
        )

    if user_id in await get_admins(chat_id):
        return await message.reply_text(
           lang.approve4
        )
    check_user = await isApproved(chat_id, user_id)
    member = await client.get_chat_member(chat_id, user_id)
    if not check_user:
        return await message.reply_text(lang.approve5.format(member.user.mention))
    await disapprove_user(chat_id, user_id)
    await message.reply_text(
        lang.approve6.format(member.user.mention,message.chat.title)
    )


@app.on_message(command(commands="approved"))
@admins_stuff()
async def _approvedlist(client, message, lang):
    chat_id = message.chat.id
    list1 = await approved_users(chat_id)
    if not list1:
        return await message.reply_text(
            lang.approve7
        )
    text = lang.approve8
    for i in list1:
        try:
            member = await client.get_chat_member(chat_id, int(i))
            text += f"⦾ {member.user.mention}\n"
        except:
            pass
    await message.reply_text(text)


@app.on_message(command(commands="approval"))
@admins_stuff()
async def _approval(client, message, lang):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply_text(
            lang.admin1
        )
    try:
        m = await client.get_chat_member(chat_id, user_id)
    except errors.BabRequest as e:
        return await message.reply(e.MESSAGE)
    check_user = await isApproved(chat_id, user_id)
    if check_user:
        return await message.reply_text(
            lang.approve9.format(m.user.mention)
        )
    return await message.reply_text(
        lang.approve10.format(m.user.mention)
    )


@app.on_message(command(commands="disapproveall") & filters.group)
@language
async def _disappall(client, message, lang):
    user_id = message.from_user.id
    chat_id = message.chat.id
    m = await _.get_chat_member(chat_id, user_id)
    if m.status != enums.ChatMemberStatus.OWNER:
        return await message.reply_text(
            lang.approve11
        )
    list1 = await approved_users(chat_id)
    if list1 is None:
        return await message.reply_text(
            lang.approve12
        )
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.btn11, callback_data=f"unaproveall_{user_id}"
                )
            ],
            [InlineKeyboardButton(lang.btn9, callback_data=f"admin_close_{user_id}")],
        ]
    )
    await message.reply_text(
        lang.approve13,
        reply_markup=btn,
    )


@app.on_callback_query(filters.regex("^unaproveall_"))
@language
async def _unappall(client, query, lang):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    if user_id != int(query.data.split("_")[1]):
        return await query.answer(
            lang.approve14, show_alert=True
        )
    await disapprove_all(chat_id)
    return await query.message.edit_text(lang.approve15)


__commands__ = ["approve", "approved", "approval", "disapprove"]
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
