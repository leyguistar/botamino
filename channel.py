class Channel:

	def __init__(self,chatid,name,token,uid,type,botid,volume=100):
		self.name = name
		self.token = token
		self.uid = uid
		self.type = type
		self.botid = botid
		self.volume = volume
		self.chatid = chatid
waitEvents = {}
def waitForChannel(chatid,e):
	waitEvents[chatid] = e
def setChannel(chatid):
	if(chatid in waitEvents):
		print('setting set for chat ',chatid)
		waitEvents[chatid].set()
		waitEvents.pop(chatid)