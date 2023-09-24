#!/usr/bin/env python3
from aminosocket import SocketHandler 
from save import Save
import simplejson as json
import amino
from time import time
from exception import PrintException
import threading
import datetime
from mensajeSaver import MensajeSaver
from amino.lib.util import headers as aminoHeaders
import requests
import random
def login(userid,client=None):
    s = Save(expected=True)
    try:
        if(not client):
            client = amino.Client()
        login = s.loginInfo(id=userid,dictionary=True)
        device_id = random.choice(deviceids)

        if(login['jsonResponse'] and login['lastLogin']+28800 > time()):
            print('inicio cache')
            secret = json.loads(login['jsonResponse'])['secret']
            client.login_cache(login['jsonResponse'])
            # client.login(secret=secret )
            # s.newSecret(userid,secret)
        elif(login['secret']  ):
            print('iniciando secret')
            r = client.login(secret=login['secret'],get=True,error=True,device_id=device_id)
            r1 = json.loads(r[1])
            secret = login['secret']
            r1['userProfile']['content'] = 'cache'
            r1['secret'] = secret
            r1 = json.dumps(r1)
            s.newLogin(id=client.profile.id,jsonResponse=r1)

        else:
            print('iniciando normal')
            r = client.login(email=login['email'],password=login['password'],get=True,error=True)

            if(type(r) == dict or r[0] != 200):
                print(userid)
                print(r)
                s.close()
                del s

                return None
                # return r['api:statuscode']
            r1 = json.loads(r[1])
            r1['userProfile']['content'] = 'cache'
            secret = r1['secret']

            r1 = json.dumps(r1)
            s.newLogin(id=client.profile.id,jsonResponse=r1)
            s.newSecret(id=client.profile.id,secret=secret)
        # print('client',id(client))
    except:
        PrintException()
    s.close()
    del s
    return client

with open('deviceids.txt','r') as h:
    deviceids = h.read().split('\n')


def loginBots():
    global client,bots
    bots = {}
    s = Save()
    bots = s.loadBots(None)
    bots = [i[0] for i in bots]
    s.cursor = s.db.cursor(dictionary=True)
    bot = s.loadBot('7c8d446e-c6b1-409a-897b-952c6fa95052')
    bot['userid'] = '7c8d446e-c6b1-409a-897b-952c6fa95052'
    s.cursor = s.db.cursor()
    client = login(bot['userid'])
    handler = SocketHandler(client.sid,client.device_id,prehan,bot['userid'],120,debug=False)
    socket = handler
    handler.start()
    s.close()

sockets = {}
lockSave = threading.Lock()
handlerSave = Save()
ley = 'your_uuid'
def prehan(data,botid):
    global client
    t = data['t']
    comid = data['o']['ndcId']
    if(comid == 0):
        return
    if('chatMessage' in data['o']):
        message = data['o']['chatMessage']
        messageId = message.get('messageId')
        tipo = message['type']
        chatid = message['threadId']
        if(chatid not in chatThreads):
            sub_client = client.sub_client(comid)
            thread = sub_client.get_chat_thread(chatid,raw=True)['thread']
            chatThreads[chatid] = thread
        else:
            thread = chatThreads[chatid]
        userid = message.get('uid')
        # if(userid != ley):
        #     return
        if(tipo != 0 and tipo != 121 and tipo != 103):
            if(message.get('content')):
                chatid = message.get('threadId')
                sub_client = client.sub_client(comid)
                if(sub_client):
                    userid = message.get('uid')
                    if(userid in bots):
                        return
                    r = sub_client.send_message(chatid,'Detectado un mensaje especial proveniente de este usuario',embedId=userid,embedType=0)
                    if(r != 200 and r['api:statuscode'] == 105):
                        login('7c8d446e-c6b1-409a-897b-952c6fa95052',client)
        else:
            if(thread['type'] != 0):
                return
            content = message.get('content')
            extensions = message.get('extensions',{})
            tipo = message['type']

            print(content)          
            if(not content):
                return
            sub_client = client.sub_client(comid)
            if(content == '/sigueme'):
                sub_client.send_message(chatid,'dale te sigo.')
                sub_client.follow(userid)
                return
            # elif(content == '/ayuda'):
            #     sub_client.send_message(chatid,'Mi unica funcion es detectar mensajes especiales que un usuario de amino normal no puede enviar y informar quien fue, a parte de eso no puedo sacar al responsable o reportarlo de ninguna forma')
            #     sub_client.send_message(chatid,'Para usarme invitame a un chat, si pones /sigueme te sigo, tambien puedes invitarme a una comunidad pasandome el link de esa comunidad')
            elif('linkSnippetList' in extensions or 'http://aminoapps.com/' in content):
                sub_client.send_message(chatid,'link detectado')
                if('linkSnippetList' in extensions):
                    link = extensions['linkSnippetList'][0]['link']
                else:
                    link = content
                response = requests.get(f"{client.api}/g/s/link-resolution?q={link}", headers=aminoHeaders.Headers(sid=client.sid).headers)
                # r = client.get_from_code(content[1])
                js = json.loads(response.text)
                if(js['api:statuscode'] == 107):
                    sub_client.send_message(chatid,'link invalido')
                    return
                extensions = js['linkInfoV2']['extensions']
                r = extensions.get('linkInfo',None)
                if(not r):
                    r = extensions.get('invitation',None)
                    newComId = extensions.get('community',{}).get('ndcId')
                    if(r):
                        newComId = r['ndcId']
                    if(not r and not newComId):
                        sub_client.send_message(chatid,'no se de que es este link')
                        return
                    if(r):
                        r = client.join_community(newComId,r['invitationId'])
                    else:
                        r = client.join_community(newComId)
                    if(r != 200):
                        print(r)
                        sub_client.send_message(chatid,'no pude unirme a la comunidad')
                        if(r['api:statuscode'] == 826):
                            sub_client.send_message(chatid,'alcance el maximo de comunidades')
                    else:
                        # s.comunidadesBots(newComId,client.profile.id)
                        sub_client.send_message(chatid,'me uni exitosamente a la comunidad')
                        sub_client.send_message(chatid,'Aqui esta mi link para que me encuentres, ya te sigo ndc://x%d/user-profile/%s' % (newComId,client.profile.id))
                        new_sub_client = client.sub_client(newComId)
                        new_sub_client.follow(userid)
                    return

            # else:
            #     sub_client.send_message(chatid,'Comandos: /ayuda /sigueme')
chatThreads = {}
client = amino.Client()
bots = []
loginBots()
print('iniciando safe bot preciona para interrumpir')
input()
for s in sockets.values():
	s.close()
