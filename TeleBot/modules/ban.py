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
async def _ban(client, message, lang):
    replied = message.reply_to_message
    chat = message.chat
    user = message.from_user.mention if message.from_user else "Anon"
    if replied and replied.sender_chat:
        channel_title, channel_id = replied.sender_chat.title, replied.sender_chat.id
        await client.ban_chat_member(chat.id, replied.sender_chat.id)
        await message.reply(lang.ban1.format(channel_title, channel_id, chat.title))

        return lang.ban2.format(user, channel_title, channel_id)

    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply(lang.admin1)
        return

    if user_id == BOT_ID:
        await message.reply(lang.ban3)
        return

    if user_id in await get_admins(chat.id):
        await message.reply(lang.ban4)
        return

    if await is_invincible(user_id):
        await message.reply(lang.ban5)
        return

    member = await client.get_chat_member(chat.id, user_id)
    text = lang.ban6.format(member.user.mention, user_id, user)
    button = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(lang.btn12, callback_data=f"unban_{user_id}_{user}")],
            [InlineKeyboardButton(lang.btn9, callback_data=f"admin_close_{user}")],
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
    return lang.ban7.format(member.user.mention, user)


async def unban_func(client, message, user_id, from_user, lang):
    chat = message.chat
    if not user_id:
        await message.reply(lang.admin1)
        return
    if user_id == BOT_ID:
        await message.reply("ʜᴏᴡ ᴡᴏᴜʟᴅ ɪ ᴜɴʙᴀɴ ᴍʏꜱᴇʟꜰ ɪꜰ ɪ ᴡᴀꜱ'ɴᴛ ʜᴇʀᴇ")
        return
    member = await client.get_chat_member(chat.id, user_id)
    if member.status != enums.ChatMemberStatus.BANNED:
        await message.reply_text("ʙʀᴜʜ ᴛʜɪs ᴘᴇʀsᴏɴ ɪs ɴᴏᴛ ʙᴀɴɴᴇᴅ.")
        return
    text = lang.ban8.format(
        member.user.mention, user_id, from_user.mention if from_user else "Anon"
    )
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
    return lang.ban9.format(
        member.user.mention, from_user.mention if from_user else "Anon"
    )


@app.on_callback_query(filters.regex("^unban_"))
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
    return await unban_func(client, query.message, user_id, from_user, lang)


@app.on_message(custom_filter.command(commands=UNBAN_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _unban(client, message, lang):
    replied = message.reply_to_message
    chat = message.chat
    user = message.from_user.mention if message.from_user else "Anon"
    if replied and replied.sender_chat:
        channel_title, channel_id = replied.sender_chat.title, replied.sender_chat.id
        await client.ban_chat_member(chat.id, channel_id)
        await message.reply(lang.ban10.format(channel_title, channel_id, chat.title))
        return lang.ban11.format(user, channel_title, channel_id)
    user_id = await extract_user_id(message)
    from_user = message.from_user
    return await unban_func(client, message, user_id, from_user)


@app.on_message(custom_filter.command(commands=TBAN_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _ban(client, message, lang):
    user = message.from_user if message.from_user else None
    user_id, reason = await extract_user_and_reason(message)
    chat = message.chat
    if not user_id:
        await message.reply_text(lang.admin1)
        return
    if user_id == BOT_ID:
        await message.reply(lang.ban3)
        return
    if user_id in await get_admins(chat.id):
        await message.reply(lang.ban4)
        return
    if await is_invincible(user_id):
        await message.reply(lang.ban5)
        return
    if not reason:
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang.btn13,
                        callback_data=f"tban:5m:{user_id}:{user.id if user else 0}",
                    ),
                    InlineKeyboardButton(
                        lang.btn16,
                        callback_data=f"tban:6h:{user_id}:{user.id if user else 0}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        lang.btn14,
                        callback_data=f"tban:3d:{user_id}:{user.id if user else 0}",
                    ),
                    InlineKeyboardButton(
                        lang.btn15,
                        callback_data=f"tban:1w:{user_id}:{user.id if user else 0}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        lang.btn9, callback_data=f"admin_close_{user.id if user else 0}"
                    )
                ],
            ]
        )
        await message.reply(lang.other8, reply_markup=btn)
        return
    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    until, unit = until_date(message, time_val, lang)
    if not until:
        return
    member = await client.get_chat_member(chat.id, user_id)
    await client.ban_chat_member(chat.id, user_id, until_date=until)
    txt = lang.ban12.format(message.chat.title, member.user.mention, time_val[0], unit)
    await message.reply_text(
        txt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang.btn12,
                        callback_data=f"unban_{user_id}_{message.from_user.id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        lang.btn9, callback_data=f"admin_close_{message.from_user.id}"
                    )
                ],
            ]
        ),
    )
    return lang.btn13.format(
        member.user.mention, user.mention if user else "Anon", time_val
    )


@app.on_callback_query(filters.regex("^tban:"))
@language
@loggable
async def _tbanCb(client, query, lang):
    value, user_id, from_user_id = query.data.split(":")[1:]
    from_user = query.from_user
    chat = query.message.chat
    if from_user.id != int(from_user_id):
        await query.answer(lang.other6, show_alert=True)
        return
    until, unit = await until_date(query.message, value, lang)
    member = await client.get_chat_member(chat.id, user_id)
    if not until_date:
        return
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.btn12, callback_data=f"unban_{user_id}_{from_user.id}"
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
        lang.ban12.format(chat.title, member.user.mention, value[0], unit),
        reply_markup=button,
    )
    return lang.btn13.format(member.user.mention, from_user.mention, value)


@app.on_message(custom_filter.command(commands=KICK_COMMAND))
@admins_stuff("can_restrict_members", bot=True)
@loggable
async def _punch(client, message, lang):
    user = message.from_user if message.from_user else None
    user_id = await extract_user_id(message)
    chat = message.chat
    if not user_id:
        await message.reply_text(lang.admin1)
        return
    if user_id == BOT_ID:
        return await message.reply(lang.ban13)
    if user_id in await get_admins(chat.id):
        return await message.reply(lang.ban15)

    if await is_invincible(user_id):
        return await message.reply(lang.ban16)

    member = await client.get_chat_member(chat.id, user_id)
    text = lang.ban17.format(
        member.user.mention, user_id, user.mention if user else "Anon"
    )

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
    return lang.ban18.format(member.user.mention, user.mention if user else "Anon")


@app.on_message(custom_filter.command(commands=PUNCH_COMMAND))
@admins_stuff("can_restrict_members", bot=True, user=False)
@loggable
async def _kickme(client, message, lang):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id in await get_admins(chat_id):
        return await message.reply(lang.other12)
    if message.command[0] == "kickme":
        await client.ban_chat_member(chat_id, user_id)
        await client.unban_chat_member(chat_id, user_id)
        await message.reply_text(lang.ban19)
    if message.command[0] == "banme":
        await client.ban_chat_member(chat_id, user_id)
        await message.reply_text(lang.ban20)


__commands__ = (
    BAN_COMMAND + 
    UNBAN_COMMAND + 
    TBAN_COMMAND + 
    KICK_COMMAND + 
    PUNCH_COMMAND
   )
__mod_name__ = "𝙱ᴀɴ"
__alt_names__ = ['ban','bans','punch']
