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
        self.clash_json = config["OUTPUT_DIR"] + "clash.json"
        self.current_war_json = config["OUTPUT_DIR"] + "current_war.json"
        self.war_log_json = config["OUTPUT_DIR"] + "wars.json"
        self.home_dir = os.path.split(sys.path[0])[0]
        if config["HOME_IS_SRC"]:
            self.home_dir = sys.path[0]
