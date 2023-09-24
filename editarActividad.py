#!/usr/bin/env python3
import amino
import os
import sys
from time import time
import ujson as json
from save import Save
import socket
from time import sleep
from plot import plotActividad
from exception import PrintException
client = amino.Client()
def hilo3(comid,js,bubbleid=None):
	sub_client = client.sub_client(comid)
	if(not js['extensions']):
	    sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],defaultBubbleId=bubbleid)
	elif('style' not in js['extensions']):
	    sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],defaultBubbleId=bubbleid)
	elif('backgroundMediaList' in js['extensions']['style'] ):
	    sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],backgroundImage=js['extensions']['style']['backgroundMediaList'][0][1],defaultBubbleId=bubbleid)
	else:
	    sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],backgroundColor=js['extensions']['style']['backgroundColor'],defaultBubbleId=bubbleid)

def log_in(alias):
	s.connect()
	login = s.loginInfo(alias=alias,dictionary=True)
	s.close()
	if(login['jsonResponse'] and login['lastLogin'] + 3600*24 > time()):
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
		r1['secret'] = login['secret']
		r1 = json.dumps(r1)
		s.connect()
		s.newLogin(id=client.profile.id,jsonResponse=r1)
		s.close()
	return login

def getActiveChats():
    TCP_IP = "127.0.0.1"
    TCP_PORT = 10004
    try:
        s = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_STREAM) # UDP
        s.connect((TCP_IP, TCP_PORT))
        data = {
            "comando":"activity"
        }

        s.send(json.dumps(data).encode('utf-8'))

        data = s.recv(100).decode('utf-8')
        data = json.loads(data)
        if(data['result'] == 'ok'):
            return data['count']
        else:
            return False
    except Exception as e:
        print(e)

s = Save(file='default.set',autoConnect=False)
bots = ['jasmine','manami','kotomi','natsuki','misaki','mei','kumi','kanna']
bubbles = {
	"jasmine":"a2ac6450-fcb5-463c-aa27-80edbce63c4c",
	"mei":"d07de212-f159-4609-8de0-8b1bafc1dde3",
	"kanna":"036d33b8-e995-4211-b435-414c60ee8fc1",
	"kotomi":"4c2d0076-8812-4023-be6a-68146bdae66d",
	"manami":"b96f1f52-a9f7-48a1-8724-5d9290ff969d",
	"natsuki": "c9d68fcf-93d9-465f-b5d1-9611ca79213b",
	"misaki": "05b7cb37-31ba-4b97-b767-be9b7c37f63b",
	"kumi": "c6633c06-8585-4cc8-b402-983c5affb64d"
}
log_in('jasmine')
ts = []
while 1:
	try:
		img = plotActividad(chat=True)
		link = client.upload_media(f=img)
		print(link)
		if (not link):
			sleep(10)
			continue
		for b in bots:
			log_in(b)
			botid = client.profile.id
			comids = client.sub_clients(size=100).comId
			n = getActiveChats()
			if(not n):
				sleep(1)
				continue
			js = None
			for comid in comids:
				# if(comid != 228964941):
				# 	continue
				sub_client = client.sub_client(comid)
				js = sub_client.get_user_info(botid,raw=True)['userProfile']
				content = js['content']
				p = content.find('[cccccccccc]\n')
				if(p > 0):
					content = content[p+13:]
				if('[IMG=ACT]' not in content):
					content += '\n[IMG=ACT]'
				text = '[c]Chats activos en la ultima hora %d\n\n[c]\n[c]\n[cccccccccc]\n' % (n) 
				js['content'] = text + content
				mediaList = js['mediaList']
				for m in mediaList:
					if(len(m) >= 4):
						if(m[3] == 'ACT'):
							m[1] = link
							break
				else:
					mediaList.append([100,link,'Actividad ultima hora','ACT'])
				hilo3(comid,js,bubbles[b])
				sleep(5)
			if(not js):
				continue
			if('avatarFrame' in js):
				frameid = js['avatarFrame']['frameId']
				sub_client = client.sub_client(228964941)
				r = sub_client.apply_frame(frameid,True)
				if(r != 200):
				  r = sub_client.purchase_frame(frameid,autoRenew=True)
				  print(r)
				  r = sub_client.apply_frame(frameid,True)
				print(r)
	except KeyboardInterrupt:
		break
	except:
		PrintException()
