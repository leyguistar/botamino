#!/usr/bin/env python3
import amino
import mysql.connector
import random
import sys
import os
import signal
import threading
import linecache
import traceback
import requests

from time import time
from save import Save
s = Save(file='default.set')
from user import User
from chat import Chat
from mensaje import Mensaje
from aminohelpers import login as loginfun
class Player:
	def __init__(self,userid,rol,chatid,votos=0,voto=None,visita=None):
		self.userid = userid
		self.rol = rol
		self.chatid = chatid
		self.votos = votos
		self.voto = voto
		self.listo = False
		self.visita = visita

def getNickname(userid):
	if(userid in nickname):
		return nicknames[userid]
	else:
		nick = sub_client.get_user_info(userid).nickname
		nicknames[userid] = nick
		return nick
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


def terminar():
	send_marco(chatid,"\n\nJuego %s terminado\n\n" % (sys.argv[2]),14)
	matar()

def handler(signum, frame):
	terminar()
def actualizar(signum, frame):
	send_message(chatid,'Terminando juego por actualizaciones')
	send_marco(chatid,"\n\nJuego terminado\n\n",14)
	matar()
signal.signal(signal.SIGTERM, actualizar) #handler para matar cuando nazca un nuevo bot

roles = ['mafia','civil','doctor','detective','amante']
rol = [0,1,1,2,3,4,0,2,1,0,3,0,1,4,1,1,1,1,1,1,1,1]
def darRoles():
	random.shuffle(users)


def visitas(chatid):
	for player in players.values():
		visita = player.visita
		# if(player.rol == 2):
		# 	if(visitaMafia == visita):
		# 		if(visitaMafia in visitasAmante.values()):
		# 			text = 'El doctor le hizo una visita a %s he inesperadamente en la casa de este' + 'se encontraba %s \
		# 			casi muerto despues de un intento de asesinato, rapidamente le atiende y consigue \
		# 			salvarle le vida y se va antes de que amanezca' % (getNickname(visitasAmante[visitaMafia]))
		# 		else:
		# 			text = 'El doctor le hizo una visita a %s he inesperadamente este se encontraba \
		# 			casi muerto despues de un intento de asesinato, rapidamente le atiende y consigue \
		# 			salvarle le vida y se va antes de que amanezca'
		# 		send_message(chatid,text)
		if(player.rol == 3):
			if(players[visita].rol == 0):
				text = 'Vas a la casa de %s pero no le encuentras, asi que te parece sospechoso \
				y te pones a revisar, te das cuenta de que hay una pistola y varias armas \
				ademas de mucha pasta en el lugar'
			elif(players[player.visita].rol == 1):
				text = 'Vas a investigar la casa de %s y lo encuentras tranquilo sin nada sopechoso' 
			elif(players[visita].rol == 2):
				if(players[visita].visita == visita):
					text = 'Vas a investigar la casa de %s \
					y le encuentras alli sentado con vata y estetoscopio ' 
				else:
					text = 'Vas a investigar la casa de %s \
					pero no le encuentras, revisas bien y consigues un estetoscopio una bata y unos primeros auxilios'

			elif(players[visita].rol == 3):
				text = 'Visitas la casa de %s y no le encuentras, pero encuentras una lupa una pipa y muchos libros'
			elif(players[visita].rol == 4):
				text = 'Vas a la casa de %s y no le encuentras pero encuentras muchos juguetes extraños con un olor bastante desagradable ademas de ropas extrañas y mucho dinero'
			send_message(player.chatid,text % (getNickname(player.visita)) ) 
	if(visitaMafia in visitasAmante.values()):
		for i in visitasAmante:
			if(visitasAmante[i] == visitaMafia):
				amante = i
				break

		if(visitaMafia in visitasDoctor.values()):
			text = '%s se salvo gracias al tratamiento medico' % (getNickname(amante))
			send_message(chatid,text)
		else:
			text = '%s se murio en casa de %s' % (getNickname(amante),getNickname(visitaMafia))
			send_message(chatid,text)
			send_message(players[amante].chatid,'Moriste')
			sub_client.leave_chat(players[amante].chatid)

			players.pop(amante)
	elif(visitaMafia in visitasDoctor.values()):
		text = '%s se salvo gracias al tratamiento medico' % (getNickname(visitaMafia))
		send_message(chatid,text)
	elif(players[visitaMafia].rol == 4):
		if(players[visitaMafia] == players[visitaMafia].userid):
			text = '%s fue asesinado por la mafia mientras estaba en actos manuales su rol era %s' % (getNickname(visitaMafia),roles[players[visitaMafia].rol])
		else:
			text = 'Al parecer la mafia intento matar a alguien pero esta persona no se encontraba en su casa'
	else:
		text = '%s fue asesinado por la mafia su rol era %s' % (getNickname(visitaMafia),roles[players[visitaMafia].rol])
		send_message(chatid,text)
		send_message(players[visitaMafia].chatid,'Moriste')
		sub_client.leave_chat(players[visitaMafia].chatid)
		players.pop(visitaMafia)
	for u in players:
		players[u].visita = None

def crearChats(chatid):
	global players,mafiaChat,tipoMensaje
	mafias = []
	i = 0
	while i < len(users):
		if(rol[i] == 0):
			r = sub_client.start_chat([users[i]],'Tu rol es: mafia\nMafia tiene un chat para comunicarse entre ellos, puedes decidir a quien matar por alli o por aqui\nSi mafia es solo uno no se crea otro chat')
			mafias.append(users[i])
		else:
			r = sub_client.start_chat([users[i]],'Tu rol es: %s\nPara confirmar pon /listo' % (roles[rol[i]]) )
		if(r[0] != 200):
			if(r[0] == 400 and r[1]['api:statuscode'] == 270 and 'url' in r[1]):
				tmp = tipoMensaje
				tipoMensaje = 0
				send_message(chatid,'Amino necesita comprobar que este juego es jugado por humanos para iniciar ')
				send_message(chatid,r[1]['url'])
				send_message(chatid,'Por favor alguien confirme (solo uno) y pongan /listo para iniciar el juego o /cancelar para cancelar el juego')
				verificado = False
				tipoMensaje = tmp
				while(not verificado):
					messageList = sub_client.get_chat_messages(chatId=chatid,size=3)  # Gets messages of each chat
					for content, id in zip(messageList.content, messageList.messageId):
						if(content == '/listo'):
							i-=1
							verificado = True
						elif(content == '/cancelar'):
							send_marco(chatid,"\n\nJuego terminado\n\n",14)
							matar()
			else:
				send_message(chatid,'Error al escribirle a ' + getNickname(users[i]) + ' al privado, escribele al bot al privado y pon /listo en el chat publico (osea este) para que el bot te diga tu rol en privado')
				players[users[i]] = Player(users[i],rol[i],None)
		else:
			players[users[i]] = Player(users[i],rol[i],r[1]['thread']['threadId'])
		i += 1
				
	if(len(mafias) > 1):
		r = sub_client.start_chat(mafias,'Bienvenidos al chat de la mafia',save=True)
		print(r[0])
		if(r[0] == 200):
			mafiaChat = r[1]['thread']['threadId']
			print(mafiaChat)
		sub_client.edit_chat(mafiaChat,title='Mafia')
		sub_client.edit_chat(mafiaChat,backgroundImage=mafiaBackground)

	l = list(players.items())
	random.shuffle(l)
	players = dict(l)

def confirmar(generalChatid):
	global mafiaChat,confirmados,sacados
	listos = False
	while not listos:
		listos = True
		for player in players.values():
			chatid = player.chatid
			userid = player.userid
			if(not chatid):
				listos = False
				continue
			messageList = sub_client.get_chat_messages(chatId=chatid,size=3)  # Gets messages of each chat
			for content, id in zip(messageList.content, messageList.messageId):
				if id in oldMessages: 
					continue
				oldMessages.append(id)
				print(userid, content)  # Simple output with nickname and messages
				if(content is None ):
					continue

				content = content.split(' ')
				comando = content[0][1:]
				if(comando == 'listo'):
					if(not players[userid].listo):
						players[userid].listo = True
						send_message(chatid,'Confirmado')
						send_message(generalChatid,'%s confirmo' % (getNickname(userid)))
					else:
						send_message(chatid,'Ya confirmaste anteriormente')
			if(not player.listo):
				listos = False
		if(sacados):
			for i in sacados:
				players.pop(i)
			sacados = []
	confirmados = True
	print('todos confirmados')
	empezarCiclo(generalChatid)

def empezarDia():
	for player in players.values():
		chatid = player.chatid
		sub_client.edit_chat(chatid,backgroundImage=fondoDia)
		send_message(chatid,'Ya es de dia hora de votar con /votar\nPuedes votar tanto en el chat publico como en el privado\nSi votas en el privado tu respuesta se mandara al publico tambien (no hay votos secretos)')
		text = '/votar [n] para votar\nJugadores vivos:\n'
		i = 1
		for u in players:
			text += '%d. %s\n' % (i,getNickname(u))
			i += 1
		send_message(chatid,text)

def empezarNoche():
	for player in players.values():
		chatid = player.chatid
		sub_client.edit_chat(chatid,backgroundImage=fondoNoche)
		if(player.rol == 0 and not mafiaChat):
			send_message(chatid,'Ya es de noche, mafia indique a quien van a visitar para matar')
		elif(player.rol == 1): 
			send_message(chatid,'Es de noche civiles a dormir')
			continue
		elif(player.rol == 2):
			send_message(chatid,'Ya es de noche, doctor indique la persona que desea visitar para curar.')
		elif(player.rol == 3):
			send_message(chatid,'Ya es de noche, detective indique la persona que desea visitar para investigar.')
		elif(player.rol == 4):
			send_message(chatid,'Ya es de noche, indica la persona que deseas visitar para complacer con tus servicios.')
		text = 'usar: /visitar [n] para visitar\nJugadores vivos:\n'
		i = 1
		for u in players:
			text += '%d. %s\n' % (i,getNickname(u))
			i += 1
		if(player.rol != 0 or not mafiaChat):
			send_message(chatid,text)
	if(mafiaChat):
		send_message(mafiaChat,'Es de noche mafia uno de ustedes indique a quien matar')
		send_message(mafiaChat,text)

def mostrarRoles(chatid):
	for p in players:
		send_message(chatid,'%s era %s' % (getNickname(p.userid),roles[p.rol]) )
def empezarCiclo(chatid):
	global daytime
	daytime = 1
	while 1:
		try:
			daytime = not daytime
			mafias = 0
			otros = 0
			for u in players:
				if(players[u].rol == 0):
					mafias += 1
				else:
					otros += 1
			if(mafias == 0 ):
				send_message(chatid,'No hay mas mafia ganan los civiles')
				try:
					mostrarRoles(chatid)
				except Exception as e:
					print(e)
					pass
				send_marco(chatid,"\n\nJuego terminado\n\n",14)
				matar()

			if(mafias >= otros):
				send_message(chatid,'Gana la mafia')
				try:
					mostrarRoles(chatid)
				except Exception as e:
					print(e)
					pass
				send_marco(chatid,"\n\nJuego terminado\n\n",14)
				matar()
			if(daytime):
				send_message(chatid,'Es de dia hora de votar')
				empezarDia()
				dia(chatid)
				if(pasar):
					send_message(chatid,'Se saltaron las votaciones asi que no matan a nadie')
			else:
				send_message(chatid,'Es de noche')
				empezarNoche()
				noche(chatid)
				if(narrador):
					visitas(narradorChat)
				else:
					visitas(chatid)
		except Exception as e:
			print('error')
			print(e)
			PrintException()
def noche(groupChat):
	global visitasDoctor,visitasAmante,visitaMafia,sacados
	visitasDoctor = {}
	visitasAmante = {}
	listos = False
	pasar = False
	visitaMafia = None
	while not listos and not pasar:
		listos = True
		for player in players.values():
			if(player.rol == 0 and mafiaChat):
				chatid = mafiaChat
			else:
				chatid = player.chatid
			userid = player.userid
			if(not visitaMafia):
				listos = False
			if(player.rol != 1 and player.rol != 0 and player.visita == None ):
				listos = False
			messageList = sub_client.get_chat_messages(chatId=chatid,size=3)  # Gets messages of each chat
			for content, id in zip(messageList.content, messageList.messageId):
				if id in oldMessages: 
					continue
				oldMessages.append(id)
				print(userid, content)  # Simple output with nickname and messages
				if(content is None ):
					continue
				content = content.split(' ')
				comando = content[0][1:]
				if(comando == 'visitar'):
					if(len(content) != 2 or not content[1].isdigit() or int(content[1])-1 not in range(len(players)) ):
						text = 'uso: /visitar [n]\nVisitar uno de los siguientes usuarios:\n'
						i = 1
						for u in players:
							text += '%d. %s\n' % (i,getNickname(u))
							i += 1
						send_message(chatid,text)
					else:
						listVivos = ['']
						for u in players:
							listVivos.append(u)

						i = int(content[1])
						if(player.rol == 0):
							visitaMafia = listVivos[i]
						elif(player.rol == 2):
							visitasDoctor[player.userid] = listVivos[i]
						elif(player.rol == 4):
							visitasAmante[player.userid] = listVivos[i]
						else:
							send_message(chatid,'los civiles no visitan')
						if(player.rol != 0):
							players[userid].visita = listVivos[i] #visita a i
						send_message(chatid,'Visitas a ' + getNickname(listVivos[i]))
				elif(comando == 'votar'):
					send_message(chatid,'Solo puedes votar en el dia')
		if(sacados):
			for i in sacados:
				if(i in players):
					send_message(groupChat,getNickname(i) + ' murio su rol era %s ' % (roles[players[i].rol]) )
					players.pop(i)
			sacados = []


def dia(generalChatid):
	global pasar,sacados
	listos = False
	pasar = False
	while not pasar:
		listos = True
		for player in players.values():
			if(player.voto == None):
				listos = False
			chatid = player.chatid
			userid = player.userid
			messageList = sub_client.get_chat_messages(chatId=player.chatid,size=3)  # Gets messages of each chat
			for content, id in zip(messageList.content, messageList.messageId):
				if id in oldMessages: 
					continue
				oldMessages.append(id)
				print(userid, content)  # Simple output with nickname and messages
				if(content is None ):
					continue
				content = content.split(' ')
				comando = content[0][1:]
				if(comando == 'visitar'):
					send_message(chatid,'Solo puedes visitar en la noche')
				elif(comando == 'votar'):
					if(len(content) != 2 or not content[1].isdigit() or int(content[1])-1 not in range(len(players)) ):
						text = 'uso: /votar [n]\nVotas por uno de los siguientes usuarios como miembro de la mafia:\n'
						i = 1
						listVivos = ['']
						for u in players:
							text += '%d. %s\n' % (i,getNickname(u))
							i += 1
							listVivos.append(u)
						send_message(chatid,text)
					else:
						i = int(content[1])
						listVivos = ['']
						for u in players:
							listVivos.append(u)
						player.voto = listVivos[i]
						send_message(chatid,'Votaste por ' + getNickname(listVivos[i]))
						send_message(generalChatid,'%s voto por %s' % (getNickname(player.userid),getNickname(listVivos[i])) )
		if(sacados):
			for i in sacados:
				if(i in players):
					send_message(generalChatid,getNickname(i) + ' murio su rol era %s ' % (roles[players[i].rol]) )
					players.pop(i)
			sacados = []
		if(listos):
			if(contarVotos(generalChatid)):
				return


def contarVotos(chatid):
	global empate
	votos = {voto: 0 for voto in players.keys()}
	for player in players.values():
		if(player.voto not in players):
			player.voto = None
			return
		votos[player.voto] += 1
	votos = {k: v for k, v in sorted(votos.items(), key=lambda item: item[1],reverse=True)}
	text = 'Votos:\n'
	for u in votos:
		text += '%s %d votos\n' % (getNickname(u),votos[u])
	values = list(votos.values())
	ma = max(values)
	u = max(votos,key=votos.get)
	if(values.count(ma) == 1):
		send_message(chatid,text)
		send_message(chatid,'Decidieron matar a %s' % (getNickname(u)))
		send_message(players[u].chatid,'Moriste')
		sub_client.leave_chat(players[u].chatid)
		send_message(chatid,'%s se murio y su rol era %s' % (getNickname(u),roles[players[u].rol] ))
		if(players[u].rol == 0 and mafiaChat):
			sub_client.kick(u,mafiaChat,False)
		players.pop(u)
		empate = None
		for u in players:
			players[u].voto = None
		return True
	else:
		if(empate):
			return False
		send_message(chatid,text)
		send_message(chatid,'Hay un empate, alguien cambie su voto\n')
		empate = True
		return False
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    traceback.print_exc()




signal.signal(signal.SIGALRM, handler)
chatid = sys.argv[1]
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
users = []
players = {}
chatid = sys.argv[1]
chat = s.loadChat(chatid)
chatThread = sub_client.get_chat_thread(chatid,raw=True)['thread']
host = chatThread['uid']
coHost = chatThread['extensions'].get('coHost',[])
chat.ops[host] = 3
for c in coHost:
	chat.ops[c] = 2

visitasDoctor = {}
visitasAmante = {}
sacados = []
marcos = []
with open('marcos.txt', 'r') as handler:
    buf = [line.rstrip() for line in handler]
    for i in range(0,len(buf),2):
        marcos.append((buf[i],buf[i+1]))
chatkey = sys.argv[1]
jugadores = []
daytime = 1
chatid = chat.id
mafiaChat = None
iniciado = False
confirmados = False
libre = False
pasar = False
empate = False
narrador = None
narradorChat = None
visitaMafia = None
lastTurno = time()
tPorTurno = 0
aTurno = daytime
tLimite = 600
# users = ['','9af3d46b-174f-4297-acc2-08bf3a47d34e','b8d2f2da-b099-4aa1-b649-6179f7fbbe2d','61bbcceb-2f36-46f8-a6cc-f03c7d6ede3b']
while 1:
	try:
		with open('juegos/asesino/fondos/mafia_bar.jpeg','rb') as h:
			mafiaBackground = client.upload_media(file=h,tipo='jpg')
	except:
		pass
	else:
		break
while 1:
	try:
		with open('juegos/asesino/fondos/noche_cuarto.jpg','rb') as h:
			fondoNoche = client.upload_media(file=h,tipo='jpg')
	except:
		pass
	else:
		break
while 1:
	try:
		with open('juegos/asesino/fondos/dia_cuarto.jpg','rb') as h:
			fondoDia = client.upload_media(file=h,tipo='jpg')
	except:
		pass
	else:
		break
with open('juegos/asesino/informacion.txt', 'r') as handler:
	send_marco(chatid,handler.read(),14)
with open('juegos/asesino/roles.txt', 'r') as handler:
	infoRoles = handler.read()
send_marco(chatid,infoRoles,14)
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

nicknames = {}

while True:
		
		try:
			if(aTurno != daytime):
				lastTurno = time()
				aTurno = daytime
			if(iniciado and tPorTurno != 0 and time() - lastTurno >= tPorTurno):
				send_message(chatid,'Se acabo el tiempo')
				daytime = not daytime

			if(time() - lastTurno >= tLimite):
				send_message(chatid,'terminando juego por inactividad')
				send_marco(chatid,"\n\nJuego terminado\n\n",14)
				matar()
			messageList = sub_client.get_chat_messages(chatId=chatid,size=5)  # Gets messages of each chat
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
							if(iniciado):
								for u in usersid:
									if(u in players):
										sacados.append(u)

							for u in usersid:
								if(u in users):
									users.remove(u)
									send_message(chatid,getNickname(u) + " Ha sido removido del juego")
						elif(not iniciado and content[0][1:] == "start"):
							if(iniciado):
								continue
							if(len(users) < 4):
								send_message(chatid,'Tienen que haber minimo 4 jugadores para empezar')
							else:
								send_marco(chatid,'Iniciando juego',14)
								daytime = 0
								lastTurno = time()
								iniciado = True
								darRoles()
								crearChats(chatid)
								send_message(chatid,'revisen sus privados')
								threadConfirmar = threading.Thread(target=confirmar, args=(chatid,))
								threadConfirmar.daemon = True
								threadConfirmar.start()

						elif(content[0][1:] == "tipoMensaje"):
							if(len(content) == 2):
								if(content[1] == 'normal'):
									tipoMensaje = 0
								elif(content[1] == 'especial'):
									tipoMensaje = 111

						elif(content[0][1:] == "saltar" or content[0][1:] == "pasar"):
							if(not confirmados):
								send_message(chatid,'Primero tienen que confirmar sus roles')
								continue
							pasar = True
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
						if(iniciado):
							send_message(chatid,'Una vez iniciado no se puede unir nadie por favor espera a la siguiente')
							continue
						if(userid not in users):
							users.append(userid)
							send_message(chatid,getNickname(userid) + " Se ha unido al juego")
					elif(content[0][1:] == "narrar"):
						if(userid in users):
							send_message(chatid,'El narrador no puede estar jugando, si quieres narrar salte')
						else:
							narrador = userid
							r = sub_client.start_chat([narrador],'Hola narrador de mafia aqui te llegaran los mensajes')
							if(r[0] != 200):
								send_message(chatid,'Error al escribirte al privado, al narrador, por favor escribele tu al bot en privado')
								narrador = None
							else:
								narradorChat = r[1]['thread']['threadId']
					elif(content[0][1:] == "roles"):
						send_marco(chatid,infoRoles,14)

					if(userid not in users):
						continue

					if(content[0][1:] == "votar"):
						if(not iniciado):
							send_message(chatid,'/start para iniciar el juego')
							continue
						if(not daytime):
							send_message(chatid,'Solo puedes votar de dia')
							continue
						player = players[userid]
						if(len(content) != 2 or not content[1].isdigit() or int(content[1])-1 not in range(len(players)) ):
							text = 'uso: /votar [n]\nVotas por uno de los siguientes usuarios como miembro de la mafia:\n'
							i = 1
							listVivos = ['']
							for u in players:
								text += '%d. %s\n' % (i,getNickname(u))
								i += 1
								listVivos.append(u)
							send_message(chatid,text)
						else:
							i = int(content[1])
							listVivos = ['']
							for u in players:
								listVivos.append(u)
							player.voto = listVivos[i]
							send_message(chatid,'%s voto por %s' % (getNickname(player.userid),getNickname(listVivos[i])) )


					elif(content[0][1:] == "listo"):
						if(players[userid].rol == 0):
							r = sub_client.start_chat([userid],'Tu rol es: mafia\nMafia tiene un chat para comunicarse entre ellos, si quieres entrar pon /entrar, pero tienes que seguir a leybot para que te pueda invitar. Si no quieres comunicarte con toda mafia por un chat grupal puedes poner solamente /listo' )
						else:
							r = sub_client.start_chat([userid],'Tu rol es: %s\nPara confirmar pon /listo' % (players[userid].rol) )
						if(r[0] != 200):
							send_message(chatid,'Error al escribirte al privado, escribele al bot al privado y pon /listo en el chat publico (osea este) para que el bot te diga tu rol en privado')
						else:
							players[userid].chatid = r[1]['thread']['threadId']

					elif(content[0][1:] == "dejar" or content[0][1:] == "salir"):
						if(iniciado):
							if(userid in players):
								sacados.append(userid)
						if(userid in users):

							users.remove(userid)
							send_message(chatid,getNickname(userid) + " Ha abandonado el juego")

					elif(content[0][1:] == "jugadores"):
						text = 'Jugadores:\n'
						i = 1
						# if(iniciado):
						# 	for p in players:
						# 		text += '%d. %s\n' % (i,getNickname(p))
						# 		i+=1
						# 	send_message(chatid,text)

						# else:
						for u in users:
							text += '%d. %s\n' % (i,getNickname(u))
							i+=1
						send_message(chatid,text)
		except Exception as e:
			print("error: ")
			print(e)
			PrintException()