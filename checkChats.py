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
from operator import itemgetter
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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

def get_host(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['author']['uid']

def send_reply(chatId,message,replyid):
	sub_client.send_message(message=message, chatId=chatId,replyTo=replyid)


print('conecting with the database')
sqlCredentials = 'default.set'
s = Save(file=sqlCredentials)
ley = ''
leybot = '4882156e-efce-4a4b-88ca-02baff4d5e89'
pruebas = '3ac22d37-fd90-4d95-b53f-76068b0b5244'
leychat = 'cc6857e6-be23-07bd-3198-c6d5d0740f70'
botgroup = '17ab60ec-0418-4c75-8ce3-fdb11613b201'

users = s.loadAllUsers()
print('starting login')
comid = '67'
login = s.loginInfo(alias='bot')
userBot = 'bot'
modo = 0 # 0 normal, 1 premium, 2 mantenimiento, 3 mantenimiento excepto premium
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
print(sub_client.profile.id)

print('chats cargados')

def reiniciar(signum, frame):
	sub_client.activity_status(2)
	client.logout()
	os.system('./checkChats.py comid=%d &' % (comid) )

	exit(0)

def actualizar(signum, frame):
	sub_client.activity_status(2)
	try:
		client.logout()
		os.remove('check%s.pid' % comid)
		exit(0)
	except:
		os.kill(os.getpid(), signal.SIGKILL)

signal.signal(signal.SIGQUIT, reiniciar) #handler para matar cuando nazca un nuevo bot
signal.signal(signal.SIGTERM, actualizar) #handler para matar cuando nazca un nuevo bot

oldMessages = s.loadStartbotTimes()
premiumChats = []
premiumUser = {}

def checkMessages(chatid,chatInfo,messageList):
	iniciado = False
	for nickname, content, id, userid, createdTime in zip(messageList.author.nickname, 
	messageList.content, messageList.messageId,messageList.author.id,messageList.createdTime):
		if id in oldMessages: 
			continue
		oldMessages.append(id)  # Adds message id to a list so it doesn't repeat commands
		if(content == None or iniciado):
			continue
		if(content == '/startbot'):
			iniciado = True
			if(chatid == pruebas):
				print('premium startbot in ' + str(chatInfo.title) + ' by ' + nickname)
				os.system("./bot.py id %s log comid=%s premium=%d user=%s &" % (chatid,comid,users[userid].premium,userBot) )
				continue					
			chatops = s.loadOPS(chatid)
			startbots = s.loadStartbotTimes(chatid)
			# lastStart = max(startbots,key=itemgetter(0))
			if(len(startbots) == 0):
				lastStart = 0
			else:
				lastStart = max(startbots)
			if(userid not in chatops or chatops[userid] < 3 and userid != get_host(chatid)):
				continue
			# if(True):
			# 	print('premium startbot in ' + str(chatInfo.title) + ' by ' + nickname)
			# 	os.system("./bot.py id %s bot log comid=%s premium=1 &" % (chatid,comid) )
			# 	continue					
				# startbotLock.release()
			if(modo == 2):
				send_reply(chatid,'[ci]Bot en mentenimiento',id)
				continue
			os.system("ps -fC python3 | grep bot | wc -l > botcount.txt")
			botcount = 0
			with open('botcount.txt','r') as h:
				botcount = int(h.read())
			print(' hay prendidos ' + str(botcount))
			
			pchat = s.checkChatPremium(chatid)
			if((userid in users and users[userid].premium > 0) or pchat):
				if(not pchat):
					s.chatPremium(userid,datetime.datetime.utcnow(),users[userid].premium,chatid)
				print('premium startbot in ' + str(chatInfo.title) + ' by ' + nickname)
				s.chatStartbot(id,createdTime.replace('T',' ').replace('Z',''),userid,time(),users[userid].premium,chatid)
				send_reply(chatid,'inicio premium espere por favor',id)
				os.system("./bot.py id %s bot log comid=%s premium=%d user=%s &" % (chatid,comid,users[userid].premium,userBot) )
			else:
				if(modo == 3):
					send_reply(chatid,'[ci]Bot en mantenimiento, para usar la version lite use /activar',id)
					continue

				# send_reply(chatid,'leybot gratis no estara disponible hasta nuevo aviso',id)
				# return
				t = int(3600*3 - (time() - lastStart) )
				if(time() - lastStart < 3600*3 and False):
					s.chatStartbot(id,createdTime.replace('T',' ').replace('Z',''),userid,time(),-1,chatid)
					print(chatid,'[ci]Faltan %d:%d minutos para poder usar startbot de nuevo' % (t/60,t%60),id)
					send_reply(chatid,'[ci]Faltan %d:%d minutos para poder usar startbot de nuevo' % (t/60,t%60),id)
				elif(botcount >= 10):
					if(modo == 0):
						send_reply(chatid,'[ci]Demasiados chats usando el bot, por favor espere a que alguno se apague o use la version premium',id)
					elif(modo == 1):
						send_reply(chatid,'[ci]Leybot gratis no esta disponible por el momento',id)
				else:
					print('free startbot in ' + str(chatInfo.title) + ' by ' + nickname)
					try:
						s.chatStartbot(id,createdTime.replace('T',' ').replace('Z',''),userid,time(),0,chatid)
					except Exception as e:
						print('error')
						print(e)

						PrintException()
						pass
					os.system("./bot.py id %s bot log comid=%s user=%s &" % (chatid,comid,userBot) )
					send_reply(chatid,'Inicio valido por favor espere mientras inicia el bot',id)
				
			# startbotLock.release()

def checkChat(chatid):
		chatInfo = sub_client.get_chat_thread(chatId=chatid)  # Gets information of each chat
		print('checkeando ' + str(chatInfo.title) )
		messageList = sub_client.get_chat_messages(chatId=chatid,size=40)  # Gets messages of each chat
		startbotLock.acquire()
		try:
			checkMessages(chatid,chatInfo,messageList)
		except Exception as e:
			print('error checkeando ' + str(chatInfo.title))
			print(e)

			PrintException()
		startbotLock.release()


if(os.path.exists('check%s.pid' % comid) ):
	with open('check%s.pid' % comid,'r') as h:
		pid = int(h.read())
	try:
		os.kill(pid, signal.SIGKILL)
	except:
		pass
with open('check%s.pid' % comid,'w') as h:
	h.write(str(os.getpid()))

startbotLock = threading.Lock()
# while 1:
# 	checkChat(botgroup)
for checksss in range(200):
	try:
		threadChecks = []
		readChats = sub_client.get_chat_threads(start=0, size=30)  
		print('agarrando chats')
		sub_client.activity_status(1)
		for chatid,tipo in zip(readChats.chatId,readChats.type):
			if(tipo == 0):
				continue
			try:
				threadCheck = threading.Thread(target=checkChat, args=(chatid,))
				threadCheck.daemon = True
				threadCheck.start()
				threadChecks.append(threadCheck)
				# checkChat(chatid)
			except Exception as e:
				print("error checkeando chat")
				print(e)
				PrintException()
	except Exception as e:
		print(e)
		PrintException()
		os.system('./checkChats.py comid=%s &' % (comid) )
		os.kill(os.getpid(), signal.SIGKILL)	
	for i in threadChecks:
		i.join()

	# sleep(0.1)
os.system('./checkChats.py comid=%s &' % (comid) )
os.kill(os.getpid(), signal.SIGKILL)	
client.logout()
