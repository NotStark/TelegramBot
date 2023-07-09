import os
from TeleBot import app,DISABLE_ENABLE_MODULES
from pyrogram import filters
from config import HANDLERS
from TeleBot.helpers.decorators.chat_status import is_user_admin
from TeleBot import CMD_LIST
from TeleBot.mongo.disable_db import add_disable, rm_disable, get_all_module_status, disable_module, enable_module,disabledel, get_disabled_commands
from itertools import zip_longest
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    )
from TeleBot.core import custom_filter


@app.on_message(filters.command(["disable","enable","disabledel","list_cmds"]))
@is_user_admin()
async def _disable_enable(client,message):
    chat_id = message.chat.id
    if message.command[0] == "disable":
        if len(message.command) < 2 :
            return await message.reply("ᴡʜᴀᴛ ꜱʜᴏᴜʟᴅ ɪ ᴅɪꜱᴀʙʟᴇ")
        args = message.command[1].lower()
        for HANDLER in HANDLERS:
            if args.startswith(HANDLER):
                args = args[1:]
        if args not in CMD_LIST:
            return await message.reply("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴅᴏᴇꜱᴛ ᴇᴠᴇɴ ᴇxɪꜱᴛꜱ ʜᴏᴡ ᴄᴀɴ ɪ ᴅɪꜱᴀʙʟᴇ ɪᴛ")
        await add_disable(chat_id,args)

        await message.reply(f"ꜱᴜᴄᴇꜱꜱ ᴅɪꜱᴀʙʟᴇᴅ ᴛʜᴇ ᴜꜱᴇ ᴏꜰ `{args}`")
    if message.command[0] == 'enable':
        args = message.command[1].lower()
        for HANDLER in HANDLERS:
            if args.startswith(HANDLER):
                args = args[1:]
        if args not in CMD_LIST:
            return await message.reply("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴅᴏᴇꜱᴛ ᴇᴠᴇɴ ᴇxɪꜱᴛꜱ ʜᴏᴡ ᴄᴀɴ ɪ ᴇɴᴀʙʟᴇ ɪᴛ")
    
        sucess = await rm_disable(chat_id,args)
        if sucess is False :
            await message.reply("ᴄᴏᴍᴍᴀɴᴅ ᴡᴀꜱɴ'ᴛ ᴅɪꜱʙʟᴇᴅ")
            return 
        await message.reply(f"ꜱᴜᴄᴇꜱꜱ ᴅɪꜱᴀʙʟᴇᴅ ᴛʜᴇ ᴜꜱᴇ ᴏꜰ `{args}`")
    if message.command[0] == "disabledel":
        usage = "ᴜꜱᴀɢᴇ /ᴅɪꜱᴀʙʟᴇᴅᴇʟ [ᴏɴ/ᴏꜰꜰ]"
        if len(message.command) < 2:
            return await message.reply(usage)
        arg = message.command[1].lower()
        if arg == "on":
            await disabledel(chat_id,True)
            return await message.reply("ᴏᴋ ᴡᴏɴ'ᴛ ɴᴏᴡ ɪ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴅɪꜱᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴡʜɪᴄʜ ᴀʀᴇ ᴜꜱᴇᴅ ʙʏ ɴᴏɴ-ᴀᴅᴍɪɴꜱ")
        elif arg == "off" :
            await disabledel(chat_id,False)
            return await message.reply("ᴏᴋ ɴᴏᴡ ɪ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴅɪꜱᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴡʜɪᴄʜ ᴀʀᴇ ᴜꜱᴇᴅ ʙʏ ɴᴏɴ-ᴀᴅᴍɪɴꜱ")
        else:
            return await message.reply(usage)
    if message.command[0] == "list_cmds" :
        commands = await get_disabled_commands(chat_id)
        if not commands:
            return await message.reply("ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴄᴏᴍᴍᴀɴᴅ ᴅɪꜱᴀʙʟᴇᴅ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ")
        txt = f"ʜᴇʀᴇ ɪꜱ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ᴄᴏᴍᴍᴀᴅꜱ ᴛʜᴀᴛ ᴀʀᴇ ᴅɪꜱᴀʙʟᴇᴅ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ:"
        for command in set(commands):
            txt += f"\n‣ `{command}`"
        await message.reply(txt)





async def generate_callback_button(chat_id ,user_id):
    dic = await get_all_module_status(chat_id)
    buttons = []
    sorted_list = sorted(DISABLE_ENABLE_MODULES.keys())
    rows = list(zip_longest(*[iter(sorted_list)] * 3, fillvalue=''))
    for row in rows:
        row_buttons = []
        for option in row:
            if option:
                status, callback = dic[option]
                row_buttons.append(InlineKeyboardButton(f"{DISABLE_ENABLE_MODULES[option]['module']} {status}", callback_data=f"module:{callback}:{option}:{user_id}"))
        buttons.append(row_buttons)

    return InlineKeyboardMarkup(buttons)



@app.on_message(filters.command("modules"))
@is_user_admin()
async def _disable_enable(client,message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await message.reply("ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪꜱᴀʙʟᴇ ᴀ ᴍᴏᴅᴜʟᴇ",reply_markup = await generate_callback_button(chat_id,user_id))


@app.on_callback_query(filters.regex("^module:"))
async def _moduleCB(client, query):
    callback , module , user_id = query.data.split(":")[1:]
    from_user = query.from_user
    chat_id = query.message.chat.id
    if from_user.id != int(user_id):
       return await query.answer("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴘᴇʀꜰʀᴏᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ 🔴.",show_alert=True)
    if callback == "disable" :
        await query.answer("ᴅɪꜱᴀʙʟɪɴɢ...")
        await disable_module(chat_id,module)
        btns = await generate_callback_button(chat_id,user_id)
        await query.message.edit_reply_markup(btns)
    elif callback == "enable":
        await query.answer("ᴇɴᴀʙʟɪɴɢ...")
        await enable_module(chat_id,module)
        btns = await generate_callback_button(chat_id,user_id)
    await query.message.edit_reply_markup(btns)
