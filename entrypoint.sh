#!/bin/bash
python3 /clash-tracker/src/docker_setup.py
cron
python3 /clash-tracker/app.py