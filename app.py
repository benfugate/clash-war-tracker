#!/bin/python3
import json
import os
import sys
import time
import traceback
from flask import Flask, render_template, request

app = Flask(__name__)

clash_file = "data/json/clash.json"
current_war_file = "data/json/current_war.json"
war_picks_file = "data/json/war_picks.json"

def load_member_info(member, order):
    member_info = {}
    member_info["trophies"] = member["trophies"]
    member_info["town_hall"] = member["town_hall"]
    member_info["name"] = member["name"]
    member_info["percentage_missed"] = round((member["misses"] / member["total"]) * 100) if "misses" in member else ""
    member_info["player_score"] = member["player_score"]
    member_info["most_recent_war"] = member["most_recent_war"] if "most_recent_war" in member else ""
    if "time_filtered_average_stars" in member:
        member_info["average_stars"] = member["time_filtered_average_stars"]
    else:
        member_info["average_stars"] = member["average_stars"] if "average_stars" in member else ""
        member_info["player_score"] = f"{member_info['player_score']}*"

    return [member_info[item] for item in order]


@app.route('/', methods=['GET'])
def index():
    load_file = current_war_file if os.path.exists(current_war_file) else clash_file
    with open(load_file) as f:
        clash = json.load(f)
    output = []
    order = ["trophies", "town_hall", "name", "percentage_missed", "average_stars", "player_score"]
    for member in clash:
        if clash[member]["in_clan"]:
            output.append(load_member_info(clash[member], order))
    output = [member[1:] for member in sorted(output,key=lambda l:l[0], reverse=True)]
    return render_template('index.html', data=output)


@app.route('/war_picks', methods=['GET', 'POST'])
def war_picks():
    in_war = []
    not_in_war = []
    order = ["trophies", "town_hall", "name", "percentage_missed", "average_stars", "player_score", "most_recent_war"]
    with open(war_picks_file) as f:
        clash = json.load(f)
        for member in clash:
            if clash[member]["in_war"]:
                in_war.append(load_member_info(clash[member], order))
            else:
                not_in_war.append(load_member_info(clash[member], order))
    in_war = sorted(in_war,key=lambda l:l[0])
    not_in_war = sorted(not_in_war,key=lambda l:l[0])
    return render_template('war_picks.html', in_war=in_war, not_in_war=not_in_war)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
