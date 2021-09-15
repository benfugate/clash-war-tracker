#!/bin/bash
python3 /clash-tracker/docker_setup.py
cron
apache2-foreground