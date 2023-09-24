#!/usr/bin/env python3
import amino
import os
import sys
import itertools
import mysql.connector
import signal
import threading
import requests
from pprint import pprint
import datetime
from save import Save
from time import time
from time import sleep
import random
import ujson as json
from amino.lib.util import headers as aminoHeaders
from amino.lib.util import helpers
from aminosocket import SocketHandler
s = Save()
bots = ['jasmine','manami','kotomi','natsuki','misaki','mei','kumi','kanna','klee','rem','rushia','minato','kai','riamu','davinci','loinki','selenity','aiko']
try:
	os.mkdir('edits')
except:
	pass
for b in bots:
	print(b)
	d = 'edits/' + b + '/'
	try:
		os.mkdir(d)
	except:
		pass
	edits = s.loadEditsBots(b)
	for imagen,userid in edits:
		print(imagen,userid)
		img = requests.get(imagen).content
		ext = imagen[imagen.rfind('.'):]
		with open(d + userid + '_' + str(int(time()*1000)) +  ext,'wb' ) as h:
			h.write(img)
print('listo')