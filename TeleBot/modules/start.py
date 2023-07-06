import time
import config
import re
from TeleBot import app, StartTime, BOT_NAME, BOT_USERNAME
from TeleBot.core.custom_filter import command
from TeleBot.core.functions import get_readable_time
from strings import get_command
from pyrogram.enums import ChatType
from pyrogram import filters
from TeleBot.core.decorators.lang import language
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from TeleBot.core.misc import paginate_modules
from TeleBot.__main__ import HELPABLE


START_COMMAND = get_command("START_COMMAND")

@app.on_message(command(START_COMMAND))
@language
async def _start(client, message, strings)
    uptime = await get_readable_time((time.time() - StartTime))
    chat_id = message.chat.id
    args = message.text.split()
    if message.chat.type == ChatType.PRIVATE:
        if len(args) >= 2:
            pass
        else:
            first_name = message.from_user.first_name
            await app.send_photo(
                chat_id,
                photo=config.START_IMG,
                caption=strings.start1.format(first_name, BOT_NAME, uptime),
                reply_markup=InlineKeyboardMarkup(
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
                                text = strings.btn4, callback_data="help_back"
                            )
                        ],
                    ]
                ),
            )

    else:
        await message.reply_photo(
            config.START_IMG,
            caption=strings.start2.format(uptime),
            # reply_markup=InlineKeyboardMarkup(btn)
        )


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(_,query):    
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    print(mod_match)