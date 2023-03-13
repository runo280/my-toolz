import os
#import configparser

#account_config = "config.conf"
#config = configparser.RawConfigParser(allow_no_value=False)
# config.read(account_config)


phone_number = os.environ['tgPhone']
password = os.environ['tgPass']

api_id = os.environ['apiId']
api_hash = os.environ['apiHash']

db_user = os.environ['mduser']
db_pass = os.environ['mdpass']
db_domain = os.environ['mdurl']
