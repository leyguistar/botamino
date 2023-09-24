#!/usr/bin/env python3
import amino
import os
import sys
import mysql.connector
from save import Save
from time import time
from time import sleep
import threading
import signal
def get_host(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['author']['uid']

def getBio(userid):
	return sub_client.get_user_info(userid).json['content']

print('conecting with the database')
s = Save()
login = s.loginInfo(alias='bot')
chats = s.loadAllChats()
chatStates = s.loadBotstate()
ley = ''
leybot = '4882156e-efce-4a4b-88ca-02baff4d5e89'
ignoreChats = ['17ab60ec-0418-4c75-8ce3-fdb11613b201','3ac22d37-fd90-4d95-b53f-76068b0b5244']
chatStates = [i for i in chatStates if i[0] not in ignoreChats]
print('starting login')
comid = '67'
for i in sys.argv:
	if('comid=' in i):
		comid = i[6:]
client = amino.Client()
client.login(email=login[0],password=login[1])
sub_client = amino.SubClient(comId=comid,profile=client.profile)
bio = getBio(leybot)
st = bio.find('\n[cccccccccc]\n')
# st = bio.find('\n[cbiu]Placas:')
if(st >= 0):
	bio = bio[:st]

countActive = 0
for e in chatStates:
	print(e)
	if(e[1] == 1 and e[4] == int(comid)):
		countActive += 1

text = '\n[cccccccccc]\n'
text += '[cbiu]Chats activos justo ahora:\n\n'
text += '[cbi]%d\n' % (countActive)
text += '\n[c]▙▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▚▜\n'
text += '\n[buic]24/7:\n\n'
for e in chatStates:
	if(e[1] == 1 and e[4] == int(comid) and e[5] > 0 ):
		text += '[cbi][%s|ndc://x%s/chat-thread/%s]\n\n' % (chats[e[0]].name.replace('|',' '),comid,e[0])
text += '[c]◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤\n'
text += '\n[buic]Gratis:\n\n'
for e in chatStates:
	if(e[1] == 1 and e[4] == int(comid) and e[5] == 0):
		text += '[cbi][%s|ndc://x%s/chat-thread/%s]\n\n' % (chats[e[0]].name.replace('|',' '),comid,e[0])
text += '[c]﹏﹏﹏﹏﹏﹏✪✭✪﹏﹏﹏﹏﹏﹏﹏\n'
text += "\n[cbiu]🄿🄻🄰🄲🄰🅂:\n\n"
for chat in chats:
	if(chats[chat].placa != None and chats[chat].placa != ''):
		text += '[c]' + chats[chat].placa + '\n'
text += '\n[c]◇☆★☆★☆★☆◆\n'
print('actualizando bio:')
bio += text
print(bio)
sub_client.edit_profile(content=bio)
client.logout()
