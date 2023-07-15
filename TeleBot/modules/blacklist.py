import re
from TeleBot import app
from pyrogram import filters
from strings import get_command
from TeleBot.mongo.blacklist_db import (
    add_blacklist,
    rm_blacklist,
    set_blacklist_mode,
    get_emoji,
    get_blacklist_mode,
    get_blacklist,
    is_blacklisted,
)
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.lang import language
from TeleBot.core.functions import  get_buttons , get_time_buttons
from TeleBot.core import custom_filter
from pyrogram.types import InlineKeyboardMarkup

ADDBLACKLIST_COMMAND = get_command("ADDBLACKLIST_COMMAND")
UNBLACKLIST_COMMAND = get_command("UNBLACKLIST_COMMAND")
BLACKLISTMODE_COMMAND = get_command("BLACKLISTMODE_COMMAND")
BLACKLISTS_COMMAND = get_command("BLACKLISTS_COMMAND")


@app.on_message(custom_filter.command(commands=ADDBLACKLIST_COMMAND))
@admins_stuff(user=True,bot=False)
async def add_blacklist_command(client, message, lang):
    user = message.from_user
    chat = message.chat
    if len(message.command) < 2:
        await message.reply(lang.blacklist1)
        return
    text = message.text.split(maxsplit=1)[1]
    to_blacklist = list(
        {trigger.strip().lower() for trigger in text.split() if trigger.strip()}
    )
    if len(to_blacklist) == 1:
        if is_blacklisted(to_blacklist[0]):
            await message.reply_text(lang.blacklist2)
            return
        await add_blacklist(chat.id, to_blacklist)
        await message.reply(
            lang.blacklist3.format(to_blacklist[0],chat.title)
        )
        return
    failed = await add_blacklist(chat.id, to_blacklist)
    
    text = lang.blacklist4
    for word in to_blacklist:
        if word not in failed:
            text += f"‣ {word}\n"
    text += lang.blacklist5
    for word in failed:
        text +=  f"‣ {word}\n"
    text += lang.blacklist6
    await message.reply(text)
    return


@app.on_message(custom_filter.command(commands=UNBLACKLIST_COMMAND))
@admins_stuff(user=True,bot=False)
async def unblacklist_command(client, message,lang):
    chat = message.chat
    if len(message.command) < 2:
        return await message.reply(lang.blacklist7)
    text = message.text.split(maxsplit=1)[1]
    to_unblacklist = list({trigger.strip().lower() for trigger in text.split() if trigger.strip()})
    sucess = await rm_blacklist(chat.id, to_unblacklist)
    if sucess == 0:
        return await message.reply(lang.blacklist8)
    return await message.reply(lang.blacklist9.format(sucess))



@app.on_message(custom_filter.command(commands=BLACKLISTMODE_COMMAND))
@admins_stuff(user=True,bot=False)
async def unblacklist_command(client, message, lang):
    '''
    0 : off
    1 : del
    2 : warn
    3 : mute
    4 : kick
    5 : ban
    6 : tban
    7: tmute
    '''
    user_id = message.from_user.id if message.from_user else 0
    buttons = await get_buttons(message,user_id,callback="blacklistmode",get_mode = get_blacklist_mode,get_emoji = get_emoji)
    await message.reply(lang.blacklist10,reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("^blacklistmode_"))
async def blmodeCb(client,query):
    mode,user_id = query.data.split("_")[1:]
    from_user = query.from_user
    chat_id = query.message.chat.id
    if from_user.id != int(user_id):
       return await query.answer("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴘᴇʀꜰʀᴏᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ 🔴.",show_alert=True)

    if mode.startswith("until="):
        until = mode.split("=")[1]
        await set_blacklist_mode(chat_id,(6,until))
        return await query.message.edit(f"ᴀʟʀɪɢʜᴛ ᴀᴍ ɢᴏɴɴᴀ ʙᴀɴ ᴛʜᴀᴛ ᴜꜱᴇʀ ᴡʜᴏ ꜱᴇɴᴅꜱ ʙʟᴀᴄᴋɪʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ ꜰᴏʀ {until}")

    txt = None
    if mode == "0":
        await set_blacklist_mode(chat_id,(0,0))
        txt = "ᴅɪꜱᴀʙʟᴇᴅ ʙʟᴀᴄᴋʟɪꜱᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴏꜰ ᴛʜɪꜱ ᴄʜᴀᴛ"
    if mode == '1':
        await set_blacklist_mode(chat_id,(1,0))
        txt = "ᴀʟʀɪɢʜᴛ ᴀᴍ ɢᴏɴɴᴀ ᴅᴇʟᴇᴛᴇ ᴛʜᴀᴛ ᴍᴇꜱꜱᴀɢᴇ ᴡʜɪᴄʜ ᴄᴏɴᴛᴀɪɴꜱ ʙʟᴀᴄᴋʟɪꜱᴛ ᴡᴏʀᴅꜱ"
    if mode == '2':
        await set_blacklist_mode(chat_id,(2,0))
        txt = "ᴀʟʀɪɢʜᴛ ᴀᴍ ɢᴏɴɴᴀ ᴅᴇʟᴇᴛᴇ ᴛʜᴀᴛ ᴍᴇꜱꜱᴀɢᴇ ᴡʜɪᴄʜ ᴄᴏɴᴛᴀɪɴꜱ ʙʟᴀᴄᴋʟɪꜱᴛ ᴡᴏʀᴅꜱ"
    if mode == '3':
        await set_blacklist_mode(chat_id,(3,0))
        txt = "ᴀʟʀɪɢʜᴛ ᴀᴍ ɢᴏɴɴᴀ ᴍᴜᴛᴇ ᴛʜᴏꜱᴇ ᴜꜱᴇʀꜱ ᴡʜᴏ ꜱᴇɴᴅꜱ ᴀɴʏ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ"
    if mode == '4':
        await set_blacklist_mode(chat_id,(4,0))
        txt = "ᴀʟʀɪɢʜᴛ ᴀᴍ ɢᴏɴɴᴀ ᴍᴜᴛᴇ ᴛʜᴏꜱᴇ ᴜꜱᴇʀꜱ ᴡʜᴏ ꜱᴇɴᴅꜱ ᴀɴʏ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ"
    if mode == '5':
        await set_blacklist_mode(chat_id,(5,0))
        txt = "ᴀʟʀɪɢʜᴛ ᴀᴍ ɢᴏɴɴᴀ ᴍᴜᴛᴇ ᴛʜᴏꜱᴇ ᴜꜱᴇʀꜱ ᴡʜᴏ ꜱᴇɴᴅꜱ ᴀɴʏ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ"
    if mode == '6':
        btn = await get_time_buttons(user_id,"blacklistmode")
        await query.message.edit("**ᴄʜᴏᴏsᴇ ᴠᴀʟᴜᴇ**", reply_markup=btn)
        return
    if mode == '7':
        btn = await get_time_buttons(user_id,"blacklistmode")
        await query.message.edit("**ᴄʜᴏᴏsᴇ ᴠᴀʟᴜᴇ**", reply_markup=btn)
        return
    await query.answer(txt,show_alert=True)
    btns = await get_buttons(query.message,user_id,callback="blacklistmode",get_mode = get_blacklist_mode,get_emoji = get_emoji)
    try:
        await query.message.edit_reply_markup(InlineKeyboardMarkup(btns))
    except:
        pass


# @app.on_message(custom_filter.command(commands=BLACKLISTS_COMMAND))
# @is_user_admin()
# async def _get_blackisted(_, message):
#     chat_id = message.chat.id
#     chat_title = message.chat.title
#     words = await get_blacklist(chat_id)
#     if not words:
#         return await message.reply_text(f"ɴᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ɪɴ {chat_title}")
#     msg = f"**ᴄᴜʀʀᴇɴᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴡᴏʀᴅs ɪɴ {chat_title}**\n"
#     for mm in words:
#         msg += f"⦾ `{mm.capitalize()}`\n"
#     return await message.reply_text(msg)


# @app.on_message(filters.group,group=blacklist_watcher)
# async def _blacklistwatcher(client,message):
#     chat_id = message.chat.id

#     ignore = await prevent_approved(message)
#     if ignore:
#         return

#     words = await get_blacklist(chat_id)
#     if not words:
#         return
#     mode, until = await get_blacklist_mode(chat_id)
#     if mode == 0:
#         return
#     user = message.from_user
#     to_match = message.text or message.caption
#     if not to_match:
#         return
#     to_match = to_match.lower()
#     for trigger in words:
#         pattern = r"( |^|[^\w])" + re.escape(trigger) + r"( |$|[^\w])"
#         if re.search(pattern, to_match, flags=re.IGNORECASE):
#             try:
#                 if mode == 1:
#                     await message.delete()
#                 if mode == 2:
#                 # will do it later
#                     return
#                 if mode == 3:
#                     await message.delete()
#                     await client.restrict_chat_member(chat_id,user.id,ChatPermissions(can_send_messages=False))
#                     return await client.send_message(chat_id,f"ᴍᴜᴛᴇᴅ {user.mention} ꜰᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}!")
#                 if mode == 4:
#                     await message.delete()
#                     await client.ban_chat_member(chat_id,user.id)
#                     await client.unban_chat_member(chat_id,user.id)
#                     return await client.send_message(chat_id,f"ᴋɪᴄᴋᴇᴅ {user.mention} ꜰᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}!")
#                 if mode == 5:
#                     await message.delete()
#                     await client.ban_chat_member(chat_id,user.id)
#                     return await client.send_message(chat_id,f"ʙᴀɴɴᴇᴅ {user.mention} ꜰᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}!")
#                 if mode == 6:
#                     await message.delete()
#                     until2,unit = await until_date(message, until)
#                     await client.ban_chat_member(chat_id, user.id,until_date=until2)
#                     return await client.send_message(chat_id,f"ᴛᴇᴍᴘᴏʀᴀʀʏ ʙᴀɴɴᴇᴅ ({until[0]} {unit}) {user.mention} ꜰᴏʀ ᴜꜱɪɴɢ ʙʟᴀᴄᴋʟɪꜱᴛᴇᴅ ᴡᴏʀᴅ: {trigger}!")
#             except Exception as e:
#                 print(e)
#                 break


__commands__ = ["unblacklist", "addblacklist", "blacklists", "blacklistmode"]
__mod_name__ = "𝙱ʟᴀᴄᴋʟɪꜱᴛ"
