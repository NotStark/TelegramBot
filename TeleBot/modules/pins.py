from TeleBot import app
from pyrogram import filters
from strings import get_command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TeleBot.core import custom_filter
from TeleBot.core.decorators.chat_status import admins_stuff
from TeleBot.core.decorators.lang import language
from TeleBot.core.decorators.log import loggable

PIN_COMMAND = get_command("PIN_COMMAND")
UNPIN_COMMAND = get_command("UNPIN_COMMAND")
PINNED_COMMAND = get_command("PINNED_COMMAND")


@app.on_message(custom_filter.command(commands=PIN_COMMAND))
@admins_stuff("can_pin_messages", bot=True)
@loggable
async def _pin(client, message, lang):
    replied = message.reply_to_message
    user = message.from_user if message.from_user else None
    if not replied:
        await message.reply_text(lang.pin1)
        return
    await replied.pin(disable_notification=True)
    await message.reply_text(
        lang.pin2,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=lang.btn33, url=replied.link),
                    InlineKeyboardButton(
                        text=lang.btn35,
                        callback_data=f"unpin_{user.id if user else 0}_{replied.id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=lang.btn9,
                        callback_data=f"admin_close_{user.id if user else 0}",
                    )
                ],
            ]
        ),
    )
    


@app.on_message(custom_filter.command(commands=PINNED_COMMAND))
@admins_stuff(bot=False, user=True)
async def _pinned(client, message, lang):
    chat = await client.get_chat(message.chat.id)
    user = message.from_user if message.from_user else None
    if not chat.pinned_message:
        return await message.reply_text(
            lang.pin5
        )
    await message.reply_text(
        lang.pin6,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=lang.btn33, url=chat.pinned_message.link
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=lang.btn9, callback_data=f"admin_close_{user.id if user else 0}"
                    )
                ],
            ]
        ),
    )
    


@app.on_message(custom_filter.command(commands=UNPIN_COMMAND))
@admins_stuff("can_pin_messages", bot=True)
@loggable
async def _unpinmsg(client, message, lang):
    user = message.from_user if message.from_user else None
    if message.command[0] == "unpin":
        replied = message.reply_to_message
        if not replied:
            await message.reply_text(
                lang.pin7
            )
            return
        await replied.unpin()
        await message.reply_text(
            lang.pin8,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text=lang.btn33, url=replied.link)],
                    [
                        InlineKeyboardButton(
                            text=lang.btn9, callback_data=f"admin_close_{user.id if user else 0}"
                        )
                    ],
                ]
            ),
        )
        return lang.pin4.format(user.mention if user else 'Anon')
    if message.command[0] == "unpinall":
        await client.unpin_all_chat_messages(message.chat.id)
        await message.reply_text(
            lang.pin9,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            lang.btn9, callback_data=f"admin_close_{user_id}"
                        )
                    ]
                ]
            ),
        )
        return lang.pin10.format(user.mention if user else 'Anon')


@app.on_callback_query(filters.regex(pattern=r"unpin_(.*)"))
@language
@loggable
async def unpin_btn(client, query, lang):
    user = query.from_user
    chat_id = query.message.chat.id
    ids = query.data.split("_")
    if int(ids[1]) == user.id:
        await client.unpin_chat_message(chat_id, int(ids[2]))
        await query.message.edit(lang.pin11)
        return lang.pin4.format(user.first_name)
    else:
        await app.answer_callback_query(
            query.id, text=lang.pin12, show_alert=True
        )


__commands__ = PIN_COMMAND + UNPIN_COMMAND + PINNED_COMMAND
__mod_name__ = "𝙿ɪɴꜱ"
__alt_names__ = ["pinings", "spins"]

__help__ = """
**⸢ᴘɪɴɪɴɢs⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /pin : ᴘɪɴ ᴀ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.
๏ /unpin : ᴜɴᴘɪɴ ᴀ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.
๏ /pinned : ɢᴇᴛ ᴛʜᴇ ʀᴇᴄᴇɴᴛʟʏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ
═───────◇───────═
"""
