import os
import coc
import json
import asyncio

username = os.environ.get("COC_USERNAME")
password = os.environ.get("COC_PASSWORD")
clan_tag = os.environ.get("COC_CLAN_TAG")

loop = asyncio.get_event_loop()
client = coc.login(username, password)
clan = loop.run_until_complete(client.get_clan(clan_tag))
members = clan.members

with open('/config/www/clash.json') as f:
    clash = json.load(f)

for member in clash:
    clash[member]['in_clan'] = False
for member in members:
    if member.tag in clash:
        clash[member.tag]['in_clan'] = True

with open('/config/www/clash.json', 'w', encoding='utf-8') as f:
    json.dump(clash, f, ensure_ascii=False, indent=4)
