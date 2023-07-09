import re
from pyrogram.types import InlineKeyboardButton

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")

async def button_markdown_parser(text):
    text_data = ""
    buttons = []

    if not text:
        return text_data, buttons

    matches = BTN_URL_REGEX.finditer(text)
    prev_end = 0

    for match in matches:
        start = match.start(1)
        end = match.end(1)
        button_label = match.group(2)
        button_url = match.group(3)
        is_same_line = bool(match.group(4))

        if is_same_line and buttons:
            buttons[-1].append(InlineKeyboardButton(text=button_label, url=button_url))
        else:
            buttons.append([InlineKeyboardButton(text=button_label, url=button_url)])

        text_data += text[prev_end:start]
        prev_end = end

    text_data += text[prev_end:]

    return text_data, buttons