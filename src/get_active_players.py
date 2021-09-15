import coc
import json
import asyncio
from config import Config

config = Config()

if not (config.username or config.password or config.clan_tag):
    raise ValueError('Missing at least one config variable')

loop = asyncio.get_event_loop()
client = coc.login(config.username, config.password)
clan = loop.run_until_complete(client.get_clan(config.clan_tag))
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
