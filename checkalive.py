#!/usr/bin/env python3
from time import time,sleep
import ujson as json
import requests
import os
import signal
import psutil
device = {
    "device_id": "017E81F926343109D52317B2483DCFFCFA6FA7FFA9EB3397240931103E2C882C571AF3664C4B39E2FE",
    "device_id_sig": "AaauX/ZA2gM3ozqk1U5j6ek89SMu",
    "user_agent": "Dalvik/2.1.0 (Linux; U; Android 7.1; LG-UK495 Build/MRA58K; com.narvii.amino.master/3.3.33180)"

}

class Headers:
    def __init__(self,data = None, type = None,sid=None):
        headers = {
            "NDCDEVICEID": device['device_id'],
            "NDC-MSG-SIG": device['device_id_sig'],
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": device['user_agent'],
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        if data: headers["Content-Length"] = str(len(data))
        if sid: headers["NDCAUTH"] = f"sid={sid}"
        self.headers = headers
def login(secret,device_id):
    data = {
        "v": 2,
        "secret": secret,
        "deviceID": device_id,
        "clientType": 100,
        "action": "normal",
        "timestamp": int(time() * 1000)
    }
    data = json.dumps(data)
    header = Headers(data=data).headers
    header['NDCDEVICEID'] = device_id
    response = requests.post(f"https://service.narvii.com/api/v1/g/s/auth/login", headers=header, data=data,timeout=None)
    r = json.loads(response.text)
    if('sid' not in r):
    	return
    return r['sid']
def send_message(chatid,comid,message,sid):
    t = time()
    data = {
        "type": 0,
        "content": message,
        "clientRefId": int(t / 10 % 1000000000),
        "attachedObject": None,
        "extensions": {},
        "timestamp": int(t * 1000)
    }
    data = json.dumps(data)
    hs = Headers(data=data,sid=sid).headers
    response = requests.post(f"https://service.narvii.com/api/v1/x{comid}/s/chat/thread/{chatid}/message", headers=hs, data=data)

    return response

def get_chat_messages(chatid,comid,sid,size=25):
    response = requests.get(f"https://service.narvii.com/api/v1/x{comid}/s/chat/thread/{chatid}/message?v=2&pagingType=t&size={size}", headers=Headers(sid=sid).headers)
    return json.loads(response.text)['messageList']
mycomid = 228964941
testcomid = 15391148
testchat = '9955c4dc-c55e-45f0-a80e-7d155af7fc33'

secret = '31 VblVMtHs 401ab401-8e9e-4ed7-91a2-50eeba7ab956 3.233.211.164 0e4a69d1b3066ca9a127890a5531929f3818f16b 1 1615275129 _WtQ33ev93JtB-4e3Pd6kXdQ0hQ'
f = 'logs/shita.sid'
if(os.path.exists(f) and time() < os.path.getmtime(f) + 43200):
	startTime = os.path.getmtime(f)
	with open(f,'r') as h:
		sid = h.read()
else:
	startTime = time()
	sid = login(secret,device['device_id'])
	with open(f,'w') as h:
		h.write(sid)
print(sid)
startTime = time()
oldMessages = []
def handler(signum, frame):
    print('recibido sigterm, ignorando')

signal.signal(signal.SIGTERM, handler)

while 1:
    retry = 3
    if(not os.path.exists('logs/activado')):
        sleep(60)
        continue
    while 1:
        r = send_message(testchat,testcomid,'/ping',sid)
        sleep(10)
        messages = get_chat_messages(testchat,testcomid,sid,size=10)
        funciona = False
        for m in messages:
            if(m['uid'] == '401ab401-8e9e-4ed7-91a2-50eeba7ab956'):
            	continue
            if(m['messageId'] in oldMessages):
            	continue
            oldMessages.append(m['messageId'])
            funciona = True
        if(not funciona):
            print('no funciona')
            if(retry > 0):
            	retry -= 1
            	continue
            with open('logs/recent.pid','r') as h:
            	pid = int(h.read())
            try:
            	os.kill(pid,signal.SIGKILL)
            except Exception as e:
            	print(e)
            os.system('python3 lite5.py &')
            sleep(120)
            retry = 3
            break
        else:
        	print('funciona')
        	retry = 3
        	sleep(10)
        	break

    if( time() > startTime + 43200):
    	sid = login(secret,device['device_id'])
    	with open(f,'w') as h:
    		h.write(sid)
    	startTime = time()
