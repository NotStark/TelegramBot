import requests
from TeleBot import pgram
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@pgram.on_message(filters.command("imdb"))
async def _IMDb(_,msg):
    if len(msg.command) < 2:        
        return await msg.reply_text("give me a query to search")
    
    text = msg.text.split(None, 1)[1].replace(" ", "%20")
    
    url=f"https://api.safone.me/tmdb?query={text}%20&limit=1"
    ok=requests.get(url).json()        
    re=ok["results"][0]
    if not re:       
        await msg.reply_text("nothing")
    else:
        title=re["title"]
        poster=re["poster"]
        runtime=re["runtime"]
        rating=re["rating"]
        releaseDate=re["releaseDate"]
        popularity=re["popularity"]
        status=re["status"]
        homepage=re["homepage"]
        imdbId=re["imdbId"]
        imdbLink=re["imdbLink"]
        id=re["id"]        
        overview=re["overview"]     
        genres = ""
        gen=re["genres"]   
        for i in gen:
            genres += i + ","                                   
        await msg.reply_photo(poster,
    caption=f"""
ð **á´Éªá´Êá´ :** {title}

â±ï¸ **Êá´É´á´Éªá´á´ :** {runtime}á´ÉªÉ´
ð **Êá´á´ÉªÉ´É¢ :** {rating}/10
ð³ï¸ **Éªá´ :** {id}

ð **Êá´Êá´á´sá´ á´á´á´á´ :** {releaseDate}
ð­ **É¢á´É´Êá´ :** {genres}
ð¥ **á´á´á´á´Êá´ÊÉªá´Ê :** {popularity}

â¡ **sá´á´á´á´s :** {status}
ð« **Éªá´á´Ê Éªá´ :** {imdbId}

ð  **á´Êá´á´ :** `{overview}`
""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ðï¸ ð¸ð¼ð³Ê",
                        url=imdbLink,
                    ),
                ],
            ],
        ),
    )
    
       
__help__="""
ãðð¢ð ð ðð¡ðð¦ã :
âââââââââââââââââ
à¹ /IMDb Â«á´á´á´ Éªá´ É´á´á´á´Â» : É¢á´á´ Òá´ÊÊ ÉªÉ´Òá´ á´Êá´á´á´ á´ á´á´á´ Éªá´ ÒÊá´á´ Éªá´á´Ê.á´á´á´
âââââââââââââââââ
"""  
__mod_name__ = "ð¸á´á´Ê"
