from TeleBot import app
from pyrogram import filters , enums
from strings import get_command
from TeleBot.core import custom_filter
from pyrogram.types import CallBackQuery
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.log import loggable

REPORTS_COMMAND = get_command("REPORTS_COMMAND")

@app.on_message(custom_filter.command(REPORTS_COMMAND))
@language
@loggable
async def _reports(client , update , lang):
    user_id  = update.sender_chat.id if update.sender_chat else update.from_user.id
    if isinstance(update, CallBackQuery):
        pass
    if update.chat.type == enums.ChatType.PRIVATE:
        if len(update.command) < 2:
            await update.reply()
        await update.reply(lang.report2,reply_markup = )
    
