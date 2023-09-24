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
def get_host(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['author']['uid']
print('conecting with the database')
s = Save()
login = s.loginInfo(alias='bot')
ley = 'your_uuid'
leybot = '4882156e-efce-4a4b-88ca-02baff4d5e89'
print('starting login')
comid = '67'
for i in sys.argv:
	if('comid=' in i):
		comid = i[6:]
client = amino.Client()
client.login(email=login[0],password=login[1])
sub_client = amino.SubClient(comId=comid,profile=client.profile)
print('logeado')
chats = s.loadAllChats()
print('chats cargados')


oldMessages = []
def checkChat(chatid):
		chatInfo = sub_client.get_chat_thread(chatId=chatid)  # Gets information of each chat
	# while True:
		messageList = sub_client.get_chat_messages(chatId=chatid,size=50)  # Gets messages of each chat
		print('checkeando ' + str(chatInfo.title) )
		for nickname, content, id, userid in zip(messageList.author.nickname, 
		messageList.content, messageList.messageId,messageList.author.id):
			if id in oldMessages: 
				continue
			oldMessages.append(id)  # Adds message id to a list so it doesn't repeat commands
			if(content == None):
				continue
			if(userid == leybot and  'Apagando bot por actualizaciones' in content):
				print('reiniciando bot en ' + str(chatInfo.title) + ' by ' + nickname)
				os.system("./bot.py id %s bot log comid=%s &" % (chatid,comid) )


while 1:
	readChats = sub_client.get_chat_threads(start=0, size=50).chatId  
	chats = s.loadAllChats()
	print('agarrando chats')
	sub_client.activity_status(1)
	for chatid in readChats:
		if(chatid not in chats):
			continue
		try:
			checkChat(chatid)
		except Exception as e:
			print("error checkeando chat")
			print(e)

client.logout()
