#!/usr/bin/env python3
import amino
import os
import sys
from pprint import pprint
from save import Save
from time import sleep
s = Save()
login = s.loginInfo(alias='bot')
s.cursor.close()
s.db.close()
client = amino.Client()
client.login(email=login[0],password=login[1])
sub_client = amino.SubClient(comId='67',profile=client.profile)
chat = {}
chat['nuevo'] = '29476c16-94ab-4a2c-a649-475f502a1049'
while True:
	users = sub_client.get_all_users(type='curators',save=True)
	for user in users.json['userProfileList']:
		print('baneando a ' + user['uid'])
		# sub_client.kick(chatId=chat['nuevo'],userId=user['uid'],allowRejoin=False)
		sub_client.unblock(user['uid'])
	users = sub_client.get_all_users(type='leaders',save=True)
	for user in users.json['userProfileList']:
		print('baneando a ' + user['uid'])
		sub_client.unblock(user['uid'])
		# sub_client.kick(chatId=chat['nuevo'],userId=user['uid'],allowRejoin=False)
client.logout()