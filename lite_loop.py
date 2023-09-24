import amino
from save import Save
from time import sleep
from exception import PrintException
import datetime
import threading
from liteobjs import testBot
from liteobjs import bots
from litefuns import send_message
def get_new_members(comunidad):
	comid = comunidad.id
	usersContados = []
	if(comid not in communityLocks):
		lock = threading.Lock()
		communityLocks[comid] = lock
	else:
		lock = communityLocks[comid] 
	lock.acquire()
	while 1:
		try:
			if(not comunidad.botid or comunidad.botid not in bots):
				break
			sub_client = bots[comunidad.botid]['client'].sub_client(comunidad.id)
			result = sub_client.get_all_users(start=0,size=100,raw=True)
			if(result['api:statuscode'] == 106):
				break
			elif(result['api:statuscode'] == 229):
				break
			elif(result['api:statuscode'] != 0):
				sleep(5)
				continue
			miembros = result['userProfileCount']
			comunidad.miembros = miembros


			users = result['userProfileList']
			for u in users:
				if(u['uid'] in usersContados):
					continue
				usersContados.append(u['uid'])				
				messageWelcomeChat(comunidad,u,miembros)
				commentNewUserWall(comunidad,u,result['api:timestamp'])
		except:
			PrintException()
		sleep(10)
	lock.release()
def messageWelcomeChat(comunidad,u,miembros):
	comid = comunidad.id
	s = Save(autoConnect=False)
	s.connect()
	doneUsers = s.loadWelcomedUsers(comid)
	userid = u['uid']
	if(userid in doneUsers):
		s.close()
		return
	chatid = comunidad.welcomeChat
	m = comunidad.welcomeChatMessage
	if(not m or not chatid):
		s.close()
		return
	m = m.replace('[nick]',u['nickname'])
	client = bots[comunidad.botid]['client']
	send_message(chatid,m,comid=comid,client=client,userid=u['uid'],embedContent='#%d miembro de la comunidad' % (miembros))
	s.addWelcomedUser(comid,userid)
	s.close()
def commentNewUserWall(comunidad,u,timestamp):
	comid = comunidad.id
	s = Save(autoConnect=False)
	s.connect()
	commentedUsers = s.loadCommentedUsers(comid)
	s.close()
	userid = u['uid']
	if(comunidad.recibir and comunidad.botid):
		try:
			sub_client = bots[comunidad.botid]['client'].sub_client(comunidad.id)
			if(userid not in commentedUsers):

				s.connect()
				r = s.loadCommentedUser(comid,userid)
				if(not r):
					message = comunidad.wallMessage
					if(not message):
						s.close()
						return
					m = message.replace('[nick]',u['nickname'])
					r = sub_client.comment(message=m,userId=userid)
					if(r != 200):
						statuscode = r['api:statuscode']
						if(statuscode == 702):
							s.commentWallUser(comid,userid)						
						elif(statuscode == 270):
							print('incapas de escribir en el muro de',userid)
							print(r)
					else:
						print('firmado el muro de ndc://x%d/user-profile/%s' % (comid,userid))
						s.commentWallUser(comid,userid)
				s.close()
		except:
			PrintException()
communityLocks = {}