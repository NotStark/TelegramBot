import os
import logging
import time 
import sys
import asyncio
import config
import sqlite3
import subprocess
from pyrogram import Client
from rich.table import Table
from rich.console import Console 
from aiohttp import ClientSession
from Python_ARQ import ARQ
from pyrogram.enums import ParseMode


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)


if sys.version_info[0] < 3 and sys.version_info[1] < 6:
    LOG.print("[bold red]ʏᴏᴜ ᴍᴜsᴛ ʜᴀᴠᴇ ᴀ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ ᴏғ 3.6. ᴇxɪᴛɪɴɢ.......\n")
    sys.exit(1)

async def get_readable_time(seconds: int) -> str:
    time_string = ""
    if seconds < 0:
        raise ValueError("Input value must be non-negative")

    if seconds < 60:
        time_string = f"{round(seconds)}s"
    else:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            time_string += f"{round(days)}days, "
        if hours > 0:
            time_string += f"{round(hours)}h:"
        time_string += f"{round(minutes)}m:{round(seconds):02d}s"

    return time_string




MOD_LOAD = []
MOD_NOLOAD = []   
CMD_LIST = [] 
DISABLE_ENABLE_MODULES = {}
BOT_NAME  = ""
BOT_USERNAME = ""
BOT_ID = 0
MENTION_BOT = ""
OWNER_USERNAME = ""
LOGGER = logging.getLogger("FRIDAY")
LOG = Console()
StartTime = time.time()
loop = asyncio.get_event_loop()
aiohttpsession = ClientSession()
arq = ARQ("arq.hamker.dev",config.ARQ_API_KEY, aiohttpsession)
app = Client (name = "TeleBot",api_id = config.API_ID,api_hash = config.API_HASH,bot_token = config.BOT_TOKEN,app_version = "1.0", parse_mode = ParseMode.MARKDOWN)


async def init():
    global BOT_NAME,BOT_USERNAME,BOT_ID
    global OWNER_USERNAME, MENTION_BOT
    LOG.print("[bold red]starting your bot")
    
    try:
        await app.start()
    except sqlite3.OperationalError as e:
        if str(e) == "database is locked" and os.name == "posix":
            LOG.print("[bold red]Session file is locked. Trying to kill blocking process...")
            subprocess.run(["fuser", "-k", "TeleBot.session"])
            os.execvp(sys.executable, [sys.executable, "-m", "TeleBot"])
        raise
    except Exception as e:
        LOG.print(f"[bold red]{e}")
    LOG.print("[bold green] loading sudo users....")   
    # x =  db.sudo.find().to_list(length=None)
    # for i in await x :
    #     config.SUDO_USERS.append(i["user_id"])
    # config.SUPREME_USERS.extend(config.SUDO_USERS)
    # msg = "--ʜᴇʀᴇ ɪs ᴛʜᴇ ʟɪsᴛ ᴏғ sᴜᴅᴏ ᴜsᴇʀs--\n"
    # for m in set(config.SUDO_USERS):
    #     try:
    #         mention = (await pgram.get_users(int(m))).first_name 
    #         msg += f"• {mention}\n"
    #     except Exception as e:
    #         print(e)
    # LOG.print(f"[bold green] loaded sudo users.\n\n{msg}") 
    details = app.me
    BOT_ID = details.id
    BOT_USERNAME = details.username  
    BOT_NAME = details.first_name
    MENTION_BOT = details.mention
    OWNER_USERNAME = (await app.get_users(config.OWNER_ID)).username
    LOG.print("[bold yellow]got all information")


import os
import logging
import time 
import sys
import asyncio
import config
import sqlite3
import subprocess
from pyrogram import Client
from rich.table import Table
from rich.console import Console 
from aiohttp import ClientSession
from Python_ARQ import ARQ
from pyrogram.enums import ParseMode


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)


if sys.version_info[0] < 3 and sys.version_info[1] < 6:
    LOG.print("[bold red]ʏᴏᴜ ᴍᴜsᴛ ʜᴀᴠᴇ ᴀ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ ᴏғ 3.6. ᴇxɪᴛɪɴɢ.......\n")
    sys.exit(1)

async def get_readable_time(seconds: int) -> str:
    time_string = ""
    if seconds < 0:
        raise ValueError("Input value must be non-negative")

    if seconds < 60:
        time_string = f"{round(seconds)}s"
    else:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            time_string += f"{round(days)}days, "
        if hours > 0:
            time_string += f"{round(hours)}h:"
        time_string += f"{round(minutes)}m:{round(seconds):02d}s"

    return time_string




MOD_LOAD = []
MOD_NOLOAD = []   
CMD_LIST = [] 
DISABLE_ENABLE_MODULES = {}
BOT_NAME  = ""
BOT_USERNAME = ""
BOT_ID = 0
MENTION_BOT = ""
OWNER_USERNAME = ""
LOGGER = logging.getLogger("TeleBot")
LOG = Console()
StartTime = time.time()
loop = asyncio.get_event_loop()
aiohttpsession = ClientSession()
arq = ARQ("arq.hamker.dev",config.ARQ_API_KEY, aiohttpsession)
app = Client (name = "TeleBot",api_id = config.API_ID,api_hash = config.API_HASH,bot_token = config.BOT_TOKEN, parse_mode = ParseMode.MARKDOWN,app_version = "1.0")


async def init():
    global BOT_NAME,BOT_USERNAME,BOT_ID
    global OWNER_USERNAME, MENTION_BOT
    LOG.print("[bold yellow]ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴘɪ...")
    try:
        await app.start()
        LOG.print('[bold cyan]ᴄᴏɴɴᴇᴄᴛᴇᴅ')
    except sqlite3.OperationalError as e:
        print(e)
        if str(e) == "database is locked" and os.name == "posix":
            LOG.print("[bold red]Session file is locked. Trying to kill blocking process...")
            subprocess.run(["fuser", "-k", "TeleBot.session"])
            os.execvp(sys.executable, [sys.executable, "-m", "TeleBot"])
        raise
    except Exception as e:
        LOG.print(f"[bold red]{e}")
    details = app.me
    
    BOT_ID = details.id
    BOT_USERNAME = details.username  
    BOT_NAME = details.first_name
    MENTION_BOT = details.mention
    OWNER_USERNAME = (await app.get_users(config.OWNER_ID)).username
    LOG.print("[bold yellow]got all information")

    
    
loop.run_until_complete(init()) 
