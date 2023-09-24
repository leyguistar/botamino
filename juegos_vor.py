import amino
from juegosfuns import getNickname,send_message,nicknames,send_marco,jugando
import random
from time import sleep
from time import time
import threading
class Vor:
	def __init__(self,juego):
		self.juego = juego.juego
		self.chatid = juego.chatid
		self.comid = juego.comid
		self.jugadores = juego.jugadores
		self.botid = juego.botid
		self.client = juego.client
		self.admins = juego.admins
		self.iniciado = False
		self.libre = False
		self.limite = juego.limite
		self.lastActive = time()
		self.contando = False
		self.turno = 0
		self.lock = threading.Lock()

		self.lastTurno = threading.Event()
		self.lastTurnoLimite = threading.Event()
		self.preguntas = preguntas.copy() 
		self.on_close = juego.on_close
		random.shuffle(self.preguntas)
		self.retos = retos.copy() 
		random.shuffle(self.retos)
		t = threading.Thread(target=self.inactivo,args=())
		t.start()

	def __del__(self):
		self.iniciado = False
	def add(self,userid,nickname):
		if(userid not in self.jugadores):
			self.jugadores.append(userid)
			send_message(self.chatid,'%s se ha unido al juego' % nickname)

	def remove(self,userid,sacado=False):
		if(userid in self.jugadores):
			if(len(self.jugadores)):
				return False
			i = self.jugadores.index(userid)
			if(i < self.turno):
				self.turno -= 1
			if(i == self.turno):
				self.next()
			self.jugadores.remove(userid)
			if(sacado):
				send_message(self.chatid,'%s a sido removido del juego' % (getNickname(userid)))
			else:
				send_message(self.chatid,'%s ha abandonado el juego' % getNickname(userid))

		return True

	def start_juego(self):
		self.iniciado = True
		self.turno = -1
		self.next()
		t = threading.Thread(target=self.contarLimite,args=())
		t.start()

	def next(self):
		if(not self.iniciado):
			return
		self.lastTurno.set()
		self.lastTurnoLimite.set()
		self.lastActive = time()
		self.turno += 1
		self.turno = self.turno % len(self.jugadores)
		if(not self.libre):
			send_message(self.chatid,'Turno de %s' % getNickname(self.jugadores[self.turno]))
	def send_turno(self):
		send_message(self.chatid,'Turno de %s' % getNickname(self.jugadores[self.turno]))

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
				self.next()
				self.lastTurnoLimite.clear()

	def inactivo(self):        

	    while 1:
	        self.lastTurno.wait(600)
	        if(self.lastTurno.is_set()):
	            self.lastTurno.clear()
	        else:
	            send_message(self.chatid,"Terminando juego por inactividad")

	            self.cancelar()
	            return

	def cancelar(self):
		print('llamaron a cancelar')
		self.limite = 0
		self.iniciado = False
		send_marco(self.chatid,"\n\nJuego %s terminado\n\n" % (self.juego))
		if(self.chatid in jugando):
		    jugando.pop(self.chatid)
		self.on_close(self.botid)

def vor(message,juego):
    content = message['content']
    nickname = message['author']['nickname']
    userid = message['uid']
    preguntas = juego.preguntas
    turno = juego.turno
    jugadores = juego.jugadores
    chatid = juego.chatid
    libre = juego.libre
    admins = juego.admins
    retos = juego.retos
    iniciado = juego.iniciado
    if(iniciado):

	    if(content == '/v'):
	        if(len(preguntas) == 0 ):
	            send_message(chatid,'Se acabaron las preguntas de verdad')
	            return
	        if(libre):
	            send_message(chatid,nickname + " tienes que responder:\n\n" + preguntas.pop())
	            juego.next()
	        else:
	            if(userid == jugadores[turno]):
	                send_message(chatid,getNickname(userid) + " tienes que responder:\n\n" + preguntas.pop())
	                juego.next()
	            else:
	                send_message(chatid,getNickname(userid) + " no es tu turno")
	                send_message(chatid,'Turno de %s' % getNickname(jugadores[turno]))

	    elif(content == "/r"):
	        if(len(retos) == 0 ):
	            send_message(chatid,'Se acabaron los retos')
	            return
	        if(libre):
	            send_message(chatid,nickname + " tienes que hacer:\n\n" + retos.pop())
	            juego.next()
	        else:
	            if(userid == jugadores[turno]):
	                send_message(chatid,getNickname(userid) + " tienes que hacer:\n\n" + retos.pop())
	                juego.next()
	            else:
	                send_message(chatid,getNickname(userid) + " no es tu turno")
	                send_message(chatid,'Turno de %s' % getNickname(jugadores[turno]))
    if(userid not in admins):
    	return
    content = content.split(' ')
    if(content[0] == "/libre"):
    	if(len(content) == 2 and (content[1] == 'si' or content[1] == 'no')):
    		if(content[1] == 'si'):
    			juego.libre = True
    			send_message(chatid,'Activando modo libre, cualquier puede pedir preguntas')
    		else:
    			juego.libre = False
    			send_message(chatid,'Modo por turnos')
    	else:
    		send_message(chatid,'uso: /libre [si|no]: Desactiva o activa el modo libre')
    elif(content[0] == "/pasar"):
    	juego.next()
    elif(content[0] == '/limite'):
        if(len(content) == 2 and content[1].isdigit()):
            juego.limite = int(content[1])
            send_message(chatid,'Limite de tiempo por turno %ds' % (juego.limite))
            juego.lastTurnoLimite.set()
        else:
            send_message(chatid,'uso: /limite [segundos]: pone un tiempo limite por turno, 0 para ninguno')
            send_message(chatid,'limite de tiempo actual %ds' % (juego.limite))

with open('juegos/vor/preguntas.txt', 'r') as handler:
    preguntas = [line.rstrip() for line in handler]
with open('juegos/vor/retos.txt', 'r') as handler:
    retos = [line.rstrip() for line in handler]

