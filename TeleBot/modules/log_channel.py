from TeleBot import app
from TeleBot.core import custom_filter
from pyrogram import enums, errors
from strings import get_command
from TeleBot.mongo.log_channel_db import set_log, unset_log, get_log_channel
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.lang import language


LOGCHANNEL_COMMAND = get_command("LOGCHANNEL_COMMAND")


@app.on_message(custom_filter.command(LOGCHANNEL_COMMAND))
@admins_stuff(user=True,bot=False)
async def _setlog(client, message, lang):
    chat = message.chat
    if message.command[0] == "setlog":
        if chat.type == enums.ChatType.CHANNEL:
            return await message.reply(
                lang.logchannel1
            )
        if message.forward_from_chat:
            channel = message.forward_from_chat
            await set_log(chat.id, channel.id)
            try:
                await client.send_message(
                    channel.id,
                    lang.logchannel2.format(channel.title),
                )
            except errors.ChatWriteForbidden:
                return await message.reply(lang.logchannel3)
        else:
            await message.reply(lang.logchannel4)
    if message.command[0] == "unsetlog":
        result, channel_id = await unset_log(chat.id)
        if result is False:
            return await message.reply(lang.logchannel5)
        await client.send_message(
            channel_id, lang.logchannel6.format(chat.title)
        )

        await message.reply(lang.logchannel17)

    if message.command[0] == "logchannel":
        channel = await get_log_channel(chat.id)
        if not channel:
            return await message.reply(lang.logchannel18)
        await message.reply(
            lang.logchannel19.format((await client.get_chat(channel)).title,channel)
        )


__commands__ = LOGCHANNEL_COMMAND
__mod_name__ = "𝙻ᴏɢ ᴄʜᴀɴɴᴇʟ"
__alt_names__ = ["log"]

__help__ = """
**⸢ʟᴏɢ ɢʀᴏᴜᴘ ᴀᴄᴛɪᴏɴs ᴛᴀᴋᴇɴ ɪɴ ʏᴏᴜʀ ᴅᴇsɪʀᴇᴅ ᴄʜᴀɴɴᴇʟ⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 
═───────◇───────═
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /setlog : ᴛᴏ sᴇᴛ ʟᴏɢ ᴄʜᴀɴɴᴇʟ.
๏ /unsetlog : ᴛᴏ ᴜɴsᴇᴛ ʟᴏɢ ᴄʜᴀɴɴᴇʟ.
๏ /logchannel : ᴛᴏ sᴇᴇ ʟᴏɢ ᴄʜᴀɴɴᴇʟ.
═───────◇───────═
"""