import os
import json

with open('/clash-tracker/config.json') as f:
    config = json.load(f)

config["COC_USERNAME"] = os.environ.get("COC_USERNAME")
config["COC_PASSWORD"] = os.environ.get("COC_PASSWORD")
config["COC_CLAN_TAG"] = os.environ.get("COC_CLAN_TAG")
config["OUTPUT_DIR"] = "/var/www/html/"

with open('/clash-tracker/config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)
