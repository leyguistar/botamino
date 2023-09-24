from collections import deque
from tipType import TipType
from comando import Comando
from programa import Programa
from goal import Goal
class Chat:

	def __init__(self,id,name,alias = '',bn = 0,mup = 0,mdown = 0,mensaje='',ops = [],modos={},tips={},coins=0,
		load= False,eventos = {},tipTypes={},placa='',tipoMensaje=100,discordid=None,goals = {},usersGoals= {},
		uid=None,comid=None,s = None,estados={},acciones={},interacciones={},settings={},strikes={},comandosDonacion={},
		intents=[],comandosBienvenida={},mensajeDonacion=None,idioma='es',mensajeDespedida='',stickerBienvenida=None,stickerDespedida=None,
		mensajeGif=""):
		self.id = id
		if(load):
			load()
		else:
			self.name = name
			self.alias = alias
			self.bn = bn
			self.mup = mup
			self.mdown = mdown
			self.mensaje = mensaje
			self.ops = ops
		self.s = s
		self.tips = tips
		self.coins = coins
		self.eventos = eventos
		self.tipTypes = tipTypes
		self.comandos = {}
		self.placa = placa
		self.tipoMensaje = tipoMensaje
		self.tags = {}
		self.discordid = discordid
		self.goals = goals
		self.usersGoals = usersGoals
		self.uid = uid
		self.comid = comid
		self.voz = 'google'
		self.interacciones = interacciones
		self.dar = {}
		self.pedidos = {}
		self.settings = settings
		self.strikes = strikes
		self.comandosDonacion = comandosDonacion
		self.intents = intents
		self.comandosBienvenida = comandosBienvenida
		self.autorizados = {}
		self.mensajeDonacion = mensajeDonacion
		self.idioma = idioma
		self.mensajeDespedida = mensajeDespedida
		self.stickerBienvenida = stickerBienvenida
		self.stickerDespedida = stickerDespedida
		self.mensajeGif = mensajeGif
	def save(self):
		self.s.chat(self.id,self.name,self.alias,self.bn,self.mup,self.mdown,self.mensaje,self.ops,self.coins,self.placa,self.uid,self.comid,self.tipoMensaje)
	def load(self):
		r = self.s.loadChat(self.id)
		self.name = r.name
		self.alias = r.alias
		self.bn = r.bn
		self.mup = r.mup
		self.mdown = r.mdown
		self.mensaje = r.mensaje
		self.ops = r.ops
		self.loadEvents()
	def loadSettings(self):
		settings = self.s.loadChatSettings(self.id)
		self.agradecer = settings[0]
		self.prefijo = settings[1]
		self.ponerMetas = settings[2]
		self.ponerEventos = settings[3]
		if(len(settings) > 4):
			self.voz = settings[4]
	def saveTipoMensaje(self,tipoMensaje):
		self.tipoMensaje = tipoMensaje
		self.s.chatMessageType(tipoMensaje,self.id)
	def saveModo(self,name,media_id,announcement):
		return self.s.chatModo(name,media_id,announcement,self.id)

	def saveTips(self):
		self.s.chatTips(self.tips,self.id)
	def createEvent(self,fecha,nombre,descripcion,comando=None,userid=None):
		if(nombre in self.eventos):
			return 'Ya hay un evento con ese nombre'
		self.s.chatEvent(fecha,nombre,descripcion,comando,userid,self.id)
		self.eventos[nombre] = (descripcion,fecha,comando,userid)
		return 'Evento creado ' + nombre
	def removeEvent(self,nombre):
		if(nombre not in self.eventos):
			return 'No hay un evento con ese nombre'
		else:
			self.eventos.pop(nombre)
			self.s.removeChatEvent(nombre,self.id)
			return 'Evento removido: ' + nombre
	def loadModo(self,name):
		return self.s.loadChatModo(name,self.id)
	def loadModos(self):
		self.modos = self.s.loadChatModos(self.id)
		return self.modos
	def loadTips(self):
		self.tips = self.s.loadChatTips(self.id)
		return self.tips
	def loadEvents(self):
		self.eventos = self.s.loadChatEvents(self.id)
		return self.eventos
	def loadTipTypes(self):
		self.tipTypes = self.s.loadChatTipTypes(self.id)
		return self.tipTypes

	def createTipType(self,nombre,desde,gif,font,mensaje,fontSize):
		for tip in self.tipTypes:
			if(desde == self.tipTypes[tip].desde):
				return 'Ya existe un nombre para ese nivel de donacion'
		self.tipTypes[nombre] = TipType(nombre,desde,gif,font,mensaje,fontSize)
		return self.s.chatTipType(nombre,desde,gif,font,mensaje,fontSize,self.id)

	def removeTipType(self,nombre):
		if(nombre in self.tipTypes):
			self.tipTypes.pop(nombre)
			self.s.removeTipType(nombre,self.id)

	def getTipType(self,coins):
		if(len(self.tipTypes) == 0 ):
			print('por alguna razon dice que el size es 0')
			return None
		maximo = -100
		nombre = None
		for t in self.tipTypes:
			if(coins > self.tipTypes[t].desde and self.tipTypes[t].desde > maximo):
				maximo = self.tipTypes[t].desde
				nombre = t
		if(nombre == None):

			print('por alguna razon nada cuadra con el nombre')
			return None
		return self.tipTypes[nombre]

	def createComand(self,nombre,comando,descripcion = "",userid=None):
		if(nombre in self.comandos):
			return 'ya hay un comando con ese nombre'
		self.s.chatComand(nombre,comando,descripcion,userid,self.id)
		self.comandos[nombre] = Comando(nombre,comando,userid,descripcion)
		return 'Comando ' + nombre + ' creado'
	def addComand(self,nombre,comando,userid):
		if(nombre not in self.comandos):
			return 'no existe ese comando'

		self.s.addChatComand(nombre,comando,userid,self.id)
		self.comandos[nombre].comandos = self.comandos[nombre].comandos + '\0' + comando
		return 'Comando ' + nombre + ' actualizado'

	def loadComandos(self):
		self.comandos = self.s.loadChatComands(self.id)
		return self.comandos
	def removeComand(self,nombre):
		if(nombre in self.comandos):
			r = self.s.removeChatComand(nombre,self.id)
			if(r):
				self.comandos.pop(nombre)
				return 'Eliminado el comando ' + nombre
			else:
				return 'Error eliminando el comando ' + nombre + '\nPosiblemente porque se esta usando en algun evento'
		else:
			return 'El comando ' + nombre + ' no existe'
	def userMessageCount(self,userid):
		return self.s.loadUserMessageCount(userid,self.id)
	def checkPremium(self):
		return self.s.checkChatPremium(self.id)
	def getPremium(self,userid,startbot,premium):
		return self.s.chatPremium(userid,startbot,premium,self.id)
	def programar(self,p):
		self.s.programar(p.nombre,p.comando,p.userid,p.tipo,p.minutos,self.id)
	def loadProgramas(self):
		return self.s.loadChatProgramas(self.id)
	def deletePrograma(self,nombre):
		self.s.deleteChatPrograma(nombre,self.id)
	def saveUserTag(self,userid,tag,text):
		if(userid not in self.tags):
			self.tags[userid] = {}								

		self.tags[userid][tag] = text 

		self.s.chatUserTag(userid,self.tags[userid],self.id)
	def loadUserTags(self):
		self.tags = self.s.loadChatUserTags(self.id)
		return self.tags
	def removeUserTag(self,userid,tag):
		if(userid in self.tags and tag in self.tags[userid]):
			self.tags[userid].pop(tag)
			self.s.chatUserTag(userid,self.tags[userid],self.id)
			return 'removida ' + tag
		else:
			return 'no tag ' + tag
	def loadAllUserMessages(self):
		return self.s.loadAllUserMessages(self.id)

	def loadDiscord(self):
		self.discordid =  self.s.loadDiscordGuild(self.id)
		return self.discordid
	def goal(self,monedasTotal,monedas,nombre,comando,userid,cantidad=None):
		if(cantidad):
			if(cantidad not in self.usersGoals): 
				self.s.chatGoalUsers(cantidad,nombre,comando,userid,self.id)
				self.usersGoals[cantidad] = Goal(0,0,nombre,comando,userid,cantidad)
				return True
		if(monedasTotal not in self.goals):
			self.goals[monedasTotal] = Goal(monedasTotal,monedas,nombre,comando,userid)
			self.s.chatGoal(monedasTotal,monedas,nombre,comando,userid,self.id)
			return True
		return False

	def loadGoals(self):
		self.goals = self.s.loadChatGoals(self.id)
		self.usersGoals = self.s.loadChatUsersGoals(self.id)
		return self.goals
	def borrarGoal(self,monedasTotal=None,cantidad=None):
		if(monedasTotal):
			if(monedasTotal in self.goals):
				self.goals.pop(monedasTotal)
				self.s.borrarChatGoal(monedasTotal,self.id)
		if(cantidad):
			if(cantidad in self.usersGoals):
				self.usersGoals.pop(cantidad)
				self.s.borrarChatUsersGoal(cantidad,self.id)
