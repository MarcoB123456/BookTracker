from pathlib import Path

import requests

from Definitions import ROOT_PATH


def build_rating(rating):
    if rating is None:
        return ""
    else:
        return "★" * rating + "☆" * (5 - rating)


def remove_image(isbn):
    Path(f"{ROOT_PATH}\\Images\\Covers\\{isbn}.jpg").unlink()


def save_image(url, isbn):
    img_data = requests.get(url).content
    with open(f"{ROOT_PATH}\\Images\\Covers\\{isbn}.jpg", 'wb') as handler:
        handler.write(img_data)
        return f"{isbn}.jpg"


def is_not_none(value):
    if value is None or value == "None":
        return False
    else:
        return True
