#! /usr/bin/env python
# -*- coding: utf-8 -*-
import socket

default_port = 8003 # default port when adding a new server
listen_port = 8003 # server listens on this port
my_address = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
              if not ip.startswith("10.")][0]
dns_module_listen_port = 8004
default_ttl = 60   # time to live in seconds
default_record_lifetime = 3600 * 24 * 30 # 1 month
