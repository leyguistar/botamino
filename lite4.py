#!/usr/bin/env python3
import amino
import os
import requests
import re
import threading
import unicodedata
import random
import linecache
import traceback
import sys
from jikanpy import Jikan
import jikanpy
import animelyrics
from time import sleep
from googletrans import Translator
import pytz
import datetime
from PIL import Image, ImageDraw, ImageSequence,ImageFont
import io
import re
import signal
try:
    import simplejson as json
except ImportError:
    import json
    print('warning simplejson not installed please install it is more faster than json')
import html2text
from urllib.parse import unquote
from urllib.parse import quote
import urllib.request
from time import time
from gtts import gTTS
from save import Save
import mysql.connector.errors
from user import User
import socket
import ssl
from pybooru import Danbooru
from pybooru import Moebooru
from aminosocket import SocketHandler
from mensaje import Mensaje
import subprocess
userBot = 'bot'
test = False
verbose = False
sqlCredentials = 'default.set'
imgdir = 'imgs/'
output = True
for i in sys.argv:
    if('user=' in i):
        userBot = i[5:]
    elif(i == 'test'):
        test = True
    elif('sql=' in i):
        sqlCredentials = i[4:]
def relogin():
    s = Save()
    login = s.loginInfo(alias=userBot)
    r = client.login(email=login[0],password=login[1],get=True)
    if(r[0] != 200):
        print('Error re logeando')
        print(r)
    r1 = json.loads(r[1])
    r1['userProfile']['content'] = 'cache'
    r1 = json.dumps(r1)
    s.newLogin(id=client.profile.id,jsonResponse=r1)
    s.db.close()
client = amino.Client()
def login():
    s = Save()
    login = s.loginInfo(alias=userBot)
    if(login[2] and login[3] + 3600 > time()):
        print('inicio cache')
        client.login_cache(login[2] )
    else:
        print('iniciando normal')
        r = client.login(email=login[0],password=login[1],get=True)
        if(r[0] != 200):
            print('F')
            exit()
        r1 = json.loads(r[1])
        r1['userProfile']['content'] = 'cache'
        r1 = json.dumps(r1)
        s.newLogin(id=client.profile.id,jsonResponse=r1)
    s.db.close()
login()
interaciones1 = os.listdir('interaccion/1')
interaciones2 = os.listdir('interaccion/2')
tipoMensaje = 0
oldMessages = []
# interaciones2.remove('cum')
# interaciones2.remove('coger')
# interaciones1.remove('gemir')
# hardcoreComandos = ['cum','coger','gemir']
def getNickname(userid,sub_client):
    if(userid == None):
        return ''
    if(userid in users):
        if(len(users[userid].alias.lstrip()) > 0):
            return users[userid].alias
        nick = sub_client.get_user_info(userid).nickname
    else:
        return sub_client.get_user_info(userid).nickname

    return nick
def get_title(chatid,comid):
    chat = get_chat_thread(chatid,comid)
    return chat['title']


def send_marco(chatid,mensaje,mup = 0,mdown = 0):
    m = marcos[mup][0] + '\n\n' + mensaje + '\n\n' + marcos[mdown][1]
    send_message(chatid,m)  

def send_reply(chatId,message,replyid,comid=None):
    if(comid == None):
        sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatId])
    else:
        sub_client = amino.SubClient(profile=client.profile,comId=comid)        
    if(output):
        sub_client.send_message(message=message, chatId=chatId,replyTo=replyid)
        # sub_client.send_message(message=message, chatId=botgroup,replyTo=replyid)

def send_invocacion(chatId,mentionUserIds,message=""):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatId])
    if(output):
        sub_client.send_message(message=message, chatId=chatId,messageType=tipoMensaje,mentionUserIds=mentionUserIds)
        # sub_client.send_message(message=message, chatId=botgroup,messageType=tipoMensaje,mentionUserIds=mentionUserIds)

def send_upload(chatid,embedImage):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    if(output):
        sub_client.send_message(chatId=chatid,embedBytes=embedImage)
        # sub_client.send_message(chatId=botgroup,embedBytes=embedImage)
def send_media(chatid,data=None,tipo=None,filename=None):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    if(filename):
        with open(filename,'rb') as h:
            data = h.read()
        tipo = 'imagen/' + filename[filename.rfind('.')+1:]
    if(not data):
        return
    link = None
    for i in range(3):
        try:
            link = client.upload_media(data=data,tipo=tipo)
            break
        except Exception as e:
            print('reintentando send media')
    if(link and output):
        sub_client.send_message(chatId=chatid,link=link)
        # sub_client.send_message(chatId=botgroup,link=link)

def good_upload(data=None,tipo=None,filename=None):
    if(filename):
        with open(filename,'rb') as h:
            data = h.read()
        tipo = 'imagen/' + filename[filename.rfind('.')+1:]
    if(not data):
        return
    link = None
    for i in range(5):
        try:
            link = client.upload_media(data=data,tipo=tipo)
            break
        except Exception as e:
            print(e)
            print('reintentando upload')
    return link
def send_imagen(chatid,file):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    if(output):
        for i in range(3):
            r = sub_client.send_message(chatId=chatid,filePath=file)
            # r = sub_client.send_message(chatId=botgroup,filePath=file)
            if(r == 200):
                break
def send_sticker(chatid,stickerid):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    if(output):
        r = sub_client.send_message(chatId=chatid,stickerId=stickerid)
        # r = sub_client.send_message(chatId=botgroup,stickerId=stickerid)


def send_gif(chatid,gif):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    if(output):
        sub_client.send_message(chatId=chatid,sendBytesGif=gif)
        # sub_client.send_message(chatId=botgroup,sendBytesGif=gif)

def send_link(chatid,link):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    if(output):
        sub_client.send_message(chatId=chatid,link=link)
        # sub_client.send_message(chatId=botgroup,link=link)

def borrarDeUsuario(chatid,userid):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    send_message(message='Borrando mensajes de ' + getNickname(userid,sub_client), chatId=chatid)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=200)  # Gets messages of each chat
    for uid, content, id in zip(messageList.author.id, messageList.content, messageList.messageId):
        if(verbose):
            print("id: " + uid)
            print("userid " + userid)
        if(uid == userid):
            sub_client.delete_message(chatId=chatid,messageId=id)
    #send_message(message='listo', chatId=chatid)
    
def borrarMedia(chatid):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    send_message(message='Borrando stickers e imagenes', chatId=chatid)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=200)  # Gets messages of each chat
    for id, mediaValue in zip(messageList.messageId,messageList.mediaValue):
        if(verbose):
            print("id %s media %s" % (str(id),str(mediaValue)))
        if(mediaValue != None ):
            sub_client.delete_message(chatId=chatid,messageId=id)
    #send_message(message='listo', chatId=chatid)

def borrarN(chatid,n):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    send_message(message='Borrando ultimos ' + str(n) + ' mensajes', chatId=chatid)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=n)  # Gets messages of each chat

    for id,content in zip(messageList.messageId,messageList.content):
        print("Borrando: " + str(content) )
        sub_client.delete_message(chatId=chatid,messageId=id)
def get_host(chatid,comid):
    chat = get_chat_thread(chatid,comid)
    return chat['uid']

def get_chat_thread(chatid,comid):
    try:
        if(chatid in chatThreads):
            chat = chatThreads[chatid]
        else:
            sub_client = amino.SubClient(profile=client.profile,comId=comid)
            thread = sub_client.get_chat_thread(chatid,raw=True)['thread']
            chatThreads[chatid] = thread
            chat = chatThreads[chatid]
            comidChat[chatid] = comid
        return chat
    except Exception as e:
        print(e)
        PrintException()
def get_cohosts(chatid,comid):
    chat = get_chat_thread(chatid,comid)
    if('coHost' in chat['extensions']):
        return chat['extensions']['coHost']
    else:
        return []

def killUser(chatid,userid):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    send_message(message=getNickname(userid,sub_client) + " fell out of the world", chatId=chatid)

def mostrarJuegos(chatid):
    mensaje = ''
    with open('juegos.txt', 'r') as handler:
        mensaje = handler.read()
    mensaje += '\n\nJuegos actuales: '
    for i in juegos:
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

def ship(chatid,u1,u2,l = 0):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    m = "💖💖💖💖💖💖💖💖💖💖💖💖\n\n"
    m+= getNickname(u1,sub_client) + " 💑 " + getNickname(u2,sub_client) + "\n\n"
    m+= "❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️"
    if(l > 0):
        sub_client.edit_chat(chatId=chatid,announcement=m,pinAnnouncement=True)
    send_message(chatid,m)
    path = 'interaccion/3/ship/'
    ipath = path + 'SFW/'
    lpath = path + 'SFWL/'
    imagenes = os.listdir(ipath)
    img = random.choice(imagenes)
    if(not os.path.exists(lpath + img)):
        link = good_upload(filename=ipath + img)
        if(verbose):
            print(link)
        if(link):
            with open(lpath + img,'w') as h:
                h.write(link)
        else:
            return
    else:
        with open(lpath + img,'r') as h:
            link = h.read()
    with open(path + 'mensajes.txt','r') as h:
        frases =  [line.rstrip().lower() for line in h]

    send_message(chatid,random.choice(frases) % (getNickname(u1,sub_client),getNickname(u2,sub_client)) )
    if(output):
        sub_client.send_message(chatid,link=link)
        # sub_client.send_message(botgroup,link=link)


def buscarLoli(m=''):
    if(m):
        result = requests.get('https://lolibooru.moe/post.json?limit=100&tags=rating%3As+' + quote(m)).text
    else:
        result = requests.get('https://lolibooru.moe/post.json?limit=100&tags=rating%3As').text
    link = None
    if(result):
        result = json.loads(result)
        for i in range(10):
            try:
                r = random.choice(result)
                url = r[booruFileType]
                print(url)
                data = requests.get(url).content
                link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
                print(link)
                break
            except Exception as e:
                print(e)
                print('reintentando')
    return link


def buscarChica(m=''):
    if(m):
        result = requests.get('https://yande.re/post.json?limit=100&tags=rating%3As+' + quote(m)).text
    else:
        result = requests.get('https://yande.re/post.json?limit=100&tags=rating%3As').text
    link = None
    if(result):
        result = json.loads(result)
        for i in range(10):
            try:
                r = random.choice(result)
                url = r[booruFileType]
                print(url)
                data = requests.get(url).content
                link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
                print(link)
                break
            except Exception as e:
                print(e)
                print('reintentando')
    return link
def buscarDanbooru(m=""):
    clientBooru = Danbooru('danbooru')
    result = clientBooru.post_list(limit=100,tags='rating:s ' + m)
    link = None
    if(result):
        for i in range(10):
            try:
                r = random.choice(result)
                url = r['file_url']
                data = requests.get(url).content
                link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
                break
            except Exception as e:
                print(e)
                print('reintentando')
    return link

def buscarMoe():
    clientBooru = Moebooru('konachan')
    result = clientBooru.post_list(limit=100,tags='order:rank rating:s ')
    link = None
    if(result):
        for i in range(10):
            try:
                r = random.choice(result)
                url = r[booruFileType]
                data = requests.get(url).content
                link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
                break
            except Exception as e:
                print(e)
                print('reintentando')
    print(link)
    return link
def buscarMoeTag(tag):
    clientBooru = Moebooru('konachan')
    result = clientBooru.post_list(limit=100,tags='rating:s ' + tag)
    link = None
    if(result):
        for i in range(10):
            try:
                r = random.choice(result)
                url = r[booruFileType]
                data = requests.get(url).content
                link = client.upload_media(data=data,tipo='image/' + url[url.rfind('.')+1:])
                break
            except Exception as e:
                print(e)
                print('reintentando')
    return link


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    traceback.print_exc()
    with open('errores.txt','a') as h:
        h.write('\ntime:{}\nEXCEPTION IN ({}, LINE {} "{}"): {}'.format(time(),filename, lineno, line.strip(), exc_obj))
        traceback.print_exc(file=h)

def bienvenida(chatid,mensaje="",bn=0,mup=0,mdown=0,userid = None,nickname=None):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    if(nickname):
        send_message(message=marcos[mup][0] + '\n\n' + 
        '\n\nBienvenid@ ' + nickname + "\n\n" + mensaje + '\n\n' + marcos[mdown][1], chatId=chatid) 
    elif(not userid):
        if(mensaje == None):
            send_message(message=marcos[mup][0] + '\n\n' +
            bienvenidas[bn] + '\n\n' + marcos[mdown][1], chatId=chatid)
        else:
            send_message(message=marcos[mup][0] + '\n\n' +
            bienvenidas[bn] + 
            '\n\n' + mensaje+ '\n\n' + marcos[mdown][1], chatId=chatid)
    elif(users[userid].bienvenida != ""):
        send_message(message=marcos[mup][0] + 
        '\n\nHola ' + getNickname(userid,sub_client) + "\n\n" + users[userid].bienvenida + '\n\n' + marcos[mdown][1], chatId=chatid)
    else:
        send_message(message=marcos[mup][0] + '\n\n' + 
        '\n\nBienvenid@ ' + getNickname(userid,sub_client) + "\n\n" + mensaje + '\n\n' + marcos[mdown][1], chatId=chatid)

def despedir(chatid,message="",mup=0,mdown=0,userid = None):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    if(userid == None):
        send_message(message=marcos[mup][0] +
        '\n\nAdios ' + message + '\n\n' + marcos[mdown][1], chatId=chatid)

    else:
        send_message(message=marcos[mup][0] +
        '\n\nAdios ' + getNickname(userid,sub_client) + '\n\n' + marcos[mdown][1], chatId=chatid)

def send_message(chatId,message,tm=-1,comid=None):
    if(comid == None):
        sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatId])
    else:
        sub_client = amino.SubClient(profile=client.profile,comId=comid)        

    if(not output):
        return
    prefijo = '[c]'
    if(tm < 0):
        tm = tipoMensaje
    if(tm == 0):
        message = (prefijo + message).replace('\n','\n' + prefijo)
    sub_client.send_message(message=message, chatId=chatId,messageType=tm)
    # sub_client.send_message(message=message, chatId=botgroup,messageType=tm)


def jail(chatid,userid):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    info = sub_client.get_user_info(userId=userid)
    img = requests.get(info.icon).content
    im1 = Image.open(imgdir + 'carcel2_resize.jpg')
    im2 = Image.open(imgdir + 'jail_bars2.png')
    im3 = Image.open(io.BytesIO(img))
    loli = Image.open(imgdir + 'jail_loli.png')
    im1.paste(im3,(150,160))
    final_img = Image.new('RGBA',im1.size,(0,0,0,0))
    final_img.paste(im1,(0,0))
    # final_img.paste(im2,(0,0),mask=im2)
    final_img.paste(loli,(0,0),loli)
    b = io.BytesIO()    
    final_img.save(b,format="png")
    try:
        link = client.upload_media(data=b.getvalue())
        send_link(chatid,link)
    except:
        final_img.save('/tmp/' + chatid + '.png',format="png")
        send_imagen(chatid,'/tmp/' + chatid + '.png')

def patear(chatid,userid):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    info = sub_client.get_user_info(userId=userid)
    img = requests.get(info.icon).content
    patada = Image.open(imgdir + 'patada.gif')
    perfil = Image.open(io.BytesIO(img))
    # perfil = Image.open('imagenes/perfil.jpg')
    perfil = perfil.resize((80,80))
    # perfil2 = perfil.copy()
    frames = []
    positions = [(232,78),(190,100),(236,90),(57,125),(83,125),(1,185)]
    # positions2 = [(232,78),(201,100),(236,90),(57,125),(83,125),(1,185)]
    i = 0
    p = 0
    for frame in ImageSequence.Iterator(patada):
        if(i%2):
            i+=1
            continue
        f = Image.new('RGBA',frame.size,(0,0,0,0))
        f.paste(frame)
        if(p < len(positions) ):
            f.paste(perfil,positions[p])
            p+=1
        i+=1
        b = io.BytesIO()
        f.save(b, format="GIF")
        f = Image.open(b)
        frames.append(f)
    # final_img.show()
    b = io.BytesIO()
    # frames[0].save('/tmp/patear.gif', save_all=True, append_images=frames[1:],loop=0,duration=120)
    # return 'gifs/kiri.gif'
    frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:],loop=0)
    try:
        link = client.upload_media(data=b.getvalue(),tipo='image/gif')
        send_link(chatid,link)
    except Exception as e:
        frames[0].save('/tmp/' + chatid + '.gif',format="GIF", save_all=True, append_images=frames[1:],loop=0)
        send_imagen(chatid,'/tmp/' + chatid + '.gif')

def letra(id):
    html = urllib.request.urlopen('https://www.musica.com/letras.asp?letra=' + id).read().decode('utf-8')
    letra = html2text.html2text(html)
    rLetra = re.compile(r'\[\]\(https://i\.musicaimg\.com/im/a-menos\.svg\)\s(.*)_fuente:',re.DOTALL)
    r4 = re.compile(r'<title>(.*)</title>',re.DOTALL)
    l = rLetra.findall(letra)[0]
    title = r4.findall(html)[0]
    title = title[:title.rfind('|')] + '\n'
    l = title + l
    return l

def buscar(name,chatid):
    global cacheLetras
    text = html2text.html2text(urllib.request.urlopen('https://www.musica.com/letras.asp?t2=' + quote(name)).read().decode('utf-8'))
    r3 = re.compile(r'\(https://www.musica.com/letras.asp\?letra=(\d*)\)\|',re.DOTALL)
    ids = r3.findall(text)
    text = 'Resultados:\n'
    cacheLetras[chatid] = ['0']
    for i in ids:
        letra = urllib.request.urlopen('https://www.musica.com/letras.asp?letra=' + i).read().decode('utf-8')
        r4 = re.compile(r'<title>(.*)</title>',re.DOTALL)
        title = r4.findall(letra)[0]
        title = title[:title.rfind('|')]
        text += title + ' (%s)\n' % (len(cacheLetras[chatid]))
        cacheLetras[chatid].append(i)
    return text

def rip(chatid,userid):
    sub_client = amino.SubClient(profile=client.profile,comId=comidChat[chatid])
    send_message(chatid,'R.I.P ' + getNickname(userid,sub_client))


def jugar(chatid,juego,comid):
    global juegoPid
    if(juego in juegos):
        send_message(chatid,'Iniciando juego %s espere' % (juego) )
        fileName = 'apa.py'
        if(juego == 'aa'):
            fileName = 'jikan_apa.py'
        elif(juego == 'trivia'):
            fileName = 'trivia.py'
        elif(juego == 'vor'):
            fileName = 'vor.py'
        elif(juego == 'retos'):
            fileName = 'retos.py'
        elif(juego == 'mafia'):
            fileName = 'asesino.py'
        if(ssock):
            comando = {"comando":"juego","juego":juego,"filename":fileName,"chatid":chatid,"comid":comid,"mensaje":100,"userid":client.profile.id}
            ssock.send(json.dumps(comando).encode('utf-8'))
        else:
            commands = ["python3",fileName,chatid,juego,"comid=" + str(comid),"mensaje="+str(100),"userid="+str(client.profile.id),"silent"]
            sub = subprocess.Popen(commands)
            del sub
    else:
        send_message(chatid,'No esta el juego ' + juego)
        return
    print('jugando ' + juego)


def getCat():
    link = None
    for i in range(10):
        try:
            text = json.loads(requests.get('https://api.thecatapi.com/v1/images/search').text)
            print(text)
            r = requests.get(text[0]['url'])
            print(r.status_code)
            link = client.upload_media(data=r.content)
            break
        except:
            print('reintentando cargar gato')
    return link
def getGif(m):
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=1" % (m, tenorapikey))
    link = None
    if(r.status_code == 200):
        js = json.loads(r.text)
        media = js['results'][0]['media'][0]
        if(media['gif']['size'] < 1048576):
            r = requests.get(media['gif']['url'])
        else:
            r = requests.get(media['tinygif']['url'])
        for i in range(10):
            try:
                link = client.upload_media(data=r.content,tipo='gif')
                break
            except Exception as e:
                print('reintentando cargar gif')
                print(e)
    return link

def reconectarSQL(s):
    try:
        s.db.reconnect(5)
    except Exception as e:
        print(e)
        print('error reconnectando base de datos :/')
        PrintException()
chatsRevisando = []
ignorar = True

def lanzarBienvenida(chatid,chat,nickname,userid):                    
    if(userid not in users):
        bienvenida(chatid,chat.mensaje,chat.bn,chat.mup,chat.mdown,nickname=nickname)
    else:
        bienvenida(chatid,chat.mensaje,chat.bn,chat.mup,chat.mdown,userid)


def checkChat(chatid,comid,message,host,cohosts,s):
        sub_client = amino.SubClient(comId=comid,profile=client.profile)
        try:
                    id = message['messageId']
                    nickname = message['author']['nickname']
                    content = message['content']
                    createdTime = message['createdTime']
                    extensions = message['extensions']
                    userid = message['uid']
                    tipo = message['type']
                    print(chatid,nickname,content)
                    if(chatid not in chats):
                        try:
                            chat = s.loadChat(chatid)
                            respuestas[chatid] = s.loadRespuestasChat(chatid)
                            opCustom[chatid] = s.loadCustomOPS(chatid)
                        except mysql.connector.errors.DatabaseError as e:
                            reconectarSQL(s)
                                
                        if(chat == None):
                            r = sub_client.get_chat_thread(chatid)
                            print('guardando chat ' + str(r.title) )
                            ops = {}
                            ops['your_uuid'] = 3
                            try:
                                s.chat(chatid,str(r.json['title']),chatid,0,0,0,'',ops,uid=r.json['uid'],comid=r.json['ndcId'] )
                                chat = s.loadChat(chatid)
                            except mysql.connector.errors.DatabaseError as e:
                                PrintException()
                                return
                                
                        chats[chatid] = chat
                    else:
                        chat = chats[chatid]
                    if(chat.uid != host):
                        chat.uid = host

                        try:
                            s.chatUid(host,chatid)
                        except:
                            PrintException()
                            return

                    if(chatid not in opCustom):
                        try:
                            opCustom[chatid] = s.loadCustomOPS(chatid)
                        except Exception as e:
                            PrintException()
                            return
                        

                    if(chatid in funados):
                        if(userid in funados[chatid]):
                            sub_client.delete_message(chatId=chatid,messageId=id)
                    if(userid not in users):
                        print('agregando nuevo usuario ' + nickname)
                        try:
                            users[userid] = User(userid,nickname,s = s)
                            users[userid].save()
                        except:
                            PrintException()
                            return
                    if(content[0] == '*' and content[-1] == '*'):
                        text = getNickname(userid,sub_client) + ' ' + content[1:-1]
                        send_message(chatid,text)
                        return
                    if(content in respuestas[chatid]):                    
                        send_message(chatid,respuestas[chatid][content])

                    if(chatid in traducirDetectarUsers and userid in traducirDetectarUsers[chatid]):
                        c = unicodedata.normalize( 'NFKC', content)
                        c = translator.translate(c,dest='es')
                        if(c != content):
                            send_message(chatid,nickname + ': ' + c.text)
                    if(content.find(" ") == -1):
                        m = None
                    else:
                        m = content[content.find(" "):].lstrip()
                    if(m == ""):
                        m = None
                    allContent = content
                    content = str(content).split(" ")
                    if(userid in cohosts):
                        opLevel = 1
                    elif(userid == host or userid == ley):
                        opLevel = 2
                    else:
                        opLevel = 0
                    usersid = []
                    if('mentionedArray' in extensions):
                        for mi in extensions['mentionedArray']:
                            print('mencion a: ' + mi['uid'])
                            usersid.append(mi['uid'])
                    if('replyMessageId' in extensions):
                        replyid = extensions['replyMessageId']
                        if('replyMessage' in extensions):
                            replyuid = extensions['replyMessage']['uid'] #cuidao con esto
                        else:
                            replyuid = None
                    else:
                        replyid = None
                        replyuid = None
                    if(not usersid and replyuid != None and replyuid != userid):
                        usersid.append(replyuid)
                    if content[0][0] == "/":
                        comando = content[0][1:]
                        comando = unicodedata.normalize( 'NFKC', comando)
                        if(comando in comandos):
                            if(comandos[comando][1] > 0):
                                send_reply(chatid,'comando en mantenimiento disculpen 😔',id)

                                # send_reply(chatid,'Uy no tengo ese comando ¿Porque no intentas iniciar el bot completo con /startbot?',id)
                                # if(os.path.exists('ayuda/comandos/' + comando + '.txt')):
                                #     with open('ayuda/comandos/' + comando + '.txt','r') as h:
                                #         text = h.read()                                
                                #     send_message(chatid,text)
                                # else:
                                #     send_message(chatid,'Todavia no hay ayuda para este comando')
                            elif(comando in opCustom[chatid]):
                                if(opCustom[chatid][comando] > opLevel):
                                    send_message(chatid,'No tienes permisos para utilizar este comando')
                                elif(opCustom[chatid][comando] == -1):
                                    send_message(chatid,'Comando deshabilitado')
                                    return
                            elif(comandos[comando][0] > opLevel):
                                send_message(chatid,'No tienes permisos para utilizar este comando')
                                return
                        else:
                            return
                        if(comando in interaciones1):
                            path = 'interaccion/1/%s/' % (comando)
                            ipath = path + 'SFW/'
                            lpath = path + 'SFWL/'
                            imagenes = os.listdir(ipath)
                            img = random.choice(imagenes)
                            if(not os.path.exists(lpath + img) or time() > os.path.getmtime(lpath + img) + (3600*4) ):
                                link = good_upload(filename=ipath + img)
                                print(link)
                                if(link):
                                    with open(lpath + img,'w') as h:
                                        h.write(link)
                                else:
                                    return
                            else:
                                with open(lpath + img,'r') as h:
                                    link = h.read()
                            with open(path + 'mensajes.txt','r') as h:
                                frases =  [line.rstrip().lower() for line in h]
                            send_message(chatid,random.choice(frases) % (getNickname(userid,sub_client)))
                            sub_client.send_message(chatid,link=link)
                            # sub_client.send_message(botgroup,link=link)

                            # send_media(chatid,filename=path + random.choice(imagenes))
                        elif(comando in interaciones2):
                            if(usersid):
                                for u in usersid:
                                    path = 'interaccion/2/%s/' % (comando)
                                    ipath = path + 'SFW/'
                                    lpath = path + 'SFWL/'
                                    imagenes = os.listdir(ipath)
                                    img = random.choice(imagenes)
                                    if(not os.path.exists(lpath + img)  or time() > os.path.getmtime(lpath + img) + (3600*4)):
                                        link = good_upload(filename=ipath + img)
                                        print(link)
                                        if(link):
                                            with open(lpath + img,'w') as h:
                                                h.write(link)
                                        else:
                                            continue
                                    else:
                                        with open(lpath + img,'r') as h:
                                            link = h.read()
                                    with open(path + 'mensajes.txt','r') as h:
                                        frases =  [line.rstrip().lower() for line in h]

                                    send_message(chatid,random.choice(frases) % (getNickname(userid,sub_client),getNickname(u,sub_client)) )
                                    sub_client.send_message(chatid,link=link)
                                    # sub_client.send_message(botgroup,link=link)
                                    send_media(chatid,filename=path + random.choice(imagenes))
                            else:
                                send_message(chatid,'Debes mencionar a alguien ')
                        elif(comando == "ayuda"):
                            if(len(content) != 2):
                                with open('lite/ayuda.txt','r') as h:
                                    text = h.read()
                                send_message(chatid,text)
                            else:
                                if(os.path.exists('ayuda/comandos/' + content[1] + '.txt')):
                                    with open('ayuda/comandos/' + content[1] + '.txt','r') as h:
                                        text = h.read()                                
                                    send_message(chatid,text)
                                else:
                                    send_message(chatid,'No hay ayuda para el comando ' + content[1])

                        elif(comando == "marcos"):
                            r = sub_client.start_chat([userid],message='hola')
                            if(r[0] == 200):
                                userchat = r[1]['thread']['threadId']
                                mostrarMarcos(userchat,comid)
                                send_message(chatid,'%s revisa tu privado para ver los marcos' % (getNickname(userid,sub_client)))
                            else:
                                send_message(chatid,'Los marcos se envian al privado porque son muchos, por favor escribele al bot para poder enviarte los marcos')
                        elif(comando == "mensaje"):
                            if(m == None):
                                send_message(chatid,'uso: /mensaje [mensaje]: Pone un mensaje de bievenida para el chat')
                                chat.mensaje = ""
                            else:
                                chat.mensaje = m
                            try:
                                chat.save()
                            except:
                                send_message(chatid,'error guardando')


                        elif(comando == "op"):
                            send_message(chatid,'tienes op %d' % (opLevel))
                        elif(comando == "alias"):
                            if(len(usersid) == 1 ):
                                if(usersid[0] not in users):
                                    users[usersid[0]] = User(usersid[0],getNickname(usersid[0]),sub_client)
                                if(replyuid != usersid[0]):
                                    m = m[m.find('@') + len(users[usersid[0]].nickname)+1:].lstrip()
                                print("alias " + m)
                                users[usersid[0]].alias = m
                                try:
                                    users[usersid[0]].save()
                                except:
                                    send_message(chatid,'error guardando')
                            else:
                                send_message(chatid,'uso: /alias @user [alias]: le pone un alias a un usuario')

                        elif(comando == "recibir"):
                            if(usersid):
                                for u in usersid:
                                    bienvenida(chatid,"",chat.bn,chat.mup,chat.mdown,u)
                            else:
                                bienvenida(chatid,chat.mensaje,chat.bn,chat.mup,chat.mdown)
                        elif(comando == "despedir"):
                            if(usersid ):
                                for u in usersid:
                                    despedir(chatid,'',chat.mup,chat.mdown,u)
                            else:
                                despedir(chatid,"se les quiere",chat.mup,chat.mdown)

                        elif(comando == "kill"):
                            if(usersid):
                                for u in usersid:
                                    killUser(chatid,u)
                            else:
                                send_message(chatid,'uso: /kill @: envia un mensaje de muerte para los usuarios con @')

                        elif(comando == "marco"):
                            if(len(content) == 2):
                                mn = int(content[1])
                                if(mn < len(marcos)   and mn >= 0):
                                    chat.mup = mn
                                    chat.mdown = mn
                                    try:
                                        chat.save()
                                    except:
                                        print('Error guardando')
                                else:
                                    send_message(chatid,'Solo puedes usar los marcos del 0 al %d' % (len(marcos-1) ) )
                            elif(len(content) == 3):
                                mn = int(content[1])
                                mn2 = int(content[1])
                                if(mn < len(marcos) and mn >= 0 and mn2 < len(marcos) and mn2 >= 0):
                                    chat.mup = mn
                                    chat.mdown = mn2
                                    try:
                                        chat.save()
                                    except:
                                        send_message(chatid,'error guardando')
                                else:
                                    send_message(chatid,'Solo puedes usar los marcos del 0 al %d' % (len(marcos-1) ) )

                            else:
                                send_message(chatid,'uso: /marco [n]: pone un marco para los mensajes del chat')
                        elif(comando == "borrarU"): 
                            if(usersid):
                                for u in usersid:
                                    borrarDeUsuario(chatid,u)
                            else:
                                send_message(chatid,'Tienes que mencionar uno o varios usuarios con @')
                        elif(comando == "borrarM"):
                            borrarMedia(chatid)
                        elif(comando == "borrarN"):
                            if(len(content) < 2 or not content[1].isdigit()):
                                send_message(chatid,'uso: /borrarN [n]: borra n mensajes del chat')
                            else:
                                borrarN(chatid,int(content[1]))
                        elif(comando == "borrar"):
                            if(replyid):
                                sub_client.delete_message(chatId=chatid,messageId=replyid)
                            else:
                                send_message(chatid,'Tienes que mencionar el mensaje que quieres borrar')
                        elif(comando == "kick"):
                            for u in usersid:
                                if(u == host):
                                    send_message(chatid,'no puedes sacar al anfi')
                                elif(u in cohosts):
                                    send_message(chatid,'no puedes sacar a un co anfi')
                                elif(u == 'your_uuid'):
                                    send_message(chatid,'no puedes a ley, ley esta rotisimo')
                                else:
                                    sub_client.kick(u,chatid,True)

                        elif(comando == "ban"):
                            for u in usersid:
                                if(u == host):
                                    send_message(chatid,'no puedes sacar al anfi')
                                elif(u in cohosts):
                                    send_message(chatid,'no puedes sacar a un co anfi')
                                elif(u == ley):
                                    send_message(chatid,'no puedes a ley, ley esta rotisimo')
                                else:
                                    sub_client.kick(u,chatid,False  )
                        elif(comando == "juegos"):
                            mostrarJuegos(chatid)
                        elif(comando == "jugar"):
                            if(len(content) < 2):
                                send_message(chatid,'uso: /jugar [juego]: pone un juego')
                                mostrarJuegos(chatid)
                            else:
                                jugar(chatid,content[1],comid)

                        elif(comando == "ship"):
                            if(len(usersid) != 2):
                                send_message(chatid,'Tienes que mencionar 2 usuarios')
                            else:
                                if(content[1].isdigit()):
                                    ship(chatid,usersid[0],usersid[1],int(content[1]))
                                else:
                                    ship(chatid,usersid[0],usersid[1])
                        elif(comando == "tp"):
                            if(m != None):
                                r = client.get_from_code(m)
                                if(r.objectType == 12):
                                    com = str(r.json['extensions']['linkInfo']['ndcId'])
                                    if(userid == ley or userid ==  get_host(r.objectId,com)):
                                        if(com != sub_client.comId):
                                            send_message(chatid,'Advertencia link de otra comunidad, enviando el bot a esa comunidad')

                                        client.join_community(com)
                                        comid = sub_client.comId
                                        sub_client.comId = com
                                        sub_client.join_chat(r.objectId)
                                        sub_client.comId = comid
                                        send_message(r.objectId,'¡Hola!\nSoy un bot y me han tepeado a este chat (solo el anfitrion deberia poder tepearme), para ayuda del bot /ayuda ')

                                        send_message(botgroup,'tp de ' + nickname + '\nA: ' + str(get_title(r.objectId,com)) )
                                    else:
                                        send_message(chatid,'Solo ley o el anfi del chat destino puede meter al bot en el chat destino')
                            else:
                                send_message(chatid,'uso: /tp [link del chat]: envia el bot a otro chat')
                        elif(comando == "random"):
                            if(len(content) == 2):
                                send_message(chatid,str(random.randint(1,int(content[1]))))
                            elif(len(content) == 3):
                                send_message(chatid,str(random.randint(int(content[1]),int(content[2]))))
                            else:
                                send_message(chatid,'uso: /random [n1] [n2]: genera un numero random entre n1 y n2')
                        elif(comando == "disponible"):
                            t = "Comandos disponibles segun tu nivel de permisos:\n"
                            for c in comandos:
                                if(comandos[c][1] > 0):
                                    continue
                                if(comandos[c][0] <= opLevel):
                                    t += c + '\n'
                            send_message(chatid,t)
                        elif(comando == "revivir"):
                            send_message(chatid,'invocando a la gente')
                            for i in range(5):
                                send_invocacion(chatid,cohosts + [host],'revivan gente')
                        elif(comando == "traducir"):
                            if(replyid or usersid):
                                if(replyid):
                                    message = sub_client.get_message_info(chatid,replyid)
                                    replyContent = message.json['content']
                                    if(content != None):
                                        replyContent = unicodedata.normalize( 'NFKC', replyContent)
                                        if(len(content) == 2 ):
                                            if(content[1] == 'ingles'):
                                                traduccion = translator.translate(replyContent,src='en',dest='es')
                                                send_message(chatid,traduccion.text)
                                            elif(content[1] == 'detectar'):
                                                traduccion = translator.translate(replyContent,dest='es')
                                                send_message(chatid,traduccion.text)
                                            elif(content[1] == 'nombre'):
                                                nom = sub_client.get_user_info(message.json['uid']).nickname
                                                
                                                send_message(chatid,unicodedata.normalize( 'NFKC', nom))
                                        else:
                                            send_message(chatid,replyContent)
                                elif(usersid):
                                    if(len(content) >= 2 ):
                                        if(content[1] == 'nombre'):
                                            for u in usersid:
                                                nom = sub_client.get_user_info(message.json['uid']).nickname
                                                send_message(chatid,unicodedata.normalize( 'NFKC', nom))
                                        else:
                                            if(chatid not in traducirDetectarUsers):
                                                traducirDetectarUsers[chatid] = []
                                            traducirDetectarUsers[chatid] += usersid
                                            print('traduciendo',traducirDetectarUsers[chatid])

                            else:
                                text = 'uso: /traducir [ingles|detectar|nombre] : traduce algo de algun idioma a tipo de letra extraño a letras normales\n'
                                text += '/traducir detectar @user: va a traducir al español todos los mensajes que @user envie\n'
                                text += '/traducir @user: va a traducir a una letra normal todos los mensajes que @user envie\n'
                                text += 'Para dejar de traducir a alguien /notraducir'
                                send_message(chatid,text)
                        elif(comando == "notraducir"):
                            traducirDetectarUsers[chatid] = []
                            send_message(chatid,'Deteniendo traducir')
                        elif(comando == "buscar"):
                            con = allContent.split('\n')
                            for i in range(5):
                                try:
                                    if(len(content) <= 1):
                                        send_message(chatid,'error, no hay nada que buscar')
                                        break
                                    elif(content[1][:5] == 'anime'):
                                        text = 'Resultados: \n'
                                        search_result = jikan.search('anime', m[5:].lstrip(), page=1)
                                        for result in search_result['results'][:10]:
                                            text += result['title'] + ' (%d)\n' % (result['mal_id'])
                                        send_message(chatid,text.replace('\n','\n\n'))
                                    elif(content[1][:5] == 'manga'): 
                                        text = 'Resultados: \n'
                                        search_result = jikan.search('manga', m[5:].lstrip(), page=1)
                                        for result in search_result['results'][:10]:
                                            text += result['title'] + ' (%d)\n' % (result['mal_id'])
                                        send_message(chatid,text.replace('\n','\n\n'))
                                    elif(content[1][:9] == 'personaje' or content[1][:9] == 'character'):
                                        text = 'Resultados: \n'
                                        print(m)
                                        print(m[9:].lstrip())
                                        search_result = jikan.search('character', m[9:].lstrip(), page=1)
                                        for result in search_result['results'][:10]:
                                            text += 'nombre: ' +result['name'] + ' (%d)\n\n' % (result['mal_id'])
                                            if(len(result['anime']) > 0):
                                                text += 'anime: ' + result['anime'][0]['name'] + '\n'
                                            if(len(result['manga']) > 0):
                                                text += 'manga: ' + result['manga'][0]['name'] + '\n'
                                            text += '\n'
                                        send_message(chatid,text)
                                    else:
                                        text = 'Resultados: \n'
                                        search_result = jikan.search('anime', m, page=1)
                                        for result in search_result['results'][:10]:
                                            text += result['title'] + ' (%d)\n' % (result['mal_id']) 
                                        send_message(chatid,text.replace('\n','\n\n'))
                                except jikanpy.exceptions.APIException as e:
                                    PrintException()
                                    pass
                                else:
                                    break           

                        elif(comando == "anime"):
                            jikanError = True
                            text = ''
                            for i in range(5):
                                try:
                                    if(m.isdigit()):
                                        result = jikan.anime(int(m))
                                    elif(m):
                                        text = 'Resultados: \n'
                                        search_result = jikan.search('anime', m[5:].lstrip(), page=1)
                                        r = search_result['results'][0]
                                        # print(result)
                                        for result in search_result['results'][:10]:
                                            text += result['title'] + ' (%d)\n' % (result['mal_id'])
                                        result = r
                                        send_message(chatid,text.replace('\n','\n\n'))
                                        text = ''

                                except jikanpy.exceptions.APIException as e:
                                    PrintException()
                                else:
                                    text += 'Nombre: ' + result['title'] + '\n'
                                    text += 'Descripcion: ' + translator.translate(result['synopsis'],src='en',dest='es').text + '\n'
                                    text += 'Episodios: ' + str(result['episodes']) + '\n'
                                    if('aired' in result):
                                        text += 'Empezo el: ' + result['aired']['from'].split('T')[0] + '\n'
                                        if(result['aired']['to']!= None):
                                            text += 'Termino el: ' + result['aired']['to'].split('T')[0] + '\n'
                                    img_data = requests.get(result['image_url']).content
                                    mediaValue = client.upload_media(data=img_data)
                                    send_message(chatid,text.replace('\n','\n\n'))
                                    send_link(chatid,link=mediaValue)
                                    jikanError = False
                                    break
                            if(jikanError):
                                send_message(chatid,'Error buscando el anime')

                        elif(comando == "temporada"):
                            if(len(content) < 2):
                                text = 'uso: /temporada [año] [temporada]:\naño: [1962-2020]\ntemporada: '
                                text += '[invierno|primavera|verano|otoño]\n'
                                text += 'ejemplo: /temporada 2020 invierno'
                                send_message(chatid,text)
                            else:
                                if(content[1].isdigit() and content[2] in temporadas):
                                    jikanError = True
                                    for i in range(5):
                                        try:
                                            temp = jikan.season(year=int(content[1]),season=temporadas[content[2]] )
                                        except jikanpy.exceptions.APIException as e:
                                            PrintException()
                                            print('error en jikan, intentando de nuevo')
                                            sleep(1)
                                        else:
                                            text = 'Animes:\n'
                                            for a in temp['anime']:
                                                text += a['title'] + ' (%d)\n\n' % (a['mal_id'])
                                            send_message(chatid,text)
                                            jikanError = False
                                            break
                                    if(jikanError):
                                        send_message(chatid,'Error buscando la temporada')
                        elif(comando == "emision"):
                            if(len(content) != 2):
                                text = 'uso: /emision [dia] :\ndia: [lunes|martes|miercoles|jueves|viernes|sabado|domingo]\n'
                                text += 'ejemplo: /emision lunes'
                                send_message(chatid,text)
                            else:
                                if( content[1] in dias):
                                    jikanError = True
                                    for i in range(5):
                                        try:
                                            day = dias[content[1]]
                                            temp = jikan.schedule(day=day)
                                            # temp = jikan.season(year=int(content[1]),season=temporadas[content[2]] )
                                        except jikanpy.exceptions.APIException as e:
                                            PrintException()
                                            print('error en jikan, intentando de nuevo')
                                            sleep(1)
                                        else:
                                            text = 'Animes:\n'
                                            for a in temp[day]:
                                                text += a['title'] + ' (%d)\n\n' % (a['mal_id'])
                                            send_message(chatid,text)
                                            jikanError = False
                                            break
                                    if(jikanError):
                                        send_message(chatid,'Error buscando la temporada')


                        elif(comando == "openings"):
                            if(len(content) >= 2 ):
                                jikanError = True
                                for i in range(5):
                                    try:
                                        if(m.isdigit()):
                                            result = jikan.anime(int(m))
                                        else:
                                            search_result = jikan.search('anime',m, page=1)
                                            result = search_result['results'][0]
                                            result = jikan.anime(result['mal_id'])

                                        text = 'Openings: '+ result['title'] +'\n\n'
                                    except jikanpy.exceptions.APIException as e:
                                        PrintException()
                                        sleep(1)
                                    else:
                                        text += '\n\n'.join(result['opening_themes'])
                                        img_data = requests.get(result['image_url']).content
                                        mediaValue = client.upload_media(data=img_data)
                                        send_link(chatid,link=mediaValue)
                                        send_message(chatid,text.replace('\n','\n\n'))
                                        jikanError = False
                                        break
                                if(jikanError):
                                    send_message(chatid,'Error buscando')
                            else:
                                send_message(chatid,'uso: /opening id: los openings del anime id')
                        elif(comando == "ending"):
                            if(len(content) >= 2 ):
                                jikanError = True
                                text = 'Endings: '+ result['title'] +'\n\n'
                                for i in range(5):
                                    try:
                                        if(m.isdigit()):
                                            result = jikan.anime(int(m))
                                        else:
                                            search_result = jikan.search('anime',m, page=1)
                                            result = search_result['results'][0]
                                            result = jikan.anime(result['mal_id'])
                                    except jikanpy.exceptions.APIException as e:
                                        PrintException()
                                        sleep(1)
                                    else:
                                        text += '\n\n'.join(result['ending_themes'])
                                        img_data = requests.get(result['image_url']).content
                                        mediaValue = client.upload_media(data=img_data)
                                        send_link(chatid,link=mediaValue)
                                        send_message(chatid,text)
                                        jikanError = False
                                        break
                                if(jikanError):
                                    send_message(chatid,'Error id no encontrado')

                            else:
                                send_message(chatid,'uso: /ending id: los openings del anime id')
                        elif(comando == "manga"):
                            if(len(content) >= 2 ):
                                jikanError = True
                                text = ''
                                for i in range(5):
                                    try:
                                        if(m.isdigit()):
                                            result = jikan.manga(int(m))
                                        elif(m):
                                            text = 'Resultados: \n'
                                            search_result = jikan.search('manga', m.lstrip(), page=1)
                                            r = search_result['results'][0]
                                            print(r)
                                            for result in search_result['results'][:10]:
                                                text += result['title'] + ' (%d)\n' % (result['mal_id'])
                                            result = r
                                            send_message(chatid,text.replace('\n','\n\n'))
                                            text = ''

                                    except jikanpy.exceptions.APIException as e:
                                        PrintException()
                                        sleep(1)
                                    else:
                                        text += 'Nombre: ' + result['title'] + '\n\n'
                                        text += 'Descripcion: ' + translator.translate(result['synopsis'],src='en',dest='es').text + '\n'
                                        if(result['chapters'] != None):
                                            text += 'Capitulos: ' + str(result['chapters']) + '\n\n'
                                        if('published' in result):
                                            text += 'Empezo el: ' + result['published']['from'].split('T')[0] + '\n\n'
                                            if(result['published']['to']!= None):
                                                text += 'Termino el: ' + result['published']['to'].split('T')[0] + '\n\n'
                                        img_data = requests.get(result['image_url']).content
                                        mediaValue = client.upload_media(data=img_data)
                                        send_message(chatid,text)
                                        send_link(chatid,link=mediaValue)
                                        jikanError = False
                                        break
                                if(jikanError):
                                    send_message(chatid,'Error id no encontrado')
                            else:
                                send_message(chatid,'uso: /manga id: da informacion de el manga con ese id (resultado de la busqueda)')

                        elif(comando == "personaje"):
                            if(len(content) >= 2 ):
                                jikanError = True
                                text = ''
                                for i in range(5):
                                    try:
                                        if(m.isdigit()):
                                            result = jikan.character(int(m))
                                        elif(m):
                                            text = 'Resultados: \n'
                                            search_result = jikan.search('character', m, page=1)
                                            r = search_result['results'][0]
                                            print(r)
                                            for result in search_result['results'][:10]:
                                                text += 'nombre: ' +result['name'] + ' (%d)\n\n' % (result['mal_id'])
                                                if(len(result['anime']) > 0):
                                                    text += 'anime: ' + result['anime'][0]['name'] + '\n'
                                                if(len(result['manga']) > 0):
                                                    text += 'manga: ' + result['manga'][0]['name'] + '\n'
                                                text += '\n'
                                            result = jikan.character(r['mal_id'])
                                            send_message(chatid,text.replace('\n','\n\n'))
                                            text = ''

                                    except jikanpy.exceptions.APIException as e:
                                        PrintException()
                                        sleep(1)
                                    else:
                                        text += 'Nombre: ' + result['name'] + '\n\n'
                                        text += 'Descripcion: ' + translator.translate(result['about'],src='en',dest='es').text + '\n\n'
                                        img_data = requests.get(result['image_url']).content
                                        mediaValue = client.upload_media(data=img_data)
                                        send_message(chatid,text.replace('\\ n','').replace('\\',''))
                                        send_link(chatid,link=mediaValue)
                                        jikanError = False
                                        break
                                if(jikanError): 
                                    send_message(chatid,'Error id no encontrado')
                            else:
                                send_message(chatid,'uso: /personaje id: da informacion de el personaje con ese id (resultado de la busqueda)')
                        elif(comando == "lyrics"):
                            try:
                                lyric = animelyrics.search_lyrics(m, show_title=True)
                                send_message(chatid,lyric)
                            except animelyrics.MissingTranslatedLyrics as e:
                                send_message(chatid,'eto no pude encontrar el anime')
                            except animelyrics.NoLyricsFound:
                                send_message(chatid,'eto... no pude encontrar la lyrica')

                        elif(comando == 'comandos'):
                            cpro = []
                            c0 = []
                            c1 = []
                            c2 = []
                            for c in comandos:
                                if(comandos[c][1] > 0):
                                    cpro.append(c)
                                else:
                                    if(comandos[c][0] == 0):
                                        c0.append(c)
                                    elif(comandos[c][0] == 1):
                                        c1.append(c)
                                    elif(comandos[c][0] == 2):
                                        c2.append(c)
                            # text = '[b]Comandos lite:\n\n'
                            text = ''
                            text += 'Comandos para todos: '
                            for c in c0:
                                text += ' %s ' % (c)
                            text += '\n\nComandos de coa: '
                            for c in c1:
                                text += ' %s ' % (c)
                            text += '\n\nComandos de anfi: '
                            for c in c2:
                                text += ' %s ' % (c)

                            # text += '\n\n[b]Comandos de la version completa:\n\n'
                            # for c in cpro:
                            #     text += ' %s ' % (c)
                            send_message(chatid,text)
                        elif(comando == "hora"):
                            tnow = pytz.timezone('UTC').localize(datetime.datetime.utcnow())
                            text = 'Hora: \n'
                            if(len(content) == 2 and content[1] == 'todas'):
                                for tz in pytz.common_timezones:
                                    if('America' in tz):
                                        text += tz[tz.rfind('/')+1:] +': ' + tnow.astimezone(pytz.timezone(tz) ).strftime("%I:%M %p") + '\n'
                            else:
                                for tz in tzs:
                                    text += tz[tz.rfind('/')+1:] +': ' + tnow.astimezone(pytz.timezone(tz) ).strftime("%I:%M %p") + '\n'
                                text += 'Para todas /hora todas'
                            send_message(chatid,text)
                        elif(comando == "le"):
                                text = getNickname(userid,sub_client) + ' ' 
                                if(replyuid):
                                    u = replyuid
                                    text += allContent[1:] + ' a ' + getNickname(u,sub_client)
                                elif(len(usersid) == 1 ):
                                    u = usersid[0]
                                    text += allContent[1:]
                                    text = text[:text.rfind('@')]
                                    text += ' a ' + getNickname(u,sub_client)
                                send_message(chatid,text)

                        elif(comando == "se"):
                            text = getNickname(userid,sub_client) + ' ' + allContent[1:]
                            send_message(chatid,text)
                        elif(comando == "rip"):
                            if(usersid):
                                for u in usersid:
                                    rip(chatid,u)
                            else:
                                send_message(chatid,'uso: /rip @: envia un rip a los usuarios mencionados')
                        elif(comando == "carcel"):
                            if(usersid):
                                for u in usersid:
                                    jail(chatid,u)
                            else:                           
                                send_message(chatid,'uso: /carcel @: mete a los usuarios mencionados a la carcel')
                        elif(comando == "patear"):
                            if(usersid):
                                for u in usersid:
                                    patear(chatid,u)
                            else:                           
                                send_message(chatid,'uso: /patear @: patea a los usuarios mencionados')
                        elif(comando == "debug"):
                            if(len(content) < 2):
                                send_message(chatid,'uso: /debug [on|off]: muestra los errores del bot en el chat')
                            elif(content[1] == 'on'):
                                debug[chatid] = True
                            elif(content[1] == 'off'):
                                debug[chatid] = False
                        elif(comando == "letra"):
                            if(chatid not in cacheLetras):
                                cacheLetras[chatid] = ['0']
                            if(len(content) == 2 and content[1].isdigit()):
                                if(len(cacheLetras[chatid]) ==1 ):
                                    send_message(chatid,'Primero tienes que buscar la cancion por nombre')
                                else:
                                    l = letra(cacheLetras[chatid][int(content[1])] )
                                    send_message(chatid,l)
                            elif(len(content) == 1):
                                send_message(chatid,'Uso:letra [id|nombre]\n\nEl id es el numero entre parentesis que aparece despues del resultado de la busqueda')
                            else:

                                r = buscar(m,chatid)
                                send_message(chatid,r)
                        elif(comando == "anuncio"):
                            if(m != None):
                                sub_client.edit_chat(chatId=chatid,announcement=m,pinAnnouncement=True)
                                sub_client.delete_message(chatId=chatid,messageId=id)
                            else:
                                send_message(chatid,'uso: /anuncio [anuncio]: cambia el anuncio del chat')

                        elif(comando == "placa"):
                            if(not m):
                                if(chat.placa):
                                    send_message(chatid,'Placa actual del chat: ' + str(chat.placa) )
                                else:
                                    send_message(chatid,'uso: /placa [placa del chat]\n Guarda la placa del chat')
                            else:
                                chat.placa = m
                                try:
                                    chat.save()
                                except:
                                    send_message(chatid,'Error guardando')
                                else:
                                    send_message(chatid,'Placa del chat actualizada: ' + m)
                                    send_message(botgroup,'El chat ' + get_title(chatid,comid) + '\nActualizo su placa: ' + m,0)
                        elif(comando == "tiempo" or comando == 'uptime'):
                            t = time() - startbotTime
                            text = "Tiempo activo del bot: %d:%d\n" % (t/60,t%60)
                            send_message(chatid,text)
                        elif(comando == "seguro"):
                            if(len(content) == 2 and content[1].isdigit):
                                send_message(chatid,'La opcion de poner el modo visualizacion durante un tiempo es de la version pro')
                                # tvisualizacion = time()
                                # tliberar = int(content[1])*60
                                # sub_client.edit_chat(chatid,viewOnly=True)
                            else:
                                tliberar = 0
                                tvisualizacion = time()                         
                                sub_client.edit_chat(chatid,viewOnly=True)
                        elif(comando == "liberar"):
                            sub_client.edit_chat(chatid,viewOnly=False)
                            tliberar = 0
                            tvisualizacion = 0
                        elif(comando == "bug"):
                            if(m == None):
                                send_message(chatid,'uso: /bug [mensaje de bug]: sirve para informar de algun bug (error) que tuvo el bot ')
                            else:
                                chatname = get_title(chatid,comid)
                                text = 'Bug reportado en el chat ' + chatname + '\n'
                                text += 'Por: '+ nickname + '\n'
                                text += m
                                send_message(botgroup,text)
                                send_message(chatid,'Bug reportado')
                        elif(comando == "sugerencia"):
                            if(m == None):
                                send_message(chatid,'uso: /sugerencia [mensaje]: Sirve para enviar sugerencias de cosas que te gustarian cambiar, quitar o cambiar al bot.\nComo por ejemplo mas lolis')
                            else:
                                chatname = get_title(chatid,comid)
                                text = 'Sugerencia en el chat ' + chatname + '\n'
                                text += 'Por: '+ nickname + '\n'
                                text += m
                                send_message(botgroup,text)
                                send_message(chatid,'Gracias por tu sugerencia')
                        elif(comando == "opinion"):
                            if(m == None):
                                send_message(chatid,'uso: /opinion [tu openion del bot]: Sirve para dar una opinion sobre el bot')
                            else:
                                chatname = get_title(chatid,comid)
                                text = 'opinion en el chat ' + chatname + '\n'
                                text += 'Por: '+ nickname + '\n'
                                text += m
                                send_message(botgroup,text)
                                send_message(chatid,'Gracias por tu opinion')
                        elif(comando == "loli"):
                            link = buscarLoli(m)
                            if(link):
                                send_message(chatid,'Aqui esta, cuidala bien')
                                send_link(chatid,link)
                            else:
                                send_message(chatid,'Solo los mas puros de corazon pueden ver esta imagen')
                                send_link(chatid,'http://st1.narvii.com/7680/d0b72bcf6e50745f0256acaf27770b2b8d70b763r5-184-180_00.jpeg')
                        elif(comando == "trapito"):
                            trapitos = os.listdir('trapitos')
                            print('trapitos/' + random.choice(trapitos))
                            send_imagen(chatid,'trapitos/' + random.choice(trapitos))
                        elif(comando == "decir"):
                            if(m):
                                if(len(m) > 50):
                                    send_message(chatid,'No se pueden decir textos de mas de 50 letras')
                                else:
                                    for i in range(3):
                                        try:
                                            tts = gTTS(text=m,lang='es',slow=False)
                                            break
                                        except:
                                            print('error obteniendo audio reintentando')
                                        else:
                                            break
                                    else:
                                        send_reply(chatid,'no pude decir esto lo siento',id)
                                        return
                                    path = '/tmp/' + str(time()).replace('.','') + '.mp3'
                                    tts.save(path)
                                    send_imagen(chatid,path)
                            else:
                                send_message(chatid,'uso: /decir [texto]: envia una nota de voz diciendo el texto')
                        elif(comando == 'entrar'):
                            if(len(content) > 1):

                                if(content[1] == 'en'):
                                    send_message(chatid,getNickname(userid,sub_client) + ' a entrado ' + ' '.join(content[1:]))
                                elif(content[1] in ['a','al']):
                                    send_message(chatid,getNickname(userid,sub_client) + ' se a unido ' + ' '.join(content[1:]))
                                else:
                                    send_message(chatid,getNickname(userid,sub_client) + ' a entrado ' + ' '.join(content[1:]))

                        elif(comando == 'dejar'):
                            if(len(content) > 1):
                                send_message(chatid,getNickname(userid,sub_client) + ' ha dejado ' + ' '.join(content[1:]))
                        elif(comando == 'miau'):
                            send_link(chatid,getCat())
                        elif(comando == "coas"):
                            text = 'Coas:\n'
                            for c in cohosts:
                                text += '%s\n' % (getNickname(c,sub_client))
                            send_message(chatid,text)
                        elif(comando == "funar"):
                            if(chatid not in funados):
                                funados[chatid] = []
                            if(usersid):
                                for u in usersid:
                                    funados[chatid].append(u)
                            else:
                                send_message(chatid,'uso: /funar @: borra todos los mensajes que envien los usuarios mencionados')
                        elif(comando == "perdonar"):
                            if(chatid not in funados):
                                return
                            if(usersid):
                                funados[chatid] = [item for item in funados[chatid] if item not in usersid]
                            else:
                                send_message(chatid,'uso: /perdonar @: perdona la funa de los usuarios mencionados')
                        elif(comando == "apagar"):
                            send_message(chatid,'bye')
                            sub_client.leave_chat(chatid)
                        elif(comando == 'startbot'):
                            send_message(chatid,'comando en mantenimiento disculpen 😔')
                            return
                            content = message['content'].split(' ')
                            if(len(content) > 1 ):
                                r = checkStartBot(chatid,userid,comid,id,s,' '.join(content[1:]) )
                            else:
                                r = checkStartBot(chatid,userid,comid,id,s )
                            if(r == 1):
                                s.botstate(4,0,comid,0,chatid)
                                send_message(chatid,'apagando bot lite')

                        elif(comando == "gif"):
                            if(m):
                                send_link(chatid,getGif(m))
                            else:
                                send_message(chatid,'uso: /gif [busqueda]\nEjemplo: /gif anime (busca gif de anime)')
                        elif(comando == "nuevo"):
                            with open('nuevo.txt','r') as h:
                                text = h.read()
                            send_message(chatid,text)
                        elif(comando == "moe"):
                            if(m):
                                link = buscarMoeTag(m)
                            else:
                                link = buscarMoe()
                            if(link):
                                send_link(chatid,link)
                        elif(comando == "danbooru"):
                            if(m):
                                link = buscarDanbooru(" " + m)
                            else:
                                link = buscarDanbooru()
                            if(link):
                                send_link(chatid,link)
                        elif(comando == "chica"):
                            link = buscarChica(m)
                            if(link):
                                send_link(chatid,link)

                        elif(comando == "ver"):
                            for u in usersid:
                                r = sub_client.get_user_info(u)
                                js = r.json
                                send_link(chatid,js['icon'])
                                text = 'Informacion de usuario:\n\n'
                                text += 'Nombre: %s\n' % (js['nickname'])
                                if(u in users):
                                    text += 'Alias: %s\n' % (users[u].alias)
                                text += 'Seguidores: %s\n' % (js['membersCount'])
                                text += 'Siguiendo: %s\n' % (js['joinedCount'])
                                text += 'Nivel: %s\n' % (js['level'])
                                text += 'Reputacion: %s\n' % (js['reputation'])
                                try:
                                    userTags = s.loadUserTags(u)
                                except:
                                    reconectarSQL(s)

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
                                        if(chat.tags[u][t] != None):
                                            texttag += t + ':' + chat.tags[u][t] + '\n'
                                        else:
                                            texttag += t + '\n'
                                        tagCount += 1
                                if(tagCount):
                                    text += texttag

                                send_message(chatid,text)
                        elif(comando == 'sigueme'):
                            sub_client.follow(userid)
                            send_reply(chatid,'Vale te sigo ^^',id)


        except Exception as e:
            PrintException()
            print(e)


#load zone
with open('marcos.txt', 'r') as handler:
    buf = [line.rstrip() for line in handler]
    marcos = []
    for i in range(0,len(buf),2):
        marcos.append((buf[i],buf[i+1]))

juegos = os.listdir('juegos')
juegos.remove('__pycache__')
juegos.remove('asesino')
juegos.remove('retos')
juegos.append('mafia')
juegos.sort()
comandos = {}
funados = {}
comandosPremium = {}
with open('lite/comandos.txt', 'r') as h:
    handler = h.read().split('\n')
    for line in handler:
        cl = line.split(' ')
        if(cl[2] == '0'):
            comandos[cl[0]] = (int(cl[1]),0)
        elif(cl[2] == '1'):
            comandos[cl[0]] = (int(cl[1]),1)
            comandosPremium[cl[0]] = int(cl[1])
for c in interaciones1:
    comandos[c] = (0,0)    
for c in interaciones2:
    comandos[c] = (0,0)    
users = {}
bienvenidas = []


#set variables
ley = 'your_uuid'
botgroup = '17ab60ec-0418-4c75-8ce3-fdb11613b201'
traducirDetectarUsers = {}
debug = {}
cacheLetras = {}
mensajesChats = {}
marcosChats = {}
chatThreads = {}
skipChats = []
tzs = ('America/Caracas','America/Buenos_Aires',
'America/Bogota','America/Mexico_City','America/Lima',
'America/Tijuana','America/Santiago','Europe/Madrid')
temporadas = {'invierno':'winter','primavera':'spring','verano':'summer','otoño':'fall'}
dias = {'lunes':'monday','martes':'tuesday','miercoles':'wednesday','thursday':'jueves','viernes':'friday','sabado':'saturday','domingo':'sunday'}
tenorapikey = "23TJ3291LB82"
booruFileType = 'sample_url'
oldMessagesLock = threading.Lock()
#no se

jikan = Jikan()
translator = Translator()
startbotTime = time()
chats = {}
opCustom = {}
comidChat = {}
respuestas = {}
threads = {}
lastActivity = {}
# chatCoHosts = {}
# chatHost = {}
# chatTypes = {}
updatedComunityStates = {}
sock = None
ssock = None

t = json.loads(requests.get('https://service.narvii.com/api/').content)['api:timestamp']
startTimeStamp = datetime.datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ')
print('iniciado')
def sendStart(chatid,comid,premium,userBot='4882156e-efce-4a4b-88ca-02baff4d5e89'):
    comando = {"comando":"start","premium":1,"comid":comid,"userBot":userBot,"chatid":chatid}
    try:
        print('enviando ',comando)
        ssock.send(json.dumps(comando).encode('utf-8'))
    except Exception as e:
        print('error enviando un mensaje al servidor ',e)

def connectServer():
    global requestReset
    global sock,ssock
    while True:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            hostname = 'leybot.leyguistar.com'
            context = ssl.create_default_context()

            sock = socket.create_connection((hostname,8443))
            ssock = context.wrap_socket(sock,server_hostname=hostname)  
            ssock.send(('{"instanceid":"%s","type":5,"chatid":"lite","pid":%d,"processid":%d}' % (instanceid,os.getpid(),processid)).encode('utf-8'))
            
            print('conectado con el servidor')
            while 1:
                text = ssock.recv()
                print('recibido',text)
                if(text == ""):
                    ssock.send('KA'.encode('utf-8'))
                    continue

                message = json.loads(text.decode('utf-8'))
                comando = message['comando']

        except Exception as e:
            # PrintException()
            print('error conectando con el servidor, reintentando')
            sleep(60)
def checkStartBot(chatid,uid,cid,replyid,s,alias=None):
    print('startbot en',uid)
    bots = s.loadBots(owner=uid)
    names = [i[1] for i in bots]
    print(names)
    count = len(names)
    if(alias):
        if(alias not in names):
            send_reply(chatid,'no hay un bot con ese nombre',replyid,comid=cid)
        else:
            for i in bots:
                if(i[1] == alias):
                    sendStart(chatid,cid,1,i[0])
                    break
            return 1

    if(count > 1):
        text = 'Hay varios bots para eligir pon /startbot [nombre del bot]:\n'
        for n in names:
            text += n + '\n'
        send_reply(chatid,text,replyid,comid=cid)
        return 2
    elif(count == 1):
        sendStart(chatid,cid,1,bots[0][0])
        return 1
    elif(not count):
        return 0

def on_group_member_join(data,s):

    message = data['o']['chatMessage']
    id = message['messageId']
    oldMessagesLock.acquire()
    if(id in oldMessages):
        oldMessagesLock.release()
        return
    oldMessages.append(id)
    oldMessagesLock.release()

    comid = data['o']['ndcId']
    chatid = message['threadId']
    userid = message['uid']
    nickname = message['author']['nickname']
    if(userid == client.profile.id):
        return
    print(message['author']['nickname'],'Bienvenido')
    if(chatid not in chats):
        try:
            chat = s.loadChat(chatid)
            respuestas[chatid] = s.loadRespuestasChat(chatid)
            opCustom[chatid] = s.loadCustomOPS(chatid)

        except mysql.connector.errors.DatabaseError as e:
            PrintException()
        except Exception as e:
            PrintException()

        if(chat == None):
            # sub_client = amino.SubClient(comid=comid,profile=client.profile)
            r = get_chat_thread(chatid,comid)
            print('guardando chat ' + str(r['title']) )
            ops = {}
            ops['your_uuid'] = 3
            try:
                s.chat(chatid,str(r['title']),chatid,0,0,0,'',ops,uid=r['uid'],comid=comid )
                chat = s.loadChat(chatid)
            except mysql.connector.errors.DatabaseError as e:
                return                
        chats[chatid] = chat
    else:
        chat = chats[chatid]
    states = s.loadBotstate(chatid)
    if(states):
        state = states[0]
    else:
        s.botstate(0,0,comid,0,chatid)
        state = 0         
    if(state == 0):
        lanzarBienvenida(chatid,chat,nickname,userid)    
    s.db.close()


def checkStart(data,s):
    message = data['o']['chatMessage']
    comid = data['o']['ndcId']
    id = message['messageId']
    cid = data['o']['ndcId']
    chatid = message['threadId']
    if(chatid not in chatThreads):
        get_chat_thread(chatid,cid)
        print('obteniendo thread',chatid)
    if(chatThreads[chatid]['type'] == 0):
        print('mensaje privado')
        return
    # print(data)
    content = message['content']
    userid = message['uid']
    states = s.loadBotstate(chatid)
    if(states):
        state = states[0]
    else:
        s.botstate(0,0,comid,0,chatid)
        state = 0         
    if(state == 0 or True):
        checkChat(chatid,cid,message,get_host(chatid,cid),get_cohosts(chatid,cid),s)
def doRelogin(t):
    while 1:
        sleep(t)
        relogin()

def getChats(t):
    sub_client = amino.SubClient(comId=67,profile=client.profile)
    while 1:
        comids = client.sub_clients().comId
        for comid in comids:
            sub_client.comId = comid
            sub_client.activity_status(1)
            sub_client.send_active_obj()
            threads = sub_client.get_chat_threads(size=100,raw=True)['threadList']
            for chat in threads:
                chatid = chat['threadId']
                chatThreads[chatid] = chat
                comidChat[chatid] = comid
        sleep(t)

try:
    r = requests.get('http://169.254.169.254/latest/meta-data/instance-id',timeout=0.5)
except:
    instanceid = 'i-local'
else:
    instanceid = r.text

def getProcessId():
    global users, bienvenidas
    s = Save()
    processid = s.process(2,__file__,'lite',5,os.getpid(),instanceid)
    users = s.loadAllUsers()
    bienvenidas = s.cargarBienvenidas()
    s.db.close()
    return processid
def han(js):
    data = json.loads(js)
    t = data['t']
    # print(data)
    handlerSave = None
    if('chatMessage' in data['o']):
        message = data['o']['chatMessage']
        messageId = message.get('messageId')
        oldMessagesLock.acquire()
        if(messageId in oldMessages):
            oldMessagesLock.release()
            return
        oldMessages.append(messageId)
        oldMessagesLock.release()

        comid = data['o']['ndcId']
        tipo = message['type']
        userid = message.get('uid',None)
        author = message.get('author',None)
        if(author):
            chatid = message['threadId']
            createdTime = message.get('createdTime')
            createdTime = createdTime[:10] + ' ' + createdTime[11:19]
            content = message.get('content',None)
            nickname = message['author'].get('nickname',None)
            title = message.get('title',None)
            handlerSave = Save()
            if(chatid not in chats):
                handlerSave.db.reset_session()
                c = handlerSave.loadChat(chatid)
                if(not c):
                    chat = get_chat_thread(chatid,comid)
                    title = chat.get('title','')
                    ops = {}
                    ops['your_uuid'] = 3
                    try:
                        print('guardando nuevo chat',title)
                        handlerSave.chat(chatid,title,chatid,0,0,0,'',ops,uid=chat['uid'],comid=comid)
                        chat = handlerSave.loadChat(chatid)
                        chats[chatid] = chat
                        respuestas[chatid] = handlerSave.loadRespuestasChat(chatid)
                        opCustom[chatid] = handlerSave.loadCustomOPS(chatid)

                    except mysql.connector.errors.DatabaseError as e:
                        return                

                else:
                    chats[chatid] = c
                    respuestas[chatid] = handlerSave.loadRespuestasChat(chatid)
                    opCustom[chatid] = handlerSave.loadCustomOPS(chatid)

            mensaje = Mensaje(message.get('messageId'),content,message.get('uid',None),nickname,createdTime,tipo,message.get('mediaValue',None),'',json.dumps(message.get('extensions',None)),s = handlerSave)
            try:
                mensaje.save(chatid)
            except mysql.connector.errors.IntegrityError as e:
                return
            except Exception as e:
                print('error guardando mensaje')
                PrintException()
                return
            print(nickname,content)
            if(test and userid != ley):
                handlerSave.db.close()
                return
            if(tipo == 0 and 'content' in message):

                try:
                    checkStart(data,s=handlerSave)
                except Exception as e:
                    PrintException()

            elif(tipo == 101):
                on_group_member_join(data,s=handlerSave)
    if(handlerSave):
        handlerSave.db.close()
    # print()
def udp_connect():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:

        data, addr = sock.recvfrom(10240) # buffer size is 1024 bytes
        tChat = threading.Thread(target=han, args=(None,data.decode('utf-8')))
        tChat.daemon = True
        tChat.start()

handler = SocketHandler(client.sid,client.device_id,han,120,debug=False)
handler.start()

processid = getProcessId()
tChat = threading.Thread(target=doRelogin, args=(3600,))
tChat.daemon = True
tChat.start()


tChat = threading.Thread(target=getChats, args=(60,))
tChat.daemon = True
tChat.start()

tChat = threading.Thread(target=connectServer, args=())
tChat.daemon = True
tChat.start()


# tChat = threading.Thread(target=udp_connect, args=())
# tChat.daemon = True
# tChat.start()

while 1:
    text = input()
    if(text == 'threads'):
        for i in threads:
            print(i,threads[i])
    elif(text == 'locks'):
        print('todo bien')
    elif(text == 'release'):
        try:
            oldMessagesLock.release()
            print('released oldMessagesLock')
        except Exception as e:
            print(e)
        
    elif(text == 'verbose'):
        verbose = not verbose
