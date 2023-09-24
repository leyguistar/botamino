import mysql.connector
import datetime
import pytz
from user import User
from chat import Chat
from mensaje import Mensaje
from tipType import TipType

class Save:
	def __init__(self):
		self.db = mysql.connector.connect(
		  host="localhost",
		  user="amino",
		  password="amino1234",
		  database="rolamino"
		)
		self.cursor = self.db.cursor()


	def objeto(self,nombre,descripcion,mediaValue):
		table = "objetos"
		self.cursor.execute('create table if not exists ' + table + "(id int primary key auto_increment,nombre varchar(50), descripcion text,mediaValue varchar(100));")
		self.cursor.execute('insert into '+table+' (nombre,descripcion,mediaValue) \
			values ("%s","%s","%s");' % (nombre,descripcion,mediaValue))
		self.db.commit()
	

	def user(self,id,nickname,mup,mdown,alias,bienvenida,despedida,timezone):
		print('guardando user ' + nickname + 'en la base de datos')
		# print('save user')
		nickname = nickname.replace('\\','\\\\').replace('"',r'\"')
		alias = alias.replace('\\','\\\\').replace('"',r'\"')
		bienvenida = bienvenida.replace('\\','\\\\').replace('"',r'\"')
		despedida = despedida.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('select id from users where id="%s"' % (id) )
		if(len(self.cursor.fetchall()) > 0):
			if(timezone == None):
				self.cursor.execute('update users set nickname="%s", alias="%s", mup=%d, mdown=%d, bienvenida="%s", despedida="%s" where id="%s";' % (nickname,alias,mup,mdown,bienvenida,despedida,id) )	
			else:				
				self.cursor.execute('update users set nickname="%s", alias="%s", mup=%d, mdown=%d, bienvenida="%s", despedida="%s",timezone="%s" where id="%s";' % (nickname,alias,mup,mdown,bienvenida,despedida,timezone,id) )	
		else:
			self.cursor.execute('insert into users (id,nickname,alias,mup,mdown,bienvenida,despedida) \
			values ("%s","%s","%s",%d,%d,"%s","%s");' % (id,nickname.replace('\\','\\\\').replace('"',r'\"'),
				alias.replace('\\','\\\\').replace('"',r'\"'),mup,mdown,bienvenida.replace('\\','\\\\').replace('"',r'\"'),
				despedida.replace('\\','\\\\').replace('"',r'\"')))
		self.db.commit()

	def loadChat(self,chatid = None,alias = None):
		# print('load chat')
		if(chatid != None):
			self.cursor.execute('select id,name,alias,bn,mup,mdown,mensaje,ops,tips from chats where id = "%s";' % (chatid))
		elif(alias != None):
			self.cursor.execute('select id,name,alias,bn,mup,mdown,mensaje,ops,tips from chats where alias = "%s";' % (alias))
		else:
			return
		result = self.cursor.fetchone()
		if(result == None):
			return 
		self.cursor.execute('select id,level from %s;' % (result[7]))
		ops = {}
		for op in self.cursor:
			ops[op[0]] = op[1]
		return Chat(result[0],result[1],result[2],int(result[3]),int(result[4]),int(result[5]),result[6],ops,s = self,coins=result[8])



	def loadAllChats(self):
		# print('load all chats')
		self.cursor.execute('select id,name,alias,bn,mup,mdown,mensaje,ops,tips from chats;')
		chats = {}
		for result in self.cursor.fetchall():

			self.cursor.execute('select id,level from %s;' % (result[7]))
			ops = {}
			for op in self.cursor:
				ops[op[0]] = op[1]
			chats[result[0]] = Chat(result[0],result[1],result[2],int(result[3]),int(result[4]),int(result[5]),result[6],ops,s = self,coins=result[8])
		return chats

	def loadUser(self,id):
		# print('load user')
		self.cursor.execute('select id,nickname,mup,mdown,alias,bienvenida,despedida,timezone from users where id = "%s";' % (id))
		result = self.cursor.fetchone()
		if(result == None):
			return 
		u = User(result[0],result[1],result[2],result[3],alias=result[4],s = self,bienvenida=result[5],despedida=result[6])
		if(result[7] != None):
			u.timezone = pytz.timezone(result[7])
		return u
	def loadAllUsers(self):
		# print('load all users')
		self.cursor.execute('select id,nickname,mup,mdown,alias,bienvenida,despedida,timezone from users;')
		users = {}
		for user in self.cursor:
			users[user[0]] = User(user[0],user[1],user[2],user[3],alias=user[4],s = self,bienvenida=user[5],despedida=user[6])
			if(user[7] != None):
				users[user[0]].timezone = pytz.timezone(user[7])
		return users


	def saveMessage(self,chatid,messageid,content,tipo,uid,nickname,createdTime,mediaValue,localMedia,extensions):
		# print('save message')
		if(content != None):
			content = content.replace("\\","\\\\").replace('"',r'\"')
		nickname = nickname.replace("\\","\\\\").replace('"',r'\"')
		tableName = 'messages_' + chatid.replace('-','_')
		
		self.cursor.execute('insert into %s (id,content,type,uid,nickname,createdTime,mediaValue,localMedia,extensions) values\
		 ("%s","%s","%s","%s","%s","%s","%s","%s","%s");' %
		(tableName,messageid,content,tipo,uid,nickname,
			createdTime,mediaValue,localMedia,str(extensions).replace('"',r'\"')))
		self.db.commit()
	def loadMessage(self,chatid,messageid):
		tableName = 'messages_' + chatid.replace('-','_')
		print('select content,type,uid,nickname,createdTime,mediaValue,localMedia,extensions from %s where id="%s";' %
			(tableName,messageid))
		
		self.cursor.execute('select content,type,uid,nickname,createdTime,mediaValue,localMedia,extensions from %s where id="%s";' %
			(tableName,messageid))
		r = self.cursor.fetchone()
		return Mensaje(messageid,r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7])

		
	def saveUserMessage(self,nombre,content,tipo,userid):
		# print('save user message')
		table = "saved_user_" + userid.replace('-','_')
		# print(nombre,content,tipo)
		no = nombre
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		content = content.replace("\\","\\\\").replace('"','\\"')
	
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(50) primary key, content text,type int);')
		try:
			self.cursor.execute('insert into %s (nombre,content,type) values ("%s","%s",%d);' %
				(table,nombre,content,tipo))
	
		except mysql.connector.IntegrityError as e:
			return 'nombre usado ' + no
		self.db.commit()
		return 'guardado ' + no
	def loadUserSave(self,nombre,userid):
		# print('load user save')
		table = "saved_user_" + userid.replace('-','_')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(50) primary key, content text,type int);')

		table = "saved_user_" + userid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('select content,type from %s where nombre="%s";' %
			(table,nombre))
		return self.cursor.fetchone()

	def deleteUserSave(self,nombre,userid):
		# print('delete user save')
		table = "saved_user_" + userid.replace('-','_')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(50) primary key, content text,type int);')
		
		table = "saved_user_" + userid.replace('-','_')
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('delete from %s where nombre="%s";' %
			(table,nombre))
		self.db.commit()
	
	def loadUserSaves(self,userid):
		# print('load user saves')
		table = "saved_user_" + userid.replace('-','_')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(50) primary key, content text,type int);')

		table = "saved_user_" + userid.replace('-','_')		
		
		self.cursor.execute('select nombre,content,type from %s;' %
			(table))
	
		return self.cursor.fetchall()
		

	def loadUserMessage(self,nombre,userid):
		# print('load user message')
		table = "saved_user_" + userid.replace('-','_')
		no = nombre
		nombre = nombre.replace("\\","\\\\").replace('"','\\"')
		self.cursor.execute('select (content,type) from ' + table + ' where nombre="%s"' % (nombre))
		r = self.cursor.fetchone()
		return r

	def loadMessagesID(self,chatid):
		# print('load messages id')
		tableName = 'messages_' + chatid.replace('-','_')
		self.cursor.execute('select id from %s ORDER BY createdTime DESC limit 25;' % (tableName))
		ids = []
		for i in self.cursor:
			ids.append(i[0])
		return ids
	def cargarMarcos(self):
		marcos = [('','')]
		self.cursor.execute('select up,down from marcos;')
		return marcos + self.cursor.fetchall()
	def cargarBienvenidas(self):
		self.cursor.execute('select texto from bienvenidas;')
		b = []
		for i in self.cursor:
			b.append(i[0])
		return b


	def loginInfo(self,alias=None,id=None):
		if(alias != None):
			self.cursor.execute('select email,password from login where alias="%s";' % (alias) )
		elif(id != None):
			self.cursor.execute('select email,password from login where id="%s";' % (id) )
		else:
			return
		return self.cursor.fetchone()

	def media(self,name,descripcion,link,chatid=None,userid=None):
		# print('save media')
		if(name == None or descripcion == None):
			return
		name = name.replace('\\','\\\\').replace('"',r'\"')
		descripcion = descripcion.replace('\\','\\\\').replace('"',r'\"')
		if(chatid != None):
			table = 'media_chat_' + chatid.replace('-','_')
		elif(userid != None):
			table = 'media_user_' + userid.replace('-','_')
		else:
			table = 'media'
		self.cursor.execute('create table if not exists '+ table +' (id int primary key auto_increment, name varchar(50),link text,descripcion text);')
		self.cursor.execute('insert into %s (name,descripcion,link) values ("%s","%s","%s");' % 
			(table,name,descripcion,link))
		self.db.commit()

	def loadMedia(self,name=None,chatid=None,userid=None,id=None):
		# print('load media')
		if(chatid != None):
			table = 'media_chat_' + chatid.replace('-','_')
		elif(userid != None):			
			table = 'media_user_' + userid.replace('-','_')
		else:
			return
		if(name != None):
			name = name.replace('\\','\\\\').replace('"',r'\"')
			self.cursor.execute('select link,id from ' + table + ' where name="%s";' % (name))
			r = self.cursor.fetchall()
			if(len(r) == 0):
				return None
			else:
				return r[0]
		elif(id != None):
			self.cursor.execute('select link,id from ' + table + ' where id=%d;' % (id))
			r = self.cursor.fetchall()
			if(len(r) == 0):
				return None
			else:
				return r[0]
		else:
			self.cursor.execute('select name,descripcion from ' + table + ';')
			r = self.cursor.fetchall()
			return r

	def chatModo(self,name,media_id,announcement,chatid):
		# print('save chat modo')
		table = 'modos_chat_' + chatid.replace('-','_')
		media_table = 'media_chat_' + chatid.replace('-','_')
		name = name.replace('\\','\\\\').replace('"',r'\"')
		announcement = announcement.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + table +
		 '(name varchar(100) primary key, media_id int, announcement text,foreign key (media_id) references '+ media_table +' (id) );')
		try:
			self.cursor.execute('insert into %s (name,media_id,announcement) values ("%s",%d,"%s");' % 
				(table,name,media_id,announcement))
		except mysql.connector.IntegrityError as e:
			self.cursor.execute('update %s set media_id=%d,announcement="%s" where name="%s";' % 
				(table,media_id,announcement,name))
			self.db.commit()
			return 'Modo ' + name + ' actualiazado'
		self.db.commit()
		return 'Modo ' + name + ' agregado' 
			
		


	def loadChatModo(self,name,chatid):
		# print('load chat modo')
		table = 'modos_chat_' + chatid.replace('-','_')
		media_table = 'media_chat_' + chatid.replace('-','_')
		name = name.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + table +
		 '(name varchar(100) primary key, media_id int, announcement text,foreign key (media_id) references '+ media_table +' (id) );')
		self.cursor.execute('select media_id,announcement from %s where name="%s";' % 
			(table,name))
		return self.cursor.fetchone()
	def loadChatModos(self,chatid):
		# print('load chat modos')
		table = 'modos_chat_' + chatid.replace('-','_')
		media_table = 'media_chat_' + chatid.replace('-','_')
		self.cursor.execute('create table if not exists ' + table +
		 '(name varchar(100) primary key, media_id int, announcement text,foreign key (media_id) references '+ media_table +' (id) );')
		self.cursor.execute('select name,media_id,announcement from %s;' % 
			(table))
		modos = {}
		for modo in self.cursor.fetchall():
			modos[modo[0]] = (modo[1],modo[2])
		return modos

	def addUserPack(self,name,stickers,userid):
		# print('add user pack')
		packTable = 'packs_user_' + userid.replace('-','_')
		savesTable = 'saved_user_' + userid.replace('-','_')

		name = name.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + packTable + '(name varchar(100) NOT NULL UNIQUE,id int auto_increment primary key);')
		try:
			self.cursor.execute('insert into %s (name) values ("%s");' % (packTable,name))
		except mysql.connector.IntegrityError as e:
			return 'ya hay un pack con ese nombre'
		self.cursor.execute('select id from %s where name="%s";' % (packTable,name))
		i = self.cursor.fetchone()
		packTable += '_' + str(i[0])
		self.cursor.execute('create table if not exists ' + packTable + '(name varchar(50) primary key,foreign key(name) references '+ savesTable +' (nombre) );')
		self.db.commit()
		for sticker in stickers:
			sticker.replace('\\','\\\\').replace('"',r'\"')
			try:
				self.cursor.execute('insert into %s (name) values ("%s");' % (packTable,sticker))
			except Exception as e:
				print(e)
		self.db.commit()

	def loadUserPack(self,name,userid):
		# print('load user pack')
		packTable = 'packs_user_' + userid.replace('-','_')
		savesTable = 'saved_user_' + userid.replace('-','_')
		name = name.replace('\\','\\\\').replace('"',r'\"')

		self.cursor.execute('select id from %s where name="%s";' % (packTable,name))
		i = self.cursor.fetchone()
		if(i == None):
			return None
		packTable += '_' + str(i[0])
		self.cursor.execute('select name from  ' + packTable + ';')
		return self.cursor.fetchall()		

	def loadUserPacks(self,userid):
		# print('load  user packs')
		packTable = 'packs_user_' + userid.replace('-','_')
		savesTable = 'saved_user_' + userid.replace('-','_')

		self.cursor.execute('select id,name from %s;' % (packTable))
		iss = self.cursor.fetchall()
		packs = {}
		for i,n in iss:
			pt = packTable + '_' + str(i)
			self.cursor.execute('select name from  ' + pt + ';')
			packs[n] = [x[0] for x in self.cursor.fetchall()]
		return packs		

	def chatTips(self,tips,chatid):
		# print('save chat tips')
		table = 'tips_chat_' + chatid.replace('-','_')
		self.cursor.execute('create table if not exists ' + table + '(uid varchar(50) primary key,coins int , lastTime datetime);')
		for tip in tips:
			self.cursor.execute('delete from ' + table + ' where uid="%s";' % (tip) )
			self.cursor.execute('insert into %s (uid,coins,lastTime) values ("%s",%d,"%s");' %
				(table,tip,tips[tip][0],tips[tip][1].strftime('%Y-%m-%d %H:%M:%S')))
		self.db.commit()
	def loadChatTips(self,chatid):
		# print('load chat tips')
		table = 'tips_chat_' + chatid.replace('-','_')
		self.cursor.execute('create table if not exists ' + table + '(uid varchar(50) primary key,coins int , lastTime datetime);')
		self.cursor.execute('select uid,coins,lastTime from ' + table + ' order by coins desc;')
		tips = {}
		for tip in self.cursor.fetchall():
			tips[tip[0]] = (tip[1],tip[2])
		return tips

	def chatEvent(self,fecha,nombre,descripcion,comando,userid,chatid):
		# print('save chat event')
		print(fecha,nombre,descripcion,comando,userid,chatid)
		table = 'eventos_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		descripcion = descripcion.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + comandos_table + '(nombre varchar(100) primary key,comando text,descripcion text);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,fecha datetime,nombre varchar(200), descripcion text,comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		if(comando != None):
			self.cursor.execute('insert into %s (fecha,nombre,descripcion,comando,userid) values ("%s","%s","%s","%s","%s");' %
					(table,fecha.astimezone(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S'),nombre,descripcion,comando,userid))
		else:
			self.cursor.execute('insert into %s (fecha,nombre,descripcion) values ("%s","%s","%s");' %
					(table,fecha.astimezone(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S'),nombre,descripcion))			
		self.db.commit()
	def loadChatEvents(self,chatid):
		# print('load chat events')
		table = 'eventos_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		self.cursor.execute('create table if not exists ' + comandos_table + '(nombre varchar(100) primary key,comando text,descripcion text);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,fecha datetime,nombre varchar(200), descripcion text,comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('delete from ' + table + ' where fecha < UTC_TIMESTAMP();')
		self.cursor.execute('select nombre,descripcion,fecha,comando,userid from ' + table + ';')
		eventos = {}
		for e in self.cursor.fetchall():	
			eventos[e[0]] = (e[1],pytz.timezone("UTC").localize(e[2]),e[3],e[4])
		# print('eventos: ')
		# print(eventos)
		return eventos

	def removeChatEvent(self,nombre,chatid):
		# print('remove chat event')
		table = 'eventos_' + chatid.replace('-','_')
		comandos_table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + comandos_table + '(nombre varchar(100) primary key,comando text,descripcion text);')
		self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,fecha datetime,nombre varchar(200), descripcion text,comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
		self.cursor.execute('delete from %s where nombre="%s"; ' % (table,nombre))
		self.db.commit()

	def chatTipType(self,nombre,desde,gif,font,mensaje,fontSize,chatid):
		table = 'tip_config_chat_' + chatid.replace('-','_')
		mensaje = mensaje.replace('\\','\\\\').replace('"',r'\"')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,desde int,gif varchar(200),font varchar(100), mensaje text,fontSize int);')
		self.cursor.execute('select nombre from %s where nombre="%s"' % (table,nombre) )
		if(len(self.cursor.fetchall()) > 0):
			self.cursor.execute('update users set desde=%d,gif="%s",font="%s",mensaje="%s",fontSize=%d where nombre="%s";' %
			 (desde,gif,font,mensaje,nombre) )			
		else:
			self.cursor.execute('insert into %s (nombre,desde,gif,font,mensaje,fontSize) values \
				("%s",%d,"%s","%s","%s",%d)' % (table,nombre,desde,gif,font,mensaje,fontSize))
		self.db.commit()
		return 'Creado tier ' + nombre + ' desde %d monedas' % (desde)
	def removeTipType(self,nombre,chatid):
		table = 'tip_config_chat_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,desde int,gif varchar(200),font varchar(100), mensaje text,fontSize int);')
		self.cursor.execute('delete from %s where nombre="%s"; ' % (table,nombre))
		self.db.commit()
	def loadChatTipTypes(self,chatid):
		table = 'tip_config_chat_' + chatid.replace('-','_')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,desde int,gif varchar(200),font varchar(100), mensaje text,fontSize int);')
		self.cursor.execute('select nombre,desde,gif,font,mensaje,fontSize from ' + table + ';')
		tipTypes = {}
		for t in self.cursor.fetchall():	
			tipTypes[t[0]] = TipType(t[0],t[1],t[2],t[3],t[4],t[5])
		return tipTypes
	def chatComand(self,nombre,comando,descripcion,chatid):
		# print('save chat event')
		table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		comando = comando.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando text,descripcion text);')
		self.cursor.execute('insert into %s (nombre,comando,descripcion) values ("%s","%s","%s");' %
				(table,nombre,comando,descripcion))
		self.db.commit()
	def addChatComand(self,nombre,comando,chatid):
		# print('save chat event')
		table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		comando = comando.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando text,descripcion text);')
		self.cursor.execute('select comando from ' + table + ' where nombre = "%s";' % (nombre))
		r = self.cursor.fetchone()
		if(r == None):
			print('El comando no existe')
			return 'El comando no existe'
		self.cursor.execute('update %s set comando="%s" where nombre="%s";' %
				(table,r[0] + ',' + comando,nombre))
		self.db.commit()
		return 'Comando agregado a /' + nombre
	def loadChatComands(self,chatid):
		table = 'comandos_' + chatid.replace('-','_')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando text,descripcion text);')
		self.cursor.execute('select nombre,comando,descripcion from ' + table + ';')
		comandos = {}
		for e in self.cursor.fetchall():	
			comandos[e[0]] = (e[1],e[2])
		return comandos
	def removeChatComand(self,nombre,chatid):
		table = 'comandos_' + chatid.replace('-','_')
		nombre = nombre.replace('\\','\\\\').replace('"',r'\"')
		self.cursor.execute('create table if not exists ' + table + '(nombre varchar(100) primary key,comando text,descripcion text);')
		try:
			self.cursor.execute('delete from %s where nombre="%s"; ' % (table,nombre))
			self.db.commit()
			return True
		except Exception as e:
			print(e)
			return False

	# def programar(self,fecha,descripcion,comando,userid,chatid):
	# 	# print('save chat event')
	# 	table = 'programado_' + chatid.replace('-','_')
	# 	comandos_table = 'comandos_' + chatid.replace('-','_')
	# 	descripcion = descripcion.replace('\\','\\\\').replace('"',r'\"')
	# 	self.cursor.execute('create table if not exists ' + comandos_table + '(nombre varchar(100) primary key,comando text,descripcion text);')
	# 	self.cursor.execute('create table if not exists ' + table + '(id int auto_increment primary key,fecha datetime,nombre varchar(200), descripcion text,comando varchar(100),userid varchar(50),foreign key (comando) references '+ comandos_table +' (nombre) );')
	# 	if(comando != None):
	# 		self.cursor.execute('insert into %s (fecha,nombre,descripcion,comando,userid) values ("%s","%s","%s","%s","%s");' %
	# 				(table,fecha.astimezone(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S'),nombre,descripcion,comando,userid))
	# 	else:
	# 		self.cursor.execute('insert into %s (fecha,nombre,descripcion) values ("%s","%s","%s");' %
	# 				(table,fecha.astimezone(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S'),nombre,descripcion))			
	# 	self.db.commit()
