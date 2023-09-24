#!/usr/bin/env python3
import os
from time import time,sleep


while 1:
	with open('logs/recent.pid','r') as h:
		pid = int(h.read())
	try:	
		os.kill(pid,0)
	except OSError:
		print('perecio, reviviendo')
		os.system('/botamino/lite5.py &')
	sleep(60)