import pytz
from collections import deque
class User:

	def __init__(self,id,nickname,mup = 0,mdown = 0,warnings = 0,alias = "",s = None,bienvenida="",despedida="",saves={},packs={},timezone=None,premium=0,discordid=None,puntos=0):
		self.id = id
		self.nickname = nickname
		self.mup = mup
		self.mdown = mdown
		self.warnings = warnings
		self.alias = alias
		self.s = s
		self.despedida = despedida
		self.bienvenida = bienvenida
		self.saves = saves
		self.packs = packs
		self.timezone = None
		self.premium = premium
		self.discordid = discordid
		self.puntos = puntos
	def save(self):
		self.s.user(self.id,self.nickname,self.mup,self.mdown,self.alias,self.bienvenida,self.despedida,self.timezone,self.premium)
	def addSavedMessage(self,nombre,content,tipo):
		if(nombre in self.saves):
			return 'nombre usado ' + nombre
		self.saves[nombre] = (content,tipo)
		return self.s.saveUserMessage(nombre,content,tipo,self.id)

	def loadSave(self,nombre):
		if(nombre in self.saves):
			return self.saves[nombre]
		self.loadSaves()
		if(nombre in self.saves):
			return self.saves[nombre]
		return None
	def loadSaves(self):
		self.saves = {}
		for n,c,t in self.s.loadUserSaves(self.id):
			self.saves[n] = (c,t)
		return self.saves
	def deleteSave(self,nombre):
		return self.s.deleteUserSave(nombre,self.id)

	def addPack(self,name,stickers):
		if(name in self.packs):
			return 'nombre de pack usado'
		self.packs[name] = stickers
		self.s.addUserPack(name,stickers,self.id)
		return 'pack agregado'
	def loadPack(self,name):
		if(name in self.packs):
			return self.packs[name]
		self.loadPacks()
		if(name in self.packs):
			return self.packs[name]
		return None
	def loadPacks(self):
		self.packs = self.s.loadUserPacks(self.id)
		return self.packs
	def loadDiscord(self):
		self.discordid = self.s.loadDiscordUser(userid=self.id)
		return self.discordid
	