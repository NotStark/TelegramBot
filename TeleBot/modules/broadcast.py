from TeleBot.mongo.chats_db import get_served_chats , remove_served_chat
from TeleBot.mongo.users_db import get_served_users
from TeleBot.core.functions import get_readable_time
from TeleBot import app
import asyncio
import time
from pyrogram.errors import ChatWriteForbidden, FloodWait
from config import DEV_USERS
from strings import get_command
from TeleBot.core import custom_filter
from pyrogram import filters


@app.on_message(custom_filter.command(get_command("BROADCAST_COMMAND"), disable=False) & filters.user(DEV_USERS))
async def _bcast(client, message):
    replied = message.reply_to_message
    txt = await message.reply("Broadcasting...")
    if len(message.command) < 2 and not replied:
        await txt.edit("What should I broadcast?")
        return
    chats = []
    start = time.time()
    pin = '-pin' in message.text
    pin_loud = '-loud' in message.text

     
    if '-c' in message.text:
        chats.extend(await get_served_chats())
    elif '-u' in message.text:
        chats.extend(await get_served_users())
    else:
        chats.extend(await get_served_chats() + await get_served_users())
    
    async def bcast():
        failed = 0
        for chat in chats:
            try:
                if replied:
                    msg = await client.forward_messages(chat, message.chat.id, replied.id)
                else:
                    await client.send_message(chat, message.text.split(maxsplit = 1)[1])
                if pin_loud:
                    try:
                        await msg.pin(disable_notification=False)
                    except:
                        pass
                elif pin:
                    try:
                        await msg.pin()
                    except:
                        pass
            except FloodWait as e:
                await asyncio.sleep(e.x) 
            except ChatWriteForbidden:
                await client.leave_chat(chat)
                await remove_served_chat(chat)
                failed += 1
            except Exception:
                failed += 1
        return failed
    failed_count = await bcast()
    if failed_count:
        await txt.edit(f"Broadcast completed with {failed_count} failures.")
    else:
        await txt.edit(f"Broadcast completed successfully.Time took: {await get_readable_time(time.time() - start)}")
