#!/usr/bin/env python3
import pafy
import json
import threading
from collections import deque
import os
import signal
import sys
from time import time
from time import sleep
from gtts import gTTS
import boto3
import subprocess
import socket
import ssl
from sys import platform
from save import Save
import requests
import psutil
import base64
from exception import PrintException
from contextlib import closing
from botocore.exceptions import ClientError
from getanimeflv import getanime

from exception import PrintException
ssl._create_default_https_context = ssl._create_unverified_context
# playerFile = 'mediatest.exe'
playerFile = 'intermediatemedia.exe'
simplePlayer = 'simpleplay.exe'
radio = 'http://pool.anison.fm:9000/AniSonFM(128)'
def decir(m,voz='google',idioma='es'):
    if(voz == 'google'):
        for i in range(3):
            try:
                tts = gTTS(text=m,lang=idioma,slow=False)
                path = '/tmp/' + str(int(time())) + '.mp3'
                tts.save(path)
                break
            except Exception as e:
                PrintException()
                print('error obteniendo audio reintentando')
            else:
                break
        else:
            return
        return path
    else:
        try:
            polly =  boto3.client('polly',region_name='us-west-2')
            response = polly.synthesize_speech(Text=m,OutputFormat='mp3',VoiceId=voz)
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    path = '/tmp/' + str(int(time()*1000)) + '.mp3'
                    try:
                        with open(path, "wb") as file:
                            file.write(stream.read())
                    except IOError as error:
                        print('IOERROR:',error)
                    else:
                    	return path

        except ClientError as error:
            print('ClientError:',error)

def waitClose(child):
	streamdata = child.communicate()[0]
class Channel:
	def __init__(self,name,token,uid,volume,type,chatid):
		self.name = name
		self.token = token
		self.uid = uid
		self.volume = volume
		self.type = type
		self.chatid = chatid
waitState = {}
stateCon = {}
radioChannels = {}
def prestartPlayer(channel,playid,userid):
	global playing
	try:
		startPlayer(channel,playid,userid)
	except:
		PrintException()
	s = Save()
	print("REMOVIENDO LO QUE ESTA EN REPRODUCCION DE",channel.chatid)
	try:
		s.removeReproduciendo(channel.chatid)
		ram = psutil.virtual_memory().available/1048576
		cpu = psutil.cpu_percent()

		if(ram < 200):
			try:
				s.updateInfo(instanceid,ram,2,cpu)
			except:
				pass
			activado = False
		else:
			activado = True
			s.updateInfo(instanceid,ram,1,cpu)
	except:
		PrintException()
	s.close()
	checkQueue(channel.chatid)
	playing -= 1
	try:
		playLock.release()
	except Exception as e:
		pass
		# print(e)
def startPlayer(channel,playid,userid):
		token = channel.token
		name = channel.name
		uid = channel.uid
		volume = channel.volume
		t = channel.type
			
		if(not playid.startswith('https://www3.animeflv.net/ver/') and playid.startswith('http') ):
			streams = [playid]
			killChat(channel.chatid)
			if(platform == 'win32'):
				args = [simplePlayer,name,token,str(uid),str(volume),str(t) ] + streams
			else:
				args = ["wine64",simplePlayer,name,token,str(uid),str(volume),str(t) ] + streams
			proc = subprocess.Popen(args,stdout=subprocess.PIPE)
			data = proc.communicate()[0]
		else:
			# if(playid.startswith('https://www3.animeflv.net/ver/')):
			# 	filename = getanime(playid[25:])
			# 	streams = [filename]
			# else:
			# 	streams = getStreams(playid,t)
			# 	filename = streams[0]
			streams = ['./plasticlove.mp3']
			killChat(channel.chatid)
			if(platform == 'win32'):
				args = [playerFile,name,token,str(uid),str(volume),playid,userid,str(t) ] + streams
			else:
				args = ["wine64",playerFile,name,token,str(uid),str(volume),playid,userid,str(t) ] + streams
			print('iniciando player',args)
			waitState[channel.name] = threading.Event()
			proc = subprocess.Popen(args,stdout=subprocess.PIPE)
			waitState[channel.name].wait()
			t = threading.Thread(target=waitClose,args=(proc,))
			t.daemon = True
			t.start()
			print('player iniciado')
			print('name',channel.name)
			conn = stateCon[channel.name]
			try:
				data = conn.recv(1024)
			except Exception as e:
				PrintException()
				os.remove(filename)
				return
			js = json.loads(data.decode('utf-8'))
			state = js['state']
			if(state=='success'):
				js['comando'] = 'playing'
				js['chatid'] = channel.chatid
				print('sending playing command')
				r = json.dumps(js)
				print(r)
				sendToBot(r.encode('utf-8'))
			else:
				os.remove(filename)
				return
			try:
				print('ESPERANDO POR EL MENSAJE FINAL')
				state = json.loads(conn.recv(1024).decode('utf-8'))['state']
				print('LLEGO EL MENSAJE FINAL',state)
			except Exception as e:
				print('NO LLEGO EL MENSAJE FINAL')
				print(e)
				state = 'ended'
			if(state == 'ended'):
				os.remove(filename)
				return
			killChat(channel.chatid)
def play_audio(channel,playid):
	global activado
	token = channel.token
	name = channel.name
	uid = channel.uid
	volume = channel.volume
	t = channel.type
	streams = [playid]
	killChat(channel.chatid)
	
	args = ["wine64",simplePlayer,name,token,str(uid),str(volume),"1" ] + streams
	print(args)
	proc = subprocess.Popen(args,stdout=subprocess.PIPE)
	data = proc.communicate()[0]
	killChat(channel.chatid)
	s = Save()
	print("REMOVIENDO LO QUE ESTA EN REPRODUCCION DE",channel.chatid)
	try:
		s.removeReproduciendo(channel.chatid)
		ram = psutil.virtual_memory().available/1048576
		cpu = psutil.cpu_percent()

		if(ram < 200):
			try:
				s.updateInfo(instanceid,ram,2,cpu)
			except:
				pass
			activado = False
		else:
			activado = True
			s.updateInfo(instanceid,ram,1,cpu)
	except:
		PrintException()
	s.close()
	checkQueue(channel.chatid)


def sendToBot(message):
	try:
		TCP_IP = botip
		TCP_PORT = 10120
		s = socket.socket(socket.AF_INET, # Internet
		                     socket.SOCK_STREAM) # UDP
		print('conectando socket',(TCP_IP, TCP_PORT))
		s.connect((TCP_IP, TCP_PORT))
		print('enviando mensaje')
		s.settimeout(5)
		s.send(message)
		print('esperando')
		data = s.recv(1024).decode('utf-8')
		print(data)
		s.close()
		return json.loads(data)
	except Exception as e:
		PrintException()
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
			channel = data[2:]
			print('se conecto una conexion de estado',channel)
			if(channel in waitState):
				waitState[channel].set()
			stateCon[channel] = conn
		else:
			print('se conecto un player')
			players[data] = conn
	conn.close()

def handleRemote(conn):
	BUFFER_SIZE = 102400  # Normally 1024, but we want fast response
	try:
			while 1:
				data = conn.recv(BUFFER_SIZE).decode('utf-8')
				print('mensajes recibido:',data)
				if(len(data) == 0):
					break
				js = json.loads(data)
				comando = js['comando']
				channel = js['channel']
				chatid = js['chatid']
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
					channels[chatid].volume = js['volume']
					player = players[channel]
					player.send(b'volume:%d' % (v))
					print('esperando por data del reproductor')
					data = player.recv(1024)
					conn.send(data)				
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
					killChat(chatid)
					if(channel in radioChannels):
						try:
							print('mantando a la radio')
							radioChannels[channel][0].kill()
						except Exception as e:
							print(e)
						print('sacando radio')
						radioChannels.pop(channel)
						c = channels[chatid]
						data = {"result":"ok"}
						data = json.dumps(data).encode('utf-8')
						conn.send(data)
					if(channel not in players):
						conn.send(b'{"result":"no playing"}')
						checkQueue(channel.chatid)
						continue
					# player = players[channel] 
					# player.send(b'skip')
					# print('esperando por data del reproductor')
					# try:
					# 	data = json.loads(player.recv(1024).decode('utf-8'))
					# except Exception as e:
					# 	print(e)
					# c = channels[chatid]
					# data = json.dumps(data).encode('utf-8')
					# conn.send(data)
					conn.send(b'{"result":"ok"}')
				elif(comando == 'cancel'):
					killChat(chatid)
					if(channel in channels):
						channels.pop(channel)
						conn.send(b'{"result":"ok"}')
						# player = players.get(channel)
						# if(player): 
						# 	player.send(b'skip')
						# 	data = player.recv(1024)
						# 	conn.send(data)
					else:
						conn.send(b'{"result":"no playing"}')
				elif(comando == 'check'):
					if(not activado):
						conn.send(b'{"result":"full"}')
					else:
						r = checkQueue(chatid)
						if(r):
							conn.send(b'{"result":"ok"}')
						else:
							conn.send(b'{"result":"no"}')							
	except Exception as e:
		PrintException()
		print(e)
	conn.close()
def killChat(chatid):
	proc = subprocess.Popen(["ps","ax"],stdout=subprocess.PIPE)
	r = proc.communicate()
	l = r[0].decode('utf-8').split('\n')
	for i in l:
		if(chatid in i):
			print(i)
			pid = None
			try:
				splited = i.split(' ')
				for x in splited:
					if(x.isdigit()):
						pid = int(x)
						break
			except:
				PrintException()
			try:
				if(pid):
					os.kill(pid,signal.SIGKILL)
			except Exception as e:
				print(e)
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
voces = []
def cargarVoces():   
    try:
        for i in boto3.client('polly',region_name='us-west-2').describe_voices()['Voices']:
            voiceid = i['Id']
            if(voiceid not in voces):
                voces.append(voiceid)
    except Exception as e:
        print('Error cargando voces',e)
        pass
    if('google' not in voces):
        voces.append('google')
    print(voces)
    text = ''
    for v in voces:
        text += ' ' + v
    return text
activado = True
def updateInfo():
	global activado
	s = Save()
	ram = psutil.virtual_memory().available/1048576
	cpu = psutil.cpu_percent()
	s.reproductorInfo(instanceid,localip,ram,1,cpu,instancetype)
	s.removeReproduciendo(instanceid=instanceid)
	s.close()
	lastUpdate = 0
	while 1:
		try:
			sleep(300)
			s.connect()
			ram = psutil.virtual_memory().available/1048576
			cpu = psutil.cpu_percent()

			if(ram < 100):
				try:
					s.updateInfo(instanceid,ram,2,cpu)
				except:
					pass
				activado = False
			else:
				activado = True
				s.updateInfo(instanceid,ram,1,cpu)
		except:
			PrintException()
		s.close()

def checkQueue(chatid):
	global playing
	lastUpdate = 0
	s = Save(autoConnect=False)
	try:
		s.connect()
		queue = s.checkQueue(chatid)
		for c in queue:
			r = s.checkReproduciendo(chatid)
			t = c['type']
			print(c)
			print(t)
			if(t == 1 and r):
				s.removeFromQueue(c['id'])
				if(c['texto'].startswith('gracias') or c['playid'].startswith('audios/') or c['playid'].startswith('voces/') or c['playid'].startswith('canciones/')  ):
					continue
				data = {
					"comando":"mensaje",
					"chatid": chatid,
				}
				if(c['idioma'] == 'es'):
					data['mensaje'] = "No se puede reproducir audio mientras se esta reproduciendo una cancion"
				else:
					data['mensaje'] = "Cannot play audio while playing music" 
				sendToBot(json.dumps(data).encode('utf-8'))
			if(r):
				if(t == 2):
					killChat(chatid)
					s.clearQueue(chatid)
					s.removeReproduciendo(chatid)
					s.close()
					return False
				else:
					s.close()
					return False
			try:
				s.removeFromQueue(c['id'])
				s.addReproducir(chatid,c['playid'],localip,instanceid)
			except Exception as e:
				print(e)
				s.close()
				continue
			channelInfo = s.loadChannelInfo(chatid)
			print(channelInfo)
			channel = Channel(channelInfo['channel'],channelInfo['token'],channelInfo['uid'],channelInfo['volume'],channelInfo['type'],chatid)
			channels[chatid] = channel
			if(channel.volume == 0):
				s.close()
				return False
			if(t == 1 or t == 2):
				text = c['playid']
				texto = c['texto']
				if(text.startswith('http')):
					path = text
				elif(text in voces):
					path = decir(c['texto'],voz=c['playid'],idioma=c['idioma'])
				elif(text.startswith('audios/') ):
					path = text.replace('audios/',audiosPath)
				elif(text.startswith('canciones/') ):
					path = text.replace('canciones/',cancionesPath)
				elif(text.startswith('voces/')):
					if(channel.volume > 50):
						channel.volume = 50
					path = text.replace('voces/',vocesPath)
				elif(text.startswith('openings/')):
					path = text.replace('openings/',openingsPath)
				t = threading.Thread(target=play_audio,args=(channel,path))
				t.start()
				s.close()
				return True
				# play_audio(channel,path)
			else:
				t = threading.Thread(target=prestartPlayer,args=(channel,c['playid'],c['userid']))
				t.start()
				playing += 1
				s.close()
				return True
	except:
		PrintException()
	s.close()

playing = 0
playLock = threading.Lock()
try:
	localip = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4',timeout=1).text
	botip = '34.217.222.236'
	r = requests.get('http://169.254.169.254/latest/meta-data/instance-id',timeout=1)
	instanceid = r.text
	r = requests.get('http://169.254.169.254/latest/meta-data/instance-type',timeout=1)
	instancetype = r.text
except:
	instanceid = 'i-local'
	instancetype = 'local'
	localip = '127.0.0.1'
	botip = '127.0.0.1'
	# PrintException()
if(os.path.exists('audios/')):
	audiosPath = 'audios/'
else:
	audiosPath = '../audios/'
if(os.path.exists('voces/')):
	vocesPath = 'voces/'
else:
	vocesPath = '../voces/'
if(os.path.exists('canciones/')):
	cancionesPath = 'canciones/'
else:
	cancionesPath = '../canciones/'
if(os.path.exists('openings/')):
	openingsPath = 'openings/'
else:
	openingsPath = '../openings/'
print('cargando voces')
cargarVoces()
print('voces cargadas')

t = threading.Thread(target=localConnections,args=())
t.start()
t = threading.Thread(target=updateInfo,args=())
t.start()

remoteConnection()