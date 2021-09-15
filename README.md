# Clash War Tracker
This is a super simple clash of clans war performance tracker.

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

`docker build -t clash-tracker .`

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
    benfugate/clashtracker:latest
```

Replace the username, password, and clan tag with your own information and with the clan you would like to track.

By exposing port 80, you will be able to view the simple webpage at `localhost:80`

Crontab will check for clan war updates every 5 minutes and the changes will be reflected on the webpage, or in
`/var/www/html/clash.json` (or `/var/www/html/current_war.json` for an active war)

### Other

If you just want to use the python script, you will want to update `config.json`
with your api login and clan information. Do not touch the `OUTPUT_DIR` or `HOME_IS_SRC`
variables unless you know what you're changing.

Then you can just run `python3 main.py` and it will output the results to the `www/` directory.

A crontab will have to be set up if you want to automate the scripts.

## Notes

The docker container will backup the clash.json every day at midnight to 
`/clash-tracker/backups`, mainly just in case I break something in the code.

Also at midnight, a helper script `get_active_players.py` will run. This script gets the list of players
currently in the clan, and will mark any players you have been tracking as not in the clan in the `clash.json`
They will also no longer appear on the webpage view, but the data will persist in case they rejoin in which the
flag wull be updated.

If `main.py` fails to run due to an error, the errors get output to `/clash-tracker/errors`
which can help diagnose what's going wrong.