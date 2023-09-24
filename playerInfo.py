#!/usr/bin/env python3
import socket
from time import sleep
import json
from litefuns import send_message,sendYoutubeObject
from litefuns import getSubClient
from litefuns import getNickname
from litefuns import send_video_youtube_info
from liteobjs import sockets
from liteobjs import channels,comidChat
from liteobjs import VOICE_SERVER_IP,VOICE_SERVER_PORT
from exception import PrintException
import datetime
import threading
def checkMessage(conn):
	try:
		data = conn.recv(1024).decode('utf-8')
		if(not len(data)):
		    return
		conn.send('{"result":"ok"}'.encode('utf-8'))
		print('llego mensaje del reproductor',data)
		js = json.loads(data)
		c = js['comando']
		chatid = js['chatid']
		if(c == 'playing'):
			id = js['id']
			position = js['position']
			userid = js['userid']
			sub_client = getSubClient(chatid)
			if(not sub_client):
				return
			if(id.startswith('http')):
				send_message(chatid,'Streaming: %s\nAgregado por:\nTranscurrido: %d\n' % (id,getNickname(userid,sub_client),str(datetime.timedelta(seconds=position))))
			else:
				duration = js['duration']
				if(chatid in channels):
					ch = channels[chatid]
					if(ch.type == 5):
						comid = comidChat[chatid]
						send_video_youtube_info(chatid,sub_client,id)

				sendYoutubeObject(chatid,sub_client,id,position,duration,userid)
		elif(c == 'recibido'):
			id = js['id']
			position = js['position']
			userid = js['userid']
			sub_client = getSubClient(chatid)
			if(not sub_client):
				return
			if(id.startswith('http')):
				send_message(chatid,'Streaming: %s\nAgregado por:%s\nTranscurrido: %d\n' % (id,getNickname(userid,sub_client),str(datetime.timedelta(seconds=position))))
			else:
				duration = js['duration']
				sendYoutubeObject(chatid,sub_client,id,None,duration,userid,text2='Pedido por:\n%s' % getNickname(userid,sub_client))
		elif(c == 'mensaje'):
			message = js['mensaje']
			send_message(chatid,message)

	except:
		PrintException()

def get_player_info():
	TCP_IP = '0.0.0.0'
	TCP_PORT = 10120
	BUFFER_SIZE = 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	while 1:
		try:
			s.bind((TCP_IP, TCP_PORT))
		except:
			sleep(1)
		else:
			break
	print('conectado audio')
	s.listen(10)
	while 1:
		try:
			conn, addr = s.accept()
			t = threading.Thread(target=checkMessage,args=(conn,))
			t.start()
		except:
			PrintException()