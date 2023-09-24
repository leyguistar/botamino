#!/usr/bin/env python3
print("import amino")
import amino
print("import discord")
import discord
print("import os")
import os
print("import sys")
import sys
print("from collections import deque")
from collections import deque
print("import itertools")
import itertools
print("import mysql.connector")
import mysql.connector
print("import linecache")
import linecache
print("import traceback")
import traceback
print("import signal")
import signal
print("import threading")
import threading
print("import requests")
import requests
print("from contextlib import closing")
from contextlib import closing
print("from googletrans import Translator")
from googletrans import Translator
print("from pprint import pprint")
from pprint import pprint
print("import datetime")
import datetime
print("from save import Save")
from save import Save
print("from time import time")
from time import time
print("from time import sleep")
from time import sleep
print("import random")
import random
print("from user import User")
from user import User
print("from chat import Chat")
from chat import Chat
print("from mensaje import Mensaje")
from mensaje import Mensaje
print("from comando import Comando")
from comando import Comando
print("from tipType import TipType")
from tipType import TipType
print("from noticia import Noticia")
from noticia import Noticia
print("from programa import Programa")
from programa import Programa
print("import unicodedata")
import unicodedata
print("from jikanpy import Jikan")
from jikanpy import Jikan
print("import jikanpy")
import jikanpy
print("from unicodedata import normalize")
from unicodedata import normalize
print("import animelyrics")
import animelyrics
print("import pytz")
import pytz
print("from PIL import Image, ImageDraw, ImageSequence,ImageFont")
from PIL import Image, ImageDraw, ImageSequence,ImageFont
print("import io")
import io
print("import re")
import re
print("import subprocess")
import subprocess
print("import boto3")
import boto3
print("import ffmpeg")
import ffmpeg
print("import botocore.exceptions")
import botocore.exceptions
try:
	print("	import ujson as json")
	import ujson as json
except ImportError:
	print("	import json")
	import json
	print('warning ujson not installed, please install it because is faster than json')

print("import html2text")
import html2text
print("from urllib.parse import unquote")
from urllib.parse import unquote
print("from urllib.parse import quote")
from urllib.parse import quote
print("import urllib.request")
import urllib.request
print("import asyncio ")
import asyncio 
print("from gtts import gTTS")
from gtts import gTTS
print("import ssl")
import ssl
print("import socket")
import socket
print("from pybooru import Danbooru")
from pybooru import Danbooru
print("from pybooru import Moebooru")
from pybooru import Moebooru
print("from nsfw import picpurify,nudity,deepAI,nudeDetect")
from nsfw import picpurify,nudity,deepAI,nudeDetect
print("from youtube_search import YoutubeSearch as ys")
from youtube_search import YoutubeSearch as ys
print("import pafy")
import pafy
print("from intent import Intent")
from intent import Intent
print("from amino.lib.util import headers as aminoHeaders")
from amino.lib.util import headers as aminoHeaders
print("from botocore.exceptions import ClientError")
from botocore.exceptions import ClientError
print('librerias cargadas')
def getNickname(userid):
	if(userid == None):
		return ''
	if(userid in users):
		if(len(users[userid].alias.lstrip()) > 0):
			return users[userid].alias
		nick = sub_client.get_user_info(userid).nickname
		if(users[userid].nickname != nick):
			users[userid].nickname = nick
			users[userid].save()
		return nick
	else:
		return sub_client.get_user_info(userid).nickname

	return nick

def getBio(userid):
	return sub_client.get_user_info(userid).json['content']

def get_title(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['title']


def getNicknameCache(userid):
	if(userid == None):
		return ''
	if(userid in users):
		if(len(users[userid].alias.lstrip()) > 0):
			return users[userid].alias
		return users[userid].nickname
	else:
		return getNickname(userid)
def send_message(chatId,message,tp=None):
	if(not output):
		return
	if(tp == None):
		tp = tipoMensaje
	if(tp == 0):
		sub_client.send_message(message=(prefijo + message).replace('\n','\n' + prefijo), chatId=chatId,messageType=tp)	
	else:
		sub_client.send_message(message=message, chatId=chatId,messageType=tp)

def send_marco(chatid,mensaje,mup = 0,mdown = 0):
	if(not output):
		return
	m = marcos[mup][0] + '\n\n' + mensaje + '\n\n' + marcos[mdown][1]
	send_message(chatid,m)	

def send_reply(chatId,message,replyid):
	if(not output):
		return
	sub_client.send_message(message=message, chatId=chatId,replyTo=replyid)

def send_invocacion(chatId,mentionUserIds,message=""):
	if(not output):
		return
	sub_client.send_message(message=message, chatId=chatId,messageType=tipoMensaje,mentionUserIds=mentionUserIds)

def send_upload(chatid,embedImage):
	if(not output):
		return
	sub_client.send_message(chatId=chatid,embedBytes=embedImage)
def send_media(chatid,data=None,tipo=None,filename=None):
	if(not output):
		return
	if(filename):
		with open(filename,'rb') as h:
			data = h.read()
		tipo = 'imagen/' + filename[filename.rfind('.')+1:]
	if(not data):
		return
	link = None
	for i in range(3):
		try:
			link = client.upload_media(data=data,tipo=tipo)
			break
		except Exception as e:
			print('reintentando send media')
	if(link):
		sub_client.send_message(chatId=chatid,link=link)

def send_imagen(chatid,file):
	if(not output):
		return
	for i in range(3):
		r = sub_client.send_message(chatId=chatid,filePath=file)
		if(r == 200):
			break

def send_audio(chatid,file):
	if(not output):
		return
	sub_client.send_message(chatid,filePath=file,fileType='audio')
def send_sticker(chatid,stickerid):
	if(not output):
		return

	r = sub_client.send_message(chatId=chatid,stickerId=stickerid)
	if(r != 200):
		send_message(chatid,'Error enviando el sticker, posiblemente porque el bot no tiene amino +')

def send_gif(chatid,gif):
	if(not output):
		return
	sub_client.send_message(chatId=chatid,sendBytesGif=gif)

def send_link(chatid,link):
	if(not output):
		return
	for i in range(2):
		print(link)
		r = sub_client.send_message(chatId=chatid,link=link)
		if(r == 200):
			break
	else:
		img  = requests.get(link).content
		sub_client.send_message(chatid,embedBytes=img)
def get_host(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['author']['uid']

def get_backGround(chatid):
	thread = sub_client.get_chat_thread(chatid)
	return thread.json['extensions']['bm'][1]

def get_cohosts(chatid):
	thread = sub_client.get_chat_thread(chatid)
	try:
		return thread.extensions['coHost']
	except:
		return []

def borrarDeUsuario(chatid,userid):
	send_message(message='Borrando mensajes de ' + getNickname(userid), chatId=chatid)
	messageList = sub_client.get_chat_messages(chatId=chatid,size=200)  # Gets messages of each chat
	for uid, content, id in zip(messageList.author.id, messageList.content, messageList.messageId):
		print("id: " + uid)
		print("userid " + userid)
		if(uid == userid):
			sub_client.delete_message(chatId=chatid,messageId=id)
	#send_message(message='listo', chatId=chatid)
	
def borrarMedia(chatid):
	send_message(message='Borrando stickers e imagenes', chatId=chatid)
	messageList = sub_client.get_chat_messages(chatId=chatid,size=200)  # Gets messages of each chat
	for id, mediaValue in zip(messageList.messageId,messageList.mediaValue):
		print("id %s media %s" % (str(id),str(mediaValue)))
		if(mediaValue != None ):
			sub_client.delete_message(chatId=chatid,messageId=id)
	#send_message(message='listo', chatId=chatid)

def borrarN(chatid,n):
	send_message(message='Borrando ultimos ' + str(n) + ' mensajes', chatId=chatid)
	messageList = sub_client.get_chat_messages(chatId=chatid,size=n)  # Gets messages of each chat

	for id,content in zip(messageList.messageId,messageList.content):
		print("Borrando: " + str(content) )
		sub_client.delete_message(chatId=chatid,messageId=id)

def bienvenida(chatid,mensaje="",bn=0,mup=0,mdown=0,userid = None,nickname=None):
	if(nickname):
		send_message(message=marcos[mup][0] + '\n\n' + 
		'\n\nBienvenid@ ' + nickname + "\n\n" + mensaje + '\n\n' + marcos[mdown][1], chatId=chatid)	
	elif(not userid):
		if(mensaje == None):
			send_message(message=marcos[mup][0] + '\n\n' +
			bienvenidas[bn] + '\n\n' + marcos[mdown][1], chatId=chatid)
		else:
			send_message(message=marcos[mup][0] + '\n\n' +
			bienvenidas[bn] + 
			'\n\n' + mensaje+ '\n\n' + marcos[mdown][1], chatId=chatid)
	elif(users[userid].bienvenida != ""):
		send_message(message=marcos[mup][0] + 
		'\n\nHola ' + getNickname(userid) + "\n\n" + users[userid].bienvenida + '\n\n' + marcos[mdown][1], chatId=chatid)
	else:
		send_message(message=marcos[mup][0] + '\n\n' + 
		'\n\nBienvenid@ ' + getNickname(userid) + "\n\n" + mensaje + '\n\n' + marcos[mdown][1], chatId=chatid)

def despedir(chatid,message="",mup=0,mdown=0,userid = None):
	if(userid == None):
		send_message(message=marcos[mup][0] +
		'\n\nAdios ' + message + '\n\n' + marcos[mdown][1], chatId=chatid)

	else:
		send_message(message=marcos[mup][0] +
		'\n\nAdios ' + getNickname(userid) + "\n\n" + users[userid].despedida + '\n\n' + marcos[mdown][1], chatId=chatid)

def mostrarLetras(chatid,i=0,j=0):
	global continuarLetras
	continuarLetras = True
	if(i == j and i == 0):
		m = ""
		for l in bienvenidas:
			m += str(i) + '\n'
			m += l + '\n'
			i+=1
		send_message(message=m, chatId=chatid)
		return

	if(j==0):
		j = len(bienvenidas)
	while i < len(marcos):
		if(i > j):
			return
		if(not continuarLetras):
			return
		send_message(message=str(i), chatId=chatid)
		
		send_message(message=bienvenidas[i], chatId=chatid)
		i+=1
	continuarLetras = False

def mostrarMarcos(chatid):
	m = ""
	i = 0
	for l in marcos:
		m += str(i) + '\n'
		m += l[0] + '\n\n' + l[1] + '\n'
		i+=1
	send_message(message=m, chatId=chatid)
def mostrarAyuda(chatid,tipo='general'):
	mensaje = ''
	tipos = [i.replace('.txt','') for i in os.listdir('ayuda/')]
	if(tipo in comandos):
		
		text = 'Comando %s\nop: %d\ntipo: %s\n\n' % (tipo,comandos[tipo][0],tipos_comandos[comandos[tipo][1]] )
		if(os.path.exists('ayuda/comandos/%s.txt' % (tipo))):
			with open('ayuda/comandos/%s.txt' % (tipo)) as h:
				text += h.read()
		else:
			text += 'Todavia no hay ayuda para este comando'
		send_message(chatid,text)
	if(tipo not in tipos):
		if(tipo not in comandos):
			send_message(chatid,'no hay ayuda para ' + tipo)
		return
	with open('ayuda/' + tipo + '.txt', 'r') as handler:
		mensaje = handler.read()

	send_message(message=mensaje, chatId=chatid)

def mostrarJuegos(chatid):
	mensaje = ''
	with open('juegos.txt', 'r') as handler:
		mensaje = handler.read()
	mensaje += '\n\nJuegos actuales: '
	for i in juegos:
		mensaje += str(i) + ' '
	send_message(message=mensaje, chatId=chatid)


juegoPid = 0
def jugar(chatid,juego,debug=False):
	global juegoPid
	if(juego in juegos):
		send_message(chatid,'Iniciando juego %s espere' % (juego) )
		fileName = 'apa.py'
		if(juego == 'aa'):
			fileName = 'jikan_apa.py'
		elif(juego == 'trivia'):
			fileName = 'trivia.py'
		elif(juego == 'vor'):
			fileName = 'vor.py'
		elif(juego == 'retos'):
			fileName = 'retos.py'
		elif(juego == 'mafia'):
			fileName = 'asesino.py'
		if(serverSocket):
			comando = {"comando":"juego","juego":juego,"filename":fileName,"chatid":chatid,"comid":comid,"mensaje":tipoMensaje,"userid":leybot}
			serverSocket.send(json.dumps(comando).encode('utf-8'))
		else:
			commands = ["python3",fileName,chatid,juego,"comid=" + str(comid),"mensaje="+str(tipoMensaje),"userid="+str(leybot),"silent"]
			sub = subprocess.Popen(commands)
			del sub
	else:
		send_message(chatid,'No esta el juego ' + juego)
		return
	print('jugando ' + juego)


def repetir(chatid,m,n,l):
	global continuarRepetir
	continuarRepetir = True
	for i in range(n):
		if(not continuarRepetir):
			break
		if(l):
			send_link(chatid,link=m)
		else:
			send_message(chatid,m)

def searchYoutube(chatid,m):
	global cacheYoutube
	results = ys(m,20).to_dict()
	cacheYoutube = []
	n = 1
	text = 'Resultados:\n'
	for r in results:
		d = r['duration']
		if(type(d) == str):
			t = [int(x) for x in r['duration'].split(':')]
			i = 0
			d = 0
			for ti in t[::-1]:
				d += ti*60**i
				i+=1
		# print(d)
		if(d < 180):
			text += '%d. %s %s\n' % (n,r['title'],r['duration'])
			r['duration'] = d
			cacheYoutube.append(r)
			n+=1	
	if(cacheYoutube):
		text += 'ingrese un numero para elegir, c para cancelar'
		send_message(chatid,text)
	else:
		send_message(chatid,'no se encontraron resultados')
def send_youtube(chatid,n):
	global cacheYoutube
	youtubeList.append(cacheYoutube[n-1])
	cacheYoutube = []
	try:
		youtubelock.acquire()

		v = pafy.new(youtubeList.popleft()['id'])
		print('duration',v.duration)
		d = v.duration
		if(type(d) == str):
			t = [int(x) for x in d.split(':')]
			i = 0
			d = 0
			for ti in t[::-1]:
				d += ti*60**i
				i+=1
		
		print('duration',d)
		r = v.getbestaudio()

		print('best: ',r.bitrate,r.extension,r.get_filesize())
		audiostreams = v.audiostreams
		print('streams: ')
		for a in audiostreams:
			print(a.bitrate, a.extension, a.get_filesize())
		tn = str(r)
		path = '/tmp/' + r.filename
		if(not os.path.exists(path)):
			r.download(path)
		print('sending',path)
		if(d < 20):
			process = (ffmpeg
			           .input(path)
			           .output(f"{path}.aac", audio_bitrate="320k")
			           .overwrite_output()
			           .run_async(pipe_stdout=True)
			           )

			process.wait()
			send_audio(chatid,f"{path}.aac")
		else:
			send_audio(chatid,path)

	except Exception as e:
		send_message(chatid,'Ocurrio un error intentando obtener el audio por favor elija otro')
		PrintException()
	finally:
		youtubelock.release()

def killMinecraft(score,level):
	img = Image.open(imgdir + 'minecraft_death_score.png')
	d = ImageDraw.Draw(img)
	font = ImageFont.truetype('fonts/MinecraftRegular.otf',20)
	d.text((442,200),str(score),(63,63,21), font=font,align ="center")
	d.text((440,198),str(score),(255,255,85), font=font,align ="center")

	level = str(level)
	if(len(level) == 1):
		d.text((424,409),str(level),(0x47,0x18,0x18), font=font,align ="center")
		d.text((422,407),str(level),(0x7c,0x81,0x25), font=font,align ="center")
	else:
		d.text((414,409),str(level),(0x47,0x18,0x18), font=font,align ="center")
		d.text((412,407),str(level),(0x7c,0x81,0x25), font=font,align ="center")		
	return img

def killUser(chatid,userid):

	info = sub_client.get_user_info(userId=userid)
	img = killMinecraft(info.json['reputation'],info.json['level'])
	b = io.BytesIO()	
	img.save(b,format="png")
	send_message(message=getNickname(userid) + " fell out of the world", chatId=chatid)
	try:
		link = client.upload_media(data=b.getvalue())
		send_link(chatid,link)
	except:
		img.save('/tmp/' + chatid + '.png',format="png")
		send_imagen(chatid,'/tmp/' + chatid + '.png')


def cancelar(f = ''):
	global continuarMarcos,continuarLetras,continuarRepetir

	if(f == 'marcos'):
		continuarMarcos = False
	elif(f == 'letras'):
		continuarLetras = False
	elif(f == 'repetir'):
		continuarRepetir = False
	elif(f == ''):
		continuarLetras = False
		continuarMarcos = False
		continuarRepetir = False

def ship(chatid,u1,u2,l = 0):
    m = "💖💖💖💖💖💖💖💖💖💖💖💖\n\n"
    m+= getNickname(u1) + " 💑 " + getNickname(u2) + "\n\n"
    m+= "❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️"
    if(l > 0):
        sub_client.edit_chat(chatId=chatid,announcement=m,pinAnnouncement=True)
    send_message(chatid,m)
    path = 'interaccion/ship/'
    ipath = path + 'SFW/'
    lpath = path + 'SFWL/'
    imagenes = os.listdir(ipath)
    img = random.choice(imagenes)
    if(not os.path.exists(lpath + img) or time() > os.path.getmtime(lpath + img) + (3600*4)):
        link = good_upload(filename=ipath + img)
        if(link):
            with open(lpath + img,'w') as h:
                h.write(link)
        else:
            return
    else:
        with open(lpath + img,'r') as h:
            link = h.read()
    with open(path + 'mensajes.txt','r') as h:
        frases =  [line.rstrip().lower() for line in h]

    send_message(chatid,random.choice(frases) % (getNickname(u1),getNickname(u2)) )
    sub_client.send_message(chatid,link=link)

def gorrito(ori,gorrito,faces):
    f = Image.new('RGBA',ori.size,(0,0,0,0))
    f.paste(ori)
    i = 0
    si = False
    
    for face in faces:
        x, y, x2, y2 = face['bbox']
        w = x2 - x
        h = y2 - y
        if(face['score'] < 0.1):
            i+=1
            continue
        i+=1
        resized = gorrito.resize((int(w*1.5) ,int(h*1.1)) )
        print(resized.size)
        print(ori.size)
        print(x,y,w,h)
        f.paste(resized,(int(x)-int(w*0.01),int(y)-resized.size[1]+int(h/3) ),resized)
        si = True

    if(not si):
        send_message(chatid,'no pude encontrar ningun rostro anime')
        return    
    b = io.BytesIO()    
    f.save(b,format="png")
    try:
        link = client.upload_media(data=b.getvalue())
        print(link)
        send_link(chatid,link)
    except:
        f.save('/tmp/' + chatid + '.png',format="png")
        send_imagen(chatid,'/tmp/' + chatid + '.png')


def gemir(chatid,userid):
	send_message(chatid,'%s gime' % (getNickname(userid)))
	ahegaos = os.listdir('interaccion/1/gemir/')
	send_imagen(chatid,'interaccion/1/gemir/' + random.choice(ahegaos))


def jail(chatid,userid):
	info = sub_client.get_user_info(userId=userid)
	img = requests.get(info.icon).content
	im1 = Image.open(imgdir + 'carcel2_resize.jpg')
	im2 = Image.open(imgdir + 'jail_bars2.png')
	im3 = Image.open(io.BytesIO(img))
	loli = Image.open(imgdir + 'jail_loli.png')
	im1.paste(im3,(150,160))
	final_img = Image.new('RGBA',im1.size,(0,0,0,0))
	final_img.paste(im1,(0,0))
	# final_img.paste(im2,(0,0),mask=im2)
	final_img.paste(loli,(0,0),loli)
	b = io.BytesIO()	
	final_img.save(b,format="png")
	try:
		link = client.upload_media(data=b.getvalue())
		send_link(chatid,link)
	except:
		final_img.save('/tmp/' + chatid + '.png',format="png")
		send_imagen(chatid,'/tmp/' + chatid + '.png')
def cum(chatid,mediaValue):
	img = requests.get(mediaValue).content
	cum = Image.open(imgdir + 'cum.gif')
	perfil = Image.open(io.BytesIO(img))
	frames = []
	for frame in ImageSequence.Iterator(cum):
		f = Image.new('RGBA',perfil.size,(0,0,0,0))
		f.paste(perfil)
		fr = frame.convert("RGBA").resize(perfil.size)
		f.paste(fr,(0,0),fr)
		b = io.BytesIO()
		f.save(b, format="GIF")
		f = Image.open(b)
		frames.append(f)
	b = io.BytesIO()
	frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=80)
	try:
		link = client.upload_media(data=b.getvalue(),tipo='image/gif')
		print(link)
		send_link(chatid,link)
	except Exception as e:
		frames[0].save('/tmp/'+chatid+'.gif',format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=80)
		send_imagen(chatid,'/tmp/' + chatid + '.gif')

def patear(chatid,userid):
	info = sub_client.get_user_info(userId=userid)
	img = requests.get(info.icon).content
	patada = Image.open(imgdir + 'patada.gif')
	perfil = Image.open(io.BytesIO(img))
	# perfil = Image.open('imagenes/perfil.jpg')
	perfil = perfil.resize((80,80))
	# perfil2 = perfil.copy()
	frames = []
	positions = [(232,78),(190,100),(236,90),(57,125),(83,125),(1,185)]
	# positions2 = [(232,78),(201,100),(236,90),(57,125),(83,125),(1,185)]
	i = 0
	p = 0
	for frame in ImageSequence.Iterator(patada):
		if(i%2):
			i+=1
			continue
		f = Image.new('RGBA',frame.size,(0,0,0,0))
		f.paste(frame)
		if(p < len(positions) ):
			f.paste(perfil,positions[p])
			p+=1
		i+=1
		b = io.BytesIO()
		f.save(b, format="GIF")
		f = Image.open(b)
		frames.append(f)
	# final_img.show()
	b = io.BytesIO()
	# frames[0].save('/tmp/patear.gif', save_all=True, append_images=frames[1:],loop=0,duration=120)
	# return 'gifs/kiri.gif'
	frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:],loop=0)
	try:
		link = client.upload_media(data=b.getvalue(),tipo='image/gif')
		send_link(chatid,link)
	except Exception as e:
		frames[0].save('/tmp/' + chatid + '.gif',format="GIF", save_all=True, append_images=frames[1:],loop=0)
		send_imagen(chatid,'/tmp/' + chatid + '.gif')


def rip(chatid,userid):
	send_message(chatid,'R.I.P ' + getNickname(userid))
	# info = sub_client.get_user_info(userId=userid)
	# img = requests.get(info.icon).content
	# arr = np.asarray(bytearray(img), dtype=np.uint8)
	# s_img = cv2.imdecode(arr,-1)
	# l_img = cv2.imread("imagenes/rip4.png") 
	# x_offset=135
	# y_offset=400
	# l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
	# position = (x_offset,y_offset-50)
	# nick = getNickname(userid)
	# print('poniendo ' + nick)
	# print(nick)
	# res = (len(nick)/4)
	# # cv2.putText(
	# #      l_img, #numpy array on which text is written
	# #      nick, #text
	# #      position, #position at which writing has to start
	# #      cv2.FONT_HERSHEY_COMPLEX, #font family
	# #      2.8, #font size
	# #      (0, 0, 0, 255), #font color
	# #      3) #font stroke
	# data = cv2.imencode('.jpg', l_img)[1].tobytes()
	# print(type(data))
	# try:
	# 	send_media(chatid,data,'jpg')
	# except:
	# 	cv2.imwrite('/tmp/' + chatid + '.jpg',l_img)
	# 	send_imagen(chatid,'/tmp/' + chatid + '.jpg')

def matar(i=0):
	global checkingTips,apagando
	try:
		print('iniciado apagar')
		apagando = True 
		checkingTips = False
		if(os.path.exists('fifos/' + chatid + '.fifo')):
			os.remove('fifos/' + chatid + '.fifo')
		s.botstate(0,os.getpid(),comid,premium,chat.id)
		if(processId):
			s.rprocess(processId)
		print('deslogeando')
		print('saliendo')
		with open('final.log','a') as h:
			text = '\nse mando a apagar el chat en %s en %d\n' % (chatid,time())
			h.write(text)
		sys.stdout.flush()
		client.logout()
		exit(i)
		# os.kill(os.getpid(), signal.SIGKILL)	
	except Exception as e:
		PrintException()
		print('error apagando: ')
		print(e)
		os.kill(os.getpid(), signal.SIGKILL)	

def checkChatStatus(chatid):
	print(chatid)
	chat = sub_client.get_chat_thread(chatid)
	print(chat)
	host = chat.json['uid']
	cohosts = chat.json['extensions'].get('coHosts',[])
	status = chat.json['status']
	if(status == 10 or status == 9):
		exit()


def loadData():
	global chat,users,host,cohosts,client,sub_client,respuestas,comandosBienvenida,comandosDonacion,messageHeaders
	messageHeaders = aminoHeaders.Headers(sid=client.sid).headers
	s = Save(file=sqlFile)
	users = s.loadAllUsers()
	s.botstate(1,os.getpid(),comid,premium,chat.id)
	respuestas = loadRespuestas(chatid)
	opCustom = s.loadCustomOpsPremium(chatid)
                            
	# Es necesario actualizar el chat?
	# chat = s.loadChat(chat.id)
	try:
		sys.stdout.flush()
		chat.loadEvents()
		tips = chat.loadTips()
		chat.loadTipTypes()
		chat.loadComandos()
		chat.loadUserTags()
		comandosBienvenida = s.loadComandosBienvenida(chatid)
		chat.loadGoals()
		comandosDonacion = s.loadComandosDonacion(chatid)
		intents = loadIntents(chatid)
	except Exception as e:
		print('Error reseting',e)
		PrintException()

	try:
		chatThread = sub_client.get_chat_thread(chatid)
		host = chatThread.json['uid']
		cohosts = chatThread.json['extensions'].get('coHosts',[])
		status = chatThread.json['status']
		if(status == 10 or status == 9):
			matar()
		sub_client.send_active_obj()
	except Exception as e:
		PrintException()
		print(e)
		print('Intentando relogear')
		client.logout()
		client = amino.Client(nosocket=True)
		client.login(email=login[0],password=login[1])
		sub_client = client.sub_client(comid)
		messageHeaders = aminoHeaders.Headers(sid=client.sid).headers

def reloadData(t):
	while 1:
		sleep(t)
		loadData()
def thanksGif(gif,tipper,coins,font,mensaje,fontSize):
	im = Image.open('gifs/' + gif)
	h = im.height
	w = im.width
	font = ImageFont.truetype('fonts/' + font,fontSize)
	frames = []
	x = 0
	y = 0
	if(w/h > 1.5):
		text = 'Gracias' + tipper.lstrip() + '\n'
		if(coins==1.0):
			text += 'Por la moneda\n'
		else:
			text += 'Por las ' + str(int(coins) )
			text += ' monedas\n'
		x = 10
		y = 0
	else:
		text = 'Gracias\n' + tipper.lstrip() + '\n'
		if(coins==1.0):
			text += 'Por la moneda' + '\n'
		else:
			text += 'Por las ' + str(int(coins) ) + '\n'
			text += 'monedas\n'
		x = 0
		y = 10
	text += mensaje

	for frame in ImageSequence.Iterator(im):
	    # Draw the text on the frame
	    d = ImageDraw.Draw(frame)
	    d.text((x,y),text,font=font,align ="center")
	    del d
	    b = io.BytesIO()
	    frame.save(b, format="GIF")
	    frame = Image.open(b)

	    frames.append(frame)

	b = io.BytesIO()
	# frames[0].save('gifs/kiri.gif', save_all=True, append_images=frames[1:])
	# return 'gifs/kiri.gif'
	frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:])
	return b
def getGif(m):
    tenorapikey = "23TJ3291LB82"
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=10" % (m, tenorapikey))
    link = None
    if(r.status_code == 200):
        js = json.loads(r.text)
        media = random.choice(js['results'] )['media'][0]
        if(media['gif']['size'] < 4194304):
            r = requests.get(media['gif']['url'])
        else:
            r = requests.get(media['tinygif']['url'])
        for i in range(10):
            try:
                link = client.upload_media(data=r.content,tipo='gif')
                break
            except Exception as e:
                print('reintentando cargar gif')
                print(e)
    return link
def send_interaccion(chatid,comando,userid,usersid):
    path = 'interaccion/%s/' % (comando)
    ipath = path + 'SFW/'
    lpath = path + 'SFWL/'
    imagenes = os.listdir(ipath)
    if(usersid and os.path.exists(path + 'mensajes2.txt')):
        for u in usersid:
            img = random.choice(imagenes)
            if(not os.path.exists(lpath + img)  or time() > os.path.getmtime(lpath + img) + (3600*4)):
                link = good_upload(filename=ipath + img)
                print(link)
                if(link):
                    with open(lpath + img,'w') as h:
                        h.write(link)
                else:
                    continue
            else:
                with open(lpath + img,'r') as h:
                    link = h.read()
            with open(path + 'mensajes2.txt','r') as h:
                frases =  [line.rstrip().lower() for line in h]

            send_message(chatid,random.choice(frases).replace('@',comando[-1]) % (getNickname(userid),getNickname(u)) )
            sub_client.send_message(chatid,link=link)
    else:
        if(os.path.exists(path + 'mensajes1.txt')):
            img = random.choice(imagenes)
            if(not os.path.exists(lpath + img) or time() > os.path.getmtime(lpath + img) + (3600*4) ):
                link = good_upload(filename=ipath + img)
                print(link)
                if(link):
                    with open(lpath + img,'w') as h:
                        h.write(link)
                else:
                    return
            else:
                with open(lpath + img,'r') as h:
                    link = h.read()
            with open(path + 'mensajes1.txt','r') as h:
                frases =  [line.rstrip().lower() for line in h]
            send_message(chatid,random.choice(frases).replace('@',comando[-1]) % (getNickname(userid)))
            sub_client.send_message(chatid,link=link)
        else:
            send_message(chatid,'Debes mencionar a alguien')

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
    	h.write(str(time()))
    	h.write('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    	traceback.print_exc(file=h)
def checkTips(chat):
	global checkingTips,fakeDonar
	tips = chat.tips
	# client = amino.Client()
	# client.login(email=login[0],password=login[1])
	# sub_client = amino.SubClient(comId=comid,profile=client.profile)
	s = Save(file=sqlFile)
	sqlSaves['tips'] = s
	checkingTips = True
	start = 0
	size = 5
	while checkingTips:
		try:
			update = False
			response = requests.get(f"{sub_client.api}/x{sub_client.comId}/s/chat/thread/{chat.id}/tipping/tipped-users-summary?start={start}&size={size}")
			text = response.text
			n = text.find('"totalCoins":')
			if(n >= 0):
				sub_text = text[n+13:]
				coins = int(float(sub_text[:sub_text.find('}')]))
			# data= sub_client.get_tipped_users(size=5,chatId=chat.id)
			#pprint(vars(data))
			# print('coins',coins)
			# coins = data.totalCoins
			if(fakeDonar):
				coins += fakeDonar
				fakeDonar = 0
			if(coins <= chat.coins):
				if(response.elapsed.seconds == 0):
					sleep(1)
				continue
			print('nueva donacion registrada')
			donations = int(coins - chat.coins)
			lastTip = max(zip(data.author.id,[datetime.datetime.strptime(tt, '%Y-%m-%dT%H:%M:%SZ') for tt in data.lastTippedTime]),key=lambda item:item[1] )
			userid = lastTip[0]
			nick = getNickname(userid)
			print('el donador es ' + nick)
			tt = chat.getTipType(donations)

			tnick = unicodedata.normalize( 'NFKC', nick)
			if(tt != None):
				b = thanksGif(tt.gif,tnick,donations,tt.font,tt.mensaje,tt.fontSize)
				send_gif(chatid,b.getvalue())
			else:


				if(donations == 1.0):
					send_marco(chatid,'gracias ' + nick +' por la moneda',chat.mup,chat.mdown)	
				else:
					send_marco(chatid,'gracias ' + nick +' por las ' + str(donations).replace('.0','') + ' monedas',chat.mup,chat.mdown)
				for comando in comandosDonacion:
					if(donations >= comando[2] and donations <= comando[3]):
						customCommands.append((comando[1],host,[userid]))
			chat.coins = coins
			if(chat.goals):
				text = 'Falta:\n'
				for g in chat.goals.values():
					falta = g.monedasTotal - chat.coins
					if(falta == 1):
						text += '%d moneda para la meta de %d monedas ' % (falta, g.monedas)
						if(g.nombre):
							text += g.nombre
					elif(falta > 0):						
						text += '%d monedas para la meta de %d monedas ' % (falta, g.monedas)
						if(g.nombre):
							text += g.nombre
					text += '\n\n'
				if(text != 'Falta:\n'):
					send_marco(chatid,text,chat.mup,chat.mdown)
				ms = chat.goals.keys()
				for m in ms:
					goal = chat.goals[m]
					if(coins >= m):
						text = 'Se alcanzo la meta de %d monedas ' % (goal.monedas)
						if(goal.nombre):
							text += goal.nombre
						send_marco(chatid,text,chat.mup,chat.mdown)
						comando = goal.comando
						userid = goal.userid
						if(comando in chat.comandos):
							pprint(vars(chat.comandos[comando]) )
							for c in chat.comandos[comando].comandos.split('\0'):
								customCommands.append((c,host))
						chat.borrarGoal(m)
			if(chat.goals):
				anuncio = None
				if(ponerMetas & 2):
					print('poniendo metas')
					chatInfo = sub_client.get_chat_thread(chatId=chat.id)  # Gets information of each chat
					text = chatInfo.content
					anuncio = chatInfo.announcement
					if(text == None):
						text = ''
					extra = ''
					if(text.find('\n[uuuuuuuuui]\n') > -1):
						extra = text[text.rfind('\n[uuuuuuuuui]\n') + len('\n[uuuuuuuuui]\n'):]
					if(text.find('[uuuuuuuuuu]') > -1):
						text = text[:text.find('[uuuuuuuuuu]')]
					text += '\n[uuuuuuuuuu]'
					text += "\n[ci]◇☆★ⓜⓔⓣⓐⓢ★☆◆\n\n"
					for e in chat.goals:
						goal = chat.goals[e]
						nombre = ''
						if(goal.nombre):
							nombre = goal.nombre
						text += '\n[c]%s\n' % (marcos[chat.mup][0])
						text += '[ciub]%d monedas %s\n' % (goal.monedas,nombre)
						text += '[ci] faltan %d monedas\n' % (goal.monedasTotal - chat.coins)
						text += '\n[c]%s\n' % (marcos[chat.mdown][1])
						
					text += '\n[uuuuuuuuui]\n'
					text += extra
					sub_client.edit_chat(chatId=chatid,content=text)
				if(ponerMetas & 4):	
					if(not anuncio):
						anuncio = sub_client.get_chat_thread(chatId=chat.id).announcement			
					text = anuncio
					if(text == None):
						text = ''
					extra = ''
					marcaextra = '\n⁺˚*•̩̩͙✩•̩̩͙*˚⁺\n'
					letraMetas = '◇☆★ⓜⓔⓣⓐⓢ★☆◆'
					if(text.find(marcaextra) > -1):
						extra = text[text.rfind(marcaextra) + len(marcaextra):]
					if(text.find(letraMetas) > -1):
						text = text[:text.find(letraMetas)]
					else:
						text += '\n'
					text += "%s\n\n" % (letraMetas)
					for e in chat.goals:
						goal = chat.goals[e]
						nombre = ''
						if(goal.nombre):
							nombre = goal.nombre + ' '
						text += '\n%s\n' % (marcos[chat.mup][0])
						text += '%d monedas %s' % (goal.monedas,nombre)
						text += 'faltan %d monedas\n' % (goal.monedasTotal - chat.coins)
					text += marcaextra
					text += extra
					sub_client.edit_chat(chatId=chatid,announcement=text)



			lc = 0
			if(lastTip[0] in chat.tips):
				lc = chat.tips[lastTip[0]][0]
			continue
			#de aqui en adelante esta medio bug
			# chat.save()
			# chat.tips[lastTip[0]] = (lc + donations,lastTip[1])
			# chat.saveTips()
			actualizarDonaciones()
		except Exception as e:
			PrintException()
			print(e)
			if(debug):
				send_message(chatid,'Error en donaciones: ' + str(e))


def ping(chatid):
	data = {
		"type": 0,
		"content": 'pong!',
		"clientRefId": int(time() / 10 % 1000000000),
		"timestamp": int(time() * 1000)
	}
	data = json.dumps(data)
	response = requests.post(f"{client.api}/x{sub_client.comId}/s/chat/thread/{chatid}/message", headers=aminoHeaders.Headers(data=data,sid=client.sid).headers, data=data)
	t = json.loads(response.text)
	t = t['message']['createdTime']
	ping = datetime.datetime.strptime(createdTime, '%Y-%m-%dT%H:%M:%SZ')
	pong = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
	t = pong-ping
	text = f"Segundos en responder: {int(t.total_seconds())}s\n"
	st = str(response.elapsed)
	text += 'Tiempo en conectar %s' % (st[st.rfind(':')+1:])
	send_message(chatid,text)
def letra(id):
	html = urllib.request.urlopen('https://www.musica.com/letras.asp?letra=' + id).read().decode('utf-8')
	letra = html2text.html2text(html)
	rLetra = re.compile(r'\[\]\(https://i\.musicaimg\.com/im/a-menos\.svg\)\s(.*)_fuente:',re.DOTALL)
	r4 = re.compile(r'<title>(.*)</title>',re.DOTALL)
	l = rLetra.findall(letra)[0]
	title = r4.findall(html)[0]
	title = title[:title.rfind('|')] + '\n'
	l = title + l
	return l
def buscar(name):
	global cacheLetras
	text = html2text.html2text(urllib.request.urlopen('https://www.musica.com/letras.asp?t2=' + quote(name)).read().decode('utf-8'))
	r3 = re.compile(r'\(https://www.musica.com/letras.asp\?letra=(\d*)\)\|',re.DOTALL)
	ids = r3.findall(text)
	text = 'Resultados:\n'
	cacheLetras = ['0']
	for i in ids:
		letra = urllib.request.urlopen('https://www.musica.com/letras.asp?letra=' + i).read().decode('utf-8')
		r4 = re.compile(r'<title>(.*)</title>',re.DOTALL)
		title = r4.findall(letra)[0]
		title = title[:title.rfind('|')]
		text += title + ' (%s)\n' % (len(cacheLetras))
		cacheLetras.append(i)
	return text

def info(chatid,topic='bot'):
	if(premium > 0 and topic == 'bot'):
		topic = 'pbot'
	mensaje = ''
	topics = [i.replace('.txt','') for i in os.listdir('info/')]
	if(topic not in topics):
		send_message(chatid,'no hay informacion respecto a ' + topic)
		return
	with open('info/' + topic + '.txt', 'r') as handler:
		mensaje = handler.read()

	send_message(message=mensaje, chatId=chatid)
def aminoLogin(alias):
	login = s.loginInfo(alias=alias)
	client = amino.Client(nosocket=True)
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
	return client.sid

def sacarcoa(chat,userid):
	sid = aminoHeaders.sid
	aminoLogin('ley')
	sub_client.remove_cohost(userid,chat)
	aminoHeaders.sid = sid
def metercoa(chat,userid):
	sid = aminoHeaders.sid
	aminoLogin('ley')

	cohosts = get_cohosts(chat)
	if(userid not in cohosts):
		cohosts.append(userid)
	else:
		aminoHeaders.sid = sid
		return True
	r = sub_client.edit_chat(chat,coHosts=cohosts)
	aminoHeaders.sid = sid
	if(r == 200):
		return send_message(chat,'%s es coa ahora' % (getNickname(userid)))
	return send_message(chat,'Coas llenos')




def limpieza(chatid,tipo,condition,maxusers,userMessages):
	global cancelarLimpieza,seguirLimpiando
	cancelarLimpieza = False
	seguirLimpiando = False
	totalkick = 0
	retryCount = 0
	if(tipo == 'reputacion'):
		minrep =condition
		send_message(chatid,'sacando del chat todos los que tienen menos de %d de reputacion' % (minrep))
		for i in range(0,1000,25):
			print(i)
			userss = sub_client.get_chat_users(chatid,i)
			for rep,id in zip(userss.reputation,userss.id):
				if(id in cohosts or id == host or id == ley or id == leybot):
					continue
				if(cancelarLimpieza):
					break
				print('comparando %d < %d' % (rep,minrep))
				if(rep < minrep):
					print('sacando ' + id)
					retryCount = 0
					while( sub_client.kick(id,chatid,True) != 200):
						print('retrying')
						if(retryCount > 5):
							break
						retryCount += 1
					else:					
						totalkick += 1
					if(totalkick >= maxusers):
						cancelarLimpieza = True
					if(totalkick % 50 == 0):
						send_message(chatid,'Matados '+	str(totalkick) +' anfi ponga /seguir para continuar o /cancelar para cancelar')

						for i in range(60):
							sleep(1)
							if(seguirLimpiando):
								send_message(chatid,'Continuando limpieza')
								seguirLimpiando = False
								break
							if(cancelarLimpieza):
								send_message(chatid,'Cancelando limpieza')
								break
						else:
							send_message(chatid,'Terminando limpieza por falta de confirmacion')
							cancelarLimpieza = True
							break
			if(cancelarLimpieza):
				break

	elif(content[1] == 'actividad'):
		minrep = 0
		maxusers = 1000
		if(len(content) >= 3 and content[2].isdigit):
			minrep = int(content[2])
		if(len(content) >= 4 and content[3].isdigit):
			maxusers = int(content[3])
		send_message(chatid,'sacando del chat todos los que tienen menos de %d mensajes registrados' % (minrep))
		for i in range(0,1000,25):
			print(i)
			userss = sub_client.get_chat_users(chatid,i)
			for rep,id in zip(userss.reputation,userss.id):
				if(id in cohosts or id == host or id == ley or id == leybot):
					continue
				if(cancelarLimpieza):
					break
				print('agarrando total de mensajes')
				count = userMessages.count(id)
				print('comparando %d < %d' % (count,minrep))
				if(count < minrep):
					print('sacando ' + id)
					retryCount = 0
					while( sub_client.kick(id,chatid,True) != 200):
						print('retrying')
						if(retryCount > 5):
							break
						retryCount += 1
					totalkick += 1
					if(totalkick >= maxusers):
						cancelarLimpieza = True
					if(totalkick % 50 == 0):
						send_message(chatid,'Matados '+	str(totalkick) +' anfi ponga /seguir para continuar o /cancelar para cancelar')

						for i in range(60):
							sleep(1)
							if(seguirLimpiando):
								send_message(chatid,'Continuando limpieza')
								seguirLimpiando = False
								break
							if(cancelarLimpieza):
								send_message(chatid,'Cancelando limpieza')
								break
						else:
							send_message(chatid,'Terminando limpieza por falta de confirmacion')
							cancelarLimpieza = True
							break

			if(cancelarLimpieza):
				break
	send_message(chatid,'Matados %d usuarios' % (totalkick))

def ver(chatid,u):
	r = sub_client.get_user_info(u)
	js = r.json
	send_link(chatid,js['icon'])
	text = 'Informacion de usuario:\n\n'
	text += 'Nombre: %s\n' % (js['nickname'])
	if(u in users):
		text += 'Alias: %s\n' % (users[u].alias)
	text += 'Seguidores: %s\n' % (js['membersCount'])
	text += 'Siguiendo: %s\n' % (js['joinedCount'])
	text += 'Nivel: %s\n' % (js['level'])
	text += 'Reputacion: %s\n' % (js['reputation'])
	userTags = s.loadUserTags(u)
	texttag = 'Tags:\n'
	tagCount = 0
	if(u in chat.tags):
		for t in chat.tags[u]:
			if(chat.tags[u][t] != None):
				texttag += t + ':' + chat.tags[u][t] + '\n'
			else:
				texttag += t + '\n'
			tagCount += 1
	if(userTags != None):										
		for t in userTags:
			if(chat.tags[u][t] != None):
				texttag += t + ':' + chat.tags[u][t] + '\n'
			else:
				texttag += t + '\n'
			tagCount += 1
	if(tagCount):
		text += texttag

	send_message(chatid,text)

def upload_file_s3(file_name, object_name=None,bucket='leybot-amino-data'):
	if object_name is None:
	    object_name = file_name

	s3_client = boto3.client('s3')
	try:
	    response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL': 'public-read'})
	except ClientError as e:
	    print(e)
	    return False
	return True

def upload_s3(data,object_name,bucket='leybot-amino-data'):
	s3_client = boto3.client('s3')
	b = io.BytesIO(data)
	try:
	    response = s3_client.upload_fileobj(b, bucket, object_name,ExtraArgs={'ACL': 'public-read'})
	except ClientError as e:
	    print(e)
	    return False
	return True

def urlAmino(url):
	print(url)
	img_data = requests.get(url).content
	return good_upload(img_data,url[url.rfind('.')+1:])
async def sendDiscord(guildid,message):
	await dc.login(discordToken,bot=True)
	print('aqui vamos')
	guild = await dc.fetch_guild(guildid)
	channels = await guild.fetch_channels()
	channel = discord.utils.get(channels, name='amino')
	print(channel)
	if(channel == None):
		channel = discord.utils.get(channels, name='general')
	print(channel)
	if(channel == None):
		return
	await channel.send(message)
	await dc.logout()
def send_discord_guild(guildid,message):
		
	loop = asyncio.get_event_loop()
	loop.run_until_complete(sendDiscord(guildid,message))

async def discordLink(guildid):
	global discordInviteLink
	await dc.login(discordToken,bot=True)
	print('aqui vamos')
	guild = await dc.fetch_guild(guildid)
	channels = await guild.fetch_channels()
	channel = discord.utils.get(channels, name='amino')
	print(channel)
	if(channel == None):
		channel = discord.utils.get(channels, name='general')
	print(channel)
	if(channel == None):
		return
	link = await channel.create_invite()
	print(link)
	discordInviteLink = link
	await dc.logout()

def get_discord_link(guildid):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(discordLink(guildid))

def good_upload(data=None,tipo=None,filename=None):
    if(filename):
        with open(filename,'rb') as h:
            data = h.read()
        tipo = 'imagen/' + filename[filename.rfind('.')+1:]
    if(not data):
        return
    link = None
    for i in range(10):
        try:
            link = client.upload_media(data=data,tipo=tipo)
            break
        except Exception as e:
            print(e)
            print('reintentando upload')
    return link

def eraseMedia(chatid,m):
	r = s.loadMedia(chatid,m)
	if(not r):
		return False
	if(r[1] == 2):
		s3 = boto3.resource('s3')
		s3.Object('leybot-amino-data',r[0].strip('https://leybot-amino-data.s3.amazonaws.com/') ).delete()
	s.deleteMedia(m,chatid)
	return True
def deleteSave(user,m):
	r = user.loadSave(m)
							
	if(not r):
		return False
	if(r[1] == 2):
		s3 = boto3.resource('s3')
		s3.Object('leybot-amino-data',r[0].strip('https://leybot-amino-data.s3.amazonaws.com/') ).delete()
	user.deleteSave(m)
	return True

def actualizarEventos():
	# client = amino.Client()
	# client.login(email=login[0],password=login[1])
	# sub_client = amino.SubClient(comId=comid,profile=client.profile)
	s = Save(file=sqlFile)
	sqlSaves['eventos'] = s
	tiempoAnuncio = 0 
	tiempoDescripcion = 0
	try:
		while 1:
			if(chat.eventos):
				if(ponerEventos & 1 and time() > tiempoDescripcion):
					print('poniendo eventos en descripcion ')
					chatInfo = sub_client.get_chat_thread(chatId=chat.id)  # Gets information of each chat
					text = chatInfo.content
					anuncio = chatInfo.announcement
					if(text == None):
						text = ''
					extra = ''
					if(text.find('\n[ccccccccci]\n') > -1):
						extra = text[text.rfind('\n[ccccccccci]\n') + len('\n[ccccccccci]\n'):]
					if(text.find('[cccccccccc]') > -1):
						text = text[:text.find('[cccccccccc]')]
					tnow = pytz.timezone('UTC').localize(datetime.datetime.utcnow())
					# print('ahora si viene lo chido')
					if(chat.eventos):
						text += '\n[cccccccccc]'
						text += "\n[ci]🅿🆁🅾🆇🅸🅼🅾🆂 🅴🆅🅴🅽🆃🅾🆂:\n\n"
						# print(chat.eventos)
						for e in chat.eventos:
							text += '\n[c]%s\n' % (marcos[chat.mup][0])
							text += '[ciub]' + e + '\n'
							text += '[c]Descripcion: ' + chat.eventos[e][0] + '\n'
							dt = chat.eventos[e][1]
							tl = dt - tnow
							ts = str(tl)
							text += '[c]Horarios: \n'
							for tz in tzs:
								text += '[c]' + tz[tz.rfind('/')+1:] +': ' + dt.astimezone(pytz.timezone(tz) ).strftime("%m-%d %I:%M %p") + '\n'
							text += '[bc]Faltan aproximadamente: ' + ts[:ts.find(':')].replace('days','dias').replace('day','día') + ' horas\n'
							text +='\n[c]%s\n' % (marcos[chat.mdown][1])
						text += '\n[ccccccccci]\n'
						# print('editando chat')
						# print(text)
					text += extra
					sub_client.edit_chat(chatId=chatid,content=text)
					tiempoDescripcion = time()+(60*60)
				if(ponerEventos & 2 and time() > tiempoAnuncio):
					print('poniendo evento en anuncios')
					chatInfo = sub_client.get_chat_thread(chatId=chat.id)  # Gets information of each chat
					text = chatInfo.announcement
					if(text == None):
						text = ''
					extra = ''
					marcaextra = '\n◇☆★☆★☆★☆◆\n'
					letraEventos = '🅿🆁🅾🆇🅸🅼🅾🆂 🅴🆅🅴🅽🆃🅾🆂'
					if(text.find(marcaextra) > -1):
						extra = text[text.rfind(marcaextra) + len(marcaextra):]
					if(text.find(letraEventos) > -1):
						text = text[:text.find(letraEventos)]
					else:
						text += '\n'
					tnow = pytz.timezone('UTC').localize(datetime.datetime.utcnow())
					# print('ahora si viene lo chido')
					if(chat.eventos):
						text += "%s:\n\n" % (letraEventos)
						for e in chat.eventos:
							text += '' + e + '\n'
							text += 'Descripcion: ' + chat.eventos[e][0] + '\n'
							dt = chat.eventos[e][1]
							tl = dt - tnow
							ts = str(tl)
							text += 'Faltan: ' + ts[:ts.find('.')].replace('days','dias').replace('day','día') + ' horas\n'
							text +='\n%s\n' % (marcos[chat.mup][0])
						text += marcaextra
					text += extra
					sub_client.edit_chat(chatId=chatid,announcement=text)
					tiempoAnuncio = time()+60


			sleep(300)
	except Exception as e:
		print('error actualizando eventos ' + str(e))
		PrintException()
		if(debug):
			send_message(chatid,'error actualizando eventos ' + str(e))

def actualizarDonaciones():
	try:
		if(not ponerDonaciones):
			return
		chatInfo = sub_client.get_chat_thread(chatId=chat.id)
		text = chatInfo.content
		if(text == None):
			text = ''
		if(text.find('[iiiiiiiiii]') > -1):
			text = text[:text.find('[iiiiiiiiii]')]
		text += '\n[iiiiiiiiii]\n'
		tips = {k: v for k, v in sorted(chat.tips.items(), key=lambda item: item[1],reverse=True)}
		total = chat.coins
		keys = list(tips.keys())
		text +='[cbu]Donaciones\n\n'
		i = 1
		for tip in tips:
			text += '[c]%d. %s %.2f%% \n' % (i,getNicknameCache(tip),(tips[tip][0]/total)*100 )
			i+=1


		sub_client.edit_chat(chatId=chatid,content=text)
	except Exception as e:
		print('error actualizando donaciones ' + str(e))
		PrintException()
		if(debug):
			send_message(chatid,'error actualizando donaciones ' + str(e))

def checkFifo(chatid):
	global premium,freetime,startbotTime
	if(os.path.exists('fifos/' + chatid + '.fifo')):
		os.remove('fifos/' + chatid + '.fifo')
	os.mkfifo('fifos/' + chatid + '.fifo')
	fifo = open('fifos/' + chatid + '.fifo','r')
	print('checkeando fifo')
	while 1:
		text = fifo.read()
		if(text):
			print('fifo message: ' + text)
			if(premium and text == 'no premium'):
				freetime = (time() - startbotTime) + 300
				premium = 0
				send_message(chatid,'El bot dejo de ser premium\nQuedan 5 minutos')
			if(text == 'noticia'):
				send_message(chatid,'Nueva noticia en /noticias')
			if(text[0] == '['):
				userid = text[1:text.find(']')]
				comando = text[text.find('/')+1:].strip()
				comando = unicodedata.normalize( 'NFKC', comando)
				comando = comando.translate(transAkane)
				t = text[:text.find('/')]
				if('<' in t):
					mentions = t[t.find('<')+1:t.find('>')].split(',')
				else:
					mentions = []
				print(comando,userid)
				if(comando in chat.comandos):
					pprint(vars(chat.comandos[comando]) )
					for c in chat.comandos[comando].comandos.split('\0'):
						customCommands.append((c,userid))
				else:
					customCommands.append(('/' + comando,userid,mentions))
		else:
			sleep(1)

def getCat():
	link = None
	for i in range(10):
		try:
			text = json.loads(requests.get('https://api.thecatapi.com/v1/images/search').text)
			print(text)
			r = requests.get(text[0]['url'])
			print(r.status_code)
			link = client.upload_media(data=r.content)
			break
		except:
			print('reintentando cargar gato')
	return link

def invocar_a_todos(chatid):
	ids = []
	for i in range(0,1000,100):
		users = sub_client.get_chat_users(chatid,i,100)
		ids += users.id
		if(len(users.id) < 99):
			break
	if(ley in ids):
		ids.remove(ley)
	send_invocacion(chatid,ids,'@todos')

def buscarLoli(m=''):
	if(m):
		result = requests.get('https://lolibooru.moe/post.json?limit=100&tags=rating%3As+' + quote(m)).text
	else:
		result = requests.get('https://lolibooru.moe/post.json?limit=100&tags=rating%3As').text
	link = None
	if(result):
		result = json.loads(result)
		for i in range(10):
			try:
				r = random.choice(result)
				url = r[booruFileType]
				print(url)
				data = requests.get(url).content
				link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
				print(link)
				break
			except Exception as e:
				print(e)
				print('reintentando')
	return link


def buscarChica(m=''):
	if(m):
		result = requests.get('https://yande.re/post.json?limit=100&tags=rating%3As+' + quote(m)).text
	else:
		result = requests.get('https://yande.re/post.json?limit=100&tags=rating%3As').text
	link = None
	if(result):
		result = json.loads(result)
		for i in range(10):
			try:
				r = random.choice(result)
				url = r[booruFileType]
				print(url)
				data = requests.get(url).content
				link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
				print(link)
				break
			except Exception as e:
				print(e)
				print('reintentando')
	return link
def buscarSakuga(m=''):
	if(m):
		result = requests.get('https://www.sakugabooru.com/post.json?limit=100&tags=rating%3As+' + quote(m)).text
	else:
		result = requests.get('https://www.sakugabooru.com/post.json?limit=100&tags=rating%3As').text
	link = None
	if(result):
		result = json.loads(result)
		results = []
		for r in result:
			if(r['file_size'] < 1048576):
				results.append(r['file_url'])
		if(results):
			for i in range(10):
				try:
					r = random.choice(results)
					url = r['file_url']
					print(url)
					data = requests.get(url).content
					link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
					print(link)
					break
				except Exception as e:
					print(e)
					print('reintentando')
	return link
def buscarDanbooru(m=""):
	clientBooru = Danbooru('danbooru')
	result = clientBooru.post_list(limit=100,tags='rating:s' + m)
	link = None
	if(result):
		for i in range(10):
			try:
				r = random.choice(result)
				url = r['file_url']
				data = requests.get(url).content
				link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
				break
			except Exception as e:
				print(e)
				print('reintentando')
	return link

def buscarMoe():
	clientBooru = Moebooru('konachan')
	result = clientBooru.post_list(limit=100,tags='order:rank rating:s ')
	link = None
	if(result):
		for i in range(10):
			try:
				r = random.choice(result)
				url = r[booruFileType]
				data = requests.get(url).content
				link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
				break
			except Exception as e:
				print(e)
				print('reintentando')
	print(link)
	return link
def buscarMoeTag(tag):
	clientBooru = Moebooru('konachan')
	result = clientBooru.post_list(limit=100,tags='rating:s ' + tag)
	link = None
	if(result):
		for i in range(10):
			try:
				r = random.choice(result)
				url = r[booruFileType]
				data = requests.get(url).content
				link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
				break
			except Exception as e:
				print(e)
				print('reintentando')
	return link

def mostrarVoces(chatid):	
	global voces
	try:
		voces =  [ i['Id'] for i in boto3.client('polly',region_name='us-east-1').describe_voices()['Voices']]
		voces.append('google')
	except:
		voces = ['google']
	print(voces)
	text = 'Voces:'
	for v in voces:
		text += ' ' + v
	send_message(chatid,text)

def loadRespuestas(chatid):
	res = s.loadRespuestasChat(chatid)
	respuestas = {}
	for r in res:
		sre = re.sub(
		    r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
		    normalize( "NFD", r[0]), 0, re.I
			)
		mensaje = normalize('NFKC',sre).lower()
		
		respuestas[mensaje] = r[1].split('|')
	return respuestas
def loadIntents(chatid):
	print('cargando intents')
	intents = s.loadIntentsChat(chatid)
	print(intents)
	for intent in intents:
		comienzos = intents[intent].comienzos
		for c,i in zip(comienzos,range(len(comienzos))):
			sre = re.sub(
			    r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
			    normalize( "NFD", c), 0, re.I
				)
			c = normalize('NFKC',sre)
			comienzos[i] = c.lower()
		opciones = {}
		for o in intents[intent].opciones:
			sre = re.sub(
			    r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
			    normalize( "NFD", o), 0, re.I
				)
			newo = normalize('NFKC',sre)
			opciones[newo.lower()] = intents[intent].opciones[o]
		intents[intent].opciones = opciones
	print('terminando de cargar')
	print(intents)
	for i in intents.values():
		print(i.comienzos)
		print(i.respuestas)
		print(i.opciones)
	return intents

def topMessages(chatid,messages,m=3):
	messageCount = {}
	for u in messages:
		if(u in messageCount):
			messageCount[u] += 1
		else:
			messageCount[u] = 1
	tops = dict(sorted(messageCount.items(), key=lambda x: x[1],reverse=True) )
	print(tops)
	i = 1
	text = ''
	for u in tops:
		n = tops[u]
		if(n == 1):
			text += '%d. %s un mensaje\n' % (i,getNickname(u))
		else:
			text += '%d. %s %d mensajes\n' % (i,getNickname(u),n)
		i += 1
		if(i > m):
			break
	return text
		 
def waifux2(link):
	r = requests.post(
    "https://api.deepai.org/api/waifu2x",
    data={
        'image': link,
    },
    headers={'api-key': '849ac977-4054-42d2-9540-98b7d0827fd8'}
	)
	
	link =r.json()['output_url']
	data = requests.get(link).content
	return good_upload(data=data,tipo='image/' + link[link.find('.')+1:])

def strike(userid,n=1):
	if(userid == host):
		send_message(chatid,'No se le pueden dar strikes al anfitrion')
		return
	if(userid == ley):
		send_message(chatid,'jaja, buen intento')
		return
	if(userid not in strikes):
		strikes[userid] = n
	else:
		strikes[userid] += n
	count = strikes[userid]
	s.strike(chatid,userid,n)
	if(count >= maxStrikes):
		sub_client.kick(userid,chatid,False)
		send_message(chatid,'%s fue baneado por strikes' % (getNickname(userid)))
	else:
		if(count == 1):
			send_message(chatid,'%s tienes un strike %d mas y seras baneado' % (getNickname(userid),maxStrikes-count))
		elif(count):
			send_message(chatid,'%s tienes %d strikes %d mas y seras baneado' % (getNickname(userid),count,maxStrikes-count))


def nsfwThread(chatid,mediaValue,userid,id):
	r = picpurify(mediaValue)
	if(r == True):
		sub_client.delete_message(chatId=chatid,messageId=id)
		strike(userid)
	elif(r == None):
		r = nudeDetect(mediaValue)
		if(r != None and r > 0.9):
			sub_client.delete_message(chatId=chatid,messageId=id)
			strike(userid)

		elif(r == None):
			r = nudity(mediaValue)
			if(r != None):
				if(r >= 0.9):
					sub_client.delete_message(chatId=chatid,messageId=id)
					strike(userid)

			else:
				r = deepAI(mediaValue)
				if(r > 0.9):
					sub_client.delete_message(chatId=chatid,messageId=id)
					strike(userid)

def nsfw(chatid,mediaValue,userid,id):
	threadnsfw = threading.Thread(target=nsfwThread, args=(chatid,mediaValue,userid,id))
	threadnsfw.daemon = True
	threadnsfw.start()

def saveMediaSticker(chatid,m,stickerid):
	try:
		s.media(m,stickerid,3,chatid)
		send_message(chatid,'guardado como sticker')
	except:
		return False
	else:
		return True

def saveMedia(chatid,m,message):
	mediaValue = message.get('mediaValue',None)
	tipo = message['type']
	c = message.get('content',None)
	if(tipo == 3 and (mediaValue.endswith('.png') or mediaValue.endswith('.gif')) and sub_client.get_sticker_collection(message['extensions']['sticker']['stickerCollectionId']).collectionType != 2):
		return saveMediaSticker(chatid,m,message['extensions']['originalStickerId'])
	elif(mediaValue):
		ext = mediaValue[mediaValue.rfind('.')+1:]
		if(ext != 'jpeg' and ext != 'jpg' and ext != 'png' and ext != 'gif' and ext != 'aac'):
			send_message(chatid,'Solo se puede guardar imagenes, gifs o audios')
			return False
		else:										
			mediahd = mediaValue.replace('_00.','_uhq.')
			
			r = requests.get(mediahd)
			if(not r.ok):
				r = requests.get(mediaValue)
			img_data = r.content
			filename = mediaValue[mediaValue.rfind('/')+1:]
			path = mediaPath + filename
			upload_s3(img_data,path)
			try:
				s.media(m,'https://leybot-amino-data.s3.amazonaws.com/media/%s/%s' % (chatid,filename) ,2,chatid)
			except Exception as e:
				print(e)
				return False
			else:
				send_message(chatid,'guardado ' + m)
				return True

	elif(c):
		try:
			s.media(m,c,0,chatid)
		except Exception as e:
			print(e)
			return False
		else:
			send_message(chatid,'mensaje guardado')
			return True
	else:
		send_message(chatid,'No puedo guardar eso')
		return False

def pilImage(name):
    if(type(name) == str):
        if(name.startswith('http')):
            img = requests.get(name).content
            img = Image.open(io.BytesIO(img))
        else:
            img = Image.open(name)
    elif(type(name) == bytes):        
        img = Image.open(io.BytesIO(img))
    else:
        img = Image.open(name)
    return img

def pastepng(img,png):
    ori = img
    f = Image.new('RGBA',ori.size,(0,0,0,0))
    png = png.resize(ori.size)
    f.paste(ori)
    f.paste(png,(0,0),png)
    b = io.BytesIO()    
    f.save(b,format="png")
    try:
        link = client.upload_media(data=b.getvalue())
        print(link)
        send_link(chatid,link)
    except:
        f.save('/tmp/' + chatid + '.png',format="png")
        send_imagen(chatid,'/tmp/' + chatid + '.png')



def getMediaValues(userid,usersid,replyid):
	values = []
	mediaValue = None
	if(replyid):
		message = sub_client.get_message_info(chatid,replyid)
		mediaValue = message.json['mediaValue']
	if(mediaValue and len(usersid) == 1):
		values.append(mediaValue)		

	elif(usersid):
		for u in usersid:
			info = sub_client.get_user_info(userId=u)
			if(info.icon):
				values.append(info.icon)
	elif(userid):

		info = sub_client.get_user_info(userId=userid)
		if(info.icon):
			values.append(info.icon)

	return values

def tmpMedia(url):
	response = requests.get(url)
	if(response.status_code == 200):
		img = requests.get(url).content

		name = '/tmp/' + url[url.rfind('/')+1:]
		with open(name,'wb') as h:
			h.write(img)
		return name
	else:
		print(response.status_code)
		print(response.text)

def getFaces(filename):
	if(filename.startswith('http')):
		name = tmpMedia(filename)
	elif(not filename.startswith('/tmp')):
		name = '/tmp/' + filename[filename.rfind('/')+1:]
		with open(filename,'rb') as f1:
			with open('/tmp/' + name,'wb') as f2:
				f2.write(f1.read()) 
	else:
		name = filename
	args = ["/anime-face-detector/detectFaces.py", name]
	print(args)
	cmd = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = cmd.communicate()
	print(out)
	faces = json.loads(out.decode('utf-8'))
	return faces

def tutorial(nombre,fase):
	global idToReply
	content = ''
	with open('tutorial/' + nombre + '.txt','r') as h:
		content = h.read()
	fases = content.split('$\n')
	if(fase >= len(fases)):
		send_message(chatid,'Tutorial %s completado' % (nombre))
		return
	lines = fases[fase].split('\n')
	lines = [l for l in lines if l]
	for l in lines:
		if(l[0] == '/'):
			print('agregando')
			print(l)
			comandosTutorial.append(l)
		else:
			if(l[0] == '#'):
				l = l[1:]
			if('&' in l):
				l = l.replace('&','')
				res = sub_client.send_message(chatId=chatid,message=l,withResponse=True,messageType=0)
				idToReply = res['message']['messageId']
			else:
				send_message(chatid,l)
	if(comandosTutorial):
		send_message(chatid,'Ahora escribe los siguientes comandos')
		for c in comandosTutorial:
			if('^' in c):
				send_reply(chatid,c.replace('%','(como quieras)').replace('^',''),idToReply)
			else:
				send_message(chatid,c.replace('%','(como quieras)'))

def checkearEventos():
	while(1):
		if(chat.eventos):
			tnow = pytz.timezone('UTC').localize(datetime.datetime.utcnow())
			for e in chat.eventos:
				if(chat.eventos[e][1] <= tnow):
					print('evento ' + e + ' ocurriendo')
					if(chat.eventos[e][2]):
						for c in chat.comandos[chat.eventos[e][2]].comandos.split('\0'):
							customCommands.append((c,host) )
					chat.eventos.pop(e)
					break
		sleep(10)
def liberar(chatid,t):
	sleep(t*60)
	sub_client.edit_chat(chatid,viewOnly=False)

def reConnect(chatid):
	global serverConnected
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	hostname = 'leybot.leyguistar.com'
	context = ssl.create_default_context()

	sock = socket.create_connection((hostname,8443),timeout=3)
	sock.settimeout(None)
	ssock = context.wrap_socket(sock,server_hostname=hostname)  
	ssock.send(('{"instanceid":"%s","type":1,"chatid":"%s","pid":%d,"processid":%d}' % (instanceid,chatid,os.getpid(),processId)).encode('utf-8'))
	serverConnected = True
	return sock,ssock

def firstConnect(chatid):
	global serverConnected
	sock,ssock = reConnect(chatid)
	text = text = ssock.recv(1024).decode('utf-8')
	res = json.loads(text)
	if(res['comando'] == 'ok'):
		return sock,ssock
	elif(res['comando'] == 'kill'):
		os.kill(os.getpid(), signal.SIGALRM)
def listenServer(chatid,sock,ssock):
	global requestReset,serverConnected
	while True:
		try:
			if(not serverConnected):
				sock, ssock = reConnect(chatid)
				serverSocket = ssock
				print('conectado con el servidor')
			text = ssock.recv().decode('utf-8')
			print('recibido',text)
			if(not text):
				ssock.send('KA'.encode('utf-8'))
				continue
			message = json.loads(text)
			comando = message['comando']
			if(comando == "apagar"):
				chatid = message['chatid']
				send_message(chatid,'apagando bot')
				print('recibido apagar')
				os.kill(os.getpid(), signal.SIGALRM)
				return
			elif(comando == "reset"):
				requestReset = True
			elif(comando == "kill"):
				print('recibido kill')
				os.kill(os.getpid(), signal.SIGALRM)
			elif(comando == "ok"):
				print('recibido ok')
		except ConnectionRefusedError as e:
			# print(e)
			serverConnected = False
			serverSocket = None
			sleep(60)

		except BrokenPipeError as e:
			# print(e)
			serverConnected = False
			serverSocket = None
			sleep(60)
		except Exception as e:
			PrintException()
			serverConnected = False
			serverSocket = None
			if(debug):
				print('error conectando con el servidor, reintentando')
			sleep(60)

def terminarSorteo(m,tiempo=0):
	sleep(tiempo)
	if(tiempo and m not in sorteos):
		return
	nombre = None
	l = None
	if(len(sorteos) == 1):
		nombre = list(sorteos.keys())[0]
		l = sorteos[nombre]
	elif(len(sorteos) > 1 ):
		if(not m):
			send_message(chatid,'uso: /terminar [nombre del sorteo]')
			text = "Sorteos activos:\n"
			for sorteo in sorteos:
				text += "%s: %d usuarios\n" % (sorteo,len(sorteos[sorteo]))
			send_message(chatid,text)
		elif(m in sorteos):
			l = sorteos[m]
			nombre = m
		else:
			send_message(chatid,'No existe el sorteo %s' % (m))
	else:
		send_message(chatid,'No hay sorteos activos')
	if(nombre):
		if(l):
			u = random.choice(l)
			send_message(chatid,'Terminando %s\nEl ganador es %s' % (nombre,getNickname(u)))
		else:
			send_message(chatid,'Terminando %s no participo nadie' % (nombre))
		sorteos.pop(nombre)

def crono(t,c,u,activo):
	sleep(t)
	if(activo[0]):
		customCommands.append((c,u) )


def conectarBaseDeDatos(host='localhost'):
	global s
	if(s == None):
		s = Save(host=host)
	else:
		s.db.reset_session()
def handler(signum, frame):
	if(apagando):
		print('recivida signal matando, pero se esta apagando')
		return
	print('recivida signal matando')
	matar()
def actualizar(signum, frame):
	if(apagando):
		print('recivida signal matando, pero se esta apagando')
		return
	send_message(chatid,'Apagando bot por actualizaciones')
	matar()
def reiniciar(signum, frame):
	global s
	if(apagando):
		print('recivida signal matando, pero se esta apagando')
		return
	print('recibida señal de quit')
	print(type(premium))
	send_message(chatid,'reiniciando bot por actualizaciones')
	# os.system('./bot.py id %s bot log premium=%d comid=%s user=%s &' % (chat.id,premium,comid,userBot) )
	checkingTips = False
	subprocess.Popen(['python3'] + sys.argv)
	matar()


print('poniendo handlers de las signals')
#inicio
s = None #save 
signal.signal(signal.SIGALRM, handler) #handler para matar cuando nazca un nuevo bot
signal.signal(signal.SIGQUIT, reiniciar) #handler para matar cuando nazca un nuevo bot
signal.signal(signal.SIGTERM, actualizar) #handler para matar cuando nazca un nuevo bot




if(len(sys.argv) < 3):
	print("pon el alias o id del chat")
	exit(0)
if(sys.argv[1] != 'alias' and sys.argv[1] != 'id'):
	print('pon si es alias o id')
	exit(0)
if('silencio' in sys.argv):
	output = False
else:
	output = True
comid = '67'

teleport = False
if('tp' in sys.argv):
	teleport = True
premium = 1
sqlhost = None
sqluser = None
sqlpassword = None
remote = False
cache = True
nostart = False
userBot = None
userBotId = '7be24129-ff57-4e1f-b4ae-cf3d72fdbfe0'
if('SQLFILE' in os.environ):
	sqlFile = os.environ['SQLFILE']
else:
	sqlFile = 'default.set' 
print('leyendo arguments')
for i in sys.argv:
	if('comid=' in i):
		comid = i[6:]
	if('premium=' in i):
		premium = int(i[8:])
	if(i == 'nostart'):
		nostart = True
	if(i == 'nocache'):
		cache = False

	if('user=' in i):
		userBot = i[5:]
	if('userid=' in i):
		userBotId = i[7:]
	if('sql=' in i):
		sqlFile = i[4:]
print('conectando con la base de datos')
s = Save(file=sqlFile)
sqlSaves = {'general':s}
if(userBot):
	login = s.loginInfo(alias=userBot)
	userBotId = login[4]
else:
	login = s.loginInfo(id=userBotId)
print(userBotId)
botOwner = s.loadBot(id=userBotId)[2]
#login
print('logeando')
client = amino.Client(nosocket=True)
if(login[2] and login[3] + 3600 > time() and cache):
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

sub_client = amino.SubClient(comId=comid,client=client)
print('logeado')
dc = discord.Client()
discordToken = 'NzUyNjE5MjIzNTM2MzY5NjY2.X1aRRQ.ikxvup9x4EHUeKiwCdllCVxRBBE'



try:
	r = requests.get('http://169.254.169.254/latest/meta-data/instance-id',timeout=0.5)
except:
	instanceid = 'i-local'
else:
	instanceid = r.text
logPath = os.environ.get('LOGDIR','logs') + '/'

savesUrl = os.environ.get('SAVESURL','https://leybot-amino-data.s3.amazonaws.com/saves') + '/'

# savesdir = os.environ.get('SAVESDIR','saves') + '/'

imgdir = os.environ.get('IMGDIR','imgs') + '/'

print('logPath',logPath)
# print('savesDir',savesdir)
#load info
if(sys.argv[1] == 'id'):
	chatid = sys.argv[2]
	chat = s.loadChat(chatid)
	if(chat == None):
		r = sub_client.get_chat_thread(chatid)
		print('guardando chat ' + str(r.title) )
		ops = {}
		ops[''] = 3
		s.chat(chatid,r.json.get('title',''),chatid,0,0,0,'',ops,uid=r.json['uid'],comid=r.json['ndcId'] )
		chat = s.loadChat(chatid)
else:
	chat = s.loadChat(alias=sys.argv[2])
	if(chat == None):
		print('error chat no chat con ese alias')
		client.logout()
		exit(0)
	chatid = chat.id
#check in there is other instance of this bot and kill it
checkChatStatus(chatid)
respawning = False
if('respawn' in sys.argv):
	respawning = True
pprint(vars(chat))
#variables
apagando = False
errorCount = 0
tipoMensaje = chat.tipoMensaje
if(teleport):
	freetime = 3600*2
else:
	freetime = 3600
mediaUrl = os.environ.get('MEDIAURL','https://leybot-amino-data.s3.amazonaws.com/media') + '/' +chat.id + '/'
# mediaPath = os.environ.get('MEDIADIR','media') + '/' +chat.id + '/'
mediaPath = 'media/' + chat.id + '/'
# print('mediaPath',mediaPath)
# if(not os.path.exists(mediaPath) ):
# 	os.mkdir(mediaPath,0o777)
logPath = logPath + instanceid + '/'
if('log' in sys.argv):
	if(not os.path.exists(logPath)):
		os.mkdir(logPath)
	sys.stdout = open(logPath + chat.id + '.log', 'w')

print('entrando en set variables')
checkingTips = True
ponerEventos = 0
ponerDonaciones = False
eliminarNSFW = False
oldMessages = []
funados = []
blindados = []
cronos = []
spamText = []
comandosTutorial = []
traducirDetectarUsers = []
traducirUsers = []
goalsBorrar = []
cacheYoutube = []
comandosDonacion = []
usersSorteo = []
voces = ['google']
listas = {}
userYoutube = None
cosasLista = {}
stickers = {}
activeIntents = {}
sorteos = {}
faseTutorial = 0
maxStrikes = 3
sizeMessageRequest=2
nombreTutorial = ''
cacheLetras = ['0']
reloadTime = 600
voz = 'google'
ley = ''
leybot = client.profile.id
leychat = 'cc6857e6-be23-07bd-3198-c6d5d0740f70'
botgroup = '17ab60ec-0418-4c75-8ce3-fdb11613b201'
booruFileType = 'sample_url'

continuarLetras = True
continuarMarcos = True
continuarRepetir = False
rotisimo = False
secreto = False
spamImagenes = False
spamStickers = False
customCommand = False
discordInviteLink = None
requestReset = False
customCommands = deque([])
youtubeList = deque([])
youtubelock = threading.Lock()
cUserid = None
serverSocket = None
debug = False
replyid = None
replyuid = None
permitido = True
tvisualizacion = 0
tliberar = 0
processId = None
spamRepetidos = 0
onlyFans = False
seguirLimpiando = False
cancelarLimpieza = False
serverConnected = False
fakeDonar = 0
lastMessageId = ""
idToReply = None
ponerMetas = 1
lastMessageTime = time()
prefijo = '[c]'
startbotTime = time()
hardcoreComandos = ['cum','coger']
tipos_comandos = ['ayuda','admin','configuracion','diversion','interaccion','utiles','informacion','secreto','ley','chat']
transAkane = str.maketrans('αв¢∂єfgнιʝкℓмиñσρqяѕтυνωχуz','abcdefghijklmnñopqrstuvwxyz')
tzs = ('America/Caracas','America/Buenos_Aires',
'America/Bogota','America/Mexico_City','America/Lima',
'America/Tijuana','America/Santiago','Europe/Madrid')
temporadas = {'invierno':'winter','primavera':'spring','verano':'summer','otoño':'fall'}
dias = {'lunes':'monday','martes':'tuesday','miercoles':'wednesday','thursday':'jueves','viernes':'friday','sabado':'saturday','domingo':'sunday'}

#load from database
print('entrando en zona de carga')
sys.stdout.flush()
users = s.loadAllUsers()
chat.loadEvents()
tips = chat.loadTips()
chat.loadTipTypes()
chat.loadComandos()
chat.loadUserTags()
comandosBienvenida = s.loadComandosBienvenida(chatid)
chat.loadGoals()
comandosDonacion = s.loadComandosDonacion(chatid)
respuestas = loadRespuestas(chatid)
try:
	intents = loadIntents(chatid)
except Exception as e:
	print(e)
	PrintException()
	intents = {}
opCustom = s.loadCustomOpsPremium(chatid)
bienvenidas = s.cargarBienvenidas()
tiposDeNoticia = s.loadTiposDeNoticia()
programas = chat.loadProgramas()
chat.loadSettings()
if(chat.voz):
	voz = chat.voz
listas = s.loadListasChat(chatid)
strikes = s.loadStrikes(chatid)
settings = s.loadChatSettings(chatid)
eliminarNSFW = settings[5]
for l in listas:
	cosasLista[l] = s.loadCosasLista(l,chatid)
#get chat features
# kop = list(chat.ops.keys())
# for op in kop:
# 	if(chat.ops[op] == 3 and users[op].premium <= 0):
# 		chat.ops.pop(op)
host = get_host(chatid)
cohosts = get_cohosts(chatid)
data= sub_client.get_tipped_users(size=1,chatId=chat.id)
chat.coins = data.totalCoins
chat.name = get_title(chat.id)
chat.ops[host] = 3
chat.ops[ley] = 4
for ch in cohosts:
	if(host == ley):
		chat.ops[ch] = 3
	if(ch != leybot and ch != ley and ch not in chat.ops):
		chat.ops[ch] = 2
chat.save()
# chat.saveTips()
if(host == ley):
	ponerEventos = 3
	ponerMetas = 7
#cargar marcos
with open('marcos.txt', 'r') as handler:
	buf = [line.rstrip() for line in handler]
marcos = []
for i in range(0,len(buf),2):
	marcos.append((buf[i],buf[i+1]))
#cargar fuentes
with open('fonts/buenas.txt', 'r') as handler:
	fonts = [line.rstrip() for line in handler]
lastReload = time()


oldMessages = oldMessages + s.loadMessagesID(chat.id)


juegos = os.listdir('juegos')
juegos.remove('__pycache__')
juegos.remove('asesino')
juegos.remove('retos')
juegos.append('mafia')
juegos.sort()
interacciones = os.listdir('interaccion')
interacciones.remove('cum')
interacciones.remove('ship')
print('entrando en jikan y translator')

jikan = Jikan()
translator = Translator()
comandos = {}
libre = -1

if(chat.agradecer):
	checkingTips = True
else:
	checkingTips = False
prefijo = chat.prefijo
ponerMetas = chat.ponerMetas
ponerEventos = chat.ponerEventos

processId = s.process(1,__file__,chatid,int(comid),os.getpid(),instanceid)
print('entrando en creacion de hilos')

#threads
#thread tips
if(checkingTips):
	threadTips = threading.Thread(target=checkTips, args=(chat,))
	threadTips.daemon = True
	threadTips.start()
#thread eventos
threadEventos = threading.Thread(target=actualizarEventos, args=())
threadEventos.daemon = True
threadEventos.start()



threadReload = threading.Thread(target=reloadData, args=(600,))
threadReload.daemon = True
threadReload.start()

# cronosDaemon = threading.Thread(target=crono, args=(60,))
# cronosDaemon.daemon = True
# cronosDaemon.start()
# threadTips = threading.Thread(target=checkFifo, args=(chatid,))
# threadTips.daemon = True
# threadTips.start()
sock = None
ssock = None
# try:
# 	sock,ssock = firstConnect(chatid)
# except:
# 	print('fallo al conectar con el servidor')
# 	pass
threadTips = threading.Thread(target=listenServer, args=(chatid,sock,ssock))
threadTips.daemon = True
threadTips.start()


mensajes = deque([],maxlen=100)
ctipos = {}
with open('comandos.txt', 'r') as handler:
	for line in handler:
		cl = line.split(' ')
		cl1 = int(cl[1])
		cl2 = int(cl[2])
		comandos[cl[0]] = (cl1,cl2)
		if(cl2 not in ctipos):
			ctipos[cl2] = []
		ctipos[cl2].append((cl1,cl[0]))
for c in interacciones:
	comandos[c] = (0,4)    
	ctipos[4].append((0,c))

marca = ''
marcaPremium = ''
with open('marcas/marca.txt','r') as h:
	marca = h.read()
marcacom = marca
if(os.path.exists('marcas/marca%s.txt' % (comid))):
	with open('marcas/marca%s.txt' % (comid),'r') as h:
		marcacom = h.read()

with open('marcas/premium.txt','r') as h:
	marcaPremium = h.read()
marcaPremiumcom = marca
if(os.path.exists('marcas/premium%s.txt' % (comid))):
	with open('marcas/premium%s.txt' % (comid),'r') as h:
		marcaPremiumcom = h.read()

print('actualizando coas y revisando marca')
userMarca = False
if(userMarca):
	if(leybot in cohosts and marca != marcacom):
		chatInfo = sub_client.get_chat_thread(chatId=chat.id)  # Gets information of each chat
		chatContent = chatInfo.content
		if(chatContent != None):
			chatContent.replace(marca,marcacom)
		# permitido = True
		sub_client.edit_chat(chatId=chatid,content=chatContent)
	if(leybot in cohosts):
		chatInfo = sub_client.get_chat_thread(chatId=chat.id)  # Gets information of each chat
		chatContent = chatInfo.content
		modi = True
		if(premium):
			if(marca in chatContent):
				chatContent = chatContent.replace(marca,marcaPremium)
			elif(marcacom in chatContent):
				chatContent = chatContent.replace(marcacom,marcaPremiumcom)
			else:
				modi = False
		else:
			if(marcaPremium in chatContent):
				chatContent = chatContent.replace(marcaPremium,marca)
			elif(marcaPremiumcom in chatContent):
				chatContent = chatContent.replace(marcaPremiumcom,marcacom)
			else:
				modi = False
		if(modi):
			sub_client.edit_chat(chatId=chatid,content=chatContent)
try:
	voces =  [ i['Id'] for i in boto3.client('polly',region_name='us-east-1').describe_voices()['Voices']]
	voces.append('google')
except:
	voces = ['google']

print('uniendose a la comunidad y el chat')
client.join_community(comid)
sub_client.join_chat(chatid)

s.botstate(1,os.getpid(),comid,premium,chat.id)
print('enviando mensaje inicial')
if(output and not nostart):
	if(not respawning):
		if(premium > 0):
			if(teleport):
				with open('ayuda/inicial.txt') as h:
					text = h.read()
				send_message(chatid,text)
			else:
				send_message(chatid,'Iniciando bot\n Para informacion y ayuda:\n/info y /ayuda\n║▌│█║▌│ █║▌│█│║▌║\n★彡Bot hecho por Ley彡★')
		else:
			send_message(chatid,'Iniciando bot\nGratis\n Para informacion y ayuda:\n/info y /ayuda\n/tutorial para un tutorial\n║▌│█║▌│ █║▌│█│║▌║\n★彡Bot hecho por Ley彡★')
	else:
		send_message(chatid,'respawning')
sys.stdout.flush()
try:
	checkSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	checkSock.sendto(('{"chatid":"'+ chatid +'","result":"ok"}').encode('utf-8'), ('127.0.0.1', 10101) )
except Exception as e:
	print('no se pudo enviar un mensaje a checkBots')
	print(e)
messageHeaders =  aminoHeaders.Headers(sid=client.sid).headers
while True:
	try:
		# if(not premium and time() - startbotTime > freetime):
		# 	send_message(chatid,'se acabo el tiempo apagando bot\nLos juegos en curso se mantienen')
		# 	matar()
		if(requestReset):
			s.db.reset_session()
			loadData()
			requestReset = False
		if(sizeMessageRequest > 20):
			sizeMessageRequest = 20

		response = requests.get(f"{sub_client.api}/x{sub_client.comId}/s/chat/thread/{chatid}/message?v=2&pagingType=t&size={sizeMessageRequest}", headers=messageHeaders)
		text = response.text
		n = text.find('"messageId":')
		messageid = text[n+12:n+48]
		if(messageid == lastMessageId and not customCommands):
			# print('tiempo en obtener mensajes:',response.elapsed)
			if(response.elapsed.seconds == 0):
				sleep(1)
			continue
		lastMessageId = messageid
		jsonResponse = json.loads(text)

		messageList = jsonResponse['messageList']
		# messageList = sub_client.get_chat_messages(chatId=chatid,size=sizeMessageRequest,raw=True)['messageList']  # Gets messages of each chat
		sizeMessageRequest = 3
		for message in messageList:
			id = message['messageId']
			if id in oldMessages:
				if(customCommands):
					ccui = customCommands.popleft()
					content = ccui[0]
					userid = ccui[1]
					if(len(ccui) < 3):
						usersid = []
					else:
						usersid = ccui[2]
					if(len(ccui) > 3 and ccui[3]):
						content += ccui[3]
					i = 1
					for u in usersid:
						print(f'@{i}')
						content = content.replace(f'@{i}',getNickname(u))
						i+=1
					user = users[userid]
					print(userid,content)
					nickname = getNickname(userid)
					id = None
					tipo = None
					mediaValue = None
					createdTime = None
					replyid = None
					replyuid = None
					customCommand = True
					if(userid in chat.ops):
						opLevel = chat.ops[userid]
					else:
						continue	
					if(not content):
						continue
					if(content[0] != '/' and content[0] != '*'):
						send_message(chatid,content)
						continue


				else:
					continue
			else:
				sizeMessageRequest += 2
				lastMessageTime = time()
				nickname = message['author']['nickname']
				content = message['content']
				userid = message['uid']
				extensions = message['extensions']
				tipo = message['type']
				mediaValue = message['mediaValue']
				createdTime = message['createdTime']
				js = message

			if(not customCommand):
				if(len(oldMessages) > 200):
					oldMessages = oldMessages[180:]
				oldMessages.append(id)
			#borrar
				if(secreto):
					sub_client.delete_message(chatId=chatid,messageId=id)
				if(userid in funados):
					sub_client.delete_message(chatId=chatid,messageId=id)
				if(onlyFans):
					if(userid not in chat.ops and userid != leybot):
						sub_client.delete_message(chatId=chatid,messageId=id)
				if(spamText and content):
					for spam in spamText:
						if(spam in content):
							sub_client.delete_message(chatId=chatid,messageId=id)
							break
				if(spamImagenes):
					if(mediaValue and js['mediaType'] == 100 and tipo == 0):
						sub_client.delete_message(chatId=chatid,messageId=id)
				else:						
					if(eliminarNSFW and mediaValue and js['mediaType'] == 100 and tipo == 0 and mediaValue[-4:len(mediaValue)] != '.gif' and userid != leybot):
						nsfw(chatid,mediaValue,userid,id)
				if(spamStickers):
					if(tipo == 3):								
						sub_client.delete_message(chatId=chatid,messageId=id)
				if(spamRepetidos and content):
					if(len([i for i in mensajes if i.content == content]) >= spamRepetidos):
						sub_client.delete_message(chatId=chatid,messageId=id)


				if(tipo == 113):
					sub_client.delete_message(chatId=chatid,messageId=id)				
				mensaje = Mensaje(id,content,userid,nickname,createdTime.replace('T',' ').replace('Z',''),tipo,mediaValue,'',json.dumps(extensions),s = s)
				try:
					mensaje.save(chatid)
				except Exception as e:
					print('mensaje duplicado')
					continue
				mensajes.append(mensaje)
				if(userid not in users):
					print('agregando nuevo usuario ' + nickname)
					users[userid] = User(userid,nickname,s = s)
					users[userid].save()
				if(users[userid].alias != ""):
					nickname = users[userid].alias
				user = users[userid]
		
				print(nickname, content,mediaValue)  # Simple output with nickname and messages
				if(userid == leybot):
					continue
				if(tipo == 101):
					print("lanzando mensaje de bienvenida al nuevo user")
					for comando in comandosBienvenida.values():
						if(comando == '/recibir'):
							bienvenida(chatid,chat.mensaje,chat.bn,chat.mup,chat.mdown,userid)
						else:
							customCommands.append((comando,host,[userid]))
					if(chat.usersGoals):
						chatInfo = sub_client.get_chat_thread(chatId=chat.id)  # Gets information of each chat
						
						totalUsers = chatInfo.membersCount 
						for goal in chat.usersGoals.values():
							if(totalUsers >= goal.cantidad):
								text = 'Se alcanzo la meta de %d usuarios ' % (goal.cantidad)
								if(goal.nombre):
									text += goal.nombre
								send_marco(chatid,text,chat.mup,chat.mdown)
								comando = goal.comando
								userid = goal.userid
								if(comando in chat.comandos):
									pprint(vars(chat.comandos[comando]) )
									for c in chat.comandos[comando].comandos.split('\0'):
										customCommands.append((c,host))
								chat.borrarGoal(cantidad=goal.cantidad)
								break

				
				if(content == None):
					continue
				contentLower = content.lower()
				sre = re.sub(
			    r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
			    normalize( "NFD", contentLower), 0, re.I
				)
				contentLower = normalize('NFKC',sre)

				if(contentLower in respuestas):
					send_message(chatid,random.choice(respuestas[contentLower]).replace('[@]',getNickname(userid)),tp=0)
				if(len(content) < 100 and userid in activeIntents):
					intent = intents[activeIntents[userid]]
					sre = re.sub(
					    r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
					    normalize( "NFD", contentLower), 0, re.I
						)
					cl = normalize('NFKC',sre)
					for opcion in intent.opciones:
						p = cl.find(opcion)
						if(p >=0):
							if((p and cl[p-1].isalnum()) or (p+len(opcion) < len(cl) and cl[p+len(opcion)].isalnum()) ):
								continue
							print(opcion,cl)
							print('coincide')
							comando = intent.opciones[opcion]
							comando = comando.replace('[@]',getNickname(userid))
							comando = comando.replace('[o]',opcion)
							if(comando[0] != '/'):
								send_message(chatid,comando,0)
							else:
								customCommands.append((comando,host,[]))
							if(userid in activeIntents):
								activeIntents.pop(userid)
				if(len(content) < 100):
					for intentId,i in intents.items():
						salirIntentWhile = False
						for j in i.comienzos:
							cl = contentLower
							if(j in cl):
								activeIntents[userid] = intentId
								sre = re.sub(
								    r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
								    normalize( "NFD", cl), 0, re.I
									)
								cl = normalize('NFKC',sre)

								for opcion in intents[intentId].opciones:
									p = cl.find(opcion)
									if(p >=0):
										if((p and cl[p-1].isalnum()) or (p+len(opcion) < len(cl) and cl[p+len(opcion)].isalnum()) ):
											continue
										print(opcion,cl)
										print('coincide')
										comando = intents[intentId].opciones[opcion]
										comando = comando.replace('[@]',getNickname(userid))
										comando = comando.replace('[o]',opcion)
										if(comando[0] != '/'):
											send_message(chatid,comando,0)
										else:
											customCommands.append((comando,host,[]))
										salirIntentWhile = True
								if(salirIntentWhile):
									break
								send_message(chatid,random.choice(i.respuestas),0)
								salirIntentWhile = True
								break
						if(salirIntentWhile):
							break
				if(userYoutube):
					if(content == 'c'):
						userYoutube = None
						cacheYoutube = []
						send_message(chatid,'cancelando')
					elif(content.isdigit()):
						i = int(content)
						if(i > len(cacheYoutube) or i == 0):
							send_message(chatid,'%d no esta entre las opciones, cancelando' % i)
							cacheYoutube = []
							userYoutube = None
						else:
							tYoutube = threading.Thread(target=send_youtube, args=(chatid,i) )
							tYoutube.daemon = True
							tYoutube.start()

				if(userid in traducirUsers ):
					print('traduciendo normal')
					c = unicodedata.normalize( 'NFKC', content)
					if(c != content):
						send_message(chatid,getNickname(userid) + ': ' + c)
				if(userid in traducirDetectarUsers):
					print('traduciendo detectar')
					c = unicodedata.normalize( 'NFKC', content)
					c = translator.translate(c,dest='es')
					if(c != content):
						send_message(chatid,getNickname(userid) + ': ' + c.text)
											
				if(listas):
					for l in listas:
						for d in listas[l]:
							if(content.startswith(d)):
								s.cosasLista(l,userid,content[len(d):],chatid)
								cosasLista[l].append((userid,content[len(d):] ))
				if(content == '@todos'):
					threadTodos = threading.Thread(target=invocar_a_todos, args=(chatid,))
					threadTodos.daemon = True
					threadTodos.start()
				opLevel = libre
				if(userid in chat.ops):
					opLevel = chat.ops[userid]
				elif(libre >= 0):
					opLevel = libre
				else:
					opLevel = -1
					if(content == '/op'):
						send_message(chatid,'no tienes poder aqui')
						continue


				usersid = []
				if('mentionedArray' in extensions):
					for m in extensions['mentionedArray']:
						print('mencion a: ' + m['uid'])
						usersid.append(m['uid'])
				if('replyMessageId' in extensions):
					replyid = extensions['replyMessageId']
					replyuid = extensions['replyMessage']['uid']
				else:
					replyid = None
					replyuid = None
				if(not usersid and replyuid != None and replyuid != userid):
					usersid.append(replyuid)
			else:
				customCommand = False
			if(content[0] == '*' and content[-1] == '*' and userid not in funados):
				text = getNickname(userid) + ' ' + content[1:-1]
				send_message(chatid,text)
				continue
				
			content = content.replace('*yo*',getNickname(userid))
			for u,i in zip(usersid,range(1,len(usersid)+1)) :
				content.replace(f'@{i}',getNickname(u))
			if(content.find(" ") == -1):
				m = None
			else:
				m = content[content.find(" "):].lstrip()
			if(m == ""):
				m = None
			if(replyuid == leybot and content[0][0] != "/"):
				print('entrado')
				for c in comandos:
					print(c)
					p = content.find(c)
					if(p > 0):
						print(c,'esta en',content)
						if(usersid[0] == replyuid):
							print('limpiando uids')
							usersid = []
						content = '/' + content[p:]
						break
			if(content[0][0] == '/'):
				allContent = content
				content = str(content).split(" ")
				comando = content[0][1:]
				comando = unicodedata.normalize( 'NFKC', comando)
				comando = comando.translate(transAkane)
				if(comando in chat.comandos):
					pprint(vars(chat.comandos[comando]) )
					for c in chat.comandos[comando].comandos.split('\0'):
						print(c)
						customCommands.append((c,userid,usersid,m))
				elif(comando in interacciones):
					send_interaccion(chatid,comando,userid,usersid)
				elif(comando not in comandos):
					print('comando desconocido')
				elif(opLevel < comandos[comando][0]):
					if(comando == 'disponible'):
						text = "Comandos disponibles segun tu nivel de permisos:\n\n"
						text += 'Comandos de interaccion:'
						for c in interacciones:
							text += ' %s ' % (c)
						text += '\n\n'
						send_message(chatid,text)
					else:
						send_message(chatid,'no tienes permisos para usar este comando')
				else:
					if(not permitido and comando != 'marcar' and comando != 'apagar' and comando != 'sinmarca'):
						if(comando == 'sinmarca' and userid == ley):
							permitido = True
							continue
						chatInfo = sub_client.get_chat_thread(chatId=chat.id)  # Gets information of each chat
						chatContent = chatInfo.content
						print(chatContent)
						if(chatContent == None):
							chatContent = ""
						if(premium and marcaPremium not in chatContent and marcaPremiumcom not in chatContent):
							sub_client.send_message(chatId=chatid,message='Los comandos estan bloqueados\nPor favor copiar y poner el siguiente mensaje en la descripcion del chat para habilitar los comandos')
							sub_client.send_message(chatId=chatid,message=marcaPremium,messageType=0)
							if(leybot in cohosts):
								sub_client.send_message(chatId=chatid,message='Como el bot es co-anfitrion, /marcar pone la marca automaticamente al final de la descripcion del chat')
							continue

						elif(not premium and marca.lower() not in chatContent.lower() and marcacom.lower() not in chatContent.lower()):
							sub_client.send_message(chatId=chatid,message='Los comandos estan bloqueados\nPor favor copiar y poner el siguiente mensaje en la descripcion del chat para habilitar los comandos')
							sub_client.send_message(chatId=chatid,message=marca,messageType=0)
							if(leybot in cohosts):
								sub_client.send_message(chatId=chatid,message='Como el bot es co-anfitrion, /marcar pone la marca automaticamente al final de la descripcion del chat')
							continue
						else:
							permitido = True

					if(comando == "borrarU"): 
						if(usersid):
							for u in usersid:
								borrarDeUsuario(chatid,u)
						else:
							send_message(chatid,'Tienes que mencionar uno o varios usuarios con @')
					elif(comando == "borrarM"):
						borrarMedia(chatid)
					elif(comando == "borrarN"):
						if(len(content) < 2 or not content[1].isdigit()):
							send_message(chatid,'uso: /borrarN [n]: borra n mensajes del chat')
						else:
							borrarN(chatid,int(content[1]))
					elif(comando == "borrar"):
						if(replyid):
							sub_client.delete_message(chatId=chatid,messageId=replyid)
						else:
							send_message(chatid,'Tienes que mencionar el mensaje que quieres borrar')
					elif(comando == "ayuda"):
						if(len(content) == 1):
							mostrarAyuda(chatid)
						elif(len(content) == 2):
							mostrarAyuda(chatid,content[1])

					elif(comando == "letras"):
						continuarLetras = False
						if(len(content) == 2):
							threadLetras = threading.Thread(target=mostrarLetras, args=(chatid,int(content[1]) ))
						elif(len(content) > 2):
							threadLetras = threading.Thread(target=mostrarLetras, args=(chatid,int(content[1]),int(content[2])))
						else:
							threadLetras = threading.Thread(target=mostrarLetras, args=(chatid, ))	
						
						threadLetras.daemon = True

						threadLetras.start()
						#mostrarLetras(chatid)
					elif(comando == "marcos"):
						r = sub_client.start_chat([userid],message='')
						# r = client.start_chat([ley],'')
						print(r[0])
						# print(r[1])
						if(r[0] == 200):
						    userchat = r[1]['thread']['threadId']
						    print(userchat)
						    print(r[1])
						    mostrarMarcos(userchat)
						    send_message(chatid,'%s revisa tu privado para ver los marcos' % (nickname))
						else:
						    send_message(chatid,'Los marcos se envian al privado por favor escribele al bot para poder enviarte los marcos')
					elif(comando == "especial"):
						if(userid not in users):
							send_marco(chatid,m)
						else:
							if(m):
								sub_client.delete_message(chatId=chatid,messageId=id)
								send_marco(chatid,m,user.mup,user.mdown)
							else:
								send_message(chatid,'uso: /especial [mensaje]: hace que el bot muestre el mensaje que se indica con los marcos de ese usuario')
					elif(comando == "recibir"):
						if(usersid):
							for u in usersid:
								bienvenida(chatid,"",-1,chat.mup,chat.mdown,u)
						else:
							bienvenida(chatid,chat.mensaje,chat.bn,chat.mup,chat.mdown)
					elif(comando == "letraBienvenida"):
						if(len(content) < 2 or not content[1].isdigit()):
							send_message(chatid,'uso: letraBienvenida [n]: cambia la letra de la bienvenida')
						else:
							bn = int(content[1])
							if(bn < len(bienvenidas) and bn >= 0):
								chat.bn = bn
								chat.save()

					elif(comando == "marco"):
						if(len(content) == 2):
							mn = int(content[1])
							if(mn < len(marcos) and mn >= 0):
								chat.mup = mn
								chat.mdown = mn 
								chat.save()
						elif(len(content) == 3):
							mn = int(content[1])
							if(mn < len(marcos) and mn >= 0):
								chat.mup = int(content[1])
								chat.mdown = int(content[2])
								chat.save()
						else:
							send_message(chatid,'uso: /marco [n]: pone un marco para los mensajes del chat')
							
					elif(comando == "mensaje"):
						if(m == None):
							send_message(chatid,'uso: /mensaje [mensaje]: Pone un mensaje de bievenida para el chat')
							chat.mensaje = ""
						else:
							chat.mensaje = m
						chat.save()
					elif(comando == "kick"):
						for u in usersid:
							if(u == host):
								send_message(chatid,'no puedes sacar al anfi')
							elif(u in cohosts):
								send_message(chatid,'no puedes sacar a un co anfi')
							elif(u == ''):
								send_message(chatid,'no puedes a ley, ley esta rotisimo')
							else:
								sub_client.kick(u,chatid,True)
						if(rotisimo and userid == ley):						
							for u in usersid:
								sub_client.kick(u,chatid,True)

					elif(comando == "ban"):
						for u in usersid:
							if(u == host):
								send_message(chatid,'no puedes sacar al anfi')
							elif(u in cohosts):
								send_message(chatid,'no puedes sacar a un co anfi')
							elif(u == ley):
								send_message(chatid,'no puedes a ley, ley esta rotisimo')
							else:
								sub_client.kick(u,chatid,False	)
					elif(comando == "kill"):
						if(usersid):
							for u in usersid:
								killUser(chatid,u)
						else:
							send_message(chatid,'uso: /kill @: envia un mensaje de muerte para los usuarios con @')
					elif(comando == "op"):
						if(libre >= 0):
							send_message(chatid,'Durante el modo libre no se puede usar op')
							continue

						if(len(content) == 1):
							send_message(chatid,'tienes op %d' % (opLevel) )
						elif(not content[1].isdigit()):
							for u in usersid:
								if(u not in chat.ops):
									send_message(chatid,getNickname(u) + ' no es op')
								else:
									send_message(chatid,getNickname(u) + ' es op %d' % chat.ops[u])
						else:
							l = int(content[1])
							if(not usersid):
								text = 'op %d:\n' % (l)
								for u,opl in chat.ops.items():
									if(opl == l):
										text += getNickname(u) + '\n'
								send_message(chatid,text)

							else:
								if(l < opLevel or userid == ley):
									for u in usersid:
										if((u in chat.ops and opLevel <= chat.ops[u]) or u == leybot ):
											continue
										chat.ops[u] = l
									chat.save()
								else:
									send_message(chatid,'no tienes suficientes permisos')
					elif(comando == "deop"):
						if(libre >= 0):
							send_message(chatid,'Durante el modo libre no se puede quitar op')
							continue
						for u in usersid:
							if(u == host):
								send_message(chatid,'no puedes quitarle el op al anfi')
							elif(u == ley):
								send_message(chatid,'no puedes quitarle el op a ley, ley esta rotisimo')
							elif(u in cohosts and user.id != host):
								send_message(chatid,'Solo el anfi puede sacarle el op a un co anfi')
							else:
								if(u in chat.ops):
									if(opLevel > chat.ops[u] or userid == ley):
										chat.ops.pop(u)
						chat.save()
					elif(comando == "marcoE"):
						if(len(content) == 2):
							user.mup = int(content[1])
							user.mdown = int(content[1])
						elif(len(content) == 3):
							user.mup = int(content[1])
							user.mdown = int(content[2])
						else:
							send_message(chatid,'uso: /marcoE [n]: pone un marco personal para tus mensajes especiales')
						user.save()
					elif(comando == "juegos"):
						mostrarJuegos(chatid)
					elif(comando == "jugar"):
						if(len(content) < 2):
							send_message(chatid,'uso: /jugar [juego]: pone un juego')
							mostrarJuegos(chatid)
						else:
							jugar(chatid,content[1])
					elif(comando == "ship"):
						if(len(usersid) != 2):
							send_message(chatid,'Tienes que mencionar 2 usuarios')
						else:
							if(content[1].isdigit()):
								ship(chatid,usersid[0],usersid[1],int(content[1]))
							else:
								ship(chatid,usersid[0],usersid[1])
					elif(comando == "apagar"):
						send_message(chatid,'apagando bot')
						matar()
					elif(comando == "alias"):
						if(len(usersid) == 1 ):
							if(usersid[0] not in users):
								users[usersid[0]] = User(usersid[0],getNickname(usersid[0]),s = s)
							if(replyuid != usersid[0]):
								m = m[m.find('@') + len(nickname)+1:].lstrip()
							print("alias " + m)
							users[usersid[0]].alias = m
							users[usersid[0]].save()
						else:
							send_message(chatid,'uso: /alias @user [alias]: le pone un alias a un usuario')
									
					elif(comando == "despedir"):
						if(usersid ):
							for u in usersid:
								despedir(chatid,users[u].despedida,chat.mup,chat.mdown,u)
						else:
							despedir(chatid,"se les quiere",chat.mup,chat.mdown)
							
					elif(comando == "save"):
						r = ""
						if(replyid == None):
							send_message(chatid,"¿Que quieres guardar?")
						elif(m == None ):
							send_message(chatid,"Falta el nombre")	
							send_message(chatid,'uso: /save [nombre]: guarda el mensaje que estas citando')
						elif('/' in m):
							send_message(chatid,"el nombre no puede contener / ")	
							
						else:
							message = sub_client.get_message_info(chatid,replyid)
							content = message.json['content']
							mediaValue = message.json['mediaValue']
							t = message.json['type']
							if(t == 100):
								send_message(chatid,'mensaje eliminado')
							else:
								tipo = message.json['type']
								print(content,mediaValue)

								if(mediaValue != None):
									img_data = requests.get(mediaValue).content
									p = mediaValue[mediaValue.rfind('/')+1:]
									url = 'https://leybot-amino-data.s3.amazonaws.com/saves/%s/%s' % (userid,p)
									upload_s3(img_data,'saves/%s/%s' % (userid,p))
									r = user.addSavedMessage(m,url,2)
								elif(content != None):
									r = user.addSavedMessage(m,content,0)
								else:
									print('no me jodas')
								send_message(chatid,r)

					elif(comando == "load"):
						r = ""
						if(m == None):
							saves = {}
							for n,c,t in s.loadUserSaves(userid):
								saves[n] = (c,t)

							t = ""
							for n in saves:
								t += n + '\n'
							send_message(chatid,"Saves:\n" + t)	
						else:
							t = s.loadUserSave(m,userid)
							if(t):
								if(t[1] == 0):
									send_message(chatid,t[0])
								elif(t[1] == 1):
									send_link(chatid,link=t[0])
								elif(t[1] == 2):
									if(t[0].endswith('.aac') or t[0].endswith('.mp3')):
										path = '/tmp/' + t[0][t[0].rfind('/')+1:]
										if(os.path.exists(path)):
											send_audio(chatid,path)
										else:
											c = requests.get(t[0]).content
											with open(path, 'wb') as h:
												h.write(c)
											send_audio(chatid,path)


									else:
										link = urlAmino(t[0])
										send_link(chatid,link)
								elif(t[1] == 3):
									send_sticker(chatid,t[0])
							else:
								send_message(chatid,'No tienes ese load')
					elif(comando == "delete"):
						if(m != None):
							if(deleteSave(user,m)):
								send_message(chatid,'borrado ' + m)
							else:
								send_message(chatid,'no se encontro ' + m)

						else:
							send_message(chatid,'uso: /delete [nombre]: sirve para borrar un save')
					elif(comando == "erase"):
						if(m):
							if(eraseMedia(chatid,m)):
								send_message(chatid,'borrado ' + m)
							else:
								send_message(chatid,'No se encontro ' + m)

						else:
							send_message(chatid,'uso: /erase [nombre media]: elimina media del chat')							
					elif(comando == "repetir"):
						if(replyid != None):

							t = int(content[1])
							if(t > 100):
								send_message(chatid,'No se puede repetir algo mas de 100 veces')
							elif(opLevel < 3 and t > 10):
								send_message(chatid,'Solo el anfi puede repetir algo mas de 10 veces')
							else:
								message = sub_client.get_message_info(chatid,replyid)
								content = message.json['content']
								mediaValue = message.json['mediaValue']		
								continuarRepetir = True
								if(mediaValue != None):
									threadRepetir = threading.Thread(target=repetir, args=(chatid,mediaValue,t,1))	
								elif(content != None):
									threadRepetir = threading.Thread(target=repetir, args=(chatid,content,t,0))	
				
								threadRepetir.daemon = True

								threadRepetir.start()
						else:
							send_message(chatid,'uso: /repetir [n]: repite el mensaje que esta citando n veces')
					elif(comando == "tp"):
						if(m != None):
							r = client.get_from_code(m)
							if(r.objectType == 12):
								com = str(r.json['extensions']['linkInfo']['ndcId'])
								if(com != sub_client.comId and userid != ley):
									send_message(chatid,'Advertencia link de otra comunidad, preguntar a ley si se puede llevar el bot a esa comunidad')
								elif(userid == ley or userid ==  get_host(r.objectId)):
									client.join_community(com)
									sub_client.comId = com
									sub_client.join_chat(r.objectId)
									sub_client.comId = comid

									os.system('./bot.py id %s bot log comid=%s userid=%s &' % (r.objectId,com,leybot) )
									send_message(botgroup,'tp de ' + nickname + '\nA: ' + str(get_title(r.objectId)) )
								else:
									send_message(chatid,'Solo ley o el anfi del chat destino puede meter al bot en el chat destino')
						else:
							send_message(chatid,'uso: /tp [link del chat]: envia el bot a otro chat')
					elif(comando == "join"):
						client.join_community(comid)
						sub_client.join_chat(chatid)
					elif(comando == "bienvenida"):
						if(len(usersid) == 1 ):
							if(usersid[0] not in users):
								users[usersid[0]] = User(usersid[0],getNickname(usersid[0]),s = s)

							if(replyid != usersid[0]):
								m = m[m.find('@') + len(users[usersid[0]].nickname)+1:].lstrip()
							users[usersid[0]].bienvenida = m
							users[usersid[0]].save()	
						else:
							send_message(chatid,'uso: /bienvenida @user [mensaje bienvenida]: le pone un mensaje de bievenida a un usuario')
					elif(comando == "despedida"):
						if(len(usersid) == 1 ):
							if(usersid[0] not in users):
								users[usersid[0]] = User(usersid[0],getNickname(usersid[0]),s = s)

							if(replyid != usersid[0]):
								m = m[m.find('@') + len(users[usersid[0]].nickname)+1:].lstrip()
							users[usersid[0]].despedida = m
							users[usersid[0]].save()	
						else:
							send_message(chatid,'uso: /despedida @user [mensaje despedida]: le pone un mensaje de despedida a un usuario')

					elif(comando == "media"):
						if(not m):
							ts = s.loadMedia(chatid)
							if(not ts):
								send_message(chatid,"uso:\n/media [nombre] \nCarga o guarda media del chat")
							else:
								text = 'Media del chat:\n'
								for t in ts:
									text += t[0] + '\n'
								send_message(chatid,text)
						else:
							if(replyid):
								message = sub_client.get_message_info(chatid,replyid)
								saveMedia(chatid,m,message.json)

							else:
								t = s.loadMedia(chatid,m)
								print(t)
								if(t):
									if(t[1] == 0):
										send_message(chatid,t[0])
									elif(t[1] == 1): #image
										send_link(chatid,link=t[0])
									elif(t[1] == 2):
										if(t[0].endswith('.aac') or t[0].endswith('.mp3')):
											path = '/tmp/' + t[0][t[0].rfind('/')+1:]
											if(os.path.exists(path)):
												send_audio(chatid,path)
											else:
												c = requests.get(t[0]).content
												with open(path, 'wb') as h:
													h.write(c)
												send_audio(chatid,path)
										else:
											link = urlAmino(t[0])
											send_link(chatid,link=link)
											# send_imagen(chatid,mediaPath + t[0])
									elif(t[1] == 3):
										send_sticker(chatid,t[0])
								else:
									send_message(chatid,'No se encontro %s en este chat' % (m))
					elif(comando == "fondo" or comando == "fondos"):
						if(m == None):
							if(comando == "fondo"):
								print('sending fondo')
								send_link(chatid,link=get_backGround(chatid))
							else:
								ts = s.loadMedia(chatid)
								if(not ts):
									send_message(chatid,"No hay media guardada")
								else:
									text = 'Media del chat:\n'
									for t in ts:
										if(t[2] == 2 and not t[1].endswith('aac')):
											text += t[0] + '\n'
									send_message(chatid,text)
							
						else:
							t = s.loadMedia(chatid,m)
							print(t)
							if(t):
								filename = t[0]
								ext = filename[filename.rfind('.')+1:]
								if(t[1] != 2 or ext not in ['jpeg','jpg','png','gif']):
									send_message(chatid,'No puedes poner este fondo')
								else:
									link = urlAmino(filename)
									sub_client.edit_chat(chatId=chatid,
										backgroundImage=link)
							else:
								send_message(chatid,'no se encontro ese fondo')
					elif(comando == "pack"):
						m = allContent.split('\n')
						if(m[0].find(' ') == -1 ):
							t = "Packs:\n"
							for i in user.loadPacks():
								t += i + '\n'
							send_message(chatid,t)
						elif(len(m) > 1):
							nombre = m[0][m[0].find(' '):].lstrip()
							ps = []

							for p in m[1:]:
								print('agregando al pack: ' + p)
								if(user.loadSave(p) == None):
									send_message(chatid,p + ' no esta en tus saves')
								else:
									ps.append(p)
							r = user.addPack(nombre,ps)
							send_message(chatid,r)
						else:
							nombre = m[0][m[0].find(' '):].lstrip()

							if(user.loadPack(nombre) != None):
								for n in user.packs[nombre]:
									t = user.loadSave(n)
									if(t[1] == 0):
										send_message(chatid,t[0])
									elif(t[1] == 1):
										send_link(chatid,link=t[0])
									elif(t[1] == 2):
										send_imagen(chatid,t[0])
									elif(t[1] == 3):
										send_sticker(chatid,t[0])

							else:
								send_message(chatid,'no pack con ese nombre')
								
					elif(comando == "activarmodorotisimo"):
						if(userid == ley):
							send_message(chatid,'activando modo rotisimo para ley')
							rotisimo = True
						else:
							send_message(chatid,'solo ley puede activar el modo rotisimo')
					elif(comando == "random"):
						if(len(content) == 2):
							send_message(chatid,str(random.randint(1,int(content[1]))))
						elif(len(content) == 3):
							send_message(chatid,str(random.randint(int(content[1]),int(content[2]))))
						else:
							send_message('uso: /random [n1] [n2]: genera un numero random entre n1 y n2')
					elif(comando == "tipoMensaje"):
						if(len(content) == 2):
							if(content[1] == 'normal'):
								tipoMensaje = 0
								chat.saveTipoMensaje(0)
							elif(content[1] == 'especial'):
								tipoMensaje = 100
								chat.saveTipoMensaje(100)
							else:
								send_message(chatid,'uso: /tipoMensaje [normal|especial]')
						else:
							send_message(chatid,'uso: /tipoMensaje [normal|especial]: cambia los mensajes del bot')
					elif(comando == "disponible"):
						text = "Comandos disponibles segun tu nivel de permisos:\n"
						for ct in ctipos:
							if(ct >= 7):
								continue
							text += 'Comandos de %s:' % (tipos_comandos[ct])
							for c in ctipos[ct]:
								if(c[0] > opLevel):
									continue
								text += ' %s ' % (c[1])
							text += '\n\n\n'
						send_message(chatid,text)
					elif(comando == "recuperar"):
						if(content[1].isdigit()):
							n = int(content[1])
						else:
							n = 1
						lm = len(mensajes)
						for m in list(mensajes)[lm-1-n:lm-1]:
							if(m.mediaValue != None):
								send_link(chatid,link=m.mediaValue)
							elif(m.content != None):
								send_message(chatid,m.content)
					elif(comando == "revivir"):
						send_message(chatid,'invocando a la gente')
						for i in range(5):
							send_invocacion(chatid,cohosts + [host],'revivan gente')
					elif(comando == "output"):
						if(len(content) == 2):
							if(content[1] == 'on'):
								output = True
							elif(content[1] == 'off'):
								output = False
						else:
							send_message(chatid,'uso: /output [on|off]: controla los mensajes del bot, si esta apagado el bot seguira prendido pero sin enviar mensajes')

					elif(comando == "traducir"):
						if(replyid or usersid):
							if(replyid):
								message = sub_client.get_message_info(chatid,replyid)
								replyContent = message.json['content']
								if(content != None):
									replyContent = unicodedata.normalize( 'NFKC', replyContent)
									if(len(content) == 2 ):
										if(content[1] == 'ingles'):
											traduccion = translator.translate(replyContent,src='en',dest='es')
											send_message(chatid,traduccion.text)
										elif(content[1] == 'detectar'):
											traduccion = translator.translate(replyContent,dest='es')
											send_message(chatid,traduccion.text)
										elif(content[1] == 'nombre'):
											nom = sub_client.get_user_info(message.json['uid']).nickname
											
											send_message(chatid,unicodedata.normalize( 'NFKC', nom))
									else:
										send_message(chatid,replyContent)
							elif(usersid):
								if(len(content) >= 2 ):
									if(content[1] == 'detectar'):
										traducirDetectarUsers += usersid
									elif(content[1] == 'nombre'):
										for u in usersid:
											nom = sub_client.get_user_info(message.json['uid']).nickname
											send_message(chatid,unicodedata.normalize( 'NFKC', nom))
									else:
										traducirUsers += usersid
								else:
									traducirUsers += usersid

						else:
							text = 'uso: /traducir [ingles|detectar|nombre] : traduce algo de algun idioma a tipo de letra extraño a letras normales\n'
							text += '/traducir detectar @user: va a traducir al español todos los mensajes que @user envie\n'
							text += '/traducir @user: va a traducir a una letra normal todos los mensajes que @user envie\n'
							text += 'Para dejar de traducir a alguien /notraducir'
							send_message(chatid,text)
					elif(comando == "notraducir"):
						traducirUsers = []
						traducirDetectarUsers = []
						send_message(chatid,'Deteniendo traducir')
					elif(comando == "buscar"):
						con = allContent.split('\n')
						for i in range(5):
							try:
								if(len(content) <= 1):
									send_message(chatid,'error, no hay nada que buscar')
									break
								elif(content[1][:5] == 'anime'):
									text = 'Resultados: \n'
									search_result = jikan.search('anime', m[5:].lstrip(), page=1)
									for result in search_result['results'][:10]:
										text += result['title'] + ' (%d)\n' % (result['mal_id'])
									send_message(chatid,text.replace('\n','\n\n'))
								elif(content[1][:5] == 'manga'): 
									text = 'Resultados: \n'
									search_result = jikan.search('manga', m[5:].lstrip(), page=1)
									for result in search_result['results'][:10]:
										text += result['title'] + ' (%d)\n' % (result['mal_id'])
									send_message(chatid,text.replace('\n','\n\n'))
								elif(content[1][:9] == 'personaje' or content[1][:9] == 'character'):
									text = 'Resultados: \n'
									print(m)
									print(m[9:].lstrip())
									search_result = jikan.search('character', m[9:].lstrip(), page=1)
									for result in search_result['results'][:10]:
										text += 'nombre: ' +result['name'] + ' (%d)\n\n' % (result['mal_id'])
										if(len(result['anime']) > 0):
											text += 'anime: ' + result['anime'][0]['name'] + '\n'
										if(len(result['manga']) > 0):
											text += 'manga: ' + result['manga'][0]['name'] + '\n'
										text += '\n'
									send_message(chatid,text)
								else:
									text = 'Resultados: \n'
									search_result = jikan.search('anime', m, page=1)
									for result in search_result['results'][:10]:
										text += result['title'] + ' (%d)\n' % (result['mal_id']) 
									send_message(chatid,text.replace('\n','\n\n'))
							except jikanpy.exceptions.APIException as e:
								PrintException()
								pass
							else:
								break			

					elif(comando == "anime"):
						jikanError = True
						text = ''
						for i in range(5):
						    try:
						        if(m.isdigit()):
						            result = jikan.anime(int(m))
						        elif(m):
						            text = 'Resultados: \n'
						            search_result = jikan.search('anime', m[5:].lstrip(), page=1)
						            r = search_result['results'][0]
						            # print(result)
						            for result in search_result['results'][:10]:
						                text += result['title'] + ' (%d)\n' % (result['mal_id'])
						            result = r
						            send_message(chatid,text.replace('\n','\n\n'))
						            text = ''

						    except jikanpy.exceptions.APIException as e:
						        PrintException()
						    else:
						        text += 'Nombre: ' + result['title'] + '\n'
						        text += 'Descripcion: ' + translator.translate(result['synopsis'],src='en',dest='es').text + '\n'
						        text += 'Episodios: ' + str(result['episodes']) + '\n'
						        if('aired' in result):
						            text += 'Empezo el: ' + result['aired']['from'].split('T')[0] + '\n'
						            if(result['aired']['to']!= None):
						                text += 'Termino el: ' + result['aired']['to'].split('T')[0] + '\n'
						        img_data = requests.get(result['image_url']).content
						        mediaValue = client.upload_media(data=img_data)
						        send_message(chatid,text.replace('\n','\n\n'))
						        send_link(chatid,link=mediaValue)
						        jikanError = False
						        break
						if(jikanError):
						    send_message(chatid,'Error buscando el anime')

					elif(comando == "temporada"):
						if(len(content) != 3):
							text = 'uso: /temporada [año] [temporada]:\naño: [1962-2020]\ntemporada: '
							text += '[invierno|primavera|verano|otoño]\n'
							text += 'ejemplo: /temporada 2020 invierno'
							send_message(chatid,text)
						else:
							if(content[1].isdigit() and content[2] in temporadas):
								jikanError = True
								for i in range(5):
									try:
										temp = jikan.season(year=int(content[1]),season=temporadas[content[2]] )
									except jikanpy.exceptions.APIException as e:
										PrintException()
										print('error en jikan, intentando de nuevo')
										sleep(1)
									else:
										text = 'Animes:\n'
										for a in temp['anime']:
											text += a['title'] + ' (%d)\n\n' % (a['mal_id'])
										send_message(chatid,text)
										jikanError = False
										break
								if(jikanError):
									send_message(chatid,'Error buscando la temporada')
					elif(comando == "emision"):
						if(len(content) != 2):
							text = 'uso: /emision [dia] :\ndia: [lunes|martes|miercoles|jueves|viernes|sabado|domingo]\n'
							text += 'ejemplo: /emision lunes'
							send_message(chatid,text)
						else:
							if( content[1] in dias):
								jikanError = True
								for i in range(5):
									try:
										day = dias[content[1]]
										temp = jikan.schedule(day=day)
										# temp = jikan.season(year=int(content[1]),season=temporadas[content[2]] )
									except jikanpy.exceptions.APIException as e:
										PrintException()
										print('error en jikan, intentando de nuevo')
										sleep(1)
									else:
										text = 'Animes:\n'
										for a in temp[day]:
											text += a['title'] + ' (%d)\n\n' % (a['mal_id'])
										send_message(chatid,text)
										jikanError = False
										break
								if(jikanError):
									send_message(chatid,'Error buscando la temporada')


					elif(comando == "openings"):
						if(len(content) >= 2 ):
						    jikanError = True
						    for i in range(5):
						        try:
						            if(m.isdigit()):
						                result = jikan.anime(int(m))
						            else:
						                search_result = jikan.search('anime',m, page=1)
						                result = search_result['results'][0]
						                result = jikan.anime(result['mal_id'])

						            text = 'Openings: '+ result['title'] +'\n\n'
						        except jikanpy.exceptions.APIException as e:
						            PrintException()
						            sleep(1)
						        else:
						            text += '\n\n'.join(result['opening_themes'])
						            img_data = requests.get(result['image_url']).content
						            mediaValue = client.upload_media(data=img_data)
						            send_link(chatid,link=mediaValue)
						            send_message(chatid,text.replace('\n','\n\n'))
						            jikanError = False
						            break
						    if(jikanError):
						        send_message(chatid,'Error buscando')
						else:
						    send_message(chatid,'uso: /opening id: los openings del anime id')
					elif(comando == "ending"):
						if(len(content) >= 2 ):
						    jikanError = True
						    for i in range(5):
						        try:
						            if(m.isdigit()):
						                result = jikan.anime(int(m))
						            else:
						                search_result = jikan.search('anime',m, page=1)
						                result = search_result['results'][0]
						                result = jikan.anime(result['mal_id'])

						            text = 'Endings: '+ result['title'] +'\n\n'
						        except jikanpy.exceptions.APIException as e:
						            PrintException()
						            sleep(1)
						        else:
						            text += '\n\n'.join(result['ending_themes'])
						            img_data = requests.get(result['image_url']).content
						            mediaValue = client.upload_media(data=img_data)
						            send_link(chatid,link=mediaValue)
						            send_message(chatid,text.replace('\n','\n\n'))
						            jikanError = False
						            break
						    if(jikanError):
						        send_message(chatid,'Error buscando')

						else:
						    send_message(chatid,'uso: /ending id: los openings del anime id')
					elif(comando == "manga"):
						if(len(content) >= 2 ):
						    jikanError = True
						    text = ''
						    for i in range(5):
						        try:
						            if(m.isdigit()):
						                result = jikan.manga(int(m))
						            elif(m):
						                text = 'Resultados: \n'
						                search_result = jikan.search('manga', m, page=1)
						                r = search_result['results'][0]
						                print(r)
						                for result in search_result['results'][:10]:
						                    text += result['title'] + ' (%d)\n' % (result['mal_id'])
						                result = r
						                send_message(chatid,text.replace('\n','\n\n'))
						                text = ''

						        except jikanpy.exceptions.APIException as e:
						            PrintException()
						            sleep(1)
						        else:
						            text += 'Nombre: ' + result['title'] + '\n\n'
						            text += 'Descripcion: ' + translator.translate(result['synopsis'],src='en',dest='es').text + '\n'
						            if(result['chapters'] != None):
						                text += 'Capitulos: ' + str(result['chapters']) + '\n\n'
						            if('published' in result):
						                text += 'Empezo el: ' + result['published']['from'].split('T')[0] + '\n\n'
						                if(result['published']['to']!= None):
						                    text += 'Termino el: ' + result['published']['to'].split('T')[0] + '\n\n'
						            img_data = requests.get(result['image_url']).content
						            mediaValue = client.upload_media(data=img_data)
						            send_message(chatid,text)
						            send_link(chatid,link=mediaValue)
						            jikanError = False
						            break
						    if(jikanError):
						        send_message(chatid,'Error id no encontrado')
						else:
						    send_message(chatid,'uso: /manga id: da informacion de el manga con ese id (resultado de la busqueda)')

					elif(comando == "personaje"):
						if(len(content) >= 2 ):
						    jikanError = True
						    text = ''
						    for i in range(5):
						        try:
						            if(m.isdigit()):
						                result = jikan.character(int(m))
						            elif(m):
						                text = 'Resultados: \n'
						                search_result = jikan.search('character', m, page=1)
						                r = search_result['results'][0]
						                print(r)
						                for result in search_result['results'][:10]:
						                    text += 'nombre: ' +result['name'] + ' (%d)\n\n' % (result['mal_id'])
						                    if(len(result['anime']) > 0):
						                        text += 'anime: ' + result['anime'][0]['name'] + '\n'
						                    if(len(result['manga']) > 0):
						                        text += 'manga: ' + result['manga'][0]['name'] + '\n'
						                    text += '\n'
						                result = jikan.character(r['mal_id'])
						                send_message(chatid,text.replace('\n','\n\n'))
						                text = ''

						        except jikanpy.exceptions.APIException as e:
						            PrintException()
						            sleep(1)
						        else:
						            text += 'Nombre: ' + result['name'] + '\n\n'
						            text += 'Descripcion: ' + translator.translate(result['about'],src='en',dest='es').text + '\n\n'
						            img_data = requests.get(result['image_url']).content
						            mediaValue = client.upload_media(data=img_data)
						            send_message(chatid,text.replace('\\ n','').replace('\\',''))
						            send_link(chatid,link=mediaValue)
						            jikanError = False
						            break
						    if(jikanError): 
						        send_message(chatid,'Error id no encontrado')
						else:
						    send_message(chatid,'uso: /personaje id: da informacion de el personaje con ese id (resultado de la busqueda)')
					elif(comando == "lyrics"):
						try:
							lyric = animelyrics.search_lyrics(m, show_title=True)
							send_message(chatid,lyric)
						except animelyrics.MissingTranslatedLyrics as e:
							send_message(chatid,'eto no pude encontrar el anime')
						except animelyrics.NoLyricsFound:
							send_message(chatid,'eto... no pude encontrar la lyrica')
					elif(comando == "info"):
						if(len(content) == 2):
							info(chatid,content[1])
						else:
							info(chatid)
					elif(comando == "calendario" or comando == 'eventos'):
						tnow = pytz.timezone('UTC').localize(datetime.datetime.utcnow())
						viejos = []
						for e in chat.eventos:
							if(chat.eventos[e][1] < tnow):
								viejos.append(e)
						for e in viejos:
							chat.eventos.pop(e)
						if(not chat.eventos):
							send_message(chatid,'No hay eventos')
						else:
							send_message(chatid,"Proximos eventos: ")
							print(chat.eventos)
							for e in chat.eventos:
								text = e + '\n'
								text += 'Descripcion: ' + chat.eventos[e][0] + '\n'
								dt = chat.eventos[e][1]
								tl = dt - tnow
								ts = str(tl)
								text += 'Faltan: ' + ts[:ts.find('.')].replace('days','dias') + '\n'
								text += 'Horarios: \n'
								for tz in tzs:
									text += tz[tz.rfind('/')+1:] +': ' + dt.astimezone(pytz.timezone(tz) ).strftime("%m-%d %I:%M %p") + '\n'
								send_marco(chatid,text,chat.mup,chat.mdown)
					elif(comando == 'timezone'):
						if(len(content) == 1 or len(content) > 3):
							text = 'Hay 2 formas de poner tu horario:\n\n'
							text += '/timezone [timezone] donde directamente escribes tu zona horaria\n\n'
							text += '/timezone [mm-dd hh:mm]: pones directamente la hora que es alla y el bot te muestra los lugares con la misma hora, para que despues selecciones uno\n\n'
							text += '/timezone [n] con el numero del timezone obtenido al introducir tu fecha\n\n'
							send_message(chatid,text)
						elif(len(content) == 2):
							if(content[1].isdigit()):
								user.timezone = pytz.timezone(pytz.all_timezones[int(content[1])])
								user.save()
								send_message(chatid,'zona horaria: ' + str(user.timezone) )
							else:
								try:
									user.timezone = pytz.timezone(content[1])
									user.save()
									send_message(chatid,'zona horaria: ' + str(user.timezone) )
								except pytz.exceptions.UnknownTimeZoneError:
									send_message(chatid,'No existe ' + content[1])
						elif(len(content) == 3):
							text = 'Timezones con ese horario:\n'
							tt = content[1] + ' ' + content[2]
							for tz in pytz.all_timezones:
								if(tt == datetime.datetime.now(tz=pytz.timezone(tz)).strftime("%m-%d %H:%M")):
									text += str(tz) + ' (%d)' % (pytz.all_timezones.index(tz)) + '\n'
							send_message(chatid,text)
							print('eventos:')
							print(chat.eventos)

					elif(comando == "evento"):
						con = allContent.split('\n')
						if(user.timezone == None):
							send_message(chatid,getNickname(userid) + ' Necesitas user /timezone para poner tu zona horaria antes de poder usar este comando')
						elif (len(con) < 3):
							send_message(chatid,'uso: /evento mm-dd hh:mm\nNombre del evento\nDescripcion\ncomando (opcional)')
						elif(len(con) >= 3):
							if(len(con[0].split(' ')) != 3):
								send_message(chatid,'error en la fecha, no tiene el formato correcto')
							else:
								c = con[0].split(' ')
								tt = '20-' + c[1] + ' ' + c[2]
								print(tt)
								tnow = pytz.timezone('UTC').localize(datetime.datetime.utcnow())

								fecha = datetime.datetime.strptime(tt, '%y-%m-%d %H:%M')
								fecha = user.timezone.localize(fecha)
								if(fecha < tnow):
									r = 'Esa fecha ya paso'
								else:
									print('horario normal: ')
									print(fecha.strftime("%m-%d %H:%M"))
									print('UTC:')
									print(fecha.astimezone(pytz.timezone('UTC')).strftime("%m-%d %H:%M"))
									nombre = con[1]
									descripcion = con[2]
									if(len(con) == 4):
										comando = con[3]
										if(comando in chat.comandos):
											r = chat.createEvent(fecha,nombre,descripcion,comando,userid)
										else:
											r = 'Error creando el evento, el comando no esta entre los comandos del chat usar /comandos para ver los comandos del chat'
									else:
										r = chat.createEvent(fecha,nombre,descripcion)
								send_message(chatid,r)
					elif(comando == "revento"):
						chat.removeEvent(m)
					elif(comando == "asesino"):
						secreto = not secreto
					elif(comando == "hora"):
						tnow = pytz.timezone('UTC').localize(datetime.datetime.utcnow())
						text = 'Hora: \n'
						if(len(content) == 2 and content[1] == 'todas'):
							for tz in pytz.common_timezones:
								if('America' in tz):
									text += tz[tz.rfind('/')+1:] +': ' + tnow.astimezone(pytz.timezone(tz) ).strftime("%I:%M %p") + '\n'
						else:
							for tz in tzs:
								text += tz[tz.rfind('/')+1:] +': ' + tnow.astimezone(pytz.timezone(tz) ).strftime("%I:%M %p") + '\n'
							text += 'Para todas /hora todas'
						send_message(chatid,text)
					elif(comando == "crear"):
						ln = allContent.split('\n')
						con = ln[0].split(' ')
						if(len(con) != 2) :
							send_message(chatid,'uso: /crear [nombre del comando]\n descripcion abajo (opcional)')							
						elif(replyid == None):
							send_message(chatid,'Falta el mensaje que continue el comando, tiene que ser un comando que empiece con / o con ./')
						else:
							nombre = con[1].lower()
							descripcion = ""
							if(len(ln) >= 2):
								descripcion = '\n'.join(ln[1:])
							if(nombre in comandos):
								text = 'ya hay un comando con ese nombre'
							else:
								message = sub_client.get_message_info(chatid,replyid)
								print(message)
								content = message.json.get('content',None)
								mediaValue = message.json.get('mediaValue',None)
								if(not content and mediaValue):
									if(saveMedia(chatid,m,message.json)):
										text = chat.createComand(nombre,'/media %s' % (m),descripcion,userid)
									elif(saveMedia(chatid,m + ' comando',message.json)):
										text = chat.createComand(nombre,'/media %s' % (m + ' comando'),descripcion,userid)
									else:
										text = "Fallo al crear el comando ya hay media con ese nombre"
								elif(content):
									if(content[0:2] == './'):
										content = content[1:]
									if(content[0] == '/' or (content[0] == '*' and content[-1] == '*') ):
										text = chat.createComand(nombre,content,descripcion,userid)
									else:
										text  = 'Solo se pueden crear comandos que empiezen con / ./ o esten entre *'
							send_message(chatid,text)
					elif(comando == "agregar"):
						
						if(len(content) != 2):
							send_message(chatid,'uso: /agregar [nombre del comando]: agrega otro comando a un comando ya creado')							
						elif(replyid == None):
							send_message(chatid,'Falta el mensaje que se va a ejecutar')
						else:
							nombre = content[1]
							message = sub_client.get_message_info(chatid,replyid)
							content = message.json['content']
							if(content[0:2] == './'):
								content = content[1:]
							if(content[0] == '/' or (content[0] == '*' and content[-1] == '*') ):
								text = chat.addComand(nombre,content,userid)
							else:
								text = 'Solo se pueden crear comandos que empiezen con / ./ o esten entre *'
							send_message(chatid,text)
					elif(comando == "eliminar"):
						
						if(len(content) != 2):
							send_message(chatid,'uso: /eliminar [nombre del comando]: elimina un comando ')							
						else:
							send_message(chatid,chat.removeComand(content[1]))
					elif(comando == "comandos"):
						if(chat.comandos):
							text = 'Comandos creados del chat:\n'
							for c in chat.comandos:
								nick = getNickname(chat.comandos[c].userid)
								text += c
								if(nick != ''):
									text += ' por %s\n' % (nick)
								else:
									text += '\n'
								if(chat.comandos[c].descripcion != None and chat.comandos[c].descripcion != ''):
									text += 'Descripcion: %s\n' % (chat.comandos[c].descripcion )	
								text +='\n'				
							send_message(chatid,text)
						text = ''
						for ct in ctipos:
							if(ct >= 7):
								continue
							text += 'Comandos de %s:' % (tipos_comandos[ct])
							for c in ctipos[ct]:
								text += ' %s ' % (c[1])
							text += '\n\n\n'
						send_message(chatid,text)

					elif(comando == "funar"):
						if(usersid):
							for u in usersid:
								if(u not in blindados):
									funados.append(u)
								else:
									send_message(chatid,'no puedes funar a %s esta blindado' % (getNickname(u)))
						else:
							send_message(chatid,'uso: /funar @: borra todos los mensajes que envien los usuarios mencionados')
					elif(comando == "blindar"):
						if(usersid):
							blindados += usersid
						else:
							send_message(chatid,'uso /blindar @: sirve para impedir que funen a los usuarios mencionados')
					elif(comando == "olvidar"):
						if(usersid):
							blindados = [item for item in blindados if item not in usersid]
						else:
							send_message(chatid,'uso /olvidar @: sirve para olvidar a usuarios blindados')
					elif(comando == "perdonar"):
						if(usersid):
							funados = [item for item in funados if item not in usersid]
						else:
							send_message(chatid,'uso: /perdonar @: perdona la funa de los usuarios mencionados')
					elif(content[0][1:] == "crearTier"):
						if(replyid == None):
							send_message(chatid,"falta la imagen o gif")
						else:
							m = allContent.split('\n')
							if(len(m) < 2):
								send_message(chatid,'uso:\n/crearTier nombre\ndesde\n[mensaje]\n[tamaño de letra]\n[fuente]')
							else:
								nombre = m[0][10:].lstrip()
								desde = int(m[1].lstrip())
								mensaje = ''
								fontSize = 20
								font = fonts[0]
								if(len(m) > 2):
									sas = re.sub(
								        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
								        unicodedata.normalize( "NFD", m[2]), 0, re.I
								    	)
									mensaje = unicodedata.normalize('NFKC',sas)
								if(len(m) > 3):
									fontSize = int(m[3])
								if(len(m) > 4):
									if(len(fonts) < int(m[4])):
										font = fonts[int(m[4])] 
								message = sub_client.get_message_info(chatid,replyid)
								mediaValue = message.json['mediaValue']
								mediahd = mediaValue.replace('_00.','_uhq.')
								
								r = requests.get(mediahd)
								if(not r.ok):
									r = requests.get(mediaValue)
								img_data = r.content
								gif = mediaValue[mediaValue.rfind('/')+1:]

								with open('gifs/' + gif,'wb') as h:
									h.write(img_data)

								if(nombre == ''):
									send_message(chatid,'falta el nombre')
								elif(desde == ""):
									send_message(chatid,'falta desde que cantidad de monedas')
								elif(mediaValue == None):
									send_message(chatid,"Falta el gif")
								else:
									tt = chat.createTipType(nombre,desde,gif,font,mensaje,fontSize)
									send_message(chatid,tt)
									if('Creado' in tt):
										send_message(chatid,'Enviando gif de ejemplo')
										tt = chat.tipTypes[nombre]
										b = thanksGif(tt.gif,'ejemplo',desde,tt.font,tt.mensaje,tt.fontSize)
										send_gif(chatid,b.getvalue())

					elif(comando == "borrarTier"):					
						chat.removeTipType(m)
					elif(comando == "tiers"):
						text = "Tiers:\n"
						x = chat.tipTypes
						ts = {k: v for k, v in sorted(x.items(), key=lambda item: item[1].desde)}
						for t in ts:
							text += t + ': %d monedas\n' % (ts[t].desde)

						send_marco(chatid,text,chat.mup,chat.mdown)

					elif(comando == "libre"):
						if(len(content) > 1 and content[1].isdigit()):
							libre = int(content)
					elif(comando == "fuentes"):
						text = 'Fuentes:'
						i = 0
						for f in fonts:
							text += f.replace('.ttf','') + ' (%d)\n' % (i)
							i+=1
						send_message(chatid,text)
					elif(comando == "ponerEventos"):
						if(len(content) < 2 or not content[1].isdigit() or int(content[1]) not in range(4)):
							text = 'uso: /ponerEventos [0|1|2|3]:\n'
							text += '0. No pone los eventos'
							text += '1. Pone los eventos en la descripcion del chat\n'
							text += '2. Pone los eventos en los anuncios del chat\n'
							text += '3. Pone los eventos en la descripcion y los anuncios del chat'
							send_message(chatid,text)
						else:
							ponerEventos = int(content[1])
							chat.settings(ponerEventos=ponerEventos)

					elif(comando == "le"):
							text = getNickname(userid) + ' ' 
							if(replyuid):
								u = replyuid
								text += allContent[1:] + ' a ' + getNickname(u)
							elif(len(usersid) == 1 ):
								u = usersid[0]
								text += allContent[1:]
								text = text[:text.rfind('@')]
								text += ' a ' + getNickname(u)
							send_message(chatid,text)

					elif(comando == "se"):
						text = getNickname(userid) + ' ' + allContent[1:]
						send_message(chatid,text)
					elif(comando == "donaciones"):
						if(len(content) == 2):
							if(content[1] == 'on'):
								ponerDonaciones = True
								actualizarDonaciones()
							elif(content[1] == 'off'):
								ponerDonaciones = False
						else:
							text = "NOTA: ESTE COMANDO SOLO FUNCIONA BIEN EN UN CHAT DONDE TODAS LAS DONACIONES HAN SIDO REGISTRADAS POR EL BOT DESDE SUS INICIOS\nDonaciones:\n"
							i = 1
							tips = {k: v for k, v in sorted(chat.tips.items(), key=lambda item: item[1],reverse=True)}
							print(tips)
							if(host == ley):
								os.system('./update_tips.py')
								chat.loadTips()
							total = chat.coins
							keys = list(tips.keys())
							for tip in tips:
								
								if(userid == tip):
									text += '%d. %s (%d monedas)\n' % (i,getNickname(tip),tips[tip][0])
								elif(i < len(keys) and keys[i] == userid):
									text += '%d. %s (%d monedas)\n' % (i,getNickname(tip),tips[userid][0]-tips[tip][0])
								elif(i >= 0 and keys[i-2] == userid):
									text += '%d. %s (%d monedas)	\n' % (i,getNickname(tip),tips[userid][0]-tips[tip][0])
								else:
									text += '%d. %s %s \n' % (i,getNickname(tip),str((tips[tip][0]/total)*100) + '%' )

								i+=1
							send_marco(chatid,text,chat.mup,chat.mdown)
					elif(comando == "rip"):
						if(usersid):
							for u in usersid:
								rip(chatid,u)
						else:
							send_message(chatid,'uso: /rip @: envia un rip a los usuarios mencionados')
					elif(comando == "carcel"):
						if(usersid):
							for u in usersid:
								jail(chatid,u)
						else:							
							send_message(chatid,'uso: /carcel @: mete a los usuarios mencionados a la carcel')
					elif(comando == "patear"):
						print('en patear',usersid)
						if(usersid):
							for u in usersid:
								patear(chatid,u)
						else:							
							send_message(chatid,'uso: /patear @: patea a los usuarios mencionados')
					elif(comando == "cum"):
						print('en cum',usersid)
						values = getMediaValues(None,usersid,replyid)
						if(values):
							for v in values:		
								cum(chatid,v)
						else:							
							send_message(chatid,'uso: /cum @: cumea a los usuarios mencionados')
					elif(comando == "debug"):
						if(len(content) < 2):
							send_message(chatid,'uso: /debug [on|off]: muestra los errores del bot en el chat')
						elif(content[1] == 'on'):
							debug = True
						elif(content[1] == 'off'):
							debug = False
						elif(content[1] == 'jugar'):
							jugar(chatid,content[2],debug=True)
						elif(content[1] == 'donar'):
							if(len(content) > 2):
								fakeDonar = int(content[2])
							else:
								fakeDonar = 1

					elif(comando == "letra"):
						if(len(content) == 2 and content[1].isdigit()):
							if(len(cacheLetras) ==1 ):
								send_message(chatid,'Primero tienes que buscar la cancion por nombre')
							else:
								l = letra(cacheLetras[int(content[1])] )
								send_message(chatid,l)
						elif(len(content) == 1):
							send_message(chatid,'Uso:letra [id|nombre]\n\nEl id es el numero entre parentesis que aparece despues del resultado de la busqueda')
						else:

							r = buscar(m)
							send_message(chatid,r)
					elif(comando == "anuncio"):
						if(m != None):
							sub_client.edit_chat(chatId=chatid,announcement=m,pinAnnouncement=True)
							sub_client.delete_message(chatId=chatid,messageId=id)
						else:
							send_message(chatid,'uso: /anuncio [anuncio]: cambia el anuncio del chat')
					elif(comando == "agradecer"):
						if(len(content) != 2):
							send_message(chatid,'Uso: /agradecer [si|no]: configura si agradecer o no las donaciones del chat')
						else:
							if(content[1] == 'si'):
								chat.settings(agradecer=True)
								checkingTips = False
								threadTips = threading.Thread(target=checkTips, args=(chat,))
								threadTips.daemon = True
								threadTips.start()

							elif(content[1] == 'no'):
								chat.settings(agradecer=False)
								checkingTips = False
					elif(comando == "limpieza"):
						if(len(content) < 2):
							send_message(chatid,'uso: /limpieza reputacion [rep] [maxima cantidad de usuarios a sacar]\nrep es la reputacion minima a tener para que no los saquen, ejemplo 50 para nivel 5 \nESTE COMANDO SACA A TODOS LOS QUE TIENEN MENOS DE NIVEL 5 DEL CHAT (permitiendoles entrar de nuevo) DEBE USARSE CON CUIDADO')
							send_message(chatid,'uso: /limpieza actividad [minimo numero de mensajes] [maxima cantidad de usuarios a sacar]')
						else:
							minrep = 50
							maxusers = 50
							if(len(content) >= 3 and content[2].isdigit):
								minrep = int(content[2])
							if(len(content) >= 4 and content[3].isdigit):
								maxusers = int(content[3])
							userMessages = None
							if(content[1] == 'actividad'):
								send_message(chatid,'Empezando limpieza por actividad, cargando mensajes')
								userMessages = chat.loadAllUserMessages()
								send_message(chatid,'Mensajes totales registrados: %d' % (len(userMessages)) )
							threadLimpieza = threading.Thread(target=limpieza, args=(chatid,content[1],minrep,maxusers,userMessages))
							threadLimpieza.daemon = True
							threadLimpieza.start()

					elif(comando == "placa"):
						if(m == None):
							send_message(chatid,'uso: /placa [placa del chat]\n Agrega la placa del chat a la bio del bot')
							if(chat.placa):
								send_message(chatid,'Placa actual del chat: ' + str(chat.placa) )
						else:
							chat.placa = m
							chat.save()
							send_message(chatid,'Placa del chat actualizada: ' + m)
							tmp = tipoMensaje
							tipoMensaje = 0
							send_message(botgroup,'El chat ' + chat.name + '\nActualizo su placa: ' + m)
							tipoMensaje = tmp
							# bio = getBio(leybot)
							# bio += '\n' + '[%s|]'
							# sub_client.edit_profile(content=bio)

					elif(comando == "marcar"):
						if(leybot not in cohosts):
							send_message(chatid,'El bot tiene que ser cohost para poder editar la descripcion')
						else:
							chatInfo = sub_client.get_chat_thread(chatId=chat.id)  # Gets information of each chat
							chatContent = chatInfo.content
							if(chatContent == None):
								chatContent = ''
							fpos = pos = -1
							pos = chatContent.find('[c]║▌│█║▌│ █║▌│█│║▌║')
							fpos = chatContent.rfind('[c]║▌│█║▌│ █║▌│█│║▌║') + len('[c]║▌│█║▌│ █║▌│█│║▌║')
							print('posiciones')
							print(pos,fpos)
							if(fpos >= 0 and pos >= 0):
								if(premium > 0):
									chatContent = chatContent[:pos] + marcaPremiumcom + chatContent[fpos:]
								else:
									chatContent = chatContent[:pos] + marcacom + chatContent[fpos:]
							else:
								print('agregando con saltos')
								if(premium > 0):
									chatContent += '\n\n' + marcaPremiumcom
								else:
									chatContent += '\n\n' + marcacom
							print(chatContent)
							sub_client.edit_chat(chatId=chatid,content=chatContent)

					elif(comando == "tiempo" or comando == 'uptime'):
						t = time() - startbotTime
						text = "Tiempo activo del bot: %d:%d\n" % (t/60,t%60)
						if(premium > 0):
							text += 'Premium'
						else:
							t = freetime - t
							text += 'Tiempo restante: %d:%d\n' % (t/60,t%60)
						send_message(chatid,text)
					elif(comando == "seguro"):
						if(len(content) == 2 and content[1].isdigit):
							threadLiberar = threading.Thread(target=liberar,args=(chatid,int(content[1])))
							threadLiberar.daemon = True
							threadLiberar.start()
						sub_client.edit_chat(chatid,viewOnly=True)
					elif(comando == "liberar"):
						sub_client.edit_chat(chatid,viewOnly=False)
					elif(comando == "onlyFans"):
						if(len(content) == 2):
							if(content[1] == 'on' or content[1] == 'si'):
								onlyFans = True
							elif(content[1] == 'off' or content[1] == 'no'):
								onlyFans = False
						else:
							send_message(chatid,'uso: /onlyFans [on|off]: borra todos los mensajes que no sean de un op')
					elif(comando == "noticias"):
						hecho = False
						if(len(content) == 2):
							if(content[1].isdigit()):
								nid = int(content[1])
								n = s.loadNoticia(nid)
								if(n == None):
									send_message(chatid,'No existe la noticia ' + str(nid))
									hecho = True
								else:
									text = n.nombre + '\n'
									text += 'fecha: ' + n.fecha.strftime("%m-%d") + '\n'
									text += n.contenido + '\n\n'
									hecho = True
									send_message(chatid,text)
							else:
								for t in tiposDeNoticia:
									if(t[1].lower() == content[1].lower()):
										text = 'Noticias ' + t[1] + ':\n'
										noticias = s.loadNoticias(t[0])
										for n in noticias[::-1]:
											text += str(n.id) + '. ' + n.nombre + '\n' 
											text += 'fecha: '  + n.fecha.strftime("%m-%d") + '\n'
											text += '\n'
										send_message(chatid,text)
										hecho = True
										break
							
						else:	
							noticias = s.loadNoticias()
							text = 'Noticias:\n'
							for n in noticias[::-1]:
								text += str(n.id) + '. ' + n.nombre + '\n' 
								text += 'Categoria: ' + tiposDeNoticia[n.tipo - 1][1] + '\n'
								text += 'fecha: '  + n.fecha.strftime("%m-%d") + '\n'
								text += '\n'
							text += 'usar: /noticias [n]: para ver mas informacion sobre una noticia'
							send_message(chatid,text)
							hecho = True
						if(not hecho):
							send_message(chatid,'uso: /noticias: muestra las noticias\n/noticias [n]: muestra la noticia n\n/noticias [categoria]: muestra todas las noticias de una categoria')
							text = 'Categorias:\n'
							for c in tiposDeNoticia:
								text += c[1] + ': ' + c[2] + '\n'
							send_message(chatid,text)
					elif(comando == "programar"):
						if(len(content ) != 4):
							text = 'uso: /programar [nombre] [cada cuanto] [comando]' + '\n'
							text += 'comando: es un comando creado del chat, no uno de los que vienen con el bot'
							text += 'cada cuanto puede ser H[numero de horas] D[hora del dia] M[numero de minutos]\n'
							text += 'Ejemplo: /programar H1 darbienvenida: da la bienvenida cada 2 horas\n'
							text += '/programar D22:00 dormir: todos los dias a las 10pm lanza el comando dormir\n'
							text += '/programar M90 revivan: ejecuta el comando revivan cada 90 minutos'
							send_message(chatid,text)
						else:

							if(content[3] not in chat.comandos):
								send_message(chatid,'El comando no esta en los comandos creados de este chat')
							elif(content[1] in programas):
								send_message(chatid,'Ya %s esta en la programacion. Usar otro nombre',content[1])
							elif(not content[2][1:].replace(':','').isdigit()):
								send_message(chatid,'El formato de tiempo esta mal es:\nDhh:mm\nM[minutos]\nH[horas]')
							elif(chat.comandos[content[3]].op != None and opLevel < chat.comandos[content[3]].op):
								send_message(chatid,'No suficientes permisos para usar el comando que intentas programar')
							else:
								if(chat.comandos[content[3]].op != None):
									finalUserId = chat.comandos[content[3]].userid
								else:
									finalUserId = userid

								if(content[2][0] == 'H'):
									t = content[2][1:]
									p = Programa(content[1],content[3],finalUserId,2,int(content[2][1:]) * 60)
									if(p.minutos == 60):
										chat.programar(p)
										programas[p.nombre] = p
										send_message(chatid,'Programado %s cada hora' % (p.nombre) )
									elif(p.minutos == 0):
										send_message(chatid,'No se puede programar algo a 0 horas')
									else:
										chat.programar(p)
										programas[p.nombre] = p
										send_message(chatid,'Programado %s cada %d horas' % (p.nombre,p.minutos/60) )
								elif(content[2][0] == 'M'):
									p = Programa(content[1],content[3],finalUserId,2,int(content[2][1:]))
									if(p.minutos == 1):
										send_message(chatid,'No se puede programar algo cada minuto')
									elif(p.minutos == 0):
										send_message(chatid,'No se puede programar a 0 minutos')
									else:
										chat.programar(p)
										programas[p.nombre] = p
										send_message(chatid,'Programado %s cada %d minutos' % (p.nombre,p.minutos) )
								elif(content[2][0] == 'D'):
									if(user.timezone == None):
										send_message(chatid,getNickname(userid) + ' Necesitas usar /timezone para poner tu zona horaria antes de poder programar por hora del dia')
									else:
										try:
											fecha = datetime.datetime.strptime(content[2][1:], '%H:%M')
										except:
											send_message(chatid,'El formato de fecha esta mal')
										else:
											fecha = user.timezone.localize(fecha).astimezone(pytz.timezone('UTC'))
											hora = datetime.datetime.time(fecha.astimezone(pytz.timezone('UTC')))
											p = Programa(content[1],content[3],finalUserId,0,hora.hour*60+hora.minute)
											chat.programar(p)
											programas[p.nombre] = p
											horaAhora = datetime.datetime.time(datetime.datetime.now(datetime.timezone.utc))	
											minutosDia = (horaAhora.hour*60) + horaAhora.minute
											if(minutosDia > p.minutos):
												send_message(chatid,'Programado %s faltan %s' % (p.nombre,datetime.timedelta(minutes=(p.minutos - minutosDia) + 1440)))
											else:
												send_message(chatid,'Programado %s faltan %s' % (p.nombre, datetime.timedelta(minutes=p.minutos - minutosDia)))

								else:
									send_message(chatid,'[cada cuanto] tiene que ser\nD: hora del dia\nM: cada cuantos minutos\nH:cada cuantas horas')
					elif(comando == "rprograma"):
						if(len(content) != 2):
							send_message(chatid,'Uso: /rprogramar [nombre del programa a quitar]: quita un programa')
						else:
							if(content[1] not in programas):
								send_message(chatid,'%s no esta programado' % (content[1]) )
							else:
								chat.deletePrograma(content[1])
								programas.pop(content[1])
								send_message(chatid,'Borrado programa ' + content[1])
					elif(comando == "programas"):
						text = 'Programado:\n'
						horaAhora = datetime.datetime.time(datetime.datetime.now(datetime.timezone.utc))	
						minutosDia = (horaAhora.hour*60) + horaAhora.minute
						for pn in programas:
							p = programas[pn]
							if(p.tipo == 0 or p.tipo == 1):
								if(minutosDia > p.minutos):		
									text += p.nombre + ' en ' + str(datetime.timedelta(minutes=(p.minutos - minutosDia) + 1440)) + '\n'
								else:
									text += p.nombre + ' en ' + str(datetime.timedelta(minutes= p.minutos - minutosDia)) + '\n'
							elif(p.tipo == 2 or p.tipo == 3):
								if(p.minutos % 60):
									text += '%s cada %d minutos\n' % (p.nombre,p.minutos) 
								else:
									text += '%s cada %d horas\n' % (p.nombre,p.minutos/60) 
						send_message(chatid,text)
					elif(comando == "cronometro"):
						if(len(content) < 3):
							send_message(chatid,'uso: /cronometro [mm:ss] [comando]\nEjemplo: /cronometro 0:30 terminar\nEn 30 segundos mostrara el comando terminar')
						elif(len(content[1].split(':')) != 2):
							send_message(chatid,'Mal formato de tiempo, tiene que ser mm:ss')
						else:
							mi,se = content[1].split(':')
							to = int(mi)*60 + int(se)
							c = ' '.join(content[2:])
							activo = [True]
							cronosDaemon = threading.Thread(target=crono, args=(to,c,userid,activo))
							cronosDaemon.daemon = True
							cronosDaemon.start()
							cronos.append((to,c,u,activo))
							send_message(chatid,'Comando %s en %s' % (c,content[1]) )
					elif(comando == "cronometros"):
						text = 'Cronometros:\n'
						i = 1
						for c in cronos:
							t = c[0] - time()
							print(c[0],t)
							text += '%d. %s en %d:%d\n' % (i,c[1],t/60,t%60)
							i+=1
						send_message(chatid,text)
					elif(comando == "rcronometro"):
						if(len(content) == 2 and content[1].isdigit and int(content[1])-1 < len(cronos)):
							i = int(content[1])-1
							cronos[i][3][0] = False
							del cronos[i]
							send_message(chatid,'Borrado cronometro ' + content[1])
						else:
							send_message(chatid,'uso: /rcronometro [n]: n es el numero del cronometro')
					elif(comando == "bug"):
						if(m == None):
							send_message(chatid,'uso: /bug [mensaje de bug]: sirve para informar de algun bug (error) que tuvo el bot ')
						else:
							chatname = get_title(chatid)
							s.bug(m,userid,chatid,id,createdTime.replace('T',' ').replace('Z',''))
							text = 'Bug reportado en el chat ' + chatname + '\n'
							text += 'Por: '+ nickname + '\n'
							text += m
							send_message(botgroup,text)
							send_message(chatid,'Bug reportado')
					elif(comando == "sugerencia"):
						if(m == None):
							send_message(chatid,'uso: /sugerencia [mensaje]: Sirve para enviar sugerencias de cosas que te gustarian cambiar, quitar o cambiar al bot.\nComo por ejemplo mas lolis')
						else:
							chatname = get_title(chatid)
							s.sugerencia(m,userid,chatid,id,createdTime.replace('T',' ').replace('Z',''))
							text = 'Sugerencia en el chat ' + chatname + '\n'
							text += 'Por: '+ nickname + '\n'
							text += m
							send_message(botgroup,text)
							send_message(chatid,'Gracias por tu sugerencia')
					elif(comando == "opinion"):
						if(m == None):
							send_message(chatid,'uso: /opinion [tu openion del bot]: Sirve para dar una opinion sobre el bot')
						else:
							chatname = get_title(chatid)
							s.opinion(m,userid,chatid,id,createdTime.replace('T',' ').replace('Z',''))
							text = 'opinion en el chat ' + chatname + '\n'
							text += 'Por: '+ nickname + '\n'
							text += m
							send_message(botgroup,text)
							send_message(chatid,'Gracias por tu opinion')
					elif(comando == "calificacion" or comando == "calificar"):
						calificaciones = s.loadEstrellas()
						if(len(content) < 2 or not content[1].isdigit() or int(content[1]) not in range(1,6) ):
							promedio = sum(calificaciones.values())/len(calificaciones)
							send_message(chatid,'Para calificar: /calificacion [1-5] [mensaje opcional]: Del 1 a 5 ¿Cuantas estrellas le das al bot? \nEstos resultados se suman al total\n adicionalmente despues de la calificacion se puede poner un mensaje diciendo el porque')
							send_message(chatid,'Calificacion actual %.1f estrellas de %d usuarios' % (promedio,len(calificaciones)))
						else:
							text = None
							if(len(content) >= 3):
								text = ' '.join(content[2:])
							send_message(chatid,'Gracias %s por calificar el bot' % (getNickname(userid)))
							s.calificar(int(content[1]),userid,text)
							calificaciones[userid] = int(content[1])
							# calificaciones.append(int(content[1]))
							promedio = sum(calificaciones.values())/len(calificaciones)
							send_message(chatid,'Calificacion actual %.1f estrellas de %d usuarios' % (promedio,len(calificaciones)))
					elif(comando == "calificaciones"):
						calificaciones = s.loadCalificaciones()
						text = 'Calificaciones del bot:'
						for c in calificaciones:
							text += '%d estrellas por %s\n' % (c[1],getNickname(c[0]))
							if(c[2] != None):
								text += '"%s"\n' % (c[2])
						send_message(chatid,text)
					elif(comando == 'tag'):
						if(len(usersid) == 1):
							if(m == None or m.find('!') == -1):
								for u in usersid:
									userTags = s.loadUserTags(u)
									text = getNickname(u) + '\n'
									tagCount = 0
									if(u in chat.tags):
										for t in chat.tags[u]:
											if(chat.tags[u][t] != None):
												text += t + ':' + chat.tags[u][t] + '\n'
											else:
												text += t + '\n'
											tagCount += 1
									if(userTags != None):										
										for t in userTags:
											if(chat.tags[u][t] != None):
												text += t + ':' + chat.tags[u][t] + '\n'
											else:
												text += t + '\n'
											tagCount += 1
									if(tagCount == 0):
										send_message(chatid,getNickname(u) + ' no tiene tags')
									else:
										send_message(chatid,text)
							else:
								if(m.find(':')  != -1):
									tag = m[m.find('!')+1:m.find(':')]
									text = m[m.find(':')+1:]
								else:
									tag = m[m.find('!')+1:]
									text = None
								print(tag,text)
								chat.saveUserTag(usersid[0],tag,text)
						else:
							if(m != None and '!' in m):
								tag = m[m.find('!')+1:]
								userResult = []
								for u in chat.tags:
									if(tag in chat.tags[u]):
										userResult.append((u,chat.tags[u][tag]) )
								if(not userResult):
									send_message(chatid,'No hay usuarios con esa tag')
								else:
									text = 'Usuarios con esa etiqueta\n'
									for u in userResult:
										if(u[1] != None):
											text += getNickname(u[0]) + ': ' +u[1] + '\n'
										else:
											text += getNickname(u[0]) + '\n'
									send_message(chatid,text)
							else:
								send_message(chatid,'uso /tag @user !tag:descripcion\nEjemplo /tag @user !personalidad:muy fria')
								text = 'Tus etiquetas:' + '\n'
								userTags = s.loadUserTags(userid)
								if userid in chat.tags:
									for t in chat.tags[userid]:
										if(chat.tags[userid][t] != None):
											text += t + ':' + chat.tags[userid][t] + '\n'
										else:
											text += t + '\n'
								if (userTags != None):
									for t in userTags:
										if(userTags[t] != None):
											text += t + ':' + userTags[t] + '\n'
										else:
											text += t + '\n'
									send_message(chatid,text)
								else:
									send_message(chatid,'no tienes etiquetas')
					elif(comando == 'rtag'):
						if(len(usersid) == 1 and m != None and m.find('!') != -1):
							send_message(chatid,chat.removeUserTag(usersid[0],m[m.find('!')+1:]))
						else:
							send_message(chatid,'uso /rtag @user !tag: remueve una etiqueta')
					elif(comando == "add"):
						if(userid == ley):
							freetime += int(m)*60
						else:
							send_message(chatid,'Comando de ley, sirve para agregar mas tiempo gratis al bot')
					elif(comando == "antispam"):
						if(len(content) < 2):
							text = 'uso: /antispam [links|imagenes|stickers|texto|repetidos]\n'
							text += '/antispam links: borra todos los links de amino que se envien en el chat\n'
							text += '/antispam imagenes: borra todo lo que sea imagenes\n'
							text += '/antispam stickers: borra los stickers\n'
							text += '/antispam repetidos [n]: borra mensajes de texto que hayan sido repetidos mas de n veces en los ultimos 100 mensajes\n'
							text += '/antispam texto [texto de ejemplo]: borra todos los mensajes que tengan "texto de ejemplo" en el mensaje '
							send_message(chatid,text)
						else:
							if(content[1] == 'links'):
								spamText.append('aminoapps.com/p')
							elif(content[1] == 'imagenes'):
								spamImagenes = True
								send_message(chatid,'modo sin imagenes')
							elif(content[1] == 'stickers'):
								spamStickers = True
								send_message(chatid,'modo sin stickers')
							elif(content[1] == 'texto'):
								if(len(content) < 3):
									text = 'uso: /antispam texto [texto]\n'
									text += 'Ejemplo: /antispam texto www: borra todos los mensajes que contengan www\n'
									send_message(chatid,text)
								else:
									spamText.append(' '.join(content[2:]) )
							elif(content[1] == 'repetidos'):
								if(len(content) != 3 or not content[2].isdigit()):
									text = 'uso: /antispam repetidos [n]\n'
									text += 'Ejemplo: /antispam repetidos 5: borra cualquier mensaje de texto que se repita mas de 5 veces\n'
									send_message(chatid,text)
								else:
									spamRepetidos = int(content[2])

							else:
								text = 'uso: /antispam [links|imagenes|texto|repetidos]\n'
								text += '/antispam links: borra todos los links de amino que se envien en el chat\n'
								text += '/antispam imagenes: borra todo lo que sea imagenes y stickers\n'
								text += '/antispam repetidos [n]: borra mensajes de texto que hayan sido repetidos mas de n veces en los ultimos 100 mensajes\n'
								text += '/antispam texto [texto de ejemplo]: borra todos los mensajes que tengan "texto de ejemplo" en el mensaje '
								send_message(chatid,text)
					elif(comando == "permitir"):
						if(len(content) < 2):
							text = 'uso: /permitir [links|imagenes|texto|repetidos]\n'
							text += 'Lo opuesto a /antispam\n'
							text += 'Textos bloqueados:\n'
							for t in spamText:
								text += t + ' \n'
							send_message(chatid,text)
						else:
							if(content[1] == 'links'):
								if('aminoapps.com/p' in spamText):
									spamText.remove('aminoapps.com/p')
							elif(content[1] == 'imagenes'):
								spamImagenes = False
							elif(content[1] == 'stickers'):
								spamStickers = False

							elif(content[1] == 'repetidos'):
								spamRepetidos = 0
							elif(content[1] == 'texto'):
								if(len(content) < 3):
									text = 'uso: /permitir texto [texto]\n'
									send_message(chatid,text)
								else:
									texto = content[2:]
									if(texto in spamText):
										spamText.remove(texto )
										send_message(chatid,'permitiendo ' + texto)
									else:
										send_message(chatid,'no esta bloqueado ' + texto)

							else:
								text = 'uso: /antispam [links|imagenes|texto|repetidos]\n'
								text += '/antispam links: borra todos los links de amino que se envien en el chat\n'
								text += '/antispam imagenes: borra todo lo que sea imagenes y stickers\n'
								text += '/antispam texto [texto de ejemplo]: borra todos los mensajes que tengan "texto de ejemplo" en el mensaje '
								send_message(chatid,text)


					elif(comando == "discord"):
						if(premium > 0):
							if(len(content) < 2 ):
								text = 'uso: /discord [link|mensaje]\n'
								text += '/discord link: link del servidor de discord asociado\n'
								# text += '/discord unirse: Si asociaste tu cuenta de amino con discord a traves de leybot, te invita al grupo de este chat en discord\n'
								text += '/discord mensaje [mensaje]: envia un mensaje al discord de este chat por el canal del bot usando tu alias'
								send_message(chatid,text)
							else:

								guildid = chat.loadDiscord()
								if(guildid == None):
									send_message(chatid,'Este chat todavia no tiene un servidor de discord asociado, para asociar uno el anfitrion de este chat debe escribirle al bot en discord desde el canal amino')
								else:
									if(content[1] == 'mensaje'):
										if(len(content) < 3):
											send_message('Falta el mensaje para enviar al servidor de discord')
										else:
											m = ' '.join(content[2:])
											send_discord_guild(guildid,getNickname(userid) + ': ' + m)
											send_message(chatid,'Mensaje enviado al discord')
									elif(content[1] == 'link'):
										print('getting link')
										get_discord_link(guildid)
										print(discordInviteLink)
										t = tipoMensaje
										tipoMensaje = 0
										print(chatid,discordInviteLink)
										send_message(chatid,str(discordInviteLink) )
										tipoMensaje = t
									# elif(content[1] == 'unirse'):
									# 	discordid = s.loadDiscordUser(userid)
									# 	if(discordid == None):
									# 		send_message(chatid,'Primero tienes que asociar tu cuenta de discord con leybot, para hacerlo escribe en discord a leybot#3620 el mensaje /amino ')
									# 	else:

						else:
							text = '¿Sabias que leybot esta tambien en discord?\n'
							text += 'Este comando sirve para vincular leybot en discord y en amino.\n'
							text += 'Puede: enviar mensajes entre las apps, actualizar links invitar usuarios\n'
							text += 'Pero es solo para los premiums'
							send_message(chatid,text)
					elif(comando == "imagenBienvenida"):
						r = s.loadMedia(name=m,chatid=chat.id)
						# if(r == None):

							
					elif(comando == "loli"):
						link = buscarLoli(m)
						if(link):
							send_message(chatid,'Aqui esta, cuidala bien')
							send_link(chatid,link)
						else:
							send_message(chatid,'Solo los mas puros de corazon pueden ver esta imagen')
							send_link(chatid,'http://st1.narvii.com/7680/d0b72bcf6e50745f0256acaf27770b2b8d70b763r5-184-180_00.jpeg')

					elif(comando == "trapito"):
						trapitos = os.listdir('trapitos')
						print('trapitos/' + random.choice(trapitos))
						send_imagen(chatid,'trapitos/' + random.choice(trapitos))
					elif(comando == "tutorial"):
						tutoriales = [i.replace('.txt','') for i in os.listdir('tutorial/')]
						if(len(content) == 1 ):
							text = 'Tutoriales: '
							for t in tutoriales:
								text += t + ','
							send_message(chatid,text[:-1] + '.')
							send_message(chatid,'Escribe /tutorial op para tutorial sobre op (el primer tutorial)')
						else:
							if(content[1] in tutoriales):
								nombreTutorial = content[1]
								faseTutorial = 0
								comandosTutorial = []
								tutorial(content[1],0)
							else:
								send_message(chatid,'No hay un tutorial para ' + content[1])
								text = 'Tutoriales: '
								for t in tutoriales:
									text += t + ','
								send_message(chatid,text[:-1] + '.')


					elif(comando == "programarBienvenida"):
						if(len(content) < 2):
							send_message(chatid,'uso: /programarBienvenida /[comando]: agrega un comando para cuando llegue un nuevo usuario\nEjemplo: /programarBienvenida /media stickerdebienvenida ')
						else:
							comando = m
							s.comandoBienvenida(chatid,comando)
							send_message(chatid,'Programado %s cuando entre alguien' % (comando))
					elif(comando == "borrarBienvenida"):
						if(len(content) < 2 or not content[1].isdigit()):
							send_message(chatid,'uso: /borrarBienvenida [id]: quita un comando de la bienvenida ')
							if(comandosBienvenida):
								text = 'Comandos programados de bienvenida:\n'
								for id,c in comandosBienvenida.items():
									text += "%d. %s\n" % (id,c)
								send_message(chatid,text)
							else:
								send_message(chatid,'No hay nada programado para bienvenida')
						else:
							id = int(content[1])
							if(id in comandosBienvenida):
								t = s.removeComandoBienvenida(chatid,id)
								comandosBienvenida.pop(id)
								send_message(chatid,'comando eliminado de la bienvenida')
							else:
								send_message(chatid,'no se encontro ese id')
					elif(comando == "decir"):
						if(m):
							if(len(m) > 200):
								send_message(chatid,"no se pueden decir textos de mas de 200 caracteres")
							else:
								if(voz == 'google'):
									for i in range(3):
										try:
											tts = gTTS(text=m,lang='es',slow=False)
											path = '/tmp/' + str(int(time())) + '.mp3'
											tts.save(path)
											break
										except Exception as e:
											print(e)
											print('error obteniendo audio reintentando')
										else:
											break
									else:
										send_reply(chatid,'no pude decir esto lo siento',id)
										continue

									send_imagen(chatid,path)
								else:
									try:
										polly =  boto3.client('polly',region_name='us-east-1')
										response = polly.synthesize_speech(Text=m,OutputFormat='mp3',VoiceId=voz)
										if "AudioStream" in response:
											with closing(response["AudioStream"]) as stream:
												path = '/tmp/' + voz + '.mp3'
												try:
												    with open('/tmp/' + voz + '.mp3', "wb") as file:
												        file.write(stream.read())
												except IOError as error:
													send_message(chatid,'tuve problemas para decir eso')
												else:
													send_audio(chatid,path)
									except botocore.exceptions.ClientError:
										voz = 'google'
										chat.settings(voz=voz)

										send_message(chatid,'tuve problemas para decir eso')

						else:
							send_message(chatid,'uso: /decir [texto]: envia una nota de voz diciendo el texto')
					elif(comando == "voz"):
						if(m):
							if(m not in voces):
								send_message(chatid,'%s no esta entre las opciones, elija una de las siguientes voces' % (m))
								mostrarVoces(chatid)
							else:
								voz = m
								send_message(chatid,'voz del bot ' + m)
								chat.settings(voz=voz)
						else:
							send_message(chatid,'uso: /voz [voz]: cambia la voz del bot')
							send_message(chatid,'voz actual ' + voz)
					elif(comando == "voces"):
						mostrarVoces(chatid)
					elif(comando == "prefijo"):
						if(not m):
							send_message(chatid,'uso: /prefijo [prefijo]: el prefijo que se le pone a los mensajes del bot cada salto de linea si el tipo de mensaje es normal')
						else:
							prefijo = m
							chat.settings(prefijo=prefijo)
					elif(comando == "meta"):
						if(len(content) < 3 or content[1] not in ['monedas','usuarios'] ):
							send_message(chatid,'uso: /meta [monedas|usuarios] [cantidad] [nombre opcional]\n[comando opcional]: Pone una meta de monedas a partir de la cantidad actual y cuando llega lo dice y ejecuta el comando')
						else:
							if(content[1] == 'monedas'):
								lineas = allContent.split('\n')
								l = lineas[0].split(' ')
								monedas = int(content[2])
								c = None
								nombre = None
								monedasTotal = chat.coins + monedas
								if(len(l) >= 4):
									nombre = ' '.join(l[3:])

								if(len(lineas) == 2):
									if(lineas[1] in chat.comandos):
										c = lineas[1]
								r = chat.goal(monedasTotal,monedas,nombre,c,userid)
								if(r):
									send_message(chatid,'meta creada %d monedas' % (monedas) )
							elif(content[1] == 'usuarios'):
								lineas = allContent.split('\n')
								l = lineas[0].split(' ')
								cantidad = int(content[2])
								if(cantidad <= 1):
									send_message(chatid,'La minima meta de usuarios es de 2 usuarios')
								elif(cantidad in chat.usersGoals ):
									send_message(chatid,'Ya existe esa meta de usuarios')
								else:
									c = None
									nombre = None
									if(len(l) >= 4):
										nombre = ' '.join(l[3:])

									if(len(lineas) == 2):
										if(lineas[1] in chat.comandos):
											c = lineas[1]
									r = chat.goal(0,0,nombre,c,userid,cantidad)
									if(r):
										send_message(chatid,'meta creada %d usuarios' % (cantidad) )

					elif(comando == "metas"):
						if(chat.goals):
							text = 'Metas de monedas:\n'
							for g in chat.goals.values():
								text += '%d monedas ' % (g.monedas)
								if(g.nombre):
									text += g.nombre + ' '
								text += 'faltan %d\n' % (g.monedasTotal - chat.coins )
							send_message(chatid,text)
						if(chat.usersGoals):
							text = 'Metas de usuarios:\n'
							for g in chat.usersGoals.values():
								text += '%d usuarios ' % (g.cantidad)
								if(g.nombre):
									text += g.nombre + ' '
								text += '\n'
							send_message(chatid,text)
						if(not chat.goals and not chat.usersGoals):
							send_message(chatid,'No hay metas')
					elif(comando == "borrarMeta"):
						if(len(content) < 2):
							text = None
							goalsBorrar = []
							i = 1
							if(chat.goals):
								text = 'Metas de monedas:\n'

								for g in chat.goals.values():
									text += '%d. %d monedas ' % (i,g.monedas)
									i+= 1
									goalsBorrar.append((0,g.monedasTotal) )
									if(g.nombre):
										text += g.nombre + ' '
									text += 'faltan %d\n' % (g.monedasTotal - chat.coins )
								send_message(chatid,text)
							if(chat.usersGoals):
								text = 'Metas de usuarios:\n'
								for g in chat.usersGoals.values():
									text += '%d. %d usuarios ' % (i,g.cantidad)
									i += 1
									goalsBorrar.append((1,g.cantidad) )
									if(g.nombre):
										text += g.nombre + ' '
									text += '\n'
							if(text):
								send_message(chatid,text)
								send_message(chatid,'uso: /borrarMeta [n]: borra la meta numero n')
							else:
								send_message(chatid,'No hay metas')
						elif(content[1].isdigit()):
							l = len(goalsBorrar)
							n = int(content[1]) - 1
							if(n >= 0 and n < l):
								if(goalsBorrar[n][0]):
									chat.borrarGoal(cantidad=goalsBorrar[n][1])
								else:
									chat.borrarGoal(goalsBorrar[n][1])
					elif(comando == "lista"):
						if(len(content) < 3):
							text = 'uso: /lista [ver|crear|borrar|limpiar|usar|nousar]'
							text += '/lista crear [nombre]|[discriminante]: crea una lista'
							text += '/lista ver [nombre]: ve el contenido de una lista'
							text += '/lista borrar [nombre]: borra una lista'
							text += '/lista limpiar [n] [nombre]: limpia las primeras n cosas de una lista'
							text += '/lista usar [nombre]|[descriminante]: agrega otro discriminante a una lista'
							text += '/lista nousar [nombre]|[descriminante]: quita un discriminante de una lista'

							send_message(chatid,text)
						else:
							resto = ' '.join(content[2:])
							discriminantes = None
							if('|' in resto):
								discriminantes = resto[resto.find('|')+1:].split('|')

							if(content[1] == 'crear'):
								if(discriminantes):
									nombre = resto[:resto.find('|')]
									if(not nombre):
										send_message(chatid,'tienes que ponerle un nombre a la lista')
									elif(nombre not in listas):
										listas[nombre] = discriminantes
										cosasLista[nombre] = []
										s.listaChat(nombre,discriminantes,chatid)
										send_message(chatid,'Creada lista ' + nombre)
								else:
									send_message(chatid,'Debes poner algo para identificar cuando un mensaje entra a la lista')
							elif(content[1] == 'ver'):
								nombre = resto
								if(nombre in cosasLista):
									text = '%s\n' % (nombre)
									i = 1
									for c in cosasLista[nombre]:
										text += '%d. %s %s\n' % (i,getNickname(c[0]),c[1])
										i+=1
									send_message(chatid,text)
								else:
									send_message(chatid,'no esta la lista ' + nombre)
							elif(content[1] == 'borrar'):
								nombre = resto
								if(nombre in listas):
									s.borrarListaChat(nombre,chatid)
									listas.pop(nombre)
									cosasLista.pop(nombre)
									send_message(chatid,'Borrada lista ' + nombre)
								else:
									send_message(chatid,'no esta la lista ' + nombre)
							elif(content[1] == 'limpiar'):
								if(content[2].isdigit()):
									n = int(content[2])
									nombre = ' '.join(content[3:])
									if(nombre in listas):
										for cosa in cosasLista[nombre][:n]:
											s.borrarCosasLista(nombre,cosa[0],cosa[1],chatid)
										cosasLista[nombre] = cosasLista[nombre][n:]
										send_message(chatid,'lista limpiada')
									else:
										send_message(chatid,'no existe la lista ' + nombre)
								else:
									send_message(chatid,'uso: /lista limpiar [n] [nombre]: limpia n mensajes de una lista')
							elif(content[1] == 'usar'):
								if(discriminantes):
									for discriminante in discriminantes:
										nombre = resto[:resto.find('|')]
										if(nombre in listas):
											listas[nombre].append(discriminante)
											s.discriminantesListaChat(nombre,listas[nombre],chatid)
											send_message(chatid,'usando ' + discriminante)
								else:
									send_message(chatid,'Falta el discriminante, separar con | ')
							elif(content[1] == 'nousar'):
								nombre = resto[:resto.find('|')]
								if(discriminantes):
									for discriminante in discriminantes:
										if(nombre in listas):
											if(discriminante in listas[nombre]):
												listas[nombre].remove(discriminante)
												s.discriminantesListaChat(nombre,listas[nombre],chatid)
												send_message(chatid,'Discriminante eliminado')
											else:
												send_message(chatid,'la lista %s no esta usando el discriminante %s' % (nombre,discriminante))
										else:
											send_message(chatid,'no existe la lista ' + nombre)
								else:
									send_message(chatid,'Falta el discriminante, separar con | ')

					elif(comando == "listas"):
						if(listas):
							text = 'Listas:\n'
							for l in listas:
								text += l + '\n'
							send_message(chatid,text)
						else:
							send_message(chatid,'No hay listas')

					elif(comando == "sticker"):
						if(premium):
							if(replyid and m):
								message = sub_client.get_message_info(chatid,replyid)
								if('originalStickerId' not in message.json['extensions']):
									send_message(chatid,'El mensaje no es un sticker')
								elif(sub_client.get_sticker_collection(message.json['extensions']['sticker']['stickerCollectionId']).collectionType == 2):
									send_message(chatid,'El sticker tiene que estar en un pack a parte no puede ser de favoritos')
								else:
									stickerid = message.json['extensions']['originalStickerId']
									r = user.addSavedMessage(m,stickerid,3)

									send_message(chatid,r)
							else:
								send_message(chatid,'uso: /sticker [nombre]: Guarda un sticker en los saves, el sticker tiene que estar en un pack a parte no puede estar en favoritos')
						else:
							send_message(chatid,'Este comando es para que el bot use sticker pero es un comando premium')
					elif(comando == "ponerMetas"):
						if(len(content) < 2 or not content[1].isdigit() or int(content[1]) not in range(8)):
							text = 'uso: /ponerMetas [0|1|2|3|4|5|6|7]: '
							text += '/ponerMetas 0: solo muestra las metas cuando se alcanzan\n'
							text += '/ponerMetas 1: muestra las metas cuando donan\n'
							text += '/ponerMetas 2: pone las metas en la descripcion del chat\n'
							text += '/ponerMetas 3: 1 y 2\n'
							text += '/ponerMetas 4: pone las metas en los anuncios\n'
							text += '/ponerMetas 5: 1 y 4\n'
							text += '/ponerMetas 6: 2 y 4\n'
							text += '/ponerMetas 7: 1, 2 y 4\n'
							send_message(chatid,text)
						else:
							ponerMetas = int(content[1])
							chat.settings(ponerMetas=ponerMetas)
					elif(comando == "seguir"):
						if(userid == host):
							seguirLimpiando = True
					elif(comando == "coa"):
						if(len(content) < 2):
							send_message(chatid,'uso: /coa [dar|quitar|dame|soltar]')
						elif(host != ley):
							send_message(chatid,'Solo se puede usar este comando en un chat donde ley es anfitrion')
						elif(content[1] == 'dar'):
							if(opLevel >= 3):
								for u in usersid:
									metercoa(chatid,u)

							else:
								send_message(chatid,'no tienes permisos para dar coa')
						elif(content[1] == 'quitar'):
							if(opLevel >= 3):
								for u in usersid:
									sacarcoa(chatid,u)
							else:
								send_message(chatid,'no tienes permisos para quitar coa')
						
						elif(content[1] == 'dame'):
							metercoa(chatid,userid)

						elif(content[1] == 'soltar'):
							sacarcoa(chatid,userid)
							send_message(chatid,'Has soltado tu coa')

					elif(comando == "coas"):
						cohosts = get_cohosts(chatid)
						text = 'Coas:\n'
						for c in cohosts:
							text += '%s\n' % (getNickname(c))
						send_message(chatid,text)

					elif(comando == 'miau'):
						send_link(chatid,getCat())
					elif(comando == "gif"):
						if(m):
							send_link(chatid,getGif(m))
						else:
							send_message(chatid,'uso: /gif [busqueda]\nEjemplo: /gif anime (busca gif de anime)')
					elif(comando == "nickname"):
						if(userid != botOwner and userid != ley):
							send_message('solo el dueño de este bot %s puede usar este comando' % (botOwner) )
						else:
							if(m):
								sub_client.edit_profile(nickname=m)
							else:
								send_message(chatid,'uso: /nickname [nuevo nombre]: le cambia el nombre al bot')
					elif(comando == "bio"):
						if(userid != botOwner and userid != ley):
							send_message('solo el dueño de este bot %s puede usar este comando' % (botOwner) )
						else:
							if(m):
								sub_client.edit_profile(content=m)
							else:
								send_message(chatid,'uso: /bio [nueva bio]: le cambia la bio al bot')
					elif(comando == "icon"):
						if(userid != botOwner and userid != ley):
							send_message('solo el dueño de este bot %s puede usar este comando' % (botOwner) )
						else:
							if(replyid == None):
								send_message(chatid,"Falta seleccionar la imagen")
							else:
								message = sub_client.get_message_info(chatid,replyid)
								mediaValue = message.json['mediaValue']
								t = message.json['type']
								if(t == 100):
									send_message(chatid,'mensaje eliminado')
								elif(mediaValue):
									sub_client.edit_profile(icon=mediaValue)
					elif(comando == "copiar"):
						if(userid != botOwner and userid != ley):
							send_message('solo el dueño de este bot %s puede usar este comando' % (botOwner) )
						else:
							if(usersid):
								js = sub_client.get_user_info(usersid[0]).json
								js['extensions'] = js.get('extensions',{})
								if(not js['extensions']):
									sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'])
								elif('style' not in js['extensions']):
									sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
								elif('backgroundMediaList' in js['extensions']['style'] ):
									sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],backgroundImage=js['extensions']['style']['backgroundMediaList'][0][1],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
								else:
									sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],backgroundColor=js['extensions']['style']['backgroundColor'],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
					elif(comando == 'ver'):
						for u in usersid:
							ver(chatid,u)
					elif(comando == "moe"):
						if(m):
							link = buscarMoeTag(m)
						else:
							link = buscarMoe()
						if(link):
							send_link(chatid,link)
					elif(comando == "danbooru"):
						if(m):
							link = buscarDanbooru(" " + m)
						else:
							link = buscarDanbooru()
						if(link):
							send_link(chatid,link)
					elif(comando == "chica"):
						link = buscarChica(m)
						if(link):
							send_link(chatid,link)
					elif(comando == "waifux2"):
						if(replyid == None):
							send_message(chatid,"Falta seleccionar la imagen")
						else:
							message = sub_client.get_message_info(chatid,replyid)
							mediaValue = message.json['mediaValue']
							t = message.json['type']
							if(t == 100):
								send_message(chatid,'mensaje eliminado')
							elif(mediaValue):
								link = waifux2(mediaValue)
								send_link(chatid,link)
					elif(comando == "strike"):
						n = 1
						if(len(content) >= 2):
							try:
								n = int(content[1])
							except:
								pass
						for u in usersid:
							strike(u,n)

					elif(comando == "sigueme"):
						if(userid == botOwner):
							sub_client.follow(userid)
							send_reply(chatid,'vale te sigo ^^',id)
					elif(comando == "strikes"):
						if(usersid):
							text = ''
							for u in usersid:
								if(u in strikes):
									text += 'strikes %s: %d\n' % (getNickname(u),strikes[u])
								else:
									text += 'strikes %s: %d\n' % (getNickname(u),0)
							send_message(chatid,text)
						else:
							text = 'Strikes:\n'
							for u in strikes:
								if(strikes[u]):
									text += '%s: %d\n' % (getNickname(u),strikes[u])
							send_message(chatid,text)
					elif(comando == "maxstrikes"):
						if(len(content) >= 2 and content[1].isdigit()):
							maxStrikes = int(content[1])
						else:
							send_message(chatid,'uso: /maxstrikes [n]: pone el numero maximo de strikes hasta el ban')
					elif(comando == "dueño"):
						if(botOwner == 'lite'):
							send_message(chatid,'Por el momento no tengo dueño, soy un bot de todos jeje')
						else:
							send_message(chatid,'Mi dueño')
							ver(chatid,botOwner)
					elif(comando == "reset"):
						loadData()
					elif(comando == "reiniciar"):
						checkingTips = False
						subprocess.Popen(['python3'] + sys.argv)
						matar()

					elif(comando == "exiliados"):
						t = sub_client.get_chat_thread(chatid,raw=True)['thread']['extensions']
						if('bannedMemberUidList' in t):
							text = 'Exiliados:\n'
							for u in t['bannedMemberUidList']:
								text += getNickname(u) + '\n'
							send_message(chatid,text)
						else:
							send_message(chatid,'No hay exiliados')
					elif(comando == "youtube"):
						if(m):
							if(content[1] == 'cancelar'):
								if(len(content) == 2):
									youtubeList.clear()
									continue	
								elif(len(content) == 3 and content[2].isdigit()):
									n = int(content[2])-1
									if(len(youtubeList) > n ):
										del youtubeList[int(content[2])]
										continue
							if(len(youtubeList) >=3):
								send_message(chatid,'El maximo de videos en la cola es 3\nPara cancelar uno /youtube cancelar')
								text = 'En cola:\n'
								n = 1
								for i in youtubeList:
									text += str(n) + '. ' + i['title'] + '\n'
									n+=1
								send_message(chatid,text)
							else:
								userYoutube = userid
								searchYoutube(chatid,m)
						else:
							if(youtubeList):
								text = 'En cola:\n'
								for i in youtubeList:
									text += i['title'] + '\n'
								send_message(chatid,text)
							else:
								send_message(chatid,'uso: /youtube [audio]: sirve para buscar audios en youtube (no muestra los videos ya que eso lo puedes hacer desde amino)')
					elif(comando == "instance"):
						send_message(chatid,'instance id:' + instanceid)
					elif(comando == "gorrito"):
						values = getMediaValues(userid,usersid,replyid)
						img = imgdir + random.choice(['gorrito.png'])

						for v in values:
							name = tmpMedia(v)
							gorrito(pilImage(name),pilImage(img),getFaces(name))
					elif(comando == "navidad"):
						values = getMediaValues(userid,usersid,replyid)
						imgs = os.listdir(imgdir + 'navidad')
						print(imgs)
						img = imgdir + 'navidad/' + random.choice(imgs)
						for v in values:
							pastepng(pilImage(v),pilImage(img))
					elif(comando == "ping"):
						ping(chatid)
					elif(comando == "sorteo"):
						if(len(content) < 2):
							text = 'uso: /sorteo [nombre] [tiempo]: crea un sorteo, el tiempo tiene que terminar con s o m\n'
							text += '/sorteos: muestra los sorteos (si hay)'
							text += '/sorteo XD: crea un sorteo llamado XD'
							text += '/sorteo 100 monedas 10s: crea un sorteo llamado 100 monedas que dure 10 segundos'
							text += '/sorteo un golpe 5m: crea un sorteo llamado un golpe que dure 5 minutos'

							send_message(chatid,text)
						else:
							if(m in sorteos):
								send_message(chatid,'%s: %d usuarios\n/terminar %s para elegir un ganador' % (m,len(sorteos[m]),m) )
							else:
								if(content[-1][-1] == 's'):
									t = content[-1][:-1]
									if(t.isdigit()):
										t = int(content[-1][:-1])
									else:
										t = 0
								elif(content[-1][-1] == 'm'):
									t = content[-1][:-1]
									if(t.isdigit()):
										t = int(content[-1][:-1])*60
									else:
										t = 0
								else:
									t = 0
								if(t):
									tl = content[1:-1]
									if(tl):
										nombre = ' '.join(content[1:-1])
									else:
										send_message(chatid,'falta el nombre del sorteo')
										nombre = None
								else:
									nombre = m
								if(nombre):
									sorteos[nombre] = []
									send_message(chatid,"sorteo %s creado, usar /entrar para participar" % (nombre))
									if(t):
										threadSorteo = threading.Thread(target=terminarSorteo, args=(nombre,t))
										threadSorteo.daemon = True
										threadSorteo.start()

					elif(comando == "sorteos"):
						if(not sorteos):
							send_message(chatid,'No hay sorteos activos')
						else:
							text = "Sorteos activos:\n"
							for sorteo in sorteos:
								text += "%s: %d usuarios\n" % (sorteo,len(sorteos[sorteo]))
							send_message(chatid,text)
					elif(comando == "terminar"):
						terminarSorteo(m)
					elif(comando == "nsfw"):
						if(len(content) < 2):
							if(eliminarNSFW):
								send_message(chatid,'Modo detectar imagenes nsfw activado\n /nsfw off para desactivar')
							else:
								send_message(chatid,'Modo detectar imagenes nsfw desactivado\n /nsfw on para activar')
						else:
							if(content[1] == 'on'):
								eliminarNSFW = True
								send_message(chatid,'detectar imagenes nsfw activado')
								s.chatSettings(chatid,nsfw=1)
							elif(content[1] == 'off'):
								eliminarNSFW = False
								send_message(chatid,'detectar imagenes nsfw desactivado')
								s.chatSettings(chatid,nsfw=0)
							else:
								send_message(chatid,'uso: /nsfw [on|off]: apaga o prende la deteccion de imagenes inapropiadas')



					elif(comando == 'entrar'):
						if(len(content) > 1):

							if(m in sorteos):
								if(userid in sorteos[m]):
									send_message(chatid,'Ya estas dentro del sorteo %s' % (m))
								else:
									sorteos[m].append(userid)
									send_message(chatid,'%s se a unido al sorteo %s' % (getNickname(userid),m))
							else:
								if(content[1] == 'en'):
									send_message(chatid,getNickname(userid) + ' a entrado ' + ' '.join(content[1:]))
								elif(content[1] in ['a','al']):
									send_message(chatid,getNickname(userid) + ' se a unido ' + ' '.join(content[1:]))
								else:
									send_message(chatid,getNickname(userid) + ' a entrado ' + ' '.join(content[1:]))
						else:
							if(len(sorteos) == 1):
								key = list(sorteos.keys())[0]

								if(userid in sorteos[key]):
									send_message(chatid,'Ya estas dentro del sorteo %s' % (key))
								else:
									sorteos[key].append(userid)
									send_message(chatid,'%s se a unido al sorteo %s' % (getNickname(userid),key))
							elif(len(sorteos) > 1):
								send_message(chatid,'Hay varios sorteos para entrar a uno pon /entrar [nombre sorteo]')
								text = "Sorteos activos:\n"
								for sorteo in sorteos:
									text += "%s: %d usuarios\n" % (sorteo,len(sorteos[sorteo]))
								send_message(chatid,text)



					elif(comando == 'dejar'):
						if(len(content) > 1):
							if(m in sorteos):
								sorteo = sorteos[m]
								if(userid in sorteo):
									sorteo.remove(userid)
									send_message(chatid,'%s ha dejado el sorteo %s' % (getNickname(userid),m))
							else:
								send_message(chatid,getNickname(userid) + ' ha dejado ' + ' '.join(content[1:]))
						else:
							for nombre,sorteo in sorteos.items():
								if(userid in sorteo):
									sorteo.remove(userid)
									send_message(chatid,'%s ha dejado el sorteo %s' % (getNickname(userid),nombre))
					elif(comando == "sleep"):
						if(len(content) == 2 and content[1].isdigit()):
							sleep(int(content[1]))
						else:
							send_message(chatid,'uso: /sleep [n]: duerme el bot (no responde) por n segundos')
					elif(comando == "mensajes"):
						if(usersid):
							for u in usersid:
								n = s.loadUserMessageCount(u,chatid)
								send_message(chatid,'mensajes de %s: %d' % (getNickname(u),n))
						else:
							send_message(chatid,'uso: /mensajes @user: muestra el numero de mensajes registrados de un usuario')
							send_message(chatid,'Tus mensajes: %s\n' % (s.loadUserMessageCount(userid,chatid)))

					elif(comando == "top"):
						timeStamp = jsonResponse['api:timestamp']
						t = datetime.datetime.strptime(timeStamp, '%Y-%m-%dT%H:%M:%SZ')
						if(len(content) < 2):
							tipo = 'todos'
							n = 3
						elif(len(content) == 2):
							n = 3
							tipo = 'todos'
							if(content[1].isdigit()):
								n = int(content[1])
							else:
								tipo = content[1]
						elif(len(content) == 3 and content[1].isdigit()):
							tipo = content[2]
							n = int(content[1])
						ayudar = True
						if(tipo == 'diario' or tipo == 'todos'):
							messages = s.loadAllUserMessages(chatid,t - datetime.timedelta(days=1))
							text = 'Top diario:\n' + topMessages(chatid,messages,n)
							send_marco(chatid,text,chat.mup,chat.mdown)
							ayudar = False
						if(tipo == 'semanal' or tipo == 'todos'):
							messages = s.loadAllUserMessages(chatid,t - datetime.timedelta(days=7))
							text = 'Top semanal:\n' + topMessages(chatid,messages,n)
							send_marco(chatid,text,chat.mup,chat.mdown)
							ayudar = False
						if(tipo == 'mensual' or tipo == 'todos'):
							messages = s.loadAllUserMessages(chatid,t - datetime.timedelta(days=30))
							text = 'Top mensual:\n' + topMessages(chatid,messages,n)
							send_marco(chatid,text,chat.mup,chat.mdown)
							ayudar = False
						if(tipo == 'total' or tipo == 'todos'):
							messages = s.loadAllUserMessages(chatid)
							text = 'Top mensajes:\n' + topMessages(chatid,messages,n)
							send_marco(chatid,text,chat.mup,chat.mdown)
							ayudar = False
						if(ayudar):
							text = 'uso: /top [n] [diaro|semanal|mensual|total|todos|n]: muestra los usuarios que mas enviaron mensajes\nEjemplos:\n'
							text += '/top 5 mensual\n'
							text += '/top 4: (todos los tops 4)\n'
							text += '/top 4: (todos los tops 4)\n'
							text += '/top semanal: (top 3 semanal)\n'

							send_message(chatid,text)							


					elif(comando == "cancelar"):
						if(opLevel >= 3):
							cancelarLimpieza = True
						if(traducirUsers or traducirDetectarUsers):
							traducirUsers = []
							traducirDetectarUsers = []
							send_message(chatid,'Deteniendo traducir')

						if(comandosTutorial):
							faseTutorial = 0
							comandosTutorial = []
							if(nombreTutorial == 'juegos'):
								send_message(chatid,'Tutorial juegos completado')
							else:
								send_message(chatid,'Cancelando tutorial')
							
							nombreTutorial = ''	
						cancelar()
				if(comandosTutorial):
					c = comandosTutorial[0]
					print('evaluando')
					print(c)
					if('%' in c):
						c = c[:c.find('%')]
					if('^' in c):
						if( idToReply != replyid):
							print('no es igual el reply')
							print(idToReply,replyid)
							continue
						else:
							print('vamos bien')
							print(idToReply,replyid)
					else:
						print('no aparece ^')
					if('@' in c and usersid):
						c = c[:c.find('@')]
					if(allContent.startswith(c.replace(r'^',''))):
						comandosTutorial = comandosTutorial[1:]
						if(not comandosTutorial):
							faseTutorial += 1
							tutorial(nombreTutorial,faseTutorial)


			# elif(content[0][0] == '!'):
			# 	if(len(usersid) == 1):
			# 		if(m == None or m.find('!') == -1):
			# 			for u in usersid:
			# 				if(u not in chat.tags):
			# 					send_message(chatid,getNickname(u) + ' no tiene etiquetas')
			# 				else:
			# 					text = getNickname(u) + '\n'
			# 					for t in chat.tags[u]:
			# 						if(chat.tags[u][t] != None):
			# 							text += t + ':' + chat.tags[u][t] + '\n'
			# 						else:
			# 							text += t + '\n'
			# 					send_message(chatid,text)

			# 		else:
			# 			tag = m[m.find('!'):m.find(':')]
			# 			if(m.find(':')  != -1):
			# 				text = m[m.find(':'):]
			# 			else:
			# 				text = None
			# 			chat.saveUserTag(usersid[0],tag,text)
			# 	else:
			# 		send_message(chatid,'uso /tag @user !tag:descripcion\nEjemplo /tag @user !personalidad:muy fria')

			# 		if userid in chat.tags:
			# 			text = 'Tus etiquetas:' + '\n'
			# 			for t in chat.tags[userid]:
			# 				if(chat.tags[userid][t] != None):
			# 					text += t + ':' + chat.tags[userid][t] + '\n'
			# 				else:
			# 					text += t + '\n'
			# 			send_message(chatid,text)

		if(programas):
			horaAhora = datetime.datetime.time(datetime.datetime.now(datetime.timezone.utc))	
			minutosDia = (horaAhora.hour*60) + horaAhora.minute
			for pName in programas:
				p = programas[pName]
				# pprint(vars(p))
				if(p.tipo == 2):
					if(int( int(time()//60) % p.minutos) == 0):							
						for c in chat.comandos[p.comando].comandos.split('\0'):
							customCommands.append((c,p.userid) )
						p.tipo = 3
				elif(p.tipo == 3):
					if(int(int(time()//60) % p.minutos) != 0):
						p.tipo = 2

				elif(p.tipo == 0):
					if(minutosDia == p.minutos):
						for c in chat.comandos[p.comando].comandos.split('\0'):
							customCommands.append((c,p.userid) )
						p.tipo = 1
				elif(p.tipo == 1 and minutosDia != p.minutos):
					p.tipo = 0


	except mysql.connector.errors.DatabaseError as e:
		PrintException()
		if(e.errno == 2006):
			print('reconectando con la base de datos')
			s.db.reconnect(5)
		else:
			print('reiniciando sesion')
			try:
				s.db.reset_session()
			except:
				s.db.reconnect(5)
	except Exception as e:
		PrintException()

		print('error de ')
		print(e)
		if(debug):
			send_message(chatid,'Error: ' + str(e))

