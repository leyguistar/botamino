#!/usr/bin/env python3
import amino
from save import Save
from time import time
from time import sleep
import ujson as json
from amino.lib.util import headers as aminoHeaders

client = amino.Client()
ley = 'your_uuid'
def log_in(alias='bot',userid=None):
	global sub_client
	if(userid):
		login = s.loginInfo(id=userid)
	else:
		login = s.loginInfo(alias=alias)
	if((login[2] and login[3] + 3600*8 > time()) ):
		print('inicio cache')
		client.login_cache(login[2])
	else:
		print('iniciando normal')
		r = client.login(email=login[0],password=login[1],get=True)
		if(type(r) != tuple or r[0] != 200):
			print(r)
			return None
		r1 = json.loads(r[1])
		r1['userProfile']['content'] = 'cache'
		r1 = json.dumps(r1)
		s.newLogin(id=client.profile.id,jsonResponse=r1)
	sub_client = client.sub_client(106909944)
	return login
sub_client = None
s = Save()
bots = s.loadBots()
for bot in bots:
	r = log_in(userid=bot[0])
	if(not r):
		continue
	client.join_community(106909944)
	sub_client.check_in()
	sub_client.lottery()
	log_in('ley')
	sub_client.invite_to_chat([bot[0]],'a4c85a48-a0b0-40cb-953c-e628046eb606')
	log_in(userid=bot[0])
	c = 'a4c85a48-a0b0-40cb-953c-e628046eb606'
	r = sub_client.join_chat(c)
	print(r)
	r = client.get_wallet_info()
	if(r['totalCoins'] == 0):
		continue
	print(r['totalCoins'])
	r = sub_client.send_coins(r['totalCoins'],chatId=c)
	print(r)