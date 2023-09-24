#!/usr/bin/env python3
import pafy
import socket
import json
import threading
from time import time
import os
from pytube import YouTube
TCP_IP = '0.0.0.0'
TCP_PORT = 10130
if(not os.path.exists('/tmp/youtube')):
	os.mkdir('/tmp/youtube')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)
print('esperando conexiones')
def handle(conn):
	print('manejando conexion')
	m = conn.recv(1024).decode('utf-8')
	js = json.loads(m)
	t = js['type']
	# title = '/tmp/youtube/16132422011521308.m4a'
	title = '/tmp/youtube/' + str(time()).replace('.','')
	y = YouTube("https://www.youtube.com/watch?v=" + js['id'])
	if(t == 4 or t == 5):
		title = title + '.mp4'
		y.streams.filter(progressive=True,file_extension='mp4').first().download(filename=title)
		# v.getbest(preftype="mp4",ftypestrict=True).download(title)
	else:
		title = title + '.m4a'
		y.streams.filter(only_audio=True).first().download(filename=title)
		# v.getbestaudio(preftype="m4a",ftypestrict=True).download(title)
	# audiostreams = [i.url for i in v.audiostreams]
	r = {
		"title":title,
	}
	se = json.dumps(r).encode('utf-8')
	print('enviando resultado',se)
	conn.send(se)
	conn.close()


while 1:
	try:
		conn, addr = s.accept()
		t = threading.Thread(target=handle,args=(conn,))
		t.start()
	except Exception as e:
		print(e)
