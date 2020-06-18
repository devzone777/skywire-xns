#!/bin/bash
# Script to stop Skywire XNS Server

pkill -f "skywire-xns"
pkill -f "xns-server"
echo -e "\033[32mSkywire XNS has stopped\n\033[0m"
