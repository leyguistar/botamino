#!/usr/bin/env python3
import amino
import os
import requests
import re
import threading
from collections import deque


client = amino.Client()
client.login(email='your_email', password='')
sub_client = amino.SubClient(comId='67', profile=client.profile)
oldMessages = []
ids = deque()

chat = 'e1ed3d4b-d58a-4209-ab1e-69218df1c3c6'
def mensajes():
    while 1:
        messageList = sub_client.get_chat_messages(chatId=chat,size = 5)  # Gets messages of each chat
        for id in messageList.messageId:
            if id in oldMessages: 
                continue
            print('guardando',id)
            ids.append(id)
            oldMessages.append(id)  # Adds message id to a list so it doesn't repeat commands
            sub_client.delete_message(chatId=chat,messageId=id)
def borrar():
    while 1:
        if(ids):
            id = ids.popleft()   
            print('borrando',id)     
            sub_client.delete_message(chatId=chat,messageId=id)
for i in range(3):
    t = threading.Thread(target=mensajes, args=())
    t.daemon = True
    t.start()

for i in range(3):
    t = threading.Thread(target=borrar, args=())
    t.daemon = True
    t.start()
t.join()
print('no funciono el join')
client.logout()
