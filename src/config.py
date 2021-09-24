import os
import sys
import json


class Config:

    def __init__(self):
        with open(f'{sys.path[0]}/config.json') as f:
            config = json.load(f)
        self.username = config["COC_USERNAME"]
        self.password = config["COC_PASSWORD"]
        self.clan_tag = config["COC_CLAN_TAG"]
        self.storage_folders = f"{os.path.split(sys.path[0])[0]}/data/"
        output_path = f"{os.path.split(sys.path[0])[0]}/data/json/"
        if config["DOCKER"]:
            output_path = "/clash-tracker/data/json"
        self.clash_json = f"{output_path}/clash.json"
        self.current_war_json = f"{output_path}/current_war.json"
        self.war_log_json = f"{output_path}/wars.json"
