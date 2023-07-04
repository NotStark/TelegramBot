from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv('API_ID', '11674810'))
API_HASH = getenv('API_HASH', '9a64eb6bf7a4e8ba17dfa06efe6f2c6c')
BOT_TOKEN = getenv('BOT_TOKEN', '5985531125:AAEb0KmRbhIHa_K0TTkk6o0kOv-ZG_gE6XM')
MONGO_DB_URL = getenv('MONGO_DB_URL', 'mongodb+srv://yeahamstark:fd443sSWOzOZOyZt@cluster0.gfjlssk.mongodb.net/?retryWrites=true&w=majority')
SUPPORT_CHAT = getenv('SUPPORT_CHAT', 'HyugaGuarDianSupport')
UPDATES_CHANNEL = getenv('UPDATES_CHANNEL', 'Supreme_Stark')
OWNER_ID = int(getenv('OWNER_ID', '6143396841'))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID', '-1001953028445'))
DEV_USERS = list(map(int, getenv("DEV_USERS", "1137851706 6143396841").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "0").split()))
ARQ_API_KEY = getenv('ARQ_API_KEY', 'QXVXTN-JORXPR-DVQAYY-VCTDAC-ARQ')
DONATION_LINK = getenv('DONATION_LINK', 'https://t.me/TheStark')
START_IMG = getenv('START_IMG')
HELP_IMG = getenv('HELP_IMG')


if not START_IMG:
    START_IMG = "https://i.pinimg.com/564x/01/d6/ae/01d6ae16511ce7d7db7aef7844c119ea.jpg"

if not HELP_IMG:
    HELP_IMG = "https://i.pinimg.com/564x/81/fd/c2/81fdc237881418f01147ecc367c594f7.jpg"

if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)

HANDLERS = getenv("HANDLERS", ". /").split()
