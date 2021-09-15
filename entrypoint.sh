#!/bin/bash
python3 /clash-tracker/src/docker_setup.py
cron
apache2-foreground