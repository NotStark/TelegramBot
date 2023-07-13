from TeleBot import app, BOT_ID
from pyrogram import filters, enums
from TeleBot.core import custom_filter
from strings import get_command
from .ban import time_buttons
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.log import loggable
from TeleBot.core.extractions import extract_user_id, extract_user_and_reason
from TeleBot.core.functions import get_admins, is_invincible, until_date
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup


MUTE_COMMAND = get_command("MUTE_COMMAND")
UNMUTE_COMMAND = get_command("UNMUTE_COMMAND")
TMUTE_COMMAND = get_command("TMUTE_COMMAND")


@app.on_message(custom_filter.command(commands=MUTE_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _mute(client, message, lang):
    chat = message.chat
    user_id = await extract_user_id(message)
    replied = message.reply_to_message
    admeme = message.from_user if message.from_user else None
    if not user_id:
        await message.reply(lang.admin1)
        return
    if user_id == BOT_ID:
        await message.reply(lang.mute1)
        return

    if user_id in await get_admins(chat.id):
        await message.reply(lang.mute2)
        return

    if await is_invincible(user_id):
        await message.reply(lang.mute3)
        return

    member = await client.get_chat_member(chat.id, user_id)
    txt = lang.mute4.format(member.user.mention, user_id, chat.title)

    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.mute36,
                    callback_data=f"unmute_{user_id}_{admeme.id if admeme else 0}",
                )
            ],
            [
                InlineKeyboardButton(
                    lang.btn9, callback_data=f"admin_close_{admeme.id if admeme else 0}"
                )
            ],
        ]
    )
    await message.reply(txt, reply_markup=button)
    if message.command[0] == "mute":
        await client.restrict_chat_member(
            chat.id, user_id, ChatPermissions(can_send_message=False)
        )
    if message.command[0] == "smute":
        await message.delete()
        if replied:
            await message.reply_to_message.delete()
        await client.restrict_chat_member(
            chat.id, user_id, ChatPermissions(can_send_message=False)
        )
        return
    if message.command[0] == "dmute":
        if replied:
            await message.reply_to_message.delete()
        await client.restrict_chat_member(
            chat.id, user_id, ChatPermissions(can_send_message=False)
        )

    await message.reply(txt, reply_markup=button)
    return lang.mute5.format(member.user.mention, admeme.mention if admeme else "Anon")


async def unmute_func(client, message, user_id, from_user, lang):
    chat = message.chat
    if not user_id:
        await message.reply(lang.admin1)
        return
    if user_id == BOT_ID:
        await message.reply(lang.mute6)
        return
    member = await client.get_chat_member(chat.id, user_id)
    if member.status != enums.ChatMemberStatus.RESTRICTED:
        return await message.reply_text(lang.mute7)
    text = lang.mute8.format(
        member.user.mention, user_id, from_user.mention if from_user else "Anon"
    )
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.btn9,
                    callback_data=f"admin_close_{from_user.id if from_user else 0}",
                )
            ]
        ]
    )
    await client.unban_chat_member(chat.id, user_id)
    await message.reply_text(text, reply_markup=button)
    return lang.mute9.format(
        member.user.mention, from_user.mention if from_user else "Anon"
    )


@app.on_callback_query(filters.regex("^unmute_"))
@language
@loggable
async def _unbanCb(client, query, lang):
    from_user_id = int(query.data.split("_")[2])
    user_id = int(query.data.split("_")[1])
    from_user = query.from_user
    if from_user.id != from_user_id:
        await query.answer(lang.other6, show_alert=True)
        return
    await query.message.delete()
    return await unmute_func(client, query.message, user_id, from_user, lang)


@app.on_message(custom_filter.command(commands=UNMUTE_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _ban(client, message, lang):
    user_id = await extract_user_id(message)
    from_user = message.from_user
    await unmute_func(client, message, user_id, from_user, lang)


@app.on_message(custom_filter.command(commands=TMUTE_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _tmute(client, message, lang):
    user_id, reason = await extract_user_and_reason(message)
    admeme = message.from_user
    chat = message.chat
    if not user_id:
        await message.reply_text(lang.admin1)
        return
    if user_id == BOT_ID:
        await message.reply(lang.mute1)
        return
    if user_id in await get_admins(chat.id):
        await message.reply(lang.mute2)
        return
    if await is_invincible(user_id):
        await message.reply(lang.mute3)
        return
    if not reason:
        btn = await time_buttons("tmute", user_id, admeme.id if admeme else 0, lang)
        await message.reply(lang.other8, reply_markup=btn)
        return
    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    until, unit = until_date(message, time_val)
    if not until:
        return
    member = await client.get_chat_member(chat.id, user_id)
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.btn36,
                    callback_data=f"unmute_{user_id}_{admeme.id if admeme else 0}",
                )
            ],
            [
                InlineKeyboardButton(
                    lang.btn9, callback_data=f"admin_close_{admeme.id if admeme else 0}"
                )
            ],
        ]
    )
    await client.restrict_chat_member(
        chat.id, user_id, ChatPermissions(can_send_messages=False), until_date=until
    )
    await message.reply_text(
        f"""
❕ᴛᴇᴍᴘᴏʀᴀʀʏ ᴍᴜᴛᴇᴅ
**🌟 ᴄʜᴀᴛ:** {chat.title}
**💥 ᴜsᴇʀ:** {member.user.mention}
**🚫 ᴍᴜᴛᴇᴅ ғᴏʀ:** {time_val[0]} {unit}    
    """,
        reply_markup=button,
    )
    return lang.mute10.format(
        member.user.mention,
        admeme.mention if admeme else "Anon",
        f"{time_val[0]} {unit}",
        reason,
    )


@app.on_callback_query(filters.regex("^tmute:"))
@language
@loggable
async def _tbanCb(client, query, lang):
    value, user_id, from_user_id = query.data.split(":")[1:]
    from_user = query.from_user
    chat = query.message.chat
    if from_user.id != int(from_user_id):
        await query.answer(lang.other6, show_alert=True)
        return
    until, unit = await until_date(query.message, value)
    member = await client.get_chat_member(chat.id, user_id)
    if not until_date:
        return
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.btn36, callback_data=f"unban_{user_id}_{from_user.id}"
                )
            ],
            [
                InlineKeyboardButton(
                    lang.btn9, callback_data=f"admin_close_{from_user.id}"
                )
            ],
        ]
    )
    await client.ban_chat_member(chat.id, user_id, until_date=until)
    await query.message.edit(
        f"""
❕ᴛᴇᴍᴘᴏʀᴀʀʏ ᴍᴜᴛᴇᴅ
**🌟 ᴄʜᴀᴛ:** {chat.title}
**💥 ᴜsᴇʀ:** {member.user.mention}
**🚫 ᴍᴜᴛᴇᴅ ғᴏʀ:** {value[0]} {unit}    
    """,
        reply_markup=button,
    )
    return lang.mute10.format(
        member.user.mention, from_user.mention, f"{value[0]} {unit}", None
    )


__commands__ = MUTE_COMMAND + UNMUTE_COMMAND + TMUTE_COMMAND
__mod_name__ = "𝙼ᴜᴛɪɴɢ"
__alt_names__ = ["mute"]
__sub_mode__ = ["𝙱ᴀɴ"]

__help__ = """
**⸢sᴏғᴛ ᴀᴄᴛɪᴏɴs⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /mute | /dmute <ᴜsᴇʀʜᴀɴᴅʟᴇ> : sɪʟᴇɴᴄᴇs ᴀ ᴜsᴇʀ. ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜsᴇʀ.
๏ /tmute <userhandle> x(m/h/d) : ᴍᴜᴛᴇs a ᴜsᴇʀ ғᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). m = ᴍɪɴᴜᴛᴇs, h = ʜᴏᴜʀs, ᴅ = ᴅᴀʏs.
๏ /unmute <userhandle> : ᴜɴᴍᴜᴛᴇs ᴀ ᴜsᴇʀ. ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜsᴇʀ. 
═───────◇───────═
"""
