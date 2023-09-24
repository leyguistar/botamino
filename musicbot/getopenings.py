#!/usr/bin/env python3
import pafy
import os
import threading
from time import sleep

def download(name,id):
	print('iniciando descarga de',id,'en',name)
	v = pafy.new(id)
	v.getbestaudio(preftype="m4a",ftypestrict=True).download(name)
	print('listo')
ids = os.listdir('openings')
ids = [i for i in ids if (not i.endswith('txt')) ]
for i in ids:
	songs = [x for x in os.listdir('openings/' + i) if x.endswith('.id')]
	d = 'openings/%s/' % (i)
	for s in songs:
		with open(d + s,'r') as h:
			youtubeid = h.read()
		name = d + s.replace('.id','.m4a')
		if(not os.path.exists(name)):
			print('descargando',name)
			download(d + s.replace('.id','.m4a'),youtubeid)
		else:
			print('ya esta',name)
