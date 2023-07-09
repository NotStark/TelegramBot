import os
import asyncio
import time
import re
import uvloop
import config
import importlib
from pyrogram import idle
from TeleBot import (
    BOT_NAME,
    app,
    LOG,
    CMD_LIST,
    DISABLE_ENABLE_MODULES,
    StartTime,
    BOT_USERNAME,
)
from rich.table import Table
from pyrogram import __version__ as v
from TeleBot.modules import ALL_MODULES
from TeleBot.core.custom_filter import command
from TeleBot.core.functions import get_readable_time, get_start_media, get_help_media
from strings import get_command
from pyrogram.enums import ChatType
from pyrogram import filters
from TeleBot.core.decorators.lang import language
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from TeleBot.mongo.rules_db import get_rules
from TeleBot.core.button_parser import button_markdown_parser
from TeleBot.core.misc import paginate_modules


HELPABLE = {}
START_COMMAND = get_command("START_COMMAND")
loop = asyncio.get_event_loop()

SUPPORT_SEND_MSG = """
🥀 {} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ...
┏•❅────✧❅✦❅✧────❅•┓
  **★ ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `1.0`
  **★ ᴩʏʀᴏɢʀᴀᴍ :** `{}`
┗•❅────✧❅✦❅✧────❅•┛
"""


LOG_MSG = "●▬▬▬▬▬▬▬▬▬▬▬▬๑۩ ʀᴏʙᴏᴛ ۩๑▬▬▬▬▬▬▬▬▬▬▬●\n"
LOG_MSG += "ʙᴏᴛ sᴛᴀʀᴛɪɴɢ ...... \n\n"
LOG_MSG += "⊙ ᴀ ᴘᴏᴡᴇʀғᴜʟ ᴘʏʀᴏɢʀᴀᴍ ʙᴀsᴇᴅ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ \n\n"
LOG_MSG += "⊙ ᴘʀᴏɪᴇᴄᴛ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : ʜᴛᴛᴘs://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/NᴏᴛSᴛᴀʀᴋ\n\n"
LOG_MSG += "⊙ ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ:\n"
LOG_MSG += "  @The_Only_God\n"
LOG_MSG += "●▬▬▬▬▬▬▬▬▬▬▬▬๑۩ ʀᴏʙᴏᴛ ۩๑▬▬▬▬▬▬▬▬▬▬▬●"


async def main():
    global HELPABLE, DISABLE_ENABLE_MODULES
    os.system("clear")
    LOG.print(Table(show_header=True, header_style="bold yellow").add_column(LOG_MSG))
    LOG.print("[bold cyan]ʟᴏᴀᴅɪɴɢ ᴍᴏᴅᴜʟᴇꜱ...")
    LOG.print("ꜰᴏᴜɴᴅ {} ᴍᴏᴅᴜʟᴇꜱ\n".format(len(ALL_MODULES)))

    for module_name in ALL_MODULES:
        module = importlib.import_module("TeleBot.modules." + module_name)
        commands = getattr(module, "__commands__", [])
        CMD_LIST.extend(commands)

        if hasattr(module, "__mod_name__") and module.__mod_name__:
            if hasattr(module, "__help__") and module.__help__:
                HELPABLE[module.__mod_name__] = module
            if commands:
                DISABLE_ENABLE_MODULES[module_name] = {
                    "module": module.__mod_name__,
                    "commands": commands,
                }

        LOG.print(f"✨ [bold cyan]ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʟᴏᴀᴅᴇᴅ: [green]{module_name}.py")
    LOG.print(f"[bold red]​🇧​​🇴​​🇹​ ​🇸​​🇹​​🇦​​🇷​​🇹​​🇪​​🇩​ ​🇦​​🇸​ {BOT_NAME}!")

    try:
        media_type, media = await get_start_media()
        caption = SUPPORT_SEND_MSG.format(BOT_NAME, v)
        chat = f"@{config.SUPPORT_CHAT}"
        await app.send_photo(
            chat, photo=media, caption=caption
        ) if media_type == "image" else await app.send_video(
            chat, video=media, caption=caption
        )

    except Exception as e:
        LOG.print(f"[bold red] {e}")
        LOG.print(
            "[bold red]ʙᴏᴛ ɪꜱɴ'ᴛ ᴀʙʟᴇ ᴛᴏ ꜱᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ @{config.SUPPORT_CHAT}!"
        )

    await idle()


async def send_help(chat_id, text, keyboard=None):
    media_type, media = await get_start_media()
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(HELPABLE, "help"))
    await app.send_photo(
        chat_id, media, caption=text, reply_markup=keyboard
    ) if media_type == "image" else await app.send_video(
        chat_id, media, caption=text, reply_markup=keyboard
    )
    return (text, keyboard)


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
                    return await client.send_message(chat_id, lang.rules10)
                chat = await client.get_chat(chat_idd)
                try:
                    txt, button = await button_markdown_parser(rules)
                    if len(button) == 0:
                        button = None
                    await client.send_message(
                        chat_id,
                        lang.rules9.format(chat.title, txt),
                        reply_markup=button,
                    )
                    return
                except Exception as e:
                    await client.send_message(
                        chat_id, lang.rules9.format(chat.title, rules)
                    )
                    raise e
            if args[1] == "help":
                await send_help(chat_id, lang.help1)

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
                    [InlineKeyboardButton(text=lang.btn4, callback_data="help_back")],
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


@app.on_message(filters.command("help"))
@language
async def get_help(client, message, lang):
    chat_id = message.chat.id
    args = message.text.split(None, 1)
    chat_type = message.chat.type
    media_type, media = await get_help_media()
    if chat_type != ChatType.PRIVATE:
        if len(args) >= 2:
            pass
        caption = lang.help2
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=lang.btn21,
                        url="https://t.me/{}?start=help".format(BOT_USERNAME),
                    )
                ],
            ],
        )
        await message.reply_photo(
            media, caption=caption, reply_markup=btn
        ) if media_type == "image" else await message.reply_video(
            media, caption=caption, reply_markup=btn
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        pass
    else:
        pass


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    if mod_match:
        module = mod_match[1]
        text = (
            "» **ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ** **{}** :\n".format(module)
            + HELPABLE[module].__help__
        )
        await query.message.edit_caption(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
            ),
        )


if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(main())
    LOG.print("[yellow] stopped client")
