import os
import json

with open('/clash-tracker/src/config.json') as f:
    config = json.load(f)

config["COC_USERNAME"] = os.environ.get("COC_USERNAME")
config["COC_PASSWORD"] = os.environ.get("COC_PASSWORD")
config["COC_CLAN_TAG"] = os.environ.get("COC_CLAN_TAG")
config["DOCKER"] = True

with open('/clash-tracker/src/config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)
