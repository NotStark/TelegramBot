from TeleBot import app, BOT_ID
from pyrogram import filters, enums
from strings import get_command
from TeleBot.core import custom_filter
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.log import loggable
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
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
    if message.sender_chat or replied and len(message.command) == 1:
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
        return
    if replied:
        reported_user = replied.from_user
        if user.id == reported_user.id:
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
        await message.reply_text(lang.report16.format(user.mention, failed))
        return lang.report9.format(user.mention, reported_user.mention, reason)
    else:
        await message.reply(lang.report17)
        return


@app.on_callback_query(filters.regex(pattern=r"report_(.*)"))
@language
@loggable
async def _reportCb(client, query, lang):
    chat_id, r_type, content = query.data.split("_")[1:]
    chat_id = int(chat_id)
    content = int(content)
    if r_type != "delete":
        permssion = "can_restrict_members"
        if not await is_user_admin(chat_id, query.from_user.id, permission=permssion):
            await query.message.edit(
                lang.other3.format(permssion, (await client.get_chat(chat_id)).title)
            )
            return
        member = await client.get_chat_member(chat_id, content)
        text = lang.report18
        if r_type == "kick":
            await client.ban_chat_member(chat_id, content)
            await client.unban_chat_member(chat_id, content)
            await query.message.edit(lang.report19)
            return text.format(
                member.user.mention, "ᴋɪᴄᴋᴇᴅ", query.from_user.first_name
            )
        if r_type == "ban":
            await client.ban_chat_member(chat_id, content)
            await query.message.edit(lang.report19.replace("ᴋɪᴄᴋᴇᴅ", "ʙᴀɴɴᴇᴅ"))
            return text.format(
                member.user.mention, "ʙᴀɴɴᴇᴅ", query.from_user.first_name
            )
        if r_type == "mute":
            await client.restrict_chat_member(chat_id, content, ChatPermissions())
            await query.message.edit(lang.report19.replace("ᴋɪᴄᴋᴇᴅ", "ʀᴇsᴛʀɪᴄᴛᴇᴅ"))
            return text.format(
                member.user.mention, "ʀᴇsᴛʀɪᴄᴛᴇᴅ", query.from_user.first_name
            )
    else:
        permssion = "can_delete_messages"
        if not await is_user_admin(chat_id, query.from_user.id, permission=permssion):
            await query.message.edit(
                lang.other3.format(permssion, (await client.get_chat(chat_id)).title)
            )
            return
        await client.delete_messages(chat_id, content)
        await query.message.edit("✅ sᴜᴄᴄᴇsғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇ")
        return


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
