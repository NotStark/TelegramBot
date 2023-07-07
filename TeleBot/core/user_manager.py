from TeleBot import BOT_ID, app
from typing import Any
from .functions import is_invincible as x , get_admins as y 


async def is_bot_admin(chat_id: int, permission: Any = None) -> bool:
    if permission is None and BOT_ID in await y(chat_id):
        return True
    else:
        chat_member = await app.get_chat_member(chat_id, BOT_ID)
        privileges = (
            chat_member.privileges.__dict__
            if chat_member.privileges is not None
            else {}
        )
        return permission in privileges and privileges[permission]


async def is_user_admin(chat_id: int, user_id: int, permission: Any = None) -> bool:
    
    if await x(user_id) or user_id == chat_id:
        return True
    elif permission is None and user_id in await y(chat_id):
        return True
    else:
        chat_member = await app.get_chat_member(chat_id, user_id)
        privileges = (
            chat_member.privileges.__dict__
            if chat_member.privileges is not None
            else {}
        )
        return permission in privileges and privileges[permission]
    

