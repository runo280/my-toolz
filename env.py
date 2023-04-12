# -*- coding: utf-8 -*-
import os
import configparser
import utils

account_config = "config.ini"
cfg = configparser.RawConfigParser(allow_no_value=False)
cfg.read(account_config)

tgPhone = cfg['one']['tgPhone'] if utils.is_offline() else os.environ['tgPhone']
tgPass = cfg['one']['tgPass'] if utils.is_offline() else os.environ['tgPass']

tgApiId = cfg['one']['tgApiId'] if utils.is_offline() else os.environ['tgApiId']
tgApiHash = cfg['one']['tgApiHash'] if utils.is_offline() else os.environ['tgApiHash']

eitaaBotToken = cfg['one']['eitaaBotToken'] if utils.is_offline() else os.environ['eitaaBotToken']
eitaaApiUrl = cfg['one']['eitaaApiUrl'] if utils.is_offline() else os.environ['eitaaApiUrl']

agg_channel = cfg['one']['agg_channel'].split('^') if utils.is_offline() else os.environ['agg_channel'].split('^')

mongoUser = cfg['one']['mongoUser'] if utils.is_offline() else os.environ['mongoUser']
mongoPass = cfg['one']['mongoPass'] if utils.is_offline() else os.environ['mongoPass']
mongoUrl = cfg['one']['mongoUrl'] if utils.is_offline() else os.environ['mongoUrl']
