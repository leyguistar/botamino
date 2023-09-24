#!/usr/bin/env python3.7
import socket
import sys
from nudenet import NudeClassifier
import threading
import json
import requests
from time import time
from exception import PrintException
import os
classifier = NudeClassifier()
def classify(filename):
	r = classifier.classify(filename)
	if(not r):
		return False
	return r
dirs = os.listdir('interaccion')
for d in dirs:
	path ='interaccion/' + d + '/SFW/'
	npath ='interaccion/' + d + '/NSFW/'
	if(os.path.exists(path)):
		imgs = os.listdir(path)
		for i in imgs:
			name = path + i
			r = classify(path + i)
			unsafe = list(r.values()) [0]['unsafe']
			if(unsafe > 0.5):
				print(r)
			if(unsafe > 0.8):
				if(not os.path.exists(npath)):
					os.mkdir(npath)
				os.rename(name,npath + i)
				os.system('eog %s &' % (npath + i))