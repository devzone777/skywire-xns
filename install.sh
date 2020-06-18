#!/bin/bash
########Skywire XNS#########

echo -e "\e[1;97;44m       SSS  KK   K YY  YY  CCC   OOO  IIIIII NN  NN                 \e[0m"
echo -e "\e[1;97;44m      SS SS KK  K  YY  YY CC  C OO OO   II   NN  NN                 \e[0m"
echo -e "\e[1;97;44m      SSS   KK K    YYYY  CC    OO OO   II   NN  NN                 \e[0m"
echo -e "\e[1;97;44m        SS  KKK      YY   CC    OO OO   II   NNN NN                 \e[0m"
echo -e "\e[1;97;44m         SS KK K     YY   CC    OO OO   II   NN NNN                 \e[0m"
echo -e "\e[1;97;44m      SS SS KK  K    YY   CC  C OO OO   II   NN  NN                 \e[0m"
echo -e "\e[1;97;44m       SSS  KK   K   YY    CCC   OOO  IIIIII NN  NN                 \e[0m"

echo -e "\e[96;5mWelcome to the Skywire XNS Installer\e[25m"

echo -e "\e[31mInstalling dependancies\e[0m"

pkill -f xns-server  # Stop skywire-xns if running
pkill -f skywire-xns # already

apt-get update  # To get the latest package lists
apt-get install curl -y
apt-get install wget -y
apt-get install python -y
apt-get install python-zmq -y
apt-get install python-twisted-core -y
apt-get install ufw -y
apt-get install screen -y
apt-get install openssl -y


#Install SSL Cert (User Prompt, use defaults)
echo -e "\e[38;5;166mCreating SSL certificate\e[0m"
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes 

#Configure Twisted
# Installs Twisted if needed, then starts a xns-server in a twisted instance,
# listening on port 8003 and 8004.
echo -e "\e[38;5;11mOpening ports for Skywire XNS\e[0m"

ufw enable
ufw allow 8003
ufw allow 8004
ufw allow 22
ufw reload


echo -e "\e[5;96mStarting Skywire XNS\e[0m"
sleep 3
kill -9 `ps -ef | grep 'Skywire-XNS'  | grep -v grep | awk '{print $2}'`
kill -9 `ps -ef | grep 'xns-server.py'  | grep -v grep | awk '{print $2}'`
#kill -9 $(ps -elf | grep Skywire-XNS| awk {'print $4'})
#kill -9 $(ps -elf | grep xns-server.py| awk {'print $4'})
twistd -y xns-server.py
screen -dmS Skywire-XNS ./skywire-xns.py

echo -e "\e[38;5;10mSkywire XNS is now installed and running on port 8003\nUse 'screen -ls' to find PID\nthen use 'screen -r PID'\nto enter Skywire XNS CLI console\e[0m"

