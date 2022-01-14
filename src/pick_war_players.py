import time
import coc
import json
import asyncio
from config import Config


config = Config()
one_month_in_seconds = 2592000


def main():

    loop = asyncio.get_event_loop()
    client = coc.login(config.username, config.password)

    if (config.username is None) or (config.password is None) or (config.clan_tag is None):
        raise ValueError('Missing at least one config variable')

    with open(config.clash_json) as file:
        clash = json.load(file)

    war_picks = {}
    clan = loop.run_until_complete(client.get_clan(config.clan_tag))
    members = clan.members
    for member in members:
        if member.tag not in clash:
            player = loop.run_until_complete(client.get_player(member.tag))
            if player.war_opted_in:
                war_picks[member.tag] = {
                    "name": member.name,
                    "player_score": -1,
                    "town_hall": player.town_hall
                }

    for tag in clash:
        if clash[tag]["in_clan"]:
            miss_percentage = (clash[tag]["misses"] / clash[tag]["total"]) * 100
            if miss_percentage == 100 and clash[tag]["total"] > 3:
                continue

            most_recent_war = 0
            for war in clash[tag]["wars"]:
                if war["timestamp"] > most_recent_war:
                    most_recent_war = war["timestamp"]
            clash[tag]["most_recent_war"] = most_recent_war
            no_recent_war = False
            if most_recent_war < int(time.time()) - one_month_in_seconds:
                no_recent_war = True

            if miss_percentage < 50 or no_recent_war:
                try:
                    player = loop.run_until_complete(client.get_player(tag))
                    if not player.war_opted_in:
                        continue
                except Exception as e:
                    print(f"API Error: {e}")
                    return

                war_picks[tag] = clash[tag]

    clash = war_picks

    while len(clash) % 5 != 0:
        most_recent_attack = 0
        most_recent_player = ""

        for tag in clash:
            if clash[tag]["player_score"] == -1:
                continue
            if clash[tag]["most_recent_war"] > most_recent_attack:
                most_recent_attack = clash[tag]["most_recent_war"]
                most_recent_player = tag
            elif clash[tag]["most_recent_war"] == most_recent_attack:
                if clash[tag]["player_score"] < clash[most_recent_player]["player_score"]:
                    most_recent_attack = clash[tag]["most_recent_war"]
                    most_recent_player = tag

        del clash[most_recent_player]

    with open(config.war_picks, 'w', encoding='utf-8') as f:
        json.dump(clash, f, ensure_ascii=False, indent=4)


try:
    main()
except Exception as e:
    print(e)
