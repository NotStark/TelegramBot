import os
import time
import psutil
import strings
import config
from pyrogram import filters, __version__ as pyro
from TeleBot import app, StartTime, BOT_NAME, OWNER_USERNAME
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from TeleBot.core.functions import get_readable_time
from TeleBot.core.decorators.lang import language


STATS_MSG = """
ʜɪɪ {},

๏ ʜᴇʀᴇ ɪs ᴍʏ sᴛᴀᴛs:
» ʙᴏᴛ : {} MB
» ᴜᴘᴛɪᴍᴇ : {}
» ʀᴀᴍ : {}%
» ᴅɪsᴋ : {}%
» ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : {}
"""


@app.on_callback_query(filters.regex("explore_cb"))
@language
async def _explore(client, query, lang):
    await query.message.edit_caption(
        lang.cb1,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(lang.btn23, callback_data="telebot_about"),
                    InlineKeyboardButton(lang.btn24, callback_data="telebot_source"),
                ],
                [
                    InlineKeyboardButton(lang.btn25, callback_data="telebot_support"),
                    InlineKeyboardButton(
                        lang.btn26,
                        url=f"https://t.me/{OWNER_USERNAME}",
                    ),
                ],
                [InlineKeyboardButton(lang.btn27, callback_data="telebot_tos")],
                [InlineKeyboardButton(lang.btn22, callback_data="start_back")],
            ]
        ),
    )


@app.on_callback_query(filters.regex(r"^telebot_"))
@language
async def _explorecb(client, query, lang):
    data = query.data
    if data == "telebot_about":
        await query.message.edit_caption(
            lang.cb2.format(BOT_NAME, config.SUPPORT_CHAT),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(lang.btn22, callback_data="start_back")]]
            ),
        )
    elif data == "telebot_source":
        await query.message.edit_caption(
            lang.cb3.format(BOT_NAME, config.SUPPORT_CHAT),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(lang.btn22, callback_data="start_back")]]
            ),
        )
    elif data == "telebot_support":
        await query.message.edit_caption(
            lang.cb4.format(BOT_NAME),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            lang.btn25, url=f"https://t.me/{config.SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            lang.btn28, url=f"https://t.me/{config.UPDATES_CHANNEL}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                           lang.btn29, url=f"https://github.com/NotStark"
                        ),
                    ],
                    [InlineKeyboardButton(lang.btn22, callback_data="start_back")],
                ]
            ),
        )
    elif data == "telebot_tos":
        await query.message.edit_caption(
            lang.cb5,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(lang.btn22, callback_data="start_back")]])
        )
    elif data == "telebot_stats":
        first_name = query.from_user.first_name
        uptime = await get_readable_time(time.time() - StartTime)
        rem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        process = psutil.Process(os.getpid())
        mb = round(process.memory_info()[0] / 1024**2)
        await client.answer_callback_query(
            query.id,
            text=STATS_MSG.format(first_name, mb, uptime, rem, disk, pyro),
            show_alert=True,
        )
