# -*- coding: utf-8 -*-
import base64
import re
import time

from Telegram import MyTelegram
from db import MyDatabase
from eitaa_api import *
from env import agg_channel
from utils import *


class Post:
    def __init__(self, pid, is_published=False, publish_id=-1):
        self.pid = pid
        self.is_published = is_published
        self.publish_id = publish_id

    def get_dic(self):
        return {'pid': self.pid, 'is_pub': self.is_published, 'pub_id': self.publish_id}


def clean_caption(caption):
    clean = re.sub(agg_channel[3], agg_channel[4], caption)
    clean = re.sub(agg_channel[5], agg_channel[6], clean)
    return clean


if __name__ == "__main__":

    if is_offline():
        print(agg_channel)
    src_channel_id = int(agg_channel[0])
    target_channel_id = agg_channel[1]
    tableName = agg_channel[2]

    db = MyDatabase(tableName)
    # get tg session
    if not is_offline():
        session_query = db.get_session()
        decoded_string = base64.b64decode(session_query['session'])
        with open("seasion.session", "wb") as session_file:
            session_file.write(decoded_string)

    tg = MyTelegram()

    # update db posts
    if db.should_update(tg.get_latest_post_id(src_channel_id)):
        list_to_db = []
        for p in tg.get_latest_posts(src_channel_id, 1):
            post = Post(p.id)
            list_to_db.append(post)
            if is_offline():
                print(p.id)
        db.add_to_db(list_to_db)

    # publish posts
    for p in db.get_publish_queue():
        time.sleep(10)
        post = tg.get_message_by_id(src_channel_id, p['pid'])
        if is_offline():
            print(post)
        text = clean_caption(post.message)
        length = len(text)
        if post.file:
            if is_offline():
                print('has file')
            filename_ = 'msgfile' + post.file.ext
            post.download_media(file=filename_)
            if length < 1400:
                r = send_file(target_channel_id, text, filename_)
                # r = send_message(target_channel_id, text)
                delete_msg_file(filename_)
                if r['ok']:
                    if is_offline():
                        print(r)
                    if not is_offline():
                        db.set_published(post.id, r['result']['message_id'])
                else:
                    if is_offline():
                        print(r)
            else:
                r = send_file(target_channel_id, "", filename_)
                time.sleep(20)
                r2 = send_message(target_channel_id, text)
                delete_msg_file(filename_)
                if r['ok'] and r2['ok']:
                    if is_offline():
                        print(r)
                    if not is_offline():
                        db.set_published(post.id, r['result']['message_id'])
                else:
                    if is_offline():
                        print(r)
                        print(r2)
        else:
            if is_offline():
                print('no file')
            r = send_message(target_channel_id, text)
            if r['ok']:
                if is_offline():
                    print(r)
                if not is_offline():
                    db.set_published(post.id, r['result']['message_id'])
            else:
                if is_offline():
                    print(r)

    # save tg session
    if not is_offline():
        with open("seasion.session", "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
            db.update_session(session_query['_id'], b64_string)
