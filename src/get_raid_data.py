import coc
import json
import asyncio
from config import Config

config = Config()

if not (config.username or config.password or config.clan_tag):
    raise ValueError("Missing at least one config variable")

async def get_raid_data():
    client = coc.Client(key_names="clash-war-tracker", key_count=1)
    try:
        await client.login(config.username, config.password)
        raid_log = await client.get_raid_log(config.clan_tag)
    except Exception as e:
        print(f"API Error: {e}")
        return

    with open(config.clash_json) as f:
        clash = json.load(f)

    for raid in raid_log:
        for member in raid.members:
            if member.tag not in clash:
                clash[member.tag] = {"raids": []}
            elif "raids" not in clash[member.tag]:
                clash[member.tag]["raids"] = []
            
            # Avoid duplicate entries
            raid_exists = False
            for r in clash[member.tag]["raids"]:
                if r["attack_time"] == raid.start_time.seconds:
                    raid_exists = True
                    break
            
            if not raid_exists:
                clash[member.tag]["raids"].append({
                    "attack_count": member.attack_count,
                    "capital_resources_looted": member.capital_resources_looted,
                    "attack_time": raid.start_time.seconds
                })

    for tag in clash:
        if "raids" in clash[tag]:
            total_attacks = sum(r["attack_count"] for r in clash[tag]["raids"])
            total_looted = sum(r["capital_resources_looted"] for r in clash[tag]["raids"])
            if total_attacks > 0:
                clash[tag]["average_raid_loot"] = round(total_looted / total_attacks, 2)
            else:
                clash[tag]["average_raid_loot"] = 0

    with open(config.clash_json, "w", encoding="utf-8") as f:
        json.dump(clash, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_raid_data())
