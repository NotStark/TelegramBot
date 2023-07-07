from TeleBot.mongo import db

approvedb = db.approve

async def approve_user(chat_id : int,user_id : int ):
    chat = await approvedb.find_one({"chat_id" : chat_id})
    if chat:
        list = chat.get("user_ids")
        list.append(user_id)
        return await approvedb.update_one({"chat_id": chat_id}, {"$set": {"user_ids": list}}, upsert=True)
    list = [user_id]
    return await approvedb.update_one({"chat_id" : chat_id},{"$set" : {"user_ids" : list}}, upsert=True)   


async def isApproved(chat_id : int,user_id : int) -> bool:
    chat = await approvedb.find_one({"chat_id" : chat_id})
    if chat:
        check = chat.get("user_ids")
        if user_id in check:
            return True
        return False

async def disapprove_user(chat_id : int,user_id : int):
    chat = await approvedb.find_one({"chat_id" : chat_id}) 
    if chat:
        list = chat.get("user_ids")
        list.remove(user_id)
        return await approvedb.update_one({"chat_id": chat_id}, {"$set": {"user_ids": list}}, upsert=True) 

async def disapprove_all(chat_id : int):
    await approvedb.delete_one({"chat_id" : chat_id}) 
    
async def approved_users(chat_id : int) -> list:
    chat = await approvedb.find_one({"chat_id" : chat_id}) 
    if chat :        
        return chat["user_ids"]
    return []