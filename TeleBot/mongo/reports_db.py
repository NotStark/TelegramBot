from TeleBot.mongo import db 

reportsdb = db.reports


async def on_off_reports(chat_id : int , arg : bool):
    return await reportsdb.update_one({"chat_id" : chat_id},{"$set" : {"reports" : arg }},upsert = True)


async def get_report(chat_id : int):
    chat = await reportsdb.find_one({"chat_id" : chat_id})
    if not chat:
        return True
    return chat['reports']