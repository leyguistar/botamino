#!/usr/bin/env python3
import discord
import amino 
from save import Save
import pprint
import random
import os
import threading
import signal
from user import User
import linecache
import sys
import traceback
from exception import PrintException
from litefuns import getNickname
from discordfuns import send_message,getChatSubClient,getChatClient,getChatComid
from discordfuns import send_interaccion

class Lista:
	def __init__(self):
		self.id = 0
		self.funados = []
listas = {}

dc = discord.Client()

@dc.event
async def on_ready():
    print('We have logged in as {0.user}'.format(dc))

async def sendDiscord(channel,message):
	await channel.send(message)
async def sendFile(channel,file):
	await channel.send(file=discord.File(file))

@dc.event
async def on_message(message):
	try:
		if message.author == dc.user:
			return
		if(message.guild and message.guild.id == 752622157435109406):
			return
		channel = message.channel
		content = message.content.split(' ')
		c = message.content
		m = None
		if(' ' in c):
			m = c[c.find(' ')+1:]
		print(message)
		print(message.content	)
		if(message.mentions):
			print(message.mentions)
		if(isinstance(channel,discord.channel.DMChannel) ):
			if content[0][0] == '/':
				comando = content[0][1:]
				if(comando == 'amino'):
					await sendDiscord(channel,'escribele el siguiente mensaje a tu bot al privado en amino')
					ok = False
					s = Save()
					while(not ok):

						code = random.randint(1000,9999)
						ok = s.linkDiscordUser(message.author.id,code,message.author.name)
					await sendDiscord(channel,'/discord %d' % (code))
		else:
			print(message.guild)
			guildid = message.guild.id
			authorid = message.author.id
			if(guildid not in listas):
				listas[guildid] = Lista()
			funados = listas[message.guild.id].funados
			if(message.author.id in funados):
				print('mensaje de funado eliminando')
				await message.delete()
			if(message.author.nick):
				nick = message.author.nick
			else:
				nick = message.author.name

			if(message.author.id == 612454908838281241):
				if(message.content == 'a' or message.content == 'A' or message.content == 'ª' or message.content == 'a-'):
					if(message.author.nick):
						nick = message.author.nick
					else:
						nick = message.author.name
					ahegaos = os.listdir('interaccion/1/gemir/NSFW')
					await channel.send(content='%s esta gimiendo' % (nick),file=discord.File('interaccion/1/gemir/NSFW/' + random.choice(ahegaos)) )
			if(not content):
				return
			if content[0][0] == '/':
				comando = content[0][1:]
				if(comando == 'amino'):
					if(len(content) < 2):
						text = 'uso : /amino [chat|mensaje|comando]'
						text += '/amino chat [link]: vincula un chat de amino con este servidor'
						text += '/amino mensaje [mensaje]: envia un mensaje al chat de amino vinculado con este servidor'
						text += '/amino comando [comando]: envia un comando al chat de amino vinculado con este servidor'
						await sendDiscord(channel,'uso: /amino [chat]\n')
					else:
						if(content[1] == 'chat'):
							if(len(content) != 3):
								await sendDiscord(channel,'Falta el link del chat de amino')
							else:
								ac = amino.Client()
								try:
									r = ac.get_from_code(content[2])
								except Exception as e:
									await sendDiscord(channel,'Error en el link')
									print(e)
								else:
									if(r.objectType == 12):
										s = Save()
										chatid = r.objectId
										comid = str(r.json['extensions']['linkInfo']['ndcId'])
										sub_client = ac.sub_client(comid)
										chatInfo = sub_client.get_chat_thread(chatid)
										userid = chatInfo.json['author']['uid']
										title = chatInfo.json['title']
										aminoid = s.loadDiscordUser(discordid=message.author.id)
										if(aminoid == None):
											await sendDiscord(channel,'Tu usuario en discord no esta vinculado con tu usuario en amino para hacerlo escribele al bot de discord en privado /amino')
										elif(aminoid == userid):
											s.discordGuild(message.guild.id,chatid)
											await sendDiscord(channel,'Vinculado exitosamente con: ' + title)
										else:
											await sendDiscord(channel,'Necesitas ser anfitrion de ese chat en amino para vincular con este grupo')

						elif(content[1] == 'mensaje'):
							if(len(content) < 3):
								await sendDiscord(channel,'Falta el mensaje')
								return
							s = Save()
							m = ' '.join(content[2:])
							chatsid = s.loadDiscordAminoChats(message.guild.id)

							if(not chatsid):
								await sendDiscord(channel,'no hay ningun chat de amino asociado a este server')
							chatid = chatsid[0]
							aminoid = s.loadDiscordUser(discordid=message.author.id)
							if(aminoid == None):
								await sendDiscord(channel,'Primero tienes que vincular tu usuario de amino con discord a traves de leybot')
								return
							m = ' '.join(content[2:])
							user = s.loadUser(aminoid)
							for chatid in chatsid:
								sub_client = getChatSubClient(chatid)
								send_message(chatid,getNickname(user,sub_client) + ': ' + m)
						elif(content[1] == 'comando'):
							await sendDiscord(channel,'actualmente no funcionando')
							return
							s = Save()
							chatsid = s.loadDiscordAminoChats(message.guild.id)
							if(not chatsid):
								await sendDiscord(channel,'no hay ningun chat de amino asociado a este server')
							chatid = chatsid[0]
							aminoid = s.loadDiscordUser(discordid=message.author.id)
							if(aminoid == None):
								await sendDiscord(channel,'Primero tienes que vincular tu usuario de amino con discord a traves de leybot')
								return
							m = ' '.join(content[2:])
							aminoMentions = []
							if(message.mentions):
								for mention in message.mentions:

									mid = mention.id

									m = m.replace('<@%d>','')
									m = m.replace('<@!%d>','')
									aid = s.loadDiscordUser(discordid=mid)
									if(mid == message.author.id):
										await sendDiscord(channel,'%s no te puedes mencionar a ti mismo en amino' % (mention.name))
									elif(not aid):
										await sendDiscord(channel,'%s no tiene su cuenta vinculada con amino' % (mention.name))
									else:
										aminoMentions.append(aid)
								
							ams = ''
							if(aminoMentions):
								ams = '<'
								for am in aminoMentions:
									ams += am + ','
								ams = ams[:-1] + '>'
							print('enviando comando %s al amino'% (m))		
							if(os.path.exists('fifos/' + chatid + '.fifo')):
								with open('fifos/' + chatid + '.fifo','w') as h:
										h.write('[%s] %s /%s\n' % (aminoid,ams,m))
								await sendDiscord(channel,'Comando mandado al amino')
				elif(comando in interacciones):
					await send_interaccion(comando,message)
				elif(comando == 'entrar'):
					if(content[1] == 'en'):
						await sendDiscord(channel,nick + ' a entrado ' + ' '.join(content[1:]))
					elif(content[1] in ['a','al']):
						await sendDiscord(channel,nick + ' se a unido ' + ' '.join(content[1:]))
					else:
						await sendDiscord(channel,nick + ' a entrado ' + ' '.join(content[1:]))

				elif(comando == 'dejar'):
					await sendDiscord(channel,nick + ' ha dejado ' + ' '.join(content[1:]))

				elif(comando == "load"):
					s = Save()
					aminoid = s.loadDiscordUser(discordid=message.author.id)
					if(aminoid == None):
						await sendDiscord(channel,'Tu usuario en discord no esta vinculado con tu usuario en amino para hacerlo escribele al bot de discord en privado /amino')
						return
					user = s.loadUser(aminoid)
					r = ""
					if(m == None):
						nombres = user.loadSaves()
						t = ""
						for n in nombres:
							t += n + '\n'
						await sendDiscord(channel,"Saves:\n" + t)	
					else:
						t = user.loadSave(m)
						print(m)
						if(t):
							if(t[1] == 0):
								await sendDiscord(channel,t[0])
							elif(t[1] == 2):
								# if('aac' in t[0] ):
								# 	await sendDiscord(channel,'Es un audio, y en discord no se pueden enviar audios')
								# else:
								await sendDiscord(channel,t[0])
							elif(t[1] == 3):
								await sendDiscord(channel,'Este es un sticker de amino')
						else:
							await sendDiscord(channel,'No tienes %s guardado' % (m))

				elif(comando == 'funar'):
					if(message.mentions):
						for mention in message.mentions:
							print('funando a ' + mention.name)
							funados.append(mention.id)

				elif(comando == 'perdonar'):
					if(message.mentions):
						for mention in message.mentions:
							if(mention.id in funados):
								print('perdonando a ' + mention.name)

								funados.remove(mention.id)

				elif(comando == 'comandos'):
					text += '```Interaccion: '
					text += ' '.join(interacciones) + '```'
					await sendDiscord(channel,text)
				elif(comando == 'say'):
					try:
						await message.delete()
					except Exception as e:
						print(e)

					await sendDiscord(channel,' '.join(content[1:]))


	except Exception as e:
		print('error')
		print(e)
		PrintException()
						
interacciones = os.listdir('interaccion')
dc.run('Nzk2Mzc1OTAwNzU2NjM5Nzk1.X_XA2g.IwTIxhoTgHRnx-lUGaABNsg50u0')
# dc.run('NzUyNjE5MjIzNTM2MzY5NjY2.X1aRRQ.ikxvup9x4EHUeKiwCdllCVxRBBE')