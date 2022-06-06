import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from textskeyboards import viberkeyboards as kb

dotenv_path = os.path.join(Path(__file__).parent.parent, 'config/.env')
load_dotenv(dotenv_path)

MAIN_COLOR = os.getenv("COLOR")


SHARE_PHONE_KEYBOARD = {
    "DefaultHeight": False,
    "BgColor": '#cdcfd1',
    "Type": "keyboard",
    "Buttons": [
        {
            "Columns": 6,
            "Rows": 1,
            "BgColor": MAIN_COLOR,
            "BgLoop": True,
            "ActionType": "share-phone",
            "ActionBody": 'phone_reply',
            "ReplyType": "message",
            "Text": 'Поділитися номером телефону',
        },
    ]
}
