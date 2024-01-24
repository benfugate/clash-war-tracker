import coc
import json
import asyncio
from config import Config
import re

import pick_war_players as pwp
config = Config()

if not (config.username or config.password or config.clan_tag):
    raise ValueError('Missing at least one config variable')

loop = asyncio.get_event_loop()
client = coc.Client(key_names="clash-war-tracker", key_count=1)
loop.run_until_complete(client.login(config.username, config.password))
clan = loop.run_until_complete(client.get_clan(config.clan_tag))
members = clan.members

with open(config.clash_json) as f:
    clash = json.load(f)

for member in clash:
    clash[member]['in_clan'] = False
for member in members:
    if member.tag in clash:
        player = loop.run_until_complete(client.get_player(member.tag))
        clash[member.tag]['town_hall'] = player.town_hall
        clash[member.tag]['name'] = re.sub(r'[^\w_]+', '', player.name.replace(" ", "_"))
        clash[member.tag]['in_clan'] = True
        clash[member.tag]['trophies'] = member.trophies

with open(config.clash_json, 'w', encoding='utf-8') as f:
    json.dump(clash, f, ensure_ascii=False, indent=4)

pwp.pick_war_players()
