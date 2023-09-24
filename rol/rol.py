#!/usr/bin/env python3
import amino
import mysql.connector
import random
import sys
import signal
import os
from collections import deque
import operator
import datetime
from unicodedata import normalize
import re

from save import Save

s = Save()
from user import User
from chat import Chat
from mensaje import Mensaje

def getNickname(userid):
	if(userid == None):
		return ''
	if(userid in usersObjects):
		if(usersObjects[userid].alias != ""):
			return usersObjects[userid].alias
	return sub_client.get_user_info(userid).nickname

def send_message(chatid,mensaje):
	sub_client.send_message(message=mensaje, chatId=chatid,messageType=tipoMensaje)

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
	for u in users:
		m += getNickname(u) + ': ' + str(users[u]) + '\n\n'
	if(m != ''):
		send_message(chatid,m)
def mostrarPosiciones(chatid,users,mn):
	m = 'Los ganadores son:\n\n'
	for u , p , i in users , range(1,4):
		m += str(i) + '. ' + getNickname(u) + ' ' + str(p) + 'pts.'   
	send_marco(chatid,m,mn)

def matar(i = 0):
	client.logout()
	exit(0)
	os.kill(os.getpid(), signal.SIGKILL)	

def terminar():
	send_marco(chatid,"\n\nJuego terminado\n\n",14)
	#
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

def enviarPregunta(turno):
	if(preguntas != None):
		send_message(chatid,preguntas[turno])
	send_imagen(chatid,file='juegos/'+ juego +'/imagenes/%d.jpg' % (turno))
juego = sys.argv[2]

f = os.open('juegos/fifo',os.O_RDWR)
os.write(f,str(os.getpid()).encode('utf-8'))
try:
	with open('juegos/' + juego + '/preguntas.txt', 'r') as handler:
		preguntas = [line.rstrip().lower() for line in handler]
except IOError:
    preguntas = None
with open('juegos/' + juego + '/respuestas.txt', 'r') as handler:
	respuestas = [line.rstrip().lower() for line in handler]

with open('juegos/' + juego + '/links.txt', 'r') as handler:
	links = [line.rstrip() for line in handler]
tipoMensaje = 100
orden = list(range(len(respuestas)))
random.shuffle(orden)
login = s.loginInfo(alias='bot')
client = amino.Client()
client.login(email=login[0],password=login[1])
sub_client = amino.SubClient(comId='67',profile=client.profile)
oldMessages = []

usersObjects = s.loadAllUsers()
users = {}
marcos = s.cargarMarcos()
chatid = sys.argv[1]
chat = s.loadChat(chatid)

oldMessages = oldMessages + s.loadMessagesID(chat.id)
turno = 0
iniciado = False
libre = False
puntos = 0
wusers = {}
with open('juegos/' + juego + '/informacion.txt', 'r') as handler:
	send_marco(chatid,handler.read(),14)


while True:
		try:
			messageList = sub_client.get_chat_messages(chatId=chatid,size=20)  # Gets messages of each chat
			chatInfo = sub_client.get_chat_thread(chatId=chatid)  # Gets information of each chat
			
			for nickname, content, id, userid, extensions , tipo , mediaValue, createdTime in zip(messageList.author.nickname, messageList.content, messageList.messageId, messageList.author.id, messageList.extensions,messageList.type, messageList.mediaValue,messageList.createdTime):
				if id in oldMessages: 
					continue
				oldMessages.append(id)
				print(nickname, content)  # Simple output with nickname and messages

				if(content is None or tipo == 100):
					continue
				usersid = getMentions(extensions)
				replyid = getMessageReply(extensions)
				s = re.sub(
			        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
			        normalize( "NFD", content), 0, re.I
			    	)
				content = normalize( 'NFC', s)
				content = normalize('NFKC',content)
				rs = respuestas[turno].split('|')
				if(userid in users and iniciado):
					if(content.lower() in rs):
						wusers[userid] = datetime.datetime.strptime(createdTime, '%Y-%m-%dT%H:%M:%SZ')
				m = content[content.find(" "):]
				content = str(content).split(" ")
				if content[0][0] == "/":  
					comando = content[0][1:]
					if(userid in chat.ops ):
						if(content[0][1:] == "sacar"):
							for u in usersid:
								if(u in users):
									users.pop(u)
									send_message(chatid,getNickname(u) + " Ha sido removido del juego")
						elif(content[0][1:] == "start"):
							send_marco(chatid,'Iniciando juego',14)
							turno = orden.pop()
							iniciado = True
							enviarPregunta(turno)
						elif(content[0][1:] == "cancelar"):
							mostrarPuntuaciones(chatid,users)
							send_marco(chatid,"\n\nJuego terminado\n\n",14)
							matar(0)
						elif(content[0][1:] == "puntos"):
							mostrarPuntuaciones(chatid,users)
						elif(content[0][1:] == "tipoMensaje"):
							if(len(content) == 2):
								if(content[1] == 'normal'):
									tipoMensaje = 0
								elif(content[1] == 'especial'):
									tipoMensaje = 100

						elif(content[0][1:] == "pasar"):
							send_message(chatid,'Respuesta: ' + respuestas[turno])
							if(len(orden) == 0):
								mostrarPuntuaciones(chatid,users)
								send_marco(chatid,'juego terminado',14)
								matar(0)
							else:
								turno = orden.pop() 
								enviarPregunta(turno)


					if(content[0][1:] == "entrar"):  
						if(userid not in users):
							users[userid] = 0
							send_message(chatid,getNickname(userid) + " Se ha unido al juego")
					elif(content[0][1:] == "ficha"):  
						pass
					elif(content[0][1:] == "crear"): 
						if(content[1] == 'objeto'):

						elif(content[1] == 'lugar'):

					elif(content[0][1:] == "dar"):
					elif(content[0][1:] == "usar"):

					elif(content[0][1:] == "dejar"):
						if(userid in users):
							users.pop(userid)
							send_message(chatid,getNickname(userid) + " Ha abandonado el juego")

			if(len(wusers) > 0 ):
				uw = min(wusers.items(), key=operator.itemgetter(1))[0]
				send_message(chatid,getNickname(uw) + " gana 1 punto\n\n" + respuestas[turno] )
				users[uw] += 1
				wusers = {}
				if(len(orden) == 0):
					mostrarPuntuaciones(chatid,users)
					send_marco(chatid,'juego terminado',14)
					matar(0)
				else:
					turno = orden.pop() 
					enviarPregunta(turno)
		except Exception as e:
			print("error ")
			print(e)
