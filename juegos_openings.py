import amino
from juegosfuns import getNickname,send_message,nicknames,send_marco
from juegosfuns import send_imagen,send_text_imagen,jugando
from juegosfuns import send_audio
import random
from time import sleep
from time import time
from jikanpy import Jikan
import jikanpy
import shutil
import re
from unicodedata import normalize
import threading
import requests
from exception import PrintException
from youtube_search import YoutubeSearch as ys
import socket
import ujson as json
import os
from save import Save
jikan = Jikan()

def getYoutube(id):
    try:
        TCP_IP = "127.0.0.1"
        TCP_PORT = 10130
        print('invocando socket')
        s = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_STREAM) # UDP
        print('conectando socket',(TCP_IP, TCP_PORT))
        s.connect((TCP_IP, TCP_PORT))
        print('enviando mensaje')
        s.send(('{"id":"%s","type":%d}' % (id,1)).encode('utf') )
        print('esperando')
        data = s.recv(10240).decode('utf-8')
        print(data)
        s.close()
        return json.loads(data)
    except Exception as e:
        print("el error esta en getyoutube")
        print(e)
def toIntDuration(d):
    if(type(d) == str):
        t = [int(x) for x in d.split(':')]
        i = 0
        d = 0
        for ti in t[::-1]:
            d += ti*60**i
            i+=1
    return d
def openings(id):
    for i in range(5):
        try:
            result = jikan.anime(int(id))
        except jikanpy.exceptions.APIException as e:
            sleep(1)
        except:
            PrintException()
        else:
            return result['opening_themes']                
def readfile(f):
    with open(f,'r') as h:
        return h.read()
class Aop:
    def __init__(self,juego):
        self.juego = juego.juego
        self.chatid = juego.chatid
        self.comid = juego.comid
        self.jugadores = juego.jugadores
        self.botid = juego.botid
        self.client = juego.client
        self.admins = juego.admins
        self.limite = juego.limite
        self.on_close = juego.on_close
        self.contando = False
        self.lastTurnoLimite = threading.Event()
        self.lastTurno = threading.Event()
        self.total = 10
        self.dificultad = 0
        self.lastActive = time()
        self.iniciado = False
        self.turno = 0
        self.puntos = {}
        self.lock = threading.Lock()
        for u in self.jugadores:
            self.puntos[u] = 0
        self.equipos = {}
        self.respuestas = []
        t = threading.Thread(target=self.inactivo,args=())
        t.start()

    def __del__(self):
        self.iniciado = False
    def start_juego(self,total):
        animes = os.listdir('openings')
        ids = [i for i in animes if (not i.endswith('txt')) ]
        print(ids)
        animes = []
        # ids = ['11757','1535','16498','20','22319','31964','5114']
        for i in ids:
            names = readfile('openings/' + i + '.txt').split('\n')
            animes.append((i,names))
        
        random.shuffle(animes)
        self.animes = animes
        self.turno = 0
        self.total = total
        self.iniciado = True
        s = Save()
        s.clearQueue(self.chatid)
        s.close()
        self.enviarAnime()
        t = threading.Thread(target=self.contarLimite,args=())
        t.start()

    def add(self,userid,nickname):
        if(userid not in self.jugadores):
            self.puntos[userid] = 0
            self.jugadores.append(userid)
            send_message(self.chatid,'%s se ha unido al juego' % nickname)

    def enviarAnime(self):
        global respuestas
        r = []
        chatid = self.chatid
        animes = self.animes
        turno = self.turno
        if(turno == self.total ):
            self.cancelar()
            return
        if(turno >= len(animes)):
            self.cancelar()
            return
        anime = self.animes[turno]

        data = None
        animeid = anime[0]
        self.respuestas.append(anime[1])
        d = 'openings/%s/' % (animeid)
        songs = [i for i in os.listdir(d) if i.endswith('.id')]
        if(not songs):
            self.next()
            return
        song = random.choice(songs)


        send_audio(self.chatid,d + song.replace('.id','.m4a') )
        print([i.translate(trans) for i in self.respuestas[turno]])
        send_message(self.chatid,'¿De que anime es el opening que esta sonando?')
        self.lastTurno.set()
    def remove(self,userid,sacado=False):
        if(userid in self.jugadores):
            if(len(self.jugadores)):
                return False
            self.puntos.pop(userid)
            if(sacado):
                send_message(self.chatid,'%s a sido removido del juego' % (getNickname(userid)))
            else:
                send_message(self.chatid,'%s ha abandonado el juego' % getNickname(userid))

        return True


    def next(self):
        if(not self.iniciado):
            return
        self.lastActive = time()
        self.lastTurno.set()
        self.turno += 1
        self.enviarAnime()

    def send_turno(self):
        send_message(self.chatid,'Turno de %s' % getNickname(self.jugadores[self.turno]))

    def inactivo(self):        
        while 1:
            self.lastTurno.wait(600)
            if(self.lastTurno.is_set()):
                self.lastTurno.clear()
            else:
                send_message(self.chatid,"Terminando juego por inactividad")
                self.cancelar()
                return
    def contarLimite(self):
        while self.iniciado:
            if(not self.limite ):
                sleep(1)
                continue
            self.lastTurnoLimite.wait(self.limite)
            if(not self.iniciado):
                return
            if(self.lastTurnoLimite.is_set()):
                self.lastTurnoLimite.clear()
            else:
                send_message(self.chatid,'Se acabo el tiempo\n\nRespuestas: %s\n' % ('\n'.join(self.respuestas[self.turno]) ))
                self.next()
                self.lastTurnoLimite.clear()

    def mostrarPuntuaciones(self):
        m = ''
        equipos = self.equipos
        puntos = self.puntos
        pequipos = {}
        m += 'Puntos:\n'
        for u,p in puntos.items():
            m += getNickname(u) + ': ' + str(p) + '\n'
            if(u in equipos):
                if(equipos[u] in pequipos):
                    pequipos[equipos[u]] += puntos[u]
                else:
                    pequipos[equipos[u]] = puntos[u]
        if(pequipos):
            m += 'Equipos:\n\n'
            for e in pequipos:
                m += e + ': ' + str(pequipos[e]) + '\n'
        if(m != ''):
            send_message(self.chatid,m)

    def mostrarPosiciones(self):
        puntos = self.puntos
        equipos = self.equipos
        if(not puntos):
            return
        m = 'Resultados:\n\n'
        i = 1
        if(len(equipos) > 0):
            pequipos = {}
            for u in puntos:
                if(u in equipos):
                    if(equipos[u] in pequipos):
                        pequipos[equipos[u]] += puntos[u]
                    else:
                        pequipos[equipos[u]] = puntos[u]
            winners = {k: v for k, v in sorted(pequipos.items(), key=lambda item: item[1],reverse=True)}
            i = 1
            for e in winners:
                m += str(i) + '. ' + e + ': ' + str(winners[e]) + 'pts.\n'
                for u in equipos:
                    if(equipos[u] == e):
                        m += getNickname(u) + '\n'
                m += '\n'
                i+= 1
        else:
            winners = {k: v for k, v in sorted(puntos.items(), key=lambda item: item[1],reverse=True)}
            for u in winners:
                m += str(i) + '. ' + getNickname(u) + ' ' + str(winners[u]) + 'pts.\n\n'   
                i += 1
        send_marco(self.chatid,m)
    def cancelar(self):
        self.limite = 0
        self.iniciado = False
        self.mostrarPuntuaciones()
        self.mostrarPosiciones()
        send_marco(self.chatid,"\nJuego %s terminado\n" % (self.juego))
        if(self.chatid in jugando):
            jugando.pop(self.chatid)
        self.on_close(self.botid)

def aop(message,juego):
    content = message['content']
    nickname = message['author']['nickname']
    userid = message['uid']
    respuestas = juego.respuestas
    turno = juego.turno
    jugadores = juego.jugadores
    chatid = juego.chatid
    admins = juego.admins
    puntos = juego.puntos
    iniciado = juego.iniciado
    equipos = juego.equipos
    try:
        s = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", content), 0, re.I
            )
        content = normalize( 'NFC', s)
        content = normalize('NFKC',content)

        if(userid in jugadores and iniciado):
            if(content.lower().translate(trans) in 
                [i.translate(trans) for i in respuestas[turno]]):
                puntos[userid] += 1
                send_message(chatid,'%s gana un punto\n\n%s' % (getNickname(userid),'\n'.join(respuestas[turno])) )
                juego.next()
        if(content[0] != '/'):
            return
        m = content[content.find(" "):]
        content = content.split(' ')
        comando = content[0][1:]
        print(comando)
        if(comando == "p"):
            if(not iniciado):
                send_message(chatid,'El juego todavia no ha iniciado')
            else:
                juego.mostrarPuntuaciones()

        elif(comando == "equipo"):
            print('en equipo')

            if(len(content ) < 2):
                print('equivocao')
                if(userid in equipos):
                    send_message(chatid,'estas en el equipo ' + equipos[userid])
                else:
                    send_message(chatid,'uso: /equipo [nombre]: Para unirte a un equipo, si el equipo no existe lo crea')
            else:
                if(userid not in jugadores):
                    juego.add(userid,nickname)
                print('asignando equipo')

                nombre = ' '.join(content[1:])
                equipos[userid] = nombre
                print('equipo ' + nombre)
                send_message(chatid,'Entraste al equipo ' + nombre)

        elif(comando == "equipos"):
            t = list(dict.fromkeys(equipos.values() ).keys() )
            text = 'Equipos:\n'
            for i in t:
                text += i + ':\n'
                for u in equipos:
                    if(equipos[u] == i):
                        text += getNickname(u) + '\n'
            send_message(chatid,text)

        if(userid not in admins):
            return
        if(comando == 'limite'):
            if(len(content) == 2 and content[1].isdigit()):
                juego.limite = int(content[1])
                juego.lastTurnoLimite.set()
                send_message(chatid,'Limite de tiempo por turno %ds' % (juego.limite))
            else:
                send_message(chatid,'uso: /limite [segundos]: pone un tiempo limite por turno, 0 para ninguno')
                send_message(chatid,'limite de tiempo actual %d' % (juego.limite))
        elif(comando == "pasar"):
            send_message(chatid,'Respuestas:\n' + '\n'.join(respuestas[turno]) )
            juego.next()
    except Exception as e:
        PrintException()
skipCharacters = '- :!.,'
trans = str.maketrans('','',skipCharacters)
