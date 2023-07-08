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

def get_media_type(media):
    mime_type, _ = mimetypes.guess_type(media)
    print(mime_type)
    if mime_type is not None:
        if mime_type.startswith("image"):
            return "image" , media
        elif mime_type.startswith("video"):
            return "video" , media
    return "unknown" , None

async def get_start_media():
    global START_IMG
    if not START_IMG:
        START_IMG = "https://i.pinimg.com/564x/01/d6/ae/01d6ae16511ce7d7db7aef7844c119ea.jpg"    
    else:
        START_IMG = random.choice(START_IMG)
    print(START_IMG)
    media_type , media = get_media_type(START_IMG)
    return media_type , media

    
async def get_help_media():
    global HELP_IMG      
    if not HELP_IMG:
        HELP_IMG = "https://i.pinimg.com/564x/81/fd/c2/81fdc237881418f01147ecc367c594f7.jpg"
    else:
        HELP_IMG = random.choice(HELP_IMG)
    media_type , media = get_media_type(HELP_IMG)
    return media_type, media

if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)


