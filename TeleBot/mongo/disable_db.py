from TeleBot.mongo import db 
from TeleBot import DISABLE_ENABLE_MODULES

disabledb = db.disable

async def add_disable(chat_id: int, disable_cmd: str):
    await disabledb.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"disable_cmds": disable_cmd}, "$setOnInsert": {"disabledel": False, "disable_modules" : []}},
        upsert=True
    )

async def get_disabled_commands(chat_id: int):
    result = await disabledb.find_one({"chat_id": chat_id})
    if result:
        return result.get("disable_cmds", [])
    return []

async def get_disable_delete(chat_id: int):
    result = await disabledb.find_one({"chat_id": chat_id})
    if result:
        return result.get("disabledel", False)
    return False

async def rm_disable(chat_id: int, disable_cmd: str) -> bool:
    chat = await disabledb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    
    disable_cmds = chat["disable_cmds"]
    if disable_cmd in disable_cmds:
        disable_cmds.remove(disable_cmd)
        await disabledb.update_one(
            {"chat_id": chat_id},
            {"$set": {"disable_cmds": disable_cmds}}
        )
        return True
    
    return False


async def disable_module(chat_id : int, module_name : str):
    commands = DISABLE_ENABLE_MODULES[module_name]["commands"]
    for command in commands:
        await add_disable(chat_id,command)
    return await disabledb.update_one({"chat_id" : chat_id}, {"$addToSet" : {"disable_modules" : module_name}})

async def enable_module(chat_id: int, module_name: str):
    commands = DISABLE_ENABLE_MODULES[module_name]["commands"]
    for command in commands:
        await rm_disable(chat_id, command)
    return await disabledb.update_one({"chat_id": chat_id}, {"$pull": {"disable_modules": module_name}})


async def get_all_module_status(chat_id: int):
    chat = await disabledb.find_one({"chat_id": chat_id})
    to_return = {}
    
    locks = chat.get('disable_modules', []) if chat else []
    
    to_return = {
        x: ('✅', 'enable') if x in locks else ('', 'disable')
        for x in DISABLE_ENABLE_MODULES.keys()
    }
    
    return to_return


async def disabledel(chat_id: int, arg: bool):
    chat = await disabledb.find_one({"chat_id": chat_id})
    if not chat:
        await add_disable(chat_id, None)

    return await disabledb.update_one(
        {"chat_id": chat_id},
        {"$set": {"disabledel": arg}}
    )
