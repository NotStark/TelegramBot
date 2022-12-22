import os
import io
import requests
import random
import glob

from TeleBot import pgram
from pyrogram import filters
from PIL import Image,ImageDraw,ImageFont

from TeleBot.resources.LOGO_LINK.LOGO_LINKS import LOGOES





@pgram.on_message(filters.command("logo"))
async def logo_make(_,message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    if len(message.command) < 2: 
        await message.reply_text("give a text to generate logo")
        return
             


    logo_text = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1]
        )
    text = await message.reply("`ᴍᴀᴋɪɴɢ ʏᴏᴜʀ ʟᴏɢᴏ`")
        
    if not replied:
        try:
            randc = random.choice(LOGOES)
            logo = Image.open(io.BytesIO(requests.get(randc).content))
            draw = ImageDraw.Draw(logo) 
            image_widthz, image_heightz = logo.size
            pointsize = 500
            fillcolor = "black"
            shadowcolor = "blue"
            fnt = glob.glob("./TeleBot/resources/Logo_fonts/*")
            randf = random.choice(fnt)
            font = ImageFont.truetype(randf, 120)
            w, h = draw.textsize(logo_text, font=font)
            h += int(h*0.21)
            image_width, image_height = logo.size
            draw.text(((image_widthz-w)/2, (image_heightz-h)/2), logo_text, font=font, fill=(255, 255, 255))
            x = (image_widthz-w)/2
            y = ((image_heightz-h)/2+6)
            draw.text((x, y), logo_text, font=font, fill="white", stroke_width=1, stroke_fill="black")
            final_logo = "friday.png"
            logo.save(final_logo, "png")
            await pgram.send_photo(chat_id,final_logo)
            await text.delete()
            if os.path.exists(final_logo):
                os.remove(final_logo)                
        except Exception as e:
            await message.reply_text(e)
    
   
    if replied:
        if replied.photo:
            await message.reply_text("ok")        
        
     
