#!/usr/bin/env python3
import amino
import os
import sys
from collections import deque
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
from user import User
from chat import Chat
import io
import base64
from mensaje import Mensaje
from comando import Comando
import unicodedata
import ujson as json
import pafy 
from amino.lib.util import headers as aminoHeaders
from amino.lib.util import helpers
from PIL import Image, ImageDraw, ImageSequence,ImageFont
from aminosocket import SocketHandler
from exception import PrintException
from join_call import join_voice_chat
	
client = amino.Client()

ley = ''
mycomid = 228964941
testcomid = 15391148
def log_in(alias):
	login = s.loginInfo(alias=alias,dictionary=True)
	if(login['lastLogin'] and login['lastLogin'] + 3600*24 > time()):
		print('inicio cache')
		client.login_cache(login['jsonResponse'] )
	else:
		print('iniciando secret')
		r = client.login(secret=login['secret'],get=True)
		if(type(r) != tuple or r[0] != 200):
			print('F')
			print(r)
			return None
		r1 = json.loads(r[1])
		r1['userProfile']['content'] = 'cache'
		r1 = json.dumps(r1)
		s.newLogin(id=client.profile.id,jsonResponse=r1)
	return login
s = Save(file='default.set')
log_in('moon')
# with open('posts/comentario_waifus.txt','r') as h:
# 	comentario = h.read()
sub_client = client.sub_client(210208021)
wikis = []
husbandos = []
waifus = []
for start in range(0,301,100):
	husbandos += sub_client.get_wikis_category("670df48a-6942-4759-b838-1dc3c44d87ce",start=start,size=100)['childrenWrapper']['itemList']
	
	waifus += sub_client.get_wikis_category("68e6d772-7f30-4095-850a-2ee225334d1d",start=start,size=100)['childrenWrapper']['itemList']
wikis = husbandos + waifus
for wiki in wikis:
	wikiId = wiki['itemId']
	# if(wiki['keywords'] == 'husbando'):
	# 	wiki['keywords'] = 'waifu'
	# 	r = sub_client.edit_wiki(wikiId,wiki)
	# 	print(r)
	# continue
	# if(wiki['commentsCount'] == 0):
	# 	r = sub_client.comment(comentario,wikiId=wikiId)
	# 	print(r)
	# 	sleep(10)
	# continue
	props = wiki['extensions']['props']
	nombre = wiki['label']
	origen = None
	mal_id = None
	for p in props:
		if(p['title'] == 'origen'):
			origen = p['value']
		if(p['title'] == 'MyAnimeList ID'):
			mal_id = int(p['value'])
	if(not origen):
		print('error para ',nombre,'no origen')
		input()
	if(not mal_id):
		print('error para ',nombre,'no origen')
		input()
	descripcion = wiki['content']
	tipo = wiki['keywords']
	print(tipo)
	icon = wiki['mediaList'][0][1]
	try:
		s.addWaifu(nombre,origen,descripcion,wikiId,tipo,img=icon,mal_id=mal_id)
	except mysql.connector.errors.IntegrityError:
		continue
	except:
		PrintException()
		continue
	response = requests.get(icon)
	if(response.status_code != 200):
		print('error en la imagen',response.status_code,nombre,wikiId,icon)
		del wiki['mediaList'][0]
		r = sub_client.edit_wiki(wikiId,wiki)
		icon = wiki['mediaList'][0][1]
		print(r)
		response = requests.get(icon)
	if(response.status_code != 200):
		print('error en la imagen',response.status_code,nombre,wikiId,icon)
		input()
	img = response.content
	if(not icon.endswith('.png')):
	    img = Image.open(io.BytesIO(img))
	    img.save('waifus/%s.png' % (wikiId),format="PNG")
	else:
	    with open('waifus/%s.png' % (wikiId),'wb') as h:
	        h.write(img)