import amino
from save import Save
from time import time
from litefuns import login,getUser
import os
import random
import discord

def getChatComid(chatid,s):
	if(chatid in chatComid):
		comid = chatComid[chatid]
	else:
		comid = s.loadChatMessageComid(chatid)
		chatComid[chatid] = comid
	return comid
def getChatClient(chatid,s):
	botid = s.loadBotChat(chatid)
	if(botid not in clients):
		client = login(botid)
		clients[botid] = client
	else:
		client = clients[botid]
	return client

def getChatSubClient(chatid,s):
	if(chatid in subClients):
		sub_client = subClients[chatid]
	else:
		client = getChatClient(chatid,s)
		comid = getChatComid(chatid,s)
		sub_client = client.sub_client(comid)
		subClients[chatid] = sub_client
	return sub_client
def send_message(chatid,message,s,tm=-1):
	comid = getChatComid(chatid,s)
	client = getChatClient(chatid,s)
	sub_client = client.sub_client(comid)

	sub_client.send_message(chatid,message)

async def send_interaccion(comando,message,mensaje=True):
	if(message.author.nick):
		nick = message.author.nick
	else:
		nick = message.author.name
	channel = message.channel
	path = 'interaccion/%s/' % (comando)
	ipath = path + 'SFW/'
	imagenes = os.listdir(ipath)
	if(message.mentions and os.path.exists(path + 'mensajes2.txt')):
		for mention in message.mentions:
			img = random.choice(imagenes)
			with open(path + 'mensajes2.txt','r') as h:
				frases =  [line.rstrip() for line in h]
			if(mention.nick):
				nick2 = mention.nick
			else:
				nick2 = mention.name
			if(mensaje):
				frase = random.choice(frases).replace('@',comando[-1])
				await channel.send(content=frase.replace('%s','**%s**') % (nick,nick2),file=discord.File(ipath + img) )
			else:
				await channel.send(file=discord.File(ipath + img) )
	else:
		if(os.path.exists(path + 'mensajes1.txt')):
			img = random.choice(imagenes)
			with open(path + 'mensajes1.txt','r') as h:
				frases =  [line.rstrip() for line in h]
			if(mensaje):
				frase = random.choice(frases).replace('@',comando[-1])
				await channel.send(content=frase.replace('%s','**%s**') % (nick),file=discord.File(ipath + img) )
			else:
				await channel.send(file=discord.File(ipath + img) )

		else:
			channel.send('Debes mencionar a alguien')



chatComid = {}
clients = {}
subClients = {}