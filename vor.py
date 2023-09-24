#!/usr/bin/env python3
import amino
import mysql.connector
import random
import sys
import os
import signal
from time import time
from save import Save
import linecache
import traceback
import requests
s = Save(file='default.set')
from user import User
from chat import Chat
from mensaje import Mensaje
from aminohelpers import login as loginfun
def getNickname(userid):
	return sub_client.get_user_info(userid).nickname

def send_message(chatid,mensaje):
	sub_client.send_message(message=mensaje, chatId=chatid,messageType=tipoMensaje)

def send_marco(chatid,mensaje,mn):
	m = marcos[mn][0] + '\n\n' + mensaje + '\n\n' + marcos[mn][1]
	send_message(chatid,m)	

def matar(i = 0):
	try:
		
		client.logout()
		exit(0)
	except:
		pass

	os.kill(os.getpid(), signal.SIGKILL)	

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    traceback.print_exc()
    with open('errores.txt','a') as h:
    	h.write('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    	traceback.print_exc(file=h)

def terminar():
	send_marco(chatid,"\n\nJuego %s terminado\n\n" % (sys.argv[2]),14)
	matar()

def handler(signum, frame):
	terminar()
def actualizar(signum, frame):
	send_message(chatid,'Terminando juego por mantenimiento')
	send_marco(chatid,"\n\nJuego terminado\n\n",14)
	matar()

signal.signal(signal.SIGTERM, actualizar) #handler para matar cuando nazca un nuevo bot

	
signal.signal(signal.SIGALRM, handler)
chatid = sys.argv[1]
with open('juegos/vor/retos.txt', 'r') as handler:
	retos = [line.rstrip() for line in handler]

with open('juegos/vor/preguntas.txt', 'r') as handler:
	preguntas = [line.rstrip() for line in handler]
random.shuffle(retos)
random.shuffle(preguntas)

tipoMensaje=0
comid = 228964941
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
pids = s.loadGamesChat(chatid)
for pid in pids:
	try:
		os.kill(pid, signal.SIGALRM)
	except OSError as e:
		print(e) 
s.removeGamesChat(chatid)
s.gameChat(chatid,os.getpid())

oldMessages = []

# usersObjects = s.loadAllUsers()
users = {}
chat = s.loadChat(chatid)
chatThread = sub_client.get_chat_thread(chatid,raw=True)['thread']
host = chatThread['uid']
coHost = chatThread['extensions'].get('coHost',[])
chat.ops[host] = 3
for c in coHost:
	chat.ops[c] = 2
marcos = []
with open('marcos.txt', 'r') as handler:
    buf = [line.rstrip() for line in handler]
    for i in range(0,len(buf),2):
        marcos.append((buf[i],buf[i+1]))


chatkey = sys.argv[1]
jugadores = []
turno = 0
chatid = chat.id
iniciado = False
libre = False
lastTurno = time()
tPorTurno = 0
aTurno = turno
tLimite = 600
ley = 'your_uuid'
with open('juegos/vor/informacion.txt', 'r') as handler:
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
				send_message(chatid,'Se acabo el tiempo')
				turno += 1
				send_message(chatid,'Turno de ' + getNickname(jugadores[turno % len(jugadores)]))

			if(time() - lastTurno >= tLimite):
				send_message(chatid,'terminando juego por inactividad')
				send_marco(chatid,"\n\nJuego terminado\n\n",14)
				matar()
			messageList = sub_client.get_chat_messages(chatId=chatid,size=10)  # Gets messages of each chat
			for nickname, content, id, userid, extensions , tipo , mediaValue, createdTime in zip(messageList.author.nickname, messageList.content, messageList.messageId, messageList.author.id, messageList.extensions,messageList.type, messageList.mediaValue,messageList.createdTime):
				if id in oldMessages: 
					continue
				oldMessages.append(id)
				print(nickname, content)  # Simple output with nickname and messages
				if(content is None ):
					continue
				if(tipo == 111):
					continue
				usersid = []
				replyid = None
				if('mentionedArray' in extensions):
					for m in extensions['mentionedArray']:
						print('mencion a: ' + m['uid'])
						usersid.append(m['uid'])
				if('replyMessageId' in extensions):
					replyid = extensions['replyMessageId']

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

									if(jugadores.index(u) < turno):
										turno -= 1
									users.pop(u)
									send_message(chatid,getNickname(u) + " Ha sido removido del juego")
						elif(not iniciado and content[0][1:] == "start"):
							if(iniciado):
								continue
							if(len(users) <= 0):
								send_message(chatid,'Primero entren con /entrar')
							else:
								send_marco(chatid,'Iniciando juego',14)
								turno = 0
								lastTurno = time()
								iniciado = True
						elif(content[0][1:] == "tipoMensaje"):
							if(len(content) == 2):
								if(content[1] == 'normal'):
									tipoMensaje = 0
								elif(content[1] == 'especial'):
									tipoMensaje = 111
						elif(content[0][1:] == "urgido" and userid == ley):
							send_message(chatid,'Agregando preguntas y retos de urgido virgo dea')
							with open('juegos/vor/retos_hard.txt', 'r') as handler:
								retos += [line.rstrip() for line in handler]


							with open('juegos/vor/preguntas_hard.txt', 'r') as handler:
								preguntas += [line.rstrip() for line in handler]
							random.shuffle(retos)
							random.shuffle(preguntas)
							r = sub_client.start_chat(users,'Verdad o reto modo virgo urgido necesitado dea bienvenidos',save=True)
							print(r[0])
							if(r[0] == 200):
								privatechat = r[1]['thread']['threadId']
								print(privatechat)
							sub_client.edit_chat(privatechat,title='verdad o reto')
							chatid = privatechat
							# sub_client.edit_chat(mafiaChat,backgroundImage=mafiaBackground)



						elif(content[0][1:] == "saltar" or content[0][1:] == "pasar"):
							turno += 1
						elif(content[0][1:] == "cancelar"):
							send_marco(chatid,"\n\nJuego terminado\n\n",14)
					
							matar()
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
							users[userid] = User(userid,getNickname(userid),0,s=s)
							send_message(chatid,getNickname(userid) + " Se ha unido al juego")
					
					if(userid not in users):
						continue

					if(content[0][1:] == "v"):
						if(not iniciado):
							send_message(chatid,'/start para iniciar el juego')
							continue
						if(len(preguntas) == 0 ):
							send_message(chatid,'Se acabaron las preguntas de verdad')
							continue
						if(libre):
							send_message(chatid,getNickname(userid) + " tienes que responder:\n\n" + preguntas.pop())
							turno += 1
							turno = turno % jugadores
						else:
							if(userid == jugadores[turno]):
								send_message(chatid,getNickname(userid) + " tienes que responder:\n\n" + preguntas.pop())
								turno += 1
							else:
								send_message(chatid,getNickname(userid) + " no es tu turno")

					elif(content[0][1:] == "r"):
						if(not iniciado):
							send_message(chatid,'/start para iniciar el juego')
							continue
						if(len(retos) == 0 ):
							send_message(chatid,'Se acabaron los retos')
							continue
						if(libre):
							send_message(chatid,getNickname(userid) + " tienes que hacer:\n\n" + retos.pop())
							turno += 1
						else:
							if(userid == jugadores[turno]):
								send_message(chatid,getNickname(userid) + " tienes que hacer:\n\n" + retos.pop())
								turno += 1
							else:
								send_message(chatid,getNickname(userid) + " no es tu turno")
					elif(content[0][1:] == "dejar" or content[0][1:] == "salir"):
						if(userid in users):
							if(len(users) == 1):
								send_message(chatid,'Abandonaron todos terminando juego')
								send_marco(chatid,"\n\nJuego terminado\n\n",14)
								matar()

							if(jugadores.index(userid) < turno):
								turno -= 1

							users.pop(userid)
							send_message(chatid,getNickname(userid) + " Ha abandonado el juego")

					elif(content[0][1:] == "jugadores"):
						text = 'Jugadores:\n'

						jugadores = list(users.keys())
						i = 1
						for u in jugadores:
							text += '%d. %s\n' % (i,getNickname(u))
							i+=1
						send_message(chatid,text)

					elif(content[0][1:] == "libre"):
						if(content[1] == 'on'):
							send_message(chatid,'modo libre')
							libre = True
						elif(content[1] == 'off'):
							send_message(chatid,'modo por turnos')
							libre = False
					jugadores = list(users.keys())
					if(turno >= len(jugadores) ):
						turno = 0
					if(iniciado and not libre ):
						print('Turno de ' + getNickname(jugadores[turno]))
						send_message(chatid,'Turno de ' + getNickname(jugadores[turno]))
		except Exception as e:
			PrintException()
			print("error: ")
			print(e)