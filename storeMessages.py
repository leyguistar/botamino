#!/usr/bin/env python3
from aminosocket import SocketHandler 
from save import Save
import ujson as json
import amino
from time import time
from exception import PrintException
import threading
import datetime
from mensajeSaver import MensajeSaver
from time import sleep
import socket
import threading
from collections import deque
import signal
import os
import random
secrets = {}

def login(userid,client=None):
    if(not client):
        client = amino.Client()
    if(userid not in secrets):
        s = Save()
        s.cursor.execute('select secret,sid from login where id="%s";' % (userid) )
        r = s.cursor.fetchone()
        s.close()
        if(not r ):
            return
        secret = r[0]
        secrets[userid] = secret
    else:
        secret = secrets[userid]
    print('iniciando',userid)
    try:
        client.login(secret=secret,device_id=random.choice(deviceids))
    except:
        print('error logeando a %s con secret: %s' % (userid,secret))
    return client.sid
def loginBots():
    bots = {}
    s = Save()
    botsChats = s.loadBotChats()
    pbots = s.loadBots(None,dictionary=True)
    topop = []
    for bot in pbots:
        sid = login(bot['userid'])
        handler = SocketHandler(sid,device_id,han,bot['userid'],120,debug=False)
        sockets[bot['userid']] = handler
        handler.start()
    s.close()

sockets = {}
lockSave = threading.Lock()
messageCacheLock = threading.Lock()
def prehan(data,botid):
    global count
    count += 1
    if(count > 20):
        return
    try:
        han(data,botid)
    except:
        PrintException()
    count -= 1

def han(data,botid):
    message = data['o']['chatMessage']
    tipo = message['type']
    if(tipo == 100 or tipo == 119):
        messageId = message['messageId']
        messageCacheLock.acquire()
        for i in messageCache:
            if(i[0] == messageId):
                result = i
                break
        else:
            messageCacheLock.release()
            return
        messageCacheLock.release()
        with open('logs/deleted_messages/%s' % (messageId),'w') as h:
            h.write(json.dumps(result))
    if(tipo !=0 and tipo != 3):
        return
    id = message['messageId']
    content = message.get('content')
    mediaValue = message.get('mediaValue')
    messageCacheLock.acquire()
    if(content):
        messageCache.append((id,0,content))
    elif(mediaValue):
        messageCache.append((id,1,mediaValue))
    messageCacheLock.release()
    createdTime = message['createdTime']
    uid = message['uid']
    chatid = message['threadId']
    chatsActivity[chatid] = time()
    # if(chatid != '88094de6-ea72-4f9c-bc01-bd355572c774'):
    #     return
    handlerSave = Save(autoConnect=False)
    lockSave.acquire()
    try:
        if(chatid not in mensajesChat):
            mensajes = {}
            mensajesChat[chatid] = mensajes
            try:
                handlerSave.connect()
                handlerSave.createSimpleMessage(chatid)
                handlerSave.close()
            except:
                PrintException()
                handlerSave.close()
        else:
            mensajes = mensajesChat[chatid]
        if(uid not in mensajes):
            try:
                handlerSave.connect()
                mensajesuser = handlerSave.loadSimpleMessagesUser(chatid,uid)
                mensajesuser = dict([(day,[count,True]) for day,count in mensajesuser.items() ])
                handlerSave.close()
            except:
                PrintException()
                handlerSave.close()
            mensajes[uid] = mensajesuser
        else:
            mensajesuser = mensajes[uid]
        day = datetime.datetime.strptime(createdTime,'%Y-%m-%dT%H:%M:%SZ').timetuple().tm_yday
        # print(uid,day)
        try:
            if(day not in mensajesuser):
                try:
                    handlerSave.connect()
                    handlerSave.simpleMessage(chatid,uid,1,day)
                    handlerSave.close()
                except:
                    handlerSave.close()
                    PrintException()
                mensajesuser[day] = [1,True]
                # print(uid,mensajesuser[day],day)
            else:
                if(type(mensajesuser[day]) == int):
                    mensajesuser[day] = [mensajesuser[day]+1,False]
                else:
                    mensajesuser[day][0] += 1
                    mensajesuser[day][1] = False
                # print(uid,mensajesuser[day],day)
                # handlerSave.updateSimpleMessage(chatid,uid,mensajesuser[day],day)
        except:
            PrintException()
    except:
        PrintException()
    lockSave.release()

def write():
    lockSave.acquire()
    handlerSave = Save(autoConnect=False)
    try:
        handlerSave.connect()
        for chatid,mensajes in mensajesChat.items():
            for uid,mensajesuser in mensajes.items():
                for day in mensajesuser:
                    if(not mensajesuser[day][1]):
                        handlerSave.updateSimpleMessage(chatid,uid,mensajesuser[day][0],day)
                        mensajesuser[day][1] = True
        handlerSave.close()
    except:
        handlerSave.close()
        PrintException()
    lockSave.release()
def saveThread():
    while 1:
        sleep(600)
        write()
def getUser(chatid,uid):
    if(stopAll):
        return
    lockSave.acquire()
    handlerSave = Save(autoConnect=False)
    if(chatid not in mensajesChat):
        mensajes = {}
        mensajesChat[chatid] = mensajes
        handlerSave.connect()
        handlerSave.createSimpleMessage(chatid)
        handlerSave.close()
    else:
        mensajes = mensajesChat[chatid]
    if(uid not in mensajes):
        handlerSave.connect()
        mensajesuser = handlerSave.loadSimpleMessagesUser(chatid,uid)
        mensajesuser = dict([(day,[count,True]) for day,count in mensajesuser.items() ])
        handlerSave.close()
        mensajes[uid] = mensajesuser
    else:
        mensajesuser = mensajes[uid]
    lockSave.release()
    return sum([i[0] for i in mensajesuser.values()])
def checkMessage(conn):
    try:
        data = conn.recv(1024).decode('utf-8')
        if(not len(data)):
            return
        print('llego request',data)
        js = json.loads(data)
        comando = js['comando']
        if(comando == 'get'):
            messageId = js['id']
            for i in messageCache:
                if(i[0] == messageId):
                    result = i
                    break
            else:
                i = None
            if(i):
                conn.send(json.dumps({"message":i,"result":"ok"}).encode('utf-8'))
            else:
                conn.send('{"result":"fail"}'.encode('utf-8'))

        elif(comando == 'count'):
            userid = js['userid']
            chatid = js['chatid']
            c = getUser(chatid,userid)
            conn.send(('{"result":"ok","count":%s}' % (c)).encode('utf-8'))
        elif(comando == 'activity'):
            now = time()
            n = 0
            for t in chatsActivity.values():
                if( t+3600 > now):
                    n += 1
            conn.send(('{"result":"ok","count":%d}' % (n)).encode('utf-8'))

        elif(comando == 'flush'):
            write()
            conn.send('{"result":"ok"}'.encode('utf-8'))

    except Exception as e:
        PrintException()
def request():
    TCP_IP = '0.0.0.0'
    TCP_PORT = 10004
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while 1:
        try:
            s.bind((TCP_IP, TCP_PORT))
        except:
            sleep(1)
        else:
            break
    s.listen(10)
    while 1:
        try:
            conn, addr = s.accept()
            t = threading.Thread(target=checkMessage,args=(conn,))
            t.start()
        except:
            PrintException()
stopAll = False
def checkarThreads():
    global stopAll
    while 1:
        t = len(threading.enumerate())
        if(t > 300):
            stopAll = True
        else:
            stopAll = False

        sleep(10)
def cerrarHandler(signum, frame):
    global cerrando
    if(cerrando):
        print('ya se esta cerrando')
        return
    else:
        print('cerrando')
    cerrando = True
    cerrar()
signal.signal(signal.SIGINT, cerrarHandler)
def cerrar():
    write()
    try:
        for s in sockets.values():
            s.close()
    except:
        pass
    os.kill(os.getpid(),signal.SIGKILL)
messageCache = deque([],maxlen=10000)

with open('deviceids.txt','r') as h:
    deviceids = h.read().split('\n')
device_id = random.choice(deviceids)
cerrando = False
mensajesChat = {}
chatsActivity = {}
count = 0
if(not os.path.exists('logs/deleted_messages')):
    os.mkdir('logs/deleted_messages')
loginBots()
print('guardando mensajes preciona algo para interrumpir')
t = threading.Thread(target=saveThread,args=())
t.daemon = True
t.start()
t = threading.Thread(target=request,args=())
t.daemon = True
t.start()
t = threading.Thread(target=checkarThreads,args=())
t.daemon = True
t.start()
while 1:
    o = input()
    if(o == 'cerrar'):
        print('cerrando')
        break
    elif(o == 'threads'):
        print('threads:',len(threading.enumerate()))
    elif(o == 'count'):
        print('count',count)

cerrar()