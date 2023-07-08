import random
import mimetypes
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv('API_ID', '11674810'))
API_HASH = getenv('API_HASH', '9a64eb6bf7a4e8ba17dfa06efe6f2c6c')
BOT_TOKEN = getenv('BOT_TOKEN', '5985531125:AAEb0KmRbhIHa_K0TTkk6o0kOv-ZG_gE6XM')
MONGO_DB_URL = getenv('MONGO_DB_URL', 'mongodb+srv://yeahamstark:fd443sSWOzOZOyZt@cluster0.gfjlssk.mongodb.net/?retryWrites=true&w=majority')
SUPPORT_CHAT = getenv('SUPPORT_CHAT', 'HyugaGuarDianSupport')
UPDATES_CHANNEL = getenv('UPDATES_CHANNEL', 'Supreme_Stark')
OWNER_ID = int(getenv('OWNER_ID', '6246327578'))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID', '-1001953028445'))
DEV_USERS = list(map(int, getenv("DEV_USERS", "6246327578").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "0").split()))
ARQ_API_KEY = getenv('ARQ_API_KEY', 'QXVXTN-JORXPR-DVQAYY-VCTDAC-ARQ')
DONATION_LINK = getenv('DONATION_LINK', 'https://t.me/TheStark')
START_IMG = getenv('START_IMG', '').split()
HELP_IMG = getenv('HELP_IMG', '')
HANDLERS = getenv("HANDLERS", ". /").split()



if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)


