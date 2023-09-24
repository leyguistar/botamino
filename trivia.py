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
from save import Save
from time import time
import json
from googletrans import Translator
import html2text
from exception import PrintException
s = Save(file='default.set')

from user import User
from chat import Chat
from mensaje import Mensaje
from aminohelpers import login as loginfun
def getNickname(userid):
	if(userid == None):
		return ''
	if(userid in usersObjects):
		if(usersObjects[userid].alias != ""):
			return usersObjects[userid].alias
	return sub_client.get_user_info(userid).nickname

def send_message(chatid,mensaje,withResponse=False):
	return sub_client.send_message(message=mensaje, chatId=chatid,messageType=tipoMensaje,withResponse=withResponse)

def send_marco(chatid,mensaje,mn):
	m = marcos[mn][0] + '\n\n' + mensaje + '\n\n' + marcos[mn][1]
	send_message(chatid,m)	

def send_imagen(chatid,link=None,file=None):
	if(link!=None):
		sub_client.send_message(chatId=chatid,link=link)
	else:
		sub_client.send_message(chatId=chatid,filePath=file)

def mostrarPuntuaciones(chatid,users):
	m = ''
	pequipos = {}
	for u in users:
		m += getNickname(u) + ': ' + str(users[u]) + '\n\n'
		if(u in equipos):
			if(equipos[u] in pequipos):
				pequipos[equipos[u]] += users[u]
			else:
				pequipos[equipos[u]] = users[u]
	if(pequipos):
		m += 'Equipos:\n\n'
		for e in pequipos:
			m += e + ': ' + str(pequipos[e]) + '\n\n'
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

def getCategorias():
	global categorias
	for i in range(3):
		try:
			categories = json.loads(requests.get('https://opentdb.com/api_category.php').text)['trivia_categories']
		except Exception as e:
			print(chatid,'Error obteniendo categorias intentando de nuevo')
			categories = None
		else:
			break
	if(categories == None):
		send_message(chatid,'Error empezando trivia por favor intente mas tarde')
		matar(0)
	categorias = {}

	for c in categories:
		categorias[c['id'] - 8] = traducir(c['name'])
	return categorias

def traducir(t):
	for i in range(5):
		try:
			return translator.translate(t,dest='es').text
		except Exception as e:
			print("Error traduciendo " + str(e))
			PrintException()
			# send_message(chatid,'ocurrio un error traduciendo')
	return t
def enviarPregunta(turno):
	global respuesta,lr,lrs,ignoreID
	print('turno ' + str(turno) )
	pregunta = traducir(html2text.html2text(data[turno]['question']) )
	respuesta = traducir(html2text.html2text(data[turno]['correct_answer']) )

	respuestas = [respuesta] + [traducir(html2text.html2text(i)) for i in data[turno]['incorrect_answers']]
	send_message(chatid,pregunta)
	i = 0
	random.shuffle(respuestas)
	lrs = ''
	text = ''
	ignoreID = None
	for r in respuestas:
		if(r == respuesta):
			lr = letras[i]
		lrs += letras[i]
		if(unaPoruna):
			t = send_message(chatid,letras[i] + ': ' + r,withResponse=True)
		else:
			text += letras[i] + ': ' + r + '\n\n'
		i+=1
	if(not unaPoruna):
		t = send_message(chatid,text,withResponse=True)
	try:
		ignoreID = t['message']['messageId']
	except:
		pass

def iniciar(n = 10,dificultad = '',categoria = 0,tipo=''):
	global preguntas,data
	print('iniciando')
	link = 'https://opentdb.com/api.php?' 
	if(categoria != 0):
		link += 'category=' + str(categoria+8) + '&'
	if(dificultad != ''):
		link += 'difficulty=' + str(dificultad) + '&'
	if(tipo != ''):
		link += 'type=' + str(tipo) + '&'
	link += 'amount=' + str(n)

	print(link)
	text = requests.get(link).text
	print(text)
	res = json.loads(text)
	while(res['response_code'] == 1):
		n-=1
		link = link[:link.rfind('=')+1] + str(n)
		print(link)
		text = requests.get(link).text
		print(text)
		res = json.loads(text)

	data = res['results']
	print(data)
	return n


categorias = {}
respuestas = []
juego = sys.argv[2]
chatid = sys.argv[1]
preguntas = None

tipoMensaje=0
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
tipoMensaje=0
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
# send_message(chatid,'Proximamente: trivia')
# signal.signal(os.getpid(),9)
chat = s.loadChat(chatid)
chatThread = sub_client.get_chat_thread(chatid,raw=True)['thread']
host = chatThread['uid']
coHost = chatThread['extensions'].get('coHost',[])
chat.ops[host] = 3
for c in coHost:
	chat.ops[c] = 2


leybot = '4882156e-efce-4a4b-88ca-02baff4d5e89'
translator = Translator()
tokenres = requests.get('https://opentdb.com/api_token.php?command=request').text
token = json.loads(tokenres)['token']
turno = 0
turnoJugador = 0
iniciado = False
libre = True
puntos = 0
dificultad = ''
categoria = 0
n = 10
data = None
lr = ''
lastTurno = time()
tRespondido = 0
tPorTurno = 0
aTurno = turno
tLimite = 600
unaPoruna = False
ignoreID = ""
difs = ['nada','easy','medium','hard']
difss = {'facil':'easy','normal':'medium','dificil':'hard'}
difin = {'easy':'facil','medium':'normal','hard':'dicifil'}
letras = 'ABCDEFGHIJKLMN'
wusers = {}
usersListos = []
jugadores = []
equipos ={}
lrs = ''
skipCharacters = '- :!.'
trans = str.maketrans('','',skipCharacters)
try:
	send_imagen(chatid,file='juegos/trivia/trivia.jpg')
except:
	pass
with open('juegos/' + juego + '/informacion.txt', 'r') as handler:
	send_marco(chatid,handler.read(),14)
getCategorias()


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
				rs = 'Se acabo el tiempo\n\nRespuesta: ' + respuesta
				send_message(chatid,rs)
				print(rs)
				if(turno == (n-1) ):
					print('matando juego')
					mostrarPuntuaciones(chatid,users)
					mostrarPosiciones(chatid,users,14)
					send_marco(chatid,'juego terminado',14)
					matar(0)
				else:
					print('incrementando turno')
					turnoJugador += 1
					turno += 1
					usersListos = []
					enviarPregunta(turno)
					if(not libre):
						send_message(chatid,'Turno de ' + getNickname(jugadores[int(turnoJugador % len(jugadores)) ]))

			if(time() - lastTurno >= tLimite):
				send_message(chatid,'terminando juego por inactividad')
				mostrarPuntuaciones(chatid,users)
				mostrarPosiciones(chatid,users,14)
				send_marco(chatid,"\n\nJuego terminado\n\n",14)
				matar()

			messageList = sub_client.get_chat_messages(chatId=chatid,size=10)  # Gets messages of each chat
			ignorar = False
			for nickname, content, id, userid, extensions , tipo , mediaValue, createdTime in zip(messageList.author.nickname, messageList.content, messageList.messageId, messageList.author.id, messageList.extensions,messageList.type, messageList.mediaValue,messageList.createdTime):
				if id in oldMessages: 
					continue
				oldMessages.append(id)
				print(nickname, content)  # Simple output with nickname and messages
				if(ignoreID == id):
					print('ignorando')
					ignorar = True
					continue
				if(content is None or tipo == 111):
					continue

				usersid = getMentions(extensions)
				replyid = getMessageReply(extensions)
				print('jugadores ' + str(jugadores) )
					
				if(not ignorar and content.upper() in lrs and iniciado and userid in users and (userid == jugadores[int(turnoJugador % len(jugadores)) ] or libre)):
					print('comparando: ' + content.upper())
					print(usersListos)
					print(userid)
					print(lr)
					if(userid in usersListos):
						continue
					usersListos.append(userid)
					if(content.upper() == lr):
						wusers[userid] = datetime.datetime.strptime(createdTime, '%Y-%m-%dT%H:%M:%SZ')
					elif((not libre and content.upper() in lrs) or len(usersListos) == len(users)):
						send_message(chatid,'respuesta incorrecta')
						rs = 'Respuesta: ' + respuesta
						send_message(chatid,rs)
							

						if(turno == (n-1) ):
							mostrarPuntuaciones(chatid,users)
							mostrarPosiciones(chatid,users,14)
							send_marco(chatid,'juego terminado',14)
							matar(0)
						else:
							turnoJugador += 1
							turno += 1
							usersListos = []
							enviarPregunta(turno)
							if(not libre):
								send_message(chatid,'Turno de ' + getNickname(jugadores[int(turnoJugador % len(jugadores)) ]))


				m = content[content.find(" "):]
				content = str(content).split(" ")

				if content[0][0] == "/":  
					if(userid in chat.ops ):
						if(content[0][1:] == "sacar"):
							for u in usersid:
								if(u in users):
									if(jugadores.index(u) < turnoJugador):
										turno -= 1
									if(u in equipos):
										equipos.pop(u)

									users.pop(u)
									send_message(chatid,getNickname(u) + " Ha sido removido del juego")
						elif(content[0][1:] == "dificultad"):
							if(len(content) == 2):
								if(content[1].isdigit()):
									d = int(content[1])
									if(d < 1 or d > 3):
										send_message(chatid,'Solo estan las siguientes dificultades:\n1 = facil\n2 = normal\n3 = dificil' )
									else:
										dificultad = difs[d]								
										send_message(chatid,'Dificultad: ' + difin[dificultad])
								elif(content[1] in difss):
									dificultad = difss[content[1]]
									send_message(chatid,'Dificultad: ' + difin[dificultad])
								else:
									send_message(chatid,'uso: /dificultad [1|2|3|facil|normal|dificil]')									
							else:
								send_message(chatid,'uso: /dificultad [1|2|3|facil|normal|dificil]')
						elif(content[0][1:] == "categoria" or content[0][1:] == "categorias" or content[0][1:] == "categoría"):
							if(len(content) == 2 and content[1].isdigit):
								c = int(content[1])
								if(c not in categorias):
									send_message(chatid,'No esta esa categoria')
								else:
									send_message(chatid,'Categoria: ' + categorias[c])
									categoria = c
									continue
							text = 'Categorias:\n'
							for c in categorias:
								text += str(c) +'. ' + categorias[c] + '\n'
							send_message(chatid,text)
						elif(content[0][1:] == "start"):
							if(iniciado):
								continue
							if(len(jugadores) == 0):
								send_message(chatid,'primero entren con /entrar')
								continue
							send_marco(chatid,'Iniciando juego',14)
							turno = 0

							turnoJugador = 0
							iniciado = True
							if(len(content) == 2):
								if(content[1].isdigit()):
									ns = int(content[1])
									if(ns > 50):
										send_message(chatid,'no pueden haber mas de 50 preguntas')
									elif(ns < 5):
										send_message(chatid,'no pueden haber menos de 5 preguntas')
									else:
										n = ns
										n = iniciar(n,dificultad,categoria)
										if(n != ns):
											send_message(chatid,'No habian suficientes preguntas jugando con ' + str(n) + ' preguntas')
										enviarPregunta(turno)
							else:
								n = iniciar(n,dificultad,categoria)
								enviarPregunta(turno)
							lastTurno = time()
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

						elif(content[0][1:] == "pasar" and iniciado):
							rs = 'Respuesta: ' + respuesta
							send_message(chatid,rs)
							if(turno == (n-1) ):
								mostrarPuntuaciones(chatid,users)
								mostrarPosiciones(chatid,users,14)
								send_marco(chatid,'juego terminado',14)
								matar(0)
							else:
								turno += 1
								turnoJugador += 1
								usersListos = []
								enviarPregunta(turno)
								if(not libre):
									send_message(chatid,'Turno de ' + getNickname(jugadores[int(turnoJugador % len(jugadores)) ]))
						elif(content[0][1:] == "libre"):
							if(content[1] == 'on'):
								send_message(chatid,'modo libre')
								libre = True
							elif(content[1] == 'off'):
								send_message(chatid,'modo por turnos')
								libre = False
						elif(content[0][1:] == "junto"):
							if(len(content) < 2):
								send_message(chatid,'uso: /junto [on|off]')
							else:
								if(content[1] == 'on'):
									send_message(chatid,'Respuestas juntas')
									unaPoruna = False
								elif(content[1] == 'off'):
									send_message(chatid,'Respuestas una por una')
									unaPoruna = True
						elif(content[0][1:] == "limite"):
							if(len(content) == 2 and content[1].isdigit):
								tPorTurno = int(content[1])
								if(tPorTurno != 0 ):
									send_message(chatid,'limite de tiempo por turno: ' + str(tPorTurno) + 's')
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
							if(jugadores.index(userid) < turnoJugador):
								turno -= 1
							if(userid in usersListos):
								usersListos.remove(userid)
							if(userid in equipos):
								equipos.pop(u)

							users.pop(userid)
							send_message(chatid,getNickname(userid) + " Ha abandonado el juego")
						if(len(users) == 0):
							send_message(chatid,'se salieron todos')
							send_marco(chatid,'juego terminado',14)
							matar(0)


					jugadores = list(users.keys())
					if(iniciado and not libre ):
						print('Turno de ' + getNickname(jugadores[int(turnoJugador % len(jugadores)) ]))
						send_message(chatid,'Turno de ' + getNickname(jugadores[int(turnoJugador % len(jugadores)) ]))


			if(len(wusers) > 0 ):
				uw = min(wusers.items(), key=operator.itemgetter(1))[0]
				send_message(chatid,getNickname(uw) + " gana 1 punto\n\n" + respuesta )
				users[uw] += 1
				wusers = {}
				if(turno == (n-1) ):
					mostrarPuntuaciones(chatid,users)
					mostrarPosiciones(chatid,users,14)
					send_marco(chatid,'juego terminado',14)
					matar(0)
				else:
					turno += 1
					turnoJugador += 1
					usersListos = []
					enviarPregunta(turno)
					if(not libre):
						send_message(chatid,'Turno de ' + getNickname(jugadores[int(turnoJugador % len(jugadores)) ]))

		except Exception as e:
			print("error ")
			print(e)
			PrintException()
