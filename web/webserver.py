#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for, request,Response,make_response
import mysql.connector
import mysql.connector.errors
import amino
import os
import sys
sys.path.insert(1, '../')
from chat import Chat
from save import Save
import linecache
import traceback
import ujson as json
import socket
import ssl
import threading
import random
from intent import Intent
from time import time
from time import sleep
from flask import send_file, send_from_directory, safe_join, abort
import boto3
from botocore.exceptions import ClientError
import secrets
import io
maxProcessInstances = 20
debug = False
if('debug' in sys.argv):
	debug = True
for i in sys.argv:
	if('n=' in i):
		maxProcessInstances = int(i[2:])


logPath = os.environ.get('LOGDIR','../logs') + '/'

savesdir = os.environ.get('SAVESDIR','../saves') + '/'

imgdir = os.environ.get('IMGDIR','../imagenes') + '/'

mediaPath = os.environ.get('MEDIADIR','../media') + '/'

sql_connection_file = '../default.set'

chain_key = ('/etc/letsencrypt/live/leybot.leyguistar.com/fullchain.pem','/etc/letsencrypt/live/leybot.leyguistar.com/privkey.pem')
		
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    traceback.print_exc()
    with open('../errores.txt','a') as h:
    	h.write('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    	traceback.print_exc(file=h)

# from flask_mysqldb import MySQL
# db = mysql.connector.connect(
#   host="localhost",
#   user="amino",
#   password="amino1234",
#   database="amino"
# )
# cursor = db.cursor()
controlCon = {}
liteCon = None
ley = 'your_uuid'
userBot = 'shita'
comid = '67'
for i in sys.argv:
	if('comid=' in i):
		comid = i[6:]
	if('user=' in i):
		userBot = i[5:]

class User:
	def __init__(self,icon,nickname,level):
		self.icon = icon
		self.nickname = nickname
		self.level = level
# class Chat:
# 	def __init__(self,mensaje,mup,mdown):
# 		self.mensaje = mensaje
# 		self.mup = mup
# 		self.mdown = mdown
"""
Cosas aws

"""

def upload_s3_io(b,object_name,bucket='leybot-amino-data'):
	s3_client = boto3.client('s3')
	try:
	    response = s3_client.upload_fileobj(b, bucket, object_name,ExtraArgs={'ACL': 'public-read'})
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


"""

Cosas de amino

"""
def loginAmino(botid):
	s = Save(file=sql_connection_file)
	login = s.loginInfo(id=botid)
	client = amino.Client(nosocket=True)
	if(login[2] and login[3] + 3600 > time()):
		print('inicio cache')
		client.login_cache(login[2] )
	else:
		print('iniciando normal')
		r = client.login(email=login[0],password=login[1],get=True)
		if(type(r) == dict or r[0] != 200):
		    print(r)
		    return None
		r1 = json.loads(r[1])
		r1['userProfile']['content'] = 'cache'
		r1 = json.dumps(r1)
		s.newLogin(id=client.profile.id,jsonResponse=r1)
	return client


def getChatsData(userid):
	s = Save(file=sql_connection_file)
	userChats = s.loadChatsUser(userid)
	chats = []
	if(debug):
		userChats = userChats[:10]
	print(chats)
	for chatid in userChats:
		if(not chatid):
			continue
		deleted = False

		chat = s.loadChat(chatid)
		chatCache = s.loadChatCache(chatid)
		if(chatCache == None):
			botid = s.loadBotChat(chatid)
			
			if(not botid):
				bots = s.loadBots(None)
				for bot in bots:
					client = loginAmino(bot[0])
					if(not client):
						continue
					sub_client = client.sub_client(chat.comid)
					t = sub_client.get_chat_thread(chatid,raw=True)
					statuscode = t['api:statuscode']

					if(statuscode != 0):
						print(chatid,t['api:statuscode'])
						if(t['api:statuscode'] == 1600):
							s.deleteChatUser(chatid,userid)
							deleted = True
							break
						elif(statuscode == 105):
							continue
					else:
						break
				else:
					print('no encontrada informacion del chat',chatid)
					s.deleteChatUser(chatid,userid)
				if(deleted):
					continue
				t = t['thread']
				if(t['status'] == 10):
					s.deleteChatUser(chatid,userid)
					continue
			else:
				client = loginAmino(botid)
				sub_client = client.sub_client(chat.comid)
				t = sub_client.get_chat_thread(chatid,raw=True)
				statuscode = t['api:statuscode']

				if(statuscode != 0):
					if(t['api:statuscode'] == 1600):
						s.deleteChatUser(chatid,userid)
						continue
					elif(statuscode == 105):
						continue
				t = t['thread']
				if(t['status'] == 10):
					s.deleteChatUser(chatid,userid)
					continue
			s.chatCache(chatid,json.dumps(t))
			chatCache = t
		else:
			chatCache = json.loads(chatCache)
		chatCache['mensaje'] = chat.mensaje
		chatCache['mup'] = chat.mup
		chatCache['mdown'] = chat.mdown
		estado = s.loadBotstate(chatid)
		chatCache['ops'] = s.loadOPS(chatid)
		if(not estado):
			chatCache['estado'] = 0
		else:
			chatCache['estado'] = estado[0]
		chats.append(chatCache)
	return chats


"""

Pagina web

"""

app = Flask(__name__)

@app.route('/')
def start():
	return render_template("index.html",icon=None)
"""

Conexion con la api

"""

@app.route('/api/login',methods=['GET','POST'])
def loginApi():
	s = Save(file=sql_connection_file)
	code = request.headers.get('code')
	userid = s.loadAppCode(int(code,16))
	if(userid):
		token = secrets.token_urlsafe(128)
		s.createLoginToken(userid,token)
		return '{"result":"ok","userid":"%s","token":"%s"}' % (userid,token)
	else:
		return '{"result":"codigo incorrecto"}'

@app.route('/api/chats',methods=['GET','POST'])
def chatsApi():
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')
	userid = s.loadWebLogin(token)
	if(userid):
		chats = getChatsData(userid)
		resp = {"result":"ok","chats":chats}
		resp = json.dumps(resp)
		return resp
	else:
		return '{"result":"no"}'

@app.route('/api/bots',methods=['GET','POST'])
def getBotsApi():
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')
	userid = s.loadWebLogin(token)
	if(userid == ley):
		bots = s.loadBots(owner=None)	
	else:
		bots = s.loadBots(owner=userid)
	js = []
	for bot in bots:
		t = {}
		t['id'] = bot[0]
		t['name'] = bot[1]
		t['descripcion'] = bot[2]
		t['owner'] = bot[3]
		js.append(t)
	js = {"result":"ok","bots":js}
	return json.dumps(js)
@app.route('/api/chat/<chatid>/estado',methods=['GET','POST'])
def chatEstadoApi(chatid):
	s = Save(file=sql_connection_file)
	if(request.method == 'POST'):
		token = request.headers.get('token')
		userid = s.loadWebLogin(token)
		estado = request.json.get('estado')
		comid = request.json.get('comid')
		if(not userid):
			return '{"result":"error de autorizacion"}'
		s.botstate(estado,0,comid,0,chatid)

	estado = s.loadBotstate(chatid)

	if(estado):
		print(estado)
		return '{"result":"ok","estado":%d}' % (estado[0])
	else:
		return '{"result":"chat no encontrado"}'


	return '{"result":"error"}'
@app.route('/api/chat/<chatid>/guardar',methods=['GET','POST'])
def chatGuardarApi(chatid):
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')
	mensaje = request.json.get('mensaje')
	mup = request.json.get('mup')
	mdown = request.json.get('mdown')
	s.chatMensaje(mensaje,chatid)	
	print(mup,mdown)		
	s.chatMarcos(mup,mdown,chatid)
	s.botstate(3,0,comid,0,chatid)
	return '{"result":"ok","estado":3}'

@app.route('/api/chat/<chatid>/add',methods=['GET','POST'])
def chatAgregarApi(chatid):
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')
	comid = request.json.get('comid')
	userid = s.loadWebLogin(token)
	s.cursor = s.db.cursor(dictionary=True)
	bots = s.loadBots(owner=userid)
	bots = dict([(i['userid'],i) for i in bots])
	state = s.loadChatState(chatid)
	if(state != 1):
		return '{"result":"el bot no se encuentra activado en ese chat"}'

	botid = s.loadBotChat()
	if((botid not in bots) and userid != ley ):
		return '{"result":"el bot actual de este chat no te pertenece"}'
	try:
		s.chatUser(chatid,userid)
	except Exception as e:
		print(e)
		return '{"result":"error agregando chat"}'

	return '{"result":"ok"}'


@app.route('/api/chat/<chatid>/comandos',methods=['GET','POST'])
def chatComandosApi(chatid):
	s = Save(file=sql_connection_file)
	if(request.method == 'GET'):
		token = request.headers.get('token')
		opCustom = s.loadCustomOPS(chatid)
		for c in comandos:
			if(c not in opCustom):
				opCustom[c] = comandos[c][0]
		sorted_dict = dict(sorted(opCustom.items(), key=lambda item: item[0]))
		response = {"result":"ok","comandos":sorted_dict}
		return json.dumps(response)
	elif(request.method == "POST"):
		comandos2 = request.json.get('comandos')
		for c in comandos:
			v = int(comandos2.get(c))
			if(v != comandos[c][0] ):
				print(c,v,comandos[c][0])
				s.customOP(c,v,chatid)
		s.botstate(3,0,comid,0,chatid)
		return '{"result":"ok"}'

@app.route('/api/chat/<chatid>/respuestas',methods=['GET','POST','DELETE'])
def chatRespuestasApi(chatid):
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')

	if(request.method == 'GET'):
		respuestas = s.loadRespuestasChatsIds(chatid)
		rjson = [{"id":r[0],"mensaje":r[1],"respuesta":r[2]} for r in respuestas]
		# for r in respuestas:
		# 	rjson.append({"id":r[0],"mensaje":r[1],"respuesta":r[1]})
		resp = {"result":"ok","respuestas":rjson}
		return json.dumps(resp)
	elif(request.method == "POST"):
		mensaje = request.json.get('mensaje')
		respuesta = request.json.get('respuesta')
		editar = request.json.get('editar')
		print(mensaje,respuesta)
		if(editar):
			s.respuestaChatEditar(mensaje,respuesta,chatid)
		else:
			try:
				s.respuestaChat(mensaje,respuesta,chatid)
				s.botstate(3,0,comid,0,chatid)
			except Exception as e:
				print(e)
				print('mensaje repetido')
				return '{"result":"mensaje repetido"}'
		s.setBotState(3,chatid)
		return '{"result":"ok"}'
	elif(request.method == "DELETE"):
		id = request.values.get('id')
		print(id)
		s.eliminarRespuestasChat(int(id),chatid)
		s.setBotState(3,chatid)
		return '{"result":"ok"}'

@app.route('/api/bot/<botid>/respuestas',methods=['GET','POST','DELETE'])
def botRespuestasApi(botid):
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')

	if(request.method == 'GET'):
		respuestas = s.loadRespuestasBotIds(botid)
		rjson = [{"id":r[0],"mensaje":r[1],"respuesta":r[2]} for r in respuestas]
		# for r in respuestas:
		# 	rjson.append({"id":r[0],"mensaje":r[1],"respuesta":r[1]})
		resp = {"result":"ok","respuestas":rjson}
		return json.dumps(resp)
	elif(request.method == "POST"):
		mensaje = request.json.get('mensaje')
		respuesta = request.json.get('respuesta')
		editar = request.json.get('editar')
		print(mensaje,respuesta)
		if(editar):
			s.respuestaBotEditar(mensaje,respuesta,botid)
		else:
			try:
				s.respuestaBot(mensaje,respuesta,botid)
				s.botstate(3,0,comid,0,botid)
			except Exception as e:
				print(e)
				print('mensaje repetido')
				return '{"result":"mensaje repetido"}'
		s.setBotState(3,botid)
		return '{"result":"ok"}'
	elif(request.method == "DELETE"):
		id = request.values.get('id')
		print(id)
		s.eliminarRespuestasBot(int(id),botid)
		s.setBotState(3,botid)
		return '{"result":"ok"}'


@app.route('/api/chat/<chatid>/comandos/bienvenida',methods=['GET','POST','DELETE'])
def chatBienvenidasApi(chatid):
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')

	if(request.method == 'GET'):
		s.cursor = s.db.cursor(dictionary=True)	
		comandos = s.loadComandosBienvenida(chatid,asDict=False)
		resp = {"result":"ok","comandos":comandos}
		return json.dumps(resp)
	elif(request.method == "POST"):
		token = request.headers.get('token')
		comando = request.json.get('comando')
		s.comandoBienvenida(chatid,comando)
		i = s.loadComandoBienvenidaMaxId(chatid)
		s.setBotState(3,chatid)

		return '{"result":"ok","id":%d}' % (i)
	elif(request.method == "DELETE"):
		id = request.values.get('id')
		print(id)
		s.removeComandoBienvenida(chatid,int(id))
		s.setBotState(3,chatid)

		return '{"result":"ok"}'

@app.route('/api/chat/<chatid>/comandos/donacion',methods=['GET','POST','DELETE'])
def chatDonacionesApi(chatid):
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')

	if(request.method == 'GET'):
		s.cursor = s.db.cursor(dictionary=True)	
		comandos = s.loadComandosDonacion(chatid,raw=True)
		resp = {"result":"ok","comandos":comandos}
		print(resp)
		return json.dumps(resp)
	elif(request.method == "POST"):
		token = request.headers.get('token')
		comando = request.json.get('comando')
		mi = request.json.get('min')
		ma = request.json.get('max')

		s.comandoDonacion(chatid,comando,mi,ma)
		i = s.loadComandoDonacionMaxId(chatid)
		print(3,chatid)
		s.setBotState(3,chatid)

		return '{"result":"ok","id":%d}' % (i)
	elif(request.method == "DELETE"):
		id = request.values.get('id')
		print(id)
		s.removeComandoDonacion(chatid,int(id))
		s.setBotState(3,chatid)

		return '{"result":"ok"}'




@app.route('/api/chat/<chatid>/ops',methods=['GET','POST','DELETE'])
def chatOpsApi(chatid):
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')

	if(request.method == 'GET'):
		users = []
		ops = s.loadOPS(chatid)
		for u in ops:
			user = s.loadUser(u)
			users.append({'nickname':user.nickname,'id':u,'alias':user.alias,'op':ops[u]})
		resp = {"result":"ok","ops":users}
		return json.dumps(resp)
	elif(request.method == "POST"):
		token = request.headers.get('token')
		ops = request.json.get('ops')
		print(chatid,ops)
		s.opChat(chatid,ops)	
		return '{"result":"ok"}'
	elif(request.method == "DELETE"):
		id = request.values.get('id')
		print(id)
		s.opChatDel(id,chatid)
		return '{"result":"ok"}'

@app.route('/api/chat/<chatid>/intents',methods=['GET','POST','DELETE'])
def chatIntentApi(chatid):
	s = Save(file=sql_connection_file)
	if(request.method == 'POST'):
		token = request.headers.get('token')
		name = request.json.get('name')
		data = request.json.get('data')
		print(name)
		print(data)
		s.intentChat(chatid,name,data)
		s.setBotState(3,chatid)
	elif(request.method == 'DELETE'):
		id = request.values.get('id')
		print(id)
		s.removeIntent(int(id))
		s.setBotState(3,chatid)
		
	intents = s.loadIntentsChat(chatid,web=True)
	return json.dumps({'result':'ok','intents':intents})
@app.route('/api/saves',methods=['GET','POST','DELETE'])
def userSavesApi():
	if(request.method=='GET'):
		print('metodo get')
		token = request.headers.get('token')
		s = Save(file=sql_connection_file)
		userid = s.loadWebLogin(token)
		if(not userid):
			return '{"result":"error de token"}'
		# if('name' in request.values):
		# 	name = request.values['name']
		# 	content,tipo = s.loadUserSave(name,userid)
		# 	if(tipo == 0):
		# 		return {'result':'ok','name':name,'type':tipo,'content':content}
		# 	try:
		# 		return send_from_directory(app.config["CLIENT_IMAGES"], filename=name, as_attachment=True)
		# 	except FileNotFoundError:
		# 		abort(404)
		saves = s.loadUserSaves(userid)
		d = []
		for sv in saves:
			d.append(dict(zip(['name','content','type'],sv)) )
		return json.dumps({'result':'ok','saves':d})
	elif(request.method=='POST'):
		print('ok')
		token = request.files['token'].filename
		s = Save(file=sql_connection_file)
		userid = s.loadWebLogin(token)
		print('add save request by ',userid)
		for i in request.files:
			print(i,request.files.get(i))
			if(i == 'file'):
				f = request.files.get(i)
				name = f.filename[:f.filename.find('/')]
				content = str(time()).replace('.','') +'.'+ f.filename[f.filename.rfind('/')+1:]
				print('guardando ' + name)
				b = io.BytesIO()
				f.save(b)
				b.seek(0)
				upload_s3_io(b,'saves/' + userid + '/' + content)
				s.saveUserMessage(name,'https://leybot-amino-data.s3.amazonaws.com/saves/' + userid + '/' + content,2,userid)
			elif(i == 'text'):
				f = request.files.get(i)
				name = f.filename
				content = f.stream.read().decode('utf-8')
				s.saveUserMessage(name,content,0,userid)
		print('enviando saves')
		saves = s.loadUserSaves(userid)
		d = []
		for sv in saves:
			d.append(dict(zip(['name','content','type'],sv)) )

		return json.dumps({'result':'ok','saves':d})
	elif(request.method=='DELETE'):
		token = request.headers.get('token')
		s = Save(file=sql_connection_file)
		userid = s.loadWebLogin(token)
		name = request.values.get('name')
		r = s.loadUserSave(name,userid)
		if(r == None):
			return json.dumps({'result':'no se encontro el save'})
			
		c,t = r
		if(t == 2):
			try:
				os.remove('saves/' + c)
			except Exception as e:
				print(e)
		s.deleteUserSave(name,userid)

			# print(i)
			# print(type(f))
		return json.dumps({'result':'ok'})
			# print(f)
	return json.dumps({'result':'error'})

@app.route('/api/<chatid>/media',methods=['GET','POST','DELETE'])
def loadMedia(chatid):
	if(request.method=='GET'):
		print('metodo get')
		token = request.headers.get('token')
		s = Save(file=sql_connection_file)
		userid = s.loadWebLogin(token)
		if(not userid):
			return '{"result":"error de login"}'
		s.cursor = s.db.cursor(dictionary=True)	
		saves = s.loadMedia(chatid)
		return json.dumps({'result':'ok','saves':saves})
	elif(request.method=='POST'):
		print('ok')
		token = request.files['token'].filename
		s = Save(file=sql_connection_file)
		userid = s.loadWebLogin(token)
		print('add save request by ',userid)
		for i in request.files:
			print(i,request.files.get(i))
			saves = s.loadMedia(chatid)
			names = [i[0] for i in saves]
			if(i == 'file'):
				f = request.files.get(i)
				name = f.filename[:f.filename.find('/')]
				print('por aqui')
				if(name in names):
					return {'result':'nombre usado %s' % (name)}
				content = str(time()).replace('.','') +'.'+ f.filename[f.filename.rfind('/')+1:]
				print('guardando ' + name)
				b = io.BytesIO()
				f.save(b)
				b.seek(0)
				upload_s3_io(b,'media/' + chatid + '/' + content)
				s.media(name,'https://leybot-amino-data.s3.amazonaws.com/media/' + chatid + '/' + content,2,chatid)
			elif(i == 'text'):
				f = request.files.get(i)
				name = f.filename
				if(name in names):
					return {'result':'nombre usado %s' % (name)}
				content = f.stream.read().decode('utf-8')
				s.media(name,content,0,chatid)
		print('enviando saves')
		s.cursor = s.db.cursor(dictionary=True)	
		saves = s.loadMedia(chatid)
		return json.dumps({'result':'ok','saves':saves})
	elif(request.method=='DELETE'):
		token = request.headers.get('token')
		s = Save(file=sql_connection_file)
		userid = s.loadWebLogin(token)
		name = request.values.get('name')
		r = s.loadMedia(chatid,name)
		if(r == None):
			return json.dumps({'result':'no se encontro el save'})
			
		c,t = r
		if(t == 2):
			try:
				os.remove(mediaPath + chatid + '/' + c)
			except Exception as e:
				print(e)
		s.deleteMedia(name,chatid)

		return json.dumps({'result':'ok'})
			# print(f)
	return json.dumps({'result':'error'})


@app.route("/api/save/<image_name>")
def get_image(image_name):

    try:
        return send_from_directory(savesdir, filename=image_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)

@app.route('/api/<chatid>/media/<image_name>',methods=['GET','POST','DELETE'])
def get_media(chatid,image_name):
    print('caio')
    try:
        return send_from_directory(mediaPath + chatid, filename=image_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)


@app.route("/api/notifications")
def getNotications():
	s = Save(file=sql_connection_file)
	token = request.headers.get('token')
	tipo = request.values.get('type',"new")
	userid = s.loadWebLogin(token)
	if(not userid):
		return json.dumps({"result":"not loged"})

	if(tipo == 'all'):
		vistas = []
	elif(tipo == 'new'):
		vistas = s.notificationVistas(userid)
	s.cursor = s.db.cursor(dictionary=True)
	notifications = s.loadNotifications(userid)
	notifications = [i for i in notifications if i['id'] not in vistas]
	notifications = [i for i in notifications if i['id']]
	notifications = sorted(notifications, key=lambda k: k['time'],reverse=True) 
	return json.dumps({"result":"ok","notifications":notifications})
@app.route("/api/notifications/ver",methods=['GET','POST'])
def verNotications():
	print(request.json)
	token = request.json.get('token','')
	s = Save(file=sql_connection_file)
	userid = s.loadWebLogin(token)
	if(not userid):
		return '{"result":"error de session"}'
	notifications = request.json.get('notifications',[])
	print('notificaciones',notifications)
	for n in notifications:
		try:
			s.verNotification(n,userid)
		except mysql.connector.errors.IntegrityError:
			pass
	return '{"result":"ok"}'

"""

Conexion con los bots

"""
keep_listen = True
listenSock = None
listenSsock = None
def listenMessages(ssock,addr,chatid):
	while 1:
		try:
			text = ssock.recv(1024).decode('utf-8')
			if(not text):
				if(chatid in controlCon):
					controlCon.pop(chatid)
				elif(chatid in chatConnections):
					print('removiendo chat %s de las connections' % (chatid))
					chatConnections.pop(chatid)
					print(chatConnections)
				ssock.close()
				break
			message = json.loads(text)
			print('recibido',chatid,text)
			comando = message['comando']
			if(comando == 'juego'):
				s = Save(file=sql_connection_file)
				s.cursor.execute('select instanceid,pid from process where type=3 and chatid="%s";' % (chatid))
				r = s.cursor.fetchall()
				print(r)
				sendProcess(text)
		except Exception as e:
			PrintException()
			print(e,chatid)
			if(chatid in chatConnections):
				chatConnections.pop(chatid)
			elif(chatid in controlCon):
				controlCon.pop(chatid)
			elif(chatid == 'lite'):
				liteCon = None
			break
def listenConnections():
	global controlCon,liteCon,listenSock,listenSsock
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain(chain_key[0],chain_key[1])

	sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	listenSock = sock
	sock.bind(('0.0.0.0', 8443))
	sock.listen(20)
	ssock = context.wrap_socket(sock, server_side=True)
	listenSsock = ssock
	while keep_listen:
		try:
			conn, addr = ssock.accept()
			message = conn.recv(1024).decode('utf-8')
			print('recibido',message)
			message = json.loads(message)
			instanceid = message['instanceid']
			tipo = message['type']
			processid = message['processid']
			if(tipo == 1):
				s = Save(file=sql_connection_file)
				print('conectado con el bot de amino')
				controlCon = (conn,addr,instanceid,processid)
				threadListenMessages = threading.Thread(target=listenMessages, args=(conn,addr))
				threadListenMessages.daemon = True
				threadListenMessages.start()

			elif(tipo == 2):
				print('coneccion tipo discord')
				discordCon = (conn,addr)

		except Exception as e:
			PrintException()
			print(e)
"""
aws

"""

"""

Cargar los datos

"""





chatConnections = {}
socketConnections = {}
comandos = {}
connections = {}
with open('../lite/comandos.txt', 'r') as h:
    handler = h.read().split('\n')
    for line in handler:
        cl = line.split(' ')
        if(os.path.exists('../ayuda/comandos/' + cl[0] + '.txt')):
        	with open('../ayuda/comandos/' + cl[0] + '.txt','r') as h:
        		text = h.read()                                
	        comandos[cl[0]] = (int(cl[1]),int(cl[2]),text)
        else:
	        comandos[cl[0]] = (int(cl[1]),int(cl[2]),'No hay informacion de este comando')

interacciones = os.listdir('../interaccion')

for c in interacciones:
	if(c in comandos):
		continue
	comandos[c] = (0,0)
	if(os.path.exists('../ayuda/comandos/' + c + '.txt')):
		with open('../ayuda/comandos/' + c + '.txt','r') as h:
			text = h.read()                                
		comandos[c] = (0,0,text)
	else:
		comandos[c] = (0,0,'No hay informacion de este comando')
if(not debug):
	threadTips = threading.Thread(target=listenConnections, args=())
	threadTips.daemon = True
	threadTips.start()

if __name__ == '__main__':
	if(debug):
		context = ('/etc/letsencrypt/live/test.leyguistar.com/fullchain.pem','/etc/letsencrypt/live/test.leyguistar.com/privkey.pem')
		app.run(host='0.0.0.0',port=443,ssl_context=context)
	else:
		context = ('/etc/letsencrypt/live/leybot.leyguistar.com/fullchain.pem','/etc/letsencrypt/live/leybot.leyguistar.com/privkey.pem')
		app.run(host='0.0.0.0',port=443,ssl_context=chain_key)
	keep_listen = False
	if(listenSsock):
		listenSsock.close()
	if(listenSock):
		listenSock.close()

