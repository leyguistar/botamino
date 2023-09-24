import amino
from juegosfuns import getNickname,send_message,nicknames,send_marco
from juegosfuns import send_imagen,send_text_imagen,jugando
import random
from time import sleep
from time import time
from jikanpy import Jikan

import re
from unicodedata import normalize
import threading
import requests
from exception import PrintException
jikan = Jikan()
class Aa:
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
        self.animes = jikan.top(type='anime', page=self.dificultad, subtype='bypopularity')['top']
        random.shuffle(self.animes)
        self.turno = 0
        self.total = total
        self.iniciado = True
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
        data = None
        for i in range(5):
            try:
                data = jikan.anime(animes[turno]['mal_id'])
            except Exception as e:
                print('error')
                print(e)
                print('reintentando')
                sleep(1)
            else:
                break
        if(data == None):
            send_message(chatid,'A ocurrido un error, terminando juego')
            self.cancelar()
            return
        rated = data.get('rating','F')
        if('Rx' in rated):
            print('sacando',data['title'],rated)
            del animes[turno]       
            self.enviarAnime()
            return
        print(data['title'])
        r.append(data['title'])
        if('title_english' in data):
            r.append(data['title_english'])
        if('title_synonyms' in data):
            r += data['title_synonyms']
        if('title_japanese' in data):
            r.append(data['title_japanese'])
        if('Adaptation' in data['related']):
            for a in data['related']['Adaptation']:
                r.append(a['name'])
        r = [ i.lower() for i in r if(i!=None) ]
        rs = [ i for i in r if(':' in i) ] 
        r = [ i.split(':')[0] for i in r ]
        r += rs
        r = list(dict.fromkeys(r))
        for old in self.respuestas:
            if(any(item in r for item in old)):
                del animes[turno]
                return self.enviarAnime()
        self.respuestas.append(r)
        url = data['image_url']
        send_text_imagen(self.chatid,'¿Que anime es?',url=url)

        print([i.translate(trans) for i in self.respuestas[turno]])


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

def aa(message,juego):
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
        elif(comando == "dificultad"):
            if(len(content) == 2):
                if(content[1].isdigit()):
                    d = int(content[1])
                    if(d > 100):
                        send_message(chatid,'la dificultad no puede ser mayor a 100')
                        return
                    elif(d < 1):
                        send_message(chatid,'la dificultad no puede ser menor a 1')
                        return
                    else:
                        send_message(chatid,'dificultad ' + str(d))
                        juego.dificultad = d                                      
                        return
            send_message(chatid,'uso: /dificultad [n]: configura el nivel de dificultad')
    except Exception as e:
        PrintException()
skipCharacters = '- :!.,'
trans = str.maketrans('','',skipCharacters)
