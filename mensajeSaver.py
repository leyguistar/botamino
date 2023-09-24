import datetime
from time import time
import threading
from exception import PrintException
class MensajeSaver:
	def __init__(self,s,s2):
		self.handlerSave1 = s
		self.handlerSave2 = s2
		self.lockSave1 = threading.Lock()
		self.lockSave2 = threading.Lock()
		self.count1 = 0
		self.count2 = 0
	def save(self,chatid,mensaje):
		return
		self.count1 += 1
		self.lockSave1.acquire()
		try:
			try:
				self.handlerSave1.saveMessage(chatid,mensaje.id,mensaje.content,mensaje.tipo,mensaje.uid,mensaje.nickname,mensaje.createdTime,mensaje.mediaValue,mensaje.localMedia,mensaje.extensions)
			except Exception as e:
				PrintException()
		except:
			pass
		self.lockSave1.release()
		self.count1 -= 1
		return 
	def addSimple(self,chatid,uid,day):
		return
		self.count2 += 1
		self.lockSave2.acquire()
		try:
			try:
				self.handlerSave2.addSimpleMessage(chatid,uid,day)
			except Exception as e:
				PrintException()
		except:
			pass
		self.lockSave2.release()
		self.count2 -= 1
		return 		
	def setSave(self,s):
		self.handlerSave = s
