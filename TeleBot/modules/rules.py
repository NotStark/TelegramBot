from TeleBot import app, BOT_USERNAME
from strings import get_command
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from TeleBot.mongo.rules_db import set_rules, is_rules, clear_rules
from TeleBot.core import custom_filter
from TeleBot.core.functions import connected , is_user_admin
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.log import loggable


SETRULES_COMMAND = get_command("SETRULES_COMMAND")
RMRULES_COMMAND = get_command("RMRULES_COMMAND")
RULES_COMMAND = get_command("RULES_COMMAND")

@app.on_message(custom_filter.command(commands=SETRULES_COMMAND))
@language
@loggable
async def _setrules(client, message,lang):
    user_id = message.sender_chat.id if message.sender_chat else message.from_user.id
    chat = await connected(message,user_id,lang,need_admin=True)
    if not chat:
        return
    if chat and not await is_user_admin(chat.id,user_id,permission="can_change_info"):
        await message.reply(lang.other3.format("can_change_info",chat.title))
        return
    check = await is_rules(chat.id)
    if check:
        await message.reply_text(
            lang.rules1
        )
        return
    if len(message.command) < 2:
        return await message.reply_text(lang.rules2)
    rules = message.text.split(None, 1)[1]
    await set_rules(chat.id, rules)
    await message.reply_text(lang.rules3.format(chat.title))
    return lang.rules4.format(rules,message.from_user.mention if message.from_user else 'Anon',chat.title)


@app.on_message(custom_filter.command(commands=RMRULES_COMMAND))
@language
@loggable
async def _rmrules(client, message,lang):
    user_id = message.sender_chat.id if message.sender_chat else message.from_user.id
    chat = await connected(message,user_id,lang,need_admin=True)
    if not chat:
        return
    if chat and not await is_user_admin(chat.id,user_id,permission="can_change_info"):
        await message.reply(lang.other3.format("can_change_info",chat.title))
        return
    check = await is_rules(chat.id)
    if not check:
        await message.reply_text(
            lang.rules5.format(chat.title)
        )
        return
    await clear_rules(chat.id)
    await message.reply_text(lang.rules6)
    return lang.rules8.format(message.from_user.mention if message.from_user else 'Anon')


@app.on_message(custom_filter.command(commands=RULES_COMMAND))
@language
async def _getrules(client, message,lang):
    user_id = message.sender_chat.id if message.sender_chat else message.from_user.id
    chat = await connected(message,user_id,lang,need_admin=False)
    if not chat:
        return
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=lang.btn20, url=f"t.me/{BOT_USERNAME}?start=rules_{chat.id}"
                )
            ]
        ]
    )
    return await message.reply_text(
        lang.rules7.format(chat.title), reply_markup=btn
    )


__commands__ = SETRULES_COMMAND + RULES_COMMAND + RMRULES_COMMAND
__mod_name__ = "𝚁ᴜʟᴇs"
__alt_names__ = ["rule","rules"]

__help__ = """
**⸢sᴇᴛ ʀᴜʟᴇs ғᴏʀ ʏᴏᴜ ᴄʜᴀᴛ sᴏ ᴛʜᴀᴛ ᴍᴇᴍʙᴇʀs ᴋɴᴏᴡ ᴡʜᴀᴛ ᴛᴏ ᴅᴏ ᴀɴᴅ ᴡʜᴀᴛ ɴᴏᴛ ᴛᴏ ᴅᴏ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ!⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
๏ /rules: ɢᴇᴛ ᴛʜᴇ ʀᴜʟᴇs ғᴏʀ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ.
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /setrules <ʀᴜʟᴇs>: sᴇᴛ ᴛʜᴇ ʀᴜʟᴇs ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ, ᴀʟsᴏ ᴡᴏʀᴋs ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ.
๏ /clearrules or /rmrules: ᴄʟᴇᴀʀ ᴛʜᴇ ʀᴜʟᴇs ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ.

ғᴏʀᴍᴀᴛᴛɪɴɢ:
๏ cʜᴇᴄᴋ /markdownhelp ғᴏʀ ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ғᴏʀᴍᴀᴛᴛɪɴɢ
═───────◇───────═
"""



