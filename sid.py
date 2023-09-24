#!/usr/bin/env python3
import amino
from save import Save
from time import time
import ujson as json
import sys
client = amino.Client()

def log_in(alias='bot',userid=None):
	if(userid):
		login = s.loginInfo(id=userid)
	else:
		login = s.loginInfo(alias=alias)
	# if(True):
	# if(False):
	if(login[2] and login[3] + 3600*8 > time()):
		print('inicio cache')
		client.login_cache(login[2] )
	else:
		print('iniciando normal')
		print(login[0],login[1])
		r = client.login(email=login[0],password=login[1],get=True)
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
log_in(sys.argv[1])
print(client.sid)