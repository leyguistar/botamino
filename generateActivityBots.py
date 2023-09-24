#!/usr/bin/env python3
import amino
from save import Save
from time import time
from time import sleep
import json
import threading
import random
import requests
from exception import PrintException
def login(userid=None,client=None,save=None,alias=None):
    if(not save):
        s = Save(expected=True)
    else:
        s = save
    try:
        if(not client):
            client = amino.Client()
        if(userid):
            login = s.loginInfo(id=userid,dictionary=True)
        elif(alias):
            login = s.loginInfo(alias=alias,dictionary=True)
            userid = login['id']
        else:
            if(s != save):
                s.close()
                del s
            return None
        device_id = random.choice(deviceids)

        if(login['jsonResponse'] and login['lastLogin']+86400 > time()):
            print('inicio cache')
            secret = json.loads(login['jsonResponse'])['secret']
            client.login_cache(login['jsonResponse'])
            # client.login(secret=secret )
            # s.newSecret(userid,secret)
        elif(login['secret']  ):
            print('iniciando secret')
            r = client.login(secret=login['secret'],get=True,error=True,device_id=device_id)
            r1 = json.loads(r[1])
            secret = login['secret']
            r1['userProfile']['content'] = 'cache'
            r1['secret'] = secret
            r1 = json.dumps(r1)
            s.newLogin(id=client.profile.id,jsonResponse=r1)

        else:
            print('iniciando normal')
            r = client.login(email=login['email'],password=login['password'],get=True,error=True)

            if(type(r) == dict or r[0] != 200):
                print(userid)
                print(r)
                if(s != save):
                    s.close()
                    del s

                return None
                # return r['api:statuscode']
            r1 = json.loads(r[1])
            r1['userProfile']['content'] = 'cache'
            secret = r1['secret']

            r1 = json.dumps(r1)
            s.newLogin(id=client.profile.id,jsonResponse=r1)
            s.newSecret(id=client.profile.id,secret=secret)
        # print('client',id(client))
    except:
        PrintException()
    if(s != save):
        s.close()
        del s
    return client
def send2(sub_client,ti,client):
    try:
        r = sub_client.send_active_obj(ti-600,ti,60,timeout=10)
        if(r['api:statuscode'] == 814):
            client.leave_community(sub_client.comId)
        print(r)
    except Exception as e:
        print(e)	

def send(sub_client,ti,client):
	send2(sub_client,ti,client)
	return
	ts = []
	try:
		for ti in range(ti-3000,ti+1,600):
			t = threading.Thread(target=send2,args=(sub_client,ti,client))
			t.start()
			ts.append(t)
		for t in ts:
			t.join()
	except Exception as e:
		print(e)	
with open('deviceids.txt','r') as h:
	deviceids = h.read().split('\n')
cacheComids = {}
s = Save()
bots = s.loadBots(dictionary=True)
s.close()
i = 0
for b in bots:
	if(b['userid'] == '7c8d446e-c6b1-409a-897b-952c6fa95052'):
		del bots[i]
		break
	i += 1
response = requests.get('https://service.narvii.com/api/')
t = response.elapsed.seconds + (response.elapsed.microseconds/100000)
if(t < 0.5):
    sle = 1
else:
    sle = 0
while 1:

    for b in bots:
        print(b)
        client = login(b['userid'])
        ti = int(time())
        if(b['userid'] not in cacheComids):
        	comids = client.sub_clients(size=100).comId
        	cacheComids[b['userid']] = comids
        else:
        	comids = cacheComids[b['userid']]
        ts = []
        for comid in comids:
            if(comid == 255022587):
            	continue
            if(comid == 67):
                continue
            sub_client = client.sub_client(comid)
            sleep(sle)
            t = threading.Thread(target=send,args=(sub_client,ti,client))
            t.start()
            ts.append(t)
        for t in ts:
        	t.join()
