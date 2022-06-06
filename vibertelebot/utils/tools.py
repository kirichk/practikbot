import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from textskeyboards import texts as resources


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)

MAIN_COLOR = os.getenv("COLOR")


def keyboard_consctructor(items: list) -> dict:
    """Pasting infromation from list of items to keyboard menu template."""
    if len(items) > 12:
        width = 1
    elif len(items) == 3:
        width = 2
    elif len(items) > 1:
        width = 3
    else:
        width = 6
    keyboard = {
        "DefaultHeight": False,
        "BgColor": '#cdcfd1',
        "Type": "keyboard",
        "Buttons": [{
                "Columns": width,
                "Rows": 1,
                "BgColor": MAIN_COLOR,
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": item[1],
                "ReplyType": "message",
                "Text": item[0],
                # "TextOpacity": 0,
        } for item in items]
    }
    keyboard['Buttons'].append({
            "Columns": 6,
            "Rows": 1,
            "BgColor": MAIN_COLOR,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": 'phone_share',
            "ReplyType": "message",
            "Text": 'Меню',
            # "TextOpacity": 0,
    })
    return keyboard
