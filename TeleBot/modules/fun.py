import random
from TeleBot import pgram
from TeleBot.modules.fun_strings import *

from pyrogram import filters 

@pgram.on_message(filters.command("toss"))
async def _run(_, message):
    await message.reply_text(random.choice(TOSS))             


@pgram.on_message(filters.command("runs"))
async def _run(_, message):
    await message.reply_text(random.choice(RUN_STRINGS))             


@pgram.on_message(filters.command("dice"))
async def _run(_, message):
    chat_id = message.chat.id
    await pgram.send_dice(chat_id, "๐ฒ")


@pgram.on_message(filters.command("dart"))
async def _run(_, message):
    chat_id = message.chat.id
    await pgram.send_dice(chat_id, "๐ฏ")

@pgram.on_message(filters.command("slot"))
async def _run(_, message):
    chat_id = message.chat.id
    await pgram.send_dice(chat_id, "๐ฐ")


@pgram.on_message(filters.command("football"))
async def _run(_, message):
    chat_id = message.chat.id
    await pgram.send_dice(chat_id, "โฝ")


@pgram.on_message(filters.command("basket"))
async def _run(_, message):
    chat_id = message.chat.id
    await pgram.send_dice(chat_id, "๐")


@pgram.on_message(filters.command("bowling"))
async def _run(_, message):
    chat_id = message.chat.id
    await pgram.send_dice(chat_id, "๐ณ")


__help__ = """
**โธขษชแด's แดแดsแด แด าแดษด แดแดแดแดสแด แดษดแดแดสโธฅ**

ใ๐๐ข๐ ๐ ๐๐ก๐๐ฆใ :
โโโโโโโโโโโโโโโโโ
เน /dice
เน /dart
เน /slot
เน /football
เน /basket
เน /bowling
เน /toss
เน /runs
โโโโโโโโโโโโโโโโโ
"""

__mod_name__ = "๐ตแดษด"

