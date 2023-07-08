import os
import asyncio
import uvloop
import config
import importlib
from pyrogram import idle
from TeleBot import BOT_NAME, app, LOG, CMD_LIST, DISABLE_ENABLE_MODULES, HELPABLE
from rich.table import Table
from TeleBot.core.functions import get_start_media
from pyrogram import __version__ as v
from TeleBot.modules import ALL_MODULES

loop = asyncio.get_event_loop()

SUPPORT_SEND_MSG = """
🥀 {} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ...
┏•❅────✧❅✦❅✧────❅•┓
  **★ ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `1.0`
  **★ ᴩʏʀᴏɢʀᴀᴍ :** `{}`
┗•❅────✧❅✦❅✧────❅•┛
"""


LOG_MSG = "●▬▬▬▬▬▬▬▬▬▬▬▬๑۩ ʀᴏʙᴏᴛ ۩๑▬▬▬▬▬▬▬▬▬▬▬●\n"
LOG_MSG += "ʙᴏᴛ sᴛᴀʀᴛɪɴɢ ...... \n\n"
LOG_MSG += "⊙ ᴀ ᴘᴏᴡᴇʀғᴜʟ ᴘʏʀᴏɢʀᴀᴍ ʙᴀsᴇᴅ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ \n\n"
LOG_MSG += "⊙ ᴘʀᴏɪᴇᴄᴛ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : ʜᴛᴛᴘs://ɢɪᴛʜᴜʙ.ᴄᴏᴍ/NᴏᴛSᴛᴀʀᴋ\n\n"
LOG_MSG += "⊙ ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ:\n"
LOG_MSG += "  @The_Only_God\n"
LOG_MSG += "●▬▬▬▬▬▬▬▬▬▬▬▬๑۩ ʀᴏʙᴏᴛ ۩๑▬▬▬▬▬▬▬▬▬▬▬●"


async def main():
    global HELPABLE, DISABLE_ENABLE_MODULES
    os.system("clear")
    LOG.print(Table(show_header=True, header_style="bold yellow").add_column(LOG_MSG))
    LOG.print("[bold cyan]ʟᴏᴀᴅɪɴɢ ᴍᴏᴅᴜʟᴇꜱ...")
    LOG.print("ꜰᴏᴜɴᴅ {} ᴍᴏᴅᴜʟᴇꜱ\n".format(len(ALL_MODULES)))

    for module_name in ALL_MODULES:
        module = importlib.import_module("TeleBot.modules." + module_name)
        alt_names =  getattr(module, "__alt_names__", [])
        print(alt_names)
        commands = getattr(module, "__commands__", [])
        CMD_LIST.extend(commands)

        if hasattr(module, "__mod_name__") and module.__mod_name__:
            if hasattr(module, "__help__") and module.__help__:
                HELPABLE[module.__mod_name__] = {
                    "help": module.__help__,
                    "alt_names": alt_names.append(
                        module.__mod_name__.lower().replace(" ", "_")
                    ),
                }
            if commands:
                DISABLE_ENABLE_MODULES[module_name] = {
                    "module": module.__mod_name__,
                    "commands": commands,
                }

        LOG.print(f"✨ [bold cyan]ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʟᴏᴀᴅᴇᴅ: [green]{module_name}.py")
    LOG.print(f"[bold red]​🇧​​🇴​​🇹​ ​🇸​​🇹​​🇦​​🇷​​🇹​​🇪​​🇩​ ​🇦​​🇸​ {BOT_NAME}!")

    try:
        media_type, media = await get_start_media()
        caption = SUPPORT_SEND_MSG.format(BOT_NAME, v)
        chat = f"@{config.SUPPORT_CHAT}"
        await app.send_photo(
        chat, photo=media, caption=caption
        ) if media_type == "image" else await app.send_video(
            chat, video=media, caption=caption
        )

    except Exception as e:
        LOG.print(f"[bold red] {e}")
        LOG.print(
            "[bold red]ʙᴏᴛ ɪꜱɴ'ᴛ ᴀʙʟᴇ ᴛᴏ ꜱᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ @{config.SUPPORT_CHAT}!"
        )

    await idle()


if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(main())
    LOG.print("[yellow] stopped client")
