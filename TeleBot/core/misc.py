from typing import Dict, List
from pyrogram.types import InlineKeyboardButton

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text



def paginate_modules(module_dict: Dict, prefix, chat=None) -> List:
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x,
                    callback_data="{}_module({})".format(
                        prefix, x
                    ),
                )
                for x in module_dict.keys()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x 
                    ),
                )
                for x in module_dict.keys()
            ]
        )

    pairs = [modules[i * 3 : (i + 1) * 3] for i in range((len(modules) + 3 - 1) // 3)]

    round_num = len(modules) / 3
    calc = len(modules) - round(round_num)
    if calc in [1, 2]:
        pairs.append((modules[-1],))
    else:
        pairs += [[EqInlineKeyboardButton("[► Back ◄]", callback_data="help_back")]]

    return pairs