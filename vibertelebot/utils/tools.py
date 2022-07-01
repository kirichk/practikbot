import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import date, datetime, timedelta


dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)

MAIN_COLOR = os.getenv("COLOR")


def keyboard_consctructor(items: list) -> dict:
    """Pasting infromation from list of items to keyboard menu template."""
    if len(items) == 3 or len(items) == 5:
        width = 3
        keyboard = {
            "DefaultHeight": False,
            "BgColor": '#cdcfd1',
            "Type": "keyboard",
            "Buttons": [{
                    "Columns": width,
                    "Rows": 1,
                    "BgColor": '#e75740',
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": item[1],
                    "ReplyType": "message",
                    "Text": item[0],
                    # "TextOpacity": 0,
            } for item in items[:-1]]
        }
        keyboard['Buttons'].append(
            {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": '#e75740',
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": items[-1][1],
                    "ReplyType": "message",
                    "Text": items[-1][0],
                    # "TextOpacity": 0,
            }
        )
    else:
        width = 6
        keyboard = {
            "DefaultHeight": False,
            "BgColor": '#cdcfd1',
            "Type": "keyboard",
            "Buttons": [{
                    "Columns": width,
                    "Rows": 1,
                    "BgColor": '#e75740',
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": item[1],
                    "ReplyType": "message",
                    "Text": item[0],
                    # "TextOpacity": 0,
            } for item in items]
        }
    return keyboard
