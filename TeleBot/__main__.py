import os
import asyncio
import re
import time
import uvloop
import config
import strings
import importlib
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    )

from pyrogram.errors import BadRequest,Unauthorized 
from pyrogram import filters,idle
from TeleBot.helpers.misc import paginate_modules
from TeleBot import (
    BOT_NAME,
    BOT_USERNAME,     
    app,
    LOG,    
    StartTime,
    get_readable_time,
    CMD_LIST,
    DISABLE_ENABLE_MODULES
    )
from fuzzywuzzy import process
from rich.table import Table
from pyrogram.enums import ParseMode,ChatType
from pyrogram import __version__ as pyrover
from TeleBot.modules import ALL_MODULES
from unidecode import unidecode
from TeleBot.mongo.rules_db import get_rules
from TeleBot.helpers.button_parser import button_markdown_parser
from TeleBot.helpers.custom_filters import command


HELPABLE = {}
loop = asyncio.get_event_loop()

async def main():
    global HELPABLE
    LOG.print(Table(show_header=True, header_style="bold yellow")
              .add_column(strings.LOG_MSG))
    LOG.print("Found {} modules\n".format(len(ALL_MODULES)))
    
    for module_name in ALL_MODULES:
        module = importlib.import_module("TeleBot.modules." + module_name)
        commands = getattr(module, "__commands__", [])
        CMD_LIST.extend(commands)
        
        if hasattr(module, "__mod_name__")  and module.__mod_name__:
            if hasattr(module,"__help__") and module.__help__:
                HELPABLE[module.__mod_name__] = module.__help__
            if commands:
                DISABLE_ENABLE_MODULES[module_name] = {"module" : module.__mod_name__, "commands" : commands}
            

        
        LOG.print(f"✨ [bold cyan]Successfully imported: [green]{module_name}.py")
        
        
        

    LOG.print(f"[bold red]Bot started as {BOT_NAME}!")
    
    try:
        await app.send_photo(f"@{config.SUPPORT_CHAT}",
                             photo=config.START_IMG,
                             caption=strings.SUPPORT_SEND_MSG.format(BOT_NAME, pyrover))
    except Exception as e:
        LOG.print(f"[bold red] {e}")
        LOG.print("[bold red]Bot isn't able to send a message to @{config.SUPPORT_CHAT}!")
    
    await idle()
      
    
# async def send_help(app,chat, text, keyboard=None):
#     if not keyboard:
#         keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))    
#     await app.send_photo(
#         chat_id=chat,
#         photo=config.START_IMG,
#         caption=text,
#         parse_mode=ParseMode.MARKDOWN,      
#         reply_markup=keyboard,
#     )
#     return (text, keyboard)

# @app.on_message(command(commands="start"))
# async def group_start(_, message):    
#     uptime = await get_readable_time((time.time() - StartTime))
#     chat_id = message.chat.id 
#     args = message.text.split()
#     if message.chat.type == ChatType.PRIVATE :

#         if len(args) >= 2:
#             if args[1].startswith("rules_"):
#                 chat_idd = int(args[1].split("_")[1])
#                 rules = await get_rules(chat_idd)
#                 if not rules:
#                     return await _.send_messsage(chat_id,"ᴛʜᴇ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ʜᴀᴠᴇɴ'ᴛ sᴇᴛ ᴀɴʏ ʀᴜʟᴇs ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ ʏᴇᴛ. \nTʜɪs ᴘʀᴏʙᴀʙʟʏ ᴅᴏᴇsɴ'ᴛ ᴍᴇᴀɴ ɪᴛ's ʟᴀᴡʟᴇss ᴛʜᴏᴜɢʜ...!")
#                 chat = await _.get_chat(chat_idd)
#                 try:
#                     txt, button = await button_markdown_parser(rules)       
#                     return await _.send_message(chat_id,f"ᴛʜᴇ ʀᴜʟᴇs ғᴏʀ **{chat.title}** ᴀʀᴇ :\n\n{txt}",reply_markup = InlineKeyboardMarkup(button))
#                 except Exception as e: 
#                     await _.send_message(chat_id,f"ᴛʜᴇ ʀᴜʟᴇs ғᴏʀ **{chat.title}** ᴀʀᴇ :\n\n{rules}")
#                     raise e
            
#             elif args[1].lower() == "help":
#                 await send_help(_,chat_id,strings.HELP_STRINGS) 
#             elif args[1].lower().startswith("ghelp_"):
#                 mod = args[1].lower().split("_", 1)[1]
# #                 try:
#                 mod = mod.replace("_", " ")
# #                 excpet :
# #                     mod = mod
#                 await _.send_photo(
#                     chat_id,
#                     photo = config.START_IMG,
#                     caption = f"{strings.HELP_STRINGS}\n{HELPABLE[mod]}",
#                     reply_markup = InlineKeyboardMarkup(
#                         [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
#                     ),
#                 )
#             # elif args[1][1:].isdigit():
#             #     await send_rules(message,int(args[1]), from_pm=True)

                
#         else:
#             first_name = message.from_user.first_name                        
#             await app.send_photo(
#            chat_id,    
#            photo=config.START_IMG,
#            caption=strings.PM_START_TEXT.format(first_name,BOT_NAME,uptime),
#            reply_markup=InlineKeyboardMarkup(strings.START_BUTTONS),
#            parse_mode=ParseMode.MARKDOWN,                   
#             )
                        
            
#     else:
#         await message.reply_photo(
#                 config.START_IMG,
#                 caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !\n<b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ:</b> <code>{}</code>".format(
#                     uptime
#                 ),
#             parse_mode=ParseMode.HTML,
#             )
                   
             
# @app.on_callback_query(filters.regex(r"help_(.*?)"))
# async def help_button(_,query):    
#     mod_match = re.match(r"help_module\((.+?)\)", query.data)
#     prev_match = re.match(r"help_prev\((.+?)\)", query.data)
#     next_match = re.match(r"help_next\((.+?)\)", query.data)
#     back_match = re.match(r"help_back", query.data) 
               
#     try:
#         if mod_match:
#             module = mod_match.group(1)
#             text = (
#                 "» **ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ** **{}** :\n".format(
#                     HELPABLE[module].__mod_name__
#                 )
#                 + HELPABLE[module].__help__
#             )
#             await query.message.edit_caption(
#                 text,
#                 parse_mode=ParseMode.MARKDOWN,                
#                 reply_markup=InlineKeyboardMarkup(
#                     [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
#                 ),
#             )

#         elif prev_match:
#             curr_page = int(prev_match.group(1))
#             await query.message.edit_caption(
#                 strings.HELP_STRINGS,
#                 parse_mode=ParseMode.MARKDOWN,
#                 reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELPABLE, "help")
#              ),
#           )
                                   
#         elif next_match:
#             next_page = int(next_match.group(1))
#             await query.message.edit_caption(
#                 strings.HELP_STRINGS,
#                 parse_mode=ParseMode.MARKDOWN,
#                 reply_markup=InlineKeyboardMarkup(
#                     paginate_modules(next_page + 1, HELPABLE, "help")
#                 ),
#             )                   

#         elif back_match:
#            await query.message.edit_caption(
#                 strings.HELP_STRINGS,
#                 parse_mode=ParseMode.MARKDOWN,
#                 reply_markup=InlineKeyboardMarkup(
#                     paginate_modules(0, HELPABLE, "help")
#                 ),
#             )            

#         return await _.answer_callback_query(query.id)

#     except BadRequest:
#         pass

# @app.on_message(command(commands="help"))
# async def get_help(_, message):
#     chat_id = message.chat.id
#     args = message.text.split(None,1)
#     chat_type = message.chat.type
#     if chat_type != ChatType.PRIVATE:
#         if len(args) >= 2 and process.extractOne(args[1].lower(),MODULES.keys())[0] in MODULES.keys():
#             module = process.extractOne(args[1].lower(),MODULES.keys())[0].replace(" ","_")
#             await message.reply_photo(
#                 photo = config.HELP_IMG,
#                 caption= f"Contact me in PM to get help of {module.capitalize().replace('_',' ')}",
#                 reply_markup=InlineKeyboardMarkup(
#                     [
#                         [
#                             InlineKeyboardButton(
#                                 text="ʜᴇʟᴘ",
#                                 url=f"https://t.me/{BOT_USERNAME}?start=ghelp_{module}"
#                             )
#                         ]
#                     ]
#                 ),
#             )
#             return
#         await message.reply_photo(
#             photo = config.HELP_IMG,
#             caption="ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴩ.",
#             reply_markup=InlineKeyboardMarkup(
#                 [
#                     [
#                         InlineKeyboardButton(
#                             text="ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ",
#                             url="https://t.me/{}?start=help".format(
#                                 BOT_USERNAME
#                             ),
#                         )
#                     ],
                    
#                 ],
#             ),
#         )
#         return

#     elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
#         module = args[1].lower()
#         text = (
#             "Here is the available help for the *{}* module:\n".format(
#                 HELPABLE[module].__mod_name__
#             )
#             + HELPABLE[module].__help__
#         )
#         await send_help(
#             _,
#             chat_id,
#             strings.HELP_STRINGS,
#             InlineKeyboardMarkup(
#                 [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
#             ),
#         )

#     else:
#         await send_help(_,chat_id,strings.HELP_STRINGS)

                              
                     
# @app.on_message(command(commands="donate"))  
# async def donate(_, message):
#     if message.from_user.id == config.OWNER_ID:
#         return await message.reply_text("ɪ ᴀᴍ ғʀᴇᴇ ᴛᴏ ᴜsᴇ ┌⁠(⁠・⁠。⁠・⁠)⁠┘⁠♪") 

#     if message.chat.type == ChatType.PRIVATE:
#          await message.reply_text(f"Yᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴘᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ [ʜᴇʀᴇ]({config.DONATION_LINK})")                                                
#     else:
#         await message.reply_text("I'ᴠᴇ PM'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!")
#         try:
#             await app.send_message(message.from_user.id,text=f"[ʜᴇʀᴇ ɪs ᴛʜᴇ ᴅᴏɴᴀᴛɪᴏɴ ʟɪɴᴋ]({config.DONATION_LINK})")
#         except Unauthorized:                
#             await message.reply_text("Cᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ PM ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ")                                                                                               
                                                                    
         
if __name__ == "__main__" :
    uvloop.install()
    loop.run_until_complete(main())
    LOG.print("[yellow] stopped client") 
