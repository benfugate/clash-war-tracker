import os
import coc
import json
import asyncio

with open('/clash-tracker/config.json') as f:
    config = json.load(f)
    username = config["COC_USERNAME"]
    password = config["COC_PASSWORD"]
    clan_tag = config["COC_CLAN_TAG"]

if not (username or password or clan_tag):
    raise ValueError('Missing at least one config variable')

loop = asyncio.get_event_loop()
client = coc.login(username, password)
clan = loop.run_until_complete(client.get_clan(clan_tag))
members = clan.members

with open('/var/www/html/clash.json') as f:
    clash = json.load(f)

for member in clash:
    clash[member]['in_clan'] = False
for member in members:
    if member.tag in clash:
        clash[member.tag]['in_clan'] = True

with open('/var/www/html/clash.json', 'w', encoding='utf-8') as f:
    json.dump(clash, f, ensure_ascii=False, indent=4)
