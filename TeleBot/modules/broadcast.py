from TeleBot.mongo.chats_db import get_served_chats
from TeleBot.mongo.users_db import get_served_users
from TeleBot import app
from strings import get_command
from TeleBot.core import custom_filter 
from pyrogram import filters


@app.on_message(filters.command(""))