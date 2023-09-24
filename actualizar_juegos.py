#!/usr/bin/env python3
import amino
from pprint import pprint
import os
import signal
import requests
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
client = amino.Client()
client.login(email='',password='')
sub_client = amino.SubClient(comId='67',profile=client.profile)

juegos = os.listdir('juegos')
juegos.remove('__pycache__')
juegos.remove('vor')
extra = []
for juego in juegos:
	try:
		with open('juegos/' + juego + '/links.txt','r') as h:
			old_links = [line.rstrip() for line in h]
		links = []
		for l in old_links:
			print('actualizando')
			print(l)
			img_data = requests.get(l).content
			links.append(client.upload_media(data=img_data))
		with open('juegos/' + juego + '/links.txt','w') as h:
			for i in links:
				h.write(i + '\n')
	except Exception as e:
		print('pasando juego ' + juego)
client.logout()