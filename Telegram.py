from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
# from telethon.tl.types import InputPeerChannel
# from telethon import functions, types

from env import *
import utils


class MyTelegram:
    _name = 'seasion.session'
    _api_id = tgApiId
    _api_hash = tgApiHash
    _phone_number = tgPhone
    _password = tgPass
    _client = None
    _dialogs = None

    def __init__(self):

        self._client = TelegramClient(self._name, self._api_id, self._api_hash, proxy=(
            "socks5", '127.0.0.1', 2080)) if (utils.is_offline()) else TelegramClient(self._name, self._api_id,
                                                                                      self._api_hash)
        self._client.connect()

        if not self._client.is_user_authorized():
            print('Not authorized')
            self._client.send_code_request(self._phone_number)
            try:
                self._client.sign_in(self._phone_number,
                                     input('Enter code:\n'))
            except SessionPasswordNeededError:
                self._client.sign_in(password=self._password)

        if self._client.is_user_authorized():
            print('Authorized')

        self._dialogs = self._client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash=1
        ))

    def send_file_to_me(self, media):
        return self._client.send_file(self._client.get_entity('me'), media, caption=media)

    def get_latest_posts(self, chnl_id, count=50):
        return self._client.get_messages(chnl_id, limit=count)

    def get_message_by_id(self, chnl_id, post_id):
        return self._client.get_messages(chnl_id, ids=post_id)

    def get_latest_post_id(self, chnl_id):
        return self._client.get_messages(chnl_id)[0].id
