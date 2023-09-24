import datetime
from time import time
class Mensaje:
	def __init__(self,id,content,uid,nickname,createdTime,tipo,mediaValue,localMedia = '',extensions = r'{}'):
		self.id = id
		self.content = content
		self.uid = uid
		self.nickname = nickname
		self.createdTime = createdTime
		self.tipo = tipo
		self.mediaValue = mediaValue
		self.localMedia = localMedia
		self.extensions = extensions
