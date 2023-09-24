import amino
from save import Save
import ujson
import requests
import ujson as json
import os
import liteobjs
from liteobjs import chatThreads,users,marcos,comidChat,bienvenidas,tipoMensaje,imgdir,ley,leybot,botgroup,temporadas,dias,tzs,clients,defaultClient
from liteobjs import comandosComunidad,tipoMensajeChat,bots,youtubeLists,cachesYoutube,voces,chatsSettings
from liteobjs import safeMessageType,aliasesChat,chats,youtubethreads,comandos,tipos_comandos,opCustom
from liteobjs import adminBot,bannedUsers,bannedChats,confidence,bannedComunidades
from liteobjs import rolesComunidad,rolesUser,bucket,leyworld
from liteobjs import VOICE_SERVER_IP,VOICE_SERVER_PORT,channels,NUDE_DETECT_IP
from liteobjs import comunidades,mensajes,comandosReverseMap,palabrasIdioma
from liteobjs import ecchibot
from liteobjs import logros
from liteobjs import deviceids
from liteobjs import lastWaifu
from liteobjs import likesWaifu,trashWaifu
from liteobjs import fichas
from liteobjs import simps,simping,media
from liteobjs import cancelarLimpieza,seguirLimpiando
from liteobjs import cuentas
from channel import Channel
from channel import waitForChannel
import channel
import base64
from userStats import UserStats
from time import time
from exception import PrintException
import random
from urllib.parse import unquote
from urllib.parse import quote
import io
from googletrans import Translator
from time import time,sleep
import datetime 
import pytz
from user import User
import boto3
from botocore.exceptions import ClientError
from amino.lib.util import headers as aminoHeaders
import datetime
from youtube_search import YoutubeSearch as ys
import pafy
import threading
import ffmpeg
from comunidad import Comunidad
from gtts import gTTS
from contextlib import closing
import re
from unicodedata import normalize
from nsfw import picpurify,nudity,deepAI
import socket
from amino.lib.util import headers as aminoHeaders
from liteobjs import sockets
from interaccion import Interaccion
from PIL import Image
import zipfile
import mysql.connector
from litemusic import play_audio
from convert import convert
def nsfw(chat,mediaValue,userid,id,sub_client,s):
    r = picpurify(mediaValue)
    chatid = chat.id
    print('filtrando x2')
    print(r)
    if(r == True):
        sub_client.delete_message(chatId=chatid,messageId=id)
        strike(chat,userid,sub_client,s)
    elif(r == None):
        r = nudeDetect(mediaValue)
        if(r != None and r > 0.9):
            sub_client.delete_message(chatId=chatid,messageId=id)
            strike(chat,userid,sub_client,s)

        elif(r == None):
            r = nudity(mediaValue)
            if(r != None):
                if(r >= 0.9):
                    sub_client.delete_message(chatId=chatid,messageId=id)
                    strike(chat,userid,sub_client,s)

            else:
                r = deepAI(mediaValue)
                if(r > 0.9):
                    sub_client.delete_message(chatId=chatid,messageId=id)
                    strike(chat,userid,sub_client,s)

def strike(chat,userid,sub_client,s,n=1):
    chatid = chat.id
    if(userid == get_host(chatid,sub_client.comId)):
        send_message(chatid,mensajeid=429)
        return
    if(userid == ley):
        send_message(chatid,mensajeid=430)
        return
    if(userid not in chat.strikes):
        chat.strikes[userid] = n
    else:
        chat.strikes[userid] += n
    count = chat.strikes[userid]
    s.strike(chatid,chat.strikes)
    maxStrikes = chat.settings['maxStrikes']
    if(count >= maxStrikes):
        sub_client.kick(userid,chatid,False)
        send_message(chatid,mensajeid=461,args=(getNickname(userid,sub_client)))
    else:
        if(count == 1):
            send_message(chatid,mensajeid=462,args=(getNickname(userid,sub_client),maxStrikes-count))
        elif(count):
            send_message(chatid,mensajeid=463,args=(getNickname(userid,sub_client),count,maxStrikes-count))


def loadRespuestas(chatid,s):
    res = s.loadRespuestas(chatid)
    respuestas = {}
    for r in res.items():
        sre = re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", r[0]), 0, re.I
            )
        mensaje = normalize('NFKC',sre).lower()
        
        respuestas[mensaje] = r[1].split('|')
    return respuestas


def eraseMedia(objectid,m):
    s = Save()
    media = loadMedia(objectid,s)
    if(m not in media):
        s.close()
        return False
    r = media[m]
    if(r['type'] == 2):
        s3 = boto3.resource('s3')
        s3.Object(bucket,m.strip('https://%s.s3.amazonaws.com/' % (bucket)) ).delete()
    s.deleteMedia(r['id'])
    s.close()
    return True


def cargarVoces():   
    try:
        for i in boto3.client('polly',region_name='us-west-2').describe_voices()['Voices']:
            voiceid = i['Id']
            if(voiceid not in voces):
                voces.append(voiceid)
    except Exception as e:
        print('Error cargando voces',e)
        pass
    if('google' not in voces):
        voces.append('google')
    print(voces)
    text = ''
    for v in voces:
        text += ' ' + v
    return text
def decir(chatid,m,voz='google',idioma='es',onlyLive=False):
    channel = get_channel(chatid)
    if(channel):
        sendAudioRequest(channel,voz,1,m,idioma)
        return
    elif(onlyLive):
        return
    if(voz == 'google'):
        for i in range(3):
            try:
                tts = gTTS(text=m,lang=idioma,slow=False)
                path = '/tmp/' + str(int(time()*1000)) + '.mp3'
                tts.save(path)
                break
            except Exception as e:
                PrintException()
                print('error obteniendo audio reintentando')
            else:
                break
        else:
            send_reply(chatid,mensajeid=428,replyid=id)
            return
        send_audio(chatid,path,onlyLive=onlyLive)
    else:
        try:
            polly =  boto3.client('polly',region_name='us-west-2')
            response = polly.synthesize_speech(Text=m,OutputFormat='mp3',VoiceId=voz)
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    path = '/tmp/' + str(int(time()*1000)) + '.mp3'
                    try:
                        with open(path, "wb") as file:
                            file.write(stream.read())
                    except IOError as error:
                        print('IOERROR:',error)
                        send_message(chatid,mensajeid=431)
                    else:
                        send_audio(chatid,path,onlyLive=onlyLive)

        except ClientError as error:
            print('ClientError:',error)
            send_message(chatid,mensajeid=431)
def relogin(delay,secret,userid):
    while 1:
        sleep(delay)
        print('relogeando',userid)
        device_id  =random.choice(deviceids)
        client = amino.Client()
        try:
            r = client.login(secret=secret,get=True,device_id=device_id)
            if(type(r) == dict or r[0] != 200):
                print(userid)
                print(r)
                return None
                # return r['api:statuscode']
            try:
                sockets[userid].sid = client.sid    
            except:
                PrintException()
            try:
                bots[userid]['client'].sid = client.sid
            except:
                PrintException()
        except:
            PrintException()
        delay = 3600*12
    
def login(userid=None,client=None,save=None,alias=None):
    if(not save):
        s = Save(expected=True)
    else:
        s = save
    try:
        if(not client):
            client = amino.Client()
        if(userid):
            login = s.loginInfo(id=userid,dictionary=True)
        elif(alias):
            login = s.loginInfo(alias=alias,dictionary=True)
            userid = login['id']
        else:
            if(s != save):
                s.close()
                del s
            return None
        device_id = random.choice(deviceids)

        if(login['jsonResponse'] and login['lastLogin']+28800 > time()):
            print('inicio cache')
            if(login['secret']):
                secret = login['secret']
            else:
                secret = json.loads(login['jsonResponse'])['secret']
            client.login_cache(login['jsonResponse'])
            # client.login(secret=secret )
            # s.newSecret(userid,secret)
            t = threading.Thread(target=relogin,args=(57600,secret,userid) )
            t.daemon = True
            t.start()
        elif(login['secret']  ):
            print('iniciando secret')
            try:
                r = client.login(secret=login['secret'],get=True,error=True,device_id=device_id)
                r1 = json.loads(r[1])
            except Exception as e:
                print(e)
                print('fallo en logear a',login['id'])
                return None
            t = threading.Thread(target=relogin,args=(86400,login['secret'],userid) )
            t.daemon = True
            t.start()
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
                if(s != save):
                    s.close()
                    del s

                return None
                # return r['api:statuscode']
            r1 = json.loads(r[1])
            r1['userProfile']['content'] = 'cache'
            secret = r1['secret']
            t = threading.Thread(target=relogin,args=(86400,secret,userid) )
            t.daemon = True
            t.start()

            r1 = json.dumps(r1)
            s.newLogin(id=client.profile.id,jsonResponse=r1)
            s.newSecret(id=client.profile.id,secret=secret)
        # print('client',id(client))
    except:
        PrintException()
    if(s != save):
        s.close()
        del s
    return client
def getClient(userid):
    if(not userid):
        return None
    if(userid not in cuentas):
        return None
    else:
        cuenta = cuentas[userid]
    client = amino.Client()
    print('login',userid)
    if(time() > cuenta['lastLogin'] + 83000):
        device_id = random.choice(deviceids)
        print('secret',cuenta['secret'])
        r = client.login(secret=cuenta['secret'],device_id=device_id)
        cuenta['lastLogin'] = time()
        cuenta['sid'] = client.sid
        s = Save()
        s.newLoginCuenta(userid,client.sid)
        s.close()
    else:
        client = amino.Client()
        client.sid = cuenta['sid']
        client.profile = amino.objects.userProfile(None)
        client.profile.id = userid
        client.userId = userid

    return client
def inviteBot(chatid,comid,client,bot):
    newClient = bot['client']
    r = newClient.join_community(comid)
    print(r)
    comError = False
    if(r != 200):
        return (r["api:statuscode"],0)
    new_sub_client = newClient.sub_client(comid)
    new_sub_client.follow(client.profile.id)
    sub_client = client.sub_client(comid)
    r = sub_client.invite_to_chat(newClient.profile.id,chatid)
    print(r)
    status = r.get('api:statuscode',-1)

    r = new_sub_client.join_chat(chatid)
    print(r)
    if(r != 200):
        if(status != 0):
            return (status,1)
        else:
            return (r['api:statuscode'],2)
    return 0,3

def changeBot(chatid,comid,client,userid,content,m,s,idioma='es'):
    if(len(content) < 2):
        send_message(chatid,mensajeid=433)
        botsComunidad = s.loadBotsCommunity(comid)
        text = mensajes[idioma][694] + '\n'
        for b in botsComunidad:
            if(b not in bots):
                continue
            bot = bots[b]
            if( (bot['public'] == 1 or bot['owner'] == userid) and not bot['muted'] ):
                text += '%s: %s\n' % (bot['name'],bot['description'])
        send_message(chatid,text)
        text = ''
        if(True):
            text += '\n' + mensajes[idioma][695] + '\n'
            for bot in bots.values():
                if(bot['userid'] in botsComunidad):
                    continue
                if( (bot['public'] == 1 or bot['owner'] == userid) and not bot['muted'] ):
                    text += '%s: %s\n' % (bot['name'],bot['description'])
        send_message(chatid,text)
    else:
        joinChat = False
        sub_client = client.sub_client(comid)
        bot = None
        for b in bots.values():
            if(b['name'] == m):
                bot = b
                break
        conError = False
        if(bot):
            botid = bot['userid']
            if(bot['muted']):
                send_message(chatid,mensajeid=434)
                return
            newClient = bot['client']
            if(bot['public'] == 1):                                            
                if(comid == leyworld):
                    joinChat = True
                else:
                    botsComunidad = s.loadBotsCommunity(comid)
                    comunidad = comunidades.get(comid)
                    if(botid not in botsComunidad): 
                        send_message(chatid,mensajeid=610)
                        return
                    else:
                        joinChat = True
            elif(bot['public'] == 0 and (userid == bot['owner'] or userid == ley) ):
                r = newClient.join_community(comid)
                print(r)
                comError = False
                if(r != 200):
                    if(r["api:statuscode"] == 229):
                        send_message(chatid,mensajeid=435)
                        return
                    elif(r['api:statuscode'] == 826):

                        send_message(chatid,mensajeid=436)
                        return

                    conError = True    
                    # s.comunidadesBots(comid,botid)
            elif(bot['public'] == 2):
                send_message(chatid,mensajeid=464,client=adminBot['client'])                
            else:
                send_message(chatid,mensajeid=443)
            if(bot['owner'] == userid or joinChat or userid == ley):
                new_sub_client = newClient.sub_client(comid)
                new_sub_client.follow(client.profile.id)
                r = sub_client.invite_to_chat(newClient.profile.id,chatid)
                print(r)
                status = r.get('api:statuscode',-1)
                if(status != 0):
                    send_message(chatid,mensajeid=437)
                    if(status == 1637):
                        send_message(chatid,mensajeid=438)
                        return

                r = new_sub_client.join_chat(chatid)
                print(r)
                if(r != 200):

                    if(r['api:statuscode'] == 235):
                        send_message(chatid,mensajeid=434)
                    else:
                        send_message(chatid,mensajeid=440)
                    if(comError):
                        send_message(chatid,mensajeid=441)                                    
                    return
                clients[chatid] = bot['client']
                send_message(chatid,mensajeid=442)
                chat = chats.get(chatid)
                addLogro(chat,userid,30,s)
                s.botChat(chatid,bot['userid'])
        else:
            send_message(chatid,mensajeid=465,args=m)                                        


def topMessages(chatid,messages,sub_client,m=3,idioma='es'):
    messageCount = {}
    for u in messages:
        if(u in messageCount):
            messageCount[u] += 1
        else:
            messageCount[u] = 1
    tops = dict(sorted(messageCount.items(), key=lambda x: x[1],reverse=True) )
    # print(tops)
    i = 1
    text = ''
    for u in tops:
        n = tops[u]
        if(n == 1):
            text += mensajes[idioma][466] % (i,getNickname(u,sub_client)) + '\n'
        else:
            text += mensajes[idioma][467] % (i,getNickname(u,sub_client),n) + '\n'
        i += 1
        if(i > m):
            break
    return text

def topMessages2(chatid,messages,sub_client,m=3,idioma='es'):
    tops = dict(sorted(messages.items(), key=lambda x: x[1],reverse=True))
    # print(tops)
    i = 1
    text = ''
    for u in tops:
        n = tops[u]
        if(n == 1):
            text += mensajes[idioma][466] % (i,getNickname(u,sub_client)) + '\n'
        else:
            text += mensajes[idioma][467] % (i,getNickname(u,sub_client),n) + '\n'
        i += 1
        if(i > m):
            break
    return text
def create_sticker(client,url=None,file=None,data=None,tipo=None ):
    if(file):        
        mediaValue = client.upload_sticker(f=file,tipo=tipo)
    elif(data):
        mediaValue = client.upload_sticker(data=data,tipo=tipo)
    elif("/st1." not in url ):
        mediaValue = client.upload_sticker(url=url,tipo=tipo)
    else:
        mediaValue = url
    sub_client = client.sub_client(leyworld)
    r = sub_client.create_sticker_collection([{"name":"x","icon":mediaValue}])
    stickerid = r['stickerCollection']['stickerList'][0]['stickerId']
    return stickerid
def searchYoutube(chatid,m,idioma):
    for i in range(5):
        try:
            results = ys(m,20).to_dict()
            break
        except:
            pass
    else:
        results = []
    cacheYoutube = []
    cachesYoutube[chatid] = cacheYoutube
    n = 1
    text = mensajes[idioma][361] + '\n'
    for r in results:
        d = r['duration']
        if(type(d) == str):
            t = [int(x) for x in r['duration'].split(':')]
            i = 0
            d = 0
            for ti in t[::-1]:
                d += ti*60**i
                i+=1
        # print(d)
        if(d < 3600):
            text += '%d. %s %s\n' % (n,r['title'],r['duration'])
            r['duration'] = d
            cacheYoutube.append(r)
            n+=1    
    if(cacheYoutube):
        text += mensajes[idioma][468]
        send_message(chatid,text)
    else:
        send_message(chatid,mensajeid=444)
def send_youtube(chatid,n):
    cacheYoutube = cachesYoutube.get(chatid,[])
    youtubeList = youtubeLists[chatid]
    youtubeList.append(cacheYoutube[n-1])
    cacheYoutube = []
    youtubethreads[0] += 1
    try:
        youtubelock.acquire()

        v = pafy.new(youtubeList.popleft()['id'])
        print('duration',v.duration)
        d = v.duration
        if(type(d) == str):
            t = [int(x) for x in d.split(':')]
            i = 0
            d = 0
            for ti in t[::-1]:
                d += ti*60**i
                i+=1
        
        print('duration',d)
        for i in range(1):
            r = v.getbestaudio()

            print('best: ',r.bitrate,r.extension,r.get_filesize())
            audiostreams = v.audiostreams
            print('streams: ')
            for a in audiostreams:
                print(a.bitrate, a.extension, a.get_filesize())
            tn = str(r)
            path = '/tmp/' + r.filename
            if(not os.path.exists(path)):
                r.download(path)
            print('sending',path)
            if(d < 30):
                r = send_audio(chatid,path)
                if(r and r != 200 and r['api:statuscode'] == 314):
                    process = (ffmpeg
                               .input(path)
                               .output(f"{path}.aac", audio_bitrate="320k")
                               .overwrite_output()
                               .run_async(pipe_stdout=True)
                               )

                    process.wait()
                    r = send_audio(chatid,f"{path}.aac")
            else:
                r = send_audio(chatid,path)
            print(r)
            if(r and r != 200 and r['api:statuscode'] == 314):
                send_message(chatid,mensajeid=445)
                continue
            break
    except Exception as e:
        send_message(chatid,mensajeid=446)
        PrintException()
    finally:
        youtubelock.release()

    youtubethreads[0] -= 1
def flushMessages():
    TCP_IP = "127.0.0.1"
    TCP_PORT = 10004
    try:
        s = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_STREAM) # UDP
        s.connect((TCP_IP, TCP_PORT))
        data = {
            "comando":"flush"
        }

        s.send(json.dumps(data).encode('utf-8'))

        data = s.recv(1024).decode('utf-8')
        print(data)
    except Exception as e:
        print(e)
def recoverMessage(messageId):
    with open('logs/deleted_messages/%s' % (messageId),'r') as h:
        m = json.loads(h.read())
    return m
    # TCP_IP = "127.0.0.1"
    # TCP_PORT = 10004
    # try:
    #     s = socket.socket(socket.AF_INET, # Internet
    #                          socket.SOCK_STREAM) # UDP
    #     s.connect((TCP_IP, TCP_PORT))
    #     data = {
    #         "comando":"get",
    #         "id":messageId
    #     }

    #     s.send(json.dumps(data).encode('utf-8'))

    #     data = s.recv(10240).decode('utf-8')
    #     data = json.loads(data)
    #     if(data['result'] == 'ok'):
    #         return data['message']
    #     else:
    #         return False
    # except Exception as e:
    #     print(e)
def getCountMessagesUser(chatid,userid):
    TCP_IP = "127.0.0.1"
    TCP_PORT = 10004
    try:
        s = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_STREAM) # UDP
        s.connect((TCP_IP, TCP_PORT))
        data = {
            "comando":"count",
            "userid":userid,
            "chatid":chatid
        }

        s.send(json.dumps(data).encode('utf-8'))

        data = s.recv(1024).decode('utf-8')
        data = json.loads(data)
        if(data['result'] == 'ok'):
            return data['count']
        else:
            return False
    except Exception as e:
        print(e)

def top2(chatid,content,timeStamp,chat,sub_client,idioma):
    flushMessages()
    t = datetime.datetime.strptime(timeStamp, '%Y-%m-%dT%H:%M:%SZ')
    palabras = palabrasIdioma[idioma]
    if(len(content) < 2):
        tipo = palabras['todos']
        n = 3
    elif(len(content) == 2):
        n = 3
        tipo = palabras['todos']
        if(content[1].isdigit()):
            n = int(content[1])
        else:
            tipo = content[1]
    elif(len(content) == 3 and content[1].isdigit()):
        tipo = content[2]
        n = int(content[1])
    ayudar = True
    today = t.timetuple().tm_yday
    print(chatid,today)
    s = Save()
    if(tipo == palabras['diario'] or tipo == palabras['todos']):
        messages = s.loadAllUserMessagesSimple(chatid,today)
        text = mensajes[idioma][615] + '\n' + topMessages2(chatid,messages,sub_client,n,idioma=idioma)
        send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
        ayudar = False
    if(tipo == palabras['semanal'] or tipo == palabras['todos']):
        messages = s.loadAllUserMessagesSimple(chatid,today-7)
        text = mensajes[idioma][616] + '\n' + topMessages2(chatid,messages,sub_client,n,idioma=idioma)
        send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
        ayudar = False
    if(tipo == palabras['mensual'] or tipo == palabras['todos']):
        messages = s.loadAllUserMessagesSimple(chatid,today-30)
        text = mensajes[idioma][617] + '\n' + topMessages2(chatid,messages,sub_client,n,idioma=idioma)
        send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
        ayudar = False
    if(tipo == palabras['total'] or tipo == palabras['todos']):
        messages = s.loadAllUserMessagesSimple(chatid)
        text = mensajes[idioma][618] + '\n' + topMessages2(chatid,messages,sub_client,n,idioma=idioma)
        send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
        ayudar = False
    if(ayudar):
        with open('ayuda/%s/comandos/top.txt','r') as h:
            text = h.read()

        send_message(chatid,text)                           
    s.close()
def top(chatid,content,timeStamp,s,chat,sub_client):
    t = datetime.datetime.strptime(timeStamp, '%Y-%m-%dT%H:%M:%SZ')
    if(len(content) < 2):
        tipo = 'todos'
        n = 3
    elif(len(content) == 2):
        n = 3
        tipo = 'todos'
        if(content[1].isdigit()):
            n = int(content[1])
        else:
            tipo = content[1]
    elif(len(content) == 3 and content[1].isdigit()):
        tipo = content[2]
        n = int(content[1])
    ayudar = True
    today = datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S').timetuple().tm_yday
    if(tipo == 'diario' or tipo == 'todos'):
        messages = s.loadAllUserMessages(chatid,t - datetime.timedelta(days=1))
        text = 'Top diario:\n' + topMessages(chatid,messages,sub_client,n)
        send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
        ayudar = False
    if(tipo == 'semanal' or tipo == 'todos'):
        messages = s.loadAllUserMessages(chatid,t - datetime.timedelta(days=7))
        text = 'Top semanal:\n' + topMessages(chatid,messages,sub_client,n)
        send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
        ayudar = False
    if(tipo == 'mensual' or tipo == 'todos'):
        messages = s.loadAllUserMessages(chatid,t - datetime.timedelta(days=30))
        text = 'Top mensual:\n' + topMessages(chatid,messages,sub_client,n)
        send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
        ayudar = False
    if(tipo == 'total' or tipo == 'todos'):
        messages = s.loadAllUserMessages(chatid)
        text = 'Top mensajes:\n' + topMessages(chatid,messages,sub_client,n)
        send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
        ayudar = False
    if(ayudar):
        text = 'uso: /top [n] [diaro|semanal|mensual|total|todos|n]: muestra los usuarios que mas enviaron mensajes\nEjemplos:\n'
        text += '/top 5 mensual\n'
        text += '/top 4: (todos los tops 4)\n'
        text += '/top semanal: (top 3 semanal)\n'

        send_message(chatid,text)                           


def info(chatid,topic='bot',idioma='es',premium=False):
    mensaje = ''
    topics = [i.replace('.txt','') for i in os.listdir('info/' + idioma)]
    if(topic not in topics):
        send_message(chatid,mensajeid=469,args=topic)
        return
    with open('info/%s/%s.txt' % (idioma,topic), 'r') as handler:
        mensaje = handler.read()
    if(not premium):
        mensaje = mensaje.split('\n-----\n')[0]
    send_message(chatid,mensaje)
def addLogro(chat,userid,logro,s=None):
    if(type(chat) == str):
        chat = chats[chat]
    if(chat.idioma != 'es'):
        return
    chatid = chat.id
    close = False
    if(not s):
        close = True
        try:
            s = Save()
        except:
            return
    logrosUser = s.loadLogros(userid)
    sub_client = clients[chatid].sub_client(comidChat[chatid])
    if(logro not in logrosUser):
        s.addLogro(userid,logro)
        logro = logros[logro]
        puntos = logro['puntos']
        nombre = logro['nombre']
        descripcion = logro['descripcion']
        s.addPuntosUser(userid,puntos)
        send_message(chatid,'Felicidades %s conseguiste el logro \n[cb]%s\n%s\nGanas %d puntos' % (getNickname(userid,sub_client),nombre,descripcion,puntos ))
    if(close):
        s.close()
def preAddLogro(chatid,userid,logro):
    chat = chats.get(chatid)
    if(not chat):
        return
    s = Save()
    try:
        addLogro(chat,userid,logro,s)
    except:
        PrintException()
    s.close()
def mostrarAyuda(chatid,commandid=None,tipo=None,idioma='es'):
    mensaje = ''
    if(commandid):
        comando = comandosReverseMap[idioma][commandid]
        if(commandid in opCustom[chatid]):
            args = (comando,opCustom[chatid][commandid],tipos_comandos[idioma][comandos[commandid][1]] )            
            mensajeid=10
        else:
            args = (comando,comandos[commandid][0],tipos_comandos[idioma][comandos[commandid][1]] )
            mensajeid=10
        if(os.path.exists('ayuda/%s/comandos/%s.txt' % (idioma,comando))):
            text = mensajes[idioma][mensajeid] % args
            with open('ayuda/%s/comandos/%s.txt' % (idioma,comando)) as h:
                text += h.read()
            send_message(chatid,text.replace('\\','\n'))
        else:
            with open('ayuda/%s/%s.txt' % (idioma,tipos_comandos['base'][comandos[commandid][1]])) as h:
                commands = h.read().split('\n')
            text = None
            for c in commands:
                if(c.startswith(comando + ':')):
                    text = mensajes[idioma][mensajeid] % args
                    text += c
                    break
            if(text):
                send_message(chatid,text.replace('\\','\n'))
            else:
                send_message(chatid,mensajeid=11)
        return
    if(tipo == None):
        with open('ayuda/%s/general.txt' % (idioma), 'r') as handler:
            mensaje = handler.read()
    else:
        try:
            r = tipos_comandos[idioma].index(tipo)
        except ValueError:
            r = -1
        if(r < 0):
            send_message(chatid,mensajeid=12,args=(tipo) )
            return
        with open('ayuda/%s/%s.txt' %(idioma,tipos_comandos['base'][r]), 'r') as handler:
            mensaje = handler.read()

    send_message(message=mensaje, chatId=chatid)

def ping(chatid,createdTime,sub_client,idioma):
    data = {
        "type": 0,
        "content": 'pong!',
        "clientRefId": int(time() / 10 % 1000000000),
        "timestamp": int(time() * 1000)
    }
    data = json.dumps(data)
    response = requests.post(f"{sub_client.api}/x{sub_client.comId}/s/chat/thread/{chatid}/message", headers=aminoHeaders.Headers(data=data,sid=sub_client.sid).headers, data=data)
    t = json.loads(response.text)
    t = t['message']['createdTime']
    ping = datetime.datetime.strptime(createdTime, '%Y-%m-%dT%H:%M:%SZ')
    pong = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
    t = pong-ping
    text = f"{mensajes[idioma][391]}: {int(t.total_seconds())}s\n"
    st = str(response.elapsed)
    text += mensajes[idioma][392] % (st[st.rfind(':')+1:])
    send_message(chatid,text)

def enter_chat(chatid,comid,bot,bot2):
    client = bot['client']
    sub_client = client.sub_client(comid)
    client2 = bot2['client']
    r = client2.join_community(comid)
    print(r)
    if(r != 200):
        send_message(chatid,mensajeid=441)
        if(r['api:statuscode'] == 826):
            send_message(chatid,mensajeid=448)
            return

        return
    sub_client2 = client2.sub_client(comid)
    sub_client2.follow(client.profile.id)
    r = sub_client.invite_to_chat(client2.profile.id,chatid)
    print(r)
    # if(r.get('api:statuscode',-1) != 0):
    #     send_message(chatid,mensajeid=449)
        # return

    r = sub_client2.join_chat(chatid)
    print(r)
    if(r != 200):
        send_message(chatid,mensajeid=440)
        return
    clients[chatid] = bot['client']


def ver(chatid,u,chat,sub_client,idioma):
    r = sub_client.get_user_info(u,raw=True)
    if(r['api:statuscode'] != 0 ):
        r['api:statuscode']
    if('userProfile' not in r):
        return False
    js = r['userProfile']
    t = r['api:timestamp']
    checkTime = datetime.datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ')

    t = js['createdTime']
    joinedTime = datetime.datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ')
    diference = checkTime - joinedTime

    # send_link(chatid,js['icon'])
    text = mensajes[idioma][470] + '\n\n'
    text += mensajes[idioma][471] % (js['nickname']) + '\n'
    if(u in users):
        text += 'Alias: %s\n' % (users[u].alias)
    text += mensajes[idioma][472] % (js['membersCount']) + '\n'
    text += mensajes[idioma][473] % (js['joinedCount']) + '\n'
    text += mensajes[idioma][474] % (js['level']) + '\n'
    text += mensajes[idioma][475] % (js['reputation']) + '\n'
    text += mensajes[idioma][476] % (diference.days) + '\n'
    s = Save()
    r = s.loadRecibido(u)
    c = getCountMessagesUser(chatid,u)
    if(c):
        text += mensajes[idioma][477] % (c) + '\n\n'
    if(r):
        text += mensajes[idioma][619].replace('\\','\n') % (r['chocolates'],r['flores'],r['besos'],r['cariño'])
        text += mensajes[idioma][620].replace('\\','\n') % (r['citas'],r['novios'],r['matrimonios'])
    else:
        text += mensajes[idioma][619].replace('\\','\n') % (0,0,0,0)
        text += mensajes[idioma][620].replace('\\','\n') % (0,0,0)
    # simps = get_simps_user(u)
    # text += 'simps: %d\n\n' % (len(simps))
    # simping = get_simping_user(u)
    # if simping:
    #     ntext = mensajes[idioma][699]
    #     badsimping = []
    #     count = 0
    #     for us in simping:
    #         nickname = getNickname(us,sub_client)
    #         if(nickname):
    #             if(count):
    #                 ntext += ', %s' % (nickname)
    #             else:
    #                 ntext += ' %s' % (nickname)
    #                 count = 1
    #         else:
    #             badsimping.append(us)
    #     for us in badsimping:
    #         simping.remove(us)
    #     if(simping):
    #         text += ntext
    #         text += '\n\n'
    # text += mensajes[idioma][478] % (s.loadMensajesUserComunidad(u,chatid)) + '\n'
    try:
        userTags = s.loadUserTags(u)
    except:
        s.close()
        return
    s.close()
    texttag = 'Tags:\n'
    tagCount = 0
    if(u in chat.tags):
        for t in chat.tags[u]:
            if(chat.tags[u][t] != None):
                texttag += t + ':' + chat.tags[u][t] + '\n'
            else:
                texttag += t + '\n'
            tagCount += 1
    if(userTags != None):                                       
        for t in userTags:
            if(userTags[t] != None):
                texttag += t + ':' + userTags[t] + '\n'
            else:
                texttag += t + '\n'
            tagCount += 1
    if(tagCount):
        text += texttag

    sub_client.send_message(chatid,message=text,embedId=u,embedType=0)
    # send_message(chatid,text)
    return text
def simpsf(chatid,u,chat,sub_client,idioma):
    text = ''
    simps = get_simps_user(u)
    text += 'simps: %d\n\n' % (len(simps))
    simping = get_simping_user(u)
    if simping:
        ntext = mensajes[idioma][699]
        badsimping = []
        count = 0
        for us in simping:
            nickname = getNickname(us,sub_client)
            if(nickname):
                if(count):
                    ntext += ', %s' % (nickname)
                else:
                    ntext += ' %s' % (nickname)
                    count = 1
            else:
                badsimping.append(us)
        for us in badsimping:
            simping.remove(us)
        if(simping):
            text += ntext
            text += '\n\n'
    sub_client.send_message(chatid,message=text,embedId=u,embedType=0)
    return text

def invocar_a_todos(chatid,sub_client):
    ids = []
    for i in range(0,1000,100):
        users = sub_client.get_chat_users(chatid,i,100)
        ids += users.id
        if(len(users.id) < 99):
            break
    if(ley in ids):
        ids.remove(ley)
    send_invocacion(chatid,ids,'@todos')

def getJuegos():
    juegos = os.listdir('juegos')
    try:
        juegos.remove('__pycache__')
    except:
        pass
    try:
        juegos.remove('asesino')
    except:
        pass
    try:
        juegos.remove('retos')
    except:
        pass
    try:
        juegos.remove('fifos')
    except:
        pass
    try:
        juegos.remove('nn')
    except:
        pass
    juegos.append('mafia')
    juegos.sort()
    return juegos

def getTrueNickname(userid,sub_client):
    if(userid == None):
        return ''
    try:
        return sub_client.get_user_info(userid).nickname
    except:
        return ''
def getNickname(userid,sub_client,nick=None):
    if(userid == None):
        return ''
    user = getUser(userid)
    if(user):
        if(len(user.alias.lstrip()) > 0):
            return user.alias
        print(userid)
        if(not nick):
            r = sub_client.get_user_info(userid,raw=True)
            if('userProfile' in r):
                nick = r['userProfile']['nickname']
            else:
                nick = ''
    else:
        if(not nick):
            r = sub_client.get_user_info(userid,raw=True)
            if('userProfile' in r):
                nick = r['userProfile']['nickname']
            else:
                nick = ''

    return nick
def get_title(chatid,comid):
    chat = get_chat_thread(chatid,comid,clients[chatid])
    return chat['title']


def send_marco(chatid,mensaje,mup = 0,mdown = 0,tm=tipoMensaje):
    m = marcos[mup][0] + '\n\n' + mensaje + '\n\n' + marcos[mdown][1]
    send_message(chatid,m,tm)  

def send_reply(chatId,message=None,replyid=None,comid=None,mensajeid=None,args=None):
    client = clients[chatId]
    if(comid == None):
        sub_client = amino.SubClient(client=client,comId=comidChat[chatId])
    else:
        sub_client = amino.SubClient(client=client,comId=comid)        
    if(mensajeid != None):
        chat = chats.get(chatId)
        if(not chat):
            return
        message = mensajes[chat.idioma][mensajeid]
        if(args):
            message = message % (args)
    sub_client.send_message(message=message, chatId=chatId,replyTo=replyid)

def send_invocacion(chatId,mentionUserIds,message=""):
    client = clients[chatId]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatId])
    sub_client.send_message(message=message, chatId=chatId,messageType=0, mentionUserIds=mentionUserIds)

# def send_upload(chatid,embedImage):
#     sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
#     sub_client.send_message(chatId=chatid,embedBytes=embedImage)
def send_media(chatid,data=None,tipo=None,filename=None):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    if(filename):
        with open(filename,'rb') as h:
            data = h.read()
        tipo = 'imagen/' + filename[filename.rfind('.')+1:]
    if(not data):
        return
    link = None
    link = good_upload(data=data,tipo=tipo)
    if(link):
        sub_client.send_message(chatId=chatid,link=link)
def tmp(type):
    return '/tmp/' + str(time()).replace('.','') + '.' + type
def download(url):
    print(url)
    for i in range(3):
        response = requests.get(url)
        if(response.status_code == 200):
            break
    else:
        return None

    f = tmp(url[url.rfind('.')+1:])
    with open(f,'wb') as h:
        h.write(response.content)
    return f


def good_upload(data=None,tipo=None,filename=None,url=None,sanitized=False):
    client = defaultClient
    if(url):
        if(not sanitized):
            r = nudeDetect(url)
            if(r >= confidence):
                return False
            sanitized = True
        filename = download(url)

    if(filename):
        with open(filename,'rb') as h:
            data = h.read()
        tipo = 'image/' + filename[filename.rfind('.')+1:]
    if(not data):
        return
    link = None
    if(not sanitized):
        r = nudeDetect(data=data,ext='.' + tipo[tipo.find('/')+1:])
        if(r >= confidence):
            return False
    for i in range(5):
        try:
            link = client.upload_media(data=data,tipo=tipo)
            break
        except Exception as e:
            PrintException()
            print('reintentando upload')
    return link
def to_private_chat(userid,text,client,comid):
    sub_client = client.sub_client(comid)
    r = sub_client.start_chat([userid],message='')
    if(r[0] == 200):
        userchat = r[1]['thread']['threadId']
        send_message(userchat,text,dividir=True,comid=comid,pm=True,tm=0,client=client)
        return True
    else:
        return False
def send_audio_thread(chatid,file,onlyLive=False):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    channel = get_channel(chatid)
    if(channel):
        sendAudioRequest(channel,file,1,'audio','es')
        return
    elif(not onlyLive):
        if(file.startswith('http')):
            path = '/tmp/' + file[file.rfind('/')+1:]
            if(not os.path.exists(path)):
                c = requests.get(file).content
                with open(path, 'wb') as h:
                    h.write(c)
        else:
            path = file
        for i in range(3):
            r = sub_client.send_message(chatId=chatid,filePath=path)
            if(r == 200):
                break
        return r

def send_audio(chatid,file,onlyLive=False,esperar=False):
    if(esperar):
        return send_audio_thread(chatid,file,onlyLive)
    else:
        t = threading.Thread(target=send_audio_thread,args=(chatid,file,onlyLive))
        t.start()
def send_imagen(chatid,file,sanitized=False,conf=None,ecchi=False):
    if(not conf):
        conf = confidence
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    link = None
    if(not sanitized):
        with open(file,'rb') as h:
            data = h.read()
        r = nudeDetect(data=data,ext=file[file.rfind('.'):])
        if(r >= conf):
            return False
    link = good_upload(filename=file,sanitized=True)
    if(link):
        send_link(chatid,link,sanitized=True,ecchi=ecchi)
    return True
def send_sticker(chatid,stickerid,client=None):
    if(not client):
        client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    r = sub_client.send_message(chatId=chatid,stickerId=stickerid)


# def send_gif(chatid,gif):
#     client = clients[chatid]
#     sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
#     link = None
#     link = good_upload(data=gif,tipo='image/gif')
#     if(link):
#         sub_client.send_message(chatId=chatid,link=link)
nudeStartedTime = 0
NUDE_ACTUAL_IP = NUDE_DETECT_IP
def nudeDetect(m=None,data=None,ext=None):
    global nudeStartedTime,NUDE_ACTUAL_IP
    TCP_IP = NUDE_ACTUAL_IP
    TCP_PORT = 15150
    url = None
    s = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) # UDP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(3)
    try:
        print(TCP_IP,TCP_PORT)
        s.connect((TCP_IP, TCP_PORT))
    except (ConnectionRefusedError,socket.timeout) as e :
        print(e)
        if(TCP_IP != '127.0.0.1'):
            TCP_IP = '127.0.0.1'
            s = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_STREAM) # UDP
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(1)
            try:
                print(TCP_IP,TCP_PORT)
                s.connect((TCP_IP, TCP_PORT))
            except (ConnectionRefusedError,socket.timeout) as e:
                if(time () > nudeStartedTime + 300):
                    print('systemctl start nudedetect.service')
                    os.system('systemctl start nudedetect.service')
                    nudeStartedTime = time()
                    sleep(5)
                    s = socket.socket(socket.AF_INET, # Internet
                                         socket.SOCK_STREAM) # UDP
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.settimeout(1)

                    try:
                        s.connect((TCP_IP, TCP_PORT))
                    except (ConnectionRefusedError,socket.timeout) as e:
                        return None
                else:
                    return None
        else:
            NUDE_ACTUAL_IP = TCP_IP
            if(time () > nudeStartedTime + 300):
                os.system('systemctl start checkbots.service')
                nudeStartedTime = time()
                sleep(5)
                s.settimeout(1)

                try:
                    s.connect((TCP_IP, TCP_PORT))
                except (ConnectionRefusedError,socket.timeout) as e:
                    return None
            else:
                return None

    s.settimeout(5)

    print('evaluando',m)
    filename = None
    if(m):
        if(m.startswith('http')):
            url = m
        elif(not data):
            filename = m
        else:
            with open(m,'rb') as h:
                data = h.read()
            ext = m[m.rfind('.'):]
            print('url')
    if(url):
        print(('{"type":"url","url":"%s"}' % (url)).encode('utf') )
        s.send(('{"type":"url","url":"%s"}' % (url)).encode('utf') )
    elif(filename):
        print(('{"type":"file","filename":"%s"}' % (filename)))
        s.send(('{"type":"file","filename":"%s"}' % (filename)).encode('utf'))        
    else:
        if(data == None):
            return 0.0
        print(('{"type":"data","size":%d,"extension":"%s"}' % (len(data),ext)))
        s.send(('{"type":"data","size":%d,"extension":"%s"}' % (len(data),ext)).encode('utf'))
        r = s.recv(1024).decode('utf-8')
        if(r == 'ok'):
            s.send(data)
        else:
            return None
    data = s.recv(1024).decode('utf-8')
    s.close()
    print('data:',data)
    try:
        data = json.loads(data)
        v = float(list(data.values())[0]['unsafe'])
        print('unsafe: ',v)
    except:
        PrintException()
        v = 1
    return v
def start_game(juego,botid,chat):

    TCP_IP = "127.0.0.1"
    TCP_PORT = 10432
    chatid = chat.id
    comid = chat.comid
    admins = chat.ops
    try:
        s = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_STREAM) # UDP
        s.settimeout(3)

        try:
            s.connect((TCP_IP, TCP_PORT))
        except (ConnectionRefusedError,socket.timeout) as e:
            TCP_PORT = 10433
            try:
                s = socket.socket(socket.AF_INET, # Internet
                                     socket.SOCK_STREAM) # UDP
                s.settimeout(3)

                s.connect((TCP_IP, TCP_PORT))
            except:
                PrintException()
                return False

        except:
            PrintException()
            return False
        s.settimeout(None)

        data = {
            'comando':'start',
            'juego':juego,
            'botid':botid,
            'chatid':chatid,
            'comid':comid,
            'ops':admins,

        }
        data = json.dumps(data)
        s.send(data.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        data = json.loads(data)
        s.close()
        if(data['result'] == 'ok'):
            return True
    except:
        PrintException()
    return False

def send_link(chatid,link,tm=-1,sanitized=False,ecchi=False,confi=None):
    if(not sanitized):
        if(not confi):
            confi = confidence 
        result = nudeDetect(link)
        if(result >= confi):
            send_message(chatid,mensajeid=451)
            return False
    if(ecchi):
        client = ecchibot['client']
        tm = 57
    else:
        client = clients[chatid]
    comid = comidChat[chatid]
    sub_client = amino.SubClient(client=client,comId=comid)
    if(tm == -1 and get_chat_thread(chatid,comid,client)['type'] != 2 and bots[client.profile.id]['public']):
        tm = safeMessageType[0]
    if(tm == -1):
        tm = 0
    r = {}
    if(link):
        print(link,tm)
        for i in range(3):
            r = sub_client.send_message(chatId=chatid,link=link,messageType=tm,withResponse=True)
            if(r['api:statuscode'] == 0):
                break
    if(ecchi):
        m = r.get('message')
        if(m):
            delete_message(chatid,m['messageId'],sub_client,15)

    return r.get('message')
def borrarDeUsuario(chatid,userid):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    send_message(chatid,mensajeid=479,args=getNickname(userid,sub_client))
    messageList = sub_client.get_chat_messages(chatId=chatid,size=200,raw=True)['messageList']  # Gets messages of each chat
    for message in messageList:
        uid = message['uid']
        id = message['messageId']
        if(uid == userid):
            sub_client.delete_message(chatId=chatid,messageId=id)

def borrarMedia(chatid):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    send_message(chatid,mensajeid=480)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=200,raw=True)['messageList']  # Gets messages of each chat
    for message in messageList:
        if(message['mediaValue'] != None ):
            delete_message(chatId=chatid,messageId=message['messageId'],sub_client=sub_client)
    #send_message(message='listo', chatId=chatid)

def useridByLink(link,idioma='es'):
    print(link)
    if(link.startswith('http://aminoapps.com/p/')):
        response = requests.get(f"http://service.narvii.com/api/v1/g/s/link-resolution?q={link}", headers=aminoHeaders.Headers().headers)
        js = json.loads(response.text)
        if(js['api:statuscode'] == 107):
            return mensajes[idioma][121],False
        extensions = js['linkInfoV2']['extensions']
        r = extensions.get('linkInfo',None)
        if(not r):
            return mensajes[idioma][122],False
        targetUserid = r['objectId']
        if(r['objectType'] != 0):
            return mensajes[idioma][123],False
        return targetUserid,True
    else:
        return mensajes[idioma][121],False
def wikiByLink(link):
    print(link)
    if(link.startswith('http://aminoapps.com/p/')):
        response = requests.get(f"http://service.narvii.com/api/v1/g/s/link-resolution?q={link}", headers=aminoHeaders.Headers().headers)
        js = json.loads(response.text)
        if(js['api:statuscode'] == 107):
            return None
        extensions = js['linkInfoV2']['extensions']
        r = extensions.get('linkInfo',None)
        if(not r):
            return None
        target = r['objectId']
        if(r['objectType'] != 2):
            return None
        return target
    else:
        return None


def borrarN(chatid,n):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    if(n > 100):
        n = 100
    send_message(chatid,mensajeid=481,args=n)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=n)  # Gets messages of each chat

    for id,content in zip(messageList.messageId,messageList.content):
        delete_message(chatId=chatid,messageId=id,sub_client=sub_client)
def delete_message_thread_staff(chatId,messageId,sub_client,delay=0):
    sleep(delay)
    sub_client.delete_message(chatId,messageId)

def delete_message_thread_normal(chatId,messageId,sub_client,delay=0):
    sleep(delay)
    sub_client.delete_message(chatId,messageId,asStaff=True)

def delete_message_thread(chatId,messageId,sub_client):
    r = sub_client.delete_message(chatId,messageId)
    res = None
    if(r == 200):
        res = 200 
    r = sub_client.delete_message(chatId,messageId,asStaff=True)
    if(res == 200):
        return res
    return r
def delete_message(chatId,messageId,sub_client,delay=0):
    t = threading.Thread(target=delete_message_thread_normal,args=(chatId,messageId,sub_client,delay))
    t.daemon = True
    t.start()
    t = threading.Thread(target=delete_message_thread_staff,args=(chatId,messageId,sub_client,delay))
    t.daemon = True
    t.start()
def delete_ban_report(chatid,messageId,userid):
    client = clients.get(chatid)
    if(not client):
        return
    sub_client = client.sub_client(comidChat.get(chatid))
    if(userid != ley):
        delete_message(chatid,messageId,sub_client)
        sub_client.kick(userid,chatid,False)
        sub_client.flag_message('Hacker, Este mensaje hace uso de un bug de amino para dañar chats',2,messageId,chatid)
        r = sub_client.ban(userid,'Hacker, envio un mensaje que bugea el chat, lo reporte')
        print(r)
        s = Save()
        try:
            s.banUser(userid,'Usar bugs de la api')
        except:
            PrintException()
        s.close()
    print('enviando mensaje')
    sub_client.send_message(chatid,'Este usuario acaba de usar un bug que puede romper el chat',embedType=0,embedId=userid)
def get_host(chatid,comid,new=False):
    chat = get_chat_thread(chatid,comid,clients[chatid],new=new)
    return chat['uid']

def loadMedia(objectid,s):
    if(objectid not in media):
        if(s.db.is_connected()):
            result = s.loadMedia(objectid) 
        else:
            s.connect()
            result = s.loadMedia(objectid) 
            s.close()
        media[objectid] = result
    else:
        result = media[objectid]
    return result
def saveMediaSticker(chatid,m,stickerid,s):
    try:
        s.media(chatid,m,stickerid,3)
        media = loadMedia(chatid,s)
        media[m] =  s.loadMedia(chatid,m)

        send_message(chatid,mensajeid=452)
    except:
        return False
    else:
        return True
def saveMedia(chatid,m,message,sub_client,s,s3_link=None):
    mediaValue = message.get('mediaValue',None)
    mediaPath = 'media/' + chatid + '/'
    media = loadMedia(chatid,s)
    if(m in media):
        return False
    tipo = message['type']
    c = message.get('content',None)
    if(tipo == 3 and (mediaValue.endswith('.png') or mediaValue.endswith('.gif')) and sub_client.get_sticker_collection(message['extensions']['sticker']['stickerCollectionId']).collectionType != 2):
        return saveMediaSticker(chatid,m,message['extensions']['originalStickerId'],s)
    elif(mediaValue):
        ext = mediaValue[mediaValue.rfind('.')+1:]
        if(ext != 'jpeg' and ext != 'jpg' and ext != 'png' and ext != 'gif' and ext != 'aac'):
            send_message(chatid,mensajeid=453)
            return False
        else:                                       
            mediahd = mediaValue.replace('_00.','_uhq.')
            
            r = requests.get(mediahd)
            if(not r.ok):
                r = requests.get(mediaValue)
            img_data = r.content
            filename = mediaValue[mediaValue.rfind('/')+1:]
            path = mediaPath + filename
            upload_s3(img_data,path)
            try:
                s.media(chatid,m,'https://%s.s3.amazonaws.com/media/%s/%s' % (bucket,chatid,filename) ,2)
                media[m] =  s.loadMedia(chatid,m)
            except Exception as e:
                PrintException()
                return False
            else:
                send_message(chatid,mensajeid=482,args=m)
                return True

    elif(c):
        try:
            s.media(chatid,m,c,0)
            media[m] =  s.loadMedia(chatid,m)
        except Exception as e:
            PrintException()
            return False
        else:
            send_message(chatid,mensajeid=454)
            return True
    else:
        send_message(chatid,mensajeid=455)
        return False
def get_chat_bot(chatid):
    client = clients.get(chatid)
    if(not client):
        return
    return bots[client.profile.id]

def testBotInCommunity(chatid,comid,client,botid):
    return
    s = Save()
    try:
        if(bots[client.profile.id]['public'] and not test):
            botsComunidad = s.loadBotsCommunity(comid)
            
            if(botsComunidad and client.profile.id not in botsComunidad and client):
                for b in botsComunidad:
                    inviteBot(chatid,comid,bots[botid]['client'],bots[b])

                s.botChat(chatid,b)
                oldClient = client
                clients[chatid] = bots[b]['client']
                client = bots[b]['client']
                send_message(chatid,'Este chat tenia asignada a %s, pero ya no esta en la comunidad, asi que estare yo en reemplazo, si quieren cambiar de bot usen /bot' % (bots[oldClient.profile.id]['name']))
    except:
        PrintException()
    s.close()


def get_chat_bot_and_thread(chatid,comid,botid):
    if(test):
        timeout=10
    else:
        timeout=2
    t = time()
    lockGetLock.acquire()
    try:
        t = time()-t
        if(t > 1):
            print('get_chat_bot_and_thread_lock_1',t)
        if(chatid not in chatThreadBotLock):
            lock = threading.Lock()
            chatThreadBotLock[chatid] = lock
        else: 
            lock = chatThreadBotLock[chatid]
    except:
        PrintException()
    lockGetLock.release()
    t = time()
    lock.acquire()
    t = time()-t
    if(t > 1):
        print('get_chat_bot_and_thread_lock_2',t)
    client = clients.get(chatid)
    thread = None
    if(client):
        bid = client.profile.id
        if(bots[bid].get('muted')):
            if(bid == botid):
                lock.release()
                return None,None
            else:
                thread = None
        else:
            try:
                thread = get_chat_thread(chatid,comid,client,timeout=timeout)
            except:
                lock.release()
                return None,None
            # if(thread and not thread['cached']):
            #     t = threading.Thread(target=testBotInCommunity,args=(chatid,comid,client,botid))
            #     t.daemon = True
            #     t.start()
    if(not thread):
        client = bots[botid]['client']
        try:
            thread = get_chat_thread(chatid,comid,client,new=True,error=True,timeout=timeout)
        except:
            lock.release()
            # print('s 2')

            return None,None
        if(not thread or thread.get('api:statuscode',-1) != 0):
            lock.release()
            # print(thread)
            # print('s 3')

            return None,None
        if(chatid in bannedChats):
            try:
                sub_client = client.sub_client(comid)            
                sub_client.leave_chat(chatid)
            except:
                pass
            lock.release()
            # print('s 4')

            return None,None
        if(thread['membershipStatus'] != 0 ):
            clients[chatid] = client
            try:
                if(thread['membershipStatus'] == 2):
                    sub_client = client.sub_client(comid)
                    sub_client.join_chat(chatid)
                s = Save()
                s.botChat(chatid,client.profile.id)
                s.close()
            except:
                lock.release()
                # print('s 5')
                return None,None
        else:
            print('dude wtf')
    lock.release()

    return client,thread



def get_chat_thread(chatid,comid=None,client=None,new=False,error=False,timeout=None,sub_client=None):
    try:
        if(chatid in chatThreads and not new):
            chat = chatThreads[chatid]
            comidChat[chatid] = comid
            chat['cached'] = True
        else:
            if(not sub_client):
                sub_client = amino.SubClient(client=client,comId=comid)
            else:
                comid = sub_client.comId
            response = sub_client.get_chat_thread(chatid,raw=True,timeout=timeout)
            if(response['api:statuscode'] != 0):
                if(error):
                    return response
                else:
                    return None
            thread = response['thread']
            thread['api:statuscode'] = response['api:statuscode']
            chatThreads[chatid] = thread
            chat = chatThreads[chatid]
            comidChat[chatid] = comid
            chat['cached'] = False
        return chat
    except KeyError as e:
        PrintException()
    except requests.exceptions.ReadTimeout:
        print('timeout en getchat',chatid)
    except Exception as e:
        PrintException()
def getRolesComunidad(comid,s):
    if(comid not in rolesComunidad):
        rolesComunidad[comid] =  s.loadRolesComunidad(comid)
    return rolesComunidad[comid]
def sacarcoa(chat,comid,userid,host):
    client = login(host)
    sub_client = client.sub_client(comid)
    sub_client.remove_cohost(userid,chat)
def metercoa(chat,comid,userid,host):
    client = login(host)
    sub_client = client.sub_client(comid)

    cohosts = get_cohosts(chat,comid)
    if(userid not in cohosts):
        cohosts.append(userid)
    else:
        return True
    r = sub_client.edit_chat(chat,coHosts=cohosts)
    print(r)
    if(r == 200):
        send_message(chat,mensajeid=483,args=(getNickname(userid,sub_client)))
    else:
        send_message(chat,mensajeid=484)

def get_cohosts(chatid,comid,new=False):
    chat = get_chat_thread(chatid,comid,clients[chatid],new=new)
    if('coHost' in chat['extensions']):
        return chat['extensions']['coHost']
    else:
        return []


def mostrarJuegos(chatid,t):
    mensaje = ''
    if(t):
        with open('lite/juegos.txt', 'r') as handler:
            mensaje = handler.read()
    else:        
        with open('juegos.txt', 'r') as handler:
            mensaje = handler.read()
    mensaje += '\n\nJuegos actuales: '
    if(t):
        mensaje += 'vor, apa, apa2, aa, aa2, aa3, aa4, pelis, pelis2'
    else:
        for i in getJuegos():
            mensaje += str(i) + ' '
    send_message(message=mensaje, chatId=chatid)

def mostrarMarcos(chatid,comid):
    m = ""
    i = 0
    for l in marcos:
        m += str(i) + '\n'
        m += l[0] + '\n\n' + l[1] + '\n'
        i+=1
    send_message(message=m, chatId=chatid,comid=comid)

def ship(chatid,u1,u2,l = 0,idioma='es'):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    m = "💖💖💖💖💖💖💖💖💖💖💖💖\n\n"
    m+= getNickname(u1,sub_client) + " 💑 " + getNickname(u2,sub_client) + "\n\n"
    m+= "❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️"
    if(l > 0):
        sub_client.edit_chat(chatId=chatid,announcement=m,pinAnnouncement=True)
    send_message(chatid,m)
    path = 'interaccion/ship/'
    ipath = path + 'SFW/'
    lpath = path + 'SFWL/'
    imagenes = os.listdir(ipath)
    img = random.choice(imagenes)
    if(not os.path.exists(lpath + img) or time() > os.path.getmtime(lpath + img) + (3600*4)):
        link = good_upload(filename=ipath + img,sanitized=True)
        if(link):
            with open(lpath + img,'w') as h:
                h.write(link)
        else:
            return
    else:
        with open(lpath + img,'r') as h:
            link = h.read()
    with open(path + 'mensajes.%s' % (idioma),'r') as h:
        frases =  [line.rstrip().lower() for line in h]

    send_message(chatid,random.choice(frases) % (getNickname(u1,sub_client),getNickname(u2,sub_client)) )
    if(link):
        sub_client.send_message(chatId=chatid,link=link)

def isLeader(userid,sub_client):
    userInfo = sub_client.get_user_info(userid,raw=True)['userProfile']
    role = userInfo['role']
    if(role == 100 or role == 102):
        return True
    else:
        return False
def isStaff(userid,sub_client):
    userInfo = sub_client.get_user_info(userid,raw=True)['userProfile']
    role = userInfo['role']
    if(role == 100 or role == 102 or role == 101):
        return True
    else:
        return False

def isCurator(userid,sub_client):
    userInfo = sub_client.get_user_info(userid,raw=True)['userProfile']
    role = userInfo['role']
    if(role == 101):
        return True
    else:
        return False

def bienvenida(chatid,mensaje="",bn=0,mup=0,mdown=0,userid = None,nickname=None,idioma='es',client=None):
    if(not client):
        client = clients[chatid]
    comid = comidChat[chatid]
    sub_client = client.sub_client(comid)
    chatThread = get_chat_thread(chatid,comid,client,new=True)
    if(not chatThread):
        subText = None
    else:
        if(idioma == 'es'):
            subText = 'Miembro #%d' % (chatThread['membersCount'])
        else:
            subText = 'Member #%d' % (chatThread['membersCount'])

    if(nickname):
        send_message(client=client,message=marcos[mup][0] + '\n' + 
        '\n' + mensajes[idioma][485] + ' ' + nickname + "\n" + mensaje + '\n' + marcos[mdown][1], chatId=chatid,userid=userid,embedContent=subText) 
        return
    elif(not userid):
        if(mensaje == None):
            send_message(client=client,message=marcos[mup][0] + '\n' +
            bienvenidas[bn] + '\n' + marcos[mdown][1], chatId=chatid,userid=userid,embedContent=subText)
            return
        else:
            send_message(client=client,message=marcos[mup][0] + '\n' +
            bienvenidas[bn] + 
            '\n' + mensaje+ '\n' + marcos[mdown][1], chatId=chatid,userid=userid,embedContent=subText)
            return
    user = users.get(userid,None)
    if(user and user.bienvenida != ""):
        send_message(client=client,message=marcos[mup][0] + 
        '\n' + mensajes[idioma][486] + ' ' + getNickname(userid,sub_client) + "\n" + users[userid].bienvenida + '\n' + marcos[mdown][1], chatId=chatid,userid=userid,embedContent=subText)
        return
    else:
        send_message(client=client,message=marcos[mup][0] + '\n\n' + 
        '\n' + mensajes[idioma][485] + ' ' + getNickname(userid,sub_client) + "\n" + mensaje + '\n' + marcos[mdown][1], chatId=chatid,userid=userid,embedContent=subText)
        return

def despedir(chatid,message="",mup=0,mdown=0,userid = None,idioma='es'):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    if(userid == None):
        send_message(message=marcos[mup][0] +
        '\n\n'+ mensajes[idioma][487] + ' ' + message + '\n\n' + marcos[mdown][1], chatId=chatid)

    else:
        send_message(message=marcos[mup][0] +
        '\n\n' + mensajes[idioma][487] + ' ' + getNickname(userid,sub_client) + '\n\n' + marcos[mdown][1], chatId=chatid)
def get_comandos_comunidad(comid):
    if(comid not in comandosComunidad):
        s = Save()
        comandosComunidad[comid] =  s.loadComandosComunidad(comid)
        s.close()
    return comandosComunidad[comid]
def testMuted(bot):
    sub_client = bots['401ab401-8e9e-4ed7-91a2-50eeba7ab956']['client'].sub_client(leyworld)
    bot['client'].join_community(leyworld)
    sub_client.invite_to_chat([bot['userid']],botgroup)
    sub_client = bot['client'].sub_client(leyworld)
    r = sub_client.join_chat(botgroup)
    if(r != 200 and r['api:statuscode'] == 235):
        bot['muted'] = True
        print('muted',bot['userid'])
        botid = bot['userid']
        if(botid in sockets):
            sockets[botid].close()
        return True
    else:
        bot['muted'] = False
        return False
def getSubClient(chatid,comid=None,client=None):
    if(not client):
        client = clients.get(chatid)
    if(not client):
        return
    if(comid == None):
        comid = comidChat.get(chatid)
    if(not comid):
        return
    sub_client = amino.SubClient(client=client,comId=comid)        
    return sub_client

def changeToRed(chatid,sub_client):

    bubble = sub_client.get_chat_bubble(chatid)
    bubbleid = bubble['bubbleId']
    originalBubble = bubbleid
    templateid = bubble['templateId']
    if(not templateid):
        return
    tmpFile = '/tmp/red-%s.zip' % (bubbleid)
    oriFile = '/tmp/%s.zip' % (bubbleid)
    tmpDir = '/tmp/red-%s' % (bubbleid)

    if(not os.path.exists(tmpFile) ):
        resource = requests.get(bubble['resourceUrl']).content
        try:
            os.mkdir(tmpDir)
        except:
            pass
        with open(oriFile,'wb') as h:
            h.write(resource)
        zin = zipfile.ZipFile (oriFile, 'r')
        zout = zipfile.ZipFile (tmpFile, 'w')
        for item in zin.infolist():
            file = zin.read(item.filename)
            if (item.filename == 'config.json'):
                config = json.loads(file)
                config['linkColor'] = '#FF0000'
                file = json.dumps(config)

            zout.writestr(item,file)
        zout.close()
        zin.close()
    client = bots[sub_client.profile.id]['client']
    r = client.generate_bubble(templateid,f=tmpFile)
    bubbleid = r['chatBubble']['bubbleId']
    r = sub_client.apply_bubble(bubbleid,False,chatid=chatid)
    return originalBubble
def chat_bubble_background(chatid,sub_client,f):    
    with open(f,'rb') as h:
        bg = h.read()
    bubble = sub_client.get_chat_bubble(chatid)
    bubbleid = bubble['bubbleId']
    tmpFile = '/tmp/red-%s.zip' % (bubbleid)
    oriFile = '/tmp/%s.zip' % (bubbleid)
    tmpDir = '/tmp/red-%s' % (bubbleid)
    resource = requests.get(bubble['resourceUrl']).content
    try:
        os.mkdir(tmpDir)
    except:
        pass
    with open(oriFile,'wb') as h:
        h.write(resource)
    templateid = bubble.get('templateId')
    if(bubble['uid'] != sub_client.profile.id):
        templateid = "06276acd-5cf0-4432-88cd-1df02c065a60"
        r = sub_client.generate_bubble(templateid,f=oriFile)
        bubbleid = r['chatBubble']['bubbleId']
    originalBubble = bubbleid

    zin = zipfile.ZipFile (oriFile, 'r')
    zout = zipfile.ZipFile (tmpFile, 'w')
    name = ''
    for item in zin.infolist():
        file = zin.read(item.filename)
        if (item.filename == 'background.png' or item.filename == 'bg.png' ):
            file = bg
            name = item.filename
        if (item.filename == 'config.json'):
                config = json.loads(file)
                if('templateId' in config):
                    config.pop('templateId')
                file = json.dumps(config)

        zout.writestr(item,file)
    zout.close()
    zin.close()
    print(tmpFile)
    r = sub_client.create_bubble(bubbleid,f=tmpFile)
    print(r)
    if(r['api:statuscode'] != 0 ):
        return False
    bubbleid = r['chatBubble']['bubbleId']
    r = sub_client.apply_bubble(bubbleid,False,chatid=chatid)
    print(r)
    return originalBubble
def chat_bubble_sticker(chatid,sub_client,f,p):    
    with open(f,'rb') as h:
        bg = h.read()
    bubble = sub_client.get_chat_bubble(chatid)
    bubbleid = bubble['bubbleId']
    tmpFile = '/tmp/red-%s.zip' % (bubbleid)
    oriFile = '/tmp/%s.zip' % (bubbleid)
    tmpDir = '/tmp/red-%s' % (bubbleid)
    resource = requests.get(bubble['resourceUrl']).content
    try:
        os.mkdir(tmpDir)
    except:
        pass
    with open(oriFile,'wb') as h:
        h.write(resource)
    templateid = bubble.get('templateId')
    if(bubble['uid'] != sub_client.profile.id):
        templateid = "06276acd-5cf0-4432-88cd-1df02c065a60"
        r = sub_client.generate_bubble(templateid,f=oriFile)
        bubbleid = r['chatBubble']['bubbleId']
    originalBubble = bubbleid

    zin = zipfile.ZipFile (oriFile, 'r')
    zout = zipfile.ZipFile (tmpFile, 'w')
    name = f[f.rfind('/')+1:]
    allowedSlots = []
    change = True
    
    for item in zin.infolist():
        file = zin.read(item.filename)
        if (item.filename == 'config.json'):
                config = json.loads(file)
                if('templateId' in config):
                    config.pop('templateId')
                slots = config['slots']
                for e in slots:
                    if(e['align'] == p):
                        e['path'] = name
                        change = False
                if(change):
                    slots.append({
                            "y":0,
                            "x":0,
                            "align":p,
                            "path":name,
                            "stickerId":"7b482bea-3c53-4195-9a6c-8409da27999f"
                        })
                for e in slots:
                    a = e.copy()
                    a.pop('path')
                    a.pop('stickerId')
                    allowedSlots.append(a)

                config['allowedSlots'] = allowedSlots
                file = json.dumps(config)

        zout.writestr(item,file)
    zout.write(f,name)

    zout.close()
    zin.close()
    print(tmpFile)
    r = sub_client.create_bubble(bubbleid,f=tmpFile)
    print(r)
    if(r['api:statuscode'] != 0 ):
        return False
    bubbleid = r['chatBubble']['bubbleId']
    r = sub_client.apply_bubble(bubbleid,False,chatid=chatid)
    print(r)
    return originalBubble
def chat_bubble_color(chatid,sub_client,color):    
    bubble = sub_client.get_chat_bubble(chatid)
    bubbleid = bubble['bubbleId']
    tmpFile = '/tmp/red-%s.zip' % (bubbleid)
    oriFile = '/tmp/%s.zip' % (bubbleid)
    tmpDir = '/tmp/red-%s' % (bubbleid)
    resource = requests.get(bubble['resourceUrl']).content
    try:
        os.mkdir(tmpDir)
    except:
        pass
    with open(oriFile,'wb') as h:
        h.write(resource)
    templateid = bubble.get('templateId')
    if(bubble['uid'] != sub_client.profile.id):
        templateid = "06276acd-5cf0-4432-88cd-1df02c065a60"
        r = sub_client.generate_bubble(templateid,f=oriFile)
        bubbleid = r['chatBubble']['bubbleId']
    originalBubble = bubbleid

    zin = zipfile.ZipFile (oriFile, 'r')
    zout = zipfile.ZipFile (tmpFile, 'w')
    
    for item in zin.infolist():
        file = zin.read(item.filename)
        if (item.filename == 'config.json'):
                config = json.loads(file)
                if('templateId' in config):
                    config.pop('templateId')
                print(config['color'],color)
                config['color'] = color
                file = json.dumps(config)

        zout.writestr(item,file)
    zout.close()
    zin.close()
    print(tmpFile)
    r = sub_client.create_bubble(bubbleid,f=tmpFile)
    print(r)
    if(r['api:statuscode'] != 0 ):
        return False
    bubbleid = r['chatBubble']['bubbleId']
    r = sub_client.apply_bubble(bubbleid,False,chatid=chatid)
    print(r)
    return originalBubble
def chat_bubble_insets(chatid,sub_client,contentInsets):    
    bubble = sub_client.get_chat_bubble(chatid)
    bubbleid = bubble['bubbleId']
    tmpFile = '/tmp/red-%s.zip' % (bubbleid)
    oriFile = '/tmp/%s.zip' % (bubbleid)
    tmpDir = '/tmp/red-%s' % (bubbleid)
    resource = requests.get(bubble['resourceUrl']).content
    try:
        os.mkdir(tmpDir)
    except:
        pass
    with open(oriFile,'wb') as h:
        h.write(resource)
    templateid = bubble.get('templateId')
    if(bubble['uid'] != sub_client.profile.id):
        templateid = "06276acd-5cf0-4432-88cd-1df02c065a60"
        r = sub_client.generate_bubble(templateid,f=oriFile)
        bubbleid = r['chatBubble']['bubbleId']
    originalBubble = bubbleid

    zin = zipfile.ZipFile (oriFile, 'r')
    zout = zipfile.ZipFile (tmpFile, 'w')
    
    for item in zin.infolist():
        file = zin.read(item.filename)
        if (item.filename == 'config.json'):
                config = json.loads(file)
                if('templateId' in config):
                    config.pop('templateId')
                config['contentInsets'] = contentInsets
                file = json.dumps(config)

        zout.writestr(item,file)
    zout.close()
    zin.close()
    print(tmpFile)
    r = sub_client.create_bubble(bubbleid,f=tmpFile)
    print(r)
    if(r['api:statuscode'] != 0 ):
        return False
    bubbleid = r['chatBubble']['bubbleId']
    r = sub_client.apply_bubble(bubbleid,False,chatid=chatid)
    print(r)
    return originalBubble
def chat_bubble_zip(chatid,sub_client,resourceFile):    
    templateid = "107147e9-05c5-405f-8553-af65d2823457"
    r = sub_client.generate_bubble(templateid,f='templates/template.zip')
    print(r)
    bubbleid = r['chatBubble']['bubbleId']
    originalBubble = bubbleid
    r = sub_client.create_bubble(bubbleid,f=resourceFile)
    print(r)
    if(r['api:statuscode'] != 0 ):
        return False
    bubbleid = r['chatBubble']['bubbleId']
    r = sub_client.apply_bubble(bubbleid,False,chatid=chatid)
    print(r)
    return r
def chat_bubble_zoom(chatid,sub_client,contentInsets):    
    bubble = sub_client.get_chat_bubble(chatid)
    bubbleid = bubble['bubbleId']
    tmpFile = '/tmp/red-%s.zip' % (bubbleid)
    oriFile = '/tmp/%s.zip' % (bubbleid)
    tmpDir = '/tmp/red-%s' % (bubbleid)
    resource = requests.get(bubble['resourceUrl']).content
    try:
        os.mkdir(tmpDir)
    except:
        pass
    with open(oriFile,'wb') as h:
        h.write(resource)
    templateid = bubble.get('templateId')
    if(bubble['uid'] != sub_client.profile.id):
        templateid = "06276acd-5cf0-4432-88cd-1df02c065a60"
        r = sub_client.generate_bubble(templateid,f=oriFile)
        bubbleid = r['chatBubble']['bubbleId']
    originalBubble = bubbleid

    zin = zipfile.ZipFile (oriFile, 'r')
    zout = zipfile.ZipFile (tmpFile, 'w')
    
    for item in zin.infolist():
        file = zin.read(item.filename)
        if (item.filename == 'config.json'):
                config = json.loads(file)
                if('templateId' in config):
                    config.pop('templateId')
                config['zoomPoint'] = contentInsets
                file = json.dumps(config)

        zout.writestr(item,file)
    zout.close()
    zin.close()
    print(tmpFile)
    r = sub_client.create_bubble(bubbleid,f=tmpFile)
    print(r)
    if(r['api:statuscode'] != 0 ):
        return False
    bubbleid = r['chatBubble']['bubbleId']
    r = sub_client.apply_bubble(bubbleid,False,chatid=chatid)
    print(r)
    return originalBubble

def send_red_text(chatid,message,sub_client):
    originalBubble = changeToRed(chatid,sub_client)
    if(not originalBubble):
        send_message(chatid,message)
    sub_client.send_message(chatid,"[bc]" + "‎‏"+message+"‬‭",mentionUserIds=[sub_client.profile.id])
    sub_client.apply_bubble(originalBubble,False,chatid=chatid)
def send_botgroup(message,client=None,sub_client=None):
    if(not client):
        client = bots['401ab401-8e9e-4ed7-91a2-50eeba7ab956']['client']
    if(not sub_client):
        sub_client = client.sub_client(leyworld)
    sub_client.send_message(botgroup,message)
def send_message(chatId,message=None,tm=-1,comid=None,avisarError=False,client=None,userid=None,mensajeid=None,args=None,embedContent=None,ecchi=False,dividir=False,pm=False):
    if(not client):
        if(ecchi):
            client = ecchibot['client'] 
        else:
            client = clients.get(chatId)
    if(not client):
        return
    if(comid == None):
        comid = comidChat[chatId]
    sub_client = amino.SubClient(client=client,comId=comid)        
    chat = chats.get(chatId)
    if(not chat and not pm):
        if(not message):
            return
        if(userid):
            r = sub_client.send_message(message=message, chatId=chatId,messageType=0,embedType=0,embedId=userid,embedContent=embedContent)
        else:
            r = sub_client.send_message(message=message, chatId=chatId,messageType=0)        
        return
    if(pm):
        prefijo = '[c]'
    else:
        prefijo = chat.settings.get('prefijo','[c]')
        if(tm < 0):
            tm = tipoMensajeChat.get(chatId,tipoMensaje)
        if(mensajeid):
            message = mensajes[chat.idioma][mensajeid]
            if(args != None):
                message = message % args
    if(message==None):
        return
    if(tm == 0):
        message = (prefijo + message).replace('\n','\n' + prefijo)
        chatType = get_chat_thread(chatId,comid,client)['type']
        if(chatType == 1 or chatType == 0):
            if('http' in message or '.com' in message or 'paypal' in message):
                tm = safeMessageType[0]
                print('tm es ahora',tm)
    if(len(message) > 2000):
        print('el tamaño es mayor a 2000')
        if(dividir):
            l = []
            i = 0
            while 1:
                i = 2000
                limite = 1000
                while 1:
                    if(message[i] == '\n'):
                        break 
                    else:
                        i -= 1   
                        if(i <= limite):
                            break
                l.append(message[:i])
                message = message[i:] 
                if(len(message) <= 2000):
                    l.append(message)
                    break
            for m in l:
                print(m,chatId,tm)
                r = sub_client.send_message(message=m,chatId=chatId,messageType=tm)
                print(r)
            return
        else:
            message = message[:1997] + '...'
    if(userid):
        r = sub_client.send_message(message=message, chatId=chatId,messageType=tm,embedType=0,embedId=userid,embedContent=embedContent)
    else:
        if(ecchi):
            r = sub_client.send_message(message=message, chatId=chatId,messageType=57,withResponse=True)
            r = r.get('message')
            if(r):
                delete_message(chatId,r['messageId'],sub_client,30)
            return        
        else:
            r = sub_client.send_message(message=message, chatId=chatId,messageType=tm)
    return

    chatid = chatId
    if(r != 200 and tm != 100):
        statuscode = r['api:statuscode']
        if(comid in bannedComunidades):
            return
        if(chatid in changinBot):
            return
        if(statuscode == 235):
            testMuted(bots[client.profile.id])
        elif(statuscode == 230):
            print('fue baneado hacer algo')
    return r
    # sub_client.send_message(message=message, chatId=botgroup,messageType=tm)

def upload_file_s3(file_name, object_name=None,bucket=bucket):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL': 'public-read'})
    except ClientError as e:
        PrintException()
        return False
    return True

def upload_s3(data,object_name,bucket=bucket):
    s3_client = boto3.client('s3')
    b = io.BytesIO(data)
    try:
        response = s3_client.upload_fileobj(b, bucket, object_name,ExtraArgs={'ACL': 'public-read'})
    except ClientError as e:
        PrintException()
        return False
    return True



def rip(chatid,userid):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    send_message(chatid,'R.I.P ' + getNickname(userid,sub_client))


def getMediaValues(chatid,userid,usersid,replyid):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])    
    values = []
    mediaValue = None
    if(replyid):
        message = sub_client.get_message_info(chatid,replyid)
        mediaValue = message.json['mediaValue']
    # if(mediaValue and len(usersid) == 1):
    if(mediaValue):
        values.append(mediaValue)       

    elif(usersid):
        for u in usersid:
            info = sub_client.get_user_info(userId=u)
            if(info.icon):
                values.append(info.icon)
    elif(userid):

        info = sub_client.get_user_info(userId=userid)
        if(info.icon):
            values.append(info.icon)

    return values
def urlAmino(url,sanitized=False):
    print(url)
    if(not sanitized):
        r = nudeDetect(url)
        if(r >= confidence):
            return False

    img_data = requests.get(url).content
    return good_upload(img_data,url[url.rfind('.')+1:],sanitized=True)

def get_voice_chat_info(socket,chatid,comid):
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":"694481"
        },
        "t":100
    }
    d = json.dumps(data)
    socket.send(d.encode('utf-8'))

def request_channel_info(socket,chatid,comid):
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":"694481"
        },
        "t":200
    }
    d = json.dumps(data)
    socket.setCallBack(201,on_channel_info)
    socket.send(d.encode('utf-8'))  
def on_leave_channel(data,userid,extra):
    data = data['o']
    chatid = data['threadId']
    comid = data['ndcId']
    if(chatid in channels):
        leaveChannel(channels[chatid])
        channels.pop(chatid)

def on_channel_info(data,userid,extra):
    data = data['o']
    chatid = data['threadId']
    comid = data['ndcId']
    print('recibida informacion de channel')
    print(data)
    if('exception' in data):
        if(extra and extra.get('retry',0) > 0):
            extra['retry'] -= extra['retry']
            socket = extra['socket']
            socket.setCallBack(111,on_active_voice_join,extra)
            sleep(2)
            get_voice_chat_info(socket,chatid,comid)
        else:
            channel.setChannel(chatid)
        return
    print(data)
    name = data['channelName']
    token = data['channelKey']
    uid = data['channelUid']
    print('registrando channel')
    print(name,token,uid)
    if(get_chat_bot(chatid)['public'] and comid != leyworld):
        t = 1
    else:
        if(name.endswith('SCREENING_ROOM')):
            t = 5
        elif(name.endswith('AUDIO')):
            t = 1
        elif(name.endswith('NEW-VIDEO')):
            t = 4
        else:
            t = 1
    chat = chats.get(chatid)
    channels[chatid] = Channel(chatid,name,token,uid,t,userid,volume=chat.settings['volume'])
    channel.setChannel(chatid)
    
def start_live_mode(socket,chatid,comid,type=1):
    bot = bots[socket.userid]
    if(bot['public'] != 0):
        print('no es un bot premium')
        return

    join_voice_chat(socket,chatid,comid,1)
    create_channel(socket,chatid,comid,type)
    request_channel_info(socket,chatid,comid)
def create_channel(socket,chatid,comid,channelType):
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":"694481",
            "channelType":channelType
        },
        "t":108
    }
    d = json.dumps(data)
    extra = {
        "chatid":chatid,
        "comid":comid,
        'socket':socket
    }
    socket.setCallBack(127,on_create_channel_failed,extra)
    socket.send(d.encode('utf-8'))
def on_create_channel_failed(data,userid,extra):
    data = data['o']
    if('exception' in data):
        chatid = extra['chatid']
        comid = extra['comid']
        socket = extra['socket']
        if(data['exception']['code'] == 107):
            send_message(chatid,mensajeid=456)
        else:
            send_message(chatid,mensajeid=457)
        leave_voice_chat(socket,chatid,comid)
def remove_from_channel(socket,chatid,comid,userid):
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":"694481",
            "joinRole":2,
            "targetUid":userid
        },
        "t":126
    }
    d = json.dumps(data)
    socket.send(d.encode('utf-8'))


def set_video_channel_info(socket,chatid,comid,title,duration=300.0,author=None,icon=None,type=1,url=None):
    if(not icon):
        icon = socket.userid
    if(not icon):
        icon = 'http://st1.narvii.com/7680/d0b72bcf6e50745f0256acaf27770b2b8d70b763r5-184-180_00.jpeg'
    if(not url):
        url = 'http://st1.narvii.com/7680/d0b72bcf6e50745f0256acaf27770b2b8d70b763r5-184-180_00.jpeg'
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":"694481",
            "playlist":{
                "currentItemIndex":0,
                "currentItemStatus":2,
                "items":[
                    {
                    "author":author,
                    "duration":duration,
                    "isDone":False,
                    "mediaList":[[100,icon,None]],
                    "title":title,
                    "type":1,
                    "url":url
                    }
                ]
            }
        },
        "t":120
    }
    d = json.dumps(data)
    socket.send(d.encode('utf-8'))

def join_voice_chat(socket,chatid,comid,joinRole):
    id = str(int(time()*100)%1000000)
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":id,
            "joinRole":joinRole
        },
        "t":112
    }
    d = json.dumps(data)
    socket.send(d.encode('utf-8'))
    # d = json.dumps(data)
    # data = {}
    # e = threading.Event()
    # events = {
    #     113:(e,data)
    # }

    # socket.setEvent(id,events)
    # socket.send(d.encode('utf-8'))
    # e.wait(2)
    # if(e.is_set()):
    #     return True
    # else:
    #     return False
def get_voice_chat_info_and_join(socket,chatid,comid,wait=1):
    extra = {"retry":3,"socket":socket}
    socket.setCallBack(111,on_active_voice_join,extra)
    sleep(wait)
    get_voice_chat_info(socket,chatid,comid)
def set_channel_info(data,userid):
    data = data['o']
    chatid = data['threadId']
    comid = data['ndcId']
    print('recibida informacion de channel')
    print(data)
    if('exception' in data):
        return False
    print(data)
    name = data['channelName']
    token = data['channelKey']
    uid = data['channelUid']
    print('registrando channel')
    print(name,token,uid)
    if(get_chat_bot(chatid)['public'] and comid != leyworld):
        t = 1
    else:
        if(name.endswith('SCREENING_ROOM')):
            t = 5
        elif(name.endswith('AUDIO')):
            t = 1
        elif(name.endswith('NEW-VIDEO')):
            t = 4
        else:
            t = 1
    chat = chats.get(chatid)
    channels[chatid] = Channel(chatid,name,token,uid,t,userid,volume=chat.settings['volume'])
    return channels[chatid] 

def detect_or_join_channel(socket,chatid,comid):
    id = str(int(time()*100)%1000000)
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":id
        },
        "t":100
    }
    d = json.dumps(data)
    e = threading.Event()
    data = {}
    e = threading.Event()
    events = {
        101:(e,data)
    }
    
    socket.setEvent(id,events)
    socket.send(d.encode('utf-8'))
    e.wait(5)
    userid = socket.userid
    if(e.is_set()):
        data = data['data']
        userList = data['o']['userList']
        if(not userList):
            return 'No hay chat de voz activo'
        elif(userid in userList):
            return get_channel_info(socket,chatid,comid)
        else:
            join_voice_chat(socket,chatid,comid,1)
            return get_channel_info(socket,chatid,comid)
def get_channel_info(socket,chatid,comid):
    id = str(int(time()*100)%1000000)
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":id
        },
        "t":200
    }
    d = json.dumps(data)
    e = threading.Event()
    data = {}
    e = threading.Event()
    events = {
        201:(e,data)
    }
    socket.setEvent(id,events)
    socket.send(d.encode('utf-8'))
    e.wait(5)
    if(e.is_set()):
        data = data['data']
        channel = set_channel_info(data,socket.userid)
        return channel
    else:
        return False


def on_active_voice_join(data,userid,extra):
    t = data['o']['channelType']    

    chatid = data['o']['threadId']
    comid = data['o']['ndcId']
    if(t == 0):
        channel.setChannel(chatid)
        print('no hay chat activo')
        return
    print('uniendome al chat de voz')
    sleep(1)
    join_voice_chat(sockets[userid],chatid,comid,1)
    request_channel_info(sockets[userid],chatid,comid)

def leave_voice_chat(socket,chatid,comid):
    join_voice_chat(socket,chatid,comid,0)
def sendVideoRequest(channel,videoid,userid):
    name = channel.name
    token = channel.token
    uid = channel.uid
    type = channel.type
    botid = channel.botid
    volume = channel.volume
    chatid = channel.chatid
    print(chatid,channel,token,uid,type,volume,botid)
    s = Save()
    l = len(s.loadReproduciendo())
    actives = 0
    for i in range(5):
        try:
            actives = s.getActivePlayers()
            print(actives)
        except mysql.connector.errors.InternalError:
            sleep(2)
        except Exception as e:
            sleep(2)
            PrintException()
        else:
            break
    print(actives)
    if(not len(actives) ):
        s.close()
        print('no hay activos')
        return False
    if(l >= 5*len(actives)):
        s.close()
        return False
    s.setChannelInfo(chatid,name,token,uid,type,volume,botid)
    s.addPlayRequest(chatid,videoid,userid)
    count = len(s.loadQueue(channel.chatid))
    if(count > 20):
        addLogro(channel.chatid,userid,46,s)
    s.close()
    sendCheckRequest(channel,actives)

    return True
def sendPauseRequest(channel,s=None):
    data = {
        "comando":"pause",
        "channel":channel.name,
        "chatid":channel.chatid,
        "token":channel.token,
        "uid":channel.uid,
    }
    if(not s):
        s = Save()
        rep = s.loadReproduciendo(channel.chatid)
        s.close()
    else:
        rep = s.loadReproduciendo(channel.chatid)
    if(not rep):
        return False
    if(rep['instanceid'] == liteobjs.instanceid):
        ip = '127.0.0.1'
    else:
        ip = rep['ip']
    if(ip):
        data = json.dumps(data).encode('utf-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, VOICE_SERVER_PORT))
        s.send(data)
        data = s.recv(1024).decode('utf-8')
        print(data)
        js = json.loads(data)
        s.close()
        if(js['result'] == 'ok'):
            return True
        else:
            return False
    else:
        return False

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, VOICE_SERVER_PORT))
    s.send(data)
    data = s.recv(1024).decode('utf-8')
    js = json.loads(data)
    s.close()
    if(js['result'] == 'ok'):
        return True
    else:
        return False

def sendAudioRequest(channel,playid,t,text,idioma,s=None):
    saver = s
    if(not s):
        saver = Save()
    name = channel.name
    token = channel.token
    uid = channel.uid
    type = channel.type
    botid = channel.botid
    volume = channel.volume
    chatid = channel.chatid
    print(chatid,channel,token,uid,type,volume,botid)
    for i in range(5):
        try:
            actives = saver.getActivePlayers()
        except mysql.connector.errors.InternalError:
            sleep(2)
        except Exception as e:
            PrintException()
            sleep(2)
        else:
            break
    else:
        return False
    if(not actives):
        return False
    saver.setChannelInfo(chatid,name,token,uid,type,volume,botid)
    count = len(saver.loadQueue(channel.chatid))
    if(count > 0):
        saver.close()
        return False
    saver.addAudioRequest(chatid,playid,t,text,idioma)
    saver.close()
    sendCheckRequest(channel,actives)
    return True
def sendCheckRequest(channel,actives):
    chatid = channel.chatid
    data = {
        "comando":"check",
        "chatid":chatid,
        "channel":channel.name,
        "token":channel.token,
        "uid":channel.uid,
    }
    actives = sorted(actives, key=lambda k: k['cpu'])
    player = actives[0]
    # for player in actives:
    #     if(player['cpu'])
    if(player['instanceid'] == liteobjs.instanceid):
        print('son iguales las ip')
        player['ip'] = '127.0.0.1'
    ip = player['ip']
    if(ip):
        data = json.dumps(data).encode('utf-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, VOICE_SERVER_PORT))
        s.send(data)
        data = s.recv(1024).decode('utf-8')
        print(data)
        js = json.loads(data)
        s.close()
        if(js['result'] == 'ok'):
            return True
        else:
            return False
    else:
        return False


def sendPlayRequest(channel,s=None):
    data = {
        "comando":"play",
        "chatid":channel.chatid,
        "channel":channel.name,
        "token":channel.token,
        "uid":channel.uid,
    }
    if(not s):
        s = Save()
        rep = s.loadReproduciendo(channel.chatid)
        s.close()
    else:
        rep = s.loadReproduciendo(channel.chatid)
    if(not rep):
        return False

    if(rep['instanceid'] == liteobjs.instanceid):
        ip = '127.0.0.1'
    else:
        ip = rep['ip']
    if(ip):
        data = json.dumps(data).encode('utf-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, VOICE_SERVER_PORT))
        s.send(data)
        data = s.recv(1024).decode('utf-8')
        print(data)
        js = json.loads(data)
        s.close()
        if(js['result'] == 'ok'):
            return True
        else:
            return False
    else:
        return False

def requestPlayPosition(channel,s=None):
    data = {
        "comando":"position",
        "channel":channel.name,
        "token":channel.token,
        "uid":channel.uid,
        "chatid":channel.chatid

    }
    if(not s):
        s = Save()
        rep = s.loadReproduciendo(channel.chatid)
        s.close()
    else:
        rep = s.loadReproduciendo(channel.chatid)
    if(not rep):
        return False

    if(rep['instanceid'] == liteobjs.instanceid):
        ip = '127.0.0.1'
    else:
        ip = rep['ip']
    if(ip):
        data = json.dumps(data).encode('utf-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, VOICE_SERVER_PORT))
        s.send(data)
        data = s.recv(1024).decode('utf-8')
        print(data)
        js = json.loads(data)
        s.close()
        if(js['result'] == 'ok'):
            return js
        else:
            return False
    else:
        return False
def requestQueue(channel,s):
    if(s):
        r = s.loadQueue(channel.chatid)
    else:
        s = Save()
        r = s.loadQueue(channel.chatid)
        s.close()
    return r
    # data = json.dumps(data).encode('utf-8')
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((VOICE_SERVER_IP, VOICE_SERVER_PORT))
    # s.send(data)
    # data = s.recv(1024).decode('utf-8')
    # js = json.loads(data)
    # s.close()
    # if(js['result'] == 'ok'):
    #     queue = js['queue']
    #     return queue
    # else:
    #     return []
def requestVolumeChange(channel,volumen,s=None):
    data = {
        "comando":"volume",
        "channel":channel.name,
        "token":channel.token,
        "uid":channel.uid,
        "volume":volumen,
        "chatid":channel.chatid
    }
    if(not s):
        s = Save()
        rep = s.loadReproduciendo(channel.chatid)
        s.updateChannelVolume(channel.chatid,volumen)
        s.close()
    else:
        s.updateChannelVolume(channel.chatid,volumen)
        rep = s.loadReproduciendo(channel.chatid)
    channel.volume = volumen
    if(not rep):
        return False
    if(rep['instanceid'] == liteobjs.instanceid):
        ip = '127.0.0.1'
    else:
        ip = rep['ip']
    if(ip):
        data = json.dumps(data).encode('utf-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, VOICE_SERVER_PORT))
        s.send(data)
        data = s.recv(1024).decode('utf-8')
        print(data)
        js = json.loads(data)
        s.close()
        if(js['result'] == 'ok'):
            return True
        else:
            return False
    else:
        return False
def skipSong(channel,s=None):
    data = {
        "comando":"skip",
        "channel":channel.name,
        "token":channel.token,
        "uid":channel.uid,
        "chatid":channel.chatid
    }
    if(not s):
        s = Save()
        rep = s.loadReproduciendo(channel.chatid)
        s.close()
    else:
        rep = s.loadReproduciendo(channel.chatid)
    if(not rep):
        return False
    if(rep['instanceid'] == liteobjs.instanceid):
        ip = '127.0.0.1'
    else:
        ip = rep['ip']
    if(ip):
        if(ip == liteobjs.instanceid):
            ip = '127.0.0.1'

        data = json.dumps(data).encode('utf-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, VOICE_SERVER_PORT))
        s.send(data)
        data = s.recv(1024).decode('utf-8')
        try:
            js = json.loads(data)
        except:
            s.close()
            return True
        s.close()
        if(js['result'] == 'ok'):
            return True
        else:
            return False
    else:
        s = Save()
        l = len(s.loadReproduciendo())
        actives = 0
        for i in range(5):
            try:
                actives = s.getActivePlayers()
            except mysql.connector.errors.InternalError:
                sleep(2)
            except Exception as e:
                sleep(2)
                PrintException()
            else:
                break
        if(not actives):
            s.close()
            return False
        if(l >= 5*len(actives)):
            s.close()
            return False
        s.setChannelInfo(channel.chatid,channel.name,channel.token,channel.uid,channel.type,channel.volume,channel.botid)
        count = len(s.loadQueue(channel.chatid))
        s.close()
        return sendCheckRequest(channel,actives)
def leaveChannel(channel,s=None):
    data = {
        "comando":"cancel",
        "channel":channel.name,
        "token":channel.token,
        "uid":channel.uid,
        "chatid":channel.chatid

    }
    if(not s):
        s = Save()
        s.clearQueue(channel.chatid)
        rep = s.loadReproduciendo(channel.chatid)
        s.clearReproduciendo(channel.chatid)

        s.close()
    else:
        s.clearQueue(channel.chatid)
        rep = s.loadReproduciendo(channel.chatid)
        s.clearReproduciendo(channel.chatid)


    if(not rep):
        return False
    if(rep['instanceid'] == liteobjs.instanceid):
        ip = '127.0.0.1'
    else:
        ip = rep['ip']

    if(ip):
        data = json.dumps(data).encode('utf-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, VOICE_SERVER_PORT))
        s.send(data)
        data = s.recv(1024).decode('utf-8')
        try:
            js = json.loads(data)
        except:
            s.close()
            return True
        s.close()
        if(js['result'] == 'ok'):
            return True
        else:
            return False
    else:
        return False

def get_channel(chatid,comid=None,botid=None):
    if(not botid):
        client = clients.get(chatid)
        if(not client):
            return
        botid = client.profile.id
    if(comid == None):
        comid = comidChat.get(chatid)
    if(not comid):
        return
    if(chatid not in channels):
        e = threading.Event()
        waitForChannel(chatid,e)
        get_voice_chat_info_and_join(sockets[botid],chatid,comid,wait=0.0)
        print('esperando por respuesta')
        e.wait()
        if(chatid not in channels):
            return None
        return channels[chatid]
    else:
        return channels[chatid]

def sendYoutubeObject(chatid,sub_client,id,position,duration,userid,text='',title='',text2=''):
    thumb = 'https://i.ytimg.com/vi/%s/default.jpg' % (id)
    link = urlAmino(thumb,sanitized=True)
    if(not text2):
        text2 = '%s / %s' % (str(datetime.timedelta(seconds=position)),str(datetime.timedelta(seconds=duration)))
    if(not text):
        idioma = chats[chatid].idioma
        text = mensajes[idioma][427] + '\n'
        results = ys('v=%s' % (id),20).to_dict()
        for r in results:
            if(r['id'] == id):
                break
        text += r['title'] + '\n'
        title = r['title']
        text += mensajes[idioma][397] % (getNickname(userid,sub_client)) + '\n'
    sub_client.send_message(chatid,message=text,embedType=1,embedLink='https://www.youtube.com/watch?v=' + id,embedTitle=title,embedContent=text2,el=link)

def send_video_youtube_info(chatid,sub_client,id):
    thumb = 'https://i.ytimg.com/vi/%s/default.jpg' % (id)
    link = urlAmino(thumb,sanitized=True)
    r = ys('v=%s' % (id),1).to_dict()[0]
    t = r['duration'].split(':')
    d = 0
    i = 0
    for ti in t[::-1]:
        d += int(ti)*60**i
        i+=1

    set_video_channel_info(sockets[sub_client.profile.id],chatid,sub_client.comId,r['title'],d,r['channel'],link,1,url='https://www.youtube.com/watch?v=' + id)
def send_text_imagen(chatid,message,url=None,filename=None):
    client = clients.get(chatid)
    if(not client):
        return
    if(url and not filename):
        filename = convert(url=url)
    elif(filename and not url):
        url = client.upload_media(f=filename)
    filename = convert(filename=filename)
    comid = comidChat[chatid]
    sub_client = client.sub_client(comid)
    r = sub_client.send_message(chatid,fileEmbedImage=filename,fileEmbedType='image/png',message=message,fileEmbedImageLink=url,withResponse=True)
    # print(r)
    if(r['api:statuscode'] != 0):
        return False
    return True
def send_text_imagen_raw(chatid,message,url,filename):
    client = clients.get(chatid)
    if(not client):
        return
    comid = comidChat[chatid]
    sub_client = client.sub_client(comid)
    r = sub_client.send_message(chatid,fileEmbedImage=filename,fileEmbedType='image/png',message=message,fileEmbedImageLink=url,withResponse=True)
    if(r['api:statuscode'] != 0):
        return False
    return True
def send_ficha(chatid,ficha):
    client = clients.get(chatid)
    if(not client):
        return
    comid = comidChat[chatid]
    sub_client = client.sub_client(comid)
    r = sub_client.send_message(chatid,link=ficha['icon'],embedTitle=ficha['nombre'],embedContent=ficha['descripcion'],embedLink='ndc://x%d/item/ficha/%s' % (comid,ficha['wikiId']),withResponse=True)
    if(r['api:statuscode'] != 0):
        return False
    return True
def crearFicha(ficha):
    objectId = ficha['objectId']
    comid = ficha['comid']
    nombre = ficha['nombre']
    h = Save()
    h.ficha(ficha['nombre'],ficha['descripcion'],ficha['objectId'],ficha['wikiId'],ficha['icon'],ficha['comid'])
    h.close()
    if(comid not in fichas):
        fichas[comid] = {}
    if(objectId not in fichas[comid]):
        fichas[comid][objectId] = {}
    fichas[comid][objectId][nombre] = ficha


def send_booru(chatid,url,file_url,message='',sanitized=False,original=False,ecchi=False):
    if(not sanitized):
        r = nudeDetect(url)
        
        if(r > confidence):
            return False
    filename = convert(url=url)
    if(ecchi):
        client = ecchibot['client']
        tm = 57
    else:
        tm = 0
        client = clients.get(chatid)
        if(not client):
            return
    comid = comidChat[chatid]
    sub_client = client.sub_client(comid)
    link = file_url
    r = sub_client.send_message(chatid,fileEmbedImage=filename,fileEmbedType='image/png',messageType=tm,message=message,fileEmbedImageLink=link,withResponse=True)
    print(r)
    if(r['api:statuscode'] != 0):
        return False
    else:
        if(ecchi):
            m = r.get('message')
            if(m):
                delete_message(chatid,m['messageId'],sub_client,15)
            return True        

    # l = r['message'].get('extensions',{}).get('linkSnippetList',None)
    # print('sent file ' + filename)

    return True
def getCat(chatid):
    text = json.loads(requests.get('https://api.thecatapi.com/v1/images/search').text)
    r = text[0]['url']
    send_text_imagen(chatid,'miau',r)
def getGif(m):
    client = defaultClient
    tenorapikey = "23TJ3291LB82"
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=10" % (m, tenorapikey))
    link = None
    if(r.status_code == 200):
        js = json.loads(r.text)
        for i in range(10):
            media = random.choice(js['results'] )['media'][0]
            if(media['gif']['size'] < 4194304):
                url = media['gif']['url']
            else:
                url = media['tinygif']['url']
            link  = urlAmino(url)
            if(link):
                break
    return link

def reconectarSQL(s):
    try:
        s.db.reconnect(5)
    except Exception as e:
        PrintException()
        print('error reconnectando base de datos :/')
chatsRevisando = []
ignorar = True

def lanzarBienvenida(chatid,chat,nickname,userid,idioma='es',client=None):     
    print('lanzando bienvenida')               
    if(userid not in users):
        users[userid] = getUser(userid,nickname=nickname)
        bienvenida(chatid,chat.mensaje,chat.bn,chat.mup,chat.mdown,userid,nickname=nickname,idioma=idioma,client=client)
    else:
        bienvenida(chatid,chat.mensaje,chat.bn,chat.mup,chat.mdown,userid,idioma=idioma,client=client)

def responder_interacciones(tipo, chat,userid,sub_client,idioma):
    chatid = chat.id
    if(userid in chat.interacciones):
        accion = chat.interacciones[userid]
        comando = comandosReverseMap['es'][accion[0]]
        path = 'interaccion/%s/' % comando
        cPath = path + tipo + '.' + idioma
        if(time() > accion[2] + 60):
            chat.interacciones.pop(userid)            
            return False
        if(os.path.exists(cPath)):
            print('en esta parte de',tipo)
            print(accion)
            with open(cPath,'r') as h:
                frases = [line.rstrip() for line in h]
            frase = random.choice(frases) 
            print(frase)
            pos = len(frase)
            if('/' in frase):
                pos = frase.rfind('/')
                comando = frase[pos+1:]
            else:
                comando = None
            frase = frase[:pos] % (getNickname(userid,sub_client),getNickname(accion[1],sub_client))
            send_message(chatid,frase)
            print('hay un comando',comando)
            if(comando):
                if(comando != 'patear'):
                    send_interaccion(chatid,comando,userid,[accion[1]],sub_client,mensaje=False)
                    return True
            elif(tipo == 'corresponder'):
                send_interaccion(chatid,comandosReverseMap['es'][accion[0]],userid,[accion[1]],sub_client,mensaje=False)
                return True
            elif(tipo == 'esquivar'):
                send_interaccion(chatid,'esquivar',userid,[accion[1]],sub_client,mensaje=False)
                return True
        else:
            chat.interacciones.pop(userid)            
            return True
        chat.interacciones.pop(userid)            
        if(comando == 'patear'):
            return ('patear',accion[1])
    else:
        return False
interaccionesLinks = {}
interaccionesMensajes = {}
interaccionesFiles = {}
def send_interaccion(chatid,comando,userid,usersid,sub_client,mensaje=True,idioma='es',ecchi=False):
    path = 'interaccion/%s/' % (comando)
    ipath = path + 'SFW/'
    lpath = path + 'SFWL/'

    if(len(usersid) > 3):
        usersid = usersid[:3]
        send_message(chatid,mensajeid=14)
    # stats = s.loadStats()
    # stats.test()
    if(comando not in interaccionesLinks):
        links = {}
        interaccionesLinks[comando] = links
    else:
        links = interaccionesLinks[comando]
    if(comando not in interaccionesMensajes):
        mensajes = {}
        interaccionesMensajes[comando] = mensajes
    else:
        mensajes = interaccionesMensajes[comando]
    if(idioma not in mensajes):
        if(os.path.exists(path + 'mensajes1.%s' % (idioma) )):
            with open(path + 'mensajes1.%s' % (idioma),'r') as h:
                frases1 =  [line.rstrip() for line in h]
        else:
            frases1 = []
        if(os.path.exists(path + 'mensajes2.%s' % (idioma) )):
            with open(path + 'mensajes2.%s' % (idioma),'r') as h:
                frases2 =  [line.rstrip() for line in h]
        else:
            frases2 = []
        mensajes[idioma] = [frases1,frases2]
    else:
        frases1 = mensajes[idioma][0]
        frases2 = mensajes[idioma][1]
    if(comando in interaccionesFiles):
        files = interaccionesFiles[comando]
    else:    
        files = os.listdir(ipath)
        interaccionesFiles[comando] = files
    if(usersid and frases2):
        for u in usersid:
            img = random.choice(files)
            if(img not in links):
                if(not os.path.exists(lpath + img)  or time() > os.path.getmtime(lpath + img) + (3600)):
                    link = good_upload(filename=ipath + img,sanitized=True)
                    print(link)
                    if(link):
                        with open(lpath + img,'w') as h:
                            h.write(link)
                else:
                    with open(lpath + img,'r') as h:
                        link = h.read()
                links[img] = link
            else:
                link = links[img]
            if(mensaje):
                if(type(mensaje) == str):
                    send_message(chatid,mensajes,ecchi=ecchi)
                else:
                    send_message(chatid,random.choice(frases2).replace('@',comando[-1]) % (getNickname(userid,sub_client),getNickname(u,sub_client)),ecchi=ecchi )
            if(link):
                send_link(chatid,link,sanitized=True,ecchi=ecchi)
                # sub_client.send_message(chatId=chatid,link=link)

    else:
        if(os.path.exists(path + 'mensajes1.%s' % (idioma))):
            img = random.choice(files)
            if(img not in links):

                if(not os.path.exists(lpath + img) or time() > os.path.getmtime(lpath + img) + (3600*4) ):
                    link = good_upload(filename=ipath + img,sanitized=True)
                    print(link)
                    if(link and type(link) == str):
                        with open(lpath + img,'w') as h:
                            h.write(link)
                    else:
                        return
                else:
                    with open(lpath + img,'r') as h:
                        link = h.read()
                links[img] = link
            else:
                link = links[img]
            if(mensaje):
                if(type(mensaje) == str):
                    send_message(chatid,mensajes,ecchi=ecchi)
                else:
                    frase = random.choice(frases1).replace('@',comando[-1])
                    if('%s' in frase):
                        send_message(chatid,frase % (getNickname(userid,sub_client)),ecchi=ecchi)                    
                    else:
                        send_message(chatid,frase,ecchi=ecchi)
            if(link):
                send_link(chatid,link,sanitized=True,ecchi=ecchi)

                # sub_client.send_message(chatId=chatid,link=link)
        else:
            send_message(chatid,mensajeid=13,ecchi=ecchi)


def tp(chatid,userid,m,idioma):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])

    if(m != None):
        r = client.get_from_code(m)
        if(r.objectType == 12):
            com = r.json['extensions']['linkInfo']['ndcId']
            if(userid ==  get_host(r.objectId,com) or userid == ley):
                if(com != sub_client.comId):
                    send_message(chatid,mensajeid=458)

                client.join_community(com)
                comid = sub_client.comId
                sub_client.comId = com
                sub_client.join_chat(r.objectId)
                sub_client.comId = comid
                send_message(r.objectId,mensajes[idioma][488].replace('\\','\n'))

                send_message(botgroup,'tp de ndc://x%d/user-profile/%s' % (com,userid) +  
                    '\nA: ndc://x%d/chat-thread/%s' % (com,r.objectId) )
            else:
                send_message(chatid,mensajeid=459)
    else:
        send_message(chatid,mensajeid=460)
def horas(todas=False,idioma='es'):
    tnow = pytz.timezone('UTC').localize(datetime.datetime.utcnow())
    text = 'Hora: \n'
    if(todas):
        for tz in pytz.common_timezones:
            if('America' in tz):
                text += tz[tz.rfind('/')+1:] +': ' + tnow.astimezone(pytz.timezone(tz) ).strftime("%I:%M %p") + '\n'
    else:
        for tz in tzs[idioma]:
            text += tz[tz.rfind('/')+1:] +': ' + tnow.astimezone(pytz.timezone(tz) ).strftime("%I:%M %p") + '\n'
        text += 'Para todas /hora todas'
    return text
def parseprops(wiki):
    props = wiki['extensions']['props']
    l = {}
    for p in props:
        l[p['title']] = p['value']
    return l
def copy_profile(sub_client,js):
    js['extensions'] = js.get('extensions',{})
    if(not js['extensions']):
        sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'])
    elif('style' not in js['extensions']):
        sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
    elif('backgroundMediaList' in js['extensions']['style'] ):
        sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],backgroundImage=js['extensions']['style']['backgroundMediaList'][0][1],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
    else:
        sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],backgroundColor=js['extensions']['style']['backgroundColor'],defaultBubbleId=js['extensions'].get('defaultBubbleId'))

def limpieza(chatid,tipo,minrep,maxusers,sub_client):
    cancelarLimpieza[chatid] = False
    seguirLimpiando[chatid] = False
    totalkick = 0
    retryCount = 0
    host = get_host(chatid,sub_client.comId,new=True)
    cohosts = get_cohosts(chatid,sub_client.comId)
    chatThread = get_chat_thread(chatid,sub_client=sub_client)
    members = chatThread['membersCount']

    if(tipo == 'reputacion'):
        send_message(chatid,mensajeid=708,args=(minrep))
        for i in range(0,members+1,100):
            print(i)
            userss = sub_client.get_chat_users(chatid,i,size=100)
            for rep,id in zip(userss.reputation,userss.id):
                if(id in cohosts or id == host or id == ley or id in bots):
                    continue
                if(cancelarLimpieza[chatid]):
                    break
                print('comparando %d < %d' % (rep,minrep))
                if(rep < minrep):
                    print('sacando ' + id)
                    retryCount = 0
                    while( sub_client.kick(id,chatid,True) != 200):
                        print('retrying')
                        if(retryCount > 5):
                            break
                        retryCount += 1
                    else:                   
                        totalkick += 1
                    if(totalkick >= maxusers):
                        cancelarLimpieza[chatid] = True
                    if(totalkick % 50 == 0):
                        send_message(chatid,'Matados '+ str(totalkick) +' para seguir con la limpieza /seguir o /cancelar para cancelar la limpieza')

                        for i in range(60):
                            sleep(1)
                            if(seguirLimpiando[chatid]):
                                send_message(chatid,'Continuando limpieza')
                                seguirLimpiando[chatid] = False
                                break
                            if(cancelarLimpieza[chatid]):
                                send_message(chatid,'Cancelando limpieza')
                                break
                        else:
                            send_message(chatid,'Terminando limpieza por falta de confirmacion')
                            cancelarLimpieza[chatid] = True
                            break
            if(cancelarLimpieza[chatid]):
                break

    elif(tipo == 'actividad'):
        flushMessages()
        s = Save()
        userMessages = s.loadAllUserMessagesSimple(chatid)
        s.close()
        send_message(chatid,mensajeid=707,args=(minrep))
        for i in range(0,members+1,100):
            print(i)
            userss = sub_client.get_chat_users(chatid,i)
            for rep,id in zip(userss.reputation,userss.id):
                if(id in cohosts or id == host or id == ley or id in bots):
                    continue
                if(cancelarLimpieza[chatid]):
                    break
                print('agarrando total de mensajes')
                if(id not in userMessages):
                    count = 0
                else:
                    count = userMessages[id]
                print('comparando %d < %d' % (count,minrep))
                if(count < minrep):
                    print('sacando ' + id)
                    retryCount = 0
                    while( sub_client.kick(id,chatid,True) != 200):
                        print('retrying')
                        if(retryCount > 5):
                            break
                        retryCount += 1
                    totalkick += 1
                    if(totalkick >= maxusers):
                        cancelarLimpieza[chatid] = True
                    if(totalkick % 50 == 0):
                        send_message(chatid,'Matados '+ str(totalkick) +' anfi ponga /seguir para continuar o /cancelar para cancelar')

                        for i in range(60):
                            sleep(1)
                            if(seguirLimpiando[chatid]):
                                send_message(chatid,'Continuando limpieza')
                                seguirLimpiando[chatid] = False
                                break
                            if(cancelarLimpieza[chatid]):
                                send_message(chatid,'Cancelando limpieza')
                                break
                        else:
                            send_message(chatid,'Terminando limpieza por falta de confirmacion')
                            cancelarLimpieza[chatid] = True
                            break

            if(cancelarLimpieza[chatid]):
                break
    elif(tipo == 'invitados'):
        totalkick = 0
        while 1:
            users = sub_client.get_chat_users(chatid,size=100,type='invited',raw=True)['memberList']
            if(not users):
                break
            ts = []
            for u in users:
                t = threading.Thread(target=sub_client.kick,args=(u['uid'],chatid))
                t.daemon = True
                t.start()
                ts.append(t)
            for t in ts:
                t.join()
                totalkick += 1


    send_message(chatid,'Matados %d usuarios' % (totalkick))


def send_waifu(chatid,waifuId,client,withWiki=False):
    if(waifuId not in likesWaifu):
        h = Save()
        r = h.loadLikesWaifu(waifuId)
        h.close()
        likesWaifu[waifuId] = r[0]
        trashWaifu[waifuId] = r[1]
        likes = r[0]
        trash = r[1]
    else:
        likes = likesWaifu[waifuId]
        trash = trashWaifu[waifuId]

    subc = client.sub_client(210208021)
    wiki = subc.get_wiki_info(waifuId,raw=True)['item']
    props = wiki['extensions']['props']
    likes = likesWaifu[waifuId]
    trash = trashWaifu[waifuId]

    text = '[cb]%s' % (wiki['label']) + '\n\n'
    text += '[ci]%s' % (wiki['keywords']) + '\n'
    text += '[c]❤️ %d     🗑 %d'  % (len(likes),len(trash)) + '\n\n'
    for p in props:
        if(p['type'] == 'text'):
            text += '%s: %s\n' % (p['title'], p['value'])
    content = wiki['content'].split('\n\n')[0]
    text += content
    f = 'waifus/' + str(waifuId) + '.png'
    if(withWiki):
        url = 'ndc://x210208021/item/' + wiki['itemId']
        text += '\n\nPara la wiki puedes darle a la imagen'
    else:
        url = wiki['mediaList'][0][1]
    f = 'waifus/' + str(waifuId) + '.png'

    resize = 'waifus/resize_' + str(waifuId) + '.png'
    send_text_imagen_raw(chatid,text,filename=resize,url=url)

    # send_text_imagen(chatid,text,filename=f,url=url)
    lastWaifu[chatid] = waifuId

def get_simps_user(userid):
    if(userid in simps):
        return simps[userid]
    else:
        s = Save()
        simpList,simpingList = s.loadSimps(userid)
        s.close()
        simps[userid] = simpList
        simping[userid] = simpingList
        return simpList

def get_simping_user(userid):
    if(userid in simping):
        return simping[userid]
    else:
        s = Save()
        simpList,simpingList = s.loadSimps(userid)
        s.close()
        simps[userid] = simpList
        simping[userid] = simpingList
        return simpingList

def get_backGround(chatid,sub_client):
    thread = sub_client.get_chat_thread(chatid)
    return thread.json['extensions']['bm'][1]

def getUser(userid,nickname=None):
    if(userid not in users):
        if(mantenimiento):
            User(userid,'',s = None)
        s = Save(expected=True)
        try:
            user = s.loadUser(userid)

            if(not user):
                if(nickname != None):
                    user = User(userid,nickname,s = None)
                else:
                    user = User(userid,'',s = None)                
                    nickname = ''
                users[userid] = user
                s.user(userid,nickname,0,0,'','','',None,0)
            users[userid] = user
        except:
            PrintException()
        s.close()
        del s
    else:
        user = users[userid]
    return user
translator = Translator()
youtubelock = threading.Lock()
lockGetLock = threading.Lock()
changinBot = []
chatThreadBotLock = {}
mantenimiento = False
test = False
# with open('interacciones/stats.txt','r') as h:
#     for ln in h.read().split('\n'):
#         l = ln.split(' ')
#         interacciones[l[0]] = Interaccion((l[0].split('..')) )
