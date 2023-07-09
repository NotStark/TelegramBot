import time
import config
import re
from TeleBot import app, StartTime, BOT_NAME, BOT_USERNAME, HELPABLE
from TeleBot.core.custom_filter import command
from TeleBot.core.functions import get_readable_time, get_start_media, get_help_media
from strings import get_command
from pyrogram.enums import ChatType
from pyrogram import filters
from TeleBot.core.decorators.lang import language
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..mongo.rules_db import get_rules
from ..core.button_parser import button_markdown_parser



START_COMMAND = get_command("START_COMMAND")


@app.on_message(command(START_COMMAND))
@language
async def _start(client, message, lang):
    uptime = await get_readable_time((time.time() - StartTime))
    chat_id = message.chat.id
    args = message.text.split()
    media_type, media = await get_start_media()
    if message.chat.type == ChatType.PRIVATE:
        if len(args) >= 2:
            if args[1].startswith("rules_"):
                chat_idd = int(args[1].split("_")[1])
                rules = await get_rules(chat_idd)
                if not rules:
                    return await client.send_message(chat_id,lang.rules10)
                chat = await client.get_chat(chat_idd)
                try:
                    txt, button = await button_markdown_parser(rules)       
                    return await client.send_message(chat_id,lang.rules9.format(chat.title,txt),reply_markup = InlineKeyboardMarkup(button))
                except Exception as e: 
                    await client.send_message(chat_id,lang.rules9.format(chat.title,rules))
                    raise e

        else:
            first_name = message.from_user.first_name
            btns = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=lang.btn1,
                            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=lang.btn2, callback_data="explore_cb"
                        ),
                        InlineKeyboardButton(
                            text=lang.btn3, callback_data="Friday_stats"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=lang.btn4, callback_data="help_back"
                        )
                    ],
                ]
            )
            caption = lang.start1.format(first_name, BOT_NAME, uptime)
            await app.send_photo(
                chat_id, media, caption=caption, reply_markup=btns
            ) if media_type == "image" else await app.send_video(
                chat_id, media, caption=caption, reply_markup=btns
            )

    else:
        caption = lang.start2.format(uptime)
        await message.reply_photo(
            media, caption=caption
        ) if media_type == "image" else await message.reply_video(
            media, caption=caption
        )


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(_, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    if mod_match:
        module = mod_match[1]
        text = (
            "» **ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ** **{}** :\n".format(module)
            + HELPABLE[module]["help"]
        )
        await query.message.edit_caption(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
            ),
        )
