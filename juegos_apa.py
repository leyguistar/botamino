import amino
from juegosfuns import getNickname,send_message,nicknames,send_marco
from juegosfuns import send_imagen,send_text_imagen,jugando
import random
from time import sleep
from time import time

import re
from unicodedata import normalize
import threading

class Apa:
    def __init__(self,juego):
        self.juego = juego.juego
        self.chatid = juego.chatid
        self.comid = juego.comid
        self.jugadores = juego.jugadores
        self.botid = juego.botid
        self.client = juego.client
        self.admins = juego.admins
        self.limite = juego.limite
        self.contando = False
        self.lastTurnoLimite = threading.Event()
        self.on_close = juego.on_close
        self.lock = threading.Lock()

        self.lastActive = time()
        self.iniciado = False
        self.turno = 0
        self.puntos = {}
        for u in self.jugadores:
            self.puntos[u] = 0
        self.load_juego(self.juego)
        self.orden = list(range(len(self.respuestas)))
        random.shuffle(self.orden)
        self.equipos = {}
        self.lastTurno = threading.Event()
        t = threading.Thread(target=self.inactivo,args=())
        t.start()
    def __del__(self):
        self.iniciado = False
    def start_juego(self):
        self.iniciado = True
        self.next()
        t = threading.Thread(target=self.contarLimite,args=())
        t.start()
    def load_juego(self,juego):
        try:
            with open('juegos/' + juego + '/preguntas.txt', 'r') as handler:
                self.preguntas = [line.rstrip().lower() for line in handler]
        except IOError:
            self.preguntas = None
        with open('juegos/' + juego + '/respuestas.txt', 'r') as handler:
            self.respuestas = [line.rstrip().lower() for line in handler]

        with open('juegos/' + juego + '/links.txt', 'r') as handler:
            self.links = [line.rstrip() for line in handler]
    def add(self,userid,nickname):
        if(userid not in self.jugadores):
            self.puntos[userid] = 0
            self.jugadores.append(userid)
            send_message(self.chatid,'%s se ha unido al juego' % nickname)

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
        self.lastTurno.set()
        if(len(self.orden) == 0):
            self.cancelar()
            return
        else:
            self.turno = self.orden.pop() 
            self.enviarPregunta()
    def enviarPregunta(self):
        file='juegos/'+ self.juego +'/imagenes/%d.jpg' % (self.turno)
        if(self.preguntas != None):
            send_text_imagen(self.chatid,self.preguntas[self.turno],filename=file)
        else:
            if(self.juego.startswith('pelis') ):
                send_text_imagen(self.chatid,'¿Que pelicula es?',filename=file)
            elif(self.juego.startswith('aa') ):
                send_text_imagen(self.chatid,'¿Que anime es?',filename=file)            
            else:
                send_imagen(self.chatid,file=file)

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
                send_message(self.chatid,'Se acabo el tiempo\n\nRespuestas: %s\n' % ('\n'.join(self.respuestas[self.turno].split('|')) ))
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
        send_marco(self.chatid,"\n\nJuego %s terminado\n\n" % (self.juego))
        if(self.chatid in jugando):
            jugando.pop(self.chatid)
        self.on_close(self.botid)

def apa(message,juego):
    content = message['content']
    nickname = message['author']['nickname']
    userid = message['uid']
    preguntas = juego.preguntas
    respuestas = juego.respuestas
    turno = juego.turno
    jugadores = juego.jugadores
    chatid = juego.chatid
    admins = juego.admins
    puntos = juego.puntos
    iniciado = juego.iniciado
    equipos = juego.equipos
    s = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", content), 0, re.I
        )
    content = normalize( 'NFC', s)
    content = normalize('NFKC',content)
    rs = respuestas[turno].split('|')
    if(userid in jugadores and iniciado):
        if(content.lower() in rs):
            puntos[userid] += 1
            send_message(chatid,'%s gana un punto\n\n%s' % (getNickname(userid),respuestas[turno]) )
            juego.next()
    if(content[0] != '/'):
        return
    m = content[content.find(" "):]
    content = content.split(' ')
    comando = content[0][1:]
    print(comando)
    if(comando == "p"):
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
            send_message(chatid,'Limite de tiempo por turno %d' % (juego.limite))
        else:
            send_message(chatid,'uso: /limite [segundos]: pone un tiempo limite por turno, 0 para ninguno')
            send_message(chatid,'limite de tiempo actual %d' % (juego.limite))
    elif(comando == "pasar"):
        send_message(chatid,'Respuesta: ' + respuestas[turno])
        juego.next()
