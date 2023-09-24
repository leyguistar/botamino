#!/usr/bin/env python3
import amino
import ujson as json
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
from exception import PrintException
from litefuns import send_imagen
from litefuns import copy_profile
from save import Save
from litefuns import send_message,send_reply,send_link,get_chat_thread,mostrarMarcos,get_comandos_comunidad
from litefuns import getNickname,getTrueNickname,send_text_imagen,send_text_imagen_raw
from litefuns import addLogro
from amino.lib.util import headers as aminoHeaders
from liteobjs import ley,leybot,botgroup,bots,defaultClient,comandosLite,respuestas
from liteobjs import bannedUsers,bannedChats,bannedComunidades
from liteobjs import comunidades,mensajes
from liteobjs import leyworld,palabrasIdioma,chats
from liteobjs import telefonos,resultadosTelefonos,imgdir
from liteobjs import telefonosInternacionales,resultadosTelefonosInternacional
import re
import random
import unicodedata
from comunidad import Comunidad
from lite_loop import commentNewUserWall,get_new_members
from itertools import islice

def checkPrivate(chatid,message,client,comid,s,bot):
	global backgroundImage
	# sub_client = amino.SubClient(comid,client)
	sub_client = client.sub_client(comid)
	try:
		content = message.get('content')
		userid = message['uid']
		role = message['author']['role']
		if(userid == client.profile.id):
			return
		comunidad = comunidades.get(comid)
		if(not comunidad):
			return
		if(not comunidad.idioma):
			cominfo = client.get_community_info(comid)
			comunidad.idioma = cominfo['primaryLanguage']
			s.comunidadIdioma(comid,comunidad.idioma)
		chat = chats[chatid]
		idioma = chat.idioma
		if(idioma not in ['en','es']):
			idioma = 'en'
		if(userid in bannedUsers):
			text = mensajes[idioma][492] + '\n'
			razon = bannedUsers[userid]
			if(razon):
				text += mensajes[idioma][493] % (razon) + '\n'
			else:
				text += mensajes[idioma][494] + '\n'

			send_message(chatid,text)
			return
		nickname = message['author']['nickname']
		tipo = message['type']

		if(role == 100 or role ==102):
			lider = True
		else:
			lider = False
		if(tipo == 103):
			sub_client.join_chat(chatid)
			if(not backgroundImage):
				r = sub_client.upload_background(chatid,f='fondos/1a98a0e6895bd01ab485d24da248d6091cab8787r3-1200-1600_00.gif')
				backgroundImage = r
			else: 
				sub_client.edit_chat(chatId=chatid,backgroundImage=backgroundImage)

			print('llego un mensaje 103')
			# if(role == 100 or role == 102):
			# 	send_message(chatid,mensajeid=495)
			if(comunidad and comunidad.privateChatMessage):
				send_message(chatid,comunidad.privateChatMessage)
			else:
				if(not content):
					with open('privado/%s/initial.txt' % (idioma),'r') as h:
						m = h.read()
					send_message(chatid,m)
			addLogro(chat,userid,43,s)
		extensions = message.get('extensions',{})
		if(not content):
			return
		print(nickname,content)
		# if(userid != ley):
		# 	return
		id = message['messageId']
		# s.PrivateChatMessageID(id)
		if(not content):
			return
		rsb = respuestas[client.profile.id]
		contentLower = content.lower()
		sre = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
		unicodedata.normalize( "NFD", contentLower), 0, re.I
		)
		contentLower = unicodedata.normalize('NFKC',sre)
		if(contentLower in rsb):                    
			send_message(chatid,random.choice(rsb[contentLower]).replace('[@]',getNickname(userid,sub_client)),tm=0)

		if('replyMessageId' in extensions):
		    replyid = extensions['replyMessageId']
		    if('replyMessage' in extensions):
		        replyuid = extensions['replyMessage']['uid'] #cuidao con esto
		    else:
		        replyuid = None
		else:
		    replyid = None
		    replyuid = None

		allContent = content
		content = content.split(' ')
		palabras = palabrasIdioma[idioma]
		if(content[0][0] == '/'):
			comando = content[0][1:]
		else:
			comando = ''
		m = None
		if(len(content) > 1):
		    m = allContent[allContent.find(' ')+1:]
		# print(idioma,comandosIdioma[idioma],comando)
		print(comandosIdioma[idioma])
		commandid = comandosIdioma[idioma].get(comando,0)
		print(comando,commandid)
		if(contentLower == 'ola' or contentLower == 'hola'):
			send_message(chatid,mensajeid=496)
			send_message(chatid,mensajeid=497)
		# elif(comando == 'premium'):
		# 	send_message(chatid,mensajeid=498)
		elif(commandid == 26): #start
		    sub_client.join_chat(chatid)
		    with open('privado/%s/mensajes/start.txt' % (idioma),'r') as h:
		        sm = h.read()
		    send_message(chatid,sm)
		    # link = None
		    # with open('fondos/1a98a0e6895bd01ab485d24da248d6091cab8787r3-1200-1600_00.gif','rb') as h:
		    #     link = client.upload_media(file=h,tipo='image/gif')
		    link = 'http://pa1.narvii.com/7791/d921609e746b770dec2ebffe274e7d72205cf792r3-480-640_00.gif'
		    sub_client.edit_chat(chatId=chatid,backgroundImage=link)
		elif(commandid == 13): #escribir
			if(userid != bot['owner'] and userid != ley):
				send_message(chatid,mensajeid=499)
				return
			if(len(content) < 2):
				text = 'usos: /escribir [mensaje o link]\n'
				text += 'Para escribir en tu muro:\n'
				text += '/escribir hola soy tu bot\n'
				text += 'Para escribir en el muro de los demas:\n'
				text += '/escribir http://aminoapps.com/p/linkejemplo hola soy el bot de %s\n' % (nickname) 
				send_message(chatid,text)
			else:
				if(content[1].startswith('http://aminoapps.com/p/')):
					response = requests.get(f"{client.api}/g/s/link-resolution?q={content[1]}", headers=aminoHeaders.Headers(sid=client.sid).headers)
					js = json.loads(response.text)
					if(js['api:statuscode'] == 107):
						send_message(chatid,mensajeid=500)
						return
					extensions = js['linkInfoV2']['extensions']
					r = extensions.get('linkInfo',None)
					if(not r):
						send_message(chatid,mensajeid=501)
						return
					targetUserid = r['objectId']
					if(r['objectType'] != 0):
						send_message(chatid,mensajeid=502)
						return
					if(len(content) < 3):
						send_message(chatid,mensajeid=503)
						return
					m = ' '.join(content[2:])
				else:
					targetUserid = userid
				r = sub_client.comment(m,userId=targetUserid)
				print(r)
				if(r != 200):
					if(r['api:statuscode'] == 270):
						send_message(chatid,mensajeid=504)
						send_message(chatid,r['url'])
					else:
						send_message(chatid,mensajeid=505)
				else:
					if(userid == targetUserid):
						send_message(chatid,mensajeid=506)
					else:
						send_message(chatid,'Listo ya le comente el muro a %s' % (getTrueNickname(targetUserid,sub_client)))
					# send_message(chatid,mensajeid=507)
		elif(commandid == 24): #salir
		    sub_client.leave_chat(chatid)
		elif(commandid == 10): #discord
			print('en discord')
			if(len(content) < 2):
				send_message(chatid,mensajeid=508)
			else:
				discordid = s.loadDiscordUserCode(int(content[1]))
				
				if(discordid == None):
					send_message(chatid,mensajeid=509)
				elif(time() - int(discordid[2]) > 3600):
					send_message(chatid,mensajeid=510)
				else:
					s.discordUser(userid,discordid[0])
					send_message(chatid,mensajeid=598,args=discordid[1])
		elif(commandid == 8): #crear
			if(userid != bot['owner'] and userid != ley):
				send_message(chatid,mensajeid=499)
				return
			ln = allContent.split('\n')
			con = ln[0].split(' ')
			if(len(con) < 2) :
			    send_message(chatid,mensajes[idioma][512].replace('\\','\n'))                          
			elif(len(ln) < 2):
				send_message(chatid,mensajeid=513)
			else:
				l0 = ln[0]
				mensaje = l0[l0.find(' ')+1:].strip().rstrip()
				respuesta = '\n'.join(ln[1:])
				if(mensaje in respuestas[bot['userid']]):
				    text = mensajes[idioma][595] % (mensaje)
				else:
					text  = mensajes[idioma][596] % (mensaje)
					sre = re.sub(
					    r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
					    unicodedata.normalize( "NFD", mensaje), 0, re.I
					    )
					mensaje = unicodedata.normalize('NFKC',sre).lower()

					respuestas[bot['userid']][mensaje] = [i for i in respuesta.split('|')]
					s.respuestas(bot['userid'],respuestas[bot['userid']])
				send_message(chatid,text)
		elif(commandid == 41): #eliminar

			if(len(content) < 2):
				send_message(chatid,mensajeid=153)                         
			else:
				botid = bot['userid']
				mlower = m.lower()
				if(mlower in respuestas[botid]):
				    respuestas[botid].pop(mlower)
				    s.connect()
				    s.respuestas(botid,respuestas[botid])
				    s.close()
				    send_message(chatid,mensajeid=154)
				else:
					send_message(chatid,mensajeid=352,args=(m))
		elif(commandid == 42): #respuestas
			botid = bot['userid']
			text = 'Respuestas:\n'
			for m,r in respuestas[botid].items():
				text += '%s: %s\n' % (m,'|'.join(r) )
			send_message(chatid,text)
		elif(commandid == 43): #edit
			if(len(content) < 2):
				send_message(chatid,'falta el nombre del bot al cual va dedicado el edit')
			else:
				name = content[1].lower()
				if(name not in nombres):
					send_message(chatid,'nombre de bot invalido solo puede ser uno de los siguientes bots')
					send_message(chatid,' '.join(nombres))
					return
				messageList = sub_client.get_chat_messages(chatId=chatid,size=5,raw=True)['messageList']
				mediaValue = None
				mid = None
				for m in messageList:
					if(m['mediaValue']):
						mediaValue = m['mediaValue']
						mid = m['messageId']
						break
				if(not mediaValue):
					send_message(chatid,'no detecte ninguna imagen reciente')
					return
				s.saveEdit(userid,name,mediaValue)
				send_reply(chatid,'exito guardando el edit',replyid=mid)

		elif(commandid == 3): #aceptar
			if(len(content) < 2 ):
			    send_message(chatid,mensajeid=514)
			elif(content[1] == palabras['lider']):
			    r = sub_client.accept_leader()
			    if(not r):
			        send_message(chatid,mensajeid=515)
			    elif(r == 200):
			        send_message(chatid,mensajeid=516)
			elif(content[1] == palabras['curador']):
			    r = sub_client.accept_curator()
			    if(not r):
			        send_message(chatid,mensajeid=517)
			    elif(r == 200):
			        send_message(chatid,mensajeid=518)

		elif(commandid == 18): #lider
			if(lider):
				with open('privado/%s/lider.txt' % (idioma),'r') as h:
					send_message(chatid,h.read())
			else:
				send_message(chatid,mensajeid=519)
		elif(commandid == 31): #config
			if(not lider):
				send_message(chatid,mensajeid=520)
				return
			if(not comunidad):
				comunidad = s.loadComunidad(comid)
				if(not comunidad):
					s.comunidad(comid)
					comunidad = Comunidad(comid)
				comunidades[comid] = comunidad 

			text = mensajes[idioma][599] + '\n'
			if(comunidad.botid):
				text += mensajes[idioma][600] % bots[comunidad.botid]['name'] + '\n'
			else:
				text += mensajes[idioma][601] + '\n'

			text += mensajes[idioma][602] + ('si' if comunidad.recibir & 1 else 'no') + '\n'
			send_message(chatid,text)
		elif(commandid == 22): #recibir
			if(userid != bot['owner']):
				send_message(chatid,mensajeid=521)
			if(not lider):
				send_message(chatid,mensajeid=522)
			if(not comunidad):
				comunidad = s.loadComunidad(comid)
				if(not comunidad):
					s.comunidad(comid)
					comunidad = Comunidad(comid)
				comunidades[comid] = comunidad

			if(len(content) < 2):
				send_message(chatid,mensajeid=523)
			elif(content[1] == palabras['si']):
				if(not comunidad.wallMessage):
					send_message(chatid,mensajes[idioma][524].replace('\\','\n'))
					return
				if(not comunidad.botid):
					send_message(chatid,mensajeid=525)
					return					
				if(comunidad.recibir):
					send_message(chatid,mensajeid=526)
				else:
					send_message(chatid,mensajeid=527)
					comunidad.recibir = 1
					s.comunidadRecibir(comid,1)
					
			elif(content[1] == palabras['no']):
				comunidad.recibir = 0
				s.comunidadRecibir(comid,0)
				send_message(chatid,mensajeid=528)
			else:
				send_message(chatid,mensajeid=523)
		elif(commandid == 37): #telefono
			if(len(content) < 2 ):
				send_message(chatid,'uso: /telefono [local|internacional|colgar]: llamas a alguien random en esta comunidad, si contesta les enviare a los 2 un link para que se comuniquen')
			else:
				if(content[1] == 'local' or content[1] == 'internacional'):
					if(content[1] == 'local'):
						send_message(chatid,'Llamada solo en esta comunidad')
						local = True
					else:
						send_message(chatid,'Llamada dentro y fuera de esta comunidad')
						local = False
					if(len(content) < 3):
						send_message(chatid,'uso: /telefono %s [mensaje inicial]: Un mensaje corto para iniciar la conversacion' % (content[1]))
					else:
						if(userid in telefonosInternacionales):
							send_message(chatid,'Ya estas haciendo una llamada')
							return

						if(comid not in telefonos):
							telefonos[comid] = {}
						if(comid not in resultadosTelefonos):
							resultadosTelefonos[comid] = {}
						if(userid in telefonos[comid]):
							send_message(chatid,'Ya estas haciendo una llamada')
							return
						m = ' '.join(content[2:])
						e = threading.Event()
						send_message(chatid,'llamando... te avisare cuando alguien conteste.')
						i = random.choice(['telefono_rosado.gif','telefono_ventana.gif','chica_telefono.gif'])
						send_imagen(chatid,imgdir + i,sanitized=True)
						if(telefonos[comid] or (not local and telefonosInternacionales)):
							if(not local and telefonosInternacionales):
								result = random.choice(list(telefonosInternacionales.keys()) )
								e,nm = telefonosInternacionales[result]
								resultadosTelefonosInternacional[result] = (userid,m)
								# telefonos[comid].pop(result)
								telefonosInternacionales.pop(result)
								link = 'ndc://x0/user-profile/' + result 
								addLogro(chat,userid,60)

							else:
								result = random.choice(list(telefonos[comid].keys()) )
								e,nm = telefonos[comid][result]
								resultadosTelefonos[comid][result] = (userid,m)
								telefonos[comid].pop(result)
								link = None
								addLogro(chat,userid,59)

							print('cambiado el valor de',result)
							e.set()
							send_message(chatid,'Alguien contesto a tu llamada')
							sub_client.send_message(chatid,'Este usuario quiere comunicarse contigo, si quieres hablar con el solo ve a su perfil siguelo y abre su privado',embedType=0,embedId=result,embedContent=nm,messageType=57,embedLink=link)
						else:
							telefonos[comid][userid] = (e,m) 
							if(not local):
								telefonosInternacionales[userid] = (e,m)
							e.wait(180)

							if(e.is_set()):
								if(userid in telefonos[comid]):
									telefonos[comid].pop(userid)
								print('revisando el valor de',userid)
								if(userid in resultadosTelefonos[comid]):
									result,m = resultadosTelefonos[comid][userid]
									link = None
									addLogro(chat,userid,59)
								else:
									result,m = resultadosTelefonosInternacional[userid]
									link = 'ndc://x0/user-profile/' + result
									addLogro(chat,userid,60)

								send_message(chatid,'Alguien contesto a tu llamada')
								sub_client.send_message(chatid,'Este usuario quiere comunicarse contigo, si quieres hablar con el solo ve a su perfil y abre su privado',embedType=0,embedId=result,embedContent=m,embedLink=link,messageType=57)
							else:
								telefonos[comid].pop(userid)
								if(userid in telefonosInternacionales):
									telefonosInternacionales.pop(userid)

								send_message(chatid,'Chale nadie contesto a tu llamada %s' % (getNickname(userid,sub_client)))
				elif(content[1] == 'colgar'):
					if(comid not in telefonos):
						telefonos[comid] = {}
					if(comid not in resultadosTelefonos):
						resultadosTelefonos[comid] = {}

					if(userid in telefonos[comid]):
						if(userid in telefonosInternacionales):
							telefonosInternacionales.pop(userid)
						telefonos[comid].pop(userid)
						send_message(chatid,'Colgaste')
					else:
						send_message(chatid,'No estabas llamando')

		elif(commandid == 38): #revisar
			with open('revisar.txt','r') as h:
				text = h.read().split('\n\n\n')
			sub_client.send_message(chatid,text[0])
			sub_client.send_message(chatid,text[1])
			sub_client.send_message(chatid,link='http://pm1.narvii.com/7885/b5763409df7a2d9ab145749a38a1919b8559fe6fr1-1214-720v2_00.jpg')

		elif(commandid == 29): #leyworld
			send_message(chatid,'http://aminoapps.com/c/leyworld')
		elif(commandid == 20): #mensaje
			if(userid != bot['owner']):
				send_message(chatid,mensajeid=521)
			if(not lider):
				send_message(chatid,mensajeid=533)

			ln = allContent.split('\n')
			content = ln[0].split(' ')
			if(len(content) != 2 ):
				send_message(chatid,mensajes[idioma][534].replace('\\','\n'))
			else:
				if(not comunidad):
					comunidad = s.loadComunidad(comid)
					if(not comunidad):
						s.comunidad(comid)
						comunidad = Comunidad(comid)
					comunidades[comid] = comunidad
				if(content[1] == palabras['muro']):
					if(len(ln) < 2):
						if(comunidad.wallMessage):						
							send_message(chatid,'Mensaje actual:\n' + comunidad.wallMessage)
						else:	
							send_message(chatid,mensajeid=535)
							send_message(chatid,mensajeid=536)
					else:
						comunidad.wallMessage = '\n'.join(ln[1:])
						s.comunidadWallMessage(comid,comunidad.wallMessage)
						send_message(chatid,mensajeid=537)

				elif(content[1] == palabras['privado']):
					if(len(ln) < 2):
						if(comunidad.privateChatMessage):						
							send_message(chatid,'Mensaje actual:\n' + comunidad.privateChatMessage)
						else:	
							send_message(chatid,mensajeid=535)
							send_message(chatid,mensajeid=539)
					else:
						comunidad.privateChatMessage = '\n'.join(ln[1:])
						s.comunidadPrivateMessage(comid,comunidad.privateChatMessage)
						send_message(chatid,mensajeid=540)
				elif(content[1] == 'chat'):
					if(len(ln) < 2):
						if(comunidad.welcomeChatMessage):						
							send_message(chatid,'Mensaje actual:\n' + comunidad.welcomeChatMessage)
						else:	
							send_message(chatid,mensajeid=535)
							send_message(chatid,mensajeid=539)
					else:
						comunidad.welcomeChatMessage = '\n'.join(ln[1:])
						s.comunidadWelcomeChatMessage(comid,comunidad.welcomeChatMessage)
						send_message(chatid,mensajeid=540)

				else:
					send_message(chatid,mensajes[idioma][534].replace('\\','\n'))
		elif(commandid == 34): #chatBienvenida
			if(userid != bot['owner']):
				send_message(chatid,mensajeid=542)
				return
			if(not lider):
				send_message(chatid,mensajeid=543)
				return
			if(len(content) < 2):
				send_message(chatid,'uso: /chatBienvenida [link del chat]: Da las bienvenidas a los usuarios en un chat')
			else:
				r = client.get_from_code(content[1])
				if(r.objectType == 12):
					comunidad.welcomeChat = r.objectId
					s.comunidadChatBienvenidas(comid,r.objectId)
					chatThread = get_chat_thread(r.objectId,comid,client,error=True,new=True)
					r = sub_client.join_chat(r.objectId)
					print(r)
					send_message(chatid,'El chat de bienvenidas es ahora %s' % (chatThread['title']))
		elif(commandid == 35): #eventos
			eventos = s.loadEventos()
			if(not eventos):
			    send_message(chatid,'No hay eventos')
			    return
			for evento in eventos:
			    text = '[ciub]' + evento['nombre'] + '\n\n'
			    text += evento['descripcion'] + '\n\n'
			    text += 'Desde el %s' % (str(evento['inicio']).split(' ')[0] ) + '\n'
			    text += 'Hasta el %s' % (str(evento['final']).split(' ')[0] ) + '\n'
			    send_text_imagen(chatid,text,evento['link'],evento['imagen'])
		elif(commandid == 36): #musica
			l = "http://pa1.narvii.com/7858/cc8ddd608e088ab5eb08b3df81b782bd4c71079ar1-320-320_00.gif"
			neo_sub_client = client.sub_client(leyworld)
			sub_client.send_message(chatid,'Si quieres saber como puedes ayudar a que vuelvan los comandos de musica puedes revisar este post',el=l,embedId="589ad7cd-73e9-4c1d-a086-3714195f7b71",embedType=1,embedLink='ndc://x228964941/blog/589ad7cd-73e9-4c1d-a086-3714195f7b71',embedContent='Explicacion rapida de porque no funcionan los comandos de musica')
			# send_imagen(chatid,'imgs/ok-anime.gif',sanitized=True)
			send_link(chatid,l,sanitized=True)
		elif(commandid == 39): #ver
			if(len(content) < 2 and not replyid):
				send_message(chatid,'Selecciona un blog')
			else:
				if(len(content) > 1):
					nombre = content[1]
					if(nombre in perfiles):
						blogId = perfiles[nombre]
						d = 'blogs/' + nombre + '/'
						files = dict([(i[:i.find('.')],i) for i in os.listdir(d)])
						subc = client.sub_client(leyworld)
						blog = subc.get_blog_info(blogId)['blog']
						content = blog['content']
						mediaList = blog['mediaList']
						while content:
						    p = content.find('[IMG=')
						    if(p >= 0):
						        text = content[:p]
						        img = content[p+5:8+p]
						        content = content[p+9:].lstrip()
						        if(img in files):
						            img = d + files[img]
						        else:
						            continue
						        print('img2',img)
						        print(text)
						        if(not text):
						            text = '[c]'
						        r = send_text_imagen_raw(chatid,text,filename=img,url='ndc://x228964941/blog/' + blogId)
						        if(not r):
						            print('error')
						            print('img',img)
						            print('text',text)
						    else:
						        break
				if(replyid):
					message = sub_client.get_message_info(chatid,replyid).json
					extensions = message.get('extensions',{})
					if(not extensions):
						extensions = {}
					at = extensions.get('attachedObjectInfo')
					if(not at):
						send_message(chatid,'El mensaje seleccionado no es de un blog valido')
					else:
						blogId = at.get('objectId')
					nombre = nombres[blogId]
					d = 'blogs/' + nombre + '/'
					files = dict([(i[:i.find('.')],i) for i in os.listdir(d)])
					subc = client.sub_client(leyworld)
					blog = subc.get_blog_info(blogId)['blog']
					content = blog['content']
					mediaList = blog['mediaList']
					while content:
					    p = content.find('[IMG=')
					    if(p >= 0):
					        text = content[:p]
					        img = content[p+5:8+p]
					        content = content[p+9:].lstrip()
					        if(img in files):
					            img = d + files[img]
					        else:
					            continue
					        print('img2',img)
					        print(text)
					        if(not text):
					            text = '[c]'
					        r = send_text_imagen_raw(chatid,text,filename=img,url='ndc://x228964941/blog/' + blogId)
					        if(not r):
					            print('error')
					            print('img',img)
					            print('text',text)
					    else:
					        break

		elif(commandid == 40): #votar
			if(len(content) < 2 and not replyid):
				votos = list(votosBot.values())
				for b in nombres:
					v = votos.count(b)
					text = '[cb]' + nombres[b] + '\n\n'
					if(v == 1):
						text += '[ci]%d voto\n' % (v)
					else:
						text += '[ci]%d votos\n' % (v)
					l = 'ndc://x%s/blog/%s' % (leyworld,b)
					filename = 'blogs/portadas/' + nombres[b] + '.png'
					# send_text_imagen_raw(chatid,text,filename=,url=l)
					sub_client.send_message(chatid,fileEmbedImage=filename,fileEmbedType='image/png',message=text,fileEmbedImageLink=l,embedId=b)

					# sub_client.send_message(chatid,nombres[b],embedId=None,el=portadas[b],embedLink=l,embedType=0,embedTitle=nombres[b],embedContent=text)
				send_message(chatid,'Para votar puedes seleccionar un mensaje con /votar o /votar [nombre del bot] , ten en cuenta que si ya votaste por un perfil de este bot estaras cambiando tu voto')
				send_message(chatid,'Para ver un preview sin necesidad de ir a el blog original puedes usar /ver [nombre]. Pero recomiendo ir al blog original')
			if(len(content) > 1):
				nombre = content[1]
				if(nombre in perfiles):
					blogId = perfiles[nombre]
					if(userid in votosBot):
						s.updateVoto(userid,blogId)
					else:
						s.addVoto(userid,blogId)
					votosBot[userid] = blogId
					votos = list(votosBot.values()).count(blogId)
					if(votos == 1):
						econtent = '1 voto'
					else:
						econtent = '%d votos' % (votos)
					sub_client.send_message(chatid,'Acabas de votar por %s' % nombres[blogId],embedId=None,el=portadas[blogId],embedType=1,embedContent=econtent,embedTitle=nombres[blogId])
					addLogro(chat,userid,50,s)
			if(replyid):
				print(replyid,chatid)
				message = sub_client.get_message_info(chatid,replyid).json
				extensions = message.get('extensions',{})
				if(not extensions):
					extensions = {}
				at = extensions.get('attachedObjectInfo')
				if(not at):
					send_message(chatid,'El mensaje seleccionado no es de un blog valido')
				else:
					blogid = at.get('objectId')
					if(userid in votosBot):
						s.updateVoto(userid,blogid)
					else:
						s.addVoto(userid,blogid)
					votosBot[userid] = blogid
					votos = list(votosBot.values()).count(blogid)
					if(votos == 1):
						econtent = '1 voto'
					else:
						econtent = '%d votos' % (votos)
					sub_client.send_message(chatid,'Acabas de votar por %s' % nombres[blogid],embedId=None,el=portadas[blogid],embedType=1,embedContent=econtent,embedTitle=nombres[blogid])
					addLogro(chat,userid,50,s)
		# elif(commandid == 41): #audio
		#     if(len(content) < 2 ):
		# 		with open('audios/ayuda.txt','r') as h:
		# 			text = h.read()
		# 		send_message(chatid,text)
		# 	else:
		# 		if(content[1] == 'grabar'):
		# 			if(len(content) < 3 or content[2] not in ['chica','chico','sorpresa']):
		# 				send_message(chatid,'Tienes que especificar si es de chica o de chico')
		# 				send_message(chatid,'/audio grabar chica [lo que vas a decir]')
		# 				send_message(chatid,'/audio grabar chico [lo que vas a decir]')
		# 				send_message(chatid,'/audio grabar sorpresa [lo que vas a decir]')
		# 			else:
		# 				if(len(content) < 4 ):
		# 					send_message(chatid,'Falta lo que quieres decir ejemplo:')
		# 					send_message(chatid,'/audio grabar %s hola ' % content[2])
		# 				else:
		# 					message = sub_client.get_message_info(chatid,replyid)
		# 					content = message.json['content']
		# 					mediaValue = message.json['mediaValue']
		# 					t = message.json['type']
		# 					if(t == 100):
		# 						send_message(chatid,mensajeid=174)
		# 					elif(not mediaValue or not mediaValue.endswith('.aac')):
		# 						send_message(chatid,'no es un audio')
		# 					else:
		# 						text = ' '.join(content[4:])
		# 						if(len(text) > 135):
		# 							send_message(chatid,'El texto es muy largo, hazlo mas corto (no tienes que incluir todo lo que dices en la nota de voz')
		# 							return
		# 						audio = requests.get(mediaValue).content
		# 						name = str(time()).replace('.','') + '.aac'

		# 						with open(name,'wb') as h:
		# 							h.write(audio)
		# 						os.open('audios.txt',)	





		elif(commandid == 30): #setbot
			if(userid != bot['owner']):
				send_message(chatid,mensajeid=542)
				return
			if(not lider):
				send_message(chatid,mensajeid=543)
				return
			if(not comunidad):
				comunidad = Comunidad(comid,client.profile.id)
				comunidades[comid] = comunidad
				s.comunidad(comid,client.profile.id)
			else:
				comunidad.botid = client.profile.id
				s.comunidadBot(comid,client.profile.id)
			t = threading.Thread(target=get_new_members, args=(comunidad,))
			t.daemon = True
			t.start()
			send_message(chatid,mensajeid=544)
		elif(commandid == 17): #liberar
		    if(len(content) < 2 ):
		        send_message(chatid,mensajeid=545)
		    else:
		        r = client.get_from_code(content[1])
		        if(r.objectType == 12):
		            chat = s.loadChat(r.objectId)
		            if(userid in chat.ops and chat.ops[userid] >= 2):
		                sub_client.edit_chat(chat.id,viewOnly=False)
		            else:
		                send_message(chatid,mensajeid=546)
		elif(commandid == 19): #marcos
			mostrarMarcos(chatid,comid)
		elif(commandid == 33): #comandos
			text = ''
			for ct in ctipos:
				text += mensajes[idioma][15] % (tipos_comandos[idioma][ct])
				for c in ctipos[ct]:
					if(not c[1]):
						continue
					try:
						text += ' %s ' % (comandosReverseMap[idioma][comandosIdioma['es'][c[1]]] )
					except:
						PrintException()
				text += '\n\n\n'
			send_message(chatid,text)

		elif(commandid == 7): #chats
			send_message(chatid,mensajeid=315)
			return
			if(len(content) < 2):
				text = 'uso: /chats [comunidad|total|autorizado]: muestra los chats donde esta tu bot\n'
				text += '/chats autorizado: chats donde lo autorizaste\n'
				text += '/chats total: todos los chats donde esta elegido (como bot principal)\n'
				text += '/chats comunidad: los chats de esta comunidad donde esta invitado o unido'
				send_message(chatid,text)
			elif(content[1] == 'autorizado'):
				text = ''
				for c in bot['autorizados']:
					cid = s.loadChatComid(c)
					text += 'ndc://x%d/chat-thread/%s\n' % (cid,c)
		elif(commandid == 27): #tag
			tags = s.loadUserTags(userid)
			if(m == None or m.find('!') == -1):
				if tags != None:
					print(tags)
					text = mensajes[idioma][702] + '\n'
					i = 1
					for t in tags:
						if(tags[t] != None):
							text += ('%d.' % i) + t + ':' + tags[t] + '\n'
						else:
							text += ('%d.' % i) + t + '\n'
						i += 1
					send_message(chatid,text)
				else:
					send_message(chatid,mensajeid=547)
				send_message(chatid,mensajeid=548)
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
				send_message(chatid,'agregada tag ' + tag)
		elif(commandid == 23): #rtag
			if(not m or not m.isdigit()):
				send_message(chatid,mensajeid=703)
				return
			n = int(m)-1
			tags = s.loadUserTags(userid)
			if(n < 0 or n > len(tags)):
				send_message(chatid,mensajeid=704)
				return
			tag = next(islice(tags, n, None))
			del tags[tag]
			s.UserTag(userid,tags)
			send_message(chatid,'removida ' + tag)
		elif(commandid == 15): #habilitar
			if(len(content) != 2):
				send_message(chatid,mensajeid=549)
			else:
				c = content[1]
				if(c not in comandosLite[idioma]):
					send_message(chatid,mensajeid=603,args=c)
				else:
					if(lider):
						send_message(chatid,mensajeid=604,args=(content[1]))
						comandosCom = get_comandos_comunidad(comid)
						comandosCom[comandosLite[idioma][c]] = 1
						s.comandoComunidad(comid,comandosCom)
					else:
						send_message(chatid,mensajeid=605)

		elif(commandid == 9): #deshabilitar
			if(len(content) != 2):
				send_message(chatid,mensajeid=550)
			else:
				c = content[1]
				if(c not in comandosLite[idioma]):
					send_message(chatid,mensajeid=603,args=c)
				else:
					userInfo = sub_client.get_user_info(userid,raw=True)['userProfile']
					role = userInfo['role']
					if(lider):
						send_message(chatid,mensajeid=606,args=(content[1]))
						comandosCom = get_comandos_comunidad(comid)
						comandosCom[comandosLite[idioma][c]] = 0
						s.comandoComunidad(comid,comandosCom)
					else:
						send_message(chatid,mensajeid=551)


		elif(commandid == 25): #sigueme
			if(not bot['public'] and userid != bot['owner']):
				send_message(chatid,mensajeid=552)
			else:
				if(comid in bannedComunidades):
					send_message(chatid,mensajeid=553)
					razon = bannedComunidades[comid]
					if(razon):
						send_message(chatid,'Razon: %s' % (razon))
					else:
						send_message(chatid,mensajeid=554)
					return						

				sub_client.follow(userid)
				send_reply(chatid,mensajeid=408,replyid=id)
		elif(commandid == 28): #web
			send_message(chatid,mensajeid=555)
			return
			token = secrets.token_urlsafe(128)
			s.createWebLogin(userid,token)
			send_message(chatid,mensajeid=556)
			send_message(chatid,'https://leybot.leyguistar.com/login/%s?token=%s' % (userid,token))
		elif(commandid == 2): #abandonar
			if(userid != bot['owner'] and userid != ley):
				send_message(chatid,mensajeid=542)
				return
			if(len(content) < 2 or content[1] != 'confirmar'):
				send_message(chatid,mensajeid=558)
				return

			if(comid == leyworld):
				send_message(chatid,mensajeid=559)
				return
			send_message(chatid,mensajeid=560)
			client.leave_community(comid)
		elif(commandid == 32): #idioma
			if(len(content) < 2):
				send_message(chatid,mensajeid=308)
			else:
				if(content[1] not in ['en','es']):
					send_message(chatid,mensajeid=309)
				else:
					s.chatSettings(chatid,idioma=content[1])
					chat.settings['idioma'] = content[1]
					chat.idioma = content[1]
					if(content[1] == 'en'):
					    send_message(chatid,mensajeid=310)
					elif(content[1] == 'es'):
					    send_message(chatid,mensajeid=311)

		elif(commandid == 11): #donar
			with open('privado/%s/mensajes/donar.txt' % (idioma),'r') as h:
				sm = h.read()
			send_text_imagen(chatid,mensajes[idioma][612],filename='imgs/donate.png',url='https://paypal.me/leyguistar')

			send_text_imagen(chatid,mensajes[idioma][613],filename='imgs/donate2.png',url='https://ko-fi.com/leyguistar')
			for line in sm.split('\n\n'):
				print(line)
				r = send_message(chatid,line)
				print(r)
				sleep(1)

		elif(commandid == 4): #app
			# send_message(chatid,mensajeid=555)
			# return
			if(len(content) < 2):
				send_message(chatid,mensajes[idioma][562].replace('\\','\n'))
			elif(content[1] == 'link'):
				send_message(chatid,mensajeid=563)
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
				send_message(chatid,mensajeid=564)
				send_message(chatid,'%s' % (code))
				send_message(chatid,mensajeid=565)
		elif('linkSnippetList' in extensions or 'http://aminoapps.com/' in allContent):
			send_message(chatid,mensajeid=566)
			if('linkSnippetList' in extensions):
				link = extensions['linkSnippetList'][0]['link']
			else:
				for c in content:
					if('http://aminoapps.com/' in c):
						link = c
			response = requests.get(f"{client.api}/g/s/link-resolution?q={link}", headers=aminoHeaders.Headers(sid=client.sid).headers)
			# r = client.get_from_code(content[1])
			js = json.loads(response.text)
			if(js['api:statuscode'] == 107):
				send_message(chatid,mensajeid=500)
				return
			extensions = js['linkInfoV2']['extensions']
			r = extensions.get('linkInfo',None)
			print(r)
			if(not bot['public'] and userid != bot['owner'] and userid != ley):
				send_message(chatid,'Soy un bot privado actualmente trabajando para ndc://x%d/user-profile/%s' % (comid,bot['owner'] ))
				# send_message(chatid,mensajeid=568)
				unaves = True
				for bot in bots.values():
					if(bot['public']):
						if(unaves):
							send_message(chatid,mensajeid=569)
							unaves = False
						send_message(chatid,'ndc://x%d/user-profile/%s' % (comid,bot['userid']))
				send_message(chatid,mensajeid=570)
				return

			if(not r):
				r = extensions.get('invitation',None)
				newComId = extensions.get('community',{}).get('ndcId')
				if(r):
					newComId = r['ndcId']
				if(not r and not newComId):
					send_message(chatid,mensajeid=571)
					return
				if(userid != bot['owner'] and userid != ley and newComId != leyworld):
					botsComunidad = s.loadBotsCommunity(newComId)
					botCount = len(botsComunidad)
					comunidad = comunidades.get(newComId)
					if(not botCount):
						send_message(chatid,)

					if(not comunidad):
						comunidad = s.loadComunidad(newComId)
						if(not comunidad):
							s.comunidad(newComId)
							comunidad = Comunidad(newComId)
						cominfo = client.get_community_info(newComId)
						comunidad.idioma = cominfo['primaryLanguage']
						s.comunidadIdioma(comid,comunidad.idioma)

						comunidades[newComId] = comunidad 

					maxBots = comunidad.bots 
					if(bot['userid'] not in botsComunidad):
						send_message(chatid,mensajeid=575)
						text = ''
						for bid in botsComunidad:
							b = bots[bid]
							text += '%s ndc://x%d/user-profile/%s\n\n' % (b['name'],newComId,b['userid'])
						send_message(chatid,text)
						return
					# else:
						# send_message(chatid,mensajeid=607,args=(newComId,client.profile.id))
						# new_sub_client = client.sub_client(newComId)
						# new_sub_client.follow(userid)

				if(r):
					r = client.join_community(newComId,r['invitationId'])
				else:
					r = client.join_community(newComId)
				if(r != 200):
					print(r)
					send_message(chatid,mensajeid=576)
					if(r['api:statuscode'] == 826):
						send_message(chatid,mensajeid=577)
				else:
					# s.comunidadesBots(newComId,client.profile.id)
					send_message(chatid,mensajeid=578)
					send_message(chatid,mensajeid=608,args=(newComId,client.profile.id))
					new_sub_client = client.sub_client(newComId)
					new_sub_client.follow(userid)
					js = sub_client.get_user_info(client.profile.id).json
					copy_profile(new_sub_client,js)
					if('avatarFrame' in js):
						frameid = js['avatarFrame']['frameId']
						r = new_sub_client.apply_frame(frameid,False)
						if(r != 200):
						  r = sub_client.purchase_frame(frameid,autoRenew=True)
						  print(r)
						  r = sub_client.apply_frame(frameid,False)
						print(r)

				return
			objectId = r['objectId']
			if(r['objectType'] == 12):
				if(objectId in bannedChats):
					text = mensajes[idioma][597] + '\n'
					razon = bannedChats[chatid]
					if(razon):
						text += mensajes[idioma][493] % (razon) + '\n'
					else:
						text += mensajes[idioma][494] + '\n'

					send_message(chatid,text)
					return
				com = r['ndcId']

				if(com in bannedComunidades and bot['public']):
					send_message(chatid,mensajeid=553)
					razon = bannedComunidades[com]
					if(razon):
						send_message(chatid,mensajeid=493,args=(razon))
					else:
						send_message(chatid,mensajeid=554)
					return						
				notJoin = False
				if(bot['public'] and com != leyworld):
					botsComunidad = s.loadBotsCommunity(com)
					botCount = len(botsComunidad)
					comunidad = comunidades.get(com)
					if(not comunidad):
						comunidad = s.loadComunidad(com)
						if(not comunidad):
							s.comunidad(com)
							comunidad = Comunidad(com)
						cominfo = client.get_community_info(com)
						comunidad.idioma = cominfo['primaryLanguage']
						s.comunidadIdioma(comid,comunidad.idioma)

						comunidades[com] = comunidad 

					maxBots = comunidad.bots 
					if(bot['userid'] not in botsComunidad):
						send_message(chatid,mensajeid=584)
						text = ''
						for bid in botsComunidad:
							b = bots[bid]
							text += '%s ndc://x%d/user-profile/%s\n\n' % (b['name'],com,b['userid'])
						send_message(chatid,text)
						return 
					else:
						notJoin = False
				sub_client.comId = com    
				if(not notJoin):
					rcom = client.join_community(com)
					print(rcom)
					if(rcom != 200):
						if(rcom['api:statuscode'] == 826):
							send_message(chatid,mensajeid=576)
							send_message(chatid,mensajeid=577)
							return
					else:
						js = sub_client.get_user_info(client.profile.id).json
						new_sub_client = client.sub_client(com)
						copy_profile(new_sub_client,js)
						if('avatarFrame' in js):
							frameid = js['avatarFrame']['frameId']
							r = new_sub_client.apply_frame(frameid,False)
							if(r != 200):
							  r = sub_client.purchase_frame(frameid,autoRenew=True)
							  print(r)
							  r = sub_client.apply_frame(frameid,False)
							print(r)
						pass
						# s.comunidadesBots(com,client.profile.id)
					# send_message(chatid,mensajeid=587)
					# return
				chatThread = get_chat_thread(r['objectId'],com,client,error=True,new=True)
				if(type(chatThread) == int ):
					if(chatThread == 230):
						send_message(chatid,mensajeid=588)
					elif(chatThread == 229):
						send_message(chatid,mensajeid=589)
					else:
						send_message(chatid,mensajeid=590)

				if(userid == ley or userid == chatThread['uid']):

					sub_client.comId = com
					s.botstate(1,0,comid,0,chatid)
					sub_client.join_chat(r['objectId'])

					send_message(botgroup,'tp de ndc://x%d/user-profile/%s' % (com,userid) +  
					    '\nA: ndc://x%d/chat-thread/%s' % (com,r['objectId']) )
					send_message(r['objectId'],mensajeid=488)
					
					send_message(chatid,mensajeid=591)
				else:
					send_message(chatid,mensajeid=592)
				sub_client.comId = comid
			else:
				send_message(chatid,mensajeid=593)
		elif(commandid in comandosReverseMap[idioma]):
			with open('privado/%s/mensajes/%s.txt' % (idioma,comandosReverseMap['es'][commandid]),'r') as h:
				sm = h.read()
			for line in sm.split('\n\n'):
				print(line)
				r = send_message(chatid,line)
				print(r)
				sleep(1)
		else:
			if(tipo == 103):
				send_message(chatid,mensajeid=594)

	except Exception as e:
	    PrintException()
ctipos = {}
s = Save()
votosBot = s.loadVotos()
s.close()
votantes = []
portadas = {
    'a7bd9971-b22b-4047-8d4a-bf9d00260e63': 'http://pm1.narvii.com/7868/194059eee17dd7eecc6cdf05a45783640781f320r1-890-1000v2_00.jpg',
    '40b5631c-fcc4-4f97-b490-0e5f22ab8654': 'http://pm1.narvii.com/7874/0bf4d50f0414d9426d73aa6c01ac657eea4b4f57r1-546-533v2_00.jpg',
    'cf33f0b3-2418-4684-abf0-5283625cb04a': 'http://pm1.narvii.com/7885/af8f2268da5f14cc447765fc947eb71b95f50a75r1-900-1000v2_00.jpg',
    '60eccd8a-75d6-4ff4-bab8-99451189e4c0': 'http://pa1.narvii.com/7889/199ed9c5a8330fd8e5c4f6c04a14bc27def15ab4r1-510-510_00.gif',
    '7ced383b-beb5-4d18-9503-5f1f73277496': 'http://pm1.narvii.com/7888/c9401876c954d6e29096290817d137a1dbdbb56br1-890-1000v2_00.jpg',
    '127538fc-e62d-40da-8150-a6aa053fe854': 'http://pm1.narvii.com/7881/0a011ee698d36a89160514fd98b0349b2a6c0f88r1-1480-1080v2_00.jpg',
    'c466caf9-3050-427b-bb67-4e4b20056c47': 'http://pa1.narvii.com/7878/e57a66a09e8432c883e56db3934cfca5608577cfr1-486-534_00.gif',
    'd6535c44-7e5f-4887-b861-9e0e5f5edb9d': 'http://pm1.narvii.com/7873/1c065ee55873679efcd93309d690aa74e9f1d726r1-1390-1000v2_00.jpg',
    'c5809bc4-4dd6-499b-add6-ac5f33170cc8': 'http://pm1.narvii.com/7879/389641b020588e7c9c5658564fc87179e3b7df36r1-850-790v2_00.jpg',
    'a23fffae-6486-434b-85f1-f31fa88d4643': 'http://pa1.narvii.com/7878/643c98a9079141d94a8826c161c6a745105237b3r1-890-1000_00.gif',
    '9d2b6433-e915-47cb-a6a6-748676c3f77c': 'http://pm1.narvii.com/7873/b61ae40afdec0ff7c62e79e3fd20bc67876df11ar1-2048-682v2_00.jpg',
    '4bb1af85-8365-4013-9771-e7fdeec5325e': 'http://pm1.narvii.com/7875/6cdcaa367a16ba6d57ab810f048a96bfab87a1cdr1-695-1030v2_00.jpg',
    '1a9bfb1c-bbee-4c3b-8da5-f40fea37dcfe': 'http://pm1.narvii.com/7875/44c25129e581afc9440b9bd54c63cc63328428c8r1-507-605v2_00.jpg',
    'ff3311a1-3bcb-4466-ab7f-04c4d0960cc7': 'http://pm1.narvii.com/7870/0ba35d7cf859500af88d4aa241fbba02f234702cr1-1242-1242v2_00.jpg'
    }
nombres = ['riamu', 'manami', 'rushia', 'aiko', 'natsuki', 'minato', 'rem', 'mei', 'misaki', 'kumi', 'kanna', 'davinci', 'kai', 'klee', 'kotomi', 'selenity', 'jasmine', 'loinki']
perfiles = {
    "Klee":"a7bd9971-b22b-4047-8d4a-bf9d00260e63",
    "Loinki":"40b5631c-fcc4-4f97-b490-0e5f22ab8654",
    "Minato":"cf33f0b3-2418-4684-abf0-5283625cb04a",
    "Kai":"60eccd8a-75d6-4ff4-bab8-99451189e4c0",
    "Aiko":"7ced383b-beb5-4d18-9503-5f1f73277496",
    "Selenity":"127538fc-e62d-40da-8150-a6aa053fe854",
    "Riamu":"c466caf9-3050-427b-bb67-4e4b20056c47",
    "Akashi":"d6535c44-7e5f-4887-b861-9e0e5f5edb9d",
    "Miranda":"c5809bc4-4dd6-499b-add6-ac5f33170cc8",
    "Zoe":"a23fffae-6486-434b-85f1-f31fa88d4643",
    "Kazashi":"9d2b6433-e915-47cb-a6a6-748676c3f77c",
    "Rem":"4bb1af85-8365-4013-9771-e7fdeec5325e",
    "Rushia":"1a9bfb1c-bbee-4c3b-8da5-f40fea37dcfe",
    "Davinci":"ff3311a1-3bcb-4466-ab7f-04c4d0960cc7"
    }

tipos_comandos = {}
tipos_comandos['es'] = ['ayuda/informacion','lider','dueño','utiles']

tipos_comandos['en'] = ['help/info','leader','owner','helpful']
cateroryids = {
	"manami":"9ad86575-f70a-415c-9a13-70482a5c4990",
	"mei":"d10bf989-66ef-4493-91a8-2705f5510342",
	"misaki":"0f3af05b-dc26-4886-83d1-c4e6ba428041",
	"kumi":"f6c4faaa-b1fb-4bd4-a98e-cbd187e85aca",
	"kanna":"c9b48e28-9c01-453e-87cd-d04b512ed319",
	"kotomi":"dcc1b562-2f63-4e6f-9832-1cdf204e1c08",
	"jasmine":"dd05310b-c88e-43d8-9a5f-66733f3b8bf4",
	"natsuki":"a9061044-ffb2-4d6e-b058-44503d5bffd4"
}
comandos = {}
blogsCache = {}
with open('privado/comandos.txt', 'r') as h:
    handler = h.read().split('\n')
    for line in handler:
        cl = line.split(' ')
        cl1 = int(cl[1])
        cl2 = int(cl[2])
        comandos[cl[0]] = (cl1,cl2)
        if(cl1 not in ctipos):
            ctipos[cl1] = []
        ctipos[cl1].append((cl1,cl[0]))
comandosIdioma = {}
comandosReverseMap = {}
comandosReverseMap['es'] = {}
comandosIdioma['es'] = {}
i = 1
with open('privado/es/comandos.txt','r') as h:
    for c in h.read().split('\n'):
        cs = c.split(' ')
        c = cs[0]
        e = int(cs[1])
        if(e):
            comandosIdioma['es'][c] = i 
            comandosReverseMap['es'][i] = c
        else:
            comandosIdioma['es'][c] = 0
            comandosReverseMap['es'][i] = 'null'

        i += 1
comandosReverseMap['en'] = {}
comandosIdioma['en'] = {}
backgroundImage = None
i = 1
with open('privado/en/comandos.txt','r') as h:
    for c in h.read().split('\n'):
        cs = c.split(' ')
        c = cs[0]
        e = int(cs[1])
        if(e):
            comandosIdioma['en'][c] = i 
            comandosReverseMap['en'][i] = c
        else:
            comandosIdioma['en'][c] = 0
            comandosReverseMap['en'][i] = 'null'
        i += 1
