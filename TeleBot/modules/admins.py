from TeleBot import app, BOT_ID
from pathlib import Path
from TeleBot.core.custom_filter import command
from pyrogram import filters, errors
from TeleBot.core.decorators.lang import language
from TeleBot.core.extractions import extract_user_id, extract_user_and_reason
from TeleBot.core.functions import get_admins, connected
from TeleBot.core.decorators.log import loggable
from TeleBot.core.decorators.chat_status import admins_stuff
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPrivileges
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.raw.functions.channels import SetStickers
from pyrogram.raw.types import InputStickerSetShortName


async def get_chat_privileges(client, status, chat_id):
    bot = (await client.get_chat_member(chat_id, BOT_ID)).privileges
    PROMOTE_DICT = {
        "normal": ChatPrivileges(
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_manage_chat=bot.can_manage_chat,
            can_promote_members=False,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
        "full": ChatPrivileges(
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
        "mid": ChatPrivileges(
            can_change_info=False,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=False,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
        "low": ChatPrivileges(),
    }
    return PROMOTE_DICT[status]


@app.on_message(command(commands="promote"))
@admins_stuff("can_promote_members", bot=True)
async def _promote(client, message, lang):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)
    from_user_id = (
        message.sender_chat.id if message.sender_chat else message.from_user.id
    )
    if user_id is None:
        return await message.reply(lang.admin1)
    if user_id == BOT_ID:
        return await message.reply(lang.admin2)
    if user_id in await get_admins(chat_id):
        return await message.reply(lang.admin3)
    await message.reply_text(
        lang.admin4,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang.btn5,
                        callback_data=f"promote_normal_{user_id}_{from_user_id}",
                    ),
                    InlineKeyboardButton(
                        lang.btn6,
                        callback_data=f"promote_full_{user_id}_{from_user_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        lang.btn7,
                        callback_data=f"promote_mid_{user_id}_{from_user_id}",
                    ),
                    InlineKeyboardButton(
                        lang.btn8,
                        callback_data=f"promote_low_{user_id}_{from_user_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        lang.btn9, callback_data=f"admin_close_{from_user_id}"
                    )
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("^promote_"))
@language
@loggable
async def _promotecb(client, query, lang):
    status, user_id, from_user_id, chat_id = query.data.split("_")[1:]
    from_user = query.from_user
    if from_user.id != int(from_user_id):
        await query.answer(lang.other6, show_alert=True)
        return
    chat = query.message.chat
    user = await client.get_chat_member(int(chat_id), int(user_id))
    print(user, chat_id, user_id)
    await query.message.delete()
    for statuss in ["normal", "full", "low", "mid"]:
        if statuss == status:
            chat_rights = await get_chat_privileges(client, status, chat.id)
            try:
                await client.promote_chat_member(chat.id, user.id, chat_rights)

            except errors.BadRequest as err:
                if err.MESSAGE == "USER_NOT_PARTICIPANT":
                    await query.message.reply(lang.admin5)
                    return
            await client.send_message(
                user.chat.id,
                lang.admin6.format(user.user.mention, chat.title, status),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=lang.btn10,
                                callback_data=f"demote_{user_id}_{from_user_id}_{chat_id}",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                lang.btn9, callback_data=f"admin_close_{from_user_id}"
                            )
                        ],
                    ]
                ),
            )
    return lang.admin7.format(user.user.mention, from_user.mention)


async def demote_func(client, message, user_id, from_user, lang):
    chat = message.chat
    user = await client.get_chat_member(chat.id, user_id)
    if user.user.is_bot:
        await message.reply(lang.admin9)
        return
    if user.status == ChatMemberStatus.OWNER:
        await message.reply(lang.admin10)
        return
    if user.status != ChatMemberStatus.ADMINISTRATOR:
        await message.reply(lang.admin11)
        return
    try:
        await client.promote_chat_member(
            chat.id,
            user_id,
            ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            ),
        )

        await client.send_message(chat.id, f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ {user.user.mention}")
    except errors.BadRequest as e:
        await message.reply(lang.admin12)
        return
    return lang.admin13.format(
        user.user.mention, from_user.mention if from_user else "Anon"
    )


@app.on_message(command("demote"))
@admins_stuff("can_promote_members", bot=True)
@loggable
async def _demote(client, message, lang):
    user_id = await extract_user_id(message)
    if user_id is None:
        await message.reply(lang.admin1)
        return
    if user_id == BOT_ID:
        await message.reply(lang.admin8)
        return
    return await demote_func(
        client, message, user_id, message.from_user.id if message.from_user else None
    )


@app.on_callback_query(filters.regex("^demote_"))
@language
@loggable
async def _demoteCb(client, query, lang):
    user_id = int(query.data.split("_")[1])
    from_user_id = int(query.data.split("_")[2])
    if query.from_user.id != from_user_id:
        await query.answer(lang.other6, show_alert=True)
        return
    await query.message.delete()
    return await demote_func(client, query.message, user_id, query.from_user)


@app.on_message(
    command(
        [
            "setgtitle",
            "setgdesc",
        ]
    )
)
@admins_stuff("can_change_info", bot=True)
@loggable
async def _group_cmds(client, message, lang):
    user = message.from_user.mention if message.from_user else "Anon"
    chat = message.chat
    if message.command[0] == "setgtitle":
        if len(message.command) < 2:
            await message.reply(lang.admin14)
            return
        title = message.text.split(maxsplit=1)[1]
        try:
            await client.set_chat_title(chat.id, title)
            await message.reply_text(lang.admin15)
        except errors.BadRequest as e:
            await message.reply_text(f"Error! {e.MESSAGE}.")
            return
        return lang.admin16.format(title, user)
    if message.command[0] == "setgdesc":
        if len(message.command) < 2:
            return await message.reply(lang.admin17)
        desc = message.text.split(maxsplit=1)[1]
        if len(desc) > 255:
            return await message.reply_text(lang.admin18)
        await client.set_chat_description(chat.id, desc)
        await message.reply_text(lang.admin19.format(chat.title))
        return lang.admin20.format(desc, user)


@app.on_message(command(["setgpic", "delgpic"]))
@admins_stuff("can_change_info", bot=True)
@loggable
async def _group_cmds2(client, message, lang):
    chat = message.chat
    user = message.from_user.mention if message.from_user else "Anon"
    if message.command[0] == "setgpic":
        replied = message.reply_to_message
        if replied and (replied.photo or replied.sticker):
            text = await message.reply_text(lang.admin21)
            g_pic = (
                await replied.download() if replied.sticker else replied.photo.file_id
            )
            await client.set_chat_photo(chat.id, photo=g_pic)
            await text.edit(lang.admin22)
            if replied.sticker:
                Path(g_pic).unlink(missing_ok=True)
            return lang.admin23.format(user)

        else:
            await message.reply_text(lang.admin24)
    if message.command[0] == "delgpic":
        await client.delete_chat_photo(chat.id)
        await message.reply_text(lang.admin25)
        return lang.admin26.format(user)


@app.on_message(command("title"))
@admins_stuff("can_promote_members", bot=True)
@loggable
async def _title(client, message, lang):
    user_id, title = await extract_user_and_reason(message)
    chat = message.chat
    if user_id is None:
        await message.reply(lang.admin1)
        return
    user = await client.get_chat_member(chat.id, user_id)
    if user.status == ChatMemberStatus.OWNER:
        await message.reply(lang.admin27)
        return
    if user.status != ChatMemberStatus.ADMINISTRATOR:
        await message.reply(lang.admin28)
        return
    if user_id == BOT_ID:
        await message.reply(lang.admin29)
        return
    if title is None:
        await message.reply(lang.admin30)
        return
    if len(title) > 16:
        await message.reply(lang.admin31)
        return

    await client.set_administrator_title(chat.id, user_id, title)
    await message.reply_text(lang.admin32.format(user.user.mention, title))
    return lang.admin33.format(
        user.user.mentio,
        title,
        message.from_user.mention if message.from_user else "Anon",
    )


@app.on_message(command("bots"))
@language
async def _botlist(client, message, lang):
    user_id = message.from_user.id if message.from_user else None
    chat_id = await connected(message, user_id, lang)
    if not chat_id:
        chat = message.chat
    else:
        chat = await client.get_chat(chat_id)
    repl = await message.reply(lang.admin36)
    header = lang.admin37.format(chat.title)
    async for m in client.get_chat_members(chat.id, filter=ChatMembersFilter.BOTS):
        header += f"◎ {m.user.mention}\n"
    await repl.edit({header})


@app.on_message(command("set_stickers"))
@admins_stuff("can_change_info", bot=True)
@loggable
async def set_sticker(client, message, lang):
    replied = message.reply_to_message
    admin = message.from_user.mention if message.from_user else 'Anon'
    chat = message.chat
    if replied:
        if not replied.sticker:
            await message.reply(
                lang.admin38
            )
            return
        stickers = message.reply_to_message.sticker.set_name
        try:
            await app.invoke(
                SetStickers(
                    channel=await client.resolve_peer(chat.id),
                    stickerset=InputStickerSetShortName(short_name=stickers),
                )
            )
            await message.reply_text(
                lang.admin39.format(chat.title)
            )
            return lang.admin42.format(stickers,admin)
        except errors.BadRequest as ee:
            if ee.MESSAGE == "PARTICIPANTS_TOO_FEW":
                await message.reply_text(
                    lang.admin40
                )
                return
    else:
        await message.reply(
            lang.admin41
        )
        return
