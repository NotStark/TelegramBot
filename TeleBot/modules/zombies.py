import time
import asyncio
from strings import get_command
from TeleBot import app
from TeleBot.core.functions import get_readable_time
from pyrogram import filters,errors
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core import custom_filter
from TeleBot.core.decorators.log import loggable

ZOMBIES = {}
ZOMBIE_COMMAND = get_command("ZOMBIE_COMMAND")

@app.on_message(custom_filter.command(commands=ZOMBIE_COMMAND))
@admins_stuff("can_restrict_members",bot=True)
async def _zombies(client,message,lang):      
    text = await message.reply(lang.zombies1)  
    chat_id = message.chat.id
    zombies = set()
    async for member in client.get_chat_members(chat_id) :          
        user = member.user        
        if user.is_deleted:            
            zombies.add(member.user.id) 
    if len(zombies) == 0:
         return await text.edit(lang.zombies2.format(message.chat.title))
    
    await text.edit(lang.zombies3.format(len(zombies),message.chat.title),reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(lang.btn19, callback_data=f"zombies_clean"),InlineKeyboardButton(lang.btn9, callback_data=f"admin_close_{message.from_user.id if message.from_user else 0}")]]))
    ZOMBIES[chat_id] = zombies


@app.on_callback_query(filters.regex("zombies_clean"))
@admins_stuff("can_restrict_members",bot=True)
@loggable
async def _clean_zombies(client,query,lang):
    chat = query.message.chat
    zombies = ZOMBIES[chat.id]
    if not ZOMBIES.get(chat.id) or len(ZOMBIES[chat.id]) == 0:
        await query.message.edit(lang.zombies2.format(chat.title))
        return
    start = time.time()
    sucess = 0
    failed = 0
    for i in zombies :
        try:                         
            await client.ban_chat_member(chat.id,i)           
            sucess += 1                
        except errors.FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            failed += 1
    end = await get_readable_time((time.time() - start))         
    await query.message.edit(lang.zombies4.format(sucess,chat.title,failed,end))
    ZOMBIES.pop(chat.id)
    return lang.zombies5.format(sucess,query.from_user.mention,)




__commands__ = ZOMBIE_COMMAND
__mod_name__ = "𝚉ᴏᴍʙɪᴇs"
__alt_names__ = ["zombies","dedusers"]

__help__ = """
**⸢ᴄʟᴇᴀɴ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴊᴜꜱᴛ ᴏɴᴇ ᴄᴏᴍᴍᴀɴᴅ⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
❂ /zombies : ᴛᴏ ᴄʟᴇᴀɴ ʏᴏᴜʀ ᴄʜᴀᴛꜱ
═───────◇───────═
"""
