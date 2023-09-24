import mysql.connector
import datetime
import pytz
import json
from time import time
from time import sleep
import re
import unicodedata
import threading
class Save:
	def __init__(self,file='default.set',autoConnect=True,connectionTimeOut=60,expected=True):
		if(file):
			with open(file,'r') as h:
				r = h.read().split('\n')
				self.host = r[0]
				self.dbuser = r[1]
				self.password = r[2]
		self.db = mysql.connector.CMySQLConnection()
		self.connectionTimeOut = connectionTimeOut
		self.expected = expected
		print(r)
		if(autoConnect):
			self.connect()
	class UnexpectedOpened(Exception):
	    def __init__(*args, **kwargs):
	        Exception.__init__(*args, **kwargs)

	def connect(self):
		if(not self.expected):
			raise self.UnexpectedOpened
		if(not self.db.is_connected()):
			r = self.db.connect(
			  host=self.host,
			  user=self.dbuser,
			  password=self.password,
			  database="amino2"
			)
			self.cursor = self.db.cursor(dictionary=True)
			# t = threading.Thread(target=self.closeTimeOut,args=(self.connectionTimeOut,) )
			# t.daemon = True
			# t.start()
		else:
			# self.cursor = self.db.cursor()
			print('is already connected')
	def __del__(self):
		self.close()
	def closeTimeOut(self,timeout):
		sleep(timeout)
		self.close()
	def close(self):
		if(self.db.is_connected()):
			self.db.close()		
	# def addToQueue()
	def checkQueue(self,chatid=None):
		if(chatid):
			self.cursor.execute('select * from musicqueue where chatid="%s";' % (chatid))
		else:
			self.cursor.execute('select * from musicqueue;')
		return self.cursor.fetchall()
	def removeFromQueue(self,id):
		self.cursor.execute('delete from musicqueue where id=%d' % (id))
		self.db.commit()
	def checkReproduciendo(self,chatid=None):
		self.cursor.execute('delete from reproduciendo where instanceid in (select instanceid from players where active=0);')
		if(chatid):
			self.cursor.execute('select * from reproduciendo where chatid="%s";' % (chatid))
			r = self.cursor.fetchone()
			return r
		else:
			self.cursor.execute('select * from reproduciendo;')			
			return self.cursor.fetchall()
	def getActivePlayers(self):
		self.cursor = self.db.cursor(dictionary=True)
		self.cursor.execute('select instanceid,ip,ram,lastTimeActive from players where active=1;')
		return self.cursor.fetchall()

	def addReproducir(self,chatid,playid,ip,instanceid):
		self.cursor.execute('insert into reproduciendo (chatid,playid,ip,instanceid) values ("%s","%s","%s","%s");' % (chatid,playid,ip,instanceid))
		self.db.commit()
	def removeReproduciendo(self,chatid=None,instanceid=None):
		if(chatid):
			self.cursor.execute('delete from reproduciendo where chatid="%s";' % (chatid))
		if(instanceid):
			self.cursor.execute('delete from reproduciendo where instanceid="%s";' % (instanceid))

		self.db.commit()

	def loadChannelInfo(self,chatid):
		self.cursor.execute('select channel,token,uid,type,volume,botid from channels where chatid="%s";' % (chatid))
		return self.cursor.fetchone()
	def clearQueue(self,chatid):
		self.cursor.execute('delete from musicqueue where chatid="%s";' % (chatid))
		self.db.commit()
	def reproductorInfo(self,instanceid,ip,ram,active,cpu,type):
		self.cursor.execute('delete from players where instanceid="%s";' % (instanceid))
		self.cursor.execute('insert into players (instanceid,ip,ram,active,lastTimeActive,cpu,type) values ("%s","%s",%d,%d,%d,%d,"%s");' % (instanceid,ip,ram,active,time(),cpu,type))
		self.db.commit()
	def updateInfo(self,instanceid,ram,active,cpu):
		self.cursor.execute('update players set active=%d, ram=%d, lastTimeActive=%d where instanceid="%s";' % (active,ram,time(),instanceid))
		self.db.commit()
	def removeReproductor(self,instanceid):
		self.cursor.execute('delete from players where instanceid="%s";' % (instanceid))
		self.db.commit()