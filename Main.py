import base64
from collections.abc import Iterable

from telethon.tl.types import MessageEntityTextUrl

import db
from Telegram import MyTelegram
from env import *
import os
import time


if __name__ == "__main__":

    # get tg session
    squery = db.get_session()
    decoded_string = base64.b64decode(squery['session'])
    with open("seasion.session", "wb") as sfile:
        sfile.write(decoded_string)

    tg = MyTelegram('seasion.session', api_id, api_hash, phone_number, password)

    for filename in os.listdir("upload"):
        print(filename)
        time.sleep(10)
        tg.send_file("upload/" + filename)

    # save tg session
    with open("seasion.session", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
        db.update_session(squery['_id'], b64_string)
