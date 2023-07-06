from TeleBot import app, BOT_ID
from TeleBot.core.custom_filter import command
from pyrogram import filters, errors
from TeleBot.core.decorators.lang import language
from TeleBot.core.extractions import extract_user_id
from TeleBot.core.functions import get_admins
from TeleBot.core.decorators.log import loggable
from TeleBot.core.chat_status import do_admins_stuff
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPrivileges


async def get_chat_privileges(client, status , chat_id):
    bot = (await client.get_chat_member(chat_id, BOT_ID)).privileges
    PROMOTE_DICT = {
        "normal": ChatPrivileges(
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_manage_chat=bot.can_manage_chat,
            can_promote_members=False,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
        "full": ChatPrivileges(
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
        "mid": ChatPrivileges(
            can_change_info=False,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=False,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
        "low": ChatPrivileges(),
    }
    return PROMOTE_DICT[status]


@app.on_message(command(commands="promote"))
@language
async def _promote(client, message, lang):
    x, chat_id = await do_admins_stuff(
        message, lang, permission="can_promote_members", check_bot=True
    )
    if x is False:
        return
    user_id = await extract_user_id(message)
    from_user_id = (
        message.sender_chat.id if message.sender_chat else message.from_user.id
    )
    if user_id is None:
        return await message.reply(
            lang.admin1
        )
    if user_id == BOT_ID:
        return await message.reply(lang.admin2)
    if user_id in await get_admins(chat_id):
        return await message.reply(
            lang.admin3
        )
    await message.reply_text(
        lang.admin4,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang.btn5,
                        callback_data=f"promote_normal_{user_id}_{from_user_id}_{chat_id}",
                    ),
                    InlineKeyboardButton(
                        lang.btn6,
                        callback_data=f"promote_full_{user_id}_{from_user_id}_{chat_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        lang.btn7,
                        callback_data=f"promote_mid_{user_id}_{from_user_id}_{chat_id}",
                    ),
                    InlineKeyboardButton(
                        lang.btn8,
                        callback_data=f"promote_low_{user_id}_{from_user_id}_{chat_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        lang.btn9, callback_data=f"admin_close_{from_user_id}"
                    )
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex('^promote_'))
@language
@loggable
async def _promotecb(client, query, lang):
    status, user_id, from_user_id , chat_id = query.data.split('_')[1:] 
    from_user = query.from_user 
    if from_user.id != int(from_user_id):
        await query.answer(lang.other6,show_alert=True)
        return
    user = await client.get_chat_member(int(chat_id),int(user_id))
    print(user , chat_id , user_id)
    await query.message.delete()
    for statuss in ["normal","full","low","mid"] :
        if statuss == status :
            chat_rights = await get_chat_privileges(client, status , user.chat.id)
            try:
                await client.promote_chat_member(user.chat.id,user.id,chat_rights)
              
            except errors.BadRequest as err: 
                if err.MESSAGE == "USER_NOT_PARTICIPANT":
                   await query.message.reply(lang.admin5)
                   return 
            await client.send_message(user.chat.id,lang.admin6.format(user.user.mention,user.chat.title,status),
                                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=lang.btn10,callback_data=f"demote_{user_id}_{from_user_id}_{chat_id}")],                                                                 
                                                                                [InlineKeyboardButton(lang.btn9,callback_data =f"admin_close_{from_user_id}")]]))
    return lang.admin7.format(user.user.mention,from_user.mention)