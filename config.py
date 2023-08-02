from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv('API_ID', ''))
API_HASH = getenv('API_HASH', '')
BOT_TOKEN = getenv('BOT_TOKEN', '')
MONGO_DB_URL = getenv('MONGO_DB_URL', '')
SUPPORT_CHAT = getenv('SUPPORT_CHAT', '')
UPDATES_CHANNEL = getenv('UPDATES_CHANNEL', '')
OWNER_ID = int(getenv('OWNER_ID', ''))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID', ''))
DEV_USERS = list(map(int, getenv("DEV_USERS", "").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
ARQ_API_KEY = getenv('ARQ_API_KEY', '')
DONATION_LINK = getenv('DONATION_LINK', '')
START_IMG = getenv('START_IMG', '').split()
HELP_IMG = getenv('HELP_IMG', '').split()
HANDLERS = getenv("HANDLERS", ". /").split()



if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)


