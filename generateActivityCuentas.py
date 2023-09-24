#!/usr/bin/env python3
import amino
from save import Save
from time import time
import threading
import random
from time import sleep
def send(sub_client,ti):
	try:
		r = sub_client.send_active_obj(ti-600,ti,60,timeout=10)
		print(r)
	except Exception as e:
		print(e)	
with open('deviceids.txt','r') as h:
	deviceids = h.read().split('\n')

while 1:
	s = Save()
	s.cursor.execute('select email,sid,id,lastLogin from cuentas;')
	results =  s.cursor.fetchall()
	s.close()
	for email,sid,userid,lastLogin in results:
		ti = int(time())
		if(ti-86400 > lastLogin):
			continue
		client = amino.Client()
		client.sid = sid
		client.device_id = random.choice(deviceids)
		sub_client = client.sub_client(15391148)
		ts = []
		# for tir in range(ti-3000,ti+1,600):
		t = threading.Thread(target=send,args=(sub_client,ti))
		t.start()
		sleep(0.1)
		ts.append(t)
		if(len(ts) > 20):
			for t in ts:
				t.join()
			ts = []