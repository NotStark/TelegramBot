from TeleBot.mongo.chats_db import get_served_chats
from TeleBot.mongo.users_db import get_served_users
from TeleBot import app
from config import DEV_USERS
from strings import get_command
from TeleBot.core import custom_filter 
from pyrogram import filters



@app.on_message(custom_filter.command(get_command("BROADCAST_COMMAND") , disable= False) & filters.user(DEV_USERS))
async def _bcast(client , message):
    replied = message.reply_to_message
    if len(message.command) < 2 or not replied:
        await message.reply("What Should i broadcast?")
    args = message.text.split(message.command[0])
    chats = []
    if '-c' in args:
        chats.extend(await get_served_chats)
    if '-u' in args:
        chats.extend(await get_served_users())

    # if ''
