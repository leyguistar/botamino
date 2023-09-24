import mysql.connector
import datetime
import pytz
import json
from time import time
from time import sleep
from user import User
from chat import Chat
from mensaje import Mensaje
from tipType import TipType
from comando import Comando
from noticia import Noticia
from programa import Programa
from comunidad import Comunidad
from goal import Goal
from intent import Intent
import re
from userStats import UserStats
import unicodedata
import threading
def text2hex(data):
	data = data.encode('latin1').hex()
	result = []
	while data:
		i = data[:32]
		i = i[:8] + '-' + i[8:12] + '-' + i[12:16] + '-' + i[16:20] + '-' + i[20:]
		result.append(i)
		data = data[32:]
	return result
def list2hex(lis):
	data = b''
	for l in lis:
		l = l.replace('-','')
		b = bytes.fromhex(l)
		data += b
	text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')
	return text

class Save:
	def __init__(self,file='default.set',autoConnect=True,connectionTimeOut=60,expected=True,doClose=False):
		if(file):
			with open(file,'r') as h:
				r = h.read().split('\n')
				self.host = r[0]
				self.dbuser = r[1]
				self.password = r[2]
		self.db = mysql.connector.CMySQLConnection()
		self.connectionTimeOut = connectionTimeOut
		self.expected = expected
		self.doClose = doClose
		if(autoConnect):
			self.connect()
	class UnexpectedOpened(Exception):
	    def __init__(*args, **kwargs):
	        Exception.__init__(*args, **kwargs)

	def connect(self):
		if(not self.expected):
			raise self.UnexpectedOpened
		if(not self.db.is_connected()):
			r = self.db.connect(
			  host=self.host,
			  user=self.dbuser,
			  password=self.password,
			  database="amino"
			)
			self.cursor = self.db.cursor()
			# t = threading.Thread(target=self.closeTimeOut,args=(self.connectionTimeOut,) )
			# t.daemon = True
			# t.start()
		else:
			pass
			# self.cursor = self.db.cursor()
			# print('is already connected')
	def __del__(self):
		self.close()
	def closeTimeOut(self,timeout):
		sleep(timeout)
		self.close()
	def conClose(self):
		if(self.doClose):
			self.close()
	def close(self):
		if(self.db.is_connected()):
			self.db.close()		
		else:
			try:
				self.db.close()
			except:
				pass
	def chat(self,chatid,name,alias,bn,mup,mdown,mensaje,ops = [],tips=0,placa='',uid=None,comid=None):
		# print(chatid,name,alias,bn,mup,mdown,mensaje)
		# print('save chat')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		if(name):
			name = name.replace("\\","\\\\").replace('"','\\"')
		else:
			name = ""
		mensaje = mensaje.replace("\\","\\\\").replace('"','\\"')
		

		print('create table if not exists ' + comandos_table + '(nombre varchar(100) primary key,comando text,descripcion text,uid varchar(50));')
		self.cursor.execute('create table if not exists ' + comandos_table + '(nombre varchar(100) primary key,comando text,descripcion text,uid varchar(50));')


		#nuevo
		self.cursor.execute('insert into chats (id,name,alias,bn,mup,mdown,mensaje,tips,placa,uid,comid) \
			values ("%s","%s","%s",%d,%d,%d,"%s","%s","%s","%s",%d);' % 
			(chatid,name,alias,bn,mup,mdown,mensaje,tips,placa,uid,comid))
		data = b''
		for l,v in ops.items():
			l = l.replace('-','')
			b = bytes.fromhex(l)
			data += b
			data += v.to_bytes(4,'big')
		text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')

		self.cursor.execute('insert into ops (chatid,ops) values ("%s","%s");' % (chatid,text))
		self.db.commit()
	def chatBn(self,bn,chatid):
		self.cursor.execute('update chats set bn=%d where id="%s";' % (bn,chatid)) 
		self.db.commit()

	def loadChatMessageType(self,chatid):
		self.cursor.execute('select tipoMensaje from chats_settings where chatid="%s";' % (chatid)) 
		r = self.cursor.fetchone()
		if(r):
			return r[0]
		else:
			return 0
	def loadChatMessageComid(self,chatid):
		self.cursor.execute('select comid from chats where chatid="%s";' % (chatid)) 
		r = self.cursor.fetchone()
		if(r):
			return r[0]
	def chatMessageType(self,tipoMensaje,chatid):
		self.cursor.execute('update chats_settings set tipoMensaje=%d where chatid="%s";' % (tipoMensaje,chatid)) 
		self.db.commit()
	def chatMensajeDonacion(self,mensaje,chatid):
		mensaje = mensaje.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update chats set mensaje_donacion="%s" where id="%s";' % (mensaje,chatid)) 
		self.db.commit()

	def chatMensajeGif(self,mensaje,chatid):
		mensaje = mensaje.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update chats set mensaje_gif="%s" where id="%s";' % (mensaje,chatid)) 
		self.db.commit()

	def chatUid(self,uid,chatid):
		self.cursor.execute('update chats set uid="%s" where id="%s";' % (uid,chatid)) 
		self.db.commit()
	def chatComid(self,comid,chatid):
		self.cursor.execute('update chats set comid="%s" where id="%s";' % (comid,chatid)) 
		self.db.commit()
	def chatStickerBienvenida(self,stickerid,chatid):
		self.cursor.execute('update chats set stickerBienvenida="%s" where id="%s";' % (stickerid,chatid)) 
		self.db.commit()
	def chatStickerDespedida(self,stickerid,chatid):
		self.cursor.execute('update chats set stickerDespedida="%s" where id="%s";' % (stickerid,chatid)) 
		self.db.commit()

	def chatMensaje(self,mensaje,chatid):
		mensaje = mensaje.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update chats set mensaje="%s" where id="%s";' % (mensaje,chatid)) 
		self.db.commit()
	def chatMensajeDespedida(self,mensaje,chatid):
		mensaje = mensaje.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update chats set mensaje_despedida="%s" where id="%s";' % (mensaje,chatid)) 
		self.db.commit()
	def chatMarcos(self,mup,mdown,chatid):
		self.cursor.execute('update chats set mup=%d, mdown=%d where id="%s";' % (mup,mdown,chatid)) 
		self.db.commit()
	def chatPlaca(self,placa,chatid):
		placa = placa.replace("\\","\\\\").replace('"','\\"')
		
		self.cursor.execute('update chats set placa="%s" where id="%s";' % (placa,chatid)) 
		self.db.commit()
	def user(self,id,nickname,mup,mdown,alias,bienvenida,despedida,timezone,premium):
		print('guardando user ' + nickname + 'en la base de datos')
		# print('save user')
		nickname = nickname.replace('\\','\\\\').replace('"',r'\"')
		alias = alias.replace('\\','\\\\').replace('"',r'\"')
		bienvenida = bienvenida.replace('\\','\\\\').replace('"',r'\"')
		despedida = despedida.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('select id from users where id="%s"' % (id) )
		if(len(self.cursor.fetchall()) > 0):
			if(timezone == None):
				self.cursor.execute('update users set nickname="%s", alias="%s", mup=%d, mdown=%d, bienvenida="%s", despedida="%s", premium=%d where id="%s";' % (nickname,alias,mup,mdown,bienvenida,despedida,premium,id) )	
			else:				
				self.cursor.execute('update users set nickname="%s", alias="%s", mup=%d, mdown=%d, bienvenida="%s", despedida="%s", premium=%d,timezone="%s" where id="%s";' % (nickname,alias,mup,mdown,bienvenida,despedida,premium,timezone,id) )	
		else:
			self.cursor.execute('insert into users (id,nickname,alias,mup,mdown,bienvenida,despedida,premium) \
			values ("%s","%s","%s",%d,%d,"%s","%s",%d);' % (id,nickname.replace('\\','\\\\').replace('"',r'\"'),
				alias.replace('\\','\\\\').replace('"',r'\"'),mup,mdown,bienvenida.replace('\\','\\\\').replace('"',r'\"'),
				despedida.replace('\\','\\\\').replace('"',r'\"'),premium))
		self.db.commit()
	def userMarcos(self,mup,mdown,id):
		self.cursor.execute('update users set mup=%d, mdown=%d where id="%s";' % (mup,mdown,id) )	
		self.db.commit()
	def userAlias(self,alias,id):
		self.cursor.execute('update users set alias="%s" where id="%s";' % (alias,id) )	
		self.db.commit()

	def loadChat(self,chatid = None,alias = None):
		# print('load chat')
		if(chatid != None):
			self.cursor.execute('select id,name,alias,bn,mup,mdown,mensaje,tips,placa,uid,comid,mensaje_donacion,stickerBienvenida,stickerDespedida,mensaje_despedida,mensaje_gif from chats where id = "%s";' % (chatid))
		elif(alias != None):
			self.cursor.execute('select id,name,alias,bn,mup,mdown,mensaje,tips,placa,uid,comid,mensaje_donacion,stickerBienvenida,stickerDespedida,mensaje_despedida,mensaje_gif from chats where alias = "%s";' % (alias))
		else:
			return
		result = self.cursor.fetchone()
		if(result == None):
			return None
		ops = self.loadOPS(chatid)
		t = self.loadChatMessageType(chatid)
		return Chat(result[0],result[1],result[2],int(result[3]),int(result[4]),int(result[5]),result[6],ops,s = self,coins=result[7],placa=result[8],uid=result[9],comid=result[10],mensajeDonacion=result[11],stickerBienvenida=result[12],stickerDespedida=result[13],mensajeDespedida=result[14],mensajeGif=result[15],tipoMensaje=t)

	def loadChatComid(self,chatid):
		self.cursor.execute('select comid from chats where id="%s";' % (chatid))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
	def opChat(self,chatid,ops):
		data = b''
		for l,v in ops.items():
			l = l.replace('-','')
			b = bytes.fromhex(l)
			data += b
			data += v.to_bytes(4,'big')
		text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')

		self.cursor.execute('update ops set ops="%s" where chatid="%s";' % (text,chatid))

		self.db.commit()

	def loadOPS(self,chatid):
		self.cursor.execute('select ops from ops where chatid="%s";' % (chatid))
		r = self.cursor.fetchone()

		ops = {}
		if(r):
			data = r[0]
			data = data.encode('latin1')
			while data:
				uid = data[:16].hex()
				uid = uid[:8] + '-' + uid[8:12] + '-' + uid[12:16] + '-' + uid[16:20] + '-' + uid[20:]
			
				level = int.from_bytes(data[16:20],'big')
				data = data[20:]
				ops[uid] = level
		return ops
	def loadAllChats(self):
		# print('load all chats')
		print('select id,name,alias,bn,mup,mdown,mensaje,tips,placa,uid,comid from chats;')
		self.cursor.execute('select id,name,alias,bn,mup,mdown,mensaje,tips,placa,uid,comid from chats;')
		chats = {}
		for result in self.cursor.fetchall():
			ops = self.loadOPS(result[0])
			chats[result[0]] = Chat(result[0],result[1],result[2],int(result[3]),int(result[4]),int(result[5]),result[6],ops,s = self,coins=result[7],placa=result[8],uid=result[9],comid=result[10])
		return chats

	def loadUser(self,id):
		# print('load user')
		self.cursor.execute('select id,nickname,mup,mdown,alias,bienvenida,despedida,timezone,premium,puntos from users where id = "%s";' % (id))
		result = self.cursor.fetchone()
		if(result == None):
			return 
		u = User(result[0],result[1],result[2],result[3],alias=result[4],s = self,bienvenida=result[5],despedida=result[6],premium=result[8],puntos=result[9])
		if(result[7] != None):
			u.timezone = pytz.timezone(result[7])
		return u
	def loadPuntosUser(self,userid):
		self.cursor.execute('select puntos from users where id="%s";' % (userid))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
		return 0
	def loadUserPremium(self,id):
		# print('load user')
		self.cursor.execute('select premium from users where id = "%s";' % (id))
		result = self.cursor.fetchone()
		if(result == None):
			return 
		return result[0]
	def loadAllUsers(self,users={}):
		# print('load all users')
		print('select id,nickname,mup,mdown,alias,bienvenida,despedida,timezone,premium from users;')
		self.cursor.execute('select id,nickname,mup,mdown,alias,bienvenida,despedida,timezone,premium from users;')
		for user in self.cursor:
			users[user[0]] = User(user[0],user[1],user[2],user[3],alias=user[4],s = self,bienvenida=user[5],despedida=user[6],premium=user[8])
			if(user[7] != None):
				users[user[0]].timezone = pytz.timezone(user[7])
		return users

	def createSimpleMessage(self,chatid):
		tableName = 'simple_messages_' + chatid.replace('-','_')
		print('create table if not exists ' + tableName + "(id int primary key auto_increment,uid varchar(36), count int, day int);")
		self.cursor.execute('create table if not exists ' + tableName + "(id int primary key auto_increment,uid varchar(36), count int, day int);")
		self.db.commit()
		
	def simpleMessage(self,chatid,uid,count,day):
		tableName = 'simple_messages_' + chatid.replace('-','_')
		self.cursor.execute('insert into %s (uid,count,day) values ("%s",%d,%d);' % (tableName,uid,count,day))
		self.db.commit()
	def updateSimpleMessage(self,chatid,uid,count,day):
		tableName = 'simple_messages_' + chatid.replace('-','_')
		# print('update %s set count=%d where uid="%s" and day=%d;' % (tableName,count,uid,day))
		self.cursor.execute('update %s set count=%d where uid="%s" and day=%d;' % (tableName,count,uid,day))
		self.db.commit()
	def loadSimpleMessages(self,chatid):
		tableName = 'simple_messages_' + chatid.replace('-','_')
		print('create table if not exists ' + tableName + "(id int primary key auto_increment,uid varchar(36), count int, day int);")
		self.cursor.execute('create table if not exists ' + tableName + "(id int primary key auto_increment,uid varchar(36), count int, day int);")
		self.cursor.execute('select uid,count,day from %s;' % tableName)
		r = self.cursor.fetchall()
		return dict([(i[0],i[1:]) for i in r])
	def loadSimpleMessagesUser(self,chatid,uid):
		tableName = 'simple_messages_' + chatid.replace('-','_')
		self.cursor.execute('select day,count from %s where uid="%s";' % (tableName,uid) )
		r = self.cursor.fetchall()
		print(r)
		return dict(r)
	def loadAllUserMessagesSimple(self,chatid,desde=None,hasta=None):

		tableName = 'simple_messages_' + chatid.replace('-','_')
		print(tableName)
		if(desde and hasta):
			self.cursor.execute('select uid,count from %s where day >= %d and day < %d ;' %
				(tableName,desde,hasta))
		elif(desde):
			self.cursor.execute('select uid,count from %s where day >= %d;' %
				(tableName,desde))
		elif(hasta):
			self.cursor.execute('select uid,count from %s where day < %d;' %
				(tableName,hasta))
		else:
			self.cursor.execute('select uid,count from %s;' %
				(tableName))
		r = self.cursor.fetchall()
		messages = {}
		for i in r:
			if(i[0] not in messages):
				messages[i[0]] = i[1]
			else:
				messages[i[0]] += i[1]			
		return messages

		
	def saveUserMessage(self,nombre,content,tipo,userid):
		# print('save user message')
		table = "saved_user_" + userid.replace('-','_')
		# print(nombre,content,tipo)
		no = nombre
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		content = content.replace("\\","\\\\").replace('"','\\"')
	
		print('create table if not exists ' + table + '(name varchar(50) primary key, content text,tipo int);')
		self.cursor.execute('create table if not exists ' + table + '(name varchar(50) primary key, content text,tipo int);')
		try:
			self.cursor.execute('insert into %s (name,content,tipo) values ("%s","%s",%d);' %
				(table,nombre,content,tipo))
	
		except mysql.connector.IntegrityError as e:
			return 'nombre usado ' + no
		self.db.commit()
		return 'guardado ' + no
	def loadUserSave(self,nombre,userid):
		# print('load user save')
		table = "saved_user_" + userid.replace('-','_')
		print('create table if not exists ' + table + '(name varchar(50) primary key, content text,tipo int);')
		self.cursor.execute('create table if not exists ' + table + '(name varchar(50) primary key, content text,tipo int);')

		table = "saved_user_" + userid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('select content,tipo from %s where name="%s";' %
			(table,nombre))
		return self.cursor.fetchone()

	def deleteUserSave(self,nombre,userid):
		# print('delete user save')
		table = "saved_user_" + userid.replace('-','_')
		print('create table if not exists ' + table + '(name varchar(50) primary key, content text,tipo int);')
		self.cursor.execute('create table if not exists ' + table + '(name varchar(50) primary key, content text,tipo int);')
		
		table = "saved_user_" + userid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('delete from %s where name="%s";' %
			(table,nombre))
		self.db.commit()
	
	def loadUserSaves(self,userid):
		# print('load user saves')
		table = "saved_user_" + userid.replace('-','_')
		print('create table if not exists ' + table + '(name varchar(50) primary key, content text,tipo int);')
		self.cursor.execute('create table if not exists ' + table + '(name varchar(50) primary key, content text,tipo int);')

		table = "saved_user_" + userid.replace('-','_')		
		
		self.cursor.execute('select name,content,tipo from %s;' %
			(table))
	
		return self.cursor.fetchall()
		

	def loadUserMessage(self,nombre,userid):
		# print('load user message')
		table = "saved_user_" + userid.replace('-','_')
		no = nombre
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('select (content,tipo) from ' + table + ' where name="%s"' % (nombre))
		r = self.cursor.fetchone()
		return r


	def loginInfo(self,alias=None,id=None,dictionary=False):
		cursor = self.db.cursor(dictionary=dictionary)
		if(alias != None):
			cursor.execute('select email,password,jsonResponse,lastLogin,sid,secret,id from login where alias="%s";' % (alias) )
		elif(id != None):
			cursor.execute('select email,password,jsonResponse,lastLogin,sid,secret,id from login where id="%s";' % (id) )
		else:
			return
		return cursor.fetchone()
	def newLogin(self,alias=None,id=None,jsonResponse=None):
		if(alias != None):
			self.cursor.execute('update login set jsonResponse=\'%s\' , lastLogin=%d where alias="%s";' % (jsonResponse,time(),alias) )
		elif(id != None):
			self.cursor.execute('update login set jsonResponse=\'%s\' , lastLogin=%d where id="%s";' % (jsonResponse,time(),id) )
		else:
			return
		self.db.commit()
	def newSecret(self,id,secret):
		self.cursor.execute('update login set secret="%s" where id="%s";' % (secret,id))
		self.db.commit()
	def loadBots(self,owner=None,dictionary=False):
		cursor = self.db.cursor(dictionary=dictionary)
		if(owner):
			cursor.execute('select id as userid,name,descripcion as description,owner,public from bots where owner="%s" or public=1;' % owner)
		else:
			cursor.execute('select id as userid,name,descripcion as description,owner,public from bots;')			
		return cursor.fetchall()
	def transferOwner(self,botid,owner):
		self.cursor.execute('update bots set owner="%s" where id="%s";' % (owner,botid))
		self.db.commit()
	def loadBot(self,id):
		self.cursor.execute('select name,descripcion,owner,public from bots where id="%s";' % id)
		return self.cursor.fetchone()
	def loadBotByName(self,name):
		self.cursor.execute('select id,name,descripcion,owner,public from bots where name="%s";' % name)
		return self.cursor.fetchone()
	def media(self,name,content,tipo,chatid):
		name = name.replace('\\','\\\\').replace('"',r'\"')
		table = 'media_chat_' + chatid.replace('-','_')
		print('create table if not exists '+ table +' (name varchar(50) primary key,content text,tipo int);')
		self.cursor.execute('create table if not exists '+ table +' (name varchar(50) primary key,content text,tipo int);')
		print('insert into %s (name,content,tipo) values ("%s","%s",%d);' % 
			(table,name,content,tipo))
		self.cursor.execute('insert into %s (name,content,tipo) values ("%s","%s",%d);' % 
			(table,name,content,tipo))
		self.db.commit()

	def loadMedia(self,chatid,name=None):
		table = 'media_chat_' + chatid.replace('-','_')
		print('create table if not exists '+ table +' (name varchar(50) primary key,content text,tipo int);')
		self.cursor.execute('create table if not exists '+ table +' (name varchar(50) primary key,content text,tipo int);')
		if(name):
			name = name.replace('\\','\\\\').replace('"',r'\"')
			self.cursor.execute('select content,tipo from ' + table + ' where name="%s";' % (name))
			r = self.cursor.fetchone()
		else:
			print('select name,content,tipo as type from ' + table + ';')
			self.cursor.execute('select name,content,tipo as type from ' + table + ';')
			r = self.cursor.fetchall()
		return r

	def deleteMedia(self,name,chatid):
		table = 'media_chat_' + chatid.replace('-','_')
		self.cursor.execute('delete from %s where name="%s";' % (table,name))
		self.db.commit()
	def chatComand(self,nombre,comando,descripcion,userid,chatid):
		# print('save chat event')
		table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		comando = comando.replace('\\','\\\\').replace('"',r'\"')
		descripcion = descripcion.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('insert into %s (nombre,comando,descripcion,uid) values ("%s","%s","%s","%s");' %
				(table,nombre,comando,descripcion,userid))
		self.db.commit()
	def addChatComand(self,nombre,comando,userid,chatid):
		# print('save chat event')
		table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		comando = comando.replace('\\','\\\\').replace('"',r'\"')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key,comando text,descripcion text,uid varchar(50));')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando text,descripcion text,uid varchar(50));')

		self.cursor.execute('select comando,uid from ' + table + ' where nombre = "%s";' % (nombre))
		r = self.cursor.fetchone()
		if(r == None):
			print('El comando no existe')
			return 'El comando no existe'
		if(r[1] == userid or r[1] == None):
			self.cursor.execute('update %s set comando="%s" where nombre="%s";' %
					(table,r[0] + '\0' + comando,nombre))
			self.db.commit()
			return 'Comando agregado a /' + nombre
		else:
			return 'Solo el usuario que hizo el comando puede agregarle mas comandos'
	def loadChatComands(self,chatid):
		table = 'comandos_' + chatid.replace('-','_')
		try:
			print('select nombre,comando,uid,descripcion from ' + table + ';')
			self.cursor.execute('select nombre,comando,uid,descripcion from ' + table + ';')
		except:
			print('create table if not exists ' + table + '(nombre varchar(100) primary key,comando text,descripcion text,uid varchar(50));')
			self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando text,descripcion text,uid varchar(50));')
			return {}
		comandos = {}
		for e in self.cursor.fetchall():	
			comandos[e[0]] = Comando(e[0],e[1].split('\0'),e[2],e[3])
		return comandos
	def removeChatComand(self,nombre,chatid):
		table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		try:
			self.cursor.execute('delete from %s where nombre="%s"; ' % (table,nombre))
			self.db.commit()
		except Exception as e:
			print(e)
			return False
		else:
			return True
	def noticias(self,nombre,descripcion,tipo,fecha):
		table = 'noticias'
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		descripcion = descripcion.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('insert into noticias (fecha,nombre,contenido,tipo) values ("%s","%s","%s",%d);' %
				(fecha.astimezone(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S'),nombre,descripcion,tipo))
		self.db.commit()

	def loadNoticias(self,tipo=None):
		if(tipo == None):
			print('select id,nombre,contenido,tipo,fecha from noticias;')
			self.cursor.execute('select id,nombre,contenido,tipo,fecha from noticias;')
		else:
			self.cursor.execute('select id,nombre,contenido,tipo,fecha from noticias where tipo=%d;' % (tipo))

		noticias = []
		for e in self.cursor.fetchall():	
			noticias.append(Noticia(e[0],e[1],e[2],e[3],e[4]) )
		return noticias
	def loadNoticia(self,id):
		self.cursor.execute('select id,nombre,contenido,tipo,fecha from noticias where id=%d;' % (id))
		e = self.cursor.fetchone()
		if(e == None):
			return None
		return Noticia(e[0],e[1],e[2],e[3],e[4])

	def loadTiposDeNoticia(self):
		print('select id,nombre,descripcion from noticias_tipos;')
		self.cursor.execute('select id,nombre,descripcion from noticias_tipos;')
		e = self.cursor.fetchall()
		return e

	def programar(self,nombre,comando,userid,tipo,minutos,chatid):
		table = 'programa_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key,comando varchar(100),userid varchar(50),tipo int,minutos int,foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando varchar(100),userid varchar(50),tipo int,minutos int,foreign key (comando) references '+ comandos_table +' (nombre) );')

		self.cursor.execute('insert into %s (nombre,comando,userid,tipo,minutos) values ("%s","%s","%s",%d,"%s");' %
				(table,nombre,comando,userid,tipo,minutos))
		self.db.commit()

	def loadChatProgramas(self,chatid):
		table = 'programa_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key,comando varchar(100),userid varchar(50),tipo int,minutos int,foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando varchar(100),userid varchar(50),tipo int,minutos int,foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('select nombre,comando,userid,tipo,minutos from %s;' % (table))
		programas = {}
		for e in self.cursor.fetchall():
			programas[e[0]] = Programa(e[0],e[1],e[2],e[3],e[4])

		return programas
	def deleteChatPrograma(self,nombre,chatid):
		table = 'programa_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key,comando varchar(100),userid varchar(50),tipo int,minutos int,foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando varchar(100),userid varchar(50),tipo int,minutos int,foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('delete from %s where nombre="%s"' % (table,nombre))		
		self.db.commit()

	def bug(self,text,userid,chatid,messageid,fecha):
		text = text.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('insert into bugs (mensaje,userid,chatid,messageid,fecha) values ("%s","%s","%s","%s","%s");' %
				(text,userid,chatid,messageid,fecha))
		self.db.commit()

	def sugerencia(self,text,userid,chatid,messageid,fecha):
		text = text.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('insert into sugerencias (mensaje,userid,chatid,messageid,fecha) values ("%s","%s","%s","%s","%s");' %
				(text,userid,chatid,messageid,fecha))
		self.db.commit()

	def opinion(self,text,userid,chatid,messageid,fecha):
		text = text.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('insert into opiniones (mensaje,userid,chatid,messageid,fecha) values ("%s","%s","%s","%s","%s");' %
				(text,userid,chatid,messageid,fecha))
		self.db.commit()

	def calificar(self,estrellas,userid,comentario=None):
		self.cursor.execute('delete from calificaciones where userid="%s"' % (userid))
		if(comentario == None):
			self.cursor.execute('insert into calificaciones (estrellas,userid) values (%d,"%s");' %
					(estrellas,userid))
		else:
			self.cursor.execute('insert into calificaciones (estrellas,userid,comentario) values (%d,"%s","%s");' %
					(estrellas,userid,comentario))

		self.db.commit()

	def loadEstrellas(self):
		print('select userid,estrellas from calificaciones;')
		self.cursor.execute('select userid,estrellas from calificaciones;')
		calificaciones = {}
		for e in self.cursor.fetchall():
			calificaciones[e[0]] = e[1]
		return calificaciones

	def loadCalificaciones(self):
		print('select userid,estrellas,comentario from calificaciones;')
		self.cursor.execute('select userid,estrellas,comentario from calificaciones;')
		return self.cursor.fetchall()

	def chatUserTag(self,userid,tags,chatid):
		table = 'tags_chat_' + chatid.replace('-','_')

		self.cursor.execute('delete from %s where userid="%s";' % (table,userid))
		print('create table if not exists ' + table + '(userid varchar(50) primary key,tags text );')
		self.cursor.execute('create table if not exists ' + table + '(userid varchar(50) primary key,tags text );')

		self.cursor.execute('insert into %s (userid,tags) values ("%s",\'%s\');' %
				(table,userid,json.dumps(tags).replace('\\','\\\\').replace("'","\\'")))
		self.db.commit()
	def loadChatUserTags(self,chatid):
		table = 'tags_chat_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(userid varchar(50) primary key,tags text );')
		self.cursor.execute('create table if not exists ' + table + '(userid varchar(50) primary key,tags text );')

		self.cursor.execute('select userid,tags from %s;' % (table))
		chatTags = {}
		for e in self.cursor.fetchall():
			chatTags[e[0]] = json.loads(e[1])
		return chatTags
	def UserTag(self,userid,tags):
		self.cursor.execute('delete from user_tags where userid="%s";' % (userid))
		self.cursor.execute('insert into user_tags (userid,tags) values ("%s",\'%s\');' %
				(userid,json.dumps(tags).replace('\\','\\\\').replace("'","\\'")))
		self.db.commit()

	def loadUserTags(self,userid):
		
		self.cursor.execute('select tags from user_tags where userid = "%s";' % (userid))
		r = self.cursor.fetchone()
		if(r == None):
			return None
		return json.loads(r[0])
	def botstate(self,state,pid,comid,premium,chatid):
		self.cursor.execute('delete from botstate where chatid="%s"' % (chatid))
		if(pid != None):
			self.cursor.execute('insert into botstate (state,lastCheck,comid,premium,pid,chatid) values (%d,%d,%d,%d,%d,"%s");' % (state,time(),int(comid),premium,pid,chatid))
		else:
			self.cursor.execute('insert into botstate (state,lastCheck,comid,premium,chatid) values (%d,%d,%d,%d,"%s");' % (state,time(),int(comid),premium,chatid))
		self.db.commit()
	def loadBotstate(self,chatid=None,premium=None,state=None):
		if(chatid != None):
			self.cursor.execute('select state,lastCheck,pid,comid,premium from botstate where chatid="%s";' % (chatid))
			return self.cursor.fetchone()
		elif(premium != None):
			self.cursor.execute('select chatid,state,lastCheck,pid,comid,premium from botstate where premium=%d ;' % (premium))
			return self.cursor.fetchall()
		elif(state != None):
			self.cursor.execute('select chatid,state,lastCheck,pid,comid,premium from botstate where state=%d ;' % (state))
			return self.cursor.fetchall()			
		else:
			print('select chatid,state,lastCheck,pid,comid,premium from botstate ;')
			self.cursor.execute('select chatid,state,lastCheck,pid,comid,premium from botstate ;')
			return self.cursor.fetchall()
	def setBotState(self,state,chatid):
		self.cursor.execute('update botstate set state=%d where chatid="%s"' % (state,chatid))
		self.db.commit()
	def loadChatState(self,chatid):
		self.cursor.execute('select state botstate where chatid="%s";' % (chatid))
		r = self.cursor.fetchone()
		if(not r):
			return
		return r[0]
	def discordGuild(self,discordid,chatid):

		self.cursor.execute('delete from discord_guilds where chatid="%s";' % (chatid))
		self.cursor.execute('insert into discord_guilds (chatid,id) values ("%s","%d");' %
				(chatid,discordid))
		self.db.commit()
	def loadDiscordGuild(self,chatid):
		self.cursor.execute('select id from discord_guilds where chatid="%s";' % (chatid))
		r = self.cursor.fetchone()
		if(r == None):
			return None
		return int(r[0])
	def loadDiscordAminoChats(self,guildid):
		self.cursor.execute('select chatid from discord_guilds where id="%s";' % (guildid))
		return [i[0] for i in self.cursor.fetchall()]

	def discordUser(self,userid,discordid):
		table = 'discord_users'
		self.cursor.execute('delete from discord_users where userid="%s" or discordid = "%s";' % (userid,discordid))
		self.cursor.execute('insert into discord_users (userid,discordid) values ("%s","%s");' %
				(userid,discordid))
		self.db.commit()

	def loadDiscordUser(self,userid=None,discordid=None):
		if(userid != None):
			self.cursor.execute('select discordid from discord_users where userid="%s";' % (userid))
		elif(discordid != None):
			self.cursor.execute('select userid from discord_users where discordid="%s";' % (discordid))
		else:
			return None
		r = self.cursor.fetchone()
		if(r == None):
			return None
		if(userid):
			return int(r[0])
		return r[0]

	def linkDiscordUser(self,discordid,code,nickname):
		self.cursor.execute('select * from discord_verify where code=%d;' % (code))
		if(self.cursor.fetchone() != None):
			return False
		self.cursor.execute('delete from discord_verify where id="%s";' % (discordid))
		self.cursor.execute('insert into discord_verify (id,code,nickname,time) values ("%s",%d,"%s",%d);' %
				(discordid,code,nickname,time()))
		self.db.commit()
		return True
	def loadDiscordUserCode(self,code):

		self.cursor.execute('select id,nickname,time from discord_verify where code=%d;' % (code))
		return self.cursor.fetchone()

	def comandoBienvenida(self,chatid,comando):
		table = 'comandos_bienvenida_' + chatid.replace('-','_')
		comando = comando.replace('\\','\\\\').replace('"',r'\"')
		print('create table if not exists ' + table + '(id int auto_increment primary key,comando text);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,comando text);')
		self.cursor.execute('insert into %s (comando) values ("%s");' %
				(table,comando))
		self.db.commit()
	def loadComandosBienvenida(self,chatid,asDict=True):
		table = 'comandos_bienvenida_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,comando text);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,comando text);')
		self.cursor.execute('select id,comando from %s;' % ( table))
		if(asDict):
			return dict(self.cursor.fetchall())
		else:
			return self.cursor.fetchall()
	def loadComandoBienvenidaMaxId(self,chatid):
		table = 'comandos_bienvenida_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,comando text);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,comando text);')
		self.cursor.execute('select max(id) from %s;' % ( table))
		return self.cursor.fetchone()[0]


	def removeComandoBienvenida(self,chatid,id):
		table = 'comandos_bienvenida_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,comando text);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,comando text);')
		self.cursor.execute('delete from %s where id=%d;' % (table,id))
		self.db.commit()


	def chatGoal(self,monedasTotal,monedas,nombre,comando,userid,chatid):
		table = 'goals_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(monedasTotal int primary key, monedas int ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(monedasTotal int primary key, monedas int ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		if(nombre):
			nombre = nombre.replace("\\","\\\\").replace('"','\\"')
			if(comando):
				self.cursor.execute('insert into %s (monedasTotal,monedas,nombre,comando,userid) values (%d,%d,"%s","%s","%s");' %
						(table,monedasTotal,monedas,nombre,comando,userid))
			else:
				self.cursor.execute('insert into %s (monedasTotal,monedas,nombre,userid) values (%d,%d,"%s","%s");' %
						(table,monedasTotal,monedas,nombre,userid))
		else:
			if(comando):
				self.cursor.execute('insert into %s (monedasTotal,monedas,comando,userid) values (%d,%d,"%s","%s");' %
						(table,monedasTotal,monedas,comando,userid))
			else:
				self.cursor.execute('insert into %s (monedasTotal,monedas,userid) values (%d,%d,"%s");' %
						(table,monedasTotal,monedas,userid))


		self.db.commit()

	def loadChatGoals(self,chatid):
		table = 'goals_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(monedasTotal int primary key, monedas int ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(monedasTotal int primary key, monedas int ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('select monedasTotal,monedas,nombre,comando,userid from %s;' % (table))
		goals = {}
		for e in self.cursor.fetchall():
			goals[e[0]] = Goal(e[0],e[1],e[2],e[3],e[4])
		return goals


	def borrarChatGoal(self,monedasTotal,chatid):
		table = 'goals_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(monedasTotal int primary key, monedas int ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(monedasTotal int primary key, monedas int ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('delete from %s where monedasTotal="%s";' % (table,monedasTotal))		
		self.db.commit()


	def chatGoalUsers(self,cantidad,nombre,comando,userid,chatid):
		table = 'goals_users_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(cantidad int primary key ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(cantidad int primary key ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		if(nombre):
			nombre = nombre.replace("\\","\\\\").replace('"','\\"')
			if(comando):
				self.cursor.execute('insert into %s (cantidad,nombre,comando,userid) values (%d,"%s","%s","%s");' %
						(table,cantidad,nombre,comando,userid))
			else:
				self.cursor.execute('insert into %s (cantidad,nombre,userid) values (%d,"%s","%s");' %
						(table,cantidad,nombre,userid))
		else:
			if(comando):
				self.cursor.execute('insert into %s (cantidad,comando,userid) values (%d,"%s","%s");' %
						(table,cantidad,comando,userid))
			else:
				self.cursor.execute('insert into %s (cantidad,userid) values (%d,"%s");' %
						(table,cantidad,userid))


		self.db.commit()

	def loadChatUsersGoals(self,chatid):
		table = 'goals_users_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(cantidad int primary key ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(cantidad int primary key ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('select cantidad,nombre,comando,userid from %s;' % (table))
		goals = {}
		for e in self.cursor.fetchall():
			goals[e[0]] = Goal(0,0,e[1],e[2],e[3],e[0])
		return goals


	def borrarChatUsersGoal(self,monedasTotal,chatid):
		table = 'goals_users_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(cantidad int primary key ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('create table if not exists ' + table + '(cantidad int primary key ,nombre varchar(100), comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('delete from %s where cantidad="%s";' % (table,monedasTotal))		
		self.db.commit()

	def listaChat(self,nombre,discriminantes,chatid):
		table = 'listas_' + chatid.replace('-','_')
		datatable = 'data_listas_' + chatid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')

		print('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		print('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('insert into %s (nombre,discriminantes) values ("%s","%s");' %
				(table,nombre,'|'.join(discriminantes) ))
		self.db.commit()
	def discriminantesListaChat(self,nombre,discriminantes,chatid):
		table = 'listas_' + chatid.replace('-','_')
		datatable = 'data_listas_' + chatid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		print('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('update %s set discriminantes="%s" where nombre="%s";' %
				(table,'|'.join(discriminantes),nombre ))
		self.db.commit()

	def loadListasChat(self,chatid):
		table = 'listas_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		self.cursor.execute('select nombre,discriminantes from %s;' % (table))
		listas = {}
		for e in self.cursor.fetchall():
			dis = e[1].split('|')
			listas[e[0]] = dis
		return listas


	def borrarListaChat(self,nombre,chatid):
		table = 'listas_' + chatid.replace('-','_')
		datatable = 'data_listas_' + chatid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		print('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('delete from  %s where nombre="%s";' %
				(datatable,nombre))
		self.cursor.execute('delete from %s where nombre="%s";' % (table,nombre))		
		self.db.commit()

	def loadCosasLista(self,nombre,chatid):
		table = 'listas_' + chatid.replace('-','_')
		datatable = 'data_listas_' + chatid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		print('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('select userid,content from %s where nombre="%s";' % (datatable,nombre))
		return self.cursor.fetchall()
	def cosasLista(self,nombre,userid,content,chatid):
		table = 'listas_' + chatid.replace('-','_')
		datatable = 'data_listas_' + chatid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		print('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('insert into %s (nombre,userid,content) values ("%s","%s","%s");' %
				(datatable,nombre,userid,content))
		self.db.commit()
	def borrarCosasLista(self,nombre,userid,content,chatid):
		table = 'listas_' + chatid.replace('-','_')
		datatable = 'data_listas_' + chatid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key, discriminantes text );')
		print('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('create table if not exists ' + datatable + '(id int primary key auto_increment,nombre varchar(50),userid varchar(50),content varchar(100),foreign key (nombre) references '+ table +' (nombre)  );')
		self.cursor.execute('delete from  %s where nombre="%s" and userid="%s" and content="%s";' %
				(datatable,nombre,userid,content))
		self.db.commit()

	def chatSettings(self,chatid,agradecer=None,prefijo=None,ponerMetas=None,ponerEventos=None,voz=None,nsfw=None,espera=None,tipoMensaje=None,maxStrikes=None,otrosBots=None,asteriscos=None,idioma=None,volume=None,sonidos=None,todos=None,bienvenidas=None,despedidas=None,modo=None):
		print('guardando settings')
		table = chatid.replace('-','_')
		if(agradecer != None):
			self.cursor.execute('update chats_settings set agradecer=%d where chatid="%s" ;' % (agradecer,chatid))
		if(prefijo != None):
			prefijo = prefijo.replace("\\","\\\\").replace('"','\\"')
			self.cursor.execute('update chats_settings set prefijo="%s" where chatid="%s" ;' % (prefijo,chatid))
		if(ponerMetas != None):
			self.cursor.execute('update chats_settings set ponerMetas=%d where chatid="%s" ;' % (ponerMetas,chatid))
		if(ponerEventos != None):
			self.cursor.execute('update chats_settings set ponerEventos=%d where chatid="%s" ;' % (ponerEventos,chatid))
		if(voz != None):
			self.cursor.execute('update chats_settings set voz="%s" where chatid="%s" ;' % (voz,chatid))
		if(nsfw != None):
			self.cursor.execute('update chats_settings set nsfw=%d where chatid="%s" ;' % (nsfw,chatid))
		if(espera != None):
			self.cursor.execute('update chats_settings set espera=%d where chatid="%s" ;' % (espera,chatid))
		if(tipoMensaje != None):
			self.cursor.execute('update chats_settings set tipoMensaje=%d where chatid="%s" ;' % (tipoMensaje,chatid))
		if(maxStrikes != None):
			self.cursor.execute('update chats_settings set maxStrikes=%d where chatid="%s" ;' % (maxStrikes,chatid))
		if(otrosBots != None):
			self.cursor.execute('update chats_settings set otrosBots=%d where chatid="%s" ;' % (otrosBots,chatid))			
		if(asteriscos != None):
			self.cursor.execute('update chats_settings set asteriscos=%d where chatid="%s" ;' % (asteriscos,chatid))			
		if(idioma != None):
			self.cursor.execute('update chats_settings set idioma="%s" where chatid="%s" ;' % (idioma,chatid))			
		if(volume != None):
			self.cursor.execute('update chats_settings set volume=%d where chatid="%s" ;' % (volume,chatid))			
		if(sonidos != None):
			self.cursor.execute('update chats_settings set sonidos=%d where chatid="%s" ;' % (sonidos,chatid))			
		if(bienvenidas != None):
			self.cursor.execute('update chats_settings set bienvenidas=%d where chatid="%s" ;' % (bienvenidas,chatid))			
		if(despedidas != None):
			self.cursor.execute('update chats_settings set despedidas=%d where chatid="%s" ;' % (despedidas,chatid))			
		if(todos != None):
			self.cursor.execute('update chats_settings set todos=%d where chatid="%s" ;' % (todos,chatid))	
		if(modo != None):
			self.cursor.execute('update chats_settings set modo=%d where chatid="%s" ;' % (modo,chatid))	
		self.db.commit()
	def loadChatSettings(self,chatid=None):			
		self.cursor = self.db.cursor(dictionary=True)
		if(not chatid):
			print('select * from chats_settings;')
			self.cursor.execute('select * from chats_settings;')
			r = self.cursor.fetchall()
		else:
			self.cursor.execute('select * from chats_settings where chatid="%s";' % (chatid))
			r = self.cursor.fetchone()
			if(not r):
				self.cursor.execute('insert into chats_settings (chatid) values ("%s");' % (chatid))
				self.db.commit()
				self.cursor.execute('select * from chats_settings where chatid="%s";' % (chatid))
				r = self.cursor.fetchone()
			r.pop('chatid')
		self.cursor = self.db.cursor(dictionary=False)
		return r
	def createAppCode(self,userid,code):
		self.cursor.execute('delete from appCode where userid="%s";' % (userid))
		self.db.commit()
		self.cursor.execute('insert into appCode (userid,code,time) values ("%s","%s",%d);' % (userid,code,time()))
		self.db.commit()

	def loadAppCode(self,code):
		self.cursor.execute('delete from appCode where  %d > time+3600;' % (time()))
		self.db.commit()
		self.cursor.execute('select userid from appCode where code=%d;' % (code))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
		return None
	def createLoginToken(self,userid,token):
		self.cursor.execute('insert into webLogin (userid,token,time) values ("%s","%s",%d);' % (userid,token,time()))
		self.db.commit()

	def loadWebLogin(self,token):
		self.cursor.execute('select userid from webLogin where token="%s";' % (token))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
		return None

	def customOP(self,comando,op,chatid):
		table = 'custom_op_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(comando int primary key, op int );')
		self.cursor.execute('create table if not exists ' + table + '(comando int primary key, op int );')
		self.cursor.execute('delete from %s where comando = %d;' % (table,comando))
		self.cursor.execute('insert into %s (comando,op) values (%d,%d);' % (table,comando,op))
		self.db.commit()
	def loadCustomOPS(self,chatid):
		table = 'custom_op_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(comando int primary key, op int );')
		self.cursor.execute('create table if not exists ' + table + '(comando int primary key, op int );')
		self.cursor.execute('select comando,op from %s;' % (table))
		return dict(self.cursor.fetchall())
	def customOpPremium(self,comando,op,chatid):
		table = 'custom_op_premium_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(comando varchar(100) primary key, op int );')
		self.cursor.execute('create table if not exists ' + table + '(comando varchar(100) primary key, op int );')
		self.cursor.execute('delete from %s where comando = "%s";' % (table,comando))
		self.cursor.execute('insert into %s (comando,op) values ("%s",%d);' % (table,comando,op))
		self.db.commit()
	def loadCustomOpsPremium(self,chatid):
		table = 'custom_op_premium_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(comando varchar(100) primary key, op int );')
		self.cursor.execute('create table if not exists ' + table + '(comando varchar(100) primary key, op int );')
		self.cursor.execute('select comando,op from %s;' % (table))
		return dict(self.cursor.fetchall())

	def respuestaChat(self,mensaje,respuesta,chatid):
		table = 'respuestas_' + chatid.replace('-','_')
		mensaje = mensaje.replace("\\","\\\\").replace('"','\\"')
		respuesta = respuesta.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('insert into %s (mensaje,respuesta) values ("%s","%s");' % (table,mensaje,respuesta))
		self.db.commit()
	def respuestaChatEditar(self,mensaje,respuesta,chatid):
		table = 'respuestas_' + chatid.replace('-','_')
		mensaje = mensaje.replace("\\","\\\\").replace('"','\\"')
		respuesta = respuesta.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update %s set respuesta="%s" where mensaje="%s";' % (table,respuesta,mensaje))
		self.db.commit()
	def loadRespuestasChat(self,chatid):
		table = 'respuestas_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('select mensaje,respuesta from %s;' % (table))
		return self.cursor.fetchall()
	def loadRespuestasChatsIds(self,chatid):
		table = 'respuestas_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('select id,mensaje,respuesta from %s;' % (table))
		return self.cursor.fetchall()
	def eliminarRespuestasChat(self,id,chatid):
		table = 'respuestas_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('delete from %s where id=%d;' % (table,id))
		self.db.commit()
	def eliminarRespuestasChatText(self,mensaje,chatid):
		table = 'respuestas_' + chatid.replace('-','_')
		mensaje = mensaje.replace("\\","\\\\").replace('"','\\"')
		print('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,mensaje varchar(200) UNIQUE, respuesta text );')
		self.cursor.execute('delete from %s where mensaje="%s";' % (table,mensaje))
		self.db.commit()

	def intentChat(self,chatid,name,data):
		self.removeIntent(None,chatid,name)
		self.cursor.execute('insert into intents (chatid,name) values ("%s","%s");' % (chatid,name.replace("\\","\\\\").replace('"','\\"')))
		self.cursor.execute('select id from intents where chatid="%s" and name="%s";' % (chatid,name.replace("\\","\\\\").replace('"','\\"')) );
		id = self.cursor.fetchone()[0]
		table = 'intent_' + str(id)
		print('create table if not exists ' + table + '(id int primary key auto_increment, mensaje text,respuesta text,tipo int,state int);')
		self.cursor.execute('create table if not exists ' + table + '(id int primary key auto_increment, mensaje text,respuesta text,tipo int,state int);')
		for i in range(len(data)):
			intentType = data[i]
			if(type(intentType) == tuple or type(intentType) == list):
				self.cursor.execute('insert into %s (mensaje,respuesta,tipo,state) values ("%s","%s",%d,%d);' % (table,'\0'.join(intentType[0]).replace("\\","\\\\").replace('"','\\"'),'\0'.join(intentType[1]).replace("\\","\\\\").replace('"','\\"'),0,i))		
			else:
				print('intentType',intentType)
				for m in intentType:
					print(m,intentType)
					self.cursor.execute('insert into %s (mensaje,respuesta,tipo,state) values ("%s","%s",%d,%d);' % (table,m.replace("\\","\\\\").replace('"','\\"'),'\0'.join(intentType[m]).replace("\\","\\\\").replace('"','\\"'),1,i))		
		self.db.commit()
	def loadIntentsChat(self,chatid,raw=False,web=False):
		self.cursor.execute('select id,name from intents where chatid="%s";' % chatid);
		intents = []
		for id,name in self.cursor.fetchall():
			if(web):
				intents.append({"id":id,"name":name,"data":self.loadIntent(id=id,raw=True)} )
			else:
				intents.append(self.loadIntent(id=id,raw=raw) )

		return intents
	def loadIntent(self,id=None,chatid=None,name=None,raw=False):

		if(not id):
			self.cursor.execute('select id from intents where chatid="%s" and name="%s";' % (chatid,name.replace("\\","\\\\").replace('"','\\"')) );
			id = self.cursor.fetchone()[0]
		i = id
		table = 'intent_' + str(i)
		self.cursor.execute('select mensaje,respuesta,tipo,state from %s;' % (table))
		r = self.cursor.fetchall()
		data = []
		for i in r:
			contentLower = i[0].lower()
			sre = re.sub(
			r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
			unicodedata.normalize( "NFD", contentLower), 0, re.I
			)
			contentLower = unicodedata.normalize('NFKC',sre)

			while(len(data) <= i[3] ):
				data.append({})
			if(i[2] == 0):
				data[i[3]] = (contentLower.split('\0'),i[1].split('\0'))
			else:
				data[i[3]][contentLower.lower()] = i[1].split('\0')
		if(raw):
			return data
		else:
			return Intent(data)
	def removeIntent(self,id=None,chatid=None,name=None):
		if(id):
			print('delete from intents where id=%d;'% (id))
			self.cursor.execute('delete from intents where id=%d;'% (id))
			self.cursor.execute('drop table intent_%d;' % (id))
		elif(chatid and name):	
			print('select id from intents where name="%s" and chatid="%s";'% (name,chatid))
			self.cursor.execute('select id from intents where name="%s" and chatid="%s";'% (name,chatid))
			ids = [x[0] for x in self.cursor.fetchall()]
			print('delete from intents where name="%s" and chatid="%s";'% (name,chatid))
			self.cursor.execute('delete from intents where name="%s" and chatid="%s";'% (name,chatid))
			for id in ids:
				self.cursor.execute('drop table intent_%d;' % (id))
		else:
			return
		self.db.commit()
	def strike(self,chatid,userid,n):
		table = 'strikes_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(userid varchar(50) primary key,n int);')
		self.cursor.execute('create table if not exists ' + table + '(userid varchar(50) primary key,n int);')
		print('delete from %s where userid="%s";'% (table,userid))
		self.cursor.execute('delete from %s where userid="%s";'% (table,userid))
		self.cursor.execute('insert into %s (userid,n) values ("%s",%d);' % (table,userid,n))
		self.db.commit()
	def loadStrikes(self,chatid,userid=None):
		table = 'strikes_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(userid varchar(50) primary key,n int);')
		self.cursor.execute('create table if not exists ' + table + '(userid varchar(50) primary key,n int);')
		if(not userid):
			self.cursor.execute('select userid,n from %s;' % (table))
			return dict(self.cursor.fetchall())
		else:
			self.cursor.execute('select n from %s where userid="%s";' % (table,userid))
			return self.cursor.fetchone()
			


	def process(self,tipo,name,chatid,comid,pid,instanceid):
		print('insert into process (type,name,chatid,comid,pid,instanceid) values (%d,"%s","%s",%d,%d,"%s");' % (tipo,name,chatid,comid,pid,instanceid))
		
		self.cursor.execute('insert into process (type,name,chatid,comid,pid,instanceid) values (%d,"%s","%s",%d,%d,"%s");' % (tipo,name,chatid,comid,pid,instanceid))
		self.db.commit()
		self.cursor.execute('select id from process where instanceid="%s" and pid=%d;' % (instanceid,pid))
		return self.cursor.fetchone()[0]
	def loadProcess(self,id=None):
		if(id):
			self.cursor.execute('select id,type,name,chatid,comid,pid,instanceid from process where id=%d;' % (id))
			return self.cursor.fetchone()
		else:			
			print('select id,type,name,chatid,comid,pid,instanceid from process;')
			self.cursor.execute('select id,type,name,chatid,comid,pid,instanceid from process;')
			return self.cursor.fetchall()
	def loadProcessPid(self,id):
		self.cursor.execute('select pid from process where id=%d;' % (id))
		return self.cursor.fetchone()
	def loadProcessInstance(self,instanceid):
		self.cursor.execute('select id,type,name,chatid,comid,pid,instanceid from process where instanceid="%s";' % (instanceid))
		return self.cursor.fetchall()
	def loadBotsInstance(self,instanceid,count=False):
		if(count):
			self.cursor.execute('select count(*) from process where type=1 and instanceid="%s";' % (instanceid))
			return self.cursor.fetchone()[0]
		else:
			self.cursor.execute('select id,type,name,chatid,comid,pid,instanceid from process where type=1 and instanceid="%s";' % (instanceid))

			return self.cursor.fetchall()
	def loadProcessChat(self,chatid):
		self.cursor.execute('select id,type,name,chatid,comid,pid,instanceid from process where chatid="%s" and type=1;' % (chatid))
		return self.cursor.fetchall()
	def rprocess(self,id=None,instanceid=None,pid=None):
		if(id):
			self.cursor.execute('delete from process where id=%d;' % (id))
		elif(instanceid and pid):
			self.cursor.execute('delete from process where instanceid="%s" and pid=%d;' % (instanceid,pid))
		else:
			return
		self.db.commit()
	def removeProcessInstance(self,instanceid):
		self.cursor.execute('delete from process where instanceid="%s";' % (instanceid))
		self.db.commit()

	def botRequest(self,chatid,userid,comid,instanceid,show=1):
		self.cursor.execute('insert into botrequests (chatid,userid,comid,instanceid,shows) values ("%s","%s",%d,"%s",%d);' % (chatid,userid,comid,instanceid,show))
		self.db.commit()
		
	def loadBotRequests(self,instanceid=None,chatid=None):
		if(instanceid):
			self.cursor.execute('select chatid,userid,comid,instanceid,shows from botrequests where instanceid="%s";' % (instanceid))		
		elif(chatid):
			self.cursor.execute('select chatid,userid,comid,instanceid,shows from botrequests where chatid="%s";' % (chatid))					
		else:
			print('select chatid,userid,comid,instanceid,shows from botrequests;')
			self.cursor.execute('select chatid,userid,comid,instanceid,shows from botrequests;')
		return self.cursor.fetchall()
	def removeBotRequests(self,chatid=None,instanceid=None):
		if(instanceid):
			self.cursor.execute('delete from botrequests where instanceid="%s";' % (instanceid))		
		elif(chatid):
			self.cursor.execute('delete from botrequests where chatid="%s";' % (chatid))		
		self.db.commit()

	def notification(self,title,text,time,tipo,userid):
		self.cursor.execute('insert into notifications (title,texto,time,type,userid) values ("%s","%s",%d,%d,"%s") ' % (title,text,time,tipo,userid))
		self.db.commit()
	def verNotification(self,id,userid):
		table = 'notificaciones_vistas_' + userid.replace('-','_')
		self.cursor.execute('create table if not exists %s (id int primary key);' % (table))
		self.cursor.execute('insert into %s values (%d) ' % (table,id))
		self.db.commit()
	def notificationVistas(self,userid):
		table = 'notificaciones_vistas_' + userid.replace('-','_')
		self.cursor.execute('create table if not exists %s (id int primary key);' % (table))
		print('select id from %s'% (table))
		self.cursor.execute('select id from %s'% (table))
		return [i[0] for i in self.cursor.fetchall()]

	def loadNotifications(self,userid=None):
		if(userid):
			self.cursor.execute('select id,title,texto,time,type,userid from notifications where userid="%s" or userid="*";' % (userid))
		else:
			print('select id,title,texto,time,type,userid from notifications where userid="*";')
			self.cursor.execute('select id,title,texto,time,type,userid from notifications where userid="*";')
		return self.cursor.fetchall()
	def chatUser(self,chatid,userid):
		table = 'chats_user_' + userid.replace('-','_')
		self.cursor.execute('create table if not exists %s (chatid varchar(50) primary key);' % (table))
		try:
			self.cursor.execute('insert into %s values ("%s");' % (table,chatid))
		except mysql.connector.errors.IntegrityError as e:
			if(e.errno == 1062):
				return
			print(e)
			return
		self.db.commit()
	def loadChatsUser(self,userid):
		table = 'chats_user_' + userid.replace('-','_')
		self.cursor.execute('create table if not exists %s (chatid varchar(50) primary key);' % (table))
		self.cursor.execute('select * from %s;' % ( table))
		return [i[0] for i in self.cursor.fetchall()]
	def deleteChatUser(self,chatid,userid):
		table = 'chats_user_' + userid.replace('-','_')
		self.cursor.execute('create table if not exists %s (chatid varchar(50) primary key);' % (table))
		self.cursor.execute('delete from %s where chatid="%s";' % (table,chatid))
		self.db.commit()
	def comandoDonacion(self,chatid,comando,min,max):
		table = 'comandos_donaciones_' + chatid.replace('-','_')
		comando = comando.replace('\\','\\\\').replace('"',r'\"')
		print('create table if not exists ' + table + '(id int auto_increment primary key,comando text, min int, max int);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,comando text, min int, max int);')
		self.cursor.execute('insert into %s (comando,min,max) values ("%s",%d,%d);' %
				(table,comando,min,max))
		self.db.commit()
	def loadComandosDonacion(self,chatid,raw=False):
		table = 'comandos_donaciones_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,comando text, min int, max int);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,comando text, min int, max int);')
		self.cursor.execute('select id,comando,min,max from %s;' % ( table))
		if(raw):
			return self.cursor.fetchall()
		else:
			return dict([(i[0],(i[1],i[2],i[3])) for i in self.cursor.fetchall()])

	def removeComandoDonacion(self,chatid,id):
		table = 'comandos_donaciones_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,comando text, min int, max int);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,comando text, min int, max int);')
		self.cursor.execute('delete from %s where id=%d;' % (table,id))
		self.db.commit()
	def loadComandoDonacionMaxId(self,chatid):
		table = 'comandos_donaciones_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int auto_increment primary key,comando text, min int, max int);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,comando text, min int, max int);')
		self.cursor.execute('select max(id) from %s;' % ( table))
		return self.cursor.fetchone()[0]
	def botChat(self,chatid,botid):
		self.cursor.execute('delete from botchats where chatid="%s";' % (chatid))
		self.cursor.execute('insert into botchats (chatid,botid) values ("%s","%s");' % (chatid,botid))
		self.db.commit()
	def loadBotChat(self,chatid):
		self.cursor.execute('select botid from botchats where chatid="%s";' % (chatid))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
	def loadChatsBot(self,botid):
		self.cursor.execute('select chatid from botchats where botid="%s";' % (botid))
		r = self.cursor.fetchall()
		return [i[0] for i in r]
	def loadBotChats(self):
		print('select chatid,botid from botchats;')
		self.cursor.execute('select chatid,botid from botchats;')
		r = self.cursor.fetchall()
		return dict(r)
	def comandoComunidad(self,comando,comid,op):
		table = 'comandos_comunidad_' + str(comid)
		print('create table if not exists ' + table + '(comando int primary key, op int );')
		self.cursor.execute('create table if not exists ' + table + '(comando int primary key, op int );')
		self.cursor.execute('delete from %s where comando = "%s";' % (table,comando))
		self.cursor.execute('insert into %s (comando,op) values ("%s",%d);' % (table,comando,op))
		self.db.commit()
	def loadComandosComunidad(self,comid):
		table = 'comandos_comunidad_' + str(comid)
		print('create table if not exists ' + table + '(comando int primary key, op int );')
		self.cursor.execute('create table if not exists ' + table + '(comando int primary key, op int );')
		self.cursor.execute('select comando,op from %s;' % (table))
		return dict(self.cursor.fetchall())
	def chatCache(self,chatid,json):
		json = json.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('delete from chats_cache where chatid="%s"; ' % (chatid))
		self.cursor.execute('insert into chats_cache (chatid,json) values ("%s","%s"); ' % (chatid,json))
		self.db.commit()
	def loadChatCache(self,chatid):
		self.cursor.execute('select json from chats_cache where chatid="%s";' % (chatid))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
	def gameChat(self,chatid,pid):
		self.cursor.execute('insert into juegos (chatid,pid) values ("%s",%d); ' % (chatid,pid))
		self.db.commit()
	def loadGamesChat(self,chatid):
		self.cursor.execute('select pid from juegos where chatid="%s";' % (chatid))
		return [i[0] for i in self.cursor.fetchall()]
	def removeGamesChat(self,chatid):
		self.cursor.execute('delete from juegos where chatid="%s";' % (chatid))
		self.db.commit()
	def nombreBot(self,botid,nombre):
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		try:
			self.cursor.execute('update bots set name="%s" where id="%s";' % (nombre,botid))
		except mysql.connector.IntegrityError as e:
			return False
		self.db.commit()
		return True
	def descripcionBot(self,botid,descripcion):
		descripcion = descripcion.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update bots set descripcion="%s" where id="%s";' % (descripcion,botid))
		self.db.commit()

	def respuestaBot(self,mensaje,respuesta,botid):
		return self.respuestaChat(mensaje,respuesta,botid)
	def respuestaBotEditar(self,mensaje,respuesta,botid):
		return self.respuestaChatEditar(mensaje,respuesta,botid)
	def loadRespuestasBot(self,botid):
		return self.loadRespuestasChat(botid)
	def loadRespuestasBotIds(self,botid):
		return self.loadRespuestasChatsIds(botid)
	def eliminarRespuestasBot(self,id,botid):
		return self.eliminarRespuestasChat(id,botid)
	def autorizarBotChat(self,botid,chatid):
		self.cursor.execute('insert into chats_autorizados (chatid,botid) values ("%s","%s");' % (chatid,botid))
		self.db.commit()
	def desautorizarBotChat(self,botid,chatid):
		self.cursor.execute('delete from chats_autorizados where chatid="%s" and botid="%s";' % (chatid,botid))
		self.db.commit()
	def loadChatsAutorizados(self,botid):
		self.cursor.execute('select chatid from chats_autorizados where botid="%s";' % (botid))
		r = self.cursor.fetchall()
		return [i[0] for i in r]
	def removeChatAutorizado(self,botid,chatid):
		self.cursor.execute('delete from chats_autorizados where botid="%s" and chatid="%s";' % (botid,chatid))
		self.db.commit()
	def banUser(self,id,reason=''):
		self.cursor.execute('insert into banned_users (id,razon) values ("%s","%s");' % (id,reason))
		self.db.commit()
	def loadBannedUsers(self,d={}):
		print('select id,razon from banned_users;')
		self.cursor.execute('select id,razon from banned_users;')
		r = self.cursor.fetchall()
		for i in r:
			d[i[0]] = i[1]
		return d

	def unbanUser(self,id):		
		self.cursor.execute('delete from banned_users where id="%s";' % (id))
		self.db.commit()
	def banChat(self,id,reason=''):
		self.cursor.execute('insert into banned_chats (id,razon) values ("%s","%s");' % (id,reason))
		self.db.commit()
	def loadBannedChats(self,d={}):
		print('select id,razon from banned_chats;')
		self.cursor.execute('select id,razon from banned_chats;')
		r = self.cursor.fetchall()
		for i in r:
			d[i[0]] = i[1]
		return d
	def unbanChat(self,id):		
		self.cursor.execute('delete from banned_chats where id="%s";' % (id))
		self.db.commit()
	def banComunidad(self,id,reason=''):
		self.cursor.execute('insert into banned_comunidades (id,razon) values (%d,"%s");' % (id,reason))
		self.db.commit()
	def loadBannedComunidades(self,d={}):
		print('select id,razon from banned_comunidades;')
		self.cursor.execute('select id,razon from banned_comunidades;')
		r = self.cursor.fetchall()
		for i in r:
			d[i[0]] = i[1]
		return d
	def unbanComunidad(self,id):		
		self.cursor.execute('delete from banned_comunidades where id=%d;' % (id))
		self.db.commit()

	def report(self,chatid,messageid,userid,content=''):
		self.cursor.execute('insert into reports (chatid,messageid,userid,content) values ("%s","%s","%s","%s")' % (chatid,messageid,userid,content))
		self.db.commit()
	def banUrl(self,url):
		self.cursor.execute('insert into banned_urls values ("%s");' % (url))
		self.db.commit()
	def loadBannedUrls(self,bannedUrls):
		print('select * from banned_urls;')
		self.cursor.execute('select * from banned_urls;')
		r = self.cursor.fetchall()
		for i in r:
			bannedUrls.append(i[0])
		return bannedUrls
	def roleComunidad(self,comid,nombre,descripcion,color):
		self.cursor.execute('insert into roles (comid,nombre,descripcion,color) values (%d,"%s","%s",%d);' % (comid,nombre,descripcion,color))
		self.db.commit()
	def loadRolesComunidad(self,comid):
		self.cursor.execute('select id,nombre,descripcion,color from roles where comid=%d;' % (comid))
		return dict([(i[0],i[1:]) for i in self.cursor.fetchall()] )
	def deleteRoleComunidad(self,roleid):
		self.cursor.execute('delete from roles where id=%d;' % (roleid))
		self.db.commit()
	def roleUser(self,userid,roleid):
		self.cursor.execute('insert into roles_user (userid,roleid) values ("%s",%d);' % (userid,roleid ))
		self.db.commit()
	def loadRolesUser(self,userid):
		self.cursor.execute('select roleid from roles_user where userid="%s";' % (userid))
		return [i[0] for i in self.cursor.fetchall()]
	def loadUsersConRole(self,roleid):
		self.cursor.execute('select userid from roles_user where roleid=%d;' % (roleid))
		return [i[0] for i in self.cursor.fetchall()]
	def deleteUserRole(self,userid,roleid):
		self.cursor.execute('delete from roles_user where userid="%s" and roleid=%d;' % (userid,roleid))
		self.db.commit()
	def comunidad(self,id,botid=None,wallMessage='',privateChatMessage='',recibir=0):
		if(not botid):
			self.cursor.execute('insert into comunities (id,wallMessage,privateChatMessage,recibir) values (%d,"%s","%s",%d);' % (id,wallMessage,privateChatMessage,recibir))
		else:
			self.cursor.execute('insert into comunities (id,botid,wallMessage,privateChatMessage,recibir) values (%d,"%s","%s","%s",%d);' % (id,botid,wallMessage,privateChatMessage,recibir))			
		self.db.commit()
	def loadComunidad(self,id):
		self.cursor.execute('select id,botid,wallMessage,privateChatMessage,recibir,welcome_chat,bots,welcomeChatMessage from comunities where id=%d;' % (id));

		r = self.cursor.fetchone()
		if(not r):
			return
		return Comunidad(r[0],r[1],r[2],r[3],r[4],r[5],r[7],r[6])
	def loadComunidades(self,comunidades={}):
		print('select id,botid,wallMessage,privateChatMessage,recibir,welcome_chat,bots,welcomeChatMessage from comunities;');
		self.cursor.execute('select id,botid,wallMessage,privateChatMessage,recibir,welcome_chat,bots,welcomeChatMessage from comunities;');
		result = self.cursor.fetchall()
		for r in result:
			comunidades[r[0]] = Comunidad(r[0],r[1],r[2],r[3],r[4],r[5],r[7],r[6])
		return comunidades
	def comunidadRecibir(self,comid,recibir):
		self.cursor.execute('update comunities set recibir=%d where id=%d;' % (recibir,comid))
		self.db.commit()
	def comunidadBot(self,comid,botid):
		self.cursor.execute('update comunities set botid="%s" where id=%d;' % (botid,comid))
		self.db.commit()
	def comunidadIdioma(self,comid,idioma):
		self.cursor.execute('update comunities set idioma="%s" where id=%d;' % (idioma,comid))
		self.db.commit()
	def comunidadChatBienvenidas(self,comid,chatid):
		self.cursor.execute('update comunities set welcome_chat="%s" where id=%d;' % (chatid,comid))
		self.db.commit()

	def comunidadWallMessage(self,comid,message):
		message = message.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update comunities set wallMessage="%s" where id=%d;' % (message,comid))
		self.db.commit()
	def comunidadPrivateMessage(self,comid,message):
		message = message.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update comunities set privateChatMessage="%s" where id=%d;' % (message,comid))
		self.db.commit()
	def comunidadWelcomeChatMessage(self,comid,message):
		message = message.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update comunities set welcomeChatMessage="%s" where id=%d;' % (message,comid))
		self.db.commit()
	def commentWallUser(self,comid,userid):
		self.cursor.execute('insert into commentedUsers (comid,userid) values (%d,"%s");' % (comid,userid))
		self.db.commit()
	def loadCommentedUsers(self,comid):
		self.cursor.execute('select userid from commentedUsers where comid=%d;' % (comid) )
		return [i[0] for i in self.cursor.fetchall()]
	def loadCommentedUser(self,comid,userid):
		self.cursor.execute('select userid from commentedUsers where comid=%d and userid="%s";' % (comid,userid) )
		r = self.cursor.fetchone()
		if(r):
			return True
		else:
			return False
	def addWelcomedUser(self,comid,userid):
		self.cursor.execute('insert into welcomedUsers (comid,userid) values (%d,"%s");' % (comid,userid))
		self.db.commit()
	def loadWelcomedUsers(self,comid):
		self.cursor.execute('select userid from welcomedUsers where comid=%d;' % (comid) )
		return [i[0] for i in self.cursor.fetchall()]
	def loadWelcomedUser(self,comid,userid):
		self.cursor.execute('select userid from welcomedUsers where comid=%d and userid="%s";' % (comid,userid) )
		r = self.cursor.fetchone()
		if(r):
			return True
		else:
			return False

	def mensajesUserComunidad(self,comid,userid,n):
		table = 'mensajes_comunidad_' + str(comid)
		self.cursor.execute('create table if not exists %s(userid varchar(50) primary key, count int); ' % (table))
		self.cursor.execute('delete from %s from userid="%s";' % (table,userid))
		self.cursor.execute('insert into %s (userid,count) values ("%s",%d); ' % (table,userid,n))
		self.db.commit()
	def loadMensajesUserComunidad(self,comid,userid):
		table = 'mensajes_comunidad_' + str(comid)
		self.cursor.execute('create table if not exists %s(userid varchar(50) primary key, count int); ' % (table))
		self.cursor.execute('select count from %s where userid="%s";' % (table,userid))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
		return 0
	def UserStatsChat(self,chatid,userid,stats):
		table = 'stats_users_chat_' + chatid
		for stat,value in stats.items:
			self.cursor.execute('update %s set %s=%d where id="%s";' % (table,stat,value,userid))
		self.db.commit()
	def UserStatChat(self,chatid,userid,stat,value):
		table = 'stats_users_chat_' + chatid
		self.cursor.execute('update %s set %s=%d where id="%s";' % (table,stat,value,userid))
		self.db.commit()
	def loadStatsChat(self,chatid,userid):
		table = 'stats_users_chat_' + chatid
		self.cursor = self.db.cursor(dictionary=True)
		self.cursor.execute('select * from %s	where userid="%s";' % (table,userid))
		self.cursor = self.db.cursor(dictionary=False)
		return self.cursor.fetchone()
	def UserStatsComunidad(self,comid,userid,stats):
		table = 'stats_users_com_' + str(comid)
		for stat,value in stats.items:
			self.cursor.execute('update %s set %s=%d where id="%s";' % (table,stat,value,userid))
		self.db.commit()
	def UserStatComunidad(self,comid,userid,stat,value):
		table = 'stats_users_com_' + str(comid)
		self.cursor.execute('update %s set %s=%d where id="%s";' % (table,stat,value,userid))
		self.db.commit()
	def loadStatsComunidad(self,comid,userid):
		table = 'stats_users_com_' + str(comid)
		self.cursor = self.db.cursor(dictionary=True)
		self.cursor.execute('select * from %s	where userid="%s";' % (table,userid))
		self.cursor = self.db.cursor(dictionary=False)
		return self.cursor.fetchone()

	def UserStats(self,userid,stats):
		for stat,value in stats.items:
			self.cursor.execute('update stats_users set %s=%d where id="%s";' % (stat,value,userid))
		self.db.commit()
	def UserStat(self,userid,stat,value):
		self.cursor.execute('update stats_users set %s=%d where id="%s";' % (stat,value,userid))
		self.db.commit()
	def loadStats(self,userid):
		self.cursor = self.db.cursor(dictionary=True)
		self.cursor.execute('select * from stats_users where userid="%s";' % (userid))
		self.cursor = self.db.cursor(dictionary=False)
		return self.cursor.fetchone()

	def userAutorizadosBotChat(self,chatid,botid,userid):
		table = 'user_autorizados_chat_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int primary key auto_increment, userid varchar(50), botid varchar(50) );')
		self.cursor.execute('create table if not exists ' + table + '(id int primary key auto_increment, userid varchar(50), botid varchar(50) );')
		self.cursor.execute('select userid from %s where botid="%s" and userid="%s";' % (table,botid,userid))
		r = self.cursor.fetchall()
		if(r):
			return
		self.cursor.execute('insert into %s (botid,userid) values ("%s","%s");' % (table,botid,userid))
		self.db.commit()
	def loadUserAutorizadosBotChat(self,chatid,botid=None):
		table = 'user_autorizados_chat_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int primary key auto_increment, userid varchar(50), botid varchar(50) );')
		self.cursor.execute('create table if not exists ' + table + '(id int primary key auto_increment, userid varchar(50), botid varchar(50) );')
		if(botid):
			self.cursor.execute('select userid from %s where botid="%s";' % (table,botid))
			autorizados = [i[0] for i in self.cursor.fetchall()]
		else:
			self.cursor.execute('select botid,userid from %s;' % (table))
			r = self.cursor.fetchall()	
			autorizados = {}
			for b,u in r:
				if(b not in autorizados):
					autorizados[b] = []
				autorizados[b].append(u)
		return autorizados
	def removeUserAutorizadosBotChat(self,chatid,botid,userid):
		table = 'user_autorizados_chat_' + chatid.replace('-','_')
		print('create table if not exists ' + table + '(id int primary key auto_increment, userid varchar(50), botid varchar(50) );')
		self.cursor.execute('create table if not exists ' + table + '(id int primary key auto_increment, userid varchar(50), botid varchar(50) );')
		self.cursor.execute('delete from %s where botid="%s" and userid="%s";' % (table,botid,userid))
		self.db.commit()
	def comunidadesBots(self,comid,botid):
		self.cursor.execute('delete from bots_community where comid=%d and botid="%s";' % (comid,botid))
		self.cursor.execute('insert into bots_community (comid,botid) values (%d,"%s"); ' % (comid,botid))
		self.db.commit()
	def removeComunidadesBots(self,comid,botid):
		self.cursor.execute('delete from bots_community where comid=%d and botid="%s";' % (comid,botid))
		self.db.commit()

	def loadCommunitiesBots(self,botid):
		self.cursor.execute('select comid from bots_community where botid="%s";' % (botid) )
		return [i[0] for i in self.cursor.fetchall()]
	def loadBotsCommunity(self,comid):
		self.cursor.execute('select botid from bots_community where comid=%d;' % (comid) )
		r = self.cursor.fetchall()
		r = [i[0] for i in r]
		r = list(dict.fromkeys(r))
		return r
	def userAutorizado(self,userid,op):
		print('insert into users_autorizados values ("%s",%d);'% (userid,op))
		self.cursor.execute('insert into users_autorizados values ("%s",%d);'% (userid,op))
		self.db.commit()
	def loadUsersAutorizados(self):
		print('select userid,op from users_autorizados;')
		self.cursor.execute('select userid,op from users_autorizados;')
		return dict(self.cursor.fetchall())
	def addPlayRequest(self,chatid,playid,userid):
		self.cursor.execute('insert into musicqueue (chatid,playid,userid) values ("%s","%s","%s");' % (chatid,playid,userid))
		self.db.commit()
	def addAudioRequest(self,chatid,playid,type,texto,idioma):
		self.cursor.execute('insert into musicqueue (chatid,playid,type,texto,idioma) values ("%s","%s",%d,"%s","%s");' % (chatid,playid,type,texto,idioma))
		self.db.commit()
	def setChannelInfo(self,chatid,channel,token,uid,type,volume,botid):
		token = token.replace('\\','\\\\')
		self.cursor.execute('delete from channels where chatid="%s"' % (chatid))
		self.cursor.execute('insert into channels (chatid,channel,token,uid,type,volume,botid) values ("%s","%s","%s",%d,%d,%d,"%s");' % (chatid,channel,token,uid,type,volume,botid))
	def updateChannelVolume(self,chatid,volume):
		self.cursor.execute('update channels set volume=%d where chatid="%s"; ' % (volume,chatid))
		self.db.commit()
	def getActivePlayers(self):
		self.cursor.execute('update players set active=0 where lastTimeActive < %d and active=1;' % (time()-60) )
		self.db.commit()
		self.cursor = self.db.cursor(dictionary=True)
		print('select instanceid,ip,ram,lastTimeActive from players where active=1;')
		self.cursor.execute('select instanceid,ip,ram,lastTimeActive from players where active=1;')
		return self.cursor.fetchall()
	def loadReproduciendo(self,chatid=None):
		if(chatid):
			self.cursor.execute('select playid,ip from reproduciendo where chatid="%s"' % (chatid))
			return self.cursor.fetchone()
		else:
			print('select chatid,playid,ip from reproduciendo;')
			self.cursor.execute('select chatid,playid,ip from reproduciendo;')
			return self.cursor.fetchall()

	def loadReproduciendoip(self,chatid):
		self.cursor.execute('select ip from reproduciendo where chatid="%s"' % (chatid))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
		return None
	def clearQueue(self,chatid):
		self.cursor.execute('delete from musicqueue where chatid="%s";' % (chatid))
		self.db.commit()
	def loadQueue(self,chatid):
		cursor = self.db.cursor(dictionary=True)
		cursor.execute('select playid as id,userid from musicqueue where chatid="%s";' % (chatid))
		return cursor.fetchall()
	def clearReproduciendo(self,chatid):
		self.cursor.execute('delete from reproduciendo where chatid="%s";' % (chatid))
		self.db.commit()
	def addRecibido(self,userid,cosa):
		self.cursor.execute('select %s from recibido where userid="%s";' % (cosa,userid))
		r = self.cursor.fetchone()
		if(not r):
			self.cursor.execute('insert into recibido (userid) values ("%s");' % (userid))
			r = 0
		else:
			r = r[0]
		r += 1
		self.cursor.execute('update recibido set %s=%d where userid="%s"' % (cosa,r,userid))
		self.db.commit()
	def loadRecibido(self,userid):
		cursor = self.db.cursor(dictionary=True)
		cursor.execute('select * from recibido where userid="%s";' % (userid))
		return cursor.fetchone()
	def evento(self,nombre,descripcion,imagen,link,inicio,final):
		self.cursor.execute('insert into eventos (nombre,descripcion,imagen,link,inicio,final) values ("%s","%s","%s","%s","%s","%s");' % (nombre,descripcion,imagen,link,inicio,final))
		self.db.commit()
	def loadEventos(self):
		c = self.db.cursor(dictionary=True)
		c.execute('select nombre,descripcion,imagen,link,inicio,final from eventos; ')
		return c.fetchall()
	def loadInventario(self,userid,asString=False):
		self.cursor.execute('select items from inventario where userid="%s";' % (userid))
		items = self.cursor.fetchone()
		print(items)
		if(not items):
			return []
		items = items[0].split('\0')
		if(asString):
			return items
		return [int(i) for i in items]
	def loadStickers(self,userid=None):
		c = self.db.cursor(dictionary=True)
		c.execute('select id,nombre,descripcion,precio,media,link from items where tipo=2;')
		return c.fetchall()
	def loadItem(self,itemid):
		c = self.db.cursor(dictionary=True)
		c.execute('select * from items where id=%d;' % (itemid))
		return c.fetchone()		
	def loadItemByMedia(self,media):
		c = self.db.cursor(dictionary=True)
		c.execute('select * from items where media="%s";' % (media))
		r = c.fetchall()
		if(len(r) > 1):
			print('re bug')
		return r[0]
	def loadItems(self,tipo=None):
		c = self.db.cursor(dictionary=True)

		if(tipo):
			c.execute('select * from items where tipo=%d;' % (tipo))
		else:
			c.execute('select * from items;')
		return c.fetchall()

	def addItemUser(self,userid,itemid):
		inventario = self.loadInventario(userid,asString=True)
		if(not inventario):
			self.cursor.execute('insert into inventario (userid) values ("%s");' % (userid))
		inventario.append(str(itemid) )
		self.cursor.execute('update inventario set items="%s" where userid="%s";' % ('\0'.join(inventario),userid))
		self.db.commit()

	def addItemTienda(self,tipo,nombre,descripcion,precio,media,link):
		self.cursor.execute('insert into items (tipo,nombre,descripcion,precio,media,link) values (%d,"%s","%s",%d,"%s","%s");' % (tipo,nombre,descripcion,precio,media,link))
		self.db.commit()
	def removeItemUser(self,userid,itemid):
		inventario = self.loadInventario(userid,asString=True)
		if(not inventario):
			return
		try:
			inventario.remove(str(itemid))
		except:
			return
		self.cursor.execute('update inventario set items="%s" where userid="%s";' % ('\0'.join(inventario),userid))
		self.db.commit()
	def updatePuntosUser(self,userid,puntos):
		self.cursor.execute('update users set puntos=%d where id="%s";' %(puntos,userid))
		self.db.commit()
	def addPuntosUser(self,userid,puntos):
		p = self.loadPuntosUser(userid)
		self.updatePuntosUser(userid,p+puntos)
	def playLottery(self,userid,coins):
		self.cursor.execute('insert into loteria (userid,value) values ("%s",%d);' % (userid,coins))
		self.db.commit()
	def resetLottery(self):
		print('delete from loteria;')
		self.cursor.execute('delete from loteria;')
		self.db.commit()
	def loadLottery(self,userid):
		self.cursor.execute('select value from loteria where userid="%s";' % (userid))
		r = self.cursor.fetchone()
		if(r):
			return r[0]
		else:
			return None
	def loadLogros(self,userid,asString=False):
		self.cursor.execute('select logros from logros where userid="%s"' % (userid))
		r = self.cursor.fetchone()
		if(not r):
			return []
		else:
			if(asString):
				return r[0].split('\0')
			return [int(i) for i in r[0].split('\0')]
	def addLogro(self,userid,logro):
		logros = self.loadLogros(userid,asString=True)
		if(not logros):
			self.cursor.execute('insert into logros (userid) values ("%s");' % (userid))
			logros = [str(logro) ]
		else:
			logros.append(str(logro))
		self.cursor.execute('update logros set logros="%s" where userid="%s";' % ('\0'.join(logros),userid))
		self.db.commit()
	def removeLogro(self,userid,logro):
		logro = str(logro)
		logros = self.loadLogros(userid,asString=True)
		if(not logros or logro not in logros):
			return 
		logros.remove(logro)
		self.cursor.execute('update logros set logros="%s" where userid="%s";' % ('\0'.join(logros),userid))
		self.db.commit()
	def escucharAudio(self,userid,n):
		self.cursor.execute('select escuchados from audios_escuchados where userid="%s";' % (userid))
		r = self.cursor.fetchone()
		if(not r):
			l = list('0'*39)
			self.cursor.execute('insert into audios_escuchados (userid) values ("%s")' % (userid))
		else:
			l = list(r[0])
		if(l[n] != '1'):
			l[n] = '1'
			self.cursor.execute('update audios_escuchados set escuchados="%s" where userid="%s"' % (''.join(l),userid) )
			self.db.commit()
			return l.count('1')
		else:
			return 0
	def updateVoto(self,userid,blogid):
		self.cursor.execute('update votos set blogid="%s" where userid="%s";' % (blogid,userid))
		self.db.commit()

	def addVoto(self,userid,blogid):
		self.cursor.execute('insert into votos (blogid,userid) values ("%s","%s");' % (blogid,userid))
		self.db.commit()
	def loadVotos(self):
		print('select userid,blogid from votos;' )
		self.cursor.execute('select userid,blogid from votos;' )
		result = self.cursor.fetchall()
		votos = {}
		for u,b in result:
			votos[u] = b
		return votos
	def loadUsosUser(self,userid,cid):
		self.cursor.execute('select usos from usos where userid="%s" and comando=%d;' % (userid,cid))
		r = self.cursor.fetchone()
		if(not r):
			return 0
		return r[0]
	def updateUsosUser(self,userid,cid,usos):
		self.cursor.execute('select count(*) from usos where userid="%s" and comando=%d;' % (userid,cid))
		r = self.cursor.fetchone()

		if(r[0]):
			self.cursor.execute('update usos set usos=%d where userid="%s" and comando=%d;' % (usos,userid,cid))
		else:
			self.cursor.execute('insert into usos (userid,comando,usos) values ("%s",%d,%d);' % (userid,cid,usos))

		self.db.commit()
	def loadGameRequests(self):
		cursor = self.db.cursor(dictionary=True)
		cursor.execute('select * from gamerequests;')
		return cursor.fetchall()
	def removeGameRequest(self,chatid):
		self.cursor.execute('delete from gamerequests where chatid="%s";' % (chatid))
		self.db.commit()
	def addGameRequest(self,chatid,comid,botid,juego):
		self.cursor.execute('delete from gamerequests where chatid="%s";' % (chatid))
		self.cursor.execute('insert into gamerequests (chatid,comid,botid,juego,t) values ("%s",%d,"%s","%s",%d);' % (chatid,comid,botid,juego,time()))
		self.db.commit()
	def addWaifu(self,nombre,origen,descripcion,wikiId,tipo,img,mal_id=None):
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		origen = origen.replace("\\","\\\\").replace('"','\\"')
		descripcion = descripcion.replace("\\","\\\\").replace('"','\\"')
		if(mal_id):
			self.cursor.execute('insert into waifus (nombre,origen,descripcion,wikiId,tipo,img,mal_id) values ("%s","%s","%s","%s","%s","%s",%d);' % (nombre,origen,descripcion,wikiId,tipo,img,mal_id))
		else:
			self.cursor.execute('insert into waifus (nombre,origen,descripcion,wikiId,tipo,img) values ("%s","%s","%s","%s","%s","%s");' % (nombre,origen,descripcion,wikiId,tipo,img))
		self.db.commit()
	def loadWaifu(self,id):
		cursor = self.db.cursor(dictionary=True)
		cursor.execute('select * from waifus where wikiId="%s";' % (id))
		return cursor.fetchone()
	def loadWaifus(self,waifus=None):
		cursor = self.db.cursor(dictionary=True)
		cursor.execute('select * from waifus where tipo="waifu";')
		r = cursor.fetchall()
		if(waifus == None):
			waifus = {}
		for i in r:
			waifus[i['wikiId']] = i 
		return waifus
	def loadHusbandos(self,waifus=None):
		cursor = self.db.cursor(dictionary=True)
		cursor.execute('select * from waifus where tipo="husbando";')
		r = cursor.fetchall()
		if(waifus == None):
			waifus = {}
		for i in r:
			waifus[i['wikiId']] = i 
		return waifus
	def likeWaifu(self,id,likes):
		data = b''
		for l in likes:
			l = l.replace('-','')
			b = bytes.fromhex(l)
			data += b
		text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update waifulikes set likes="%s" where waifuId="%s";' % (text,id))
		self.db.commit()
	def trashWaifu(self,id,likes):
		data = b''
		for l in likes:
			l = l.replace('-','')
			b = bytes.fromhex(l)
			data += b
		text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update waifulikes set trash="%s" where waifuId="%s";' % (text,id))
		self.db.commit()

	def loadLikesWaifu(self,id):
		self.cursor.execute('select likes,trash from waifulikes  where waifuId="%s";' % (id))
		ids = self.cursor.fetchone()
		if not ids:
			self.cursor.execute('insert into waifulikes (waifuId,likes,trash) values ("%s","","");' % (id))
			self.db.commit()
			return ([],[])
		data = ids[0]
		likes = []
		if(len(data)%16 != 0):
			return ([],[])
		data = data.encode('latin1').hex()
		while data:
			i = data[:32]
			i = i[:8] + '-' + i[8:12] + '-' + i[12:16] + '-' + i[16:20] + '-' + i[20:]
			likes.append(i)
			data = data[32:]
		data = ids[1]
		trash = []
		if(len(data)%16 != 0):
			return (likes,trash)
		data = data.encode('latin1').hex()
		
		while data:
			i = data[:32]
			i = i[:8] + '-' + i[8:12] + '-' + i[12:16] + '-' + i[16:20] + '-' + i[20:]
			trash.append(i)
			data = data[32:]
		return (likes,trash)

	def loadHarem(self,userid):
		self.cursor.execute('select harem from harems where userid="%s";' % (userid))
		ids = self.cursor.fetchone()
		if(not ids):
			self.cursor.execute('insert into harems (userid,harem) values ("%s","");' % (userid))
			self.db.commit()
			return []
		else:
			data = ids[0]
			waifus = []
			data = data.encode('latin1').hex()
			while data:
				i = data[:32]
				i = i[:8] + '-' + i[8:12] + '-' + i[12:16] + '-' + i[16:20] + '-' + i[20:]
				waifus.append(i)
				data = data[32:]
		return waifus
	def loadReclamosWaifu(self,userid):
		self.cursor.execute('select reclamos from harems where userid="%s"' % (userid))
		r = self.cursor.fetchone()
		if(not r):
			self.cursor.execute('insert into harems (userid,harem) values ("%s","");' % (userid))
			self.db.commit()
			return 1
		return r[0]
	def updateReclamos(self,userid,value):
		self.cursor.execute('update harems set reclamos=%d where userid="%s";' % (value,userid))
		self.db.commit()
	def updateHarem(self,userid,harem):
		data = b''
		for l in harem:
			l = l.replace('-','')
			b = bytes.fromhex(l)
			data += b
		text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update harems set harem="%s" where userid="%s";' % (text,userid))
		self.db.commit()
	def ficha(self,nombre,descripcion,objectId,wikiId,icon,comid):
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		descripcion = descripcion.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('insert into fichas (nombre,descripcion,objectId,wikiId,icon,comid) values ("%s","%s","%s","%s","%s",%d);' %
			(nombre,descripcion,objectId,wikiId,icon,comid))
		self.db.commit()
	def borrarFicha(self,comid,objectId,nombre):
		self.cursor.execute('delete from fichas where comid=%d and objectId="%s" and nombre="%s";' % (comid,objectId,nombre))
		self.db.commit()
	def loadFichas(self,fichas):
		cursor = self.db.cursor(dictionary=True)

		cursor.execute('select * from fichas;')
		results = cursor.fetchall()
		for ficha in results:
			comid = ficha['comid']
			objectId = ficha['objectId']
			nombre = ficha['nombre']

			if(comid not in fichas):
				fichas[comid] = {}
			if(objectId not in fichas[comid]):
				fichas[comid][objectId] = {}
			fichas[comid][objectId][nombre] = ficha
		return fichas
	def simpsUser(self,userid,simps):
		print('guardando simps',simps)
		data = b''
		for l in simps:
			l = l.replace('-','')
			b = bytes.fromhex(l)
			data += b
		text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update simps set simps="%s" where userid="%s";' % (text,userid))
		self.db.commit()

	def simpingUser(self,userid,simps):
		data = b''
		for l in simps:
			l = l.replace('-','')
			b = bytes.fromhex(l)
			data += b
		text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('update simps set simping="%s" where userid="%s";' % (text,userid))
		self.db.commit()

	def loadSimps(self,userid):
		self.cursor.execute('select simps,simping from simps where userid="%s";' % (userid))
		ids = self.cursor.fetchone()
		if not ids:
			self.cursor.execute('insert into simps (userid,simps,simping) values ("%s","","");' % (userid))
			self.db.commit()
			return ([],[])
		data = ids[0]
		likes = []
		if(len(data)%16 != 0):
			return ([],[])
		data = data.encode('latin1').hex()
		while data:
			i = data[:32]
			i = i[:8] + '-' + i[8:12] + '-' + i[12:16] + '-' + i[16:20] + '-' + i[20:]
			likes.append(i)
			data = data[32:]
		data = ids[1]
		trash = []
		if(len(data)%16 != 0):
			return (likes,trash)
		data = data.encode('latin1').hex()
		
		while data:
			i = data[:32]
			i = i[:8] + '-' + i[8:12] + '-' + i[12:16] + '-' + i[16:20] + '-' + i[20:]
			trash.append(i)
			data = data[32:]
		return (likes,trash)
