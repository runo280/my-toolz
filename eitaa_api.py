# -*- coding: utf-8 -*-
from env import *
from os.path import isfile
import requests
import json


def send_message(chnl_id, text, pin=False, view_to_delete=-1,
                 disable_notification=False, reply_to_message_id=None):
    r = requests.post(
        f"https://{eitaaApiUrl}/api/{eitaaBotToken}/sendMessage",
        data={
            'chat_id': chnl_id,
            'text': text,
            'pin': int(pin),
            'viewCountForDelete': view_to_delete,
            'disable_notification': int(disable_notification),
            'reply_to_message_id': reply_to_message_id if reply_to_message_id is not None else '',
        }
    )
    return json.loads(r.text)


def send_file(chnl_id, text, file, pin=False, view_to_delete=-1,
              disable_notification=False, reply_to_message_id=None):
    if not isfile(file):
        raise Exception(f"File `{file}` not found")

    r = requests.post(
        f"https://{eitaaApiUrl}/api/{eitaaBotToken}/sendFile",
        data={
            'chat_id': chnl_id,
            'caption': text,
            'pin': int(pin),
            'viewCountForDelete': view_to_delete,
            'disable_notification': int(disable_notification),
            'reply_to_message_id': reply_to_message_id if reply_to_message_id is not None else '',
        },
        files={
            'file': open(file, 'rb'),
        }
    )
    return json.loads(r.text)
