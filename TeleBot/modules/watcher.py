from TeleBot import app
from TeleBot.mongo.chats_db import add_served_chat
from TeleBot.mongo.users_db import add_served_user
from TeleBot.mongo.blacklist_chat_db import is_blacklisted
from TeleBot.core.filter_groups import chat_watcher
from TeleBot.core.decorators.lang import language

@app.on_message(group=chat_watcher)
@language
async def _amd(_, message,lang):
    chat = message.chat
    if message.from_user:
        user = message.from_user
        await add_served_user(user.id,user.username)

    if str(message.chat.id).startswith("-"):
        if await is_blacklisted(chat.id):
            await message.reply_text(lang.blchat1)
            return await _.leave_chat(chat.id)
        await add_served_chat(chat.id)
