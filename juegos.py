#!/usr/bin/env python3
from aminosocket import SocketHandler 
from save import Save
import simplejson as json
import amino
from time import time
from exception import PrintException
import threading
from time import sleep
import socket
import threading
import signal
import os
from juegosfuns import Juego,send_message,jugando
from juegosfuns import clients,sockets,login,nicknames,getNickname,juegosApa
from juegos_vor import Vor,vor
from juegos_apa import Apa,apa
from juegos_openings import Aop,aop
from juegosfuns import send_marco
from juegos_jikan import Aa,aa
countBots = {}
def on_close(botid):
    print('llamaron a on_close')
    countBots[botid] -= 1
    c = countBots[botid]
    if(c == 0):
        try:
            print('cerrando socket de',botid)
            sockets[botid].close()
            sockets.pop(botid)
        except:
            PrintException()
def han(data,botid):
    message = data['o']['chatMessage']
    tipo = message['type']
    refId = message['clientRefId']
    if(refId < 0):
        return
    if(tipo != 0 ):
        return
    content = message.get('content')
    if(not content):
        return
    id = message['messageId']
    chatid = message['threadId']
    if(chatid in jugando):
        userid = message['uid']
        print(chatid,userid,content)
        if(jugando[chatid].botid == userid):
        	return
        nickname = message['author']['nickname']
        nicknames[userid] = nickname
        juego = jugando[chatid]
        jugadores = juego.jugadores
        admins = juego.admins
        allContent = content
        nombre = juego.juego
        content = content.split(' ')
        if(content[0] != '/'):
            comando = content[0][1:]
            if(comando == 'entrar'):
                if(userid not in jugadores):
                	juego.add(userid,nickname)
            elif(comando == 'salir'):
                r = juego.remove(userid)
                if(not r):
                    send_message(chatid,'Abandonaron todos')
                    send_marco(chatid,'Terminando juego %s' % (nombre))
                    jugando[chatid].cancelar()
            elif(comando == 'start'):
                if(not jugadores):
                    send_message(chatid,'Primero entren con /entrar')
                    return
                if(userid not in admins):
                	return
                if(juego.iniciado):
                    return
                	# send_message(chatid,'Tienes que tener minimo p[')
                if(nombre == 'vor'):
                    send_marco(chatid,'Iniciando juego Verdad o reto')
                    juego.start_juego()
                elif(nombre == 'aop'):
                    if(len(content) == 2):
                        if(content[1].isdigit()):
                            ns = int(content[1])
                            if(ns > 50):
                                send_message(chatid,'no pueden haber mas de 50 animes')
                                return
                            elif(ns < 5):
                                send_message(chatid,'no pueden haber menos de 5 animes')
                                return
                            else:
                                animes = ns
                    else:
                        animes = 10
                    send_marco(chatid,'Iniciando juego %s con %d animes' % (nombre,animes))
                    juego.start_juego(animes)
                elif(nombre == 'aa'):
                    if(len(content) == 2):
                        if(content[1].isdigit()):
                            ns = int(content[1])
                            if(ns > 50):
                                send_message(chatid,'no pueden haber mas de 50 animes')
                                return
                            elif(ns < 5):
                                send_message(chatid,'no pueden haber menos de 5 animes')
                                return
                            else:
                                animes = ns
                    else:
                        animes = 10

                    send_marco(chatid,'Iniciando juego %s con %d animes' % (nombre,animes))
                    juego.start_juego(animes)

                elif(nombre in juegosApa):
                    send_marco(chatid,'Iniciando juego %s' % (nombre))
                    juego.start_juego()


            elif(comando == 'jugadores'):
                text = 'jugadores:\n'
                for u in jugadores:
                    text += getNickname(u) + '\n'
                send_message(chatid,text)
            elif(comando == 'comandos' or comando == 'c'):
                text = '[cb]Comandos de los juegos\n\n'
                with open('juegos/info/comandos.txt','r') as h:
                    text += h.read() + '\n'
                send_marco(chatid,text)
                text = '[cb]Comandos de %s\n\n' % (nombre)
                with open('juegos/%s/comandos.txt' % nombre,'r') as h:
                    text += h.read()
                send_marco(chatid,text)
            elif(comando == 'inf'):
                with open('juegos/%s/informacion.txt' % (nombre),'r') as h:
                    text = h.read()
                send_marco(chatid,text)
            elif(userid in juego.admins):
                if(comando == 'cancelar'):
                	juego.cancelar()
                elif(comando == 'sacar'):
                    extensions = message.get('extensions')
                    if(not extensions):
                        extensions = {}
                    usersid = []
                    if('mentionedArray' in extensions):
                        for mi in extensions['mentionedArray']:
                            usersid.append(mi['uid'])
                    if(not usersid):
                        send_message(chatid,'uso: /sacar @user: remueve a un jugador')
                    for u in usersid:
                        r = juego.remove(userid,sacado=True)
                        if(not r):
                            send_message(chatid,'Abandonaron todos')
                            jugando[chatid].cancelar()

            if(nombre == 'vor'):
                juego.lock.acquire()
                vor(message,juego)
                juego.lock.release()
            elif(nombre == 'aa'):
                juego.lock.acquire()
                aa(message,juego)
                juego.lock.release()
            elif(nombre == 'aop'):
                juego.lock.acquire()
                aop(message,juego)
                juego.lock.release()

            elif(nombre in juegosApa):
                juego.lock.acquire()
                apa(message,juego)
                juego.lock.release()
            else:
                print('este mensaje no fue enviado a ningun juego')
def startSocket(client):
    botid = client.profile.id
    handler = SocketHandler(client.sid,client.device_id,han,botid,120,debug=False)
    sockets[botid] = handler
    handler.start()

def checkMessage(conn):
    try:
        data = conn.recv(1024).decode('utf-8')
        if(not len(data)):
            return
        print('llego request',data)
        js = json.loads(data)
        chatid = js['chatid']
        ops = js['ops']
        admins = [i for i in ops if(ops[i] > 0)]
        if(chatid in jugando):
            print('terminando',jugando[chatid].juego)
            send_marco(chatid,'Terminando juego %s' % (jugando[chatid].juego))
            jugando[chatid].cancelar()
        juego = js['juego']
        botid = js['botid']
        comid = js['comid']
        if(botid not in clients):
            client = login(botid)
            clients[botid] = client
        else:
            client = clients[botid]
        if(botid not in countBots):
            countBots[botid] = 1
        else:
            countBots[botid] += 1

        if(botid not in sockets):
            startSocket(client)
        print('socket iniciado')
        juego = Juego(juego,chatid,comid,[],botid,client,admins,on_close)
        print('juego parte 1')
        if(juego.juego == 'vor'):
            print('juego parte 2')
            juego = Vor(juego)  
            print('juego parte 3')
        elif(juego.juego == 'aa'):
            juego = Aa(juego)                  
        elif(juego.juego == 'aop'):
            juego = Aop(juego)
        elif(juego.juego in juegosApa):
            print('Iniciando',juego.juego)
            juego = Apa(juego)  
        else:
            conn.send('{"result":"no game"}')
            return
        print('poniendo el juego en juegos')
        jugando[chatid] = juego
        with open('juegos/%s/informacion.txt' % (juego.juego),'r') as h:
            text = h.read()
        send_marco(chatid,text)
        print('marco enviado')
        conn.send('{"result":"ok"}'.encode('utf-8'))

    except Exception as e:
        PrintException()
def remoteConnection():
    global listeningSocket
    TCP_IP = '0.0.0.0'
    TCP_PORT = 10432
    TCP_PORT1 = 10432
    TCP_PORT2 = 10433
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while 1:
        try:
            s.bind((TCP_IP, TCP_PORT))
        except:
            PrintException()
            if(TCP_PORT == TCP_PORT1):
                TCP_PORT = TCP_PORT2
            else:
                TCP_PORT = TCP_PORT1                
            sleep(2)
        else:
            break
    s.listen(10)
    listeningSocket = s
    print('esperando conexiones')
    while not cerrando:
        try:
            conn, addr = s.accept()
            print('conexion remote recivida')
            t = threading.Thread(target=checkMessage,args=(conn,))
            t.daemon = True
            t.start()

        except Exception as e:
            print(e)

# def checkRequest():
#     s = Save()
#     while not cerrando:
#         s.close()
#         try:
#             s.connect()
#         except:
#             PrintException()
#             sleep(20)
#             continue
#         try:
#             requests = s.loadGameRequests()
#             for js in requests:
#                 chatid = js['chatid']
#                 if(time() > js['t']+60 ):
#                 	s.removeGameRequest(chatid)
#                 	continue
#                 ops = s.loadOPS(chatid)
#                 admins = [i for i in ops if(ops[i] > 0)]
#                 if(chatid in jugando):
#                     send_marco(chatid,'Terminando juego %s' % (jugando[chatid].juego))
#                     jugando[chatid].cancelar()
#                 juego = js['juego']
#                 botid = js['botid']
#                 comid = js['comid']
#                 if(botid not in clients):
#                     client = login(botid)
#                     clients[botid] = client
#                 else:
#                     client = clients[botid]
#                 if(botid not in countBots):
#                     countBots[botid] = 1
#                 else:
#                     countBots[botid] += 1

#                 if(botid not in sockets):
#                     startSocket(client)
#                 juego = Juego(juego,chatid,comid,[],botid,client,admins,on_close)
#                 if(juego.juego == 'vor'):
#                     juego = Vor(juego)	
#                 elif(juego.juego == 'aa'):
#                     juego = Aa(juego)                  
#                 elif(juego.juego == 'aop'):
#                     juego = Aop(juego)
#                 elif(juego.juego in juegosApa):
#                     print('Iniciando',juego.juego)
#                     juego = Apa(juego)	
#                 else:
#                     s.removeGameRequest(chatid)
#                     return
#                 jugando[chatid] = juego
#                 with open('juegos/%s/informacion.txt' % (juego.juego),'r') as h:
#                     text = h.read()
#                 send_marco(chatid,text)
#                 s.removeGameRequest(chatid)
#         except:
#             PrintException()

#         sleep(1)
#     while(jugando):
#     	sleep(10)
#     cerrar()
cerrando= False
def cerrarHandler(signum, frame):
    global cerrando
    if(cerrando):
        print('ya esta en modo cerrar')
        return
    else:
        print('dejando de recibir requests, se cerrara cuando ya no hayan juegos')
    cerrando = True
    listeningSocket.close()
    while(jugando):
      sleep(10)
    cerrar()

signal.signal(signal.SIGINT, cerrarHandler)
def cerrar():
    try:
        for s in sockets.values():
            s.close()
    except:
        pass
    os.kill(os.getpid(),signal.SIGKILL)
remoteConnection()