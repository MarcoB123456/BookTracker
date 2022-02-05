import os

from Definitions import ROOT_PATH
import requests


def build_rating(rating):
    if rating is None:
        return ""
    else:
        return "★" * rating + "☆" * (5 - rating)


def remove_image(isbn):
    os.remove(f"{ROOT_PATH}\\Images\\Covers\\{isbn}.jpg")


def save_image(url, isbn):
    img_data = requests.get(url).content
    with open(f"{ROOT_PATH}\\Images\\Covers\\{isbn}.jpg", 'wb') as handler:
        handler.write(img_data)
        return f"{isbn}.jpg"