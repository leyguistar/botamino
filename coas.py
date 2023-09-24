#!/usr/bin/env python3
import amino
import os
import sys
import mysql.connector
from save import Save
import linecache
import traceback
from time import time
import json
s = Save(file='default.set')
def send_message(chatId,message):
	sub_client.send_message(message=message, chatId=chatId,messageType=100)
def getNickname(userid):
	return sub_client.get_user_info(userid).nickname

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

def sacarcoa(chat,userid):
	sub_client.remove_cohost(userid,chat)

def metercoa(chat,userid):
	cohosts = get_cohosts(chat)
	if(userid not in cohosts):
		cohosts.append(userid)
	else:
		return True
	r = sub_client.edit_chat(chat,coHosts=cohosts)
	if(r == 200):
		return send_message(chat,'%s es coa ahora' % (getNickname(userid)))
	return send_message(chat,'Coas llenos')

def get_cohosts(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.extensions['coHost']

login = s.loginInfo(alias='ley')
client = amino.Client()
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
sub_client = amino.SubClient(comId='67',profile=client.profile)
mc = sc = None
for i in sys.argv:
	if('m=' in i):
		mc = i[2:]
	if('s=' in i):
		sc = i[2:]
	if('c=' in i):
		chatid = i[2:]
if(mc):
	metercoa(chatid,mc)
if(sc):
	sacarcoa(chatid,sc)

client.logout()