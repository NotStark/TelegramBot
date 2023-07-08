from TeleBot import app, BOT_ID
from pyrogram import filters, enums
from strings import get_command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TeleBot.core.extractions import extract_user_id
from TeleBot.core.functions import is_invincible, until_date, get_admins
from TeleBot.core.extractions import extract_user_and_reason
from TeleBot.core import custom_filter
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.log import loggable
from TeleBot.core.decorators.lang import language


BAN_COMMAND = get_command("BAN_COMMAND")
UNBAN_COMMAND = get_command("UNBAN_COMMAND")
TBAN_COMMAND = get_command("TBAN_COMMAND")
KICK_COMMAND = get_command("KICK_COMMAND")
PUNCH_COMMAND = get_command("PUNCH_COMMAND")

@app.on_message(custom_filter.command(commands=BAN_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _ban(client, message,lang):
    replied = message.reply_to_message
    chat = message.chat
    user = message.from_user.mention if message.from_user else 'Anon'
    if replied and replied.sender_chat:
        channel_title , channel_id = replied.sender_chat.title , replied.sender_chat.id
        await client.ban_chat_member(chat.id, replied.sender_chat.id)
        await message.reply(
            lang.ban1.format(channel_title, channel_id , chat.title)
        )

        return lang.ban2.format(user,channel_title,channel_id)

    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply(
            lang.admin1
        )

    if user_id == BOT_ID:
        return await message.reply(lang.ban3)

    if user_id in await get_admins(chat.id):
        return await message.reply(
            lang.ban4
        )

    if await is_invincible(user_id):
        return await message.reply(lang.ban5)

    member = await client.get_chat_member(chat.id, user_id)
    text = lang.ban6.format(member.user.mention,user_id,user)
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.btn12, callback_data=f"unban_{user_id}_{user}"
                )
            ],
            [
                InlineKeyboardButton(
                    lang.btn9, callback_data=f"admin_close_{user}"
                )
            ],
        ]
    )
    if message.command[0] == "ban":
        await client.ban_chat_member(chat.id, user_id)
    if message.command[0] == "sban":
        await message.delete()
        if replied:
            await message.reply_to_message.delete()
        await client.ban_chat_member(chat.id, user_id)
        return
    if message.command[0] == "dban":
        if replied:
            await message.reply_to_message.delete()
        await client.ban_chat_member(chat.id, user_id)
    await message.reply(text, reply_markup=button)
    return lang.ban7.format(member.user.mention,user)


async def unban_func(client, message, user_id, from_user,lang):
    chat = message.chat
    if not user_id:
        return await message.reply(
            "I ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ...!"
        )
    if user_id == BOT_ID:
        return await message.reply("ʜᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴜɴʙᴀɴ ᴍʏꜱᴇʟꜰ ɪꜰ ɪ ᴡᴀꜱ'ɴᴛ ʜᴇʀᴇ")
    member = (await client.get_chat_member(chat.id, user_id)).user
    if member.status != enums.ChatMemberStatus.BANNED:
        await message.reply_text("ʙʀᴜʜ ᴛʜɪs ᴘᴇʀsᴏɴ ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ.")
    text = f"**❕ᴜɴʙᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ ꜱᴜᴄᴇꜱꜱꜰᴜʟʟ**:\n\n‣ **ᴜꜱᴇʀ** : {user.mention}\n‣ **ᴜꜱᴇʀ ɪᴅ** : {user_id}\n‣ **ᴜɴʙᴀɴɴᴇᴅ ʙʏ** : {from_user.mention if from_user else 'Anon'}"
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• ᴄʟᴏsᴇ •",
                    callback_data=f"admin_close_{from_user.id if from_user else 0}",
                )
            ]
        ]
    )
    await client.unban_chat_member(chat.id, user_id)
    await message.reply_text(text, reply_markup=button)


@app.on_callback_query(filters.regex("^unban_"))
@language
@loggable
async def _unbanCb(client, query , lang):
    from_user_id = int(query.data.split("_")[2])
    user_id = int(query.data.split("_")[1])
    from_user = query.from_user
    if from_user.id != from_user_id:
        return await query.answer("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴘᴇʀꜰʀᴏᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ 🔴.", show_alert=True)
    await query.message.delete()
    await unban_func(client, query.message, user_id, from_user)


@app.on_message(custom_filter.command(commands=UNBAN_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _unban(client, message , lang):
    replied = message.reply_to_message
    chat = message.chat
    if replied and replied.sender_chat:
        await client.ban_chat_member(chat.id, replied.sender_chat.id)
        await message.reply(
            f"ꜱᴜᴄᴇꜱꜱꜰᴜʟʟʏ ᴜɴʙᴀɴɴᴇᴅ {replied.sender_chat.title} ({replied.sender_chat.id}) ɪɴ {chat.title}"
        )
        return
    user_id = await extract_user_id(message)
    from_user = message.from_user
    await unban_func(client, message, user_id, from_user)


@app.on_message(custom_filter.command(commands=TBAN_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _ban(client, message , lang):
    user_id, reason = await extract_user_and_reason(message)
    chat = message.chat
    if not user_id:
        await message.reply_text(
            "I ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ...!"
        )
        return
    if user_id == BOT_ID:
        return await message.reply("ɪ'ᴍ ɴᴏᴛ ɢᴏɴɴᴀ ʙᴀɴ ᴍʏꜱᴇʟꜰ ꜰᴏᴏʟ")
    if user_id in await get_admins(chat.id):
        return await message.reply(
            "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏꜰ ᴛʜɪꜱ ᴄʜᴀᴛ.ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ʜɪᴍ.ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴅᴏ ɪᴛ ᴍᴀɴᴜᴀʟʟʏ"
        )
    if await is_invincible(user_id):
        return await message.reply("ꜱᴏʀʀʏ ʙᴜᴛ ɪ ᴄᴀɴ'ᴛ ʙᴀɴ ᴍʏ ᴅᴀᴅᴅʏ")
    if not reason:
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝟻 ᴍɪɴᴜᴛᴇs",
                        callback_data=f"tban:5m:{user_id}:{message.from_user.id}",
                    ),
                    InlineKeyboardButton(
                        "𝟼 ʜᴏᴜʀs",
                        callback_data=f"tban:6h:{user_id}:{message.from_user.id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "𝟹 ᴅᴀʏs",
                        callback_data=f"tban:3d:{user_id}:{message.from_user.id}",
                    ),
                    InlineKeyboardButton(
                        "𝟷 ᴡᴇᴇᴋ",
                        callback_data=f"tban:1w:{user_id}:{message.from_user.id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "ᴄᴀɴᴄᴇʟ", callback_data=f"admin_close_{message.from_user.id}"
                    )
                ],
            ]
        )
        return await message.reply("**ᴄʜᴏᴏsᴇ ᴠᴀʟᴜᴇ**", reply_markup=btn)
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
                    "• ᴜɴʙᴀɴ •", callback_data=f"unban_{user_id}_{message.from_user.id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "• ᴄʟᴏsᴇ •", callback_data=f"admin_close_{message.from_user.id}"
                )
            ],
        ]
    )
    await client.ban_chat_member(chat.id, user_id, until_date=until)
    await message.reply_text(
        f"""
❕ᴛᴇᴍᴘ ʙᴀɴɴᴇᴅ
**🌟 ᴄʜᴀᴛ:** {message.chat.title}
**💥 ᴜsᴇʀ:** {member.user.mention}
**🚫 ʙᴀɴɴᴇᴅ ғᴏʀ:** {time_val[0]} {unit}    
    """,
        reply_markup=button,
    )


@app.on_callback_query(filters.regex("^tban:"))
@language
@loggable
async def _tbanCb(client, query , lang):
    value, user_id, from_user_id = query.data.split(":")[1:]
    from_user = query.from_user
    chat = query.message.chat
    if from_user.id != int(from_user_id):
        return await query.answer("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴘᴇʀꜰʀᴏᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ 🔴.", show_alert=True)
    until, unit = await until_date(query.message, value)
    member = await client.get_chat_member(chat.id, user_id)
    if not until_date:
        return
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• ᴜɴʙᴀɴ •", callback_data=f"unban_{user_id}_{from_user.id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "• ᴄʟᴏsᴇ •", callback_data=f"admin_close_{from_user.id}"
                )
            ],
        ]
    )
    await client.ban_chat_member(chat.id, user_id, until_date=until)
    await query.message.edit(
        f"""
❕ᴛᴇᴍᴘ ʙᴀɴɴᴇᴅ
**🌟 ᴄʜᴀᴛ:** {chat.title}
**💥 ᴜsᴇʀ:** {member.user.mention}
**🚫 ʙᴀɴɴᴇᴅ ғᴏʀ:** {value[0]} {unit}    
    """,
        reply_markup=button,
    )


@app.on_message(custom_filter.command(commands=KICK_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _punch(client, message , lang):
    user_id = await extract_user_id(message)
    chat = message.chat
    if not user_id:
        await message.reply_text(
            "I ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ...!"
        )
        return
    if user_id == BOT_ID:
        return await message.reply("ɪ'ᴍ ɢᴏɴɴᴀ ᴋɪᴄᴋ ᴍʏꜱᴇʟꜰ")
    if user_id in await get_admins(chat.id):
        return await message.reply(
            "ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀɴ ᴀᴅᴍɪɴɪꜱᴛʀᴀᴛᴏʀ ᴏꜰ ᴛʜɪꜱ ᴄʜᴀᴛ.ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ʜɪᴍ.ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴅᴏ ɪᴛ ᴍᴀɴᴜᴀʟʟʏ."
        )

    if await is_invincible(user_id):
        return await message.reply("ꜱᴏʀʀʏ ʙᴜᴛ ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴍʏ ᴅᴀᴅᴅʏ")

    member = await client.get_chat_member(chat.id, user_id)
    text = f"**❗ᴋɪᴄᴋᴇᴅ!**\n\n‣ **ᴜꜱᴇʀ** : {member.user.mention}\n\‣ **ᴜꜱᴇʀ ɪᴅ** : {user_id}\n‣ **ᴋɪᴄᴋᴇᴅ ʙʏ** : {message.from_user.mention}"

    if message.command[0] in ["kick", "punch"]:
        await client.ban_chat_member(chat.id, user_id)
        await client.unban_chat_member(chat.id, user_id)
    if message.command[0] == "dkick":
        if message.reply_to_message:
            await message.reply_to_message.delete()
        await client.ban_chat_member(chat.id, user_id)
        await client.unban_chat_member(chat.id, user_id)

    if message.command[0] == "skick":
        if message.reply_to_message:
            await message.reply_to_message.delete()
        await message.delete()
        await client.ban_chat_member(chat.id, user_id)
        await client.unban_chat_member(chat.id, user_id)
        return
    await message.reply(text)


@app.on_message(custom_filter.command(commands=PUNCH_COMMAND))
@admins_stuff("can_restrict_members",bot=True , user = False)
@loggable
async def _kickme(client, message , lang):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id in await get_admins(chat_id):
        return await message.reply("ɪ ᴄᴀɴ'ᴛ ᴘᴇʀꜰᴏʀᴍ ᴛʜɪꜱ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴛᴏ ᴀᴅᴍɪɴꜱ")
    if message.command[0] == "kickme":
        await client.ban_chat_member(chat_id, user_id)
        await client.unban_chat_member(chat_id, user_id)
        await message.reply_text("*ᴋɪᴄᴋs ʏᴏᴜ ᴏᴜᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ*")
    if message.command[0] == "banme":
        await client.ban_chat_member(chat_id, user_id)
        await message.reply_text("**🚫 ʙᴀɴɴᴇᴅ ʏᴏᴜ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.**")


__commands__ = BAN_COMMAND + UNBAN_COMMAND + TBAN_COMMAND + KICK_COMMAND + PUNCH_COMMAND
__mod_name__ = "ʙᴀɴ"
