from TeleBot import app, BOT_ID
from pyrogram import filters, enums
from strings import get_command
from TeleBot.core import custom_filter
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.log import loggable
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TeleBot.mongo.reports_db import get_report, on_off_reports
from TeleBot.core.functions import is_user_admin, is_invincible


REPORTS_COMMAND = get_command("REPORTS_COMMAND")
REPORT_COMMAND = get_command("REPORT_COMMAND")

@app.on_message(custom_filter.command(REPORTS_COMMAND))
@language
@loggable
async def _reports(client, message, lang):
    chat = message
    if chat.type == enums.ChatType.PRIVATE:
        if len(message.command) < 2:
            await message.reply(lang.report1.format(await get_report(chat.id)))
            return
        arg = message.command[1].lower()
        if arg in ("on", "yes"):
            status = True
            await message.reply(lang.report2)
        if arg in ("no", "off"):
            status = False
            await message.reply(lang.report3)
        await on_off_reports(chat.id, status)
        return
    permission = "can_change_info"
    if not await is_user_admin(
        chat.id,
        message.sender_chat.id if message.sender_chat else message.from_user.id,
        permission=permission,
    ):
        await message.reply(lang.other3.format(permission))
    if len(message.command) < 2:
        await message.reply(lang.report4.format(await get_report(chat.id)))
        return
    arg = message.command[1].lower()
    if arg in ("on", "yes"):
        status = True
        await message.reply(lang.report5)
    if arg in ("no", "off"):
        status = False
        await message.reply(lang.report6)
    await on_off_reports(chat.id, status)
    return lang.report7.format(
        status, message.from_user.mention if message.from_user else "Anon"
    )


@app.on_message(
    (
        custom_filter.command(REPORT_COMMAND)
        | custom_filter.command(commands="admins", prefixes="@")
    )
    & filters.group
)
@language
@loggable
async def _report(client, message, lang):
    chat = message.chat
    replied = message.reply_to_message
    if await get_report(chat.id) is not True:
        return
    if message.sender_chat is not None:
        reported = lang.report8
        async for m in client.get_chat_members(
            chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            if not m.user.is_bot:  # ignoring bots
                reported += f'<a href="tg://user?id={m.user.id}">\u2063</a>'
        await message.reply_text(reported, parse_mode=enums.ParseMode.HTML)
        return
    user = message.from_user
    if await is_user_admin(chat.id, user.id):
        await message.reply(lang.report10)
    if replied:
        reported_user = replied.from_user
        if len(message.command) == 1:
            await message.reply_text(lang.report11)
            return
        elif user.id == reported_user.id:
            await message.reply_text(lang.report12)
            return
        elif reported_user.id == BOT_ID:
            await message.reply_text(lang.report13)
            return
        elif await is_invincible(reported_user.id):
            await message.reply_text(lang.report14)
            return
        reason = message.text.split(maxsplit=1)[1]
        msg = lang.report15.format(
            chat.title, user.mention, reported_user.mention, reason
        )
        link = replied.link
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        lang.btn30,
                        callback_data=f"report_{chat.id}_kick_{reported_user.id}",
                    ),
                    InlineKeyboardButton(
                        lang.btn31,
                        callback_data=f"report_{chat.id}_ban_{reported_user.id}",
                    ),
                    InlineKeyboardButton(
                        lang.btn32,
                        callback_data=f"report_{chat.id}_mute_{reported_user.id}",
                    ),
                ],
                [
                    InlineKeyboardButton(lang.btn33, url=link),
                    InlineKeyboardButton(
                        lang.btn34,
                        callback_data=f"report_{chat.id}_delete_{replied.id}",
                    ),
                ],
                [InlineKeyboardButton(lang.btn9, callback_data="close_btn")],
            ]
        )
        failed = 0
        async for admin in client.get_chat_members(
            chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            if not admin.user.is_bot:
                if await get_report(admin.user.id) is True:
                    try:
                        await client.send_message(admin.user.id, msg, reply_markup=btn)
                    except Exception:
                        failed += 1
        await message.reply_text(
            lang.report16.format(user.mention,failed)
        )
        return lang.report9.format(user.mention, reported_user.mention, reason)
    else:
        await message.reply(lang.report17)
        return


# @app.on_callback_query(filters.regex(pattern=r"report_(.*)"))
# @language
# async def _reportCb(client, query,lang):
#     data = query.data.split("_")
#     user_id = int(data[3])
#     mention = query.from_user.mention
#     chat_id = int(data[1])
#     r_type = data[2]
#     if type == "kick":
#         try:
#             await client.ban_chat_member(chat_id,user_id)
#             await client.unban_chat_member(chat_id,user_id)
#             await client.send_message(chat_id, f"[{first_name}](tg://user?id={user_id}) ᴡᴀs ᴋɪᴄᴋᴇᴅ ʙʏ {mention}")
#             await query.answer("✅ sᴜᴄᴄᴇsғᴜʟʟʏ ᴋɪᴄᴋᴇᴅ")
#         except Exception as e:
#            return await _.send_message(query.message.chat.id,f"ᴇʀʀᴏʀ : {e}")
#     if r_type == "ban":
#         try:
#             await client.ban_chat_member(chat_id,user_id)
#             await client.send_message(chat_id, f"[{first_name}](tg://user?id={user_id}) ᴡᴀs ʙᴀɴɴᴇᴅ ʙʏ {mention}")
#             await query.answer("✅ sᴜᴄᴄᴇsғᴜʟʟʏ ʙᴀɴɴᴇᴅ")
#         except Exception as e:
#            return await client.send_message(query.message.chat.id,f"ᴇʀʀᴏʀ : {e}")
#     if r_type == "mute":
#         try:
#             await client.restrict_chat_member(chat_id,user_id,ChatPermissions())
#             await client.send_message(chat_id, f"[{first_name}](tg://user?id={user_id}) ᴡᴀs ʀᴇsᴛʀɪᴄᴛᴇᴅ ʙʏ {mention}")
#             return await query.answer("✅ sᴜᴄᴄᴇsғᴜʟʟʏ ʀᴇsᴛʀɪᴄᴛᴇᴅ")
#         except Exception as e:
#            return await client.send_message(query.message.chat.id,f"ᴇʀʀᴏʀ : {e}")
#     if r_type == "delete":
#         try:
#             await client.delete_messages(chat_id,user_id)
#             await query.answer("✅ sᴜᴄᴄᴇsғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇ")
#         except Exception as e:
#            return await _.send_message(query.message.chat.id,f"ᴇʀʀᴏʀ : {e}")



__commands__ = REPORTS_COMMAND + REPORT_COMMAND
__alt_names__ = ["reportings"]
__mod_name__ = "𝚁ᴇᴘᴏʀᴛ"

__help__ = """
**⸢ʀᴇᴘᴏʀᴛ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ ᴀᴅᴍɪɴs⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 
═───────◇───────═
๏ /report <reason>: ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴀᴅᴍɪɴꜱ.
๏ @admin: ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴀᴅᴍɪɴs.
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /reports <on/off>: ᴄʜᴀɴɢᴇ ʀᴇᴘᴏʀᴛ sᴇᴛᴛɪɴɢ, ᴏʀ ᴠɪᴇᴡ ᴄᴜʀʀᴇɴᴛ ꜱᴛᴀᴛᴜꜱ.
  • ɪғ ᴅᴏɴᴇ ɪɴ ᴘᴍ, ᴛᴏɢɢʟᴇꜱ ʏᴏᴜʀ ꜱᴛᴀᴛᴜꜱ.
  • ɪғ ɪɴ ɢʀᴏᴜᴘ, ᴛᴏɢɢʟᴇꜱ ᴛʜᴀᴛ ɢʀᴏᴜᴘꜱ ꜱᴛᴀᴛᴜꜱ
═───────◇───────═
"""


