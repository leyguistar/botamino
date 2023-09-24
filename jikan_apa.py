#!/usr/bin/env python3
import amino
import mysql.connector
import random
import sys
import signal
import os
import requests
from collections import deque
import operator
import datetime
from time import sleep
from unicodedata import normalize
import re
from jikanpy import Jikan
from save import Save
from time import time
s = Save(file='default.set')
from user import User
from chat import Chat
from mensaje import Mensaje
from exception import PrintException
from aminohelpers import login as loginfun
def getNickname(userid):
	if(userid == None):
		return ''
	if(userid in usersObjects):
		if(usersObjects[userid].alias != ""):
			return usersObjects[userid].alias
	return sub_client.get_user_info(userid).nickname

def send_message(chatid,message):
	if(tipoMensaje == 0):
		sub_client.send_message(message=('[c]' + message).replace('\n','\n[c]'), chatId=chatid,messageType=tipoMensaje)	
	else:
		sub_client.send_message(message=message, chatId=chatid,messageType=tipoMensaje)

def send_marco(chatid,mensaje,mn):
	m = marcos[mn][0] + '\n\n' + mensaje + '\n\n' + marcos[mn][1]
	send_message(chatid,m)	

def send_imagen(chatid,link):
	sub_client.send_message(chatId=chatid,link=link)

def mostrarPuntuaciones(chatid,users):
	m = ''
	for u in users:
		m += getNickname(u) + ': ' + str(users[u]) + '\n\n'
	if(m != ''):
		send_message(chatid,m)
def mostrarPosiciones(chatid,users,mn):
	if(not users):
		return
	m = 'Resultados:\n\n'
	i = 1
	if(len(equipos) > 0):
		pequipos = {}
		for u in users:
			if(u in equipos):
				if(equipos[u] in pequipos):
					pequipos[equipos[u]] += users[u]
				else:
					pequipos[equipos[u]] = users[u]
		winners = {k: v for k, v in sorted(pequipos.items(), key=lambda item: item[1],reverse=True)}
		i = 1
		for e in winners:
			m += str(i) + '. ' + e + ': ' + str(winners[e]) + 'pts.\n'
			for u in equipos:
				if(equipos[u] == e):
					m += getNickname(u) + '\n'
			m += '\n'
			i+= 1
	else:
		winners = {k: v for k, v in sorted(users.items(), key=lambda item: item[1],reverse=True)}
		for u in winners:
			m += str(i) + '. ' + getNickname(u) + ' ' + str(winners[u]) + 'pts.\n\n'   
			i += 1
	send_marco(chatid,m,mn)

def matar(i = 0):
	try:
		sys.stdout.close()
		client.logout()
		exit(0)
	except:
		pass

	os.kill(os.getpid(), signal.SIGKILL)	

def terminar():
	send_marco(chatid,"\n\nJuego %s terminado\n\n" % (sys.argv[2]),14)
	
	matar()
def handler(signum, frame):
	terminar()
signal.signal(signal.SIGALRM, handler)

def actualizar(signum, frame):
	send_message(chatid,'Terminando juego por actualizaciones')
	send_marco(chatid,"\n\nJuego terminado\n\n",14)
	matar()

signal.signal(signal.SIGTERM, actualizar) #handler para matar cuando nazca un nuevo bot

def getMentions(extensions):
	usersid = []
	if('mentionedArray' in extensions):
		for m in extensions['mentionedArray']:
			print('mencion a: ' + m['uid'])
			usersid.append(m['uid'])
	return usersid
				
def getMessageReply(extensions):
	replyid = None
	if('replyMessageId' in extensions):
		replyid = extensions['replyMessageId']
	return replyid

def enviarAnime(turno):
	global respuestas
	r = []
	if(turno >= len(animes)):
		mostrarPuntuaciones(chatid,users)
		mostrarPosiciones(chatid,users,14)
		send_marco(chatid,'juego terminado',14)
		matar(0)
	data = None
	for i in range(5):
		try:
			data = jikan.anime(animes[turno]['mal_id'])
		except Exception as e:
			print('error')
			print(e)
			print('reintentando')
			sleep(1)
		else:
			break
	if(data == None):
		send_message(chatid,'A ocurrido un error, terminando juego')
		mostrarPuntuaciones(chatid,users)
		mostrarPosiciones(chatid,users,14)
		send_marco(chatid,'juego terminado',14)
		matar(0)
	rated = data.get('rating','F')
	if('Rx' in rated):
		print('sacando',data['title'],rated)
		del animes[turno]		
		enviarAnime(turno)
		return
	print(data['title'])
	r.append(data['title'])
	if('title_english' in data):
		r.append(data['title_english'])
	if('title_synonyms' in data):
		r += data['title_synonyms']
	if('title_japanese' in data):
		r.append(data['title_japanese'])
	if('Adaptation' in data['related']):
		for a in data['related']['Adaptation']:
			r.append(a['name'])
	r = [ i.lower() for i in r if(i!=None) ]
	rs = [ i for i in r if(':' in i) ] 
	r = [ i.split(':')[0] for i in r ]
	r += rs
	r = list(dict.fromkeys(r))
	for old in respuestas:
		if(any(item in r for item in old)):
			del animes[turno]
			return enviarAnime(turno)
	respuestas.append(r)
	img_data = requests.get(data['image_url']).content
	for i in range(10):
		try:
			link = client.upload_media(data=img_data)
			send_imagen(chatid,link)
			break
		except:
			print('reintentando enviar imagen')
	else:
		send_message(chatid,'A ocurrido un error enviando la imagen al chat')
		matar()
	print([i.translate(trans) for i in respuestas[turno]])

def iniciar(n = 10,dificultad = 1):
	global animes
	animes = jikan.top(type='anime', page=dificultad, subtype='bypopularity')['top']
	random.shuffle(animes)
	enviarAnime(0)
	# for anime in animes:
	# 	r = []
	# 	data = jikan.anime(anime['mal_id'])
	# 	r.append(data['title'])
	# 	if('title_english' in data):
	# 		r.append(data['title_english'])
	# 	if('title_synonyms' in data):
	# 		r += da ta['title_synonyms']
	# 	respuestas.append(r)
	# 	sleep(1)
	# print(respuestas)
animes = []
respuestas = []
juego = sys.argv[2]
jikan = Jikan()
chatid = sys.argv[1]
preguntas = None

tipoMensaje=111
comid = '67'
userBotId = None
userBot = 'bot'
for i in sys.argv:
	if('comid=' in i):
		comid = i[6:]
	elif('mensaje=' in i):
		tipoMensaje = int(i[8:])
	elif('user=' in i):
		client = loginfun(s,alias=i[5:])
	elif('userid=' in i):
		userBotId = i[7:]
		client = loginfun(s,userid=userBotId)

sub_client = amino.SubClient(comId=comid,client=client)
oldMessages = []
pids = s.loadGamesChat(chatid)
for pid in pids:
	try:
		os.kill(pid, signal.SIGALRM)
	except OSError as e:
		print(e) 
s.removeGamesChat(chatid)
s.gameChat(chatid,os.getpid())

usersObjects = s.loadAllUsers()
users = {}
marcos = []
with open('marcos.txt', 'r') as handler:
    buf = [line.rstrip() for line in handler]
    for i in range(0,len(buf),2):
        marcos.append((buf[i],buf[i+1]))
chatid = sys.argv[1]
chat = s.loadChat(chatid)
chatThread = sub_client.get_chat_thread(chatid,raw=True)['thread']
host = chatThread['uid']
coHost = chatThread['extensions'].get('coHost',[])
chat.ops[host] = 3
for c in coHost:
	chat.ops[c] = 2



turno = 0
iniciado = False
libre = False
puntos = 0
dificultad = 1
n = 10

lastTurno = time()
tPorTurno = 0
aTurno = turno
tLimite = 600
equipos ={}

wusers = {}
skipCharacters = '- :!.,'
trans = str.maketrans('','',skipCharacters)
with open('juegos/' + juego + '/informacion.txt', 'r') as handler:
	send_marco(chatid,handler.read(),14)

try:
	r = requests.get('http://169.254.169.254/latest/meta-data/instance-id',timeout=0.1)
except:
	instanceid = 'local'
else:
	instanceid = r.text


if('LOGDIR' in os.environ):
	logPath = os.environ['LOGDIR'] + '/'
else:
	logPath = 'logs/' 
if('silent' in sys.argv):
	sys.stdout = open(logPath + __file__.replace('.py','') + chat.id + '.log', 'w')



while True:
		try:
			if(aTurno != turno):
				lastTurno = time()
				aTurno = turno
			if(iniciado and tPorTurno != 0 and time() - lastTurno >= tPorTurno):
				rs = 'Se acabo el tiempo\n\nRespuestas: \n' + '\n'.join(respuestas[turno])
				send_message(chatid,rs)
				if(turno == (n-1) ):
					mostrarPuntuaciones(chatid,users)
					mostrarPosiciones(chatid,users,14)
					send_marco(chatid,'juego terminado',14)
					matar(0)
				else:
					turno += 1
					enviarAnime(turno)

			if(time() - lastTurno >= tLimite):
				send_message(chatid,'terminando juego por inactividad')
				mostrarPuntuaciones(chatid,users)
				mostrarPosiciones(chatid,users,14)
				send_marco(chatid,"\n\nJuego terminado\n\n",14)
				matar()
			messageList = sub_client.get_chat_messages(chatId=chatid,size=20)  # Gets messages of each chat
			
			for nickname, content, id, userid, extensions , tipo , mediaValue, createdTime in zip(messageList.author.nickname, messageList.content, messageList.messageId, messageList.author.id, messageList.extensions,messageList.type, messageList.mediaValue,messageList.createdTime):
				if id in oldMessages: 
					continue
				oldMessages.append(id)
				print(nickname, content)  # Simple output with nickname and messages

				if(content is None or tipo == 111):
					continue


				usersid = getMentions(extensions)
				replyid = getMessageReply(extensions)
				s = re.sub(
			        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
			        normalize( "NFD", content), 0, re.I
			    	)
				content = normalize( 'NFC', s)
				content = normalize('NFKC',content)
				if(userid in users and iniciado):
					print('comparando')
					print(content.lower().translate(trans))
					print([i.translate(trans) for i in respuestas[turno]])
					if(content.lower().translate(trans) in 
						[i.translate(trans) for i in respuestas[turno]]):
						wusers[userid] = datetime.datetime.strptime(createdTime, '%Y-%m-%dT%H:%M:%SZ')
				m = content[content.find(" "):]
				content = str(content).split(" ")
				if content[0][0] == "/":  
					if(userid in chat.ops ):
						if(content[0][1:] == "sacar"):
							for u in usersid:

								if(u in users):
									if(len(users) == 1):
										send_message(chatid,'Abandonaron todos terminando juego')
										send_marco(chatid,"\n\nJuego terminado\n\n",14)
										matar()
								if(u in equipos):
									equipos.pop(u)

									users.pop(u)
									send_message(chatid,getNickname(u) + " Ha sido removido del juego")
						elif(content[0][1:] == "dificultad"):
							if(len(content) == 2):
								if(content[1].isdigit()):
									d = int(content[1])
									if(d > 100):
										send_message(chatid,'la dificultad no puede ser mayor a 100')
									elif(d < 1):
										send_message(chatid,'la dificultad no puede ser menor a 1')
									else:
										send_message(chatid,'dificultad ' + str(d))
										dificultad = d										
						elif(content[0][1:] == "start"):
							if(iniciado):
								continue
							if(len(content) == 2):
								if(content[1].isdigit()):
									ns = int(content[1])
									if(ns > 50):
										send_message(chatid,'no pueden haber mas de 50 animes')
									elif(ns < 5):
										send_message(chatid,'no pueden haber menos de 5 animes')
									else:
										n = ns
										lastTurno = time()
										send_marco(chatid,'Iniciando juego',14)
										turno = 0
										iniciado = True
										iniciar(n,dificultad)
							else:
								lastTurno = time()
								send_marco(chatid,'Iniciando juego',14)
								turno = 0
								iniciado = True
								iniciar(n,dificultad)
						elif(content[0][1:] == "cancelar"):
							mostrarPuntuaciones(chatid,users)
							mostrarPosiciones(chatid,users,14)
							send_marco(chatid,"\n\nJuego terminado\n\n",14)
							matar(0)
						elif(content[0][1:] == "puntos"):
							mostrarPuntuaciones(chatid,users)
						elif(content[0][1:] == "tipoMensaje"):
							if(len(content) == 2):
								if(content[1] == 'normal'):
									tipoMensaje = 0
								elif(content[1] == 'especial'):
									tipoMensaje = 111

						elif(content[0][1:] == "pasar"):
							rs = 'Respuestas: \n' + '\n'.join(respuestas[turno])
							send_message(chatid,rs)
							if(turno == (n-1) ):
								mostrarPuntuaciones(chatid,users)
								mostrarPosiciones(chatid,users,14)
								send_marco(chatid,'juego terminado',14)
								matar(0)
							else:
								turno += 1
								enviarAnime(turno)

						elif(content[0][1:] == "limite"):
							if(len(content) == 2 and content[1].isdigit):
								tPorTurno = int(content[1])
								if(tPorTurno != 0 ):
									send_message(chatid,'limite de tiempo por turno: ' + str(tPorTurno))
								else:
									send_message(chatid,'Sin limite de tiempo por turno')
							else:
								send_message(chatid,'uso: /limite [n]: segundos para que se acabe el turno, 0 para infinito')

					if(content[0][1:] == "entrar"):  
						if(userid not in users):
							users[userid] = 0
							send_message(chatid,getNickname(userid) + " Se ha unido al juego")
					elif(content[0][1:] == "equipo"):
						print('en equipo')

						if(len(content ) < 2):
							print('equivocao')
							if(userid in equipos):
								send_message(chatid,'estas en el equipo ' + equipos[userid])
							else:
								send_message(chatid,'uso: /equipo [nombre]: Para unirte a un equipo, si el equipo no existe lo crea')
						else:
							if(userid not in users):
								users[userid] = 0
								send_message(chatid,getNickname(userid) + " Se ha unido al juego")
							print('asignando equipo')

							nombre = ' '.join(content[1:])
							equipos[userid] = nombre
							print('equipo ' + nombre)
							send_message(chatid,'Entraste al equipo ' + nombre)

					elif(content[0][1:] == "equipos"):
						t = list(dict.fromkeys(equipos.values() ).keys() )
						text = 'Equipos:\n'
						for i in t:
							text += i + ':\n'
							for u in equipos:
								if(equipos[u] == i):
									text += getNickname(u) + '\n'
						send_message(chatid,text)
					elif(content[0][1:] == "jugadores"):
						text = 'Jugadores:\n'

						jugadores = list(users.keys())
						i = 1
						for u in jugadores:
							if(u in equipos):
								text += '%d. %s equipo %s\n' % (i,getNickname(u),equipos[userid])
							else:
								text += '%d. %s\n' % (i,getNickname(u))
							i+=1
						send_message(chatid,text)


					elif(content[0][1:] == "jugadores"):
						text = 'Jugadores:\n'

						jugadores = list(users.keys())
						i = 1
						for u in jugadores:
							text += '%d. %s\n' % (i,getNickname(u))
							i+=1
						send_message(chatid,text)

					elif(content[0][1:] == "dejar" or content[0][1:] == "salir"):

						if(userid in users):
							if(len(users) == 1):
								send_message(chatid,'Abandonaron todos terminando juego')
								send_marco(chatid,"\n\nJuego terminado\n\n",14)
								matar()
							if(userid in equipos):
								equipos.pop(userid)

							users.pop(userid)
							send_message(chatid,getNickname(userid) + " Ha abandonado el juego")

			if(len(wusers) > 0 ):
				uw = min(wusers.items(), key=operator.itemgetter(1))[0]
				rs = '\n'.join(respuestas[turno])
				send_message(chatid,getNickname(uw) + " gana 1 punto\n\n" + rs )
				users[uw] += 1
				wusers = {}
				if(turno == (n-1) ):
					mostrarPuntuaciones(chatid,users)
					mostrarPosiciones(chatid,users,14)
					send_marco(chatid,'juego terminado',14)
					matar(0)
				else:
					turno += 1
					enviarAnime(turno)
		except Exception as e:
			PrintException()
			print("error ")
			print(e)
