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
from user import User
from chat import Chat
from mensaje import Mensaje
from comando import Comando
import unicodedata
import ujson as json
import pafy 
from amino.lib.util import headers as aminoHeaders

def getNickname(userid):
	return client.get_user_info(userid).nickname
def getBio(userid):
	return client.get_user_info(userid).json['content']
def send_message(chatId,message,tm=-1):
	if(tm == -1):
		tm = tipoMensaje
	return client.send_message(message=message, chatId=chatId,messageType=tm)
def send_reply(chatId,message,replyid):
	client.send_message(message=message, chatId=chatId,replyTo=replyid)
def good_upload(data=None,tipo=None,filename=None):
    if(filename):
        with open(filename,'rb') as h:
            data = h.read()
        tipo = 'imagen/' + filename[filename.rfind('.')+1:]
    if(not data):
        return
    link = None
    for i in range(5):
        try:
            link = client.upload_media(data=data,tipo=tipo)
            break
        except Exception as e:
            print(e)
            print('reintentando upload')
    return link



def send_invocacion(chatId,mentionUserIds,message=""):
	client.send_message(message=message, chatId=chatId,messageType=tipoMensaje,mentionUserIds=mentionUserIds)

def send_imagen(chatid,file):
	client.send_message(chatId=chatid,filePath=file)

def send_link(chatid,link):
	return client.send_message(chatId=chatid,link=link)

def get_host(chatid):
	thread = client.get_chat_thread(chatid)
	return thread.json['author']['uid']
def get_title(chatid):
	thread = client.get_chat_thread(chatid)
	return thread.json['title']

def get_cohosts(chatid):
	thread = client.get_chat_thread(chatid)
	return thread.extensions['coHost']

def log_in(alias='bot',userid=None):
	if(userid):
		login = s.loginInfo(id=userid)
	else:
		login = s.loginInfo(alias=alias)
	# if(True):
	# if(False):
	if(login[2] and login[3] + 3600 > time()):
		print('inicio cache')
		client.login_cache(login[2] )
	else:
		print('iniciando normal')
		print(login[0],login[1])
		r = client.login(email=login[0],password=login[1],get=True)
		if(type(r) != tuple or r[0] != 200):
			print('F')
			return None
		r1 = json.loads(r[1])
		r1['userProfile']['content'] = 'cache'
		r1 = json.dumps(r1)
		s.newLogin(id=client.profile.id,jsonResponse=r1)
	return login
s = Save()
client = amino.Client()
log_in('shita')
ley = 'your_uuid'
tipoMensaje = 0

