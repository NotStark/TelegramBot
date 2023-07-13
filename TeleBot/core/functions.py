import re
import config
import mimetypes
import random
from datetime import datetime, timedelta
from TeleBot import app, BOT_ID
from cachetools import TTLCache
from pyrogram.enums import ChatMembersFilter
from time import perf_counter
from pyrogram import enums
from typing import Any
from TeleBot.mongo.connection_db import (
    get_connected_chat,
    is_connection_allowed,
    disconnect_chat,
)
from TeleBot.mongo.disable_db import get_disabled_commands, get_disable_delete
from pyrogram.errors import MessageDeleteForbidden
from TeleBot.mongo.approve_db import is_approved
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .button_parser import button_markdown_parser
from TeleBot.mongo.notes_db import get_note_data


async def is_invincible(user_id: int) -> bool:
    INVINCIBLES = config.SUDO_USERS + config.DEV_USERS
    return user_id in INVINCIBLES


admin_cache = TTLCache(maxsize=610, ttl=60 * 10, timer=perf_counter)


async def get_admins(chat_id: int):
    if chat_id in admin_cache:
        return admin_cache[chat_id]
    admins = [
        member.user.id
        async for member in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    admin_cache[chat_id] = admins
    return admins


async def get_readable_time(seconds: int) -> str:
    time_string = ""
    if seconds < 0:
        raise ValueError("Input value must be non-negative")

    if seconds < 60:
        time_string = f"{round(seconds)}s"
    else:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            time_string += f"{round(days)}days, "
        if hours > 0:
            time_string += f"{round(hours)}h:"
        time_string += f"{round(minutes)}m:{round(seconds):02d}s"

    return time_string


async def connected(message, user_id: int, lang, need_admin=True):
    if message.chat.type == enums.ChatType.PRIVATE:
        connected_chat = await get_connected_chat(user_id)
        if not connected_chat:
            await message.reply(lang.other1)
            return None

        if need_admin and not await is_user_admin(connected_chat, user_id):
            await message.reply(lang.admin34)
            return None

        chat = await app.get_chat(connected_chat)
        if not await is_connection_allowed(connected_chat) and not await is_invincible(
            user_id
        ):
            await message.reply(lang.admin35)
            await disconnect_chat(user_id)
            return None

        return chat

    elif need_admin and not await is_user_admin(message.chat.id, user_id):
        await message.reply(lang.admin34)
        return None

    return message.chat


async def remove_markdown(text: str) -> str:
    patterns = [
        r"\*\*(.*?)\*\*",
        r"__(.*?)__",
        r"\*(.*?)\*",
        r"_(.*?)_",
        r"`(.*?)`",
        r"\[(.*?)\]\((.*?)\)",
        r"~~(.*?)~~",
        r"\[(.*?)\]\[(.*?)\]",
        r"\!\[(.*?)\]\((.*?)\)",
    ]
    for pattern in patterns:
        text = re.sub(pattern, r"\1", text)
    return text


async def is_bot_admin(chat_id: int, permission: Any = None) -> bool:
    if permission is None and BOT_ID in await get_admins(chat_id):
        return True
    else:
        chat_member = await app.get_chat_member(chat_id, BOT_ID)
        privileges = (
            chat_member.privileges.__dict__
            if chat_member.privileges is not None
            else {}
        )
        return permission in privileges and privileges[permission]


async def is_user_admin(chat_id: int, user_id: int, permission: Any = None) -> bool:
    if await is_invincible(user_id) or user_id == chat_id:
        return True
    elif permission is None and user_id in await get_admins(chat_id):
        return True
    else:
        chat_member = await app.get_chat_member(chat_id, user_id)
        privileges = (
            chat_member.privileges.__dict__
            if chat_member.privileges is not None
            else {}
        )
        return permission in privileges and privileges[permission]


async def disable_action(message, command):
    chat_id = message.chat.id
    sender_id = message.sender_chat.id if message.sender_chat else message.from_user.id

    if await is_invincible(sender_id):
        return True

    disable_cmds = await get_disabled_commands(chat_id)

    if command in disable_cmds:
        if await get_disable_delete(chat_id):
            admins = await get_admins(chat_id)
            if sender_id not in admins and sender_id != chat_id:
                try:
                    await message.delete()
                except MessageDeleteForbidden:
                    pass
                else:
                    return False

            return False
        else:
            return False

    return True


def get_media_type(media):
    mime_type, _ = mimetypes.guess_type(media)
    if mime_type:
        if mime_type.startswith("image"):
            return "image", media
        elif mime_type.startswith("video"):
            return "video", media
    return "unknown", None


async def get_start_media():
    if not config.START_IMG:
        START_IMG = (
            "https://i.pinimg.com/564x/01/d6/ae/01d6ae16511ce7d7db7aef7844c119ea.jpg"
        )
    else:
        START_IMG = random.choice(config.START_IMG)
    media_type, media = get_media_type(START_IMG)
    return media_type, media


async def get_help_media():
    if not config.HELP_IMG:
        HELP_IMG = (
            "https://i.pinimg.com/564x/81/fd/c2/81fdc237881418f01147ecc367c594f7.jpg"
        )
    else:
        HELP_IMG = random.choice(config.HELP_IMG)
    media_type, media = get_media_type(HELP_IMG)
    return media_type, media


async def until_date(message, time_val, lang):
    time_units = {"m": "minutes", "h": "hours", "d": "days", "w": "weeks"}

    try:
        time_amount, time_unit = time_val
    except (IndexError, ValueError):
        await message.reply_text(lang.other9)
        return None, None

    if time_unit not in time_units:
        await message.reply_text(lang.other10)
        return None, None

    if not time_amount.isdigit():
        await message.reply_text(lang.other11)
        return None, None

    time_amount = int(time_amount)
    delta_unit = time_units[time_unit]
    until = datetime.now() + timedelta(**{delta_unit: time_amount})

    return until, delta_unit


async def get_help(module_dict, module_name):
    for key, value in module_dict.items():
        module_names = []
        for name in getattr(value, "__alt_names__", []) + [key]:
            module_names.append(name.replace(" ", "_").lower())
        if module_name.lower() in module_names:
            return key


async def prevent_approved(message):
    ignore = False
    chat_id = message.chat.id
    user_id = message.sender_chat.id if message.sender_chat else message.from_user.id
    if await is_approved(chat_id, user_id):
        ignore = True
    if await is_user_admin(chat_id, user_id):
        ignore = True

    return ignore


async def fillings(message, user, text):
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name or ""
    full_name = f"{first_name} {last_name}"
    username = user.username
    mention = user.mention
    chat_title = message.chat.title

    try:
        to_return = text.format(
            id=user_id,
            first=first_name,
            fullname=full_name,
            username=username,
            mention=mention,
            chatname=chat_title,
        )
    except Exception as e:
        to_return = text

    return to_return


async def get_note_tpye(message):
    data_type = None
    content = None
    text = ""

    if message.reply_to_message:
        if message.reply_to_message.text:
            text = message.reply_to_message.text
            data_type = 0
        elif message.reply_to_message.sticker:
            content = message.reply_to_message.sticker.file_id
            data_type = 1
        elif message.reply_to_message.animation:
            content = message.reply_to_message.animation.file_id
            text = message.reply_to_message.caption or ""
            data_type = 2
        elif message.reply_to_message.document:
            content = message.reply_to_message.document.file_id
            text = message.reply_to_message.caption or ""
            data_type = 3
        elif message.reply_to_message.photo:
            content = message.reply_to_message.photo.file_id
            text = message.reply_to_message.caption or ""
            data_type = 4
        elif message.reply_to_message.audio:
            content = message.reply_to_message.audio.file_id
            text = message.reply_to_message.caption or ""
            data_type = 5
        elif message.reply_to_message.voice:
            content = message.reply_to_message.voice.file_id
            text = message.reply_to_message.caption or ""
            data_type = 6
        elif message.reply_to_message.video:
            content = message.reply_to_message.video.file_id
            text = message.reply_to_message.caption or ""
            data_type = 7
        elif message.reply_to_message.video_note:
            content = message.reply_to_message.video_note.file_id
            data_type = 8

    if len(message.command) >= 3:
        note_name = message.command[1].lower()
        text = " ".join(message.command[2:])
    else:
        note_name = message.command[1].lower()

    return note_name, content, text, data_type


async def send_note_message(message, note_name, chat_id):
    content, text, data_type = await get_note_data(chat_id, note_name)
    filled_text = await fillings(message, message.from_user, text)
    filled_text, buttons = await button_markdown_parser(filled_text)
    if len(buttons) > 0:
        reply_markup = InlineKeyboardMarkup(buttons)
    else:
        reply_markup = None
    try:
        if data_type == 0:
            await message.reply_text(filled_text, reply_markup=None)
        elif data_type == 1:
            await message.reply_sticker(content, reply_markup=reply_markup)
        elif data_type == 2:
            await message.reply_animation(
                content, reply_markup=reply_markup, caption=text
            )
        elif data_type == 3:
            await message.reply_document(
                content, reply_markup=reply_markup, caption=text
            )
        elif data_type == 4:
            await message.reply_photo(content, reply_markup=reply_markup, caption=text)
        elif data_type == 5:
            await message.reply_audio(content, reply_markup=reply_markup, caption=text)
        elif data_type == 6:
            await message.reply_voice(content, reply_markup=reply_markup, caption=text)
        elif data_type == 7:
            await message.reply_video(content, reply_markup=reply_markup, caption=text)
        elif data_type == 8:
            await message.reply_video_note(content, reply_markup=reply_markup)
    except Exception as e:
        await message.reply(
            f"ᴛʜɪꜱ ɴᴏᴛᴇ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ꜱᴇɴᴛ, ᴀꜱ ɪᴛ ɪꜱ ɪɴᴄᴏʀʀᴇᴄᴛʟʏ ꜰᴏʀᴍᴀᴛᴛᴇᴅ. ᴀꜱᴋ ɪɴ @{config.SUPPORT_CHAT} ɪꜰ ʏᴏᴜ ᴄᴀɴ'ᴛ ꜰɪɢᴜʀᴇ ᴏᴜᴛ ᴡʜʏ\n\n‣ ᴇʀʀᴏʀ : {str(e)}"
        )


async def get_filter_type(message):
    if not message.reply_to_message:
        if message.text and len(message.text.split()) >= 3:
            content = None
            text = message.text.split(None, 2)[2]
            data_type = 0
        else:
            text = None
            data_type = None
            content = None
    else:
        reply_message = message.reply_to_message

        if reply_message.text and len(message.text.split()) >= 2:
            content = None
            text = reply_message.text
            data_type = 0
        elif reply_message.sticker:
            content = reply_message.sticker.file_id
            text = None
            data_type = 1
        elif reply_message.document:
            content = reply_message.document.file_id
            text = reply_message.caption
            data_type = 2
        elif reply_message.photo:
            content = reply_message.photo.file_id
            text = reply_message.caption
            data_type = 3
        elif reply_message.audio:
            content = reply_message.audio.file_id
            text = reply_message.caption
            data_type = 4
        elif reply_message.voice:
            content = reply_message.voice.file_id
            text = reply_message.caption
            data_type = 5
        elif reply_message.video:
            content = reply_message.video.file_id
            text = reply_message.caption
            data_type = 6
        elif reply_message.video_note:
            content = reply_message.video_note.file_id
            text = None
            data_type = 7
        elif reply_message.animation:
            content = reply_message.animation.file_id
            text = reply_message.caption
            data_type = 8
        else:
            text = None
            data_type = None
            content = None

    if len(message.command) >= 3:
        filter_name = message.text.split(maxsplit=2)[1].lower()
        text = message.text.split(maxsplit=2)[2]
    else:
        filter_name = message.command[1].lower()

    return filter_name, text, data_type, content


async def get_buttons(message, user_id, prefix, get_mode, get_emoji, lang):
    chat_id = message.chat.id
    mode, until = await get_mode(chat_id)
    emoji = await get_emoji(chat_id, mode)
    buttons = [
        [
            InlineKeyboardButton(
                f"{lang.btn39} {emoji if mode == 1 else ''}",
                callback_data=f"{prefix}_1_{user_id}",
            ),
            InlineKeyboardButton(
                f"{lang.btn44} {emoji if mode == 2 else ''}",
                callback_data=f"{prefix}_2_{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                f"{lang.btn40} {emoji if mode == 3 else ''}",
                callback_data=f"{prefix}_3_{user_id}",
            ),
            InlineKeyboardButton(
                f"{lang.btn30[1:]} {emoji if mode == 4 else ''}",
                callback_data=f"{prefix}_4_{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                f"{lang.btn31[1:]} {emoji if mode == 5 else ''}",
                callback_data=f"{prefix}_5_{user_id}",
            ),
            InlineKeyboardButton(
                f"{lang.btn41} {emoji if mode == 6 else ''}",
                callback_data=f"{prefix}_6_{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                f"{lang.btn42} {emoji if mode == 7 else ''}",
                callback_data=f"{prefix}_7_{user_id}",
            ),
            InlineKeyboardButton(
                f"{lang.btn43} {emoji if mode == 0 else ''}",
                callback_data=f"{prefix}_0_{user_id}",
            ),
        ],
        [InlineKeyboardButton(lang.btn9, callback_data=f"admin_close_{user_id}")],
    ]
    return buttons


async def get_time_buttons(user_id: int, prefix: str , lang : dict):
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    lang.btn13, callback_data=f"{prefix}_until=5m_{user_id}"
                ),
                InlineKeyboardButton(
                    lang.btn16, callback_data=f"{prefix}_until=6h_{user_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    lang.btn14, callback_data=f"{prefix}_until=3d_{user_id}"
                ),
                InlineKeyboardButton(
                    lang.btn15, callback_data=f"{prefix}_until=1w_{user_id}"
                ),
            ],
            [InlineKeyboardButton(lang.btn9, callback_data=f"admin_close_{user_id}")],
        ]
    )
    return btn
