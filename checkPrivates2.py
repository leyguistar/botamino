#!/usr/bin/env python3
import amino
import os
import sys
from collections import deque
import itertools
import mysql.connector
import signal
import threading
import requests
from pprint import pprint
import datetime
from save import Save
from time import time
from time import sleep
import random
import unicodedata
import threading
import signal
import linecache
import traceback
import secrets
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
def get_host(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['author']['uid']

def send_reply(chatId,message,replyid):
	sub_client.send_message(message=message, chatId=chatId,replyTo=replyid)

def send_message(chatId,message):
	sub_client.send_message(message=message, chatId=chatId,messageType=0)

def send_media(chatid,file):
	sub_client.send_message(chatId=chatid,filePath=file)


def get_title(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['title']
def get_memberCount(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['membersCount']

def mostrarAyuda(chatid,tipo='general'):
	mensaje = ''
	tipos = [i.replace('.txt','') for i in os.listdir('ayuda/')]
	if(tipo not in tipos):
		send_message(chatid,'no hay ayuda para ' + tipo)
		return
	with open('ayuda/' + tipo + '.txt', 'r') as handler:
		mensaje = handler.read()

	send_message(message=mensaje, chatId=chatid)

def info(chatid,topic='bot'):
	mensaje = ''
	topics = [i.replace('.txt','') for i in os.listdir('info/')]
	if(topic not in topics):
		send_message(chatid,'no hay informacion respecto a ' + topic)
		return
	with open('info/' + topic + '.txt', 'r') as handler:
		mensaje = handler.read()

	send_message(message=mensaje, chatId=chatid)

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


print('conecting with the database')
sqlCredentials = 'default.set'
s = Save(file=sqlCredentials)
ley = 'your_uuid'
leybot = '4882156e-efce-4a4b-88ca-02baff4d5e89'
leychat = 'cc6857e6-be23-07bd-3198-c6d5d0740f70'
botgroup = '17ab60ec-0418-4c75-8ce3-fdb11613b201'
pruebas = '3ac22d37-fd90-4d95-b53f-76068b0b5244'

users = s.loadAllUsers()
print('starting login')
comid = '67'
login = s.loginInfo(alias='bot')
userBot = 'bot'
modo = 0
for i in sys.argv:
	if('comid=' in i):
		comid = i[6:]
	if('user=' in i):
		login = s.loginInfo(alias=i[5:])
		userBot = i[5:]
	elif('modo=' in i):
		modo = int(i[5:])

client = amino.Client()
if(login[2] and login[3] + 3600 > time()):
	client.login_cache(login[2] )
else:
	r = client.login(email=login[0],password=login[1],get=True)
	if(r[0] != 200):
		print('F')
		exit()
	s.newLogin(id=client.profile.id,jsonResponse=r[1])
sub_client = amino.SubClient(comId=comid,profile=client.profile)
print('logeado')

print('chats cargados')

def reiniciar(signum, frame):
	sub_client.activity_status(2)
	client.logout()
	os.execl(sys.executable, sys.executable, *sys.argv)
	exit(0)

def actualizar(signum, frame):
	sub_client.activity_status(2)
	try:
		client.logout()
		os.remove('checkPrivate.pid')
		exit(0)
	except:
		os.kill(os.getpid(), 9)


signal.signal(signal.SIGQUIT, reiniciar) #handler para matar cuando nazca un nuevo bot
signal.signal(signal.SIGTERM, actualizar) #handler para matar cuando nazca un nuevo bot

oldMessages = s.loadPrivateChatMessagesID()
			
def checkPrivate(chatid,message):
			content = message['content']
			userid = message['uid']
			nickname = message['nickname']
			id = message['messageId']
			s.PrivateChatMessageID(id)
			content = content.split(' ')
			comando = content[0][1:]
			m = None
			if(len(content) > 1):
				m = ' '.join(content[1:])
			if(comando == 'tp'):
				if(len(content) < 2):
					send_message(chatid,'Uso: /tp [link del chat]')
				else:
					r = client.get_from_code(content[1])
					if(r.objectType == 12):
						com = str(r.json['extensions']['linkInfo']['ndcId'])
						# if(com != sub_client.comId and userid != ley):
						# 	send_message(chatid,'El chat es de otra comunidad, preguntar a ley si se puede llevar el bot a esa comunidad')
						# elif(userid != ley and get_memberCount(r.objectId) <= 20):
						# 	send_message(chatid,'El chat tiene que tener minimo 20 usuarios')
						if(userid == ley or userid ==  get_host(r.objectId)):
							client.join_community(com)
							sub_client.comId = com
							sub_client.join_chat(r.objectId)
							send_message(botgroup,'tp de ' + nickname + '\nA: ' + str(get_title(r.objectId)) )
							sub_client.comId = comid
							send_message(chatid,'El bot fue enviado a el chat, si vez que entro un usuario llamado leybot escribe /activar en el chat para activarlo')
						else:
							send_message(chatid,'Tienes que ser anfi de ese chat para meter al bot en el chat destino')
			elif(comando == 'start'):
				sub_client.join_chat(chatid)
				with open('privado/start.txt','r') as h:
					sm = h.read()
				send_message(chatid,sm)
				link = None
				with open('fondos/1a98a0e6895bd01ab485d24da248d6091cab8787r3-1200-1600_00.gif','rb') as h:
					link = client.upload_media(file=h,tipo='image/gif')
				
				sub_client.edit_chat(chatId=chatid,backgroundImage=link)
			elif(comando == 'Ayuda'):
				if(len(content) >= 2 ):
					mostrarAyuda(chatid,content[1])
				else:
					mostrarAyuda(chatid)
			elif(comando == 'Info'):
				if(len(content) >= 2 ):
					info(chatid,content[1])
				else:
					info(chatid)
			elif(comando == 'salir'):
				sub_client.leave_chat(chatid)
			elif(comando == 'liberar'):
				if(len(content) < 2 ):
					send_message(chatid,'uso: /liberar [link del chat]: quita el modo visualizacion de un chat donde eres por lo menos op 2')
				else:
					r = client.get_from_code(content[1])
					if(r.objectType == 12):
						chat = s.loadChat(r.objectId)
						if(userid in chat.ops and chat.ops[userid] >= 2):
							sub_client.edit_chat(chat.id,viewOnly=False)
						else:
							send_message(chatid,'no tienes permisos en este chat')
			elif(comando == 'tag'):
				tags = s.loadUserTags(userid)
				if(m == None or m.find('!') == -1):
					if tags != None:
						print(tags)
						text = 'Tus etiquetas:' + '\n'
						for t in tags:
							if(tags[t] != None):
								text += t + ':' + tags[t] + '\n'
							else:
								text += t + '\n'
						send_message(chatid,text)
					else:
						send_message(chatid,'no tienes etiquetas')
					send_message(chatid,'Para agregar una tag /tag !tag:descripcion\nEjemplo /tag !personalidad:muy fria')
				else:
					if(m.find(':')  != -1):
						text = m[m.find(':')+1:]
						tag = m[m.find('!')+1:m.find(':')]
					else:
						text = None
						tag = m[m.find('!')+1:]
					if(tags == None):
						tags = {}
					print('insertando')
					print(tag,text)
					tags[tag] = text
					s.UserTag(userid,tags)
					send_message(chatid,'agregado etiqueta ' + tag)
			elif(comando == 'rtag'):
				tags = s.loadUserTags(userid)
				if(m != None and m in tags):
					tags.pop(m)
					s.UserTag(userid,tags)
					send_message(chatid,'removida ' + m)

			elif(comando == 'startbot'):
				send_message(chatid,'Uy, parece que usaste un comando de una version vieja de leybot ¿Probaste /activar en el chat publico?')
				send_message(chatid,'O si no ¿probaste enviando al chat con /tp?\nSi fue baneado puedes escribir /sigueme para que te siga y puedas invitarlo de nuevo')
			elif(comando == 'sigueme'):
				sub_client.follow(userid)
				send_reply(chatid,'Vale te sigo ^^',id)
			elif(comando == 'web'):
				token = secrets.token_urlsafe(128)
				s.createWebLogin(userid,token)
				send_message(chatid,'Ve a el siguiente link para logearte en la pagina de leybot')
				send_message(chatid,'https://leybot.leyguistar.com/login/%s?token=%s' % (userid,token))
			elif(comando == 'app'):
				token = secrets.token_urlsafe(128)
				s.createWebLogin(userid,token)
				send_message(chatid,'Introduce el siguiente codigo en la app para logearte')
				send_message(chatid,'%s' % (token))
			elif(comando in comandos):
				with open('privado/%s.txt' % (comando),'r') as h:
					sm = h.read()
				send_message(chatid,sm)

comandos = [i.replace('.txt','') for i in os.listdir('privado')]
tiposDeNoticia = s.loadTiposDeNoticia()

		sub_client.activity_status(1)
		for chatid,i in zip(readChats.chatId,range(len(readChats.chatId))):
			if(readChats.json[i]['type'] == 0 ):
				try:
					checkChat(chatid,True)
				except Exception as e:
					print("error checkeando chat")
					print(e)
					PrintException()
	except:
		os.system('./checkPrivates.py comid=%s &' % (comid) )
		os.kill(os.getpid(), signal.SIGKILL)	

while 1:
	try:
		readChats = sub_client.get_chat_threads(start=0, size=50) 
		print('agarrando chats')
		sub_client.activity_status(1)
		for chatid,i in zip(readChats.chatId,range(len(readChats.chatId))):
			if(readChats.json[i]['type'] == 0 ):
				try:
					checkChat(chatid)
				except Exception as e:
					PrintException()
					print("error checkeando chat")
					print(e)
	except:
		PrintException()
		os.execl(sys.executable, sys.executable, *sys.argv)

	# threadCheck = threading.Thread(target=checkChat, args=(chatid,))
	# threadCheck.daemon = True
	# threadCheck.start()
	# sleep(0.1)

client.logout()
