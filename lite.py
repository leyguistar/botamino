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
try:
    import ujson as json
except ImportError:
    import json
    print('warning ujson not installed please install it is more faster than json')
import html2text
from urllib.parse import unquote
from urllib.parse import quote
import urllib.request
from time import time
from gtts import gTTS

client = amino.Client()
client.device_id = '010E4A69D1B3066CA9A127890A5531929F3818F16BA22092D5A91DEFB2CB73F53648E28EFAB98A4B61'
client.login(email='', password='')
sub_client = amino.SubClient(comId='67', profile=client.profile)
interaciones1 = os.listdir('interaccion/1')
interaciones2 = os.listdir('interaccion/2')
tipoMensaje = 100
oldMessages = []
interaciones2.remove('cum')
interaciones2.remove('coger')
interaciones1.remove('gemir')
hardcoreComandos = ['cum','coger','gemir']
def getNickname(userid):
    return sub_client.get_user_info(userid).nickname
def get_title(chatid):
    thread = sub_client.get_chat_thread(chatid)
    return thread.json['title']


def send_marco(chatid,mensaje,mup = 0,mdown = 0):
    m = marcos[mup][0] + '\n\n' + mensaje + '\n\n' + marcos[mdown][1]
    send_message(chatid,m)  

def send_reply(chatId,message,replyid):
    sub_client.send_message(message=message, chatId=chatId,replyTo=replyid)

def send_invocacion(chatId,mentionUserIds,message=""):
    sub_client.send_message(message=message, chatId=chatId,messageType=tipoMensaje,mentionUserIds=mentionUserIds)

def send_upload(chatid,embedImage):
    sub_client.send_message(chatId=chatid,embedBytes=embedImage)
def send_media(chatid,data=None,tipo=None,filename=None):
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
    if(link):
        sub_client.send_message(chatId=chatid,link=link)

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
    for i in range(3):
        r = sub_client.send_message(chatId=chatid,filePath=file)
        if(r == 200):
            break
def send_sticker(chatid,stickerid):
    r = sub_client.send_message(chatId=chatid,stickerId=stickerid)


def send_gif(chatid,gif):
    sub_client.send_message(chatId=chatid,sendBytesGif=gif)

def send_link(chatid,link):
    sub_client.send_message(chatId=chatid,link=link)

def borrarDeUsuario(chatid,userid):
    send_message(message='Borrando mensajes de ' + getNickname(userid), chatId=chatid)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=200)  # Gets messages of each chat
    for uid, content, id in zip(messageList.author.id, messageList.content, messageList.messageId):
        print("id: " + uid)
        print("userid " + userid)
        if(uid == userid):
            sub_client.delete_message(chatId=chatid,messageId=id)
    #send_message(message='listo', chatId=chatid)
    
def borrarMedia(chatid):
    send_message(message='Borrando stickers e imagenes', chatId=chatid)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=200)  # Gets messages of each chat
    for id, mediaValue in zip(messageList.messageId,messageList.mediaValue):
        print("id %s media %s" % (str(id),str(mediaValue)))
        if(mediaValue != None ):
            sub_client.delete_message(chatId=chatid,messageId=id)
    #send_message(message='listo', chatId=chatid)

def borrarN(chatid,n):
    send_message(message='Borrando ultimos ' + str(n) + ' mensajes', chatId=chatid)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=n)  # Gets messages of each chat

    for id,content in zip(messageList.messageId,messageList.content):
        print("Borrando: " + str(content) )
        sub_client.delete_message(chatId=chatid,messageId=id)
def get_host(chatid):
    thread = sub_client.get_chat_thread(chatid)
    return thread.json['author']['uid']

def get_cohosts(chatid):
    thread = sub_client.get_chat_thread(chatid)
    try:
        return thread.extensions['coHost']
    except:
        return []

def killUser(chatid,userid):
    send_message(message=getNickname(userid) + " fell out of the world", chatId=chatid)

def mostrarJuegos(chatid):
    mensaje = ''
    with open('juegos.txt', 'r') as handler:
        mensaje = handler.read()
    mensaje += '\n\nJuegos actuales: '
    for i in juegos:
        mensaje += str(i) + ' '
    send_message(message=mensaje, chatId=chatid)

def mostrarMarcos(chatid):
    m = ""
    i = 0
    for l in marcos:
        m += str(i) + '\n'
        m += l[0] + '\n\n' + l[1] + '\n'
        i+=1
    send_message(message=m, chatId=chatid)

def ship(chatid,u1,u2,l = 0):
    m = "💖💖💖💖💖💖💖💖💖💖💖💖\n\n"
    m+= getNickname(u1) + " 💑 " + getNickname(u2) + "\n\n"
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

    send_message(chatid,random.choice(frases) % (getNickname(u1),getNickname(u2)) )
    sub_client.send_message(chatid,link=link)




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
        h.write('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
        traceback.print_exc(file=h)

def bienvenida(chatid,mensaje="",mup=0,mdown=0,userid = None):
    if(userid == None):
        if(mensaje == None):
            send_message(message=marcos[mup][0] + '\n\n' +
            '🅱🅸🅴🅽🆅🅴🅽🅸🅳🅾🆂 🅽🆄🅴🆅🅾🆂 🅸🅽🆃🅴🅶🆁🅰🅽🆃🅴🆂' + '\n\n' + marcos[mdown][1], chatId=chatid)
        else:
            send_message(message=marcos[mup][0] + '\n\n' +
            '🅱🅸🅴🅽🆅🅴🅽🅸🅳🅾🆂 🅽🆄🅴🆅🅾🆂 🅸🅽🆃🅴🅶🆁🅰🅽🆃🅴🆂' + 
            '\n\n' + mensaje+ '\n\n' + marcos[mdown][1], chatId=chatid)
    else:
        send_message(message=marcos[mup][0] + '\n\n' + 
        '\n\nBienvenid@ ' + getNickname(userid) + "\n\n" + mensaje + '\n\n' + marcos[mdown][1], chatId=chatid)

def despedir(chatid,message="",mup=0,mdown=0,userid = None):
    if(userid == None):
        send_message(message=marcos[mup][0] +
        '\n\nAdios ' + message + '\n\n' + marcos[mdown][1], chatId=chatid)

    else:
        send_message(message=marcos[mup][0] +
        '\n\nAdios ' + getNickname(userid) + '\n\n' + marcos[mdown][1], chatId=chatid)

def send_message(chatId,message,tm=-1):
    prefijo = '[c]'
    if(tm < 0):
        tm = tipoMensaje
    if(tm == 0):
        sub_client.send_message(message=(prefijo + message).replace('\n','\n' + prefijo), chatId=chatId,messageType=tm)
    else:
        sub_client.send_message(message=message, chatId=chatId,messageType=tm)

def jail(chatid,userid):
    info = sub_client.get_user_info(userId=userid)
    img = requests.get(info.icon).content
    im1 = Image.open('imagenes/carcel2_resize.jpg')
    im2 = Image.open('imagenes/jail_bars2.png')
    im3 = Image.open(io.BytesIO(img))
    loli = Image.open('imagenes/jail_loli.png')
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
    info = sub_client.get_user_info(userId=userid)
    img = requests.get(info.icon).content
    patada = Image.open('imagenes/patada.gif')
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
    send_media(chatid,'R.I.P ' + getNickname(userid))

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


chatsRevisando = []
ignorar = True
def checkChat(chat,ignorar,cohosts,host):
        chatid = chat
        chatPath = 'chats/' + chatid + '/'
        if(not os.path.exists(chatPath)):
            os.mkdir(chatPath)

        try:
            messageList = sub_client.get_chat_messages(chatId=chat,size = 1)  # Gets messages of each chat
            # print('mensajes obtenidos')
            for nickname, content, id, mediaValue, createdTime, extensions, userid , tipo in zip(messageList.author.nickname, 
                messageList.content, messageList.messageId,messageList.mediaValue,
                messageList.createdTime,messageList.extensions,messageList.author.id,messageList.type):
                if id in oldMessages: 
                    continue
                oldMessages.append(id)  # Adds message id to a list so it doesn't repeat commands
                print(nickname,content,mediaValue)
                if(chatid in skipChats):
                    if(content == "startlite"):
                        if(chatid in skipChats):
                            if(userid == host or userid in cohosts):
                                skipChats.remove(chatid)
                        else:
                            send_reply(chatid,'bot lite actualmente prendido',id)
                if(ignorar):
                    continue

                if(tipo == 101):
                    if(chatid not in mensajesChats):
                        try:
                            with open(chatPath + 'mensaje.txt','r') as h:
                                mensaje = h.read()
                            mensajesChats[chatid] = mensaje
                        except Exception as e:
                            mensaje = ''
                            mensajesChats[chatid] = ''
                    else:
                        mensaje = mensajesChats[chatid] 
                    if(chatid not in marcosChats):
                        try:
                            with open(chatPath + 'marcos.txt','r') as h:
                                m = h.read().split('\n')
                                mup = int(m[0])
                                mdown = int(m[1])
                            marcosChats[chatid] = (mup,mdown)
                        except Exception as e:
                            mup = 0
                            mdown = 0
                            marcosChats[chatid] = (0,0)
                    else:
                        m = marcosChats[chatid]
                        mup = m[0]
                        mdown = m[1]
                    bienvenida(chatid,mensaje,mup,mdown,userid)

                if(chatid in funados):
                    if(userid in funados[chatid]):
                        sub_client.delete_message(chatId=chatid,messageId=id)

                if(content == None):
                    continue
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
                    for m in extensions['mentionedArray']:
                        print('mencion a: ' + m['uid'])
                        usersid.append(m['uid'])
                if('replyMessageId' in extensions):
                    replyid = extensions['replyMessageId']
                    replyuid = extensions['replyMessage']['uid']
                else:
                    replyid = None
                    replyuid = None
                if(not usersid and replyuid != None and replyuid != userid):
                    usersid.append(replyuid)
                # if(chatid != 'e1ed3d4b-d58a-4209-ab1e-69218df1c3c6'):
                #     continue
                if content[0][0] == "/":
                    comando = content[0][1:]
                    comando = unicodedata.normalize( 'NFKC', comando)
                    # print(comandos)
                    if(comando in comandos):
                        if(comandos[comando][1] > 0):
                            send_reply(chatid,'Este es un comando premium',id)
                            if(os.path.exists('ayuda/comandos/' + comando + '.txt')):
                                with open('ayuda/comandos/' + comando + '.txt','r') as h:
                                    text = h.read()                                
                                send_message(chatid,text)
                            else:
                                send_message(chatid,'Todavia no hay ayuda para este comando')

                        elif(comandos[comando][0] > opLevel):
                            send_message(chatid,'No tienes permisos para utilizar este comando')
                            continue
                    else:
                        continue
                    if(comando in interaciones1):
                        path = 'interaccion/1/%s/' % (comando)
                        ipath = path + 'SFW/'
                        lpath = path + 'SFWL/'
                        imagenes = os.listdir(ipath)
                        img = random.choice(imagenes)
                        if(not os.path.exists(lpath + img)):
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
                        send_message(chatid,random.choice(frases) % (nickname))
                        sub_client.send_message(chatid,link=link)

                        # send_media(chatid,filename=path + random.choice(imagenes))
                    elif(comando in interaciones2):
                        if(usersid):
                            for u in usersid:
                                path = 'interaccion/2/%s/' % (comando)
                                ipath = path + 'SFW/'
                                lpath = path + 'SFWL/'
                                imagenes = os.listdir(ipath)
                                img = random.choice(imagenes)
                                if(not os.path.exists(lpath + img)):
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

                                send_message(chatid,random.choice(frases) % (nickname,getNickname(u)) )
                                sub_client.send_message(chatid,link=link)
                                
                                # send_media(chatid,filename=path + random.choice(imagenes))
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
                        # r = client.start_chat([ley],'')
                        print(r[0])
                        # print(r[1])
                        if(r[0] == 200):
                            userchat = r[1]['thread']['threadId']
                            print(userchat)
                            print(r[1])
                            mostrarMarcos(userchat)
                            send_message(chatid,'%s revisa tu privado para ver los marcos' % (nickname))
                        else:
                            send_message(chatid,'Los marcos se envian al privado por favor escribele al bot para poder enviarte los marcos')
                    elif(comando == "recibir"):
                        if(chatid not in mensajesChats):
                            try:
                                with open(chatPath + 'mensaje.txt','r') as h:
                                    mensaje = h.read()
                                mensajesChats[chatid] = mensaje
                            except Exception as e:
                                mensaje = ''
                                mensajesChats[chatid] = ''
                        else:
                            mensaje = mensajesChats[chatid] 
                        if(chatid not in marcosChats):
                            try:
                                with open(chatPath + 'marcos.txt','r') as h:
                                    m = h.read().split('\n')
                                    mup = int(m[0])
                                    mdown = int(m[1])
                                marcosChats[chatid] = (mup,mdown)
                            except Exception as e:
                                mup = 0
                                mdown = 0
                                marcosChats[chatid] = (0,0)
                        else:
                            m = marcosChats[chatid]
                            mup = m[0]
                            mdown = m[1]

                        if(usersid):
                            for u in usersid:
                                bienvenida(chatid,"",mup,mdown,u)
                        else:
                            bienvenida(chatid,mensaje,mup,mdown)
                    elif(comando == "despedir"):
                        if(chatid not in mensajesChats):
                            try:
                                with open(chatPath + 'mensaje.txt','r') as h:
                                    mensaje = h.read()
                                mensajesChats[chatid] = mensaje
                            except Exception as e:
                                mensaje = ''
                                mensajesChats[chatid] = ''
                        else:
                            mensaje = mensajesChats[chatid] 
                        if(chatid not in marcosChats):
                            try:
                                with open(chatPath + 'marcos.txt','r') as h:
                                    m = h.read().split('\n')
                                    mup = int(m[0])
                                    mdown = int(m[1])
                                marcosChats[chatid] = (mup,mdown)
                            except Exception as e:
                                mup = 0
                                mdown = 0
                                marcosChats[chatid] = (0,0)
                        else:
                            m = marcosChats[chatid]
                            mup = m[0]
                            mdown = m[1]

                        if(usersid ):
                            for u in usersid:
                                despedir(chatid,'',mup,mdown,u)
                        else:
                            despedir(chatid,"se les quiere",mup,mdown)

                    elif(comando == "kill"):
                        if(usersid):
                            for u in usersid:
                                killUser(chatid,u)
                        else:
                            send_message(chatid,'uso: /kill @: envia un mensaje de muerte para los usuarios con @')

                    if(userid not in cohosts and userid != host and userid != ley):
                        return
                    if(comando == "marco"):
                        if(len(content) == 2):
                            mn = int(content[1])
                            if(mn < 11   and mn >= 0):
                                with open(chatPath + 'marcos.txt','w') as h:
                                    h.write(str(mn) + '\n' + str(mn) )
                            else:
                                send_message(chatid,'La version lite del bot solo puede usar los marcos del 0 al 10')
                        elif(len(content) == 3):
                            mn = int(content[1])
                            mn2 = int(content[1])
                            if(mn < 11 and mn >= 0 and mn2 < 11 and mn2 >= 0):
                                with open(chatPath + 'marcos.txt','w') as h:
                                    h.write(str(mn) + '\n' + str(mn) )
                            else:
                                send_message(chatid,'La version lite del bot solo puede usar los marcos del 0 al 10')
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
                                if(userid == ley or userid ==  get_host(r.objectId)):
                                    if(com != sub_client.comId):
                                        send_message(chatid,'Advertencia link de otra comunidad, enviando el bot a esa comunidad')

                                    client.join_community(com)
                                    comid = sub_client.comId
                                    sub_client.comId = com
                                    sub_client.join_chat(r.objectId)
                                    sub_client.comId = comid
                                    send_message(r.objectId,'¡Hola!\nSoy leybot y me han tepeado a este chat (solo el anfitrion deberia poder tepearme), para ayuda del bot /ayuda ')

                                    send_message(botgroup,'tp de ' + nickname + '\nA: ' + str(get_title(r.objectId)) )
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
                            send_message('uso: /random [n1] [n2]: genera un numero random entre n1 y n2')
                    elif(comando == "disponible"):
                        t = "Comandos disponibles segun tu nivel de permisos:\n"
                        for c in comandos:
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
                                send_message(chatid,'Error id no encontrado')
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
                        text = '[b]Comandos lite:\n\n'
                        text += 'Comandos para todos: '
                        for c in c0:
                            text += ' %s ' % (c)
                        text += '\n\nComandos de coa: '
                        for c in c1:
                            text += ' %s ' % (c)
                        text += '\n\nComandos de anfi: '
                        for c in c2:
                            text += ' %s ' % (c)

                        text += '\n\n[b]Comandos de la version completa:\n\n'
                        for c in cpro:
                            text += ' %s ' % (c)
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
                            text = getNickname(userid) + ' ' 
                            if(replyuid):
                                u = replyuid
                                text += allContent[1:] + ' a ' + getNickname(u)
                            elif(len(usersid) == 1 ):
                                u = usersid[0]
                                text += allContent[1:]
                                text = text[:text.rfind('@')]
                                text += ' a ' + getNickname(u)
                            send_message(chatid,text)

                    elif(comando == "se"):
                        text = getNickname(userid) + ' ' + allContent[1:]
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
                            send_message(chatid,'uso: /placa [placa del chat]\n Guarda la placa del chat')
                            if(os.path.exists(chatPath + 'placa.txt')):
                                with open(chatPath + 'placa.txt','r') as h:
                                    placa = h.read()
                                send_message(chatid,'Placa actual del chat: ' + str(chat.placa) )
                        else:
                            placa = m
                            with open(chatPath + 'placa.txt','w') as h:
                                h.write(m)
                            send_message(chatid,'Placa del chat actualizada: ' + m)
                            send_message(botgroup,'El chat ' + get_title(chatid) + '\nActualizo su placa: ' + m,0)
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
                            chatname = get_title(chatid)
                            text = 'Bug reportado en el chat ' + chatname + '\n'
                            text += 'Por: '+ nickname + '\n'
                            text += m
                            send_message(botgroup,text)
                            send_message(chatid,'Bug reportado')
                    elif(comando == "sugerencia"):
                        if(m == None):
                            send_message(chatid,'uso: /sugerencia [mensaje]: Sirve para enviar sugerencias de cosas que te gustarian cambiar, quitar o cambiar al bot.\nComo por ejemplo mas lolis')
                        else:
                            chatname = get_title(chatid)
                            text = 'Sugerencia en el chat ' + chatname + '\n'
                            text += 'Por: '+ nickname + '\n'
                            text += m
                            send_message(botgroup,text)
                            send_message(chatid,'Gracias por tu sugerencia')
                    elif(comando == "opinion"):
                        if(m == None):
                            send_message(chatid,'uso: /opinion [tu openion del bot]: Sirve para dar una opinion sobre el bot')
                        else:
                            chatname = get_title(chatid)
                            text = 'opinion en el chat ' + chatname + '\n'
                            text += 'Por: '+ nickname + '\n'
                            text += m
                            send_message(botgroup,text)
                            send_message(chatid,'Gracias por tu opinion')
                    elif(comando == "loli"):
                        send_message(chatid,'Solo los mas puros de corazon pueden ver esta imagen')
                        send_link(chatid,'http://st1.narvii.com/7680/d0b72bcf6e50745f0256acaf27770b2b8d70b763r5-184-180_00.jpeg')
                    elif(comando == "trapito"):
                        trapitos = os.listdir('trapitos')
                        print('trapitos/' + random.choice(trapitos))
                        send_imagen(chatid,'trapitos/' + random.choice(trapitos))
                    elif(comando == "decir"):
                        if(m):
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
                                continue
                            if(not os.path.exists(chatPath + 'audios/')):
                                os.mkdir(chatPath + 'audios/')
                            path = chatPath + 'audios/' + str(int(time())) + '.mp3'
                            tts.save(path)
                            send_imagen(chatid,path)
                        else:
                            send_message(chatid,'uso: /decir [texto]: envia una nota de voz diciendo el texto')
                    elif(comando == 'entrar'):
                        if(len(content) > 1):

                            if(content[1] == 'en'):
                                send_message(chatid,getNickname(userid) + ' a entrado ' + ' '.join(content[1:]))
                            elif(content[1] in ['a','al']):
                                send_message(chatid,getNickname(userid) + ' se a unido ' + ' '.join(content[1:]))
                            else:
                                send_message(chatid,getNickname(userid) + ' a entrado ' + ' '.join(content[1:]))

                    elif(comando == 'dejar'):
                        if(len(content) > 1):
                            send_message(chatid,getNickname(userid) + ' ha dejado ' + ' '.join(content[1:]))
                    elif(comando == 'miau'):
                        send_link(chatid,getCat())
                    elif(comando == "coas"):
                        text = 'Coas:\n'
                        for c in cohosts:
                            text += '%s\n' % (getNickname(c))
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
                            continue
                        if(usersid):
                            funados[chatid] = [item for item in funados[chatid] if item not in usersid]
                        else:
                            send_message(chatid,'uso: /perdonar @: perdona la funa de los usuarios mencionados')
                    elif(comando == "apagar"):
                        skipChats.append(chatid)
                        send_message(chatid,'apagando bot lite')
                    elif(comando == "skip"):
                        skipChats.append(chatid)
                        send_message(chatid,'apagando version lite')

        except Exception as e:
            PrintException()
            print(e)

        chatsRevisando.remove(chatid)


print('pues aqui')
#load zone
with open('marcos.txt', 'r') as handler:
    buf = [line.rstrip() for line in handler]
    marcos = []
    for i in range(0,len(buf),2):
        marcos.append((buf[i],buf[i+1]))

juegos = os.listdir('juegos')
juegos.remove('__pycache__')
juegos.remove('fifo')
juegos.remove('asesino')
juegos.remove('fifos')
juegos.remove('retos')
juegos.append('mafia')
juegos.sort()
comandos = {}
funados = {}
comandosPremium = {}
with open('lite/comandos.txt', 'r') as h:
    handler = h.read().split('\n')
    for line in handler:
        # print(line)
        cl = line.split(' ')
        # print(cl)
        if(cl[2] == '0'):
            # print(cl[0])
            comandos[cl[0]] = (int(cl[1]),0)
        elif(cl[2] == '1'):
            comandos[cl[0]] = (int(cl[1]),1)
            comandosPremium[cl[0]] = int(cl[1])
for c in interaciones1:
    comandos[c] = (0,0)    
for c in interaciones2:
    comandos[c] = (0,0)    

#set variables
ley = 'your_uuid'
botgroup = '17ab60ec-0418-4c75-8ce3-fdb11613b201'
traducirDetectarUsers = {}
debug = {}
cacheLetras = {}
mensajesChats = {}
marcosChats = {}
skipChats = []
tzs = ('America/Caracas','America/Buenos_Aires',
'America/Bogota','America/Mexico_City','America/Lima',
'America/Tijuana','America/Santiago','Europe/Madrid')
temporadas = {'invierno':'winter','primavera':'spring','verano':'summer','otoño':'fall'}
dias = {'lunes':'monday','martes':'tuesday','miercoles':'wednesday','thursday':'jueves','viernes':'friday','sabado':'saturday','domingo':'sunday'}

#no se

jikan = Jikan()
translator = Translator()
startbotTime = time()

# while True:
#     chatsRevisando.append(botgroup)
#     checkChat(botgroup,False,[],ley)    
while True:
    readChats = sub_client.get_chat_threads(start=0, size=10)  # Gets all chats the user is in
    for chatid,title,cohosts,host in zip(readChats.chatId,readChats.title,readChats.coHosts,readChats.creatorId):

        if(chatid not in chatsRevisando):
            # print('revisando ' + title)
            chatsRevisando.append(chatid)
            tChat = threading.Thread(target=checkChat, args=(chatid,ignorar,cohosts,host))
            tChat.daemon = True
            tChat.start()
    ignorar = False
