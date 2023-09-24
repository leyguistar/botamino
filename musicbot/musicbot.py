#!/usr/bin/env python3
import pafy
import json
import threading
from collections import deque
import os
import sys
from time import time
#from gtts import gTTS
#import boto3
import subprocess
import socket
import ssl
from sys import platform
ssl._create_default_https_context = ssl._create_unverified_context
# playerFile = 'mediatest.exe'
playerFile = 'intermediatemedia.exe'
simplePlayer = 'simpleplay.exe'
radio = 'http://pool.anison.fm:9000/AniSonFM(128)'
def waitClose(child):
	streamdata = child.communicate()[0]
class Channel:
	def __init__(self,name,token,uid,volume,type,queue):
		self.name = name
		self.token = token
		self.uid = uid
		self.volume = volume
		self.type = type
		self.queue = queue
waitState = {}
stateCon = {}
radioChannels = {}
def startPlayer(channel):
	while (channel.queue):
		token = channel.token
		name = channel.name
		uid = channel.uid
		volume = channel.volume
		t = channel.type
		request = channel.queue.popleft()
		id = request['id']
		userid = request['userid']
		if(id.startswith('http')):
			streams = [id]
			if(platform == 'win32'):
				args = [simplePlayer,name,token,str(uid),str(volume),str(t) ] + streams
			else:
				args = ["wine64",simplePlayer,name,token,str(uid),str(volume),str(t) ] + streams
			proc = subprocess.Popen(args,stdout=subprocess.PIPE)
			radioChannels[name] = (proc,id,userid,int(time()) )
			data = proc.communicate()[0]
		else:
			streams = getStreams(id,t)
			if(platform == 'win32'):
				args = [playerFile,name,token,str(uid),str(volume),id,userid,str(t) ] + streams
			else:
				args = ["wine64",playerFile,name,token,str(uid),str(volume),id,userid,str(t) ] + streams
			print('iniciando player',args)
			waitState[channel.name] = threading.Event()
			proc = subprocess.Popen(args,stdout=subprocess.PIPE)
			waitState[name] = threading.Event()
			waitState[name].wait()
			t = threading.Thread(target=waitClose,args=(proc,))
			t.daemon = True
			t.start()
			conn = stateCon[name]
			try:
				data = conn.recv(1024)
			except Exception as e:
				continue
			js = json.loads(data.decode('utf-8'))
			state = js['state']
			if(state=='success'):
				js['comando'] = 'playing'
				js['chatid'] = name.replace('-AUDIO','').replace('-SCREENING_ROOM','').replace('-NEW-VIDEO','')
				if(botCon):
					print('sending playing command')
					print(json.dumps(js))
					botCon.send(json.dumps(js).encode('utf-8') )
				else:
					print('fallo al enviar sending comando')

			else:
				continue
			state = json.loads(conn.recv(1024).decode('utf-8'))['state']
			if(state == 'ended'):
				continue
	if(channel.name in channels):
		channels.pop(channel.name)
def getYoutube(id,t):
	try:
		TCP_IP = "127.0.0.1"
		TCP_PORT = 10130
		print('invocando socket')
		s = socket.socket(socket.AF_INET, # Internet
		                     socket.SOCK_STREAM) # UDP
		print('conectando socket',(TCP_IP, TCP_PORT))
		s.connect((TCP_IP, TCP_PORT))
		print('enviando mensaje')
		s.send(('{"id":"%s","type":%d}' % (id,t)).encode('utf') )
		print('esperando')
		data = s.recv(10240).decode('utf-8')
		print(data)
		s.close()
		return json.loads(data)
	except Exception as e:
		print("el error esta en getyoutube")
		print(e)
def getStreams(id,t):
	try:
		v = getYoutube(id,t)
		print(v['title'])
		return [v['title']]
		if(t == 1):
			return v['audiostreams']
		else:
			return [v['best']]		
	except Exception as e:
		print(e)
		return []
	return []
channels = {}
players = {}
botCon = None
def botConnections():
	global botCon
	TCP_IP = '0.0.0.0'
	TCP_PORT = 10106
	BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	print('esperando conexiones')
	while 1:
		try:
			conn, addr = s.accept()
			botCon = conn
			print('conexion bot recivida')
		except Exception as e:
			print(e)


def localConnections():
	TCP_IP = '127.0.0.1'
	TCP_PORT = 10102
	BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(50)
	while 1:
		conn, addr = s.accept()
		data = conn.recv(BUFFER_SIZE).decode('utf-8')
		if(data.startswith('S:')):
			print('se conecto una conexion de estado')
			channel = data[2:]
			if(channel in waitState):
				waitState[channel].set()
			stateCon[channel] = conn
		else:
			print('se conecto un player')
			players[data] = conn
	conn.close()
def handleRemote(conn):
	BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
	try:
			while 1:
				data = conn.recv(BUFFER_SIZE).decode('utf-8')
				print('mensajes recibido:',data)
				if(len(data) == 0):
					break
				js = json.loads(data)
				comando = js['comando']
				channel = js['channel']
				if(comando == "play"):
					if(channel in radioChannels):
						rc = radioChannels[channel]
						data = {"result":"ok","id":rc[1],"userid":rc[2]}
						data = json.dumps(data).encode('utf-8')
						conn.send(data)
						continue
					if(channel not in players):
						conn.send(b'{"result":"no playing"}')
						continue
					player = players[channel]
					player.send(b'play')
					print('esperando por data del reproductor')
					data = player.recv(1024)
					conn.send(data)

				elif(comando == "pause"):
					if(channel not in players):
						conn.send(b'{"result":"no playing"}')
						continue
					player = players[channel]
					player.send(b'pause')
					print('esperando por data del reproductor')
					data = player.recv(1024)
					conn.send(data)

				elif(comando == 'volume'):
					if(channel not in players):
						conn.send(b'{"result":"no playing"}')
						continue
					v = js['volume']
					channels[channel].volume = js['volume']
					player = players[channel]
					player.send(b'volume:%d' % (v))
					print('esperando por data del reproductor')
					data = player.recv(1024)
					conn.send(data)				
				elif(comando == 'queue'):
					if(channel in channels):
						data = {"result":"ok","queue":list(channels[channel].queue) }
						r = json.dumps(data).encode('utf-8')
						conn.send(r)
					else:
						data = {"result":"ok","queue":[] }
						r = json.dumps(data).encode('utf-8')
						conn.send(r)
				elif(comando == 'position'):
					if(channel in radioChannels):
						rc = radioChannels[channel]
						data = {"result":"ok","id":rc[1],"userid":rc[2],"position":int(time()-rc[3]) }
						data = json.dumps(data).encode('utf-8')
						conn.send(data)
						continue
					if(channel not in players):
						conn.send(b'{"result":"no playing"}')
						continue
					player = players[channel] 
					player.send(b'position')
					print('esperando por data del reproductor')
					data = player.recv(1024)
					conn.send(data)
				elif(comando == 'skip'):
					if(channel in radioChannels):
						try:
							print('mantando a la radio')
							radioChannels[channel][0].kill()
						except Exception as e:
							print(e)
						print('sacando radio')
						radioChannels.pop(channel)
						c = channels[channel]
						data = {"result":"ok"}
						if(c.queue):
							data['next'] = c.queue[0]
						data = json.dumps(data).encode('utf-8')
						conn.send(data)
					if(channel not in players):
						conn.send(b'{"result":"no playing"}')
						continue
					player = players[channel] 
					player.send(b'skip')
					print('esperando por data del reproductor')
					data = json.loads(player.recv(1024).decode('utf-8'))
					c = channels[channel]
					if(c.queue):
						data['next'] = c.queue[0]
					data = json.dumps(data).encode('utf-8')
					conn.send(data)


				elif(comando == 'add'):
					request = js['request']
					token = js['token']
					uid = js['uid']
					t = js['type']
					first = False
					if(channel in channels and channels[channel].token != token):
						channels[channel].token = token
					if(channel not in channels):
						channels[channel] = Channel(channel,token,uid,100,t,deque([request]) )
						t = threading.Thread(target=startPlayer,args=(channels[channel],))
						t.start()
					else:
						channels[channel].queue.append(request )

					data = {"result":"ok","queue":list(channels[channel].queue) }
					r = json.dumps(data).encode('utf-8')
					conn.send(r)
				elif(comando == 'cancel'):
					if(channel in channels):
						channels[channel].queue.clear()
						channels.pop(channel)
						conn.send(b'{"result":"ok"}')
						player = players.get(channel)
						if(player): 
							player.send(b'skip')
							data = player.recv(1024)
							conn.send(data)
					else:
						conn.send(b'{"result":"no playing"}')
	except Exception as e:
		print(e)
	conn.close()

def remoteConnection():
	TCP_IP = '0.0.0.0'
	TCP_PORT = 10105
	BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(10)
	print('esperando conexiones')
	while 1:
		try:
			conn, addr = s.accept()
			print('conexion remote recivida')
			t = threading.Thread(target=handleRemote,args=(conn,))
			t.daemon = True
			t.start()

		except Exception as e:
			print(e)
t = threading.Thread(target=localConnections,args=())
t.start()
t = threading.Thread(target=botConnections,args=())
t.start()
remoteConnection()