#!/usr/bin/env python3
import amino
import mysql.connector
import random
import sys
import os
import signal
from PIL import Image
import requests
from save import Save
from time import time
s = Save(file='default.set')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath ) + '/juegos/retos'
os.chdir(dname)
print('directory: ' +  dname)

from aminohelpers import login as loginfun
from user import User
from chat import Chat
from mensaje import Mensaje
def getNickname(userid):
	if(userid == None):
		return ''
	if(userid in usersObjects):
		if(usersObjects[userid].alias != ""):
			return usersObjects[userid].alias
	return sub_client.get_user_info(userid).nickname


def send_message(chatid,mensaje):
	sub_client.send_message(message=mensaje, chatId=chatid,messageType=tipoMensaje)

def send_marco(chatid,mensaje,mn):
	m = marcos[mn][0] + '\n\n' + mensaje + '\n\n' + marcos[mn][1]
	send_message(chatid,m)	

def send_imagen(chatid,link=None,file=None):
	if(link!=None):
		sub_client.send_message(chatId=chatid,link=link)
	else:
		sub_client.send_message(chatId=chatid,filePath=file)


def matar(i = 0):
	try:
		client.logout()
		exit(0)
	except:
		pass

	os.kill(os.getpid(), signal.SIGKILL)	


def terminar():
	send_marco(chatid,"\n\nJuego %s terminado\n\n" % (sys.argv[2]),14)
	matar()

def handler(signum, frame):
	terminar()
def actualizar(signum, frame):
	send_message(chatid,'Terminando juego por actualizaciones')
	send_marco(chatid,"\n\nJuego terminado\n\n",14)
	matar()

signal.signal(signal.SIGTERM, actualizar) #handler para matar cuando nazca un nuevo bot

def getImagenes(filePath):
	global path
	im = Image.open('gifs/' + filePath)
	path = 'imagenes/' + filePath.replace('.gif','')
	os.mkdir(path)
	path += '/'
	i = 0
	try:
	    while 1:
	        im.seek(im.tell()+1)
	        im.save(path + '%d.png' % (i),'PNG')
	        i+=1
	except EOFError:
		pass
	return i

def enviarReto(chatid,n):
	send_imagen(chatid,file=path + '%d.png' % (n))

path = ''
signal.signal(signal.SIGALRM, handler)
chatid = sys.argv[1]

# random.shuffle(retos)
tipoMensaje=111
comid = '67'
userBotId = None
userBot = 'bot'
for i in sys.argv:
	if('comid=' in i):
		comid = i[6:]
	elif('mensaje=' in i):
		tipoMensaje = int(i[8:])
	elif('user=' in i):
		client = loginfun(s,alias=i[5:])
	elif('userid=' in i):
		userBotId = i[7:]
		client = loginfun(s,userid=userBotId)
sub_client = amino.SubClient(comId=comid,client=client)
oldMessages = []
pids = s.loadGamesChat(chatid)
for pid in pids:
	try:
		os.kill(pid, signal.SIGALRM)
	except OSError as e:
		print(e) 
s.removeGamesChat(chatid)
s.gameChat(chatid,os.getpid())

usersObjects = s.loadAllUsers()
users = {}
chatid = sys.argv[1]
chat = s.loadChat(chatid)
chatThread = sub_client.get_chat_thread(chatid,raw=True)['thread']
host = chatThread['uid']
coHost = chatThread['extensions'].get('coHost',[])
chat.ops[host] = 3
for c in coHost:
	chat.ops[c] = 2

retos = None
marcos = []
with open('marcos.txt', 'r') as handler:
    buf = [line.rstrip() for line in handler]
    for i in range(0,len(buf),2):
        marcos.append((buf[i],buf[i+1]))

jugadores = []
turno = 0
chatid = chat.id
iniciado = False
libre = False
gifname = None

lastTurno = time()
aTurno = turno
tLimite = 600
tPorTurno = 0

with open('informacion.txt', 'r') as handler:
	send_marco(chatid,handler.read(),14)

try:
	r = requests.get('http://169.254.169.254/latest/meta-data/instance-id',timeout=0.1)
except:
	instanceid = 'local'
else:
	instanceid = r.text


if('LOGDIR' in os.environ):
	logPath = os.environ['LOGDIR'] + '/'
else:
	logPath = 'logs/' 
if('silent' in sys.argv):
	sys.stdout = open(logPath + __file__.replace('.py','') + chat.id + '.log', 'w')


while True:
		
		try:
			if(aTurno != turno):
				lastTurno = time()
				aTurno = turno
			if(iniciado and tPorTurno != 0 and time() - lastTurno >= tPorTurno):
				if(len(retos) == 0 ):
					send_message(chatid,'Se acabaron los retos')
					send_marco(chatid,"\n\nJuego terminado\n\n",14)
					matar()
			
				enviarReto(chatid,retos.pop())
				turno += 1
				send_message(chatid,'Turno de ' + getNickname(jugadores[turno] % len(jugadores)))


			if(time() - lastTurno >= tLimite):
				send_message(chatid,'terminando juego por inactividad')
				send_marco(chatid,"\n\nJuego terminado\n\n",14)
				matar()
			messageList = sub_client.get_chat_messages(chatId=chatid,size=10)  # Gets messages of each chat
			for nickname, content, id, userid, extensions , tipo , mediaValue, createdTime in zip(messageList.author.nickname, messageList.content, messageList.messageId, messageList.author.id, messageList.extensions,messageList.type, messageList.mediaValue,messageList.createdTime):
				if id in oldMessages: 
					continue
				oldMessages.append(id)
				print(nickname, content)  # Simple output with nickname and messages

				if(content is None ):
					continue
				if(tipo == 111):
					continue
				usersid = []
				replyid = None
				if('mentionedArray' in extensions):
					for m in extensions['mentionedArray']:
						print('mencion a: ' + m['uid'])
						usersid.append(m['uid'])
				if('replyMessageId' in extensions):
					replyid = extensions['replyMessageId']

				m = content[content.find(" "):]
				content = str(content).split(" ")
				if content[0][0] == "/":  
					if(userid in chat.ops ):
						if(content[0][1:] == "sacar"):
							for u in usersid:
								if(len(users) == 1):
									send_message(chatid,'Abandonaron todos terminando juego')
									send_marco(chatid,"\n\nJuego terminado\n\n",14)
									matar()

								if(u in users):
									users.pop(u)
									send_message(chatid,getNickname(u) + " Ha sido removido del juego")
						elif(content[0][1:] == "retos"):

							if(iniciado):
								send_message(chatid,"No se puede cambiar el gif una vez iniciado el juego")
							elif(replyid == None):
								send_message(chatid,"falto referenciar el gif")
							else:
								message = sub_client.get_message_info(chatid,replyid)
								mediaValue = message.json['mediaValue']
								t = message.json['type']

								if(t == 100):
									send_message(chatid,'mensaje eliminado')

								else:
									print(mediaValue)

									if(mediaValue != None and mediaValue[-1:-5:-1][::-1] == '.gif'):
										gifname = mediaValue[mediaValue.rfind('/')+1:]
										if(os.path.exists('gifs/' + gifname)):
											path ='imagenes/' + gifname.replace('.gif','') + '/'
											l = len(os.listdir('imagenes/' + gifname.replace('.gif','') + '/'))
										else:
											img_data = requests.get(mediaValue).content
											with open('gifs/' + gifname,'wb') as h:
												h.write(img_data)
											l = getImagenes(gifname)
										retos = list(range(l))
										random.shuffle(retos)
								
										send_message(chatid,'ok ahora /start para iniciar el juego')
									else:
										send_message(chatid,'no es un gif')

						elif(content[0][1:] == "start"):
							if(iniciado):
								continue
							if(retos == None):
								send_message(chatid,'Falta poner el gif de retos')
							else:
								send_marco(chatid,'Iniciando juego',14)
								turno = 0
								lastTurno = time()
								iniciado = True
								enviarReto(chatid,retos.pop())
						elif(content[0][1:] == "tipoMensaje"):
							if(len(content) == 2):
								if(content[1] == 'normal'):
									tipoMensaje = 0
								elif(content[1] == 'especial'):
									tipoMensaje = 111

						elif(content[0][1:] == "cancelar"):
							send_marco(chatid,"\n\nJuego terminado\n\n",14)
							matar()
					
						elif(content[0][1:] == "limite"):
							if(len(content) == 2 and content[1].isdigit):
								tPorTurno = int(content[1])
								if(tPorTurno != 0 ):
									send_message(chatid,'limite de tiempo por turno: ' + str(tPorTurno))
								else:
									send_message(chatid,'Sin limite de tiempo por turno')
							else:
								send_message(chatid,'uso: /limite [n]: segundos para que se acabe el turno, 0 para infinito')

					if(content[0][1:] == "entrar"):  
						if(userid not in users):
							users[userid] = User(userid,getNickname(userid),0,s=s)
							send_message(chatid,getNickname(userid) + " Se ha unido al juego")

					if(userid not in users):
						continue
					if(content[0][1:] == "listo"):
						if(not iniciado):
							continue
						if(len(retos) == 0 ):
							send_message(chatid,'Se acabaron los retos')
							send_marco(chatid,"\n\nJuego terminado\n\n",14)
							matar()
					
						if(libre):
							enviarReto(chatid,retos.pop())
							turno += 1
						else:
							if(userid == jugadores[turno]):
								turno += 1
								enviarReto(chatid,retos.pop())
							else:
								send_message(chatid,getNickname(userid) + " no es tu turno")
					elif(content[0][1:] == "jugadores"):
						text = 'Jugadores:\n'

						jugadores = list(users.keys())
						i = 1
						for u in jugadores:
							text += '%d. %s\n' % (i,getNickname(u))
							i+=1
						send_message(chatid,text)

					elif(content[0][1:] == "dejar" or content[0][1:] == "salir"):

						if(userid in users):
							if(len(users) == 1):
								send_message(chatid,'Abandonaron todos terminando juego')
								send_marco(chatid,"\n\nJuego terminado\n\n",14)
								matar()
							users.pop(userid)
							send_message(chatid,getNickname(userid) + " Ha abandonado el juego")
					elif(content[0][1:] == "libre"):
						if(content[1] == 'on'):
							send_message(chatid,'modo libre')
							libre = True
						elif(content[1] == 'off'):
							send_message(chatid,'modo por turnos')
							libre = False
					jugadores = list(users.keys())
					if(turno >= len(jugadores) ):
						turno = 0
					if(iniciado and not libre ):
						send_message(chatid,'Turno de ' + getNickname(jugadores[turno]))
		except Exception as e:
			print("error: ")
			print(e)