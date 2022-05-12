#!/bin/python3
import json
import os
import sys
import time
import traceback
from flask import Flask, render_template, request

app = Flask(__name__)

clash_file = "/clash-tracker/data/json/clash.json"
current_war = "/clash-tracker/data/json/current_war.json"


@app.route('/', methods=['GET'])
def index():
    load_file = current_war if os.path.exists(current_war) else clash_file
    with open(load_file) as f:
        clash = json.load(f)
    output = []
    for member in clash:
        if member["in_clan"]:
            town_hall = member["town_hall"]
            name = member["name"]
            player_score = member["player_score"]
            if member["time_filtered_average_stars"]:
                average_stars = member["time_filtered_average_stars"]
            else:
                average_stars = member["average_stars"]
                player_score = f"{player_score}*"
            percentage_missed = round((member["misses"]/member["total"])*100)
            output.append([town_hall, name, percentage_missed, average_stars, player_score])
    # TODO sort the list by trophies
    return render_template('index.html', data=output)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('war_picks.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
