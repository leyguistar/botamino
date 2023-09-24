#!/usr/bin/env python3
import os
import sys
if('log' in sys.argv):
	try:
		sys.stdout = open('/checkbots.log','w')
	except:
		pass
import signal
import ssl
import socket
from time import time
from time import sleep
import ujson as json
import threading
import psutil
import subprocess
import requests
import mysql.connector.errors
print('cargadas cosas sin problemas')

try:
	r = requests.get('http://169.254.169.254/latest/meta-data/instance-id',timeout=1)
except:
	instanceid = 'i-local'
else:
	instanceid = r.text
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
sys.path.append(dname)
os.chdir(dname)
from save import Save
from exception import PrintException
startRequests = {}
requiredMem = 104857600
# sqlFile = 'remote_sql.set'	

def check(pid):
	try:	
		os.kill(pid,0)
	except OSError:
		return 0
	else:
		return 1
def startProcess(args,chatid=None):
	proc = subprocess.Popen(args)
	r = proc.communicate()[0]
	pid = proc.pid
	while(chatid and r != 0 ):
		s = Save(file=sqlFile)
		chat = s.loadBotstate(chatid=chatid)
		if(chat and chat[0] == 1 and chat[2] == pid):
			del s
			proc = subprocess.Popen(args + ['nostart'])
			r = proc.communicate()[0]
			pid = proc.pid
		else:
			break
def connectServer():
	while True:
		try:
			hostname = 'leybot.leyguistar.com'
			context = ssl.create_default_context()

			sock = socket.create_connection((hostname,8443))
			ssock = context.wrap_socket(sock,server_hostname=hostname)  
			ssock.send(('{"instanceid":"%s","type":2,"chatid":"*","pid":%d,"processid":%d}' % (instanceid,os.getpid(),processid)).encode('utf-8'))
			print('conectado con el servidor')
			while 1:
				text = ssock.recv().decode('utf-8')
				print('recibido',text)
				if(text == ""):
					ssock.send('KA'.encode('utf-8'))
					continue
				message = json.loads(text)
				comando = message['comando']
				if(comando == "start"):
					premium = message['premium']
					comid = message['comid']
					userBot = message['userBot']
					chatid = message['chatid']
					# mem = psutil.virtual_memory()
					# if(mem < requiredMem):
					# 	text = json.dumps({'response':'No hay recursos suficientes','chatid':chatid})
					# 	ssock.send(text.encode('utf-8'))
					args = ["python3",'bot.py','id',chatid,'log','premium='+str(premium),"comid="+str(comid),"userid="+userBot]
					if(message['show'] == 0):
						args.append('nostart')
					t = threading.Thread(target=startProcess, args=(args,chatid))
					t.daemon = True
					t.start()
					startRequests[chatid] = {'time':time(),'args':args}
				elif(comando == 'juego'):
					print('iniciando juego')
					args = ["python3",message['filename'],message['chatid'],message['juego'],"comid="+str(message["comid"]),"mensaje="+str(message["mensaje"]),"userid="+str(message['userid']),"silent"]
					t = threading.Thread(target=startProcess, args=(args,))
					t.daemon = True
					t.start()

				elif(comando == 'cpu'):
					text = json.dumps({'comando':'cpu','cpu':psutil.cpu_percent()} )
					ssock.send(text.encode('utf-8'))
				elif(comando == 'kill'):
					pid = message['pid']
					try:
						os.kill(pid, signal.SIGALRM)
					except Exception as e:
						print(e)
		except Exception as e:
			# PrintException()
			print('error conectando con el servidor,',e,'reintentando')
			sleep(60)

def recvChats():
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.bind(('127.0.0.1', 10101))

	while True:
	    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	    message =  json.loads(data.decode('utf-8'))
	    chatid = message['chatid']
	    result = message['result']
	    if(chatid in startRequests and result == 'ok'):
	    	startRequests.pop(chatid)


if('LOGDIR' in os.environ):
	logPath = os.environ['LOGDIR'] + '/'
else:
	logPath = 'logs/' 
if('SQLFILE' in os.environ):
	sqlFile = os.environ['SQLFILE']
else:
	sqlFile = 'default.set' 



if('log' in sys.argv):
	sys.stdout = open('logs/checkbots_%d.log' % (time()), 'w')



print('conecting with the database')
s = Save(file=sqlFile)
processid = s.process(2,__file__,'*',0,os.getpid(),instanceid)

threadClient = threading.Thread(target=connectServer, args=())
threadClient.daemon = True
threadClient.start()

threadClient = threading.Thread(target=recvChats, args=())
threadClient.daemon = True
threadClient.start()
while 1:
	try:
		sys.stdout.flush()
		s.db.reset_session()
		chats = s.loadBotstate(state=1)
		process = s.loadProcessInstance(instanceid)
		botRequests = s.loadBotRequests(instanceid)
		for r in botRequests:
			args = ["python3",'bot.py','id',r[0],'log','premium=1',"comid="+str(r[2]),"userid="+r[1]]
			if(r[4] == 0):
				args.append('nostart')		
			t = threading.Thread(target=startProcess, args=(args,r[0]))
			t.daemon = True
			t.start()
			startRequests[r[0]] = {'time':time(),'args':args}

			s.removeBotRequests(chatid=r[0])
		for p in process:
			try:	
				os.kill(p[5],0)
			except OSError:
				s.rprocess(p[0])
				print(p[2],p[3],'perecio')
		sys.stdout.flush()	
		for chatid in startRequests:
			if(startRequests[chatid]['time'] > time()+60):
				t = threading.Thread(target=startProcess, args=(startRequests[chatid]['args'],chatid))
				t.daemon = True
				t.start()
				

	except mysql.connector.errors.DatabaseError as e:
		s = Save(file=sqlFile)
	except Exception as e:
		PrintException(__file__)
	finally:
		sleep(60)