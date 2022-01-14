# Clash War Tracker
This is a super simple clash of clans war performance tracker.
It started as a simple script that I ended up building on quite a bit,
so it has turned into a little bit of a mess. But it works for what I need.

I wanted to be able to track my clan members performance between wars, 
including easily seeing how many missed attacks they had.
This is then displayed on a simple webpage for viewing.

There may be tools out there that already do this, but now there's this tool too I guess.

## Dependencies
Pip packages coc.py is needed, and aiohttp as well to make that work.

Run  `pip install -r requirements.txt` to install these unless you are using docker.

If you are not using docker, you will have to sort out how to get a web server up
and running on your own if you want to use that part of this program.

You will also need a free clash of clans API account from https://developer.clashofclans.com/

## Building
I have this built into a docker container. You can build it yourself using

`docker build -t clashtracker .`

within this root directory to build your own image, or you can pull my docker image

`docker pull benfugate/clashtracker`

## Usage

### Docker
```
docker run \
    -p 80:80 \
    -e COC_USERNAME=<USERNAME> \
    -e COC_PASSWORD=<PASSWORD> \
    -e COC_CLAN_TAG=<CLAN_TAG> \
    -v <DATA FOLDER>:/clash-tracker/data/ \
    benfugate/clashtracker:latest
```

Replace the username, password, and clan tag with your own information and with the clan you would like to track.

By exposing port 80, you will be able to view the simple webpage at `localhost:80`

If you do not mount a `<DATA_FOLDER>` volume to `docker run`, the data files contained in `/clash-tracker/data/`
will be overwritten when the docker image is updated. The `data/` folder in this repo can and should be
used as a template for the host mounting point to retain data through updates.

Crontab will check for clan war updates every 5 minutes, and the changes will be reflected on the webpage, or in
`/clash-tracker/data/json/clash.json` (or `/clash-tracker/data/json/current_war.json` for an active war)

## Other

If you just want to use the python script, you will want to update `config.json`
with your api login and clan information. You do not need to modify the `DOCKER` variable, this is set automatically
if `docker run` is used.

Then you can just run `python3 main.py` and it will output the results to the `data/json/` directory.

A crontab will have to be set up if you want to automate the scripts.

### pick_war_players.py

A new python script was added, which depends on the clash.json file generationed by `main.py`.
When this script runs (at midnight, every day) it will create another file `war_picks.json` with 10/15/20/25 players to
participate in the next war. These players are determined based on if they have participated recently, if they are new
to the clan, and have good war performance.

## Notes

The docker container will backup the clash.json every day at midnight to 
`/clash-tracker/data/backups`, mainly just in case I break something in the code.

Also at midnight, a helper script `get_active_players.py` will run. This script gets the list of players
currently in the clan, and will mark any players you have been tracking as not in the clan in the `clash.json`.
They will also no longer appear on the webpage view, but the data will persist in case they rejoin in which the
flag will be updated. This script will also update clash.json to reflect the players current town hall and trophy numbers.

By default, the config.json will have a value `WAR_FILTER_SECONDS`. This value will be used
to filter out old war attack information. Any attack that is older than this value in seconds (1 month by default)
will no longer be considered when creating player evaluation variables.

If a player does not have any attacks in the filter period, then their lifetime average stars and score will be
displayed instead

If `main.py` fails to run due to an error, the errors get output to `/clash-tracker/data/errors`
which can help diagnose what's going wrong.