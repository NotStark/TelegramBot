from TeleBot import app, BOT_ID
from TeleBot.core.custom_filter import command
from pyrogram import filters, errors
from TeleBot.core.decorators.lang import language
from TeleBot.core.extractions import extract_user_id
from TeleBot.core.functions import get_admins
from TeleBot.core.chat_status import do_admins_stuff
from pyrogram.types import (
    InlineKeyboardButton , 
    InlineKeyboardMarkup , 
    ChatPrivileges 
    )

async def get_chat_privileges(client,message,status):
    chat_id = message.chat.id
    bot = (await client.get_chat_member(chat_id,BOT_ID)).privileges
    PROMOTE_DICT = {
        "normal" : ChatPrivileges(
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_manage_chat=bot.can_manage_chat,
            can_promote_members = False,
            can_manage_video_chats=bot.can_manage_video_chats ),
        "full" :  ChatPrivileges(
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats),
        "mid" : ChatPrivileges(
            can_change_info=False,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=False,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats),
        "low" :  ChatPrivileges(),
    }
    return PROMOTE_DICT[status]


@app.on_message(command(commands="promote"))
@language
async def _promote(client,message, lang):
    x , chat_id = await do_admins_stuff(message,lang, permission= "can_promote_members" , check_bot= True)
    if x is False:
        return
    user_id = await extract_user_id(message)
    chat_id = message.chat.id
    from_user_id = message.sender_chat.id if message.sender_chat else message.from_user.id
    if user_id is None:
        return await message.reply("I ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ ʏᴏᴜ'ʀᴇ ᴛᴀʟᴋɪɴɢ ᴀʙᴏᴜᴛ, ʏᴏᴜ'ʀᴇ ɢᴏɪɴɢ ᴛᴏ ɴᴇᴇᴅ ᴛᴏ sᴘᴇᴄɪғʏ ᴀ ᴜsᴇʀ...!")
    if user_id == BOT_ID:
        return await message.reply("ʙʀᴜʜ ʜᴏᴡ ᴄᴀɴ ɪ ᴘʀᴏᴍᴏᴛᴇ ᴍʏsᴇʟғ.")
    if user_id in await get_admins(chat_id):
        return await message.reply("ʜᴏᴡ ᴀᴍ ɪ ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴛʜᴀᴛ'ꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ?")
    await message.reply_text("ᴄʜᴏᴏꜱᴇ ᴀᴛ ᴡʜᴀᴛ ᴘᴏꜱɪᴛɪᴏɴ ʏᴏᴜ ᴡᴀɴɴᴀ ᴘʀᴏᴍᴏᴛᴇ ᴛʜᴇ ᴜꜱᴇʀ !",reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton("ɴᴏʀᴍᴀʟ ᴘʀᴏᴍᴏᴛᴇ",callback_data =f"promote_normal_{user_id}_{from_user_id}"),InlineKeyboardButton("ꜰᴜʟʟ ᴘʀᴏᴍᴏᴛᴇ",callback_data = f"promote_full_{user_id}_{from_user_id}")],
                                                                                                                       [InlineKeyboardButton("ᴍɪᴅ ᴘʀᴏᴍᴏᴛᴇ",callback_data =f"promote_mid_{user_id}_{from_user_id}"),InlineKeyboardButton("ʟᴏᴡ ᴘʀᴏᴍᴏᴛᴇ",callback_data = f"promote_low_{user_id}_{from_user_id}")],
                                                                                                                       [InlineKeyboardButton("ᴄʟᴏꜱᴇ",callback_data =f"admin_close_{from_user_id}")]
                                                                                                                    ]))




@app.on_callback_query(filters.regex('^promote_'))
async def _promotecb(client, query):
    status,user_id,from_user_id = query.data.split('_')[1:]
    user_id = int(user_id)
    from_user_id = int(from_user_id)
    chat = query.message.chat
    from_user = query.from_user 
    user = await client.get_chat_member(chat.id,user_id)
    if from_user.id != from_user_id:
        await query.answer("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴘᴇʀꜰʀᴏᴍ ᴛʜɪꜱ ᴀᴄᴛɪᴏɴ 🔴.",show_alert=True)
        return
    await query.message.delete()
    for statuss in ["normal","full","low","mid"] :
        if statuss == status :
            chat_rights = await get_chat_privileges(client,query.message,status)
            try:
                await client.promote_chat_member(chat.id,user_id,chat_rights)
              
            except errors.BadRequest as err: 
                if err.MESSAGE == "USER_NOT_PARTICIPANT":
                   await query.message.reply("ɪ ᴄᴀɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇ ꜱᴏᴍᴇᴏɴᴇ ᴡʜᴏ ɪꜱɴ'ᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.")
                   return 
            await client.send_message(chat.id,f"ꜱᴜᴄᴇꜱꜱꜰᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇᴅ {user.user.mention} ɪɴ {chat.title} ᴡɪᴛʜ `{status}` ʀɪɢʜᴛꜱ.",
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="​ᴅᴇᴍᴏᴛᴇ​",callback_data=f"demote_{user_id}_{from_user_id}")],                                                                 
                                                                                [InlineKeyboardButton("ᴄʟᴏꜱᴇ",callback_data =f"admin_close_{from_user_id}")]]))
    return f"#PROMOTED\n\n» **ᴜꜱᴇʀ**: {user.user.mention}\n» **ᴀᴅᴍɪɴ**: {from_user.mention}"
   