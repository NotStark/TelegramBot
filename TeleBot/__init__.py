import os
import logging
import time 
import asyncio
import config
import sqlite3
import subprocess
from pyrogram import Client
from rich.table import Table
from rich.console import Console 
from Python_ARQ import ARQ
from pyrogram.enums import ParseMode


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)


# --- VARS ---
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
app = Client (name = "TeleBot",api_id = config.API_ID,api_hash = config.API_HASH,bot_token = config.BOT_TOKEN,app_version = "1.0", parse_mode = ParseMode.MARKDOWN)
# --- VARS ---

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
    LOG.print(f'[bold yellow]ʏᴏᴜʀ ʙᴏᴛ ɪɴꜰᴏ...\n‣ ʙᴏᴛ ɪᴅ: {BOT_NAME}\n‣ ʙᴏᴛ ɴᴀᴍᴇ: {BOT_NAME}\n‣ ʙᴏᴛ ᴜꜱᴇʀɴᴀᴍᴇ: {BOT_USERNAME}')
    OWNER_USERNAME = (await app.get_users(config.OWNER_ID)).username

    
    
loop.run_until_complete(init()) 
