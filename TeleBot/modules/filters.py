import re
from TeleBot import app
from TeleBot.core import custom_filter
from TeleBot.mongo.filters_db import (
    add_filter,
    stop_filter,
    get_filters_list,
    remove_all_filters,
    get_filter,
)
from strings import get_command
from TeleBot.core.functions import get_filter_type
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus
from TeleBot.core.filter_groups import filters_watcher
from TeleBot.core.button_parser import button_markdown_parser
from TeleBot.core.functions import fillings , connected
from TeleBot.core.decorators.lang import language


FILTER_COMMAND = get_command("FILTER_COMMAND")
STOP_COMMAND = get_command("STOP_COMMAND")
FILTERS_COMMAND = get_command("FILTERS_COMMAND")
RMALLFILTERS_COMMAND = get_command("RMALLFILTERS_COMMAND")

@app.on_message(custom_filter.command(FILTER_COMMAND))
@language
async def _filter(client, message, lang):
    replied = message.reply_to_message
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=True
    )
    if not chat:
        return
    if replied is None and len(message.command) < 3:
        return await message.reply(
            lang.filter1
        )
    filter_name, text, data_type, content = await get_filter_type(message)
    await add_filter(chat.id, filter_name, content, text, data_type)
    return await message.reply(lang.filter2.format(filter_name,chat.title))


@app.on_message(custom_filter.command(STOP_COMMAND))
@language
async def _stopfilter(client, message, lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=True
    )
    if not chat:
        return
    if len(message.command) < 2:
        return await message.reply(lang.filter3)
    keyword = message.command[1].lower()
    result = await stop_filter(chat.id, keyword)
    if not result:
        return await message.reply(
            lang.filter4
        )
    return await message.reply(
        lang.filter5.format(keyword,chat.title)
    )


@app.on_message(custom_filter.command(FILTERS_COMMAND))
@language
async def _filters(client, message, lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=True
    )
    if not chat:
        return
    filters_name = await get_filters_list(chat.id)
    if not filters_name:
        return await message.reply(lang.filter6.format(chat.title))
    txt = lang.filter7.format(chat.title)
    for filter_name in filters_name:
        txt += f"\n‣ `{filter_name}`"
    await message.reply(txt)


@app.on_message(custom_filter.command(RMALLFILTERS_COMMAND))
@language
async def _rmallfilter(client, message ,lang):
    user = message.from_user
    chat = await connected(
        message, user.id if user else message.sender_chat.id, lang, need_admin=True
    )
    if not chat:
        return
    filters_name = await get_filters_list(chat.id)
    if not filters_name:
        return await message.reply(lang.filter6.format(chat.title))

    return await message.reply(
        lang.filter8.format(chat.title)
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(lang.btn37, callback_data=f"stopallfilter_{chat.id}"),
                    InlineKeyboardButton(
                        lang.btn38,
                        callback_data=f"admin_close_{user.id if user else 0}",
                    ),
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("^stopallfilter_"))
@language
async def _stopallfilter(client, query,lang):
    chat_id = int(query.data.split("_")[1])
    user = await client.get_chat_member(chat_id, query.from_user.id)
    if user.status != ChatMemberStatus.OWNER:
        return await query.answer(lang.filter)
    await remove_all_filters(chat_id)
    return await query.message.edit(lang.filter10)


@app.on_message(filters.group, group=filters_watcher)
async def _filterwatcher(client, message):
    chat = message.chat
    if not message.from_user:
        return
    user = message.from_user
    if message.command and message.command[0] in FILTER_COMMAND:
        return
    text = message.text or message.caption
    if not text:
        return

    filters_name = await get_filters_list(chat.id)
    if not filters_name:
        return
    for filter_name in filters_name:
        regex_pattern = r"( |^|[^\w])" + re.escape(filter_name) + r"( |$|[^\w])"
        if re.search(regex_pattern, text, re.IGNORECASE):
            x = await get_filter(chat.id, filter_name)
            filter_text, content, data_type = x["text"], x["content"], x["data_type"]
            filled_text = await fillings(message, user, filter_text)
            try:
                filled_text, button = await button_markdown_parser(filled_text)
                # TODO test buttons
                if not button:
                    button = None
                else:
                    button = InlineKeyboardMarkup(button)

            except:
                filled_text, button = filled_text, None

            if data_type == 0:
                await client.send_message(
                    chat.id,
                    filled_text,
                    reply_markup=button,
                    reply_to_message_id=message.id,
                )
            elif data_type == 1:
                await client.send_sticker(
                    chat.id, sticker=content, reply_to_message_id=message.id
                )
            elif data_type == 2:
                await client.send_document(
                    chat.id,
                    document=content,
                    caption=filled_text,
                    reply_markup=button,
                    reply_to_message_id=message.id,
                )
            elif data_type == 3:
                await client.send_photo(
                    chat.id,
                    photo=content,
                    caption=filled_text,
                    reply_markup=button,
                    reply_to_message_id=message.id,
                )
            elif data_type == 4:
                await client.send_audio(
                    chat.id,
                    audio=content,
                    caption=filled_text,
                    reply_markup=button,
                    reply_to_message_id=message.id,
                )
            elif data_type == 5:
                await client.send_voice(
                    chat.id,
                    voice=content,
                    caption=filled_text,
                    reply_markup=button,
                    reply_to_message_id=message.id,
                )
            elif data_type == 6:
                await client.send_video(
                    chat.id,
                    video=content,
                    caption=filled_text,
                    reply_markup=button,
                    reply_to_message_id=message.id,
                )
            elif data_type == 7:
                await client.send_video_note(
                    chat.id,
                    video_note=content,
                    caption=filled_text,
                    reply_markup=button,
                    reply_to_message_id=message.id,
                )
            elif data_type == 8:
                await client.send_animation(
                    chat.id,
                    animation=content,
                    caption=filled_text,
                    reply_markup=button,
                    reply_to_message_id=message.id,
                )
