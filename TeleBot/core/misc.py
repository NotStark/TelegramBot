from typing import Dict, List
from pyrogram.types import InlineKeyboardButton

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

async def paginate_modules(module_dict: Dict, prefix, chat=None, column_size: int = 3) -> List:
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    mod_name.title(),
                    callback_data="{}_module({})".format(
                        prefix, mod_name.lower()
                    ),
                )
                for mod_name in module_dict.keys()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    mod_name.title(),
                    callback_data="{}_module({},{})".format(
                        prefix, chat, mod_name.lower()
                    ),
                )
                for mod_name in module_dict.values()
            ]
        )
    print(modules)
    pairs = [modules[i * column_size: (i + 1) * column_size] for i in range((len(modules) + column_size - 1) // column_size)]

    calc = len(modules) % column_size
    if calc == 1 or calc == 2:
        pairs.append((modules[-1],))
    else:
        pairs += [[EqInlineKeyboardButton("Back", callback_data="help_back")]]

    return pairs
