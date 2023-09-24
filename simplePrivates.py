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
import lite_private
from exception import PrintException
import ujson as json
import socket
import ssl
from amino.lib.util import headers as aminoHeaders
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
client  = amino.Client()
try:
	r = requests.get('http://169.254.169.254/latest/meta-data/instance-id',timeout=1)
except:
	instanceid = 'i-local'
else:
	instanceid = r.text


latestActivityTime = {}
s = Save(file='default.set')
oldMessages = s.loadPrivateChatMessagesID()
login = s.loginInfo(alias='bot')



if(login[2] and login[3] + 3600 > time()):
	print('inicio cache')
	client.login_cache(login[2] )
else:
	print('iniciando normal')
	r = client.login(email=login[0],password=login[1],get=True)
	if(r[0] != 200):
		print('F')
		exit()
	r1 = json.loads(r[1])
	r1['userProfile']['content'] = 'cache'
	r1 = json.dumps(r1)
	s.newLogin(id=client.profile.id,jsonResponse=r1)


def reLogin():
	login = s.loginInfo(alias='bot')
	print('iniciando normal')
	r = client.login(email=login[0],password=login[1],get=True)
	if(r[0] != 200):
		print('F')
		exit()
	r1 = json.loads(r[1])
	r1['userProfile']['content'] = 'cache'
	r1 = json.dumps(r1)
	s.newLogin(id=client.profile.id,jsonResponse=r1)

def connectServer():
    global requestReset
    global sock,ssock
    while True:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            hostname = 'leybot.leyguistar.com'
            context = ssl.create_default_context()

            sock = socket.create_connection((hostname,8443))
            ssock = context.wrap_socket(sock,server_hostname=hostname)  
            ssock.send(('{"instanceid":"%s","type":5,"chatid":"privates","pid":%d,"processid":%d}' % (instanceid,os.getpid(),processid)).encode('utf-8'))
            
            print('conectado con el servidor')
            while 1:
                text = ssock.recv()
                print('recibido',text)
                if(text == ""):
                    ssock.send('KA'.encode('utf-8'))
                    continue

                message = json.loads(text.decode('utf-8'))
                comando = message['comando']
                print('comando resivido',comando)
        except Exception as e:
            # PrintException()
            print('error conectando con el servidor, reintentando')
            sleep(60)




ley = 'your_uuid'
leybot = '4882156e-efce-4a4b-88ca-02baff4d5e89'
leychat = 'cc6857e6-be23-07bd-3198-c6d5d0740f70'
botgroup = '17ab60ec-0418-4c75-8ce3-fdb11613b201'
pruebas = '3ac22d37-fd90-4d95-b53f-76068b0b5244'
if('debug' in sys.argv):
	debug = True
else:
	debug = False
sub_client = None
def get_host(chatid,comid=None):
	c = sub_client.comId
	if(comid):
		sub_client.comId = comid
	thread = sub_client.get_chat_thread(chatid)
	sub_client.comId = c
	return thread.json['uid']

def send_reply(chatId,message,replyid,comid=None):
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


def sendStart(chatid,comid,premium,userBot='4882156e-efce-4a4b-88ca-02baff4d5e89'):
    comando = {"comando":"start","premium":1,"comid":comid,"userBot":userBot,"chatid":chatid}
    try:
        print('enviando ',comando)
        ssock.send(json.dumps(comando).encode('utf-8'))
    except Exception as e:
        print('error enviando un mensaje al servidor ',e)



def checkStartBot(userChat,chatid,uid,cid,replyid,n=0):
	bots = s.loadBots(owner=uid)
	if(n > 0):
		if(n <= len(bots)):
			i = bots[n-1]
			sendStart(chatid,cid,1,i[0])
			userStartBotRequests.pop(uid)
			return 1
		else:
			send_message(userChat,'opcion invalida, cancelando')
			userStartBotRequests.pop(uid)
			return 0		
	print('startbot en',uid)
	userStartBotRequests[uid] = (chatid,cid)
	names = [i[1] for i in bots]
	print(names)
	count = len(names)
	if(count > 1):
	    text = 'Hay varios bots selecciona uno:\n'
	    for i,n in enumerate(names):
	        text += '%d. %s\n'  % (i+1,n)
	    send_reply(userChat,text,replyid,comid=cid)
	    return 2
	elif(count == 1):
	    sendStart(chatid,cid,1,bots[0][0])
	    return 1
	elif(not count):
	    return 0



def checkPrivate(chatid,message,client,comid):
	global sub_client
	try:
		content = message['content']
		userid = message['uid']
		nickname = message['author']['nickname']
		print(nickname,content)
		if(debug and userid != ley):
			return
		id = message['messageId']
		if(userid in userStartBotRequests):
			if(content.isdigit()):
				i = int(content)
				checkStartBot(chatid,userStartBotRequests[userid][0],userid,userStartBotRequests[userid][1],id,i)
			else:
				send_message(chatid,'no elegiste ningun bot, cancelando')
				userStartBotRequests.pop(userid)

		sub_client = amino.SubClient(comId=comid, profile=client.profile)
		# s.PrivateChatMessageID(id)
		content = content.split(' ')
		comando = content[0][1:]
		m = None
		if(len(content) > 1):
		    m = ' '.join(content[1:])
		if(comando == 'tp'):
			if(len(content) < 2):
			    send_message(chatid,'Uso: /tp [link del chat]')
			else:
				response = requests.get(f"{client.api}/g/s/link-resolution?q={content[1]}", headers=aminoHeaders.Headers().headers)
				# r = client.get_from_code(content[1])
				js = json.loads(response.text)
				print(js)
				if(js['api:statuscode'] == 107):
					send_message(chatid,'link invalido')
					return
				r = js['linkInfoV2']['extensions']['linkInfo']
				print(r)
				objectId = r['objectId']
				if(r['objectType'] == 12):
					com = r['ndcId']
					# if(com != sub_client.comId and userid != ley):
					#   send_message(chatid,'El chat es de otra comunidad, preguntar a ley si se puede llevar el bot a esa comunidad')
					# elif(userid != ley and get_memberCount(r.objectId) <= 20):
					#   send_message(chatid,'El chat tiene que tener minimo 20 usuarios')
					sub_client.comId = com    
					rcom = client.join_community(com)
					print(rcom)
					chatThread = sub_client.get_chat_thread(r['objectId'],raw=True)['thread']
					if(userid == ley or userid ==  chatThread['uid']):

						rcode = client.join_community(com)
						print(rcode)
						sub_client.comId = com
						sub_client.join_chat(r['objectId'])
						send_message(botgroup,'tp de ' + nickname + '\nA: ' + str(chatThread.get('title','None') ) )
						sub_client.comId = comid
						s.chat(chatThread['threadId'],str(chatThread['title']),chatThread['threadId'],0,0,0,'',[],uid=chatThread['uid'],comid=com )
						send_message(chatid,'El bot fue enviado a el chat')
					else:
						send_message(chatid,'Tienes que ser anfi de ese chat para meter al bot en el chat destino')
					sub_client.comId = comid
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
				if(len(content) < 2):
					send_message(chatid,'Uso: /startbot [link del chat]')
				else:
					r = client.get_from_code(content[1])
					com = str(r.json['extensions']['linkInfo']['ndcId'])
					
					destChatid = r.objectId
					try:
						chatops = s.loadOPS(destChatid)
					except:
						send_reply(chatid,'[ci]chat no registrado, para integrar el bot a un nuevo chat usar /tp',id)
						return
					if((userid not in chatops or chatops[userid] < 3) and userid != get_host(destChatid,com) and userid != ley):
						send_message(chatid,'Solo op 3 o el anfi del chat puede prender el bot')
					else:
						checkStartBot(chatid,destChatid,userid,r.json['extensions']['linkInfo']['ndcId'],id)
						# startbotLock.release()

				# send_message(chatid,'Comando no disponible')
		    # send_message(chatid,'Uy, parece que usaste un comando de una version vieja de leybot ¿Probaste /activar en el chat publico?')
		    # send_message(chatid,'O si no ¿probaste enviando al chat con /tp?\nSi fue baneado puedes escribir /sigueme para que te siga y puedas invitarlo de nuevo')
		elif(comando == 'sigueme'):
		    sub_client.follow(userid)
		    send_reply(chatid,'Vale te sigo ^^',id)
		elif(comando == 'web'):
			send_message(chatid,'Actualmente no disponible')
			return
			token = secrets.token_urlsafe(128)
			s.createWebLogin(userid,token)
			send_message(chatid,'Ve a el siguiente link para logearte en la pagina de leybot')
			send_message(chatid,'https://leybot.leyguistar.com/login/%s?token=%s' % (userid,token))
		elif(comando == 'app'):
			if(len(content) < 2):
				send_message(chatid,'Para descargar la app\n/app link\nPara un codigo de acceso\n/app code')
			elif(content[1] == 'link'):
				send_message(chatid,'link de la app: leyguistar.com/leybot')
			elif(content[1] == 'code'):
				while 1:
					try:
						code = secrets.token_hex(3)
						print('creando codigo',code)
						s.createAppCode(userid,int(code,16))
						break
					except Exception as e:
						print(e)
						print('creando otro token')
				send_message(chatid,'Introduce el siguiente codigo en la app para logearte')
				send_message(chatid,'%s' % (code))
				send_message(chatid,'Codigo valido durante una hora, o hasta que solicites otro')
		elif(comando in comandos):
		    with open('privado/%s.txt' % (comando),'r') as h:
		        sm = h.read()
		    send_message(chatid,sm)
	except Exception as e:
	    PrintException()

comandos = [i.replace('.txt','') for i in os.listdir('privado')]

tChat = threading.Thread(target=connectServer, args=())
tChat.daemon = True
tChat.start()

userStartBotRequests = {}

processid = s.process(4,__file__,'*',0,os.getpid(),instanceid)

sub_client = amino.SubClient(67,client.profile)
print('entrando en while')
while 1:
	try:
		chats = sub_client.get_chat_threads(start=0, size=100,raw=True).get('threadList',None)
		if(chats == None):
			reLogin() 
		print('agarrando chats')
		sub_client.activity_status(1)
		for chat in chats:
			chatid = chat['threadId']
			if(chat['type'] == 0 ):
				lastest = datetime.datetime.strptime(chat['latestActivityTime'],'%Y-%m-%dT%H:%M:%SZ')
				if(chatid in latestActivityTime):
					if(latestActivityTime[chatid] == lastest):
						continue
				print('revisando',chatid)
				latestActivityTime[chatid] = lastest
				messageList = sub_client.get_chat_messages(chatId=chatid,size=20,raw=True)['messageList']  # Gets messages of each chat
				for message in messageList:
					id = message['messageId']
					if(id in oldMessages):
						continue
					oldMessages.append(id)
					s.PrivateChatMessageID(id)
					try:
						checkPrivate(chatid,message,client,67)
					except Exception as e:
						PrintException()
						print("error checkeando chat")
						print(e)
	except:
		PrintException()

	# threadCheck = threading.Thread(target=checkChat, args=(chatid,))
	# threadCheck.daemon = True
	# threadCheck.start()
	# sleep(0.1)

client.logout()
