#!/usr/bin/env python3
import amino
import os
import sys
import threading
from save import Save
from time import time
from time import sleep
import ujson as json
import json
mycomid = 106909944

def hilo(client,bot):
	scs = client.sub_clients(size=100)
	bot['comids'] = scs.comId

def hilo3(sub_client,userid,chatid):
	sub_client.invite_to_chat(userid,chatid)

def hilo2(bot,comid,lider):
	sub_client = bot['client'].sub_client(comid)
	chats = sub_client.get_chat_threads(size=100,raw=True)['threadList']
	ts = []
	for c in chats:
		chatid = c['threadId']
		t = threading.Thread(target=hilo3,args=(sub_client,lider['userid'],chatid))
		t.start()
		ts.append(t)
	for t in ts:
		t.join()
	bot['comids'].remove(comid)
	bot['client'].leave_community(comid)
def login(userid,client=None):
    if(not client):
        client = amino.Client()
    client.device_id = '01FDA5110556B382F849B30AEF9986D10C71A75048151CA3686BBB8A28BFA10B3417DDBFE8CC556D3F'
    login = s.loginInfo(id=userid)
    if(login[2] and login[3] + 3600*8 > time()):
        print('inicio cache')
        client.login_cache(login[2] )
    else:
        print('iniciando normal')
        r = client.login(email=login[0],password=login[1],get=True)

        if(type(r) == dict or r[0] != 200):
            print(r)
            return None
        r1 = json.loads(r[1])
        r1['userProfile']['content'] = 'cache'
        r1 = json.dumps(r1)
        s.newLogin(id=client.profile.id,jsonResponse=r1)
    # print('client',id(client))
    # s.db.close()
    return client
s = Save(file='default.set')
print(1)
s.cursor = s.db.cursor(dictionary=True)
print(2)
pbots = s.loadBots(None)
print(3)
s.cursor = s.db.cursor(dictionary=False)
print(4)
bots = {}
ts = []
topop = []
for bot in pbots:
	print(bot['userid'])
	client = login(bot['userid'])
	if(not client):
		continue
	bot['client'] = client
	t = threading.Thread(target=hilo,args=(client,bot))
	t.start()
	ts.append(t)
for t in ts:
	t.join()
for bot in pbots:
	if(bot['public'] == 1):
		bots[bot['userid']] = bot
bots = dict(sorted(bots.items(), key=lambda item: item[1]['comids'],reverse=True))
ts = []
for lider in bots.values():
	print(len(lider['comids']) )
	for comid in lider['comids']:
		if(int(comid) == mycomid or int(comid) == 67):
			continue
		for bot in bots.values():
			if(bot['userid'] == lider['userid']):
				continue
			if(comid in bot['comids']):
				t = threading.Thread(target=hilo2,args=(bot,comid,lider))
				t.start()
				ts.append(t)
				if(len(ts) >= 10):
					for t in ts:
						t.join()
					ts = []
	for t in ts:
		t.join()