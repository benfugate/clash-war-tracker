#!/usr/bin/python3

import os
import json
import subprocess
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

cd = os.path.dirname(os.path.realpath(__file__))
clash_file = f"{cd}/data/json/clash.json"
current_war_file = f"{cd}/data/json/current_war.json"
war_picks_file = f"{cd}/data/json/war_picks.json"
last_refresh_time = datetime.now() - timedelta(minutes=20)


def load_member_info(member, order, skip_check=False):
    if not skip_check and (not member["in_clan"] or not "trophies" in member):
        return None
    member_info = {"trophies": member["trophies"], "town_hall": member["town_hall"], "name": member["name"],
                   "percentage_missed": f"{round((member['misses'] / member['total']) * 100)}%" if "misses" in member \
                       else "",
                   "player_score": member["player_score"],
                   "most_recent_war": member["most_recent_war"] if "most_recent_war" in member else ""}
    if member_info["most_recent_war"]:
        member_info["most_recent_war"] = datetime.fromtimestamp(member_info["most_recent_war"]).strftime('%x')
    if "time_filtered_average_stars" in member and member["time_filtered_average_stars"]:
        member_info["average_stars"] = member["time_filtered_average_stars"]
    else:
        if "average_stars" not in member:
            member_info["average_stars"] = ""
        else:
            member_info["average_stars"] = "" if not member["average_stars"] else f"{member['average_stars']}*"
            member_info["player_score"] = f"{member_info['player_score']}*"

    return [member_info[item] for item in order]


@app.route('/', methods=['GET'])
def index():
    load_file = current_war_file if os.path.exists(current_war_file) else clash_file
    with open(load_file) as f:
        clash = json.load(f)
        modify_time = datetime.fromtimestamp(os.path.getmtime(load_file)).strftime('%c')
    output = []
    order = ["trophies", "town_hall", "name", "percentage_missed", "average_stars", "player_score"]
    for member in clash:
        if clash[member]["in_clan"]:
            member_info = load_member_info(clash[member], order)
            if member_info:
                output.append(member_info)
    output = [member[1:] for member in sorted(output, key=lambda l:l[0], reverse=True)]
    return render_template('index.html', data=output, load_file=os.path.basename(load_file), last_modified=modify_time)


@app.route('/war_picks', methods=['GET', 'POST'])
def war_picks():
    global last_refresh_time
    if request.method == 'POST':
        if request.form.get('update') == 'update':
            if datetime.now() - timedelta(minutes=20) > last_refresh_time:
                last_refresh_time = datetime.now()
                subprocess.run(["python3", "/clash-tracker/src/get_active_players.py"])
                return redirect("/war_picks")
    in_war = []
    not_in_war = []
    order = ["trophies", "town_hall", "name", "percentage_missed", "average_stars", "player_score", "most_recent_war"]
    with open(war_picks_file) as f:
        clash = json.load(f)
        modify_time = datetime.fromtimestamp(os.path.getmtime(war_picks_file)).strftime('%c')
        for member in clash:
            member_info = load_member_info(clash[member], order, skip_check=True)
            if clash[member]["in_war"]:
                in_war.append(member_info)
            else:
                not_in_war.append(member_info)
    in_war = sorted(in_war, key=lambda l:l[0], reverse=True)
    not_in_war = sorted(not_in_war, key=lambda l:l[0], reverse=True)

    # Replace the first index (trophies) with a simple list counter
    number = 1
    for i in range(len(in_war)):
        in_war[i][0] = number
        number += 1
    for i in range(len(not_in_war)):
        not_in_war[i][0] = number
        number += 1

    return render_template('war_picks.html', in_war=in_war, not_in_war=not_in_war, last_modified=modify_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
