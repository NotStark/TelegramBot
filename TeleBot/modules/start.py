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
from TeleBot.core.misc import paginate_modules


START_COMMAND = get_command("START_COMMAND")


@app.on_message(command(START_COMMAND))
@language
async def _start(client, message, strings):
    uptime = await get_readable_time((time.time() - StartTime))
    chat_id = message.chat.id
    args = message.text.split()
    media_type, media = await get_start_media()
    if message.chat.type == ChatType.PRIVATE:
        if len(args) >= 2:
            pass
        else:
            first_name = message.from_user.first_name
            btns = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=strings.btn1,
                            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=strings.btn2, callback_data="explore_cb"
                        ),
                        InlineKeyboardButton(
                            text=strings.btn3, callback_data="Friday_stats"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=strings.btn4, callback_data="help_back"
                        )
                    ],
                ]
            )
            caption = strings.start1.format(first_name, BOT_NAME, uptime)
            await app.send_photo(
                chat_id, media, caption=caption, reply_markup=btns
            ) if media_type == "image" else await app.send_video(
                chat_id, media, caption=caption, reply_markup=btns
            )

    else:
        caption = strings.start2.format(uptime)
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
