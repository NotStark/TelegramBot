import os
from TeleBot import app, DISABLE_ENABLE_MODULES
from pyrogram import filters
from config import HANDLERS
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.log import loggable
from TeleBot import CMD_LIST
from strings import get_command
from TeleBot.mongo.disable_db import (
    add_disable,
    rm_disable,
    get_all_module_status,
    disable_module,
    enable_module,
    disabledel,
    get_disabled_commands,
)
from itertools import zip_longest
from TeleBot.core.functions import connected
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from TeleBot.core import custom_filter


DISABLE_COMMAND = get_command("DISABLE_COMMAND")
MODULE_COMMAND = get_command("MODULE_COMMAND")


@app.on_message(custom_filter.command(DISABLE_COMMAND))
@loggable
async def _disable_enable(client, message,lang):
    chat = await connected(message,message.sender_chat.id if message.sender_chat else message.from_user.id , lang , need_admin=True)
    if not chat:
        return
    user = message.from_user.mention if message.from_user else 'Anon'
    if message.command[0] == "disable":
        if len(message.command) < 2:
            await message.reply(lang.disable1)
            return
        args = message.command[1].lower()
        for HANDLER in HANDLERS:
            if args.startswith(HANDLER):
                args = args[1:]
        if args not in CMD_LIST:
            await message.reply(
                lang.disable2
            )
            return
        await add_disable(chat.id, args)

        await message.reply(lang.disable3.format(args))
        return lang.disable4.format(args,user)
    if message.command[0] == "enable":
        args = message.command[1].lower()
        for HANDLER in HANDLERS:
            if args.startswith(HANDLER):
                args = args[1:]
        if args not in CMD_LIST:
            await message.reply(
                lang.disable5
            )
            return 

        sucess = await rm_disable(chat.id, args)
        if sucess is False:
            await message.reply(lang.disable6)
            return
        await message.reply(lang.disable7.format(args))
        return lang.disable8.format(args,user)
    if message.command[0] == "disabledel":
        usage = lang.disable9
        if len(message.command) < 2:
            await message.reply(usage)
            return 
        arg = message.command[1].lower()
        if arg == "on":
            await disabledel(chat.id, True)
            await message.reply(
                lang.disable10
            )
            return lang.disable12.format(True,user)
        elif arg == "off":
            await disabledel(chat.id, False)
            await message.reply(
                lang.disable11
            )
            return lang.disable12.format(False,user)
        else:
            await message.reply(usage)
            return
    if message.command[0] == "list_cmds":
        commands = await get_disabled_commands(chat.id)
        if not commands:
            await message.reply(lang.disable13.format(chat.title))
            return
        txt = lang.disable14.format(chat.title)
        for command in set(commands):
            txt += f"\n‣ `{command}`"
        await message.reply(txt)


async def generate_callback_button(chat_id, user_id):
    dic = await get_all_module_status(chat_id)
    buttons = []
    sorted_list = sorted(DISABLE_ENABLE_MODULES.keys())
    rows = list(zip_longest(*[iter(sorted_list)] * 3, fillvalue=""))
    for row in rows:
        row_buttons = []
        for option in row:
            if option:
                status, callback = dic[option]
                row_buttons.append(
                    InlineKeyboardButton(
                        f"{DISABLE_ENABLE_MODULES[option]['module']} {status}",
                        callback_data=f"module:{callback}:{option}:{user_id}",
                    )
                )
        buttons.append(row_buttons)

    return InlineKeyboardMarkup(buttons)


@app.on_message(custom_filter.command(MODULE_COMMAND))
@admins_stuff(user=True, bot=False)
async def _disable_enable(client, message,lang):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await message.reply(
        lang.disable15,
        reply_markup=await generate_callback_button(chat_id, user_id),
    )


@app.on_callback_query(filters.regex("^module:"))
@language
@loggable
async def _moduleCB(client, query,lang):
    callback, module, user_id = query.data.split(":")[1:]
    from_user = query.from_user
    chat_id = query.message.chat.id
    if from_user.id != int(user_id):
        await query.answer(lang.other6, show_alert=True)
        return
    if callback == "disable":
        DISABLED = True
        await query.answer(lang.disable16)
        await disable_module(chat_id, module)
        btns = await generate_callback_button(chat_id, user_id)
        await query.message.edit_reply_markup(btns)
    elif callback == "enable":
        DISABLED = False
        await query.answer(lang.disable17)
        await enable_module(chat_id, module)
        btns = await generate_callback_button(chat_id, user_id)
    await query.message.edit_reply_markup(btns)
    
    return lang.disable18.format(module,from_user.mention) if DISABLED else lang.disable19.format(module,from_user.mention)



__commands__ = DISABLE_COMMAND + MODULE_COMMAND
__mod_name__ = "𝙳ɪsᴀʙʟᴇ"
__alt_names__ = ["disabling"]


__help__ = """
**⸢ᴅɪsᴀʙʟᴇ/ᴇɴᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 
═───────◇───────═
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /disable <command> : ᴛᴏ ᴅɪsᴀʙʟᴇ ᴀ ᴄᴏᴍᴍᴀɴᴅ.
๏ /enable <command> : ᴛᴏ ᴇɴᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅ.
๏ /module : ᴛᴏ ᴅɪsᴀʙʟᴇ / ᴇɴᴀʙʟᴇ ᴍᴏᴅᴜʟᴇs.
═───────◇───────═
"""