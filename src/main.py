import os
import shutil
import sys
import time
import coc
import json
import asyncio
import traceback
from config import Config

config = Config()


def main():

    loop = asyncio.get_event_loop()

    if (config.username is None) or (config.password is None) or (config.clan_tag is None):
        raise ValueError('Missing at least one config variable')

    client = coc.login(config.username, config.password)
    war = loop.run_until_complete(client.get_current_war(config.clan_tag))
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
    war_members_names = []
    war_members_tags = []
    war_attacks_missed = []
    war_attacks = []
    for member in war.clan.members:
        war_members_names.append(member.name)
        war_members_tags.append(member.tag)
        war_attacks_missed.append(2)
        war_attacks.append(
            {
                "attacks": {
                    "first_attack": {"stars": None, "destruction": None},
                    "second_attack": {"stars": None, "destruction": None}
                },
                "timestamp": int(time.time())
            }
        )

    # Look through war attacks and fill out any used attacks
    for attack in war.attacks:
        if str(attack.attacker_tag) in war_members_tags:
            war_attacks_missed[war_members_tags.index(str(attack.attacker_tag))] -= 1
            attacks = war_attacks[war_members_tags.index(str(attack.attacker_tag))]["attacks"]
            if attacks["first_attack"]["stars"] is None:
                attacks["first_attack"]["stars"] = attack.stars
                attacks["first_attack"]["destruction"] = attack.destruction
            else:
                attacks["second_attack"]["stars"] = attack.stars
                attacks["second_attack"]["destruction"] = attack.destruction

    # If war attacks were blank, remove them from the json
    for i in range(len(war_attacks)):
        if war_attacks[i]["attacks"]["first_attack"]["stars"] is None:
            war_attacks[i] = None
        elif war_attacks[i]["attacks"]["second_attack"]["stars"] is None:
            del war_attacks[i]["attacks"]["second_attack"]

    # Clean up all those separate lists by combining into one master list
    final_list = []
    for i in range(len(war_members_names)):
        final_list.append([
            war_members_tags[i],
            war_members_names[i].replace(" ", "_"),
            war_attacks_missed[i],
            war_attacks[i]
        ])

    with open(config.clash_json) as f:
        clash = json.load(f)

    # Update or add to the clash json with new war info
    for i in range(len(final_list)):
        if final_list[i][0] in clash:
            tag = final_list[i][0]
            clash[tag]["name"] = final_list[i][1]
            clash[tag]["misses"] += final_list[i][2]
            clash[tag]["total"] += 2
            if final_list[i][3]:
                clash[tag]["wars"].append(final_list[i][3])
            clash[tag]["in_clan"] = True
        else:
            tag = final_list[i][0]
            clash[tag] = {}
            clash[tag]["name"] = final_list[i][1]
            clash[tag]["misses"] = final_list[i][2]
            clash[tag]["total"] = 2
            clash[tag]["war_battles"] = []
            if final_list[i][3]:
                clash[tag]["wars"] = [final_list[i][3]]
            clash[tag]["in_clan"] = True
        if war.is_cwl:
            clash[tag]["total"] -= 1
            clash[tag]["misses"] -= 1

    # Calculate some player statistics from the numbers we have gathered
    for tag in clash:
        total_stars = 0
        total_destruction = 0
        attacks = 0
        if "wars" in clash[tag]:
            for war in clash[tag]["wars"]:
                for attack in war["attacks"]:
                    total_stars += war["attacks"][attack]["stars"]
                    total_destruction += war["attacks"][attack]["destruction"]
                    attacks += 1
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

    # Output calculated data to files
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(clash, f, ensure_ascii=False, indent=4)
    with open(config.war_log_json, 'w', encoding='utf-8') as f:
        json.dump(opponents, f, ensure_ascii=False, indent=4)


try:
    main()
except Exception as e:
    errors_dir = f'{config.home_dir}/errors/'
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
