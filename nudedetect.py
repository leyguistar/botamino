#!/usr/bin/env python3.7
import socket
import sys
from nudenet import NudeClassifier
import threading
import json
import requests
from time import time
from exception import PrintException
import os
TCP_IP = "0.0.0.0"
TCP_PORT = 15150
classifier = NudeClassifier()
s = socket.socket(socket.AF_INET, # Internet
	socket.SOCK_STREAM) # UDP
s.bind((TCP_IP, TCP_PORT))
s.listen(20)
def classify(filename):
	r = classifier.classify(filename)
	for k in r:	
		d = r[k]
		for j in d:
			d[j] = str(d[j])
	if(not r):
		return False
	return json.dumps(r)
def han(conn,addr):
	try:
		data = conn.recv(1024)
		r = json.loads(data.decode('utf-8'))
		print('recibido',r)
		t = r["type"]
		result = None
		delete = False
		if(t == 'url'):
			print('procesando url')
			url = r['url']
			name = '/tmp/' + url[url.rfind('://')+3:].replace('.','').replace('/','')
			rn = name + '.result'
			if(os.path.exists(rn)):
				with open(rn,'r') as h:
					result = h.read()
			else:
				delete = True
				print(r['url'])
				response = requests.get(r['url'])

				if(response.status_code == 200):
					with open(name,'wb') as h:
						h.write(response.content)
				else:
					print('error in fetch url',response.status_code)
				filename = name
		elif(t == 'data'):
			print('enviando ok')
			conn.send('ok'.encode('utf-8'))
			size = r['size']
			ext = r['extension']
			b = bytearray()
			data = conn.recv(65536)
			b.extend(data)
			while(len(b) < size):
				print('actual size',len(b))
				data = conn.recv(65536)
				if(not data):
					break
				b.extend(data)
			if(len(b) != size):
				print('data do not match the size')
				print('expected: %d\nActual size: %d' % (size,len(data)) )
				return
			print('processing')
			delete = True
			filename = '/tmp/' + str(time()).replace('.','') + ext
			with open(filename,'wb') as h:
				h.write(b)
		elif(t == 'file'):
			filename = r['filename']
			rn = filename + '.result'
			if(os.path.exists(rn)):
				with open(rn,'r') as h:
					result = h.read()
			
		if(not result):
			result = classify(filename)
			if(result):
				with open(filename + '.result','w') as h:
					h.write(result)
				print('result in: ' + filename + '.result' )
			else:
				result = '{}'
		print('result',result)
		conn.send(result.encode('utf-8'))

		conn.close()
	except:
		PrintException()
	if(delete):
		try:
			os.remove(filename)
		except:
			PrintException()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print('ready\nlisto')
while 1:
	conn, addr = s.accept()
	t = threading.Thread(target=han,args=(conn,addr))
	t.start()
	# han(conn,addr)
