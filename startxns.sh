#!/bin/bash
# Startup script for Skywire XNS P2P Server

twistd -y xns-server.py
echo -e "\033[32mSkywire XNS is now running\n\033[0m"
python skywire-xns.py
