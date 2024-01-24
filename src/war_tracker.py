import os
import shutil
import sys
import time
import re
import coc
import json
import asyncio
import traceback

from config import Config
import pick_war_players as pwp

config = Config()


def war_tracker():

    loop = asyncio.get_event_loop()

    if (config.username is None) or (config.password is None) or (config.clan_tag is None):
        raise ValueError('Missing at least one config variable')

    try:
        client = coc.Client(key_names="clash-war-tracker", key_count=1)
        loop.run_until_complete(client.login(config.username, config.password))
        war = loop.run_until_complete(client.get_current_war(config.clan_tag))
    except Exception as e:
        print(f"API Error: {e}")
        return
    if not war:
        return

    with open(config.war_log_json) as f:
        opponents = json.load(f)

    # Decide how we should handle this run...
    if war.opponent.tag in opponents['clans']:
        # We have seen this war before
        if (opponents['clans'][-1] == war.opponent.tag) and (war.state == "inWar"):
            # Expected - This war is still ongoing
            output_filename = config.current_war_json
        elif (opponents['clans'][-1] == war.opponent.tag) and (war.state != "inWar"):
            # The last war has ended, and we haven't started a new war yet.
            if os.path.exists(config.current_war_json):
                os.remove(config.current_war_json)
            else:
                # Nothing to do, the data has been saved already
                return
            # Expected end of war - we deleted current_war.json,
            #     run script normally and save to clash.json
            output_filename = config.clash_json
        else:
            # Unexpected - we have fought this clan before at some point, or something is weird.
            opponents['clans'].append(war.opponent.tag)
            output_filename = config.current_war_json
    else:
        # We have never seen this clan before
        if war.state == "inWar":
            # In a new war
            if os.path.exists(config.current_war_json):
                # War data still exists, so we need to save that before continuing
                shutil.copyfile(config.current_war_json, config.clash_json)
                os.remove(config.current_war_json)
            opponents['clans'].append(war.opponent.tag)
            output_filename = config.current_war_json
        else:
            # Not in a war, probably preparation or no war at all
            if os.path.exists(config.current_war_json):
                # War data still exists, so we need to save that before quitting
                # This may happen if we are in a CWL. Potentially dangerous
                #         to stats if script breaks, and data is incomplete...
                shutil.copyfile(config.current_war_json, config.clash_json)
                os.remove(config.current_war_json)
            return

    # Build a frame to store war member data in
    war_info = {}
    for member in war.clan.members:
        war_player = {
            "name": re.sub(r'[^\w_]', '', member.name.replace(" ", "_")),
            "tag": member.tag, "town_hall": member.town_hall, "missed_attacks": 2,
            "attack_info": {
                "attacks": {
                    "first_attack": {"stars": None, "destruction": None},
                    "second_attack": {"stars": None, "destruction": None}
                },
                "timestamp": int(time.time())
            }}
        war_info[member.tag] = war_player

    # Look through war attacks and fill out any used attacks
    for attack in war.attacks:
        if attack.attacker_tag in war_info:
            war_info[attack.attacker_tag]["missed_attacks"] -= 1
            attacks = war_info[attack.attacker_tag]["attack_info"]["attacks"]
            if attacks["first_attack"]["stars"] is None:
                attacks["first_attack"]["stars"] = attack.stars
                attacks["first_attack"]["destruction"] = attack.destruction
            else:
                attacks["second_attack"]["stars"] = attack.stars
                attacks["second_attack"]["destruction"] = attack.destruction

    # If war attacks were blank, remove them from the json
    for tag in war_info:
        if war_info[tag]["attack_info"]["attacks"]["first_attack"]["stars"] is None:
            war_info[tag]["attack_info"]["attacks"] = None
        elif war_info[tag]["attack_info"]["attacks"]["second_attack"]["stars"] is None:
            del war_info[tag]["attack_info"]["attacks"]["second_attack"]

    with open(config.clash_json) as f:
        clash = json.load(f)

    # Update or add to the clash json with new war info
    for tag in war_info:
        if war_info[tag]["tag"] in clash:
            tag = war_info[tag]["tag"]
            clash[tag]["misses"] += war_info[tag]["missed_attacks"]
            clash[tag]["total"] += 2
            if war_info[tag]["attack_info"]["attacks"]:
                clash[tag]["wars"].append(war_info[tag]["attack_info"])
        else:
            tag = war_info[tag]["tag"]
            clash[tag] = {}
            clash[tag]["misses"] = war_info[tag]["missed_attacks"]
            clash[tag]["total"] = 2
            clash[tag]["wars"] = []
            if war_info[tag]["attack_info"]["attacks"]:
                clash[tag]["wars"] = [war_info[tag]["attack_info"]]

        clash[tag]["name"] = war_info[tag]["name"]
        clash[tag]["in_clan"] = True
        clash[tag]["town_hall"] = war_info[tag]["town_hall"]
        clash[tag]["most_recent_war"] = int(time.time())

        if war.is_cwl:
            clash[tag]["total"] -= 1
            clash[tag]["misses"] -= 1

    # Calculate some player statistics from the numbers we have gathered
    for tag in clash:
        total_stars, total_destruction, attacks = 0, 0, 0
        time_filtered_total_stars, time_filtered_total_destruction, time_filtered_attacks = 0, 0, 0

        if "wars" in clash[tag]:
            for war in clash[tag]["wars"]:
                if "attacks" in war:
                    for attack in war["attacks"]:
                        total_stars += war["attacks"][attack]["stars"]
                        total_destruction += war["attacks"][attack]["destruction"]
                        attacks += 1
                    if war['timestamp'] > int(time.time()) - config.war_filter:
                        for attack in war["attacks"]:
                            time_filtered_total_stars += war["attacks"][attack]["stars"]
                            time_filtered_total_destruction += war["attacks"][attack]["destruction"]
                            time_filtered_attacks += 1

        if attacks != 0:
            clash[tag]["average_stars"] = round(total_stars / attacks, 2)
            clash[tag]["average_destruction"] = round(total_destruction / attacks, 2)
        else:
            clash[tag]["average_stars"] = None
            clash[tag]["average_destruction"] = None
        if clash[tag]["average_stars"]:
            star_score = clash[tag]["average_stars"] / 3
            destruction_score = clash[tag]["average_destruction"] / 100
            activity_score = 1 - (clash[tag]["misses"] / clash[tag]["total"])
            clash[tag]["player_score"] = round(((star_score + destruction_score + activity_score) / 3) * 100, 2)
        else:
            clash[tag]["player_score"] = 0

        if time_filtered_attacks != 0:
            clash[tag]["time_filtered_average_stars"] = round(time_filtered_total_stars / time_filtered_attacks, 2)
            clash[tag]["time_filtered_average_destruction"] = round(
                time_filtered_total_destruction / time_filtered_attacks, 2)
        else:
            clash[tag]["time_filtered_average_stars"] = None
            clash[tag]["time_filtered_average_destruction"] = None
        if clash[tag]["time_filtered_average_stars"]:
            star_score = clash[tag]["time_filtered_average_stars"] / 3
            destruction_score = clash[tag]["time_filtered_average_destruction"] / 100
            activity_score = 1 - (clash[tag]["misses"] / clash[tag]["total"])
            clash[tag]["player_score"] = round(((star_score + destruction_score + activity_score) / 3) * 100, 2)

    # Output calculated data to files
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(clash, f, ensure_ascii=False, indent=4)
    with open(config.war_log_json, 'w', encoding='utf-8') as f:
        json.dump(opponents, f, ensure_ascii=False, indent=4)

    if output_filename == config.clash_json:
        pwp.pick_war_players()


try:
    war_tracker()
except Exception as e:
    errors_dir = f'{config.storage_folders}/errors/'
    if not os.path.exists(errors_dir):
        os.makedirs(errors_dir)

    list_of_files = os.listdir(errors_dir)
    full_path = ["{0}/{1}".format(errors_dir, x) for x in list_of_files]
    if len(list_of_files) == 5:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)
    with open(f"{errors_dir}/exception-{int(time.time())}.txt", "w") as errorfile:
        e_type, e_val, e_tb = sys.exc_info()
        traceback.print_exception(e_type, e_val, e_tb, file=errorfile)
