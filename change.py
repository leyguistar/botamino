#!/usr/bin/env python3
from pprint import pprint
import os
import signal
import requests
from save import Save
import amino
s = Save()
client = amino.Client()
login = s.loginInfo(alias='bot')
client.login(email=login[0],password=login[1])
sub_client = amino.SubClient(comId='67',profile=client.profile)
comids = client.sub_clients().comId

def get_host(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['author']['uid']

s.cursor.execute('select id,comid,name from chats;')
chats = s.cursor.fetchall()
for c in chats:
	if(not c[1]):
		# for comid in comids:
			comid = '67'
			sub_client.comId = comid
			chat = sub_client.get_chat_thread(c[0])
			if(type(chat) == dict):
				print(c[2],'no',comid)
				for comid in comids:
					sub_client.comId = comid
					chat = sub_client.get_chat_thread(c[0])
					if(type(chat) == dict):
						print(c[2],'no',comid)
					else:
						s.chatComid(chat.json['ndcId'],chat.json['threadId'])
						print(chat.json['title'],'si',comid)
						break

			else:
				s.chatComid(chat.json['ndcId'],chat.json['threadId'])
				print(chat.json['title'],'si',comid)
client.logout()