#!/usr/bin/env python3
import amino
import os
import requests
import threading
import unicodedata
import random
import sys
import animelyrics
from time import sleep
from googletrans import Translator
import datetime
import signal
import lite_private
from youtube_search import YoutubeSearch as ys
from collections import deque
import resource
try:
    import ujson as json
except ImportError:
    import json
    print('warning ujson not installed please install it is faster than json')
from time import time
from save import Save
import mysql.connector.errors
from user import User
import socket
from aminosocket import SocketHandler
import aminosocket
from mensaje import Mensaje
import subprocess
from litefuns import login,getJuegos,send_message,send_interaccion,getNickname,mostrarMarcos,send_reply,bienvenida,despedir
from litefuns import borrarDeUsuario,borrarMedia,borrarN,mostrarJuegos,ship,get_host,get_title,send_invocacion,send_link
from litefuns import tp,get_chat_thread,lanzarBienvenida,ver,get_comandos_comunidad
from litefuns import horas,rip,send_imagen,getCat,getGif,getUser,download,send_audio,simpsf
from litefuns import get_host,get_cohosts,send_marco,getTrueNickname,get_backGround,getMediaValues
from litefuns import upload_s3,upload_file_s3,urlAmino,send_sticker,ping
from litefuns import send_youtube,searchYoutube,top,cargarVoces,decir,saveMedia,saveMediaSticker
from litefuns import eraseMedia,loadRespuestas,responder_interacciones,nsfw,strike
from litefuns import get_chat_bot_and_thread,changeBot,info,mostrarAyuda,delete_message,delete_message_thread
from litefuns import nudeDetect,metercoa,sacarcoa,isLeader,isCurator,isStaff,useridByLink
from litefuns import testMuted,top2,invocar_a_todos
from litefuns import get_voice_chat_info_and_join,leave_voice_chat,requestQueue,sendPauseRequest,requestVolumeChange,sendVideoRequest,get_voice_chat_info
from litefuns import requestPlayPosition,sendYoutubeObject,sendPlayRequest
from litefuns import skipSong,leaveChannel
from litefuns import start_live_mode,getSubClient
from litefuns import recoverMessage,addLogro,send_waifu
from litefuns import send_red_text,start_game
from litefuns import remove_from_channel,request_channel_info,send_text_imagen
from litefuns import preAddLogro,send_botgroup
from litefuns import get_channel,limpieza
from litefuns import delete_ban_report,copy_profile
from litefuns import detect_or_join_channel
from litefuns import to_private_chat
from litefuns import good_upload,send_text_imagen_raw
from litefuns import send_ficha,wikiByLink
from litemusic import play_audio
from litefuns import on_leave_channel
from litefuns import crearFicha,tmp
from litefuns import get_simps_user,get_simping_user
from litefuns import loadMedia
from litefuns import getClient,chat_bubble_background,chat_bubble_sticker,chat_bubble_color,chat_bubble_insets,chat_bubble_zoom,chat_bubble_zip
from convert import convert
import convert as conver
from playerInfo import get_player_info
import playerInfo
from channel import waitForChannel
from anime import manga,personaje,temporada,buscarAnime,emision,openings,endings
from edits import jail,patear,killUser,cum,gorrito,getFaces,pilImage,writeWikipedia,bienvenidaGif,licencia,bikini
from edits import applyGif,arcoiris,fiesta
from booru import buscarLoli,buscarMoe,buscarDanbooru,buscarChica,buscarr34
from liteobjs import comunidades,privadoPruebas
from liteobjs import lastWaifu
from liteobjs import likesWaifu,trashWaifu
from liteobjs import harems
from liteobjs import fichas
from liteobjs import filters
from liteobjs import chatThreads,users,marcos,comidChat,bienvenidas,tipoMensaje,imgdir,leybot,ley,botgroup,kirito,shita,clients,bots,defaultClient,comandosLite
from liteobjs import tipoMensajeChat,youtubeLists,cachesYoutube,userYoutube,voces,safeMessageType
from liteobjs import aliasesChat,lastUserCommand,chats,testBot,youtubethreads,respuestas,comandos
from liteobjs import opCustom,tipos_comandos,adminBot
from liteobjs import bannedUsers,bannedChats,chatSugerencias
from liteobjs import confidence,sentBooru,bannedUrls,bannedComunidades
from liteobjs import rolesComunidad,rolesUser
from liteobjs import sockets
from liteobjs import bucket
from liteobjs import channels
from liteobjs import seguirLimpiando,cancelarLimpieza
from liteobjs import logros
from liteobjs import tipos_items
from liteobjs import leyworld,ecchibot,palabrasjum
from liteobjs import resultadosTelefonos,telefonos
from liteobjs import comandosReverseMap,mensajes,palabrasIdioma
from liteobjs import waifus,husbandos,allWaifus
from liteobjs import modos,cuentas
from PIL import Image
from plot import plotActividad
import liteobjs
from amino.lib.util import headers as aminoHeaders
from amino.acm import ACM
import litefuns
import edits
from letras import buscar,letra,cacheLetras
import argparse
from exception import PrintException
from comando import Comando
from comunidad import Comunidad
import re
import psutil
test = False
sqlCredentials = 'default.set'
imgdir = 'imgs/'
output = True
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--sql", required=False,
    help="sql file",default='default.set')
ap.add_argument("-x", "--safe", required=False,
    help="safe message type",default=57)
ap.add_argument("-p", "--premium", action='store_true')
ap.add_argument("-m", "--mantenimiento", action='store_true')

ap.add_argument('-t', action='store_true')
args = ap.parse_args()

premium = args.premium
safeMessageType[0] = args.safe
test = args.t
if(test):
    liteobjs.VOICE_SERVER_IP = '127.0.0.1'
    litefuns.VOICE_SERVER_IP = '127.0.0.1'
    playerInfo.VOICE_SERVER_IP = '127.0.0.1'
    liteobjs.NUDE_DETECT_IP = '127.0.0.1'
    liteobjs.EDIT_SERVER_IP = '127.0.0.1'
    conver.EDIT_SERVER_IP = '127.0.0.1'
    litefuns.NUDE_DETECT_IP = '127.0.0.1'
    litefuns.EDIT_SERVER_IP = '127.0.0.1'
    # edits.NUDE_DETECT_IP = '127.0.0.1'
    edits.EDIT_SERVER_IP = '127.0.0.1'
litefuns.test = test
mantenimiento = args.mantenimiento
if(mantenimiento):
    litefuns.mantenimiento = True
sqlCredentials = args.sql
del ap
def jugar(chatid,juego,comid,userid,debug=False):
    print('en jugar')
    if(juego in getJuegos()):
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
        commands = ["python3",fileName,chatid,juego,"comid=" + str(comid),"mensaje="+str(111),"userid="+str(clients[chatid].profile.id)]
        if(not debug):
            commands.append('silent')
        print(' '.join(commands) + ' &' )
        os.system(' '.join(commands) + ' &' )
    else:
        send_message(chatid,mensajeid=2,args=(juego,) )
        return

    print('jugando ' + juego)
def gorrito_imagen(chatid,v,client,errorMessage='',successMessage='Aqui tienes tu gorrito uwu'):
    img = imgdir + 'gorrito.png'
    name = download(v)
    print(v)
    print(name)
    saveName = 'gorritos/' + name[5:name.rfind('.')] + '.png'
    if(os.path.exists(saveName)):
        if(os.stat(saveName).st_size == 0):
            if(errorMessage):
                send_message(chatid,errorMessage)            
        else:
            send_imagen(chatid,saveName)
            if(successMessage):
                send_message(chatid,successMessage)
    else:

        f = gorrito(chatid,pilImage(name),pilImage(imgdir + 'gorrito.png'),getFaces(name),client)
        # if(f):
        #     if(successMessage):
        #         send_message(chatid,successMessage)
        #     if(not os.path.exists('gorritos')):
        #         os.mkdir('gorritos')
        #     f.save(saveName,format="png")
        # else:
        #     if(errorMessage):
        #         send_message(chatid,errorMessage)
        #     with open(saveName,'w') as h:
        #         pass
def executeCommand(chat,content,userid,usersid,replyid,replyuid,createdTime,chatThread,client,esperar=True,user=None,id=None,role=None,premiumCommand=None):
    try:
        if(not content):
            return
        if(userid in bannedUsers):
            return
        modo = chat.settings['modo']

        if(modo == 3):

            opLevel = chat.ops.get(userid,0)
            if(opLevel < 2):
                return
        if(modo == 1):
            if(content.startswith('///')):
                content = content[2:]
            else:
                return
        comid = chatThread['ndcId']
        comandosCom = get_comandos_comunidad(comid)
        h = Save(autoConnect=False)
        bot = bots[client.profile.id]
        autorizados = chat.autorizados.get(client.profile.id,[])
        if(autorizados and userid != ley and userid != bot['owner']):
            if(userid not in autorizados):
                return
            else:
                opLevel = 3
        if(not user):
            user = getUser(userid)

        sub_client = client.sub_client(comid)
        if(content.find(" ") == -1):
            m = None
        else:
            m = content[content.find(" "):].lstrip()
        if(m == ""):
            m = None
        allContent = content
        content = str(content).split(" ")

        opLevel = chat.ops.get(userid,0)
        if(chat):
            chatid = chat.id
            host = chat.uid
        else:
            chatid = chatThread['threadId']
            host = chatThread['uid']
            if(userid == host):
                opLevel = 3

        palabras = palabrasIdioma[chat.idioma]
        ecchi = False

        if content[0][0] == "/":
            if(len(content[0]) < 2):
                return
            comando = content[0][1].lower() + content[0][2:]
            comando = unicodedata.normalize( 'NFKC', comando)
            commandid = comandosIdioma[chat.idioma].get(comando,0)
            if(not commandid and comando not in chat.comandos):
                return

            print('id comando',commandid,comando,chat.idioma)
            if(comando not in chat.comandos):
                if(premium and bot['public'] ):
                    t = comandos[commandid][1]
                    if(t == 8 or t == 16 or t == 7):
                        send_reply(chatid,mensajeid=4,replyid=id)
                        return

                if(chat.settings['modo'] == 1):
                    if(comandos[commandid][1] != 15 and opLevel < 2):
                        return
                elif(chat.settings['modo'] == 2):
                    if(comandos[commandid][1] != 13 and opLevel < 2):
                        return                
                elif(chat.settings['modo'] == 3):
                    if(opLevel < 2):
                        return
                elif(chat.settings['modo'] == 4):
                    if(opLevel < 3):
                        return
            else:
                if(bot['public'] and comid != leyworld):
                    send_message(chatid,mensajeid=143)
                    return
                lastComand = lastUserCommand.get(userid,('',0))
                if(esperar and time() - lastComand[1] < chat.settings["espera"]):
                    send_reply(chatid,mensajeid=3,args=(chat.settings["espera"]),replyid=id)
                    addLogro(chat,userid,40)
                    return
                lastUserCommand[userid] = (comando,time())
                for c in chat.comandos[comando].comandos:
                    if(c):
                        print('content',c)
                        if(c[0] == '*' and c[0] == c[-1]):
                            text = getNickname(userid,sub_client) + ' ' + c[1:-1]
                            send_message(chatid,text)
                        else:
                            executeCommand(chat,c,userid,usersid,replyid,replyuid,createdTime,chatThread,client,esperar=False,user=user,role=role)
                return
            if(commandid):
                print(comandos[commandid])
                if(comandos[commandid][2] == 1 and bot['public'] == 1 and userid != ley and chatThread['uid'] != ley and comid != leyworld and premiumCommand != commandid):
                    # send_reply(chatid,'comando no disponible en esta version',id)
                    return
                elif(comandos[commandid][2] == 2 and bot['public'] == 2 and userid != ley and chatThread['uid'] != ley and comid != leyworld):
                    # send_reply(chatid,'comando no disponible en esta version',id)
                    return
                elif(comandos[commandid][2] == 3 and userid != ley):
                    return
                elif(comandos[commandid][2] == 4 ):                
                    send_reply(chatid,mensajeid=4,replyid=id)
                    return
                elif(comandos[commandid][2] == 5 and bot['public'] == 1 and comid != leyworld):
                    send_reply(chatid,mensajeid=5,replyid=id)
                    return                                
                elif(comandos[commandid][2] == 6 and comid != leyworld and bot['public'] == 1 and chat.idioma == 'es'):                
                    ecchi = True

                    if(chatThread['type'] == 2):
                        send_voice_note(chatid,9)
                        addLogro(chat,userid,32)
                        return
                    sub_client = client.sub_client(comid)
                elif(commandid in opCustom[chatid]):
                    if(opCustom[chatid][commandid] > opLevel):
                        send_message(chatid,mensajeid=6)
                        addLogro(chat,userid,12)

                        return
                    elif(opCustom[chatid][commandid] == -1):
                        send_message(chatid,mensajeid=7)
                        return
                # elif(comandos[commandid][0] == -1 and comandos[commandid]):
                elif(commandid in comandosCom and comandosCom[commandid] == 0):
                    send_message(chatid,mensajeid=8)
                    return
                elif(comandos[commandid][0] == -1 and chatThread['type'] == 2 and commandid not in comandosCom):
                    send_message(chatid,mensajeid=9,args=(comando) )
                    return
                elif(comandos[commandid][0] > opLevel):
                    send_message(chatid,mensajeid=6)
                    send_voice_note(chatid,4)    
                    addLogro(chat,userid,12)
                    return

            else:
                return
            lastComand = lastUserCommand.get(userid,('',0))
            # if(esperar and time() - lastComand[1] < chat.settings["espera"]):
            t = time()
            tdesde = t - lastComand[1]
            if(esperar):
                if( lastComand[0] == commandid and tdesde < comandos[commandid][3] ):
                    send_reply(chatid,mensajeid=662,args=(comandos[commandid][3]),replyid=id)
                    return
                elif(tdesde < 2):
                    send_reply(chatid,mensajeid=3,args=(2),replyid=id)
                    addLogro(chat,userid,40)
                    return

            lastUserCommand[userid] = (commandid,t)
            for u in usersid:
                chat.interacciones[u] = (commandid,userid,t)
            if(commandid > 1000):
                print('interaccion',interacciones[commandid-1000])
                send_interaccion(chatid,interacciones[commandid-1000],userid,usersid,sub_client,idioma=chat.idioma,ecchi=ecchi)
            elif(commandid == 1): #8ball
                if(not m):
                    send_message(chatid,mensajeid=21)
                else:
                    send_message(chatid,random.choice(ochoball[chat.idioma]))
            elif(commandid == 2 or commandid == 3): #abrazar #abrazo
                if(not usersid and comando == 'abrazo'):
                    # send_audio(chatid,'audios/Ven aquí, te daré un abrazo.aac')
                    send_voice_note(chatid,10,onlyLive=False)

                    send_interaccion(chatid,'abrazar',userid,usersid,sub_client,mensaje=False,idioma=chat.idioma,ecchi=ecchi)
                    send_message(chatid,mensajeid=144)
                else:
                    send_interaccion(chatid,'abrazar',userid,usersid,sub_client,idioma=chat.idioma,ecchi=ecchi)

            elif(commandid == 4):  #aceptar 
                if(len(content) < 2 ):
                    send_message(chatid,mensajeid=22)
                elif(content[1] == palabras['anfitrion']):
                    r = sub_client.accept_host(chatid)
                    if(not r):
                        send_message(chatid,mensajeid=26)
                    elif(r == 200):
                        send_message(chatid,mensajeid=27)
                        addLogro(chat,userid,48)
                elif(content[1] == palabras['lider']):
                    r = sub_client.accept_leader()
                    if(not r):
                        send_message(chatid,mensajeid=28)
                    elif(r == 200):
                        send_message(chatid,mensajeid=29)
                elif(content[1] == palabras['curador']):
                    r = sub_client.accept_curator()
                    if(not r):
                        send_message(chatid,mensajeid=30)
                    elif(r == 200):
                        send_message(chatid,mensajeid=31)
            elif(commandid == 5): #actividad
                t = time()-60
                text = mensajes[chat.idioma][32] + '\n'
                text += mensajes[chat.idioma][33] % (len(messagesPerMinute)) + '\n'

                text += mensajes[chat.idioma][34] % (len([i for i in lastActivityChat.values() if t <= i])) + '\n'
                try:
                    h.connect()
                    text += mensajes[chat.idioma][631] % (len(h.loadReproduciendo()))
                    img = plotActividad()
                    send_text_imagen(chatid,text,filename=img)
                    addLogro(chat,userid,34,h)
                except:
                    PrintException()
                h.close()
                # send_message(chatid,text)

            elif(commandid == 6): #tips
                if(len(content) != 2):
                    send_message(chatid,mensajeid=37)
                else:
                    try:
                        h.connect()
                        if(content[1] == palabras['si']):
                            h.chatSettings(chatid,agradecer=1)
                            chat.settings['agradecer'] = 1
                        elif(content[1] == palabras['no'] ):
                            h.chatSettings(chatid,agradecer=0)
                            chat.settings['agradecer'] = 0
                    except:
                        PrintException()
                    h.close()
            elif(commandid == 7): #agregar 
                
                if(len(content) != 2):
                    send_message(chatid,mensajeid=38)                           
                elif(content[1] not in chat.comandos):
                    send_message(chatid,mensajeid=39)
                elif(replyid == None):
                    send_message(chatid,mensajeid=40)
                else:
                    nombre = content[1]
                    comando = chat.comandos[nombre]
                    if(comando.userid != userid):
                        send_message(chatid,mensajeid=700)
                        return
                    message = sub_client.get_message_info(chatid,replyid)
                    content = message.json['content']
                    mediaValue = message.json.get('mediaValue',None)
                    print(content,mediaValue)
                    try:
                        h.connect()
                    except:
                        PrintException()
                        return
                    if(not content and mediaValue):
                        if(saveMedia(chatid,m,message.json,sub_client,h)):
                            content = '/media %s' % (m)
                        else:
                            for i in range(2,20):
                                mediaName = '%s %d' % (m,i)
                                r = saveMedia(chatid,mediaName,message.json,sub_client,h)
                                if(r == True):
                                    break
                            else:
                                text = mensajes[chat.idioma][41]
                                send_message(chatid,text)
                                h.close()
                                return

                            content = '/media %s' % (mediaName)
                        comando = chat.comandos[nombre]
                        comando.comandos.append(content)
                        h.addChatComand(comando.id,comando.comandos)
                        text = mensajes[chat.idioma][43] % (nombre)
                    elif(content):
                        if(content[0:2] == './'):
                            content = content[1:]
                        if(content[0] == '/' or (content[0] == '*' and content[-1] == '*') ):
                            comando = chat.comandos[nombre]
                            comando.comandos.append(content)
                            h.addChatComand(comando.id,comando.comandos)
                            text = mensajes[chat.idioma][701]
                        else:
                            text = mensajes[chat.idioma][42]
                    h.close()
                    send_message(chatid,text)
            elif(commandid == 8): #alias
                if(len(usersid) == 1 ):
                    if(replyuid != usersid[0]):
                        m = m[m.find("‬‭")+2:].lstrip()
                    if(usersid[0] == client.profile.id and userid != ley):
                        send_message(chatid,mensajeid=45)
                    elif(usersid[0] in bots and userid != ley):
                        send_message(chatid,mensajeid=44)                                    
                    else:
                        print("alias " + m)
                        user2 = getUser(usersid[0])
                        user2.alias = m
                        try:
                            h.connect()
                            h.userAlias(m,usersid[0])
                            addLogro(chat,userid,8,h)
                        except:
                            send_message(chatid,mensajeid=46)
                        h.close()
                else:
                    if(userid == ley):
                        user.alias = m
                        try:
                            h.connect()
                            h.userAlias(m,userid)
                        except:
                            send_message(chatid,mensajeid=46)
                        h.close()
                    else:
                        send_message(chatid,mensajeid=47)
            elif(commandid == 9): #anime
                if(m):
                    r= buscarAnime(chatid,m,client,idioma=chat.idioma)
                    if(r == 'h'):
                        addLogro(chat,userid,9)
                else:
                    send_message(chatid,mensajeid=48)
            elif(commandid == 10): #antispam
                if(len(content) < 2):
                    with open('ayuda/%s/comandos/antispam.txt' % (chat.idioma)) as e:
                        send_message(chatid,e.read())
                else:
                    if(content[1] == 'links'):
                        if(chatid in spamTextChat):
                            spamTextChat[chatid].append('aminoapps.com/p')
                        else:
                            spamTextChat[chatid] = ['aminoapps.com/p']
                        send_message(chatid,mensajeid=690)
                    elif(content[1] == palabras['imagenes']):
                        spamImagenesChat[chatid] = True
                        send_message(chatid,mensajeid=49)
                    elif(content[1] == 'stickers'):
                        spamStickersChat[chatid] = True
                        send_message(chatid,mensajeid=50)
                    elif(content[1] == palabras['texto']):
                        if(len(content) < 3):
                            text = mensajes[chat.idioma][51] + '\n'
                            text += mensajes[chat.idioma][52]
                            send_message(chatid,text)
                        else:
                            if(chatid in spamTextChat):
                                spamTextChat[chatid].append(' '.join(content[2:]))
                            else:
                                spamTextChat[chatid] = [' '.join(content[2:])]
                    elif(content[1] == 'flood'):
                        if(len(content) != 3 or not content[2].isdigit()):
                            text = mensajes[chat.idioma][53] + '\n'
                            text += mensajes[chat.idioma][54]
                            send_message(chatid,text)
                        else:
                            spamRepetidosChat[chatid] = int(content[2])
                            send_message(chatid,mensajeid=693,args=(int(content[2])))
                    elif(content[1] == 'no' or content[1] == 'desactivar'):
                        if(chatid in spamImagenesChat):
                            spamImagenesChat[chatid] = False
                        if(chatid in spamStickersChat):
                            spamStickersChat[chatid] = False
                        if(chatid in spamRepetidosChat):
                            spamRepetidosChat[chatid] = 0
                        if(chatid in spamTextChat):
                            spamTextChat[chatid] = []
                        send_message(chatid,mensajeid=661)
                    else:
                        with open('ayuda/%s/comandos/antispam.txt' % (chat.idioma)) as e:
                            send_message(chatid,e.read())
            elif(commandid == 11): #anuncio
                if(m != None):
                    sub_client.edit_chat(chatId=chatid,announcement=m,pinAnnouncement=True)
                    delete_message(chatId=chatid,messageId=id,sub_client=sub_client)
                else:
                    send_message(chatid,mensajeid=55)
            elif(commandid == 177 or commandid == 12): #apagar #desactivar
                try:
                    h.connect()
                    h.botstate(0,0,comid,0,chatid)
                except:
                    PrintException()
                h.close()
                chatStates[chatid] = 0
                if(chat.idioma != 'es'):
                    send_message(chatid,mensajeid=56)
                else:
                    send_message(chatid,comando[:-1] + "ndo bot")
            elif(commandid == 13): #app
                if(len(content) < 2):
                    send_message(chatid,mensajeid=57)
                elif(content[1] == 'chat'):
                    if(bots[client.profile.id]['owner'] == userid or userid == ley):
                        try:
                            h.connect()
                            h.chatUser(chatid,userid)
                        except:
                            PrintException()
                        h.close()
                        send_message(chatid,mensajeid=58)
                    else:
                        send_message(chatid,mensajeid=59)
            elif(commandid == 14): #asesino
                modoAsesino[chatid] = not modoAsesino.get(chatid,False)
            elif(commandid == 15): #ayuda
                addLogro(chat,userid,10)
                if(len(content) == 1):
                    mostrarAyuda(chatid,idioma=chat.idioma)
                elif(len(content) == 2):
                    cid = comandosIdioma[chat.idioma].get(content[1],0)
                    if(cid):
                        mostrarAyuda(chatid,commandid=cid,idioma=chat.idioma)
                    else:
                        mostrarAyuda(chatid,tipo=content[1],idioma=chat.idioma)

            elif(commandid == 16): #audio
                audios = os.listdir('audios')
                audios = [i for i in audios if i.endswith('.aac')]
                if(len(content) < 2):
                    i = random.randint(0,38)
                    send_audio(chatid,'audios/' + audios[i])
                    try:
                        h.connect()
                        r = h.escucharAudio(userid,i)
                        if(r == 39):
                            addLogro(chat,userid,11,h)
                    except:
                        PrintException()
                    h.close()
                elif(content[1].isdigit()):
                    n = int(content[1])-1
                    if(n >= len(audios) ):
                        send_message(chatid,mensajeid=60)
                    else:
                        channel = get_channel(chatid)
                        send_audio(chatid,'audios/' + audios[n])
                        try:
                            h.connect()
                            r = h.escucharAudio(userid,n)
                            if(r == 39):
                                addLogro(chat,userid,11,h)
                        except:
                            PrintException()
                        h.close()
                else:
                    send_message(chatid,mensajeid=61)
            elif(commandid == 17): #audios 
                audios = os.listdir('audios')
                audios = [i for i in audios if i.endswith('.aac')]
                audios = [i[:i.rfind('.')] for i in audios]

                text = mensajes[chat.idioma][62] + '\n'
                for i,a in enumerate(audios,1):
                    text += '%d. %s\n' % (i,a)
                r = to_private_chat(userid,text,client,comid)
                if(r):
                    send_message(chatid,mensajeid=637,args=getNickname(userid,sub_client))
                else:
                    send_message(chatid,mensajeid=638,args=(getNickname(userid,sub_client)))
            elif(commandid == 18): #autorizados
                if(bot['public']):
                    send_message(chatid,mensajeid=63)
                    return
                if(not autorizados):
                    send_message(chatid,mensajed=64)
                    return
                text = mensajes[chat.idioma][65] + "\n"
                for u in autorizados:
                    text += '%s\n' % (getNickname(u,sub_client))
                send_message(chatid,text)
            elif(commandid == 19): #autorizar
                if(bot['public']):
                    send_message(chatid,mensajeid=66)
                    return
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=67)
                    return
                if(not usersid):
                    send_message(chatid,mensajeid=68)
                for u in usersid:
                    if(u in autorizados):
                        send_message(chatid,mensajeid=69,args=(getNickname(u,sub_client)))
                        continue
                    h.close()
                    send_message(chatid,mensajeid=70,args=(getNickname(u,sub_client),bot['name']))
                    autorizados.append(u)
                chat.autorizados[client.profile.id] = autorizados 
                try:
                    h.connect()
                    h.userAutorizadosBotChat(chatid,chat.autorizados)
                except:
                    PrintException()

            elif(commandid == 20): #ban
                for u in usersid:
                    if(u == host):
                        send_message(chatid,mensajeid=71)
                    elif(u in get_cohosts(chatid,comid,new=True)):
                        send_message(chatid,mensajeid=72)
                    elif(u == ley):
                        send_message(chatid,mensajeid=73)
                    else:
                        r = sub_client.kick(u,chatid,False)
                        if(r != 200):
                            if(client.profile.id not in get_cohosts(chatid,comid,new=True)):
                                send_message(chatid,mensajeid=74)
            elif(commandid == 21): #banchat
                if(len(content) < 2):
                    send_message(chatid,mensajeid=145)
                else:
                    reason = ''
                    if(len(content) > 2):
                        reason = ' '.join(content[2:])
                    try:
                        h.connect()
                        h.banChat(content[1],reason)                
                    except:
                        PrintException()
                    h.close()
                    bannedChats[content[1]] = reason
            elif(commandid == 22): #banuser 
                if(len(content) < 2):
                    send_message(chatid,mensajeid=146)
                else:
                    reason = ''
                    if(usersid):
                        if('@' not in allContent):
                            reason = m
                        try:
                            h.connect()

                            for u in usersid:
                                h.banUser(u,reason)
                                bannedUsers[u] = reason
                        except:
                            PrintException()
                        h.close()
                    else:
                        if(len(content) > 2):
                            reason = ' '.join(content[2:])
                        try:
                            h.connect()
                            h.banUser(content[1],reason)
                        except:
                            PrintException()
                        h.close()
                        bannedUsers[content[1]] = reason
            elif(commandid == 23): #bio 
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=67)
                else:
                    if(m):
                        sub_client.edit_profile(content=m)
                    else:
                        send_message(chatid,mensajeid=75)
            elif(commandid == 24): #borrar 

                if(replyid):
                    r = delete_message_thread(chatId=chatid,messageId=replyid,sub_client=sub_client)
                    if(r != 200):
                        send_message(chatid,mensajeid=76)
                else:
                    send_message(chatid,mensajeid=77)
            elif(commandid == 25): #borrarM 
                borrarMedia(chatid)
            elif(commandid == 26): #borrarN 
                if(len(content) < 2 or not content[1].isdigit()):
                    send_message(chatid,mensajeid=78)
                else:
                    borrarN(chatid,int(content[1]))
            elif(commandid == 27): #borrarU 
                if(usersid):
                    for u in usersid:
                        borrarDeUsuario(chatid,u)
                else:
                    send_message(chatid,mensajeid=79)
            elif(commandid == 28): #bot 
                h.connect()
                changeBot(chatid,comid,client,userid,content,m,h,idioma=chat.idioma)
                h.close()
            elif(commandid == 29): #bots 
                h.connect()
                botsComunidad = h.loadBotsCommunity(comid)
                h.close()
                if(botsComunidad):
                    text = mensajes[chat.idioma][609]+ '\n'
                    for b in botsComunidad:
                        if(b not in bots):
                            continue
                        bot = bots[b]
                        if( (bot['public'] == 1 or bot['owner'] == userid) and not bot['muted'] ):
                            text += '%s: %s\n' % (bot['name'],bot['description'])
                    send_message(chatid,text)
                text = ''
                if(True):
                    text += '\n'+mensajes[chat.idioma][80]+'\n'
                    for bot in bots.values():
                        if(bot['userid'] in botsComunidad):
                            continue
                        if( (bot['public'] == 1 or bot['owner'] == userid) and not bot['muted'] ):
                            text += '%s: %s\n' % (bot['name'],bot['description'])
                
                send_message(chatid,text)

            elif(commandid == 30): #bug 
                if(m == None):
                    send_message(chatid,mensajeid=81)
                else:
                    chatname = get_title(chatid,comid)
                    text = 'Bug reportado en el chat ndc://x%d/chat-thread/%s\n' % (comid,chatid)
                    text += 'Por: '+ getTrueNickname(userid,sub_client) + ' ndc://x%d/user-profile/%s\n' % (comid,userid)
                    text += m
                    send_botgroup(text)
                    send_message(chatid,mensajeid=82)
                    addLogro(chat,userid,41)
            elif(commandid == 31): #br 
                if(role != 100 and role != 102):
                    send_message(chatid,mensajeid=83)
                    return
                if(len(content) < 2):
                    send_message(chatid,mensajeid=84)
                    return
                h.connect()
                roles = h.loadRolesComunidad(comid)
                for rid,r in roles.items():
                    if(r[0] == m):
                        send_message(chatid,mensajeid=85,args=(m) )
                        users = h.loadUsersConRole(rid)
                        for u in users: 
                            sub_client.remove_title(u,r[0])
                            h.deleteUserRole(u,rid)
                        h.deleteRoleComunidad(rid)
                        send_message(chatid,mensajeid=86,args=(m))
                        h.close()
                        return
                h.close()
                send_message(chatid,mensajeid=87,args=(m))
            elif(commandid == 32): #cancelar
                if(traducirDetectarUsers.get(chatid,[]) ):
                    traducirDetectarUsers[chatid] = []
                    send_message(chatid,mensajeid=88)
                if(chatid in continuarRepetir):
                    continuarRepetir[chatid] = False
                if(chatid in cancelarLimpieza):
                    cancelarLimpieza[chatid] = True
            elif(commandid == 33): #carcel
                if(userid not in countCarcel):
                    countCarcel[userid] = 0
                if(usersid):
                    if(len(usersid) > 3):
                        usersid = usersid[:3]
                        send_message(chatid,mensajeid=14)
                    for u in usersid:
                        countCarcel[userid] += 1
                        jail(chatid,u,client,chat.idioma)
                    if(countCarcel[userid] > 10):
                        addLogro(chat,userid,33)
                else:                           
                    send_message(chatid,mensajeid=89)
            elif(commandid == 34): #cb
                if(len(content) < 2):
                    send_message(chatid,mensajeid=90)
                else:
                    comando = m
                    h.connect()
                    h.comandoBienvenida(chatid,comando)
                    chat.comandosBienvenida = h.loadComandosBienvenida(chatid)
                    h.close()
                    send_message(chatid,mensajeid=91,args=(comando))

            elif(commandid == 35): #cbr
                if(len(content) < 2 or not content[1].isdigit()):
                    send_message(chatid,mensajeid=92)
                    if(chat.comandosBienvenida):
                        text = mensajes[chat.idioma][93]+'\n'
                        for id,c in chat.comandosBienvenida.items():
                            text += "%d. %s\n" % (id,c)
                        send_message(chatid,text)
                    else:
                        send_message(chatid,mensajeid=94)
                else:
                    id = int(content[1])
                    if(id in chat.comandosBienvenida):
                        h.connect()
                        t = h.removeComandoBienvenida(id)
                        h.close()
                        chat.comandosBienvenida.pop(id)
                        send_message(chatid,mensajeid=95)
                    else:
                        send_message(chatid,mensajeid=96)
            elif(commandid == 36): #cd
                lines = allContent.split('\n')
                c1 = lines[0].split(' ')
                print(c1)
                if(len(c1) != 3 or not c1[1].isdigit() or not c1[2].isdigit()):                                
                    send_message(chatid,mensajeid=97,args=('\n'))
                elif(len(lines) < 2):
                    send_message(chatid,mensajeid=98)
                else:
                    desde = int(c1[1])
                    hasta = int(c1[2])
                    comando = '\n'.join(lines[1:])
                    h.connect()
                    h.comandoDonacion(chatid,comando,desde,hasta)
                    chat.comandosDonacion = h.loadComandosDonacion(chatid)
                    h.close()
                    send_message(chatid,mensajeid=99)
            elif(commandid == 37): #cdr
                if(len(content) != 2 or not content[1].isdigit()):
                    text = mensajes[chat.idioma][100]+'\n'
                    for c,v in chat.comandosDonacion.items():
                        text += mensajes[chat.idioma][101] %(c,v[0],'\n',v[1],v[2],'\n')
                    send_message(chatid,text)
                else:
                    commandId = int(content[1])
                    if(commandId in chat.comandosDonacion):
                        chat.comandosDonacion.pop(commandId)
                        h.connect()
                        h.removeComandoDonacion(commandId)
                        h.close()
                        send_message(chatid,mensajeid=102)
                    else:
                        text = mensajes[chat.idioma][96]+'\n'

                        for c,v in chat.comandosDonacion.items():
                            text += mensajes[chat.idioma][101] %(c,v[0],'\n',v[1],v[2],'\n')
                        send_message(chatid,text)
            elif(commandid == 38): #chatid
                send_message(chatid,chatid)
            elif(commandid == 39): #chica
                offFilter = False
                if(chatid in filters and not filters[chatid]):
                    offFilter = True
                buscarChica(chatid,m,idioma=chat.idioma,ecchi=ecchi,offFilter=offFilter)
            elif(commandid == 40): #coa
                host = get_host(chatid,comid,new=True)
                if(len(content) < 2):
                    send_message(chatid,mensajeid=103)
                elif(host != ley and host not in bots):
                    send_message(chatid,mensajeid=104)
                elif(content[1] == palabras['dar']):
                    if(opLevel >= 3):
                        for u in usersid:
                            metercoa(chatid,comid,u,host)

                    else:
                        send_message(chatid,mensajeid=105)
                elif(content[1] == palabras['quitar']):
                    if(opLevel >= 3):
                        for u in usersid:
                            sacarcoa(chatid,comid,u,host)
                    else:
                        send_message(chatid,mensajeid=106)
                
                elif(content[1] == palabras['dame']):
                    metercoa(chatid,comid,userid,host)

                elif(content[1] == palabras['soltar']):
                    sacarcoa(chatid,comid,userid,host)
                    send_message(chatid,mensajeid=107)
            elif(commandid == 41): #coas
                text = palabras['coas'] + ':\n'
                cohosts = get_cohosts(chatid,comid,new=True)
                for c in cohosts:
                    text += '<$%s$>\n' % (getNickname(c,sub_client))
                sub_client.send_message(chatid,text,linkText=True,mentionUserIds=cohosts)
            elif(commandid == 42): #comandos
                if(len(content) >= 2):
                    if(content[1] in tipos_comandos[chat.idioma]):
                        text = mensajes[chat.idioma][15] % (content[1])
                        for c in ctipos[tipos_comandos[chat.idioma].index(content[1]) ]:
                            print(c)
                            cid = comandosMap[ c[1]]
                            if(comandos[cid] [2] > 0 and bot['public']):
                                continue
                            text += ' %s ' % (comandosReverseMap[chat.idioma][cid])
                        send_message(chatid,text)
                    else:
                        text = mensajes[chat.idioma][18] + '\n'
                        for i in tipos_comandos[chat.idioma][:15]:
                            text += i + ', ' 
                        text = text[:-2]
                        send_message(chatid,text)
                    return
                if(chat.comandos):
                    text = mensajes[chat.idioma][16] + '\n'
                    for c in chat.comandos:
                        nick = getNickname(chat.comandos[c].userid,sub_client)
                        text += c
                        if(nick != ''):
                            text += ' ' + mensajes[chat.idioma][19]  % (nick) + '\n'
                        else:
                            text += '\n'
                        if(chat.comandos[c].descripcion != None and chat.comandos[c].descripcion != ''):
                            text += mensajes[chat.idioma][19] % (chat.comandos[c].descripcion )   + '\n'
                        text +='\n'    
                    send_message(chatid,text)
                text = mensajes[chat.idioma][18] + '\n'
                for i in tipos_comandos[chat.idioma][:15]:
                    text += i + ', '

                text = text[:-2]
                text += '\n\n' + mensajes[chat.idioma][634].replace('\\','\n')
                send_message(chatid,text)

                text = ''
                commandlist = []
                for ct in ctipos:
                    if(ct >= 17):
                        continue
                    text += mensajes[chat.idioma][15] % (tipos_comandos[chat.idioma][ct])
                    for c in ctipos[ct]:
                        cid = comandosMap[ c[1]]
                        if(comandos[cid] [2] > 0 and bot['public']):
                            continue
                        if(comandos[cid][2] > 1):
                            continue
                        cname = comandosReverseMap[chat.idioma][cid]
                        if(cname in commandlist or cname == 'null'):
                            continue
                        commandlist.append(cname)
                        text += ' %s ' % (cname)

                    text += '\n\n\n'
                if(chatThread['type'] != 2 and chat.idioma == 'es'):
                    # text += 'Para el bot ecchi: /ecchi'   
                    send_message(chatid,'coger, gemir, nalgada, tentar, deseo, cum, crema, secuestrar',client=ecchibot['client'])      

                r = to_private_chat(userid,text,client,comid)
                if(r):
                    send_message(chatid,mensajeid=635,args=(getNickname(userid,sub_client)))
                else:
                    send_message(chatid,mensajeid=636,args=(getNickname(userid,sub_client)))

            elif(commandid == 43): #compatibilidad
                if(len(usersid)  == 1):
                    if(usersid[0] in bots):
                        send_message(chatid,mensajeid=147)
                    else:
                        send_message(chatid,random.choice(compatibilidad[chat.idioma]))
                else:
                    send_message(chatid,mensajeid=36)
            elif(commandid == 44): #config
                # with open('chatsettings.txt','r') as h:
                #     text = h.read()
                # send_message(chatid,text)
                text = mensajes[chat.idioma][108]+'\n'
                settings = chat.settings
                text += '%s: %s\n\n' % (palabras['prefijo'],settings['prefijo'])
                if(bot['public'] == 0 or comid == leyworld):
                    text += '%s: %s\n\n' % (palabras['voz'],settings['voz'])
                text += '%s: %d\n\n' % (palabras['espera'],settings['espera'])
                text += '%s: %d\n\n' % (palabras['maxstrikes'],settings['maxStrikes'])
                text += '%s: %s\n\n' % (palabras['idioma'],settings['idioma'])
                text += 'volume: %s\n\n' % (settings['volume'])
                if(settings['tipoMensaje'] == 100):
                    text += '%s: %s\n\n' % (palabras['tipoMensaje'],palabras['especial'])
                else:
                    text += '%s: %s\n\n' % (palabras['tipoMensaje'],palabras['normal'])

                if(settings['agradecer']):
                    text += '%s: %s\n\n' % (palabras['agradecer'],palabras['si'])
                else:
                    text += '%s: %s\n\n' % (palabras['agradecer'],palabras['no'])
                if(settings['otrosBots']):                    
                    text += '%s: %s\n\n' % (palabras['otrosBots'],palabras['si'])
                else:
                    text += '%s: %s\n\n' % (palabras['otrosBots'],palabras['no'])
                if(settings['asteriscos']):                    
                    text += '%s: %s\n\n' % (palabras['asteriscos'],palabras['si'])
                else:
                    text += '%s: %s\n\n' % (palabras['asteriscos'],palabras['no'])
                if(settings['sonidos']):                    
                    text += '%s: %s\n\n' % (palabras['sonidos'],palabras['si'])
                else:
                    text += '%s: %s\n\n' % (palabras['sonidos'],palabras['no'])
                if(settings['bienvenidas']):                    
                    text += '%s: %s\n\n' % (palabras['bienvenidas'],palabras['si'])
                else:
                    text += '%s: %s\n\n' % (palabras['bienvenidas'],palabras['no'])
                if(settings['despedidas']):                    
                    text += '%s: %s\n\n' % (palabras['despedidas'],palabras['si'])
                else:
                    text += '%s: %s\n\n' % (palabras['despedidas'],palabras['no'])

                text += '%s: %s\n\n' % (palabras['modo'],modos[chat.idioma][settings['modo']])
                if(chat.idioma == 'es'):
                    if(settings['todos']):                    
                        text += '%s: %s\n\n' % ('todos',palabras['si'])
                    else:
                        text += '%s: %s\n\n' % ('todos',palabras['no'])

                send_marco(chatid,text,chat.mup,chat.mdown,chat.settings['tipoMensaje'])
                # elif(len(content) < 3):
                #     send_message(chatid,"uso: /config [configuracion] [nuevo valor]: cambiar el valor de una configuracion del chat")
                # else:
                #     if(content[1] not in chat.settings):
                #         send_message(chatid,mensajeid=148)
                #     else:
                #         send_message(chatid,'%s actualizado a %s' % (content[1],content[2]))

            elif(commandid == 45): #copiar
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=67)
                else:
                    if(not usersid):

                        send_message(chatid,mensajeid=109)
                        js = sub_client.get_user_info(userid).json
                    else:
                        js = sub_client.get_user_info(usersid[0]).json
                    js['extensions'] = js.get('extensions',{})
                    if(len(content) > 2):
                        if(content[1] == 'icon'):
                            sub_client.edit_profile(icon=js['icon'])
                            return
                        elif(content[1] == palabras['bio']):
                            if(not js['extensions']):
                                sub_client.edit_profile(content=js['content'],mediaList=js['mediaList'])
                            elif('style' not in js['extensions']):
                                sub_client.edit_profile(content=js['content'],mediaList=js['mediaList'],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
                            elif('backgroundMediaList' in js['extensions']['style'] ):
                                sub_client.edit_profile(content=js['content'],mediaList=js['mediaList'],backgroundImage=js['extensions']['style']['backgroundMediaList'][0][1],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
                            else:
                                sub_client.edit_profile(content=js['content'],mediaList=js['mediaList'],backgroundColor=js['extensions']['style']['backgroundColor'],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
                            return
                        elif(content[1] == palabras['burbuja']):

                            sub_client.purchase_bubble(nickname=js['1e6ee751-012c-4426-b7a6-6bc1ecad48ee'])
                            return
                        elif(content[1] == 'nickname'):
                            sub_client.edit_profile(nickname=js['nickname'])
                            return
                    if(not js['extensions']):
                        sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'])
                    elif('style' not in js['extensions']):
                        sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
                    elif('backgroundMediaList' in js['extensions']['style'] ):
                        sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],backgroundImage=js['extensions']['style']['backgroundMediaList'][0][1],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
                    else:
                        sub_client.edit_profile(icon=js['icon'],nickname=js['nickname'],content=js['content'],mediaList=js['mediaList'],backgroundColor=js['extensions']['style']['backgroundColor'],defaultBubbleId=js['extensions'].get('defaultBubbleId'))
                    send_message(chatid,mensajeid=110)
            elif(commandid == 46 or commandid == 47): #corresponder #corresponde
                r = responder_interacciones("corresponder",chat,userid,sub_client,idioma=chat.idioma)
                if(not r):
                    send_interaccion(chatid,"corresponder",userid,usersid,sub_client,idioma=chat.idioma,ecchi=ecchi)
                else:
                    addLogro(chat,userid,14)
            elif(commandid == 48): #crear
                ln = allContent.split('\n')
                con = ln[0].split(' ')
                if(len(con) < 2) :
                    send_message(chatid,mensajeid=111)                          
                elif(replyid == None):
                    send_message(chatid,mensajeid=112)
                else:
                    nombre = con[1].lower()
                    if(nombre in chat.comandos or nombre in comandosIdioma[chat.idioma] ):
                        send_message(chatid,mensajeid=113)
                        return
                    descripcion = ""
                    if(len(ln) >= 2):
                        descripcion = '\n'.join(ln[1:])
                    if(nombre in comandosIdioma[chat.idioma]):
                        text = mensajes[chat.idioma][113]
                    elif(nombre in chat.comandos):
                        text = mensajes[chat.idioma][113]
                    else:
                        message = sub_client.get_message_info(chatid,replyid)
                        print(message)
                        creado = False
                        content = message.json.get('content',None)
                        mediaValue = message.json.get('mediaValue',None)
                        print(content,mediaValue)
                        h.connect()
                        if(not content and mediaValue):
                            if(saveMedia(chatid,m,message.json,sub_client,h)):
                                content = '/media %s' % (m)
                            elif(saveMedia(chatid,m + ' comando',message.json,sub_client,h)):
                                content = '/media %s' % (m + ' comando')
                            else:
                                text = mensajes[chat.idioma][114]
                                h.close()
                                return
                            h.chatComand(nombre,content,descripcion,userid,chatid)
                            cid = h.loadCommandId(nombre,chatid)
                            chat.comandos[nombre] = Comando(cid,nombre,[content],userid,descripcion)
                            text = mensajes[chat.idioma][115] % (nombre)
                            creado = True
                        elif(content):
                            if(content[0:2] == './'):
                                content = content[1:]
                            if(content[0] == '/' or (content[0] == '*' and content[-1] == '*') ):
                                h.chatComand(nombre,content,descripcion,userid,chatid)
                                cid = h.loadCommandId(nombre,chatid)
                                chat.comandos[nombre] = Comando(cid,nombre,[content],userid,descripcion)
                                text = mensajes[chat.idioma][115] % (nombre)
                                creado = True
                            else:
                                mensaje = m.strip()
                                text  = mensajes[chat.idioma][116] % (mensaje)
                                sre = re.sub(
                                    r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                                    unicodedata.normalize( "NFD", mensaje), 0, re.I
                                    )
                                mensaje = unicodedata.normalize('NFKC',sre).lower()

                                respuestas[chatid][mensaje] = [i for i in content.split('|')]
                                h.respuestas(chatid,respuestas[chatid])
                                creado = True
                    send_message(chatid,text)
                    h.close()
                    return creado
            elif(commandid == 49): #crema
                values = getMediaValues(chatid,None,usersid,replyid)
                for u in usersid:
                    send_message(chatid,mensajeid=117,args=(getNickname(userid,sub_client),getNickname(u,sub_client)),ecchi=ecchi )
                if(values):
                    for v in values:        
                        cum(chatid,v,client,ecchi=ecchi)
                else:                           
                    send_message(chatid,mensajeid=118,ecchi=ecchi)
            elif(commandid == 50): #cum
                if(userid not in cumcount):
                    cumcount[userid] = 0
                if(cumcount[userid] >= 10):
                    addLogro(chat,userid,29)
                values = getMediaValues(chatid,None,usersid,replyid)
                if(len(usersid) > 3):
                    usersid = usersid[:3]
                    send_message(chatid,mensajeid=14,ecchi=ecchi)
                    
                for u in usersid:
                    send_message(chatid,mensajeid=119,args=(getNickname(userid,sub_client),getNickname(u,sub_client)),ecchi=ecchi)
                if(values):
                    for v in values:
                        cumcount[userid] += 1
                        cum(chatid,v,client,ecchi=ecchi)
                else:                           
                    send_message(chatid,mensajeid=120,ecchi=ecchi)
            elif(commandid == 51): #curador
                if(not isLeader(userid,sub_client)):
                    send_message(chatid,mensajeid=83)
                    return                                
                if(len(content) > 1 and content[1].startswith('http://aminoapps.com/p/')):
                    response = requests.get(f"{client.api}/g/s/link-resolution?q={content[1]}", headers=aminoHeaders.Headers(sid=client.sid).headers)
                    js = json.loads(response.text)
                    if(js['api:statuscode'] == 107):
                        send_message(chatid,mensajeid=121)
                        return
                    extensions = js['linkInfoV2']['extensions']
                    r = extensions.get('linkInfo',None)
                    if(not r):
                        send_message(chatid,mensajeid=122)
                        return
                    targetUserid = r['objectId']
                    if(r['objectType'] != 0):
                        send_message(chatid,mensajeid=123)
                        return
                    usersid = [targetUserid]  
                if(usersid):
                    acm = client.acm(comid)
                    for u in usersid:
                        r = acm.promote(u,'curator')
                        if(r == 200):
                            send_message(chatid,mensajeid=124,args=(getTrueNickname(u,sub_client)) )
                        else:
                            send_message(chatid,mensajeid=125,args=(getTrueNickname(u,sub_client)))
                else:
                    send_message(chatid,mensajeid=126)
            elif(commandid == 52): #danbooru
                offFilter = False
                if(chatid in filters and not filters[chatid]):
                    offFilter = True
                buscarDanbooru(chatid,m,idioma=chat.idioma,ecchi=ecchi,offFilter=offFilter)
            elif(commandid == 53): #debug
                if(len(content) < 2):
                    send_message(chatid,mensajeid=127)
                elif(content[1] == 'on'):
                    debug[chatid] = True
                elif(content[1] == 'off'):
                    debug[chatid] = False
                elif(content[1] == 'jugar'):
                    jugar(chatid,content[2],comid,client.profile.id,debug=True)

                elif(content[1] == 'safe'):
                    if(userid != ley):
                        return
                    safeMessageType[0] = int(content[2])
            elif(commandid == 54): #decir
                if(m):
                    if('onichan' in m):
                        addLogro(chat,userid,31)
                    if(len(m) > 200):
                        send_message(chatid,mensajeid=128)
                    else:
                        voz = chat.settings['voz']
                        if(bot['public']):
                            decir(chatid,m,'google',chat.idioma)
                        else:
                            decir(chatid,m,voz,chat.idioma)
                else:
                    send_message(chatid,mensajeid=129)
            elif(commandid == 55): #dejar
                if(len(content) > 1):
                    send_message(chatid,mensajeid=130,args=(getNickname(userid,sub_client),' '.join(content[1:])) )
            elif(commandid == 56): #delete
                if(m != None):
                    r = False

                    try:
                        h.connect()
                        r = eraseMedia(userid,m)
                    except:
                        PrintException()
                    h.close()
                    if(r):
                        send_message(chatid,mensajeid=131,args=m)
                    else:
                        send_message(chatid,mensajeid=132,args=m)

                else:
                    send_message(chatid,mensajeid=133)
            elif(commandid == 57): #deop
                for u in usersid:
                    if(u == host):
                        send_message(chatid,mensajeid=134)
                    elif(u == ley):
                        send_message(chatid,mensajeid=135)
                    elif(u in get_cohosts(chatid,comid) and user.id != host):
                        send_message(chatid,mensajeid=136)
                    else:
                        h.connect()
                        if(u in chat.ops):
                            if(opLevel > chat.ops[u] or userid == ley):
                                chat.ops.pop(u)
                                h.opChat(chatid,chat.ops)
                        h.close()
            elif(commandid == 58): #descripcion
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=67)
                else:
                    if(m):
                        h.connect()
                        h.descripcionBot(client.profile.id,m)
                        h.close()
                        bots[client.profile.id]['description'] = m
                        send_message(chatid,mensajeid=137)
                    else:
                        send_message(chatid,mensajeid=138)
            elif(commandid == 59): #deshabilitar
                if(len(content) == 1):
                    send_message(chatid,mensajeid=139)
                else:
                    if(content[1] == palabras['de']):
                        c = content[2]
                        if(c in tipos_comandos[chat.idioma]):
                            send_message(chatid,mensajeid=696,args=(c))
                            h.connect()
                            text = mensajes[chat.idioma][697]
                            for c in ctipos[tipos_comandos[chat.idioma].index(c) ]:
                                print(c)
                                cid = comandosMap[ c[1]]
                                if(cid == 124 or cid == 59 or cid == 80):
                                    continue
                                opCustom[chatid][cid] = -1
                                h.customOP(chatid,opCustom[chatid])
                                text += ' ' + comandosReverseMap[chat.idioma][cid]
                            send_message(chatid,text)
                    else:
                        if(len(content) > 2):
                            h.connect()
                            text = mensajes[chat.idioma][697]
                            for c in content[1:]:
                                if(c in comandosIdioma[chat.idioma]):
                                    c = comandosIdioma[chat.idioma][c]
                                    if(c == 124):
                                        send_message(chatid,mensajeid=140)
                                        continue

                                    text += ' ' + comandosReverseMap[chat.idioma][c]
                                    opCustom[chatid][c] = -1
                                    h.customOP(chatid,opCustom[chatid])
                                    if(c == 80):
                                        addLogro(chat,userid,62,h)
                            addLogro(chat,userid,4,h)
                            send_message(chatid,text)
                            h.close()
                        else:
                            c = content[1]
                            if(c not in comandosIdioma[chat.idioma]):
                                send_message(chatid,mensajeid=141)
                            else:
                                c = comandosIdioma[chat.idioma][c]
                                if(c == 124):
                                    send_message(chatid,mensajeid=140)
                                    return
                                send_message(chatid,mensajeid=142,args=content[1])
                                opCustom[chatid][c] = -1
                                h.connect()
                                h.customOP(chatid,opCustom[chatid])
                                addLogro(chat,userid,4,h)
                                if(c == 80):
                                    addLogro(chat,userid,62,h)
                                h.close()
            elif(commandid == 60): #desautorizar
                if(bot['public']):
                    if(userid != ley and userid != get_host(chatid,comid,new=True)): 
                        send_message(chatid,mensajeid=149)
                        return
                    h.connect()
                    h.botstate(2,0,comid,0,chatid)
                    h.close()
                    return

                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=150)
                    return
                if(not usersid):
                    h.connect()
                    h.desautorizarBotChat(client.profile.id,chatid)
                    h.close()
                    bot['autorizados'].remove(chatid)
                    send_message(chatid,mensajeid=345,args=(bot['name']))
                    return
                if(not autorizados):
                    send_message(chatid,mensajeid=151)
                    return
                for u in usersid:
                    if(u not in autorizados):
                        send_message(chatid,mensajeid=346,args=(getNickname(u,sub_client),bot['name'] ) )
                        continue                    
                    autorizados.remove(u)
                    send_message(chatid,mensajeid=347,args=(getNickname(u,sub_client),bot['name'] ))
                chat.autorizados[client.profile.id] = autorizados
                h.connect()
                h.userAutorizadosBotChat(chatid,chat.autorizados)
                h.close()
            elif(commandid == 61): #despedir
                if(usersid ):
                    for u in usersid:
                        despedir(chatid,'',chat.mup,chat.mdown,u)
                else:
                    despedir(chatid,mensajes[chat.idioma][348],chat.mup,chat.mdown)
            elif(commandid == 62): #discord
                pass
            elif(commandid == 63): #disponible
                text = mensajes[chat.idioma][349]+"\n"

                # text = ''
                commandlist = []
                for ct in ctipos:
                    if(ct >= 17):
                        continue
                    text += mensajes[chat.idioma][15] % (tipos_comandos[chat.idioma][ct])
                    for c in ctipos[ct]:
                        cid = comandosMap[ c[1]]
                        if(comandos[cid] [2] > 0 and bot['public']):
                            continue
                        if(comandos[cid][0] > opLevel):
                            continue
                        cname = comandosReverseMap[chat.idioma][cid]
                        if(cname in commandlist or cname == 'null'):
                            continue
                        commandlist.append(cname)
                        text += ' %s ' % (cname)
                    text += '\n\n\n'

                send_message(chatid,text)
            elif(commandid == 64): #dueño
                send_message(chatid,mensajeid=152)
                addLogro(chat,userid,28)
                r = ver(chatid,bot['owner'],chat,sub_client,idioma=chat.idioma)
                if(r == 225 or not r):
                    profile = client.get_user_info(bot['owner'])['userProfile']
                    sub_client.send_message(chatid,'[c]',embedType=0,embedTitle=profile['nickname'],embedContent=mensajes[chat.idioma][152])
                    # send_message(chatid,'ndc://x0/user-profile/%s' % (bot['owner']))

            elif(commandid == 65): #eliminar
                
                if(len(content) < 2):
                    send_message(chatid,mensajeid=153)                         
                else:
                    if(m.startswith('/')):
                        c = content[1][1:]
                        if(c in chat.comandos):
                            h.connect()
                            h.removeChatComand(chat.comandos[c].id)
                            h.close()
                            chat.comandos.pop(c)
                            send_message(chatid,mensajeid=350,args=(c))
                        else:
                            send_message(chatid,mensajeid=351,args=(content[1]))
                    else:
                        mlower = m.lower()
                        if(mlower in respuestas[chatid]):
                            respuestas[chatid].pop(mlower)
                            h.connect()
                            h.respuestas(chatid,respuestas[chatid])
                            h.close()
                            send_message(chatid,mensajeid=154)
                        else:
                            send_message(chatid,mensajeid=352,args=(m))
            elif(commandid == 66): #emision
                emision(chatid,content,idioma=chat.idioma)
            elif(commandid == 67): #endings
                endings(chatid,content,m,client,idioma=chat.idioma)
            elif(commandid == 68): #entrar
                if(len(content) > 1):

                    if(content[1] == 'en'):
                        send_message(chatid,mensajeid=371,args=(getNickname(userid,sub_client),' '.join(content[1:])) )
                    elif(content[1] in ['a','al']):
                        send_message(chatid,getNickname(userid,sub_client) + ' se a unido ' + ' '.join(content[1:]))
                    else:
                        send_message(chatid,mensajeid=371,args=(getNickname(userid,sub_client),' '.join(content[1:])) )
            elif(commandid == 69): #erase
                if(m):
                    if(eraseMedia(chatid,m)):
                        send_message(chatid,'borrado ' + m)
                    else:
                        send_message(chatid,'No se encontro ' + m)

                else:
                    send_message(chatid,mensajeid=155)                           

            elif(commandid == 70): #especial
                if(m):
                    delete_message(chatId=chatid,messageId=id,sub_client=sub_client)
                    send_marco(chatid,m,user.mup,user.mdown,tm=109)
                else:
                    send_message(chatid,mensajeid=156)
            elif(commandid == 71): #espera
                if(len(content) != 2 or not content[1].isdigit()):
                    send_message(chatid,mensajeid=157)
                else:
                    t = int(content[1])
                    chat.settings["espera"] = t
                    h.connect()
                    h.chatSettings(espera=t)
                    h.close()
            elif(commandid == 72): #esquivar
                r = responder_interacciones("esquivar",chat,userid,sub_client,chat.idioma)
                if(not r):
                    send_interaccion(chatid,"esquivar",userid,usersid,sub_client,idioma=chat.idioma,ecchi=ecchi)
                else:
                    addLogro(chat,userid,13)
                # if(r[0] == 'patear'):
                #     patear(chatid,r[1],client)
            elif(commandid == 73): #estadisticas
                if(len(content) < 2 or not content[1].isdigit):
                    send_message(chatid,mensajeid=158)
                else:
                    t = threading.Thread(target=getTotalActivity,args=(chatid,int(content[1])))
                    t.daemon = True
                    t.start()
            elif(commandid == 74): #exiliados
                t = sub_client.get_chat_thread(chatid,raw=True)['thread']['extensions']
                if('bannedMemberUidList' in t):
                    text = 'Exiliados:\n'
                    for u in t['bannedMemberUidList']:
                        text += '<$%s$>' % (getTrueNickname(u,sub_client)) + '\n'
                    sub_client.send_message(chatid,text,linkText=True,mentionUserIds=t['bannedMemberUidList'])
                else:
                    send_message(chatid,mensajeid=159)

            elif(commandid == 75): #fap
                addLogro(chat,userid,27)
                send_audio(chatid,'audios/Me voy a masturbar chao.aac',esperar=True)
                # send_imagen(chatid,'imgs/me_voy_a_masturbar_chau.jpeg',sanitized=True)
                if(chatThread['type'] == 2 and get_host(chatid,comid) != client.profile.id):
                    sub_client.leave_chat(chatid)
                else:
                    send_message(chatid,'%s ha dejado la conversacion.' % getTrueNickname(client.profile.id,sub_client),tm=100)
                sleep(5 + random.randint(1,10) )
                if(chatThread['type'] == 2 and get_host(chatid,comid) != client.profile.id):
                    sub_client.join_chat(chatid)
                else:
                    send_message(chatid,'%s se ha unido a la conversacion.' % getTrueNickname(client.profile.id,sub_client),tm=100)
                # send_imagen(chatid,'imgs/ya_me_masturbe_holi.jpeg',sanitized=True)
                send_audio(chatid,'audios/Ya me mastuber holi.aac',esperar=True)
            elif(commandid == 76 or commandid == 77): #fondo #fondos
                if(m == None):
                    if(comando == "fondos"):
                        ts = loadMedia(chatid,h)
                        if(not ts):
                            send_message(chatid,mensajeid=337)
                        else:
                            text = mensajes[chat.idioma][373]+'\n'
                            for t in ts:
                                if(t['type'] == 2 and not t[1].endswith('aac')):
                                    text += t['name'] + '\n'
                            send_message(chatid,text)
                    else:
                        link = get_backGround(chatid,sub_client)
                        r = nudeDetect(link)
                        if(r > 0.8):
                            send_message(chatid,mensajeid=160)
                        else:
                            send_text_imagen(chatid,mensajes[chat.idioma][372],link)
                else:
                    media = loadMedia(chatid,h)
                    if(m in media):
                        t = media[m]
                        filename = t['name']
                        ext = filename[filename.rfind('.')+1:]
                        if(t[1] != 2 or ext not in ['jpeg','jpg','png','gif']):
                            send_message(chatid,mensajeid=161)
                        else:
                            data = requests.get(filename).content
                            sub_client.upload_background(chatId=chatid,
                                data=data,tipo='image/' + ext)
                    else:
                        send_message(chatid,mensajeid=162)
            elif(commandid == 78): #funar
                if(chatThread['type'] != 2):
                    send_message(chatid,mensajeid=163)
                    return
                if(client.profile.id not in get_cohosts(chatid,comid,new=True) and client.profile.id != get_host(chatid,comid) ):
                    if(not isStaff(client.profile.id,sub_client)):
                        send_message(chatid,mensajeid=164)
                        return
                if(chatid not in funados):
                    funados[chatid] = []
                if(usersid):
                    addLogro(chat,userid,6)
                    for u in usersid:
                        funados[chatid].append(u)
                else:
                    send_message(chatid,mensajeid=165)
            elif(commandid == 79): #gif
                if(m):
                    send_link(chatid,getGif(m),sanitized=True)
                else:
                    send_message(chatid,mensajeid=166)
            elif(commandid == 80): #habilitar
                if(len(content) == 1):
                    send_message(chatid,mensajeid=167)
                else:
                    c = content[1]
                    if(c not in comandosIdioma[chat.idioma]):
                        send_message(chatid,mensajeid=168)
                    else:
                        c = comandosIdioma[chat.idioma][c]
                        custom = opCustom[chatid].get(c,-2)
                        if(comandos[c][0] == -1):
                            if(chatThread['type'] == 2):
                                userInfo = sub_client.get_user_info(userid,raw=True)['userProfile']
                                role = userInfo['role']
                                if((role >= 100 and role <= 102) or userid == ley or bots[client.profile.id]['owner'] == userid):
                                    send_message(chatid,mensajeid=387,args=content[1])

                                    opCustom[chatid][c] = 0
                                    h.connect()
                                    h.customOP(chatid,opCustom[chatid])
                                    h.close()
                                    if(role == 100 or role == 102):
                                        send_message(chatid,mensajeid=169)
                                else:
                                    send_message(chatid,mensajeid=170)
                            else:
                                send_message(chatid,mensajeid=374,args=content[1])
                                send_message(chatid,mensajeid=171)
                                opCustom[chatid][c] = 0
                                h.connect()
                                h.customOP(chatid,opCustom[chatid])
                                h.close()
                            return
                        if(c in comandosCom and comandosCom[c] == 0):
                            send_message(chatid,mensajeid=172)
                            return
                        if(custom != -1):
                            send_message(chatid,mensajeid=375,args=(content[1]))
                        else:
                            send_message(chatid,mensajeid=374,args=content[1])
                            opCustom[chatid].pop(c)
                            h.connect()
                            h.customOP(chatid,opCustom[chatid])
                            h.close()
            elif(commandid == 81): #hora
                if(len(content) == 2 and content[1] == palabras['todas']):
                    text = horas(True,idioma=chat.idioma)
                else:
                    text = horas(idioma=chat.idioma)
                send_message(chatid,text)
            elif(commandid == 82): #horoscopo
                text = mensajes[chat.idioma][35] % (getNickname(userid,sub_client)) + '\n'
                for key in horoscopo[chat.idioma]:
                    text += '%s %s\n\n' % (key,random.choice(horoscopo[chat.idioma][key][:-1]) )
                send_message(chatid,text)
            elif(commandid == 83): #icon
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=173)
                else:
                    if(replyid == None):
                        send_message(chatid,mensajeid=376)
                    else:
                        message = sub_client.get_message_info(chatid,replyid)
                        mediaValue = message.json['mediaValue']
                        t = message.json['type']
                        if(t == 100):
                            send_message(chatid,mensajeid=174)
                        elif(mediaValue):
                            sub_client.edit_profile(icon=mediaValue)
            elif(commandid == 84): #info
                addLogro(chat,userid,15)
                if(len(content) == 2):
                    info(chatid,content[1],idioma=chat.idioma,premium=(not bot['public']))
                else:
                    info(chatid,idioma=chat.idioma,premium=(not bot['public']) )
            elif(commandid == 85): #join
                if(chatid in channels):
                    leaveChannel(channels[chatid])
                    channels.pop(chatid)

                get_voice_chat_info_and_join(sockets[client.profile.id],chatid,comid)
            elif(commandid == 86): #juegos
                if(comid != leyworld):
                    mostrarJuegos(chatid,bot['public'])
                else:
                    mostrarJuegos(chatid,0)
            elif(commandid == 87): #jugar
                if(len(content) < 2):
                    send_message(chatid,mensajeid=175)
                    mostrarJuegos(chatid,bot['public'])
                else:
                    if(content[1] not in juegos):
                        send_message(chatid,mensajeid=2,args=(content[1],))
                    else:
                        if((bot['public'] and comid != leyworld) or content[1] == 'aop'):
                            # send_message(chatid,'no se puede jugar')
                            r = start_game(content[1],client.profile.id,chat)
                            if(not r):
                                send_message(chatid,'De momento no se puede jugar')
                            # admins = []
                            # for o in chat.ops:
                            #     if(chat.ops[o] > 0):
                            #         admins.append(o)
                            # if(not r):
                            #     send_message(chatid,'Error iniciando el juego %s' % (content[1]))
                        else:
                            jugar(chatid,content[1],comid,client.profile.id)
            elif(commandid == 88): #kick
                for u in usersid:
                    if(u == host):
                        send_message(chatid,mensajeid=176)
                    elif(u in get_cohosts(chatid,comid,new=True)):
                        send_message(chatid,mensajeid=177)
                    elif(u == 'your_uuid'):
                        send_message(chatid,mensajeid=178)
                    else:
                        r = sub_client.kick(u,chatid,True)
                        if(r != 200):
                            if(client.profile.id not in get_cohosts(chatid,comid,new=True)):
                                send_message(chatid,mensajeid=179)
            elif(commandid == 89): #kill
                if(usersid):
                    for u in usersid:
                        killUser(chatid,u,client)
                else:
                    send_message(chatid,mensajeid=180)
            elif(commandid == 90): #le
                    text = getNickname(userid,sub_client) + ' ' 
                    if(replyuid):
                        u = replyuid
                        text += allContent[1:] + ' a ' + getNickname(u,sub_client)
                    elif(len(usersid) == 1 ):
                        u = usersid[0]
                        text += allContent[1:]
                        text = text[:text.rfind('@')]
                        text += ' a ' + getNickname(u,sub_client)
                    else:
                        if(m):
                            text += m
                    send_message(chatid,text)
            elif(commandid == 91): #leave
                leave_voice_chat(sockets[client.profile.id],chatid,comid)
                if(chatid in channels):
                    leaveChannel(channels[chatid])
                    channels.pop(chatid)
            elif(commandid == 92): #letra
                if(chatid not in cacheLetras):
                    cacheLetras[chatid] = ['0']
                if(len(content) == 2 and content[1].isdigit()):
                    if(len(cacheLetras[chatid]) == 1 ):
                        send_message(chatid,mensajeid=181)
                    else:
                        l = letra(cacheLetras[chatid][int(content[1])] )
                        send_message(chatid,l)
                elif(len(content) == 1):
                    send_message(chatid,mensajeid=182)
                else:
                    r = buscar(m,chatid,idioma=chat.idioma)
                    if(r['result'] == 'letras'):
                        text = 'Resultados:\n'
                        i = 1
                        for l in r['letras']:
                            text += '%d. %s' % (i,l)
                    elif(r['result'] == 'lyrics'):
                        data = r['lyrics']
                        title = data['title']
                        text = data['lyrics']
                        author = data['author']
                        if('thumbnail' in data):
                            img = list(data['thumbnail'].values())[0]
                            img = urlAmino(img)
                        else:
                            img = None
                        if('links' in data):
                            link = list(data['links'].values())[0]
                        else:
                            link = None
                        if(len(text) > 2000):
                            text = text[:1997] + '...'
                        r = sub_client.send_message(chatid,message=text,embedType=0,embedLink=link,
                            embedContent=title,embedTitle=author,el=img)
                        print(r)
                    else:
                        send_message(chatid,mensajeid=681)
            elif(commandid == 93): #letraBienvenida
                if(len(content) < 2 or not content[1].isdigit()):
                    send_message(chatid,mensajeid=183)
                else:
                    bn = int(content[1])
                    if(bn < len(bienvenidas) and bn >= 0):
                        chat.bn = bn
                        h.connect()
                        h.chatBn(bn,chatid)
                        h.close()
            elif(commandid == 94): #llamada
                start_live_mode(sockets[client.profile.id],chatid,comid,1)
            elif(commandid == 95): #liberar
                sub_client.edit_chat(chatid,viewOnly=False)
            elif(commandid == 96): #lider
                if(not isLeader(userid,sub_client)):
                    send_message(chatid,mensajeid=184)
                    return
                if(len(content) > 1 and content[1].startswith('http://aminoapps.com/p/')):
                    response = requests.get(f"{client.api}/g/s/link-resolution?q={content[1]}", headers=aminoHeaders.Headers(sid=client.sid).headers)
                    js = json.loads(response.text)
                    if(js['api:statuscode'] == 107):
                        send_message(chatid,mensajeid=185)
                        return
                    extensions = js['linkInfoV2']['extensions']
                    r = extensions.get('linkInfo',None)
                    if(not r):
                        send_message(chatid,mensajeid=186)
                        return
                    targetUserid = r['objectId']
                    if(r['objectType'] != 0):
                        send_message(chatid,mensajeid=187)
                        return
                    usersid = [targetUserid]  
                if(usersid):
                    acm = client.acm(comid)
                    for u in usersid:
                        r = acm.promote(u,'leader')
                        if(r == 200):
                            send_message(chatid,mensajeid=377,args=(getTrueNickname(u,sub_client)))
                        else:
                            send_message(chatid,mensajeid=378,args=(getTrueNickname(u,sub_client)))
                else:
                    send_message(chatid,mensajeid=188)
            elif(commandid == 97): #load
                r = ""
                if(m == None):
                    saves = loadMedia(userid,h)

                    t = ""
                    for n in saves:
                        t += n + '\n'
                    send_message(chatid,"Saves:\n" + t) 
                else:
                    media = loadMedia(userid,h)
                    if(m in media):
                        t = media[m]
                        if(t['type'] == 0):
                            send_message(chatid,t['content'])
                        elif(t['type'] == 1):
                            send_link(chatid,link=t['content'])
                        elif(t['type'] == 2):
                            if(t['content'].endswith('.aac') or t['content'].endswith('.mp3')):
                                send_audio(chatid,t['content'])
                            else:
                                link = urlAmino(t['content'])
                                if(not link):
                                    return
                                send_link(chatid,link,sanitized=True)
                        elif(t[1] == 3):
                            send_sticker(chatid,t['content'])
                    else:
                        send_message(chatid,mensajeid=189)
            elif(commandid == 98): #loli
                offFilter = False
                if(chatid in filters and not filters[chatid]):
                    offFilter = True

                buscarLoli(chatid,m,idioma=chat.idioma,ecchi=ecchi,offFilter=offFilter)
            elif(commandid == 99): #lyrics
                try:
                    lyric = animelyrics.search_lyrics(m, show_title=True)
                    send_message(chatid,lyric)
                except animelyrics.MissingTranslatedLyrics as e:
                    send_message(chatid,mensajeid=190)
                except animelyrics.NoLyricsFound:
                    send_message(chatid,mensajeid=191)

            elif(commandid == 100): #manga
                manga(chatid,content,m,client,idioma=chat.idioma)
            elif(commandid == 101): #marco
                if(len(content) == 2 and content[1].isdigit()):
                    mn = int(content[1])
                    if(mn < len(marcos)   and mn >= 0):
                        chat.mup = mn
                        chat.mdown = mn
                        h.connect()
                        try:

                            h.chatMarcos(chat.mup,chat.mdown,chatid)
                        except:
                            print('Error guardando')
                        h.close()
                    else:
                        send_message(chatid,mensajeid=379,args=(len(marcos-1) ) )
                elif(len(content) == 3 and content[1].isdigit() and content[2].isdigit()):
                    mn = int(content[1])
                    mn2 = int(content[1])
                    if(mn < len(marcos) and mn >= 0 and mn2 < len(marcos) and mn2 >= 0):
                        chat.mup = mn
                        chat.mdown = mn2
                        h.connect()
                        try:
                            h.chatMarcos(chat.mup,chat.mdown,chatid)
                        except:
                            send_message(chatid,mensajeid=192)
                        h.close()
                    else:
                        send_message(chatid,mensajeid=379,args=(len(marcos-1) ) )

                else:
                    send_message(chatid,mensajeid=193)
            elif(commandid == 102): #marcoE
                if(len(content) == 2 and content[1].isdigit()):
                    user.mup = int(content[1])
                    user.mdown = int(content[1])
                elif(len(content) == 3 and content[1].isdigit() and content[2].isdigit()):
                    user.mup = int(content[1])
                    user.mdown = int(content[2])
                else:
                    send_message(chatid,mensajeid=194)
                h.connect()
                h.userMarcos(user.mup,user.mdown,userid)
                h.close()
            elif(commandid == 103): #marcos
                r = sub_client.start_chat([userid],message='')
                if(r[0] == 200):
                    userchat = r[1]['thread']['threadId']
                    mostrarMarcos(userchat,comid)
                    send_message(chatid,mensajeid=611,args=(getNickname(userid,sub_client)),comid=comid)
                else:
                    send_message(chatid,mensajeid=195)
            elif(commandid == 104): #matar
                if(usersid):
                    for u in usersid:
                        trapitos = os.listdir('kill1')
                        send_message(chatid,mensajeid=380,args=(getNickname(userid,sub_client),getNickname(u,sub_client)))
                        send_imagen(chatid,'kill1/' + random.choice(trapitos),sanitized=True)
                else:
                    send_message(chatid,mensajeid=196)
            elif(commandid == 105): #maxstrikes
                if(len(content) >= 2 and content[1].isdigit()):
                    chat.settings['maxStrikes'] = int(content[1])
                    h.connect()
                    h.chatSettings(chatid,maxStrikes=int(content[1]))
                    h.close()
                else:
                    send_message(chatid,mensajeid=197)
            elif(commandid == 106): #media
                if(not m):
                    ts = loadMedia(chatid,h)
                    if(not ts):
                        send_message(chatid,mensajes[chat.idioma][381].replace('\\','\n'))
                    else:
                        text = mensajes[chat.idioma][373]+'\n'
                        for t in ts:
                            text += t + '\n'
                        send_message(chatid,text)
                else:
                    if(replyid):
                        message = sub_client.get_message_info(chatid,replyid)
                        h.connect()
                        saveMedia(chatid,m,message.json,sub_client,h)
                        h.close()
                    else:
                        ts = loadMedia(chatid,h)
                        t = ts.get(m)
                        if(t):
                            if(t['type'] == 0):
                                send_message(chatid,t['content'])
                            elif(t['type'] == 1): #image
                                r = send_link(chatid,link=t['content'])
                            elif(t['type'] == 2):
                                if(t['content'].endswith('.aac') or t['content'].endswith('.mp3')):
                                    name = t['content']
                                    f = download(name)
                                    send_audio(chatid,f)
                                else:
                                    link = urlAmino(t['content'])
                                    if(not link):
                                        send_message(chatid,mensajeid=451)
                                        return
                                    send_link(chatid,link=link,sanitized=True)
                            elif(t['type'] == 3):
                                send_sticker(chatid,t['content'])
                        else:
                            send_message(chatid,'No se encontro %s en este chat' % (m))
            elif(commandid == 107): #mensaje
                if(len(content) > 1):
                    if(content[1] == palabras['bienvenida']):
                        m = allContent[allContent.find(palabras['bienvenida'])+len(palabras['bienvenida']):].strip()
                        chat.mensaje = m.lstrip()
                        h.connect()
                        try:
                            h.chatMensaje(m,chatid)
                            addLogro(chat,userid,3,h)
                        except:
                            send_message(chatid,mensajeid=192)
                        else:
                            send_message(chatid,mensajeid=199)
                        h.close()
                        return
                    elif(content[1] == palabras['donacion'] ):
                        m = allContent[allContent.find(palabras['donacion'])+len(palabras['donacion']):].strip()
                        chat.mensajeDonacion = m.lstrip()
                        h.connect()
                        try:
                            h.chatMensajeDonacion(m,chatid)
                        except:
                            send_message(chatid,mensajeid=192)
                        else:
                            send_message(chatid,mensajeid=201)
                        h.close()
                        return
                    elif(content[1] == 'sticker' ):
                        m = allContent[allContent.find('sticker')+7:].strip()
                        if(not m):
                            send_message(chatid,mensajeid=642)
                            return
                        else:
                            chat.mensajeGif = m.lstrip()
                            h.connect()
                            try:
                                h.chatMensajeGif(m,chatid)
                            except:
                                send_message(chatid,mensajeid=192)
                            else:
                                send_message(chatid,mensajeid=640)
                            h.close()
                            return

                send_message(chatid,mensajeid=202)
            elif(commandid == 108): #messageid
                if(replyid):
                    send_message(chatid,replyid)
                else:
                    send_message(chatid,id)
            elif(commandid == 109): #miau
                getCat(chatid)
            elif(commandid == 110): #moe 
                offFilter = False
                if(chatid in filters and not filters[chatid]):
                    offFilter = True

                buscarMoe(chatid,m,idioma=chat.idioma,ecchi=ecchi,offFilter=offFilter)
            elif(commandid == 111):  #ndclink
                send_message(chatid,'ndc://x%d/chat-thread/%s' % (comid,chatid) )
            elif(commandid == 112): #nickname
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=173)
                else:
                    if(m):
                        sub_client.edit_profile(nickname=m)
                    else:
                        send_message(chatid,mensajeid=204)
            elif(commandid == 113): #noalias
                user.alias = ""
                h.connect()
                h.userAlias('',userid)
                h.close()
                send_message(chatid,mensajeid=205)
            elif(commandid == 114): #nombre
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=173)
                else:
                    if(m):
                        if(len(m) >= 50):
                            send_message(chatid,mensajeid=207)
                            return
                        h.connect()
                        r = h.nombreBot(client.profile.id,m)
                        h.close()
                        if(r):
                            send_message(chatid,mensajeid=382,args=m)
                            bots[client.profile.id]['name'] = m
                            client.edit_profile(nickname=m)
                        else:
                            send_message(chatid,mensajeid=208)
                    else:
                        send_message(chatid,mensajeid=209)
            elif(commandid == 115): #notraducir
                traducirDetectarUsers[chatid] = []
                send_message(chatid,mensajeid=210)
            elif(commandid == 116): #nsfw
                if(len(content) < 2):
                    if(chat.settings['nsfw']):
                        send_message(chatid,mensajeid=211)
                    else:
                        send_message(chatid,mensajeid=212)
                else:
                    if(content[1] == palabras['si'] ):
                        eliminarNSFW = True
                        send_message(chatid,mensajeid=213)
                        h.connect()
                        h.chatSettings(chatid,nsfw=1)
                        h.waitClose()
                        chat.settings['nsfw'] = 1
                    elif(content[1] == palabras['no']):
                        eliminarNSFW = False
                        send_message(chatid,mensajeid=214)
                        h.connect()
                        h.chatSettings(chatid,nsfw=0)
                        h.close()
                        chat.settings['nsfw'] = 0
                    else:
                        send_message(chatid,mensajeid=215)
            elif(commandid == 117): #otrosBots
                if(len(content) < 2):
                    send_message(chatid,mensajeid=216)
                    return
                if(content[1] == palabras['si'] ):
                    send_message(chatid,mensajeid=217)
                    chat.settings['otrosBots'] = 1
                    h.connect()
                    h.chatSettings(chatid,otrosBots=1)
                    h.close()
                elif(content[1] == palabras['no']):
                    send_message(chatid,mensajeid=218)
                    chat.settings['otrosBots'] = 0
                    h.connect()
                    h.chatSettings(chatid,otrosBots=0)
                    h.close()
            elif(commandid == 118): #op
                if(len(content) == 1):
                    send_message(chatid,mensajeid=383,args=(opLevel) )
                elif(not content[1].isdigit()):
                    for u in usersid:
                        if(u not in chat.ops):
                            send_message(chatid,mensajeid=384,args=getNickname(u,sub_client))
                        else:
                            send_message(chatid,mensajeid=385,args=(getNickname(u,sub_client),chat.ops[u]) )
                else:
                    l = int(content[1])
                    if(not usersid):
                        text = 'op %d:\n' % (l)
                        print(chat.ops)
                        mentions = []
                        for u,opl in chat.ops.items():
                            if(opl == l):
                                text += '<$%s$>\n' % (getNickname(u,sub_client))
                                mentions.append(u)
                                # text += getNickname(u,sub_client) + '\n'
                        sub_client.send_message(chatid,text,mentionUserIds=mentions,linkText=True)

                    else:
                        if(l < opLevel or userid == ley):
                            for u in usersid:
                                if((u in chat.ops and opLevel <= chat.ops[u]) or u == leybot ):
                                    continue
                                chat.ops[u] = l
                                h.connect()
                                h.opChat(chatid,chat.ops)

                                addLogro(chat,userid,19,h)
                                h.close()
                        else:
                            send_message(chatid,mensajeid=219)
            elif(commandid == 119): #openings
                openings(chatid,content,m,client,idioma=chat.idioma)
            elif(commandid == 120):#opinion 
                if(m == None):
                    send_message(chatid,mensajeid=220)
                else:
                    addLogro(chat,userid,17)
                    chatname = get_title(chatid,comid)
                    text = 'Opinion en el chat ndc://x%d/chat-thread/%s\n' % (comid,chatid)
                    text += 'Por: '+ getTrueNickname(userid,sub_client) + ' ndc://x%d/user-profile/%s\n' % (comid,userid)
                    text += m
                    send_botgroup(text)
                    
                    send_message(chatid,mensajeid=221)
            elif(commandid == 121): #patear
                if(usersid):
                    if(len(usersid) > 3):
                        usersid = usersid[:3]
                        send_message(chatid,mensajeid=222)

                    for u in usersid:
                        patear(chatid,u,client)
                else:                           
                    send_message(chatid,mensajeid=223)
            elif(commandid == 122): #pause
                if(chatid not in channels):
                    e = threading.Event()
                    waitForChannel(chatid,e)
                    request_channel_info(sockets[client.profile.id],chatid,comid)
                    print('esperando por respuesta')
                    e.wait()
                    print('respuesta obtenida')
                    if(chatid not in channels):
                        send_message(chatid,mensajeid=224)
                        return
                channel = channels[chatid]
                sendPauseRequest(channel)
            elif(commandid == 123): #perdonar
                if(chatid not in funados):
                    return
                if(usersid):
                    addLogro(chat,userid,7)
                    funados[chatid] = [item for item in funados[chatid] if item not in usersid]
                else:
                    send_message(chatid,mensajeid=225)
            elif(commandid == 124): #permisos
                if(len(content) != 3):
                    send_message(chatid,mensajeid=226)
                else:
                    try:
                        op = int(content[2])
                    except:
                        op = -2
                    c = content[1]
                    if(content[1] not in comandosIdioma[chat.idioma]):
                        send_message(chatid,mensajeid=141)
                        return
                    c = comandosIdioma[chat.idioma][c]
                    if(c == 124):
                        send_message(chatid,mensajeid=227)
                        return
                    custom = opCustom[chatid].get(c,-2)
                    if(op >= 0 and comandos[c][0] == -1):
                        if(chatThread['type'] == 2):
                            userInfo = sub_client.get_user_info(userid,raw=True)['userProfile']
                            role = userInfo['role']
                            if( (role >= 100 and role <= 102) or userid == ley or bots[client.profile.id]['owner'] == userid):
                                send_message(chatid,mensajeid=386,args=content[1])
                                opCustom[chatid][c] = 0
                                h.connect()
                                h.customOP(chatid,opCustom[chatid])
                                addLogro(chat,userid,18,h)
                                h.close()

                                if(role == 100 or role == 102):
                                    send_message(chatid,mensajeid=169)
                            else:
                                send_message(chatid,mensajeid=170)
                                return
                        else:
                            send_message(chatid,mensajeid=387,args=content[1])
                            send_message(chatid,mensajeid=171)
                            opCustom[chatid][c] = 0
                            h.connect()
                            h.customOP(chatid,opCustom[chatid])
                            h.close()
                        return

                    if(op >= -1 and op <= 3):

                        send_message(chatid,mensajeid=388,args=(content[1],op) )
                        h.connect()
                        h.customOP(chatid,opCustom[chatid])
                        addLogro(chat,userid,18,h)
                        h.close()
                        opCustom[chatid][c] = op
                    else:                                
                        send_message(chatid,mensajeid=232)
            elif(commandid == 125): #permitir
                if(len(content) < 2):
                    text = mensajes[chat.idioma][389]
                    if(spamTextChat[chatid]):
                        text += '\n' + mensajes[chat.idioma][390] + '\n'
                        for t in spamTextChat[chatid]:
                            text += t + ' \n'
                        send_message(chatid,text)
                else:
                    if(content[1] == 'links'):
                        unaves = True
                        if('aminoapps.com/p' in spamTextChat[chatid]):
                            spamTextChat[chatid].remove('aminoapps.com/p')
                            if(unaves):
                                send_message(chatid,mensajeid=691)
                                unaves = False
                        if(unaves):
                            send_imagen(chatid,mensajeid=692)
                    elif(content[1] == palabras['imagenes']):
                        spamImagenesChat[chatid] = False
                        send_message(chatid,mensajeid=657)
                    elif(content[1] == 'stickers'):
                        spamStickersChat[chatid] = False
                        send_message(chatid,mensajeid=658)

                    elif(content[1] == 'flood'):
                        spamRepetidosChat[chatid] = 0
                        send_message(chatid,mensajeid=659)

                    elif(content[1] == 'texto'):
                        spamTextChat[chatid] = []
                        send_message(chatid,mensajeid=660)
                    else:
                        send_message(chatid,mensajeid=389)
            elif(commandid == 126): #personaje
                personaje(chatid,content,m,client,idioma=chat.idioma)
            elif(commandid == 127): #ping
                ping(chatid,createdTime,sub_client,idioma=chat.idioma)
            elif(commandid == 128): #placa
                if(not m):
                    if(chat.placa):
                        send_message(chatid,mensajeid=393,args=str(chat.placa) )
                    else:
                        send_message(chatid,mensajeid=233)
                else:
                    chat.placa = m
                    try:
                        h.connect()
                        h.chatPlaca(m,chatid)
                    except:
                        send_message(chatid,mensajeid=234)
                    else:
                        send_message(chatid,mensajeid=394,args=m)
                        send_botgroup(text,'El chat ' + get_title(chatid,comid) + '\nActualizo su placa: ' + m)
                    h.close()
                    
            elif(commandid == 176 or commandid == 129): #play #youtube
                if(comando == 'play'):
                    if(chatid not in channels):
                        e = threading.Event()
                        waitForChannel(chatid,e)
                        get_voice_chat_info_and_join(sockets[client.profile.id],chatid,comid,wait=0.0)
                        print('esperando por respuesta')
                        e.wait()
                        print('respuesta obtenida')
                        # detect_or_join_channel(sockets[client.profile.id],chatid,comid)
                        if(chatid not in channels):
                            send_message(chatid,mensajeid=224)
                            return

                    if(not m):
                        sendPlayRequest(channels[chatid])
                        return
                    if(m.startswith('http')):
                        if(m.startswith('https://www.youtube.com/watch?v=')):
                            r = sendVideoRequest(channels[chatid],m[32:43],userid)
                            if(r):
                                addLogro(chat,userid,16)
                                send_message(chatid,mensajeid=236)
                            else:
                                send_message(chatid,mensajeid=237)
                        elif(m.startswith('https://youtu.be/')):
                            r = sendVideoRequest(channels[chatid],m[17:28],userid)
                            if(r):
                                addLogro(chat,userid,16)
                                send_message(chatid,mensajeid=236)
                            else:
                                send_message(chatid,mensajeid=237)

                        else:
                            r = sendVideoRequest(channels[chatid],m,userid)
                            addLogro(chat,userid,16)
                            if(r):
                                send_message(chatid,mensajeid=240)
                            else:
                                send_message(chatid,mensajeid=237)

                        return

                if(chatid in youtubeLists):
                    youtubeList = youtubeLists[chatid]
                else:
                    youtubeList = deque([])
                    youtubeLists[chatid] = youtubeList
                if(m):
                    if(content[1] == palabras['cancelar']):
                        if(len(content) == 2):
                            youtubeList.clear()
                            return    
                        elif(len(content) == 3 and content[2].isdigit()):
                            n = int(content[2])-1
                            if(len(youtubeList) > n ):
                                del youtubeList[int(content[2])]
                                return
                    if(len(youtubeList) >=3):
                        send_message(chatid,mensajeid=242)
                        text = 'En cola:\n'
                        n = 1
                        for i in youtubeList:
                            text += str(n) + '. ' + i['title'] + '\n'
                            n+=1
                        send_message(chatid,text)
                    else:
                        userYoutube[chatid] = userid
                        searchYoutube(chatid,m,chat.idioma)
                else:
                    if(comando == 'play'):
                        send_message(chatid,mensajeid=243)
                        return
                    if(youtubeList):
                        text = mensajes[chat.idioma][401]+'\n'
                        for i in youtubeList:
                            text += i['title'] + '\n'
                        send_message(chatid,text)
                    else:
                        send_message(chatid,mensajeid=402,args=(comando))
            elif(commandid == 130): #playing
                if(chatid not in channels):
                    e = threading.Event()
                    waitForChannel(chatid,e)
                    request_channel_info(sockets[client.profile.id],chatid,comid)
                    print('esperando por respuesta')
                    e.wait()
                    print('respuesta obtenida')
                    if(chatid not in channels):
                        send_message(chatid,mensajeid=224)
                        return
                channel = channels[chatid]
                r = requestPlayPosition(channel)
                if(not r):
                    send_message(chatid,mensajeid=633)
                    return
                id = r['id']
                position = r['position']
                u = r['userid']
                if(id.startswith('http')):
                    send_message(chatid,'Streaming: %s\nTranscurrido: %s\n' % (id,str(datetime.timedelta(seconds=position))))
                else:
                    duration = r['duration']
                    sendYoutubeObject(chatid,sub_client,id,position,duration,u)
            elif(commandid == 131): #prefijo
                if(not m):
                    send_message(chatid,mensajeid=245)
                else:
                    print(chat.settings)
                    chat.settings['prefijo'] = m
                    h.connect()
                    h.chatSettings(chatid,prefijo=m)
                    h.close()
            elif(commandid == 132): #proyeccion
                start_live_mode(sockets[client.profile.id],chatid,comid,5)
            elif(commandid == 133): #queue
                if(chatid not in channels):
                    e = threading.Event()
                    waitForChannel(chatid,e)
                    request_channel_info(sockets[client.profile.id],chatid,comid)
                    print('esperando por respuesta')
                    e.wait()
                    print('respuesta obtenida')
                    if(chatid not in channels):
                        send_message(chatid,mensajeid=224)
                        return
                channel = channels[chatid]
                try:
                    h.connect()
                    queue = requestQueue(channel,h)
                    h.close()
                except:
                    PrintException()
                if(not queue):
                    send_message(chatid,mensajeid=247)
                else:
                    i = 1
                    text = mensajes[chat.idioma][395] +'\n'
                    unaves = True
                    fid = None
                    for q in queue:
                        id = q['id']
                        u = q['userid']
                        if(id.startswith('http')):
                            text += mensajes[chat.idioma][396].replace('\\','\n') % (i,id,getNickname(u,sub_client))
                        else:
                            r = ys('v=%s' % (id),1).to_dict()[0]
                            if(unaves):
                                title = r['title']
                                text2 = mensajes[chat.idioma][397] % (getNickname(u,sub_client))
                                fid = id
                                unaves = False
                            text += mensajes[chat.idioma][398].replace('\\','\n') % (i,r['title'],r['duration'],getNickname(u,sub_client))
                        i+=1
                    text += mensajes[chat.idioma][399]+'\n\n'
                    sendYoutubeObject(chatid,sub_client,fid,0,0,userid,text=text,title=title,text2=text2)
            elif(commandid == 134): #random
                if(len(content) == 2):
                    if(not content[1].isdigit()):
                        send_message(chatid,mensajeid=656)
                        send_message(chatid,mensajeid=248)
                    else:
                        send_message(chatid,str(random.randint(1,int(content[1]))))
                elif(len(content) == 3):
                    if(not content[1].isdigit() or not content[2].isdigit()):
                        send_message(chatid,mensajeid=656)
                        send_message(chatid,mensajeid=248)
                    else:
                        send_message(chatid,str(random.randint(int(content[1]),int(content[2]))))
                else:
                    send_message(chatid,mensajeid=248)
            elif(commandid == 135): #recibir
                if(usersid):
                    for u in usersid:
                        bienvenida(chatid,"",chat.bn,chat.mup,chat.mdown,u)
                else:
                    bienvenida(chatid,chat.mensaje,chat.bn,chat.mup,chat.mdown)
            elif(commandid == 136): #recuperar
                if(content[1].isdigit()):
                    n = int(content[1])
                else:
                    n = 1
                messageIds = lastDeletedMessages.get(chatid,[])
                print(messageIds)
                for mid in messageIds:
                    m = recoverMessage(mid)
                    if(m):
                        if(m[1] == 0):
                            send_message(chatid,m[2])
                        elif(m[1] == 1):
                            send_link(chatid,m[2],confi=0.5)
                        n -= 1
                        if(n <= 0):
                            break
            elif(commandid == 137): #remove 
                if(not usersid):
                    send_message(chatid,mensajeid=249)
                for u in usersid:
                    remove_from_channel(sockets[client.profile.id],chatid,comid,u)
            elif(commandid == 138): #repetir
                if(replyid != None):

                    t = int(content[1])
                    if(t > 100):
                        send_message(chatid,mensajeid=250)
                    elif(opLevel < 3 and t > 10):
                        send_message(chatid,mensajeid=251)
                    else:
                        message = sub_client.get_message_info(chatid,replyid)
                        content = message.json['content']
                        mediaValue = message.json['mediaValue']     
                        continuarRepetir[chatid] = True
                        if(mediaValue != None):
                            l = True
                            m = mediaValue
                            r = nudeDetect(m)
                            if(r >= confidence):
                                send_message(chatid,mensajeid=252)
                                return
                        elif(content != None):
                            l = False
                            m = content
                        for i in range(t):
                            if(not continuarRepetir[chatid]):
                                break
                            if(l):
                                send_link(chatid,link=m,sanitized=True)
                            else:
                                send_message(chatid,m)
                else:
                    send_message(chatid,mensajeid=253)
            elif(commandid == 139): #reportar
                if(len(content) < 2 and not replyid):
                    send_message(chatid,mensajeid=254)
                    send_message(chatid,mensajeid=255)
                    send_message(chatid,mensajeid=256)
                elif(replyid):
                    m = m if m else ''
                    if(replyid in sentBooru):
                        url = sentBooru[replyid]
                        bannedUrls.append(url)
                        h.connect()
                        h.banUrl(url)
                        h.close()
                        send_message(chatid,mensajeid=257)
                        send_message(botgroup,'' % (comid,chatid))
                        send_botgroup('imagen reportada en el chat ndc://x%d/chat-thread/%s' % (comid,chatid))
                        send_botgroup('%s por favor revisala' % (url))
                    else:
                        send_message(chatid,mensajeid=258)
                    h.connect()
                    h.report(chatid,replyid,userid,m)
                    h.close()
                    text = 'reporte del chat chat ndc://x%d/chat-thread/%s\n' % (comid,chatid)
                    text += 'Por: ndc://x%s/user-profile/%s' % (comid,userid)
                    if(m):
                        text += 'mensaje: ' + m
                    send_botgroup(text)
                else:
                    h.connect()
                    h.report(chatid,id,userid,m)
                    h.close()
                    send_message(chatid,mensajeid=258)
                    text = 'reporte del chat chat ndc://x%d/chat-thread/%s\n' % (comid,chatid)
                    text += 'Por: ndc://x%s/user-profile/%s' % (comid,userid)
                    if(m):
                        text += ' mensaje: ' + m
                    send_botgroup(text)
            elif(commandid == 140): #reset
                h.connect()
                h.setBotState(3,chatid)
                chatStates[chatid] = 3
                h.close()
                send_message(chatid,mensajeid=260)
            elif(commandid == 141): #revivir
                send_message(chatid,mensajeid=261)
                for i in range(3):
                    send_invocacion(chatid,get_cohosts(chatid,comid) + [host],'revivan gente')
            elif(commandid == 142): #role
                if(usersid):
                    # roles = rolesComunidad[comid]
                    h.connect()
                    roles = h.loadRolesComunidad(comid)
                    for u in usersid:
                        hasRole = False
                        rolesU = h.loadRolesUser(u)
                        for r in rolesU:
                            text = mensajes[chat.idioma][403] % (getNickname(u,sub_client)) + "\n\n" 
                            if(r in roles):
                                hasRole = True
                                role = roles[r]
                                text += '[cub]%s\n[ci]%s\n\n' % (role[0],role[1])

                        if(not hasRole):
                            send_message(chatid,mensajeid=400,args=(getNickname(u,sub_client)))
                        else:
                            send_message(chatid,text)
                    h.close()
                    return
                ln = allContent.split('\n')
                con = ln[0].split(' ')
                if(role != 100 and role != 102):
                    send_message(chatid,mensajeid=262)
                    return
                if(len(con) < 2):
                    send_message(chatid,mensajeid=263)
                elif(len(ln) < 2):
                    send_message(chatid,mensajeid=264)
                else:
                    color = con[-1].lower()
                    textColor = color
                    if(color[0] != '#'):
                        send_message(chatid,mensajeid=265)
                        send_message(chatid,mensajeid=266)
                        return
                    color = color[1:]
                    try:
                        color = int(color,16)
                    except Exception as e:

                        send_message(chatid,mensajeid=265)
                        send_message(chatid,mensajeid=266)
                        return
                    nombre = ln[0][6:ln[0].rfind('#')].strip().rstrip()
                    print(nombre)
                    descripcion = ' '.join(ln[1:])
                    print(comid,nombre,descripcion,color)
                    h.connect()
                    roles = h.loadRolesComunidad(comid)
                    for rid,r in roles.items():
                        if(nombre == r[0]):
                            send_message(chatid,mensajeid=269)
                            h.close()
                            return
                    h.roleComunidad(comid,nombre,descripcion,color)
                    # rolesComunidad[comid] = s.loadRolesComunidad(comid)
                    h.close()
                    send_message(chatid,'Role %s agregado' % (nombre))
            elif(commandid == 143): #roles
                h.connect()
                roles = h.loadRolesComunidad(comid)
                h.close()
                if(not roles):
                    send_message(chatid,mensajeid=270)
                else:
                    text = mensajes[chat.idioma][404]+"\n\n"
                    for role in roles.values():
                        text += '[cub]%s\n[ci]%s\n\n' % (role[0],role[1])
                    send_message(chatid,text)

            elif(commandid == 144): #rip
                if(usersid):
                    if(len(usersid) > 3):
                        send_message(chatid,mensajeid=222)
                    for u in usersid:
                        rip(chatid,u)
                else:
                    send_message(chatid,mensajeid=271)
            elif(commandid == 145): #save
                r = ""
                if(replyid == None):
                    send_message(chatid,mensajeid=340)
                elif(m == None ):
                    send_message(chatid,mensajeid=341)  
                    send_message(chatid,mensajeid=272)
                elif('/' in m):
                    send_message(chatid,mensajeid=342)   
                    
                else:
                    message = sub_client.get_message_info(chatid,replyid)
                    content = message.json['content']
                    mediaValue = message.json['mediaValue']
                    t = message.json['type']
                    if(t == 100):
                        send_message(chatid,mensajeid=174)
                    else:
                        message = message.json
                        h.connect()
                        r = saveMedia(userid,m,message,sub_client,h)
                        h.close()
                        if(r):
                            send_message(chatid,mensajeid=482,args=m)
                        else:
                            send_message(chatid,mensajeid=455)

            elif(commandid == 146): #se
                text = getNickname(userid,sub_client) + ' ' + allContent[1:]
                send_message(chatid,text)
            elif(commandid == 147): #seguir
                if(chatid in seguirLimpiando and not seguirLimpiando[chatid]):
                    seguirLimpiando[chatid] = True
                    return
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=274)
                else:
                    if(usersid):
                        for u in usersid:
                            send_message(chatid,mensajeid=405,args=(getNickname(u,sub_client)) )
                            sub_client.follow(u)
                    else:
                        send_message(chatid,mensajeid=275)
            elif(commandid == 148): #seguro
                sub_client.edit_chat(chatid,viewOnly=True)
            elif(commandid == 149): #setrole
                if(role < 100 and role > 102):
                    send_message(chatid,mensajeid=276)
                    return
                if(len(content) < 2):
                    send_message(chatid,mensajeid=277)
                    send_message(chatid,mensajeid=278)
                    return
                p = m.rfind('http://aminoapps.com/p/')
                if(p > 0):
                    uid,r = useridByLink(m[p:],idioma=chat.idioma)
                    name = m[:p]
                    if(r):
                        usersid = [uid]
                    else:
                        send_message(chatid,uid)
                else:
                    if(not usersid or usersid[0] == replyuid):
                        name = m
                    else:
                        name = m[:m.rfind('@')]
                if(not usersid):
                    usersid = [userid]
                h.connect()
                roles = h.loadRolesComunidad(comid)
                roleid = None            
                role = None
                for rid,r in roles.items():
                    if(r[0] in name):
                        roleid = rid
                        role = r
                        break
                if(not roleid):
                    send_message(chatid,mensajeid=406,args=(name))
                    h.close()
                    return
                for u in usersid:
                    sub_client.add_title(u,r[0],'#%06X' % (r[2]) )
                    h.roleUser(u,roleid)
                    send_message(chatid,mensajeid=407,args=(name,getNickname(u,sub_client)))
                h.close()
            elif(commandid == 150): #ship
                if(len(usersid) != 2):
                    send_message(chatid,mensajeid=279)
                else:
                    if(content[1].isdigit()):
                        addLogro(chat,userid,20)
                        ship(chatid,usersid[0],usersid[1],int(content[1]),idioma=chat.idioma)
                    else:
                        addLogro(chat,userid,20)
                        ship(chatid,usersid[0],usersid[1],idioma=chat.idioma)
            elif(commandid == 151): #sigueme
                if(bot['public'] or bot['owner'] == userid or userid == ley):
                    sub_client.follow(userid)
                    send_reply(chatid,mensajes[chat.idioma][408],id)
                    addLogro(chat,userid,5)
                else:
                    send_reply(chatid,mensajes[chat.idioma][409],id)
            elif(commandid == 152): #skip
                if(chatid not in channels):
                    e = threading.Event()
                    waitForChannel(chatid,e)
                    request_channel_info(sockets[client.profile.id],chatid,comid)
                    print('esperando por respuesta')
                    e.wait()
                    print('respuesta obtenida')
                    if(chatid not in channels):
                        send_message(chatid,mensajeid=224)
                        return
                r = skipSong(channels[chatid])
                if(not r):
                    send_message(chatid,mensajeid=343)
            elif(commandid == 153): #sticker
                if(replyid and m):
                    message = sub_client.get_message_info(chatid,replyid)
                    if('originalStickerId' not in message.json['extensions']):
                        send_message(chatid,mensajeid=281)
                    elif(sub_client.get_sticker_collection(message.json['extensions']['sticker']['stickerCollectionId']).collectionType == 2):
                        send_message(chatid,mensajeid=282)
                    else:
                        stickerid = message.json['extensions']['originalStickerId']
                        r = user.addSavedMessage(m,stickerid,3)

                        send_message(chatid,r)
                else:
                    send_message(chatid,mensajeid=283)
            elif(commandid == 154): #strike 
                n = 1
                if(len(content) >= 2):
                    try:
                        n = int(content[1])
                    except:
                        pass
                h.connect()
                for u in usersid:
                    strike(chat,u,sub_client,h,n)
                h.close()
            elif(commandid == 155): #strikes
                if(usersid):
                    text = ''
                    for u in usersid:
                        if(u in chat.strikes):
                            text += 'strikes %s: %d\n' % (getNickname(u,sub_client),chat.strikes[u])
                        else:
                            text += 'strikes %s: %d\n' % (getNickname(u,sub_client),0)
                    send_message(chatid,text)
                else:
                    text = 'Strikes:\n'
                    for u in chat.strikes:
                        if(chat.strikes[u]):
                            text += '%s: %d\n' % (getNickname(u,sub_client),chat.strikes[u])
                    send_message(chatid,text)


            elif(commandid == 156): #sugerencia
                if(m == None):
                    send_message(chatid,mensajeid=284)
                else:
                    chatname = get_title(chatid,comid)
                    text = 'Sugerencia en el chat ndc://x%d/chat-thread/%s\n' % (comid,chatid)
                    text += 'Por: '+ getTrueNickname(userid,sub_client) + ' ndc://x%d/user-profile/%s\n' % (comid,userid)
                    text += m
                    send_botgroup(text)
                    send_message(chatid,mensajeid=285)
            elif(commandid == 157): #temporada
                temporada(chatid,content,idioma=chat.idioma)
            elif(commandid == 158): #test
                if(len(content) >= 2):
                    if(content[1] == 'unirse'):
                        sub_client.invite_to_chat([testBot],chatid)
                        c = bots[testBot]['client']
                        sc = c.sub_client(comid)
                        r = c.join_community(comid)
                        if(r != 200):
                            send_message(chatid,mensajeid=286)
                            return
                        sc.leave_chat(chatid)
                        sub_client.invite_to_chat([testBot],chatid)
                        sc.join_chat(chatid)
                        c.leave_community(comid)
                else:
                    with open('ayuda/%s/comandos/test.txt' % (chat.idioma),'r') as e:
                        t = e.read()
                        send_message(chatid,t)
            elif(commandid == 159): #tipoMensaje
                if(len(content) == 2):
                    if(content[1] == palabras['normal']):
                        tm = 0
                    elif(content[1] == palabras['especial']):
                        tm = 109
                    else:
                        send_message(chatid,mensajeid=287)
                        return
                    tipoMensajeChat[chatid] = tm
                    chat.settings['tipoMensaje'] = tm
                    h.connect()
                    h.chatMessageType(tm,chatid)
                    h.close()
                else:
                    send_message(chatid,mensajeid=288)
            elif(commandid == 160): #top
                # send_message(chatid,mensajeid=289)
                # return
                top2(chatid,content,createdTime,chat,sub_client,idioma=chat.idioma)

            elif(commandid == 161): #traducir
                if(replyid or usersid):
                    if(replyid):
                        message = sub_client.get_message_info(chatid,replyid)
                        replyContent = message.json['content']
                        if(content != None):
                            replyContent = unicodedata.normalize( 'NFKC', replyContent)
                            if(len(content) == 2 and content[1] == palabras['nombre']):
                                    nom = sub_client.get_user_info(message.json['uid']).nickname
                                    send_message(chatid,unicodedata.normalize( 'NFKC', nom))
                            else:
                                traduccion = translator.translate(replyContent,dest=chat.idioma)
                                send_message(chatid,traduccion.text)
                                # send_message(chatid,replyContent)
                    elif(usersid):
                        if(len(content) >= 2 and content[1] == palabras['nombre']):
                            for u in usersid:
                                nom = sub_client.get_user_info(message.json['uid']).nickname
                                send_message(chatid,unicodedata.normalize( 'NFKC', nom))
                        
                        else:
                            if(chatid not in traducirDetectarUsers):
                                traducirDetectarUsers[chatid] = []
                            for u in usersid:
                                if(u == client.profile.id):
                                    send_message(chatid,mensajeid=290)
                                else:
                                    traducirDetectarUsers[chatid].append(u)
                            print('traduciendo',traducirDetectarUsers[chatid])
                elif(len(content) > 1):
                    m = unicodedata.normalize( 'NFKC', m)
                    traduccion = translator.translate(m,dest=chat.idioma)
                    send_message(chatid,traduccion.text)

                else:
                    with open('ayuda/%s/comandos/traducir.txt' % (chat.idioma),'r') as e:
                        text = e.read()
                    send_message(chatid,text)
            elif(commandid == 162): #trapito
                trapitos = os.listdir('trapitos')
                print('trapitos/' + random.choice(trapitos))
                send_imagen(chatid,'trapitos/' + random.choice(trapitos),sanitized=True)

            elif(commandid == 163): #transferir
                if(len(content) < 2):
                    send_message(chatid,mensajeid=291)
                else:
                    if(content[1] == palabras['dueño']):
                        if(len(usersid) != 1 ):
                            send_message(chatid,mensajeid=292)
                            return
                        if(bot['owner'] != userid and userid != ley):
                            send_message(chatid,mensajeid=150)
                            return
                        bot['owner'] = usersid[0]
                        h.connect()
                        h.transferOwner(client.profile.id,usersid[0])
                        h.close()
                    elif(content[1] == palabras['anfitrion']):
                        if(get_host(chatid,comid) != client.profile.id):
                            send_message(chatid,mensajeid=294)
                            return
                        if(opLevel < 3):
                            send_message(chatid,mensajeid=295)
                        else:
                            if(not usersid):
                                usersid = [userid]
                            sub_client.transfer_host(chatid,usersid)
                            send_message(chatid,mensajeid=296)

            elif(commandid == 164): #unbanuser
                if(len(content) < 2):
                    send_message(chatid,mensajeid=297)
                else:
                    if(usersid):
                        if('@' not in allContent):
                            reason = m
                        h.connect()
                        for u in usersid:
                            h.unbanUser(u)
                            bannedUsers.pop(u)
                        h.close()
                    else:
                        h.connect()
                        h.unbanUser(content[1])
                        h.close()
                        bannedUsers.pop(content[1])
            elif(comando == 165): #unbanchat
                if(len(content) < 2):
                    send_message(chatid,mensajeid=297)
                else:
                    if(usersid):
                        if('@' not in allContent):
                            reason = m
                        h.connect()
                        for u in usersid:
                            h.unbanChat(u)
                            bannedChats.pop(u)
                        h.close()
                    else:
                        h.connect()
                        h.unbanChat(content[1])
                        h.close()
                        bannedChats.pop(content[1])
            elif(commandid == 166): #uptime
                t = time() - startbotTime
                text = "Tiempo activo del bot: %d:%d\n" % (t/60,t%60)
                send_message(chatid,text)

            elif(commandid == 167): #unsetrole
                if(role < 100 and role > 102):
                    send_message(chatid,mensajeid=276)
                    return
                if(len(content) < 2):
                    send_message(chatid,mensajeid=300)
                    send_message(chatid,mensajeid=278)
                    return
                p = m.rfind('http://aminoapps.com/p/')
                if(p > 0):
                    uid,r = useridByLink(m[p:])
                    name = m[:p]
                    if(r):
                        usersid = [uid]
                    else:
                        send_message(chatid,uid)
                else:
                    if(not usersid or usersid[0] == replyuid):
                        name = m
                    else:
                        name = m[:m.rfind('@')]
                if(usersid and usersid[0] == replyuid):
                    name = m
                else:
                    name = m[:m.rfind('@')]
                if(not usersid):
                    usersid = [userid]
                h.connect()
                roles = h.loadRolesComunidad(comid)
                roleid = None            
                role = None
                for rid,r in roles.items():
                    if(r[0] in name):
                        roleid = rid
                        role = r
                        break
                if(not roleid):
                    send_message(chatid,mensajeid=406,args=(name))
                    h.close()
                    return
                for u in usersid:
                    rolesUser = h.loadRolesUser(u)
                    if(roleid not in rolesUser):
                        send_message(chatid,mensajeid=410,args=(getNickname(u,sub_client),role[0]))
                        continue
                    sub_client.remove_title(u,role[0])
                    h.deleteUserRole(u,roleid)
                    send_message(chatid,mensajeid=411,args=(role[0],getNickname(u,sub_client)))
                h.close()
            elif(commandid == 168): #userid
                for u in usersid:
                    send_message(chatid,u)
            elif(commandid == 169): #ver 
                if(not usersid):
                    ver(chatid,userid,chat,sub_client,idioma=chat.idioma)
                for u in usersid:
                    ver(chatid,u,chat,sub_client,idioma=chat.idioma) 

            elif(commandid == 170): #version
                with open('version.txt','r') as x:
                    version = x.read()
                send_message(chatid,mensajeid=412,args=(version))
            elif(commandid == 171): #videollamada
                start_live_mode(sockets[client.profile.id],chatid,comid,4) 
                if(chatThread['type'] != 2 or client.profile.id in get_cohosts(chatid,comid)):
                    addLogro(chat,userid,21)
            elif(commandid == 172): #voces
                text = palabras['Voces'] + ':' +  cargarVoces()
                send_message(chatid,text)
            elif(commandid == 173): #volumen
                if(chatid not in channels):
                    e = threading.Event()
                    waitForChannel(chatid,e)
                    request_channel_info(sockets[client.profile.id],chatid,comid)
                    e.wait()
                    if(chatid not in channels):
                        send_message(chatid,mensajeid=224)
                        return
                if(len(content) < 2):
                    send_message(chatid,mensajeid=303)
                elif(not content[1].isdigit()):
                    send_message(chatid,mensajeid=304)
                else:
                    v = int(content[1])
                    if(v > 100):
                        v = 100
                    channels[chatid].volume = v
                    h.connect()
                    h.chatSettings(chatid,volume=v)
                    h.close()
                    chat.settings['volume'] = v
                    send_message(chatid,mensajeid=639)

                    requestVolumeChange(channels[chatid],v)

            elif(commandid == 174): #voz
                if(m):
                    if(m not in voces):
                        send_message(chatid,mensajeid=413,args=(m))
                        text = palabras['Voces'] + ':' +  cargarVoces()
                        send_message(chatid,text)
                    else:
                        voz = m
                        send_message(chatid,mensajeid=414,args=m)
                        h.connect()
                        h.chatSettings(chatid,voz=voz)
                        chat.settings['voz'] = voz 
                        h.close()
                else:
                    send_message(chatid,mensajeid=305)
                    send_message(chatid,mensajeid=415,args=chat.settings['voz'])

            elif(commandid == 175): #wikipedia
                lines = allContent.split('\n')
                if(len(content) == 1):                                
                    send_message(chatid,mensajeid=306)
                elif(len(lines) < 2):
                    send_message(chatid,mensajeid=307)
                else:

                    title = lines[0][lines[0].find(' ')+1:]
                    addLogro(chat,userid,26)
                    writeWikipedia(chatid,title,'\n'.join(lines[1:]),client)

            elif(commandid == 178): #idioma
                if(len(content) < 2):
                    send_message(chatid,mensajeid=308)
                    return
                if(content[1] not in ['en','es']):
                    send_message(chatid,mensajeid=309)
                else:
                    h.connect()
                    h.chatSettings(chatid,idioma=content[1])
                    h.close()
                    chat.settings['idioma'] = content[1]
                    chat.idioma = content[1]
                    if(content[1] == 'en'):
                        send_message(chatid,mensajeid=310)
                    elif(content[1] == 'es'):
                        send_message(chatid,mensajeid=311)


            elif(commandid == 179): #dar
                print(tipos_dar)
                if(not usersid or len(content) < 2 or content[1] not in tipos_dar[chat.idioma]):
                    send_message(chatid,'uso: /dar [chocolate|flores|beso|cariño] @user: le das algo a alguien')
                    return
                t = tipos_dar[chat.idioma][content[1]]
                with open('lite/dar.es','r') as x:
                    textos_dar = x.read().split('\n')
                if(len(usersid) == 1 and usersid[0] == client.profile.id):
                    
                    if(t == 1):
                            send_voice_note(chatid,7)
                    elif(t == 2):
                        send_message(chatid,'gracias pero soy alergica a las flores')
                            # send_voice_note(chatid,2)
                    elif(t == 3):
                        send_imagen(chatid,'imgs/dar_beso.gif',sanitized=True)
                        # send_voice_note(chatid,2)
                        send_message(chatid,'¿Me estas dando un besito? nooooooooo')

                    elif(t == 4):
                        # send_voice_note(chatid,2)
                        send_message(chatid,'gracias uwu')
                        # send_imagen(chatid,'imgs/dar_cariño.gif',sanitized=True)
                else:

                    if(t == 1):
                        send_imagen(chatid,'imgs/dar_chocolate.gif',sanitized=True)
                    elif(t == 2):
                        send_imagen(chatid,'imgs/dar_flores.gif',sanitized=True)
                    elif(t == 3):
                        send_imagen(chatid,'imgs/dar_beso.gif',sanitized=True)
                    elif(t == 4):
                        send_imagen(chatid,'imgs/dar_cariño.gif',sanitized=True)
                addLogro(chat,userid,22)

                for u in usersid:
                    if(u == client.profile.id):
                        continue
                    send_message(chatid,textos_dar[t-1] % (getNickname(u,sub_client),getNickname(userid,sub_client)))
                    chat.dar[u] = (t,userid)
            elif(commandid == 180): #pedir
                if(not usersid or len(content) < 2 or content[1] not in tipos_pedir[chat.idioma]):
                    send_message(chatid,'uso: /pedir [cita|beso|matrimonio|noviazgo|divorcio] @user: le das algo a alguien')
                    return
                with open('lite/pedir.es','r') as x:
                    textos_pedir = x.read().split('\n')
                t = tipos_pedir[chat.idioma][content[1]]
                if(len(usersid) != 1 or usersid[0] != client.profile.id):
                    if(t == 1):
                        send_imagen(chatid,'imgs/pedir_cita.gif',sanitized=True)
                    elif(t == 2):
                        send_imagen(chatid,'imgs/pedir_cita.gif',sanitized=True)
                    elif(t == 3):
                        send_imagen(chatid,'imgs/pedir_cita.gif',sanitized=True)
                    elif(t == 4):
                        send_imagen(chatid,'imgs/pedir_cita.gif',sanitized=True)
                    elif(t == 5):
                        send_imagen(chatid,'imgs/divorce.gif',sanitized=True)


                for u in usersid:
                    if(u == client.profile.id):
                        if(t == 2):
                            h.connect()
                            h.addRecibido(userid,'besos')
                            h.close()
                            send_voice_note(chatid,2)
                            if(chatid not in channels):
                                send_message(chatid,'%s ¿Quieres un beso mio? Te lo doy uwu' % (getNickname(userid,sub_client)))
                            send_interaccion(chatid,'besar',userid,[u],sub_client,mensaje=False,idioma=chat.idioma,ecchi=ecchi)
                        elif(t == 1):
                            send_voice_note(chatid,3)
                            if(chatid not in channels):
                                send_message(chatid,'¿Una cita conmigo? ay >_< que pena tengo que preguntarle a mi dueño si me deja pero no creo ya que me hace trabajar 24/7')
                        elif(t == 3):
                            send_voice_note(chatid,5)
                            if(chatid not in channels):
                                send_message(chatid,'Ma ma ma ¿¡Matrimonio!? ae creo que es mucho :s me siento alagada pero no puedo toy chiquita.')
                        elif(t == 4):
                            send_voice_note(chatid,6)
                            if(chatid not in channels):
                                send_message(chatid,'¿Novios? ¿Tu y yo? %s' % (getNickname(userid,sub_client) ))
                                sleep(1)
                                send_message(chatid,'Dejame pensar... mmm')
                                sleep(1)
                                send_reply(chatid,'Nah',id)
                    else:
                        send_message(chatid,textos_pedir[t-1] % (getNickname(u,sub_client),getNickname(userid,sub_client)))
                        chat.pedidos[u] = (t,userid)

            elif(commandid == 181): #si
                if(userid in chat.pedidos):
                    h.connect()
                    t,u = chat.pedidos[userid]
                    if(t == 1):

                        h.addRecibido(userid,'citas')
                        h.addRecibido(u,'citas')
                        send_message(chatid,'Yo les preparo todo')
                        r = sub_client.start_chat([u,userid],message='Les prepare este chat para que tengan su cita uwu')
                        if(r[0] != 200):
                            send_message(chatid,'Chale no pude crearles un chat')
                        else:
                            c = r[1]['thread']['threadId']
                            img = random.choice(imagenesCita)
                            if(img not in cacheImagenesCita):
                                r = sub_client.upload_background(c,f='cita/fondos/' + img)
                                print(r)
                                cacheImagenesCita[img] = r
                                sub_client.edit_chat(c,title='cita',pinAnnouncement=True,announcement='cita de %s y %s' % (getNickname(u,sub_client),getNickname(userid,sub_client) ))
                            else:
                                r = cacheImagenesCita[img]
                                sub_client.edit_chat(c,backgroundImage=r,title='cita',pinAnnouncement=True,announcement='cita de %s y %s' % (getNickname(u,sub_client),getNickname(userid,sub_client)) )
                            h.botstate(1,0,comid,0,c)
                            h.close()
                            sub_client.transfer_host(chatid,[u,userid])
                            sleep(5)
                            h.connect()
                            newChat = chats.get(c)
                            if(newChat):
                                newChat.ops[u] = 3
                                newChat.ops[userid] = 3
                                h.opChat(chatid,newChat.ops)


                    elif(t == 2):
                        h.addRecibido(u,'besos')
                        send_message(chatid,'%s acepta darle un beso a %s' % (getNickname(userid,sub_client),getNickname(u,sub_client)))
                        send_interaccion(chatid,'besar',userid,[u],sub_client,mensaje=False,idioma=chat.idioma,ecchi=ecchi)
                    elif(t == 3):
                        h.addRecibido(userid,'matrimonios')
                        h.addRecibido(u,'matrimonios')
                        send_message(chatid,'¡Felicidades! %s. %s acepto tu propuesta de matrimonio.' % (getNickname(u,sub_client),getNickname(userid,sub_client)) )
                        send_interaccion(chatid,'matrimonio',userid,[u],sub_client,mensaje=False,idioma=chat.idioma,ecchi=ecchi)
                    elif(t == 4):
                        h.addRecibido(userid,'novios')
                        h.addRecibido(u,'novios')
                        send_message(chatid,'%s acepta ser novio/a de %s' % (getNickname(userid,sub_client),getNickname(u,sub_client)))
                    elif(t == 5):
                        r = h.divorce(userid,u)
                        if(r):
                            send_message(chatid,'Listo divorciados')
                        else:
                            send_message(chatid,'No se pueden divorciar')
                    chat.pedidos.pop(userid)

                if(userid in chat.dar):
                    h.connect()
                    addLogro(chat,userid,23,h)
                    t,u = chat.dar[userid]
                    if(t == 1):

                        h.addRecibido(userid,'chocolates')
                        send_message(chatid,'%s acepta los chocolates de %s' % (getNickname(userid,sub_client),getNickname(u,sub_client)))
                        if('comer_chocolate.gif' in cacheImagenes):
                            link = cacheImagenes['comer_chocolate.gif']
                        else:
                            link = good_upload(filename='imgs/comer_chocolate.gif')
                            cacheImagenes['comer_chocolate.gif'] = link
                        send_link(chatid,link,sanitized=True)

                    elif(t == 2):
                        h.addRecibido(userid,'flores')
                        send_message(chatid,'%s acepta las flores de %s' % (getNickname(userid,sub_client),getNickname(u,sub_client)))
                        if('tener_flores.gif' in cacheImagenes):
                            link = cacheImagenes['tener_flores.gif']
                        else:
                            link = good_upload(filename='imgs/tener_flores.gif',sanitized=True)
                            cacheImagenes['tener_flores.gif'] = link
                        send_link(chatid,link,sanitized=True)

                    elif(t == 3):
                        h.addRecibido(userid,'besos')
                        send_message(chatid,'%s acepta el beso de %s' % (getNickname(userid,sub_client),getNickname(u,sub_client)))

                        send_interaccion(chatid,'besar',u,[userid],sub_client,mensaje=False,idioma=chat.idioma,ecchi=ecchi)
                    elif(t == 4):
                        h.addRecibido(userid,'cariño')
                        send_message(chatid,'%s acepta el cariño de %s' % (getNickname(userid,sub_client),getNickname(u,sub_client)))
                        send_interaccion(chatid,'pat',u,[userid],sub_client,mensaje=False,idioma=chat.idioma,ecchi=ecchi)
                    chat.dar.pop(userid)
                h.close()
            elif(commandid == 182): #no
                if(userid in chat.pedidos):
                    send_voice_note(chatid,8)
                    t,u = chat.pedidos[userid]            
                    if(t == 1):
                        send_message(chatid,'bueno mas suerte para la proxima %s' % getNickname(u,sub_client) )
                    elif(t == 2):
                        send_message(chatid,'u_u bueno no te rindas %s seguro algun dia lo consigues ' % getNickname(u,sub_client) )
                    elif(t == 3):
                        if('boda_sad.gif' in cacheImagenes):
                            link = cacheImagenes['boda_sad.gif']
                        else:
                            link = good_upload(filename='imgs/boda_sad.gif')
                            cacheImagenes['boda_sad.gif'] = link
                        send_link(chatid,link,sanitized=True)

                        # send_imagen(chatid,'imgs/boda_sad.gif',sanitized=True)
                        send_message(chatid,'matrimonio puede ser algo extremo %s ¿Porque no mejor le pides otra cosa?' % getNickname(u,sub_client) )                        
                    elif(t == 4):
                        send_message(chatid,'F por %s' % getNickname(u,sub_client) )                        
                    chat.pedidos.pop(userid)
                if(userid in chat.dar):
                    addLogro(chat,userid,24)
                    t,u = chat.dar[userid]            
                    if(t == 1):
                        send_message(chatid,'te han rechazado los chocolates %s' % getNickname(u,sub_client) )
                    elif(t == 2):
                        send_message(chatid,'parece que a %s no le gustaron tus flores %s  ' % (getNickname(userid,sub_client),getNickname(u,sub_client)) )
                    elif(t == 3):
                        send_message(chatid,'%s rechazo tu beso %s ' % (getNickname(userid,sub_client),getNickname(u,sub_client)) )
                    elif(t == 4):
                        send_message(chatid,'%s no acepta tu cariño %s ' % (getNickname(userid,sub_client),getNickname(u,sub_client)) )
                    chat.dar.pop(userid)

            elif(commandid == 183): #asteriscos
                if(len(content) < 2):
                    send_message(chatid,mensajeid=621)
                else:
                    if(content[1] == palabras['si']):
                        chat.settings['asteriscos'] = 1
                        h.connect()
                        h.chatSettings(chatid,asteriscos=1)
                        h.close()
                        send_message(chatid,mensajeid=623)   
                    elif(content[1] == palabras['no']):
                        chat.settings['asteriscos'] = 0
                        h.connect()
                        h.chatSettings(chatid,asteriscos=0)  
                        h.close() 
                        send_message(chatid,mensajeid=622)   
            elif(commandid == 184): #ecchi
                if(chatThread['type'] == 2):
                    return
                ecchibot['client'].join_community(comid)
                sub_client.invite_to_chat([ecchibot['userid']],chatid)
                subc = ecchibot['client'].sub_client(comid)

                r = subc.send_message(chatid,'jeje hola')
                if(r == 200):
                    addLogro(chat,userid,42)
                else:
                    send_message(chatid,'but no body came')
            elif(commandid == 185): #burbuja
                    if(len(content) < 2):
                        h.connect()
                        items =  h.loadItems(tipo=1)
                        h.close()
                        text = 'Burbujas:\n\n'
                        for item in items:
                            if(item['descripcion']):
                                text += '#%d %s\n%s\n\n' % (item['id'],item['nombre'],item['descripcion'])
                            else:
                                text += '#%d %s\n\n' % (item['id'],item['nombre'])                            
                        text += 'Para ver mas informacion de un item usar /item [id]\nPara elegir una burbuja /burbuja [id]'
                        send_message(chatid,text)
                    elif(content[1].isdigit()):

                        itemid = int(content[1])
                        h.connect()
                        inventario = h.loadInventario(userid)
                        if(itemid not in inventario):
                            send_message(chatid,'No tienes ese item')
                            h.close()
                            return
                        item = h.loadItem(itemid)
                        h.close()
                        if(item['tipo'] != 1):
                            send_message(chatid,'Este item no es una burbuja')
                            return
                        bubbleid = item['link']
                        r = sub_client.purchase_bubble(bubbleid)
                        r = sub_client.apply_bubble(bubbleid,False,chatid=chatid)
                        if(r != 200):
                            send_message(chatid,mensajeid=625)
                        else:
                            send_message(chatid,mensajeid=626+random.randint(0,1))


            elif(commandid == 186): #copiarmarco
                if(len(usersid) != 1):
                    # send_message(chatid,mensajeid=628)
                    usersid = [userid]
                if(len(content) == 2 and content[1] == palabras['todos']):
                    toall = True
                else:
                    toall = False
                perfil = sub_client.get_user_info(usersid[0],raw=True)['userProfile']
                frameid = perfil['avatarFrame']['frameId']
                r = sub_client.purchase_frame(frameid)
                r = sub_client.apply_frame(frameid,toall)
                if(r == 200):
                    send_message(chatid,mensajeid=629)
                else:
                    send_message(chatid,mensajeid=630)
            elif(commandid == 187): #eventos
                h.connect()
                eventos = h.loadEventos()
                addLogro(chat,userid,25,h)
                h.close()
                if(not eventos):
                    send_message(chatid,'No hay eventos')
                    return
                for evento in eventos:
                    text = '[ciub]' + evento['nombre'] + '\n\n'
                    text += evento['descripcion'] + '\n\n'
                    text += 'Desde el %s' % (str(evento['inicio']).split(' ')[0] ) + '\n'
                    text += 'Hasta el %s' % (str(evento['final']).split(' ')[0] ) + '\n'
                    if(chatThread['type'] == 2):
                        link = good_upload(filename=evento['imagen'])
                        send_text_imagen_raw(chatid,text,filename=evento['imagen'],url=link)
                    else:
                        send_text_imagen_raw(chatid,text,evento['link'],evento['imagen'])

            elif(commandid == 188): #bienvenida
                if(len(content) < 2):
                    send_message(chatid,'uso: /bienvenida [sticker|mensaje]: configura un sticker y un mensaje de bienvenida.')
                    return
                if(content[1] == 'sticker'):
                    if(len(content) < 3):
                        h.connect()
                        stickers =  h.loadStickers()
                        inventario = h.loadInventario(userid)
                        h.close()
                        text = 'stickers:\n'
                        for sticker in stickers:
                            if(sticker['precio'] == 0 or sticker['id'] in inventario):
                                text += '%d. %s: %s\n' % (sticker['id'],sticker['nombre'],sticker['descripcion'])
                        text += '\nPara ver un sticker /item [id]'
                        send_message(chatid,text)
                    else:
                        if(not content[2].isdigit()):
                            send_message(chatid,'uso: /bienvenida sticker [id]: pone un sticker de bienvenida ')
                            return
                        h.connect()
                        inventario = h.loadInventario(userid)
                        itemid = int(content[2])
                        item = h.loadItem(itemid)
                        if(item and (itemid in inventario or item['precio'] == 0) ):
                            text = 'Ahora el sticker %s esta en la bienvenida' % (item['nombre'])
                            sub_client.send_message(chatid,text,embedType=0,embedLink=item['link'],embedTitle=item['nombre'],embedContent=item['descripcion'],el=item['media'])
                            h.chatStickerBienvenida(item['link'],chatid)
                            chat.stickerBienvenida = item['link']
                            addLogro(chat,userid,3,h)
                        else:
                            send_message(chatid,'No tienes el sticker %d' % (itemid))
                        h.close()
                elif(content[1] == 'mensaje'):
                    m = allContent[allContent.find(palabras['mensaje'])+len(palabras['mensaje']):].strip()
                    chat.mensaje = m
                    h.connect()
                    try:
                        h.chatMensaje(m,chatid)
                    except:
                        send_message(chatid,mensajeid=192)
                    else:
                        send_message(chatid,mensajeid=199)
                        addLogro(chat,userid,3,h)
                    h.close()
                    return

            elif(commandid == 189): #tienda
                if(len(content) < 2):
                    with open('tienda/%s/inicio.txt' % (chat.idioma),'r') as e:
                        text = e.read()
                    send_message(chatid,text)
                    return
                if(content[1] == 'comprar'):
                    if(len(content) < 3 or not content[2].isdigit()):
                        send_message(chatid,'uso: /tienda comprar [id]: compras un objeto ')
                    else:
                        objectId =  int(content[2])
                        h.connect()
                        cosa = h.loadItem(objectId)
                        items = h.loadInventario(userid)
                        if(objectId in items):
                            send_message(chatid,'Ya tienes ese item en tu inventario')
                            h.close()
                            return
                        if(cosa):
                            user = getUser(userid)
                            user.puntos = h.loadPuntosUser(userid)
                            if(cosa['precio'] > user.puntos):
                                send_message(chatid,'No tienes suficientes puntos')
                            else:
                                if(cosa['tipo'] == 3):
                                    h.updateUsosUser(userid,int(cosa['media']),int(cosa['link']))
                                h.addItemUser(userid,objectId)
                                h.updatePuntosUser(userid,user.puntos - cosa['precio'])
                                user.puntos -= cosa['precio']
                                send_message(chatid,'Compra de %s exitosa, puedes revisar tu /inventario para ver tus compras' % (cosa['nombre']))
                                addLogro(chat,userid,2,h)

                        else:
                            send_message(chatid,'No hay item #' + str(content[2]) )
                        h.close()
                elif(content[1] == 'stickers'):
                    h.connect()
                    items =  h.loadStickers()
                    h.close()
                    text = 'Stickers:\n\n'
                    for item in items:
                        if(item['descripcion']):
                            text += '#%d %s\n%s\n\n' % (item['id'],item['nombre'],item['descripcion'])
                        else:
                            text += '#%d %s\n\n' % (item['id'],item['nombre'])                            
                    text += 'Para ver mas informacion de un item usar /item [id]'
                    send_message(chatid,text)
                elif(content[1] == 'burbujas'):
                    h.connect()
                    items =  h.loadItems(tipo=1)
                    h.close()
                    text = 'Burbujas:\n'
                    for item in items:
                        if(item['descripcion']):
                            text += '#%d %s\n%s\n\n' % (item['id'],item['nombre'],item['descripcion'])
                        else:
                            text += '#%d %s\n\n' % (item['id'],item['nombre'])                            
                    text += 'Para ver mas informacion de un item usar /item [id]'
                    r = to_private_chat(userid,text,client,comid)
                    if(r):
                        send_message(chatid,'%s te envie los items al privado' % (getNickname(userid,sub_client)))
                    else:
                        send_message(chatid,'%s te intente enviar los items al privado pero no pude abrirte privado :(' % (getNickname(userid,sub_client)))

                elif(content[1] == 'comandos'):
                    h.connect()
                    items = h.loadItems(tipo=3)
                    h.close()
                    text = 'Comandos:\n'
                    for item in items:
                        if(item['descripcion']):
                            text += '#%d %s\n%s\nUsos: %d\n' % (item['id'],item['nombre'],item['descripcion'],int(item['link']) )
                        else:
                            text += '#%d %s\n\n' % (item['id'],item['nombre'])                            
                    text += 'Para ver mas informacion de un item usar /item [id]'
                    send_message(chatid,text)
                elif(content[1] == 'todo'):
                    h.connect()
                    items =  h.loadItems()
                    h.close()
                    text = 'Items de la tienda:\n\n'
                    tipos = {}
                    for i in items:
                        t = i['tipo']
                        if(t not in tipos):
                            tipos[t] = [i]
                        else:
                            tipos[t].append(i)
                    for tipo in tipos:
                        text += '[c]%ss\n\n' % (tipos_items[chat.idioma][tipo] )
                        for item in tipos[tipo]:
                            if(item['precio'] != 0):
                                text += '#%d %s\n%s\nPrecio: %dpts\n\n' % (item['id'],item['nombre'],item['descripcion'],item['precio'])
                    text += 'Para ver mas informacion de un item user /item [id]'
                    r = to_private_chat(userid,text,client,comid)
                    if(r):
                        send_message(chatid,'%s te envie los items al privado' % (getNickname(userid,sub_client)))
                    else:
                        send_message(chatid,'%s te intente enviar los items al privado pero no pude abrirte privado :(' % (getNickname(userid,sub_client)))

                elif(content[1] == 'puntos'):
                    with open('tienda/%s/puntos.txt' % (chat.idioma),'r') as x:
                        text = x.read()
                    user = getUser(userid)
                    h.connect()
                    user.puntos = h.loadPuntosUser(userid)
                    h.close()
                    text += '\n\nTienes %d puntos' % (user.puntos)
                    send_message(chatid,text)
                elif(content[1] == 'ayuda'):
                    with open('tienda/%s/ayuda.txt' % (chat.idioma),'r') as x:
                        text = x.read()
                    send_message(chatid,text)

                else:
                    send_message(chatid,'uso: /tienda [ayuda|stickers|burbujas|puntos|comprar|todo]')

            elif(commandid == 190): #inventario
                h.connect()
                inventario = h.loadInventario(userid)
                print(inventario)
                text = "Tu inventario:\n\n"
                tipos = {}
                for i in inventario:
                    item = h.loadItem(i)
                    descripcion = item['descripcion']
                    if(item['tipo'] == 3):
                        text += '#%d %s\n%s\nTipo: %s\nUsos restantes: %d\n\n' % (item['id'],item['nombre'],descripcion,tipos_items[chat.idioma][ item['tipo'] ],h.loadUsosUser(userid,int(item['media']) ) )
                    elif(descripcion):
                        text += '#%d %s\n%s\nTipo: %s\n\n' % (item['id'],item['nombre'],descripcion,tipos_items[chat.idioma][ item['tipo'] ] )
                    else:
                        text += '#%d %s\nTipo: %s\n\n' % (item['id'],item['nombre'],tipos_items[chat.idioma][ item['tipo'] ] )

                h.close()
                text += 'Para ver mas informacion de un item user /item [id]'
                send_message(chatid,text)
            elif(commandid == 191 or commandid == 198): #logros
                h.connect()
                ls = h.loadLogros(userid)
                h.close()
                if(len(content) >= 2 and content[1].isdigit()):
                    l = int(content[1])
                    if(l in ls):
                        l = logros[l]
                        text = '[c]%s\n\n%s\n\n[c]%d pts' % (l['nombre'],l['descripcion'],l['puntos'])
                        send_message(chatid,text)
                        return
                    else:
                        send_message(chatid,'No tienes el logro #%d' % (l))
                if(not ls):
                    send_message(chatid,'Todavia no tienes ningun logro')
                else:
                    text = 'Tus logros:\n'
                    for l in sorted(ls):
                        text += '#%d %s\n' % (l,logros[l]['nombre'])
                    text += 'Para ver detalles /logro [id]'
                    send_message(chatid,text)

            elif(commandid == 192): #item
                if(len(content) < 2 or not content[1].isdigit()):
                    send_message(chatid,'uso: /item [id]: muestra informacion de un item')
                else:
                    itemid = int(content[1])
                    h.connect()
                    item = h.loadItem(itemid)
                    h.close()
                    if(item):
                        text = 'ID: #%d\n' % (item['id'])
                        text += 'Nombre: %s\n' % (item['nombre'])
                        if(item['descripcion']):
                            text += 'Descripcion: %s\n' % (item['descripcion'])
                            descripcion = item['descripcion']
                        else:
                            descripcion = None
                        text += 'Tipo: %s\n' % (tipos_items[chat.idioma][item['tipo']])
                        if(item['precio']):
                            text += 'Precio: %dpts\n' % (item['precio'])
                        if(item['tipo'] == 3):
                            text += 'Usos: %d' % int(item['link'])
                            send_message(chatid,text)
                            
                        else:
                            sub_client.send_message(chatid,text,embedType=0,embedLink=item['link'],embedTitle=item['nombre'],embedContent=descripcion,el=item['media'])
                            
                    else:
                        send_message(chatid,'No se encontro ese item')
            elif(commandid == 193): #loteria
                # send_message(chatid,'Ya no hay mas loteria')
                h.connect()
                r = h.loadLottery(userid)
                h.close()
                if(r != None):
                    if(r == 1):
                        send_message(chatid,'Ya jugaste loteria hoy, tu resultado fue una moneda')
                    else:
                        send_message(chatid,'Ya jugaste loteria hoy, tu resultado fue: %d monedas' % (r))

                    return
                i = random.randint(1,100)
                r = sub_client.get_user_blogs(userid,size=25,raw=True)
                itemid = None
                nopoder = False
                if('blogList' in r):
                    if(len(r['blogList']) > 0):
                        for blog in r['blogList']:
                        # blog = r['blogList'][0]
                            if(not blog['tipInfo']['tippable']):
                                # send_message(chatid,'No puedes recibir donaciones')
                                nopoder = True
                            else:
                                itemid = blog['blogId']
                                tipo = 1
                                nopoder = False
                                break
                if(not itemid):
                    r = sub_client.get_user_wikis(userid,size=25,raw=True)
                    if('itemList' not in r):
                        send_message(chatid,'No tienes ningun blog ni wiki para donarte en caso de que ganes')
                        return
                    else:
                        if(len(r['itemList']) > 0):
                            for item in r['itemList']:
                                itemid = item['itemId']
                                wiki = sub_client.get_wiki_info(itemid,raw=True)['item']
                                if(not wiki['tipInfo']['tippable']):
                                    # send_message(chatid,'No puedes recibir donaciones')
                                    nopoder = True
                                else:
                                    nopoder = False
                                    break
                        tipo = 2
                if(nopoder):                    
                    send_message(chatid,'No puedes recibir donaciones')
                    return
                if(not itemid):
                    send_message(chatid,'No tienes ninguna wiki o blog en el cual donarte')
                    return
                nick = getNickname(userid,sub_client)
                h.connect()
                if(i <= 80):
                    h.playLottery(userid,0)
                    send_message(chatid,'Mas suerte la proxima %s' % (nick))
                    addLogro(chat,userid,47,h)
                elif(i > 80 and i <=90):
                    h.playLottery(userid,1)
                    send_message(chatid,'Felicidades %s ganaste una moneda' % (nick))
                    if(tipo == 1):
                        sub_client.send_coins(1,blogId=itemid)
                    elif(tipo == 2):
                        sub_client.send_coins(1,objectId=itemid)
                elif(i > 90 and i <=98):
                    h.playLottery(userid,2)
                    send_message(chatid,'Felicidades %s ganaste 2 monedas' % (nick))
                    if(tipo == 1):
                        sub_client.send_coins(2,blogId=itemid)
                    elif(tipo == 2):
                        sub_client.send_coins(2,objectId=itemid)
                else:
                    h.playLottery(userid,5)
                    send_message(chatid,'Felicidades %s ganaste 5 monedas' % (nick))
                    if(tipo == 1):
                        sub_client.send_coins(5,blogId=itemid)
                    elif(tipo == 2):
                        sub_client.send_coins(5,objectId=itemid)
                    addLogro(chat,userid,35,h)
                h.close()
            elif(commandid == 194): #add
                if(len(content) < 2):
                    send_message(chatid,'uso: /add [sticker|burbuja] nombre|precio|descripcion')
                    return
                if(content[1] == 'sticker'):
                    m = ' '.join(content[2:])
                    m = m.split('|')
                    if(len(m) < 3):
                        send_message(chatid,'uso: /add [sticker] nombre|precio|descripcion')
                        return
                    if(replyid):
                        message = sub_client.get_message_info(chatid,replyid)
                        mediaValue = message.json.get('mediaValue')
                        if(mediaValue):
                            if("/st1." not in mediaValue ):
                                mediaValue = client.upload_sticker(url=mediaValue)
                            r = sub_client.create_sticker_collection([{"name":"x","icon":mediaValue}])
                            stickerid = r['stickerCollection']['stickerList'][0]['stickerId']
                        else:

                            stickerid = message.json['extensions']['originalStickerId']
                        nombre = m[0]
                        precio = int(m[1])
                        descripcion = m[2]
                        h.connect()
                        h.addItemTienda(2,nombre,descripcion,precio,mediaValue,stickerid)
                        h.close()
                        send_message(chatid,'Sticker agregado a la tienda')
                elif(content[1] == 'burbuja'):
                    if(not replyid):
                        send_message(chatid,mensajeid=624)
                    else:
                        if(len(content) > 1 and content[1] == palabras['todos']):
                            toall = True
                        else:
                            toall = False
                        message = sub_client.get_message_info(chatid,replyid)
                        bubbleid = message.json.get('chatBubbleId')
                        if(bubbleid):
                            descripcion = m[0]
                            precio = int(m[1])
                            nombre = message.json.get('chatBubble').get('name')
                            mediaValue = message.json.get('chatBubble').get('coverImage')
                            h.connect()
                            h.addItemTienda(1,nombre,descripcion,precio,mediaValue,bubbleid)
                            h.close()

            elif(commandid == 195): #copiarburbuja
                if(replyid):
                    if((userid == bot['owner'] or userid == ley or comid == leyworld) ):
                        if(len(content) > 1 and content[1] == palabras['todos']):
                            toall = True
                        else:
                            toall = False
                        message = sub_client.get_message_info(chatid,replyid)
                        bubbleid = message.json.get('chatBubbleId')
                        if(bubbleid):
                            r = sub_client.purchase_bubble(bubbleid)
                            r = sub_client.apply_bubble(bubbleid,toall,chatid=chatid)
                            if(r != 200):
                                print('obteniendo burbuja')
                                bubble = sub_client.get_bubble(bubbleid)['chatBubble']
                                print(bubble)
                                templateid = bubble['templateId']
                                name = bubble['name']
                                print('templateid:',templateid)
                                if(not templateid and name != "Custom Bubble"):
                                    comids = bubble.get('availableNdcIds')
                                    if(comids):
                                        for c in comids:
                                            r = client.join_community(c)
                                            if(r != 200):
                                                continue
                                            neo_sub_client = client.sub_client(c)
                                            r = neo_sub_client.purchase_bubble(bubbleid)
                                            print(r)
                                            r = sub_client.apply_bubble(bubbleid,toall,chatid=chatid)
                                            print(r)
                                            if(r == 200):
                                                client.leave_community(c)
                                                break
                                            client.leave_community(c)
                                        if(r == 200):
                                            send_message(chatid,mensajeid=626+random.randint(0,1))
                                        else:
                                            send_message(chatid,mensajeid=625)

                                    return
                                zipResource = bubble['resourceUrl']
                                print('descargando zip')
                                response = requests.get(zipResource)
                                if(not templateid):
                                    n = tmp('zip')
                                    with open(n,'wb') as h:
                                        h.write(response.content)
                                    r = chat_bubble_zip(chatid,sub_client,n)
                                else:
                                    r = client.generate_bubble(templateid,data=response.content)
                                    print(r)
                                    bubbleid = r['chatBubble']['bubbleId']
                                    print('aplicando burbuja')
                                    r = sub_client.apply_bubble(bubbleid,toall,chatid=chatid)
                                if(r == 200):
                                    send_message(chatid,mensajeid=626+random.randint(0,1))
                                else:
                                    send_message(chatid,mensajeid=625)
                            else:
                                send_message(chatid,mensajeid=626+random.randint(0,1))
                    else:
                        send_message(chatid,mensajeid=67)

                else:
                    send_message(chatid,mensajeid=624)

            elif(commandid == 196): #despedida
                if(len(content) < 2):
                    send_message(chatid,'uso: /despedida [sticker|mensaje]: configura un sticker y un mensaje de despedida.')
                    return
                if(content[1] == 'sticker'):
                    if(len(content) < 3):
                        h.connect()
                        stickers =  h.loadStickers()
                        inventario = h.loadInventario(userid)
                        h.close()
                        text = 'stickers:\n'
                        for sticker in stickers:
                            if(sticker['precio'] == 0 or sticker['id'] in inventario):
                                text += '%d. %s: %s\n' % (sticker['id'],sticker['nombre'],sticker['descripcion'])
                        text += '\nPara ver un sticker /item [id]'
                        send_message(chatid,text)
                    else:
                        if(not content[2].isdigit()):
                            send_message(chatid,'uso: /bienvenida sticker [id]: pone un sticker de bienvenida ')
                            return
                        h.connect()
                        inventario = h.loadInventario(userid)
                        itemid = int(content[2])
                        item = h.loadItem(itemid)
                        if(item and (itemid in inventario or item['precio'] == 0) ):
                            text = 'Ahora el sticker %s esta en la despedida' % (item['nombre'])
                            sub_client.send_message(chatid,text,embedType=0,embedLink=item['link'],embedTitle=item['nombre'],embedContent=item['descripcion'],el=item['media'])
                            h.chatStickerDespedida(item['link'],chatid)
                            chat.stickerDespedida = item['link']
                            addLogro(chat,userid,45,h)
                        else:
                            send_message(chatid,'No tienes el sticker %d' % (itemid))
                        h.close()
                elif(content[1] == 'mensaje'):
                    m = allContent[allContent.find(palabras['mensaje'])+len(palabras['mensaje']):].strip()
                    if(not m):
                        send_message(chatid,'Borrando mensaje de despedida')
                        return
                    chat.mensajeDespedida = m
                    if('[nick]' not in m):
                        send_message(chatid,'Guardando mensaje sin [nick], el [nick] se reemplaza por el nickname del usuario')
                    try:
                        h.connect()
                        h.chatMensajeDespedida(m,chatid)
                        addLogro(chat,userid,45,h)
                        h.close()
                    except:
                        send_message(chatid,mensajeid=192)
                    else:
                        send_message(chatid,mensajeid=632)
                    return
            elif(commandid == 197): #puntos
                user = getUser(userid)
                h.connect()
                user.puntos = h.loadPuntosUser(userid)
                h.close()
                text = 'Tienes %d puntos' % (user.puntos)
                send_message(chatid,text)
            elif(commandid == 199): #usar
                if(len(content) < 2):
                    send_message(chatid,'uso: /usar [/comando]: Te permite usar un comando que hayas comprado ')
                    return
                if(content[1][1:] in comandosIdioma[chat.idioma]):
                    h.connect()
                    cid = comandosIdioma[chat.idioma][content[1][1:]]
                    usos = h.loadUsosUser(userid,cid)
                    if(usos > 0):
                        usos -= 1
                        if(usos == 0):
                            i = h.loadItemByMedia(cid)
                            if(i):
                                h.removeItemUser(userid,i)
                        c = allContent[allContent[1:].find('/')+1:]
                        print(c)
                        h.close()
                        r = executeCommand(chat,c,userid,usersid,replyid,replyuid,createdTime,chatThread,client,user=user,id=id,role=role,premiumCommand=cid,esperar=False)
                        if(r == True):
                            h.connect()
                            h.updateUsosUser(userid,cid,usos)
                    else:
                        send_message(chatid,'No tienes usos disponibles para el comando %s' % (content[1][1:]))
                    h.close()
            elif(commandid == 200): #sonidos
                if(len(content) < 2):
                    send_message(chatid,mensajeid=643)
                else:
                    if(content[1] == palabras['si']):
                        chat.settings['sonidos'] = 1
                        h.connect()
                        h.chatSettings(chatid,sonidos=1)
                        h.close()
                        send_message(chatid,mensajeid=645)   
                    elif(content[1] == palabras['no']):
                        chat.settings['sonidos'] = 0
                        h.connect()
                        h.chatSettings(chatid,sonidos=0)   
                        h.close()
                        send_message(chatid,mensajeid=644)   
            elif(commandid == 201): #curiosidad
                text = random.choice(facts[chat.idioma])
                send_message(chatid,text)
                addLogro(chat,userid,54)
            elif((commandid >= 202 and commandid <= 207) or commandid == 210 or commandid == 211): #ave #zorro #panda #koala #perro #gato #mapache #canguro
                if(commandid == 202):
                    animal = 'birb'
                elif(commandid == 203):
                    animal = 'fox'
                elif(commandid == 204):
                    animal = 'panda'
                elif(commandid == 205):
                    animal = 'koala'
                elif(commandid == 206):
                    animal = 'dog'
                elif(commandid == 207):
                    animal = 'cat'
                elif(commandid == 210):
                    animal = 'racoon'
                elif(commandid == 211):
                    animal = 'kangaroo'
                if(commandid == 202):
                    r = requests.get('https://some-random-api.ml/facts/bird').content
                else:
                    r = requests.get('https://some-random-api.ml/facts/' + animal).content
                r = json.loads(r)
                print(r)
                text = r['fact']
                if(chat.idioma != 'en'):
                    text = translator.translate(text,dest=chat.idioma).text
                img = requests.get('https://some-random-api.ml/img/' + animal).json()['link']
                name = img[8:].replace('/','')
                d = 'animales/%s/imagenes/' % (animal)
                if(name in imagenesAnimales):
                    output = imagenesAnimales[name]
                else:
                    data = requests.get(img).content
                    filename = d + name
                    with open(filename,'wb') as h:
                        h.write(data)
                    output = 'resize_' + name + '.png'
                    outputfile = d + output
                    convert(url=img,output=outputfile)
                    imagenesAnimales[name] = output
                send_text_imagen_raw(chatid,text,url=img,filename=d + output)

            elif(commandid == 208 or commandid == 209): #pokedex #pokemon
                if(len(content) != 2):
                    send_message(chatid,mensajeid=652)
                else:
                    if(content[1].isdigit()):
                        result = requests.get('https://some-random-api.ml/pokedex?id=%d' % (int(content[1])) ).text
                    else:
                        result = requests.get('https://some-random-api.ml/pokedex?pokemon=%s' % (content[1])).text
                    result = json.loads(result)

                    if('error' in result):
                        text = result['error']
                        if(chat.idioma != 'en'):
                            text = translator.translate(text,dest=chat.idioma).text
                        send_message(chatid,text)
                    else:
                        ms = mensajes[chat.idioma]
                        descripcion = result['description']
                        tipos = ' '.join(result['type'])
                        habilidades = ' '.join(result['abilities'])
                        especies = ' '.join(result['species'])
                        if(chat.idioma != 'en'):
                            # print(tipos)
                            # print(habilidades)
                            # print(especies)
                            try:
                                tipos = translator.translate(tipos,dest=chat.idioma).text                            
                            except:
                                PrintException()
                            try:
                                descripcion = translator.translate(descripcion,dest=chat.idioma).text                            
                            except:
                                PrintException()
                            try:
                                habilidades = translator.translate(habilidades,dest=chat.idioma).text                            
                            except:
                                PrintException()
                            try:
                                especies = translator.translate(especies,dest=chat.idioma).text                            
                            except:
                                PrintException()
                        text = ms[370] % (result['name']) + '\n\n'
                        text += 'id: %s' % (result['id']) + '\n\n'
                        text += ms[646] % (tipos) + '\n\n'
                        text += ms[647] % (habilidades) + '\n\n'
                        text += ms[648] % (result['weight']) + '\n\n'
                        text += ms[649] % (result['height']) + '\n\n'
                        text += ms[650] % (especies) + '\n\n'
                        text += ms[651] % (result['base_experience']) + '\n\n'
                        text += ms[19] % (descripcion) + '\n'
                        img = result['sprites']['animated']
                        # img = requests.get(img).content
                        img = urlAmino(img,sanitized=True)
                        print(img)
                        sub_client.send_message(chatid,message=text,embedType=0,el=img,embedTitle=result['name'],embedContent=descripcion)
            elif(commandid == 212): #chiste
                if(chat.idioma == 'es'):
                    send_message(chatid,'Los chistes son tan malos que los quite xd')
                    return
                r = requests.get('https://some-random-api.ml/joke').content
                r = json.loads(r)
                print(r)
                text = r['joke']
                if(chat.idioma != 'en'):
                    text = translator.translate(text,dest=chat.idioma).text
                send_message(chatid,text)
                addLogro(chat,userid,53)
            elif(commandid == 213): #licencia
                if(len(content) < 2):
                    send_message(chatid,mensajeid=684)
                else:
                    send_message(chatid,mensajeid=685)
                    if(len(usersid) == 1):
                        # print('aqui en 1')
                        c = allContent[1:]
                        c = re.sub("‎‏" + ".*" + "‬‭","",c)
                        licencia(chatid,usersid[0],c,userid,idioma=chat.idioma)
                    else:
                        licencia(chatid,userid,allContent[1:],idioma=chat.idioma)
                    if( 'para usar el bot' in m):
                        addLogro(chat,userid,55)
                    for x in ['coger','follar','violar','tirar','tener sexo']:
                        if(x in m):
                            if( 'al admin' in m or 'a el admin' in m):
                                addLogro(chat,userid,61)
                                break
                    addLogro(chat,userid,52)

            elif(commandid == 214): #todos
                if(len(content) < 2):
                    send_message(chatid,mensajeid=653)
                else:
                    if(content[1] == palabras['si']):
                        chat.settings['todos'] = 1
                        h.connect()
                        h.chatSettings(chatid,todos=1)
                        h.close()
                        send_message(chatid,mensajeid=654)   
                    elif(content[1] == palabras['no']):
                        chat.settings['todos'] = 0
                        h.connect()
                        h.chatSettings(chatid,todos=0)   
                        h.close()
                        send_message(chatid,mensajeid=655)   

            elif(commandid == 215): #goal
                goals = os.listdir('goals/original')
                g = random.choice(goals)
                g = g[:g.find('_')+1]
                goals = [i for i in goals if i.startswith(g)]
                n = len(goals)
                i = 1
                for g in goals:
                    if(g.endswith('gif')):
                        send_imagen(chatid,'goals/original/' + g,sanitized=True)
                    else:
                        # with open('goals/url/' + g,'r') as h:
                        #     url = h.read()
                        url = good_upload(filename='goals/original/' + g,sanitized=True)
                        send_text_imagen_raw(chatid,'%d/%d' % (i,n),filename='goals/png/' + g + '.png',url=url)
                    i += 1

            elif(commandid == 216): #besar
                if(m):
                    m = re.sub("‎‏" + ".*" + "‬‭","",m)
                if(m):   
                    hecho = False
                    if('mejilla' in m):
                        send_interaccion(chatid,'mejilla',userid,usersid,sub_client,idioma=chat.idioma,ecchi=ecchi)
                        addLogro(chat,userid,56)
                        hecho = True
                    for p in palabrasjum:
                        if(p in m):
                            send_interaccion(chatid,'sonrojar',client.profile.id,[],sub_client,idioma=chat.idioma,ecchi=ecchi,mensaje=False)
                            send_message(chatid,'ahhhhhh nooooooo >~< que cosas dices')
                            hecho = True
                            addLogro(chat,userid,57)
                            break
                    if(not hecho):
                        send_interaccion(chatid,'besar',userid,usersid,sub_client,idioma=chat.idioma,ecchi=ecchi)                    
                else:
                    send_interaccion(chatid,'besar',userid,usersid,sub_client,idioma=chat.idioma,ecchi=ecchi)   
            elif(commandid == 217): #telefono
                if(len(content) < 2 ):
                    send_message(chatid,'uso: /telefono [llamar|colgar]: llamas a alguien random en esta comunidad, si contesta les enviare a los 2 un link para que se comuniquen')
                else:
                    if(content[1] == 'llamar'):
                        if(len(content) < 3):
                            send_message(chatid,'uso: /telefono llamar [mensaje inicial]: Un mensaje corto para iniciar la conversacion')
                        else:
                            if(comid not in telefonos):
                                telefonos[comid] = {}
                            if(comid not in resultadosTelefonos):
                                resultadosTelefonos[comid] = {}
                            if(userid in telefonos[comid]):
                                send_message(chatid,'Ya estas haciendo una llamada')
                                return
                            m = ' '.join(content[2:])
                            e = threading.Event()
                            send_message(chatid,'llamando... te avisare cuando alguien conteste. Mientras recuerda que te paso los detalles por privado asi que ten mi privado abierto.')
                            i = random.choice(['telefono_rosado.gif','telefono_ventana.gif','chica_telefono.gif'])
                            send_imagen(chatid,imgdir + i,sanitized=True)
                            addLogro(chat,userid,58)
                            if(telefonos[comid]):
                                result = random.choice(list(telefonos[comid].keys()) )
                                e,nm = telefonos[comid][result]
                                resultadosTelefonos[comid][result] = (userid,m)
                                telefonos[comid].pop(result)
                                print('cambiado el valor de',result)
                                e.set()
                                send_message(chatid,'Alguien contesto a tu llamada %s te paso los detalles por privado' % (getNickname(userid,sub_client)))
                                r = sub_client.start_chat([userid],message='')
                                if(r[0] == 200):
                                    userchat = r[1]['thread']['threadId']
                                    sub_client.send_message(userchat,'Este usuario quiere comunicarse contigo, si quieres hablar con el solo ve a su perfil y abre su privado',embedType=0,embedId=result,embedContent=nm,messageType=57)
                                    addLogro(chat,userid,59)
                                else:
                                    send_message(chatid,'Chale no pude abrirte privado para enviarte la informacion')
                            else:
                                telefonos[comid][userid] = (e,m) 
                                e.wait(180)
                                if(e.is_set()):

                                    print('revisando el valor de',userid)
                                    result,m = resultadosTelefonos[comid][userid]
                                    send_message(chatid,'Alguien contesto a tu llamada %s te paso los detalles por privado' % (getNickname(userid,sub_client)))
                                    r = sub_client.start_chat([userid],message='')
                                    if(r[0] == 200):
                                        userchat = r[1]['thread']['threadId']
                                        sub_client.send_message(userchat,'Este usuario quiere comunicarse contigo, si quieres hablar con el solo ve a su perfil y abre su privado',embedType=0,embedId=result,embedContent=m,messageType=57)
                                        addLogro(chat,userid,59)
                                    else:
                                        send_message(chatid,'Chale no pude abrirte privado para enviarte la informacion')
                                else:
                                    telefonos[comid].pop(userid)
                                    send_message(chatid,'Chale nadie contesto a tu llamada %s' % (getNickname(userid,sub_client)))
                    elif(content[1] == 'colgar'):
                        if(comid not in telefonos):
                            telefonos[comid] = {}
                        if(comid not in resultadosTelefonos):
                            resultadosTelefonos[comid] = {}

                        if(userid in telefonos[comid]):
                            telefonos[comid].pop(userid)
                            send_message(chatid,'Colgaste')
                        else:
                            send_message(chatid,'No estabas llamando')

            elif(commandid == 218): #waifu
                waifu = random.choice(waifuValues)
                waifuId = waifu['wikiId']
                if(waifuId not in likesWaifu):
                    h.connect()
                    r = h.loadLikesWaifu(waifuId)
                    h.close()
                    likesWaifu[waifuId] = r[0]
                    trashWaifu[waifuId] = r[1]
                    likes = r[0]
                    trash = r[1]
                else:
                    likes = likesWaifu[waifuId]
                    trash = trashWaifu[waifuId]
                text = '[cb]    %s\n\n' % waifu['nombre']
                text += '[ci] %s\n\n' % waifu['origen']
                text += '[ci] ❤️ %d\n\n' % len(likes)
                text += '[ci] 🗑 %d\n\n' % len(trash)

                resize = 'waifus/resize_' + str(waifuId) + '.png'
                link = good_upload(filename=resize,sanitized=True)
                send_text_imagen_raw(chatid,text,filename=resize,url=link)
                lastWaifu[chatid] = waifuId

            elif(commandid == 219): #husbando

                waifu = random.choice(husbandoValues )
                waifuId = waifu['wikiId']
                if(waifuId not in likesWaifu):
                    h.connect()
                    r = h.loadLikesWaifu(waifuId)
                    h.close()
                    likesWaifu[waifuId] = r[0]
                    trashWaifu[waifuId] = r[1]
                    likes = r[0]
                    trash = r[1]
                else:
                    likes = likesWaifu[waifuId]
                    trash = trashWaifu[waifuId]
                text = '[cb]    %s\n\n' % waifu['nombre']
                text += '[ci] %s\n\n' % waifu['origen']
                text += '[ci] ❤️ %d\n\n' % len(likes)
                text += '[ci] 🗑 %d\n\n' % len(trash)
                f = 'waifus/' + str(waifuId) + '.png'

                resize = 'waifus/resize_' + str(waifuId) + '.png'
                link = good_upload(filename=resize,sanitized=True)
                send_text_imagen_raw(chatid,text,filename=resize,url=link)
                lastWaifu[chatid] = waifuId

            elif(commandid == 220): #harem
                if(userid in harems):
                    harem = harems[userid]
                else:
                    h.connect()
                    harem = h.loadHarem(userid)
                    h.close()
                    harems[userid] = harem

                if(harem):
                    if(len(content) == 2 and content[1].isdigit()):
                        i = int(content[1])-1
                        if(i >= len(harem) or i < 0):
                            send_message(chatid,mensajeid=678)
                            return
                        waifuId = harem[i]
                        send_waifu(chatid,waifuId,client)

                    else:
                        text = 'Tu harem:\n'
                        n = 1
                        for i in harem:
                            w = allWaifus[i]
                            text += '[cu]%d. %s\n[ci]%s\n\n' % (n,w['nombre'],w['origen'])
                            n += 1
                        text += 'Puedes usar /harem [numero] para ver mas informacion'
                        send_message(chatid,text)
                else:
                    send_message(chatid,mensajeid=673)

            elif(commandid == 221): #reclamar
                h.connect()
                i = h.loadReclamosWaifu(userid)
                if(userid in harems):
                    harem = harems[userid]
                else:
                    harem = h.loadHarem(userid)
                    harems[userid] = harem
                h.close()
                if(chatid not in lastWaifu):
                    send_message(chatid,mensajeid=674,args=i)
                else:
                    if(i <= 0 ):
                        send_message(chatid,mensajeid=675)
                        return
                    i -= 1
                    lastWaifuId = lastWaifu[chatid]
                    waifu = allWaifus[lastWaifuId]
                    if(lastWaifuId in harem):
                        send_message(chatid,mensajeid=677,args=waifu['nombre'])
                    else:
                        send_message(chatid,mensajeid=676,args=(waifu['nombre']))
                        harem.append(lastWaifuId)
                        h.connect()
                        h.updateReclamos(userid,i)

                        h.updateHarem(userid,harem)
                        h.close()


            elif(commandid == 222): #like
                if(usersid):
                    for u in usersid:
                        send_message(chatid,mensajeid=666,args=(getNickname(u,sub_client)))      
                else:              
                    if(chatid not in lastWaifu):
                        send_message(chatid,mensajeid=663)
                    else:
                        lastWaifuId = lastWaifu[chatid]
                        nombre = allWaifus[lastWaifuId]['nombre']
                        if(userid in likesWaifu[lastWaifuId]):
                            send_message(chatid,mensajeid=668,args=(nombre))
                        else:
                            send_message(chatid,mensajeid=666,args=(nombre))    
                            if(lastWaifuId not in likeWaifuLock):
                                likeWaifuLock[lastWaifuId] = threading.Lock()
                            likeWaifuLock[lastWaifuId].acquire()    
                            likes = likesWaifu[lastWaifuId]            
                            likes.append(userid)
                            h.connect()
                            h.likeWaifu(lastWaifuId,likes)
                            h.close()
                            likeWaifuLock[lastWaifuId].release()
            elif(commandid == 223): #trash
                if(usersid):
                    for u in usersid:
                        send_message(chatid,mensajeid=667,args=(getNickname(u,sub_client)))      
                else:              
                    if(chatid not in lastWaifu):
                        send_message(chatid,mensajeid=663)
                    else:
                        lastWaifuId = lastWaifu[chatid]
                        nombre = allWaifus[lastWaifuId]['nombre']
                        if(userid in trashWaifu[lastWaifuId]):
                            send_message(chatid,mensajeid=668,args=(nombre))
                        else:
                            send_message(chatid,mensajeid=667,args=(nombre))    
                            if(lastWaifuId not in trashWaifuLock):
                                trashWaifuLock[lastWaifuId] = threading.Lock()
                            trashWaifuLock[lastWaifuId].acquire()    
                            likes = trashWaifu[lastWaifuId]            
                            likes.append(userid)
                            h.connect()
                            h.trashWaifu(lastWaifuId,likes)
                            h.close()
                            trashWaifuLock[lastWaifuId].release()

            elif(commandid == 224): #unlike
                if(usersid):
                    for u in usersid:
                        send_message(chatid,mensajeid=669,args=(getNickname(u,sub_client)))      
                else:              
                    if(chatid not in lastWaifu):
                        send_message(chatid,mensajeid=663)
                    else:
                        lastWaifuId = lastWaifu[chatid]
                        nombre = allWaifus[lastWaifuId]['nombre']
                        if(userid not in likesWaifu[lastWaifuId]):
                            send_message(chatid,mensajeid=670,args=(nombre))
                        else:
                            send_message(chatid,mensajeid=669,args=(nombre))    
                            if(lastWaifuId not in likeWaifuLock):
                                likeWaifuLock[lastWaifuId] = threading.Lock()
                            likeWaifuLock[lastWaifuId].acquire()    
                            likes = likesWaifu[lastWaifuId]      
                            likes.remove(userid)      
                            h.connect()
                            h.likeWaifu(lastWaifuId,likes)
                            h.close()
                            likeWaifuLock[lastWaifuId].release()

            elif(commandid == 225): #untrash
                if(usersid):
                    for u in usersid:
                        send_message(chatid,mensajeid=672,args=(getNickname(u,sub_client)))      
                else:              
                    if(chatid not in lastWaifu):
                        send_message(chatid,mensajeid=663)
                    else:
                        lastWaifuId = lastWaifu[chatid]
                        nombre = allWaifus[lastWaifuId]['nombre']
                        if(userid not in trashWaifu[lastWaifuId]):
                            send_message(chatid,mensajeid=671,args=(nombre))
                        else:
                            send_message(chatid,mensajeid=672,args=(nombre))    
                            if(lastWaifuId not in trashWaifuLock):
                                trashWaifuLock[lastWaifuId] = threading.Lock()
                            trashWaifuLock[lastWaifuId].acquire()    
                            likes = trashWaifu[lastWaifuId]            
                            likes.remove(userid)
                            h.connect()
                            h.trashWaifu(lastWaifuId,likes)
                            h.close()
                            trashWaifuLock[lastWaifuId].release()

            elif(commandid == 226 or commandid == 227): #buscarwaifu
                if(not m):
                    send_message(chatid,mensajeid=679)
                else:
                    query = m.lower()
                    results = []
                    text = mensajes[chat.idioma][361] + '\n'
                    if(commandid == 226):
                        busqueda = waifus
                    else:
                        busqueda = husbandos  
                    n = 1                      
                    for k,w in busqueda.items():
                        nombre = w['nombre'].lower()
                        if(query in nombre):
                            results.append(k)
                            text += '%d. %s' % (n,w['nombre']) + '\n'
                            n += 1
                    text += '\n'
                    if(results):
                        waifuSearch[chatid] = results
                        countWaifuSearch[chatid] = 10
                        text += mensajes[chat.idioma][468]
                        send_message(chatid,text)          
                    else:
                        send_message(chatid,mensajeid=681)        

            elif(commandid == 228): #waifuwiki
                t1 = time()
                if(chatid not in lastWaifu):
                    send_message(chatid,mensajeid=663)
                else:
                    lastWaifuId = lastWaifu[chatid]
                    send_waifu(chatid,lastWaifuId,client,withWiki=True)

            elif(commandid == 229): #bienvenidas
                if(len(content) < 2):
                    send_message(chatid,mensajeid=687)
                else:
                    if(content[1] == palabras['si']):
                        chat.settings['bienvenidas'] = 1
                        h.connect()
                        h.chatSettings(chatid,bienvenidas=1)
                        h.close()
                        send_message(chatid,mensajeid=689)   
                    elif(content[1] == palabras['no']):
                        chat.settings['bienvenidas'] = 0
                        h.connect()
                        h.chatSettings(chatid,bienvenidas=0)   
                        h.close()
                        send_message(chatid,mensajeid=688)   
            elif(commandid == 230): #arcoiris
                values = getMediaValues(chatid,None,usersid,replyid)
                if(values):
                    for v in values:
                        arcoiris(chatid,v,client,ecchi=ecchi)
                else:
                    userinfo = sub_client.get_user_info(userid,raw=True)['userProfile']
                    icon = userinfo['icon']
                    if(icon):
                        arcoiris(chatid,icon,client,ecchi=ecchi)
            elif(commandid == 231): #botar
                if(len(content) < 2):
                    send_message(chatid,'uso: /botar [numero de waifu]: botas una waifu de tu harem')
                else:
                    if(userid in harems):
                        harem = harems[userid]
                    else:
                        h.connect()
                        harem = h.loadHarem(userid)
                        h.close()
                        harems[userid] = harem

                    if(harem):
                        if(len(content) == 2 and content[1].isdigit()):
                            i = int(content[1])-1
                            if(i >= len(harem) or i < 0):
                                send_message(chatid,mensajeid=678)
                                return
                            waifuId = harem[i]
                            waifu = allWaifus[waifuId]
                            t = waifu['tipo']
                            if(t == 'waifu'):
                                send_message(chatid,'Haz lanzado a la pobre %s fuera de tu harem. Pero hey tienes mas espacio para meter a alguien mas' % (waifu['nombre']))
                            else:
                                send_message(chatid,'Le pediste amablemente a %s que se fuera y se fue. Puedes reclamar a alguien mas' % (waifu['nombre']))
                            del harem[i]
                            h.connect()
                            i = h.loadReclamosWaifu(userid)
                            h.updateReclamos(userid,i+1)
                            h.updateHarem(userid,harem)
                            h.close()

                        else:
                            text = 'Tu harem:\n'
                            n = 1
                            for i in harem:
                                w = allWaifus[i]
                                text += '[cu]%d. %s\n[ci]%s\n\n' % (n,w['nombre'],w['origen'])
                                n += 1
                            text += 'Puedes usar /harem [numero] para ver mas informacion'
                            send_message(chatid,text)
                    else:
                        send_message(chatid,mensajeid=673)
            elif(commandid == 232 or commandid == 234): #lugar #ficha
                if(len(content) < 2):
                    if(commandid == 232):
                        send_message(chatid,'uso: %s [crear|borrar]: creas o borras un lugar del chat' % (content[0]))
                    else:
                        send_message(chatid,'uso: %s [crear|borrar]: creas o borras una de tus fichas ' % (content[0]))
                else:
                    if(content[1] == 'crear'):
                        ln = allContent.split('\n')
                        if(len(ln[0].split(' ') ) < 3 ):
                            send_message(chatid,'uso: %s crear [nombre o link de la wiki]' % (content[0]) )
                            return
                        if(content[2].startswith('http://aminoapps.com/p/')):
                            wikiId = wikiByLink(content[1])
                            if(not wikiId):
                                send_message(chatid,'link invalido para crear un lugar')
                            else:
                                wiki = sub_client.get_wiki_info(wikiId,raw=True)['item']
                                mediaList = wiki['mediaList']
                                if(len(mediaList) < 1):
                                    send_message(chatid,'La wiki no tiene imagenes')
                                    return
                                icon = mediaList[0][1]
                                nombre = wiki['label']
                                if(userid not in fichas[comid]):
                                    fichas[comid][userid] = {}
                                if(chatid not in fichas[0]):
                                    fichas[0][chatid] = {}

                                if(len(nombre) > 50):
                                    send_message(chatid,'El nombre es demasiado largo')
                                    return
                                if(commandid == 232):
                                    if(nombre in fichas[0][chatid]):
                                        send_message(chatid,'Ya hay un lugar con ese nombre')
                                        return
                                else:
                                    if(nombre in fichas[comid][userid]):
                                        send_message(chatid,'Ya tienes una ficha con ese nombre')
                                        return
                                if(commandid == 232):
                                    objectId = chatid
                                else:
                                    objectId = userid
                                props = wiki['extensions']['props']
                                descripcion = ''
                                for p in props:
                                    if(p['title'].lower() == 'descripcion' or p['title'].lower() == 'descripción'):
                                        descripcion = p['value']
                                ficha = {
                                    "nombre":nombre,
                                    "objectId":objectId,
                                    "descripcion": descripcion,
                                    "wikiId":wikiId,
                                    "icon":icon,
                                    "comid":0
                                }
                                dataFicha[chatid] = (ficha,userid)
                                if(commandid == 232):

                                    if(objectId not in fichas[0]):
                                        fichas[0][objectId] = {}    
                                    fichas[0][objectId][nombre] = [ficha]
                                else:
                                    ficha['comid'] = comid
                                    if(objectId not in fichas[comid]):
                                        fichas[comid][objectId] = {}    
                                    fichas[comid][objectId][nombre] = [ficha]

                                h.connect()
                                h.ficha(nombre,descripcion,objectId,wikiId,icon,ficha['comid'])
                                h.close()
                                send_message(chatid,'Se creo el lugar %s' % (ficha['nombre']))
                                send_ficha(chatid,ficha)
                        else:
                            if(replyid):
                                message = sub_client.get_message_info(chatid,replyid).json
                                icon = message.get('mediaValue')
                            else:
                                icon=None
                            if(len(content) > 2):
                                m = ' '.join(content[2:])
                            else:
                                send_message(chatid,'uso: %s crear [nombre o link de la wiki]' % (content[0]))
                            if(icon):
                                link = good_upload(url=icon)
                                if(not link):
                                    send_message(chatid,'La imagen seleccionada no es valida')
                                else:
                                    subc = client.sub_client(15391148)
                                    subc.post_file([[100,link,None]],'0ce1a0f6-c438-42be-ab68-bc09e365bda1')
                            ln = m.split('\n')
                            nombre = ln[0]
                            if(chatid not in fichas[0]):
                                fichas[0][chatid] = {}
                            if(comid not in fichas):
                                fichas[comid] = {}
                            if(userid not in fichas[comid]):
                                fichas[comid][userid] = {}
                            if(len(nombre) > 50):
                                send_message(chatid,'El nombre es demasiado largo')
                                return
                            if(commandid == 232):
                                if(nombre in fichas[0][chatid]):
                                    send_message(chatid,'Ya hay un lugar con ese nombre')
                                    return
                            else:
                                if(nombre in fichas[comid][userid]):
                                    send_message(chatid,'Ya tienes una ficha con ese nombre')
                                    return

                            if(len(ln) > 1):
                                descripcion = '\n'.join(ln[1:])
                            else:
                                descripcion = None
                            if(commandid == 232):
                                objectId = chatid
                            else:
                                objectId = userid

                            wikiId = None
                            ficha = {
                                "nombre":nombre,
                                "objectId":objectId,
                                "descripcion": descripcion,
                                "wikiId":wikiId,
                                "icon":icon,
                                "comid":0
                            }
                            if(commandid == 234):
                                ficha['comid'] = comid
                            dataFicha[chatid] = (ficha,userid)
                            if(not descripcion):
                                if(commandid == 232):
                                    send_message(chatid,'Ahora envie un mensaje con la descripcion del lugar')
                                else:
                                    send_message(chatid,'Ahora envie un mensaje con la descripcion de tu ficha')

                            else:
                                if(not icon):

                                    if(commandid == 232):
                                        send_message(chatid,'Ahora envie la imagen del lugar')
                                    else:
                                        send_message(chatid,'Ahora envia una imagen para tu ficha')

                                else:
                                    crearFicha(ficha)
                                    if(commandid == 232):
                                        send_message(chatid,'Se creo el lugar %s' % (ficha['nombre']))
                                    else:
                                        send_message(chatid,'Se creo la ficha %s' % (ficha['nombre']))

                                    send_ficha(chatid,ficha)
                                    dataFicha.pop(chatid)

                    elif(content[1] == 'borrar'):
                        if(len(content) < 3):
                            send_message(chatid,'uso: %s borrar [nombre]' % (content[0]))
                        else:
                            m = ' '.join(content[2:])
                            if(commandid == 232):
                                if(chatid not in fichas[0]):
                                    fichas[0][chatid] = {}
                                if(m in fichas[0][chatid]):
                                    send_message(chatid,'Eliminando %s' % (m))
                                    ficha = fichas[0][chatid][m]
                                    h.connect()
                                    h.borrarFicha(ficha['comid'],ficha['objectId'],ficha['nombre'])
                                    fichas[0][chatid].pop(m)
                            else:
                                if(userid not in fichas[comid]):
                                    fichas[comid][userid] = {}
                                if(m in fichas[comid][userid]):
                                    send_message(chatid,'Eliminando %s' % (m))
                                    ficha = fichas[comid][userid][m]
                                    h.connect()
                                    h.borrarFicha(ficha['comid'],ficha['objectId'],ficha['nombre'])
                                    fichas[comid][userid].pop(m)


            elif(commandid == 233): #lugares
                if(chatid not in fichas[0]):
                    fichas[0][chatid] = {}
                if(not fichas[0][chatid]):                    
                    send_message(chatid,'Este chat no tiene ningun lugar registrado')
                else:
                    send_message(chatid,'Lugares de este chat:')
                    for lugar in fichas[0][chatid].values():
                        send_ficha(chatid,lugar)
            elif(commandid == 235): #fichas
                if(comid not in fichas):
                    fichas[comid] = {}
                if(userid not in fichas[comid]):
                    fichas[comid][userid] = {}
                if(not fichas[comid][userid]):                    
                    send_message(chatid,'No tienes ninguna ficha')
                else:
                    send_message(chatid,'Tus fichas en esta comunidad:')
                    for lugar in fichas[comid][userid].values():
                        send_ficha(chatid,lugar)
            elif(commandid == 236): #ir
                if(not m):
                    send_message(chatid,'uso: /ir [nombre del lugar]')
                else:
                    lugares = fichas[0].get(chatid,{})
                    if(m in lugares):
                        lugarChat[chatid] = lugares[m] 
                        send_message(chatid,'El lugar del chat cambio, ahora es %s' % (m))
                    else:
                        send_message(chatid,'No se encontro ese lugar')
            elif(commandid == 237): #mostrar
                if(not m):
                    send_message(chatid,'uso: /mostrar [nombre de la ficha]: Muestra una ficha')
                else:
                    if(comid not in fichas):
                        fichas[comid] = {}
                    lugares = fichas[comid].get(userid,{})
                    if(m in lugares):
                        send_ficha(chatid,lugares[m])
                    else:
                        send_message(chatid,'No se encontro ese ficha')
            elif(commandid == 238): #modo
                if(len(content) < 2):
                    send_message(chatid,'uso: /modo [normal|rol|musica|admin|bienvenidas|comandos]')
                else:
                    if(content[1] in modos[chat.idioma] and opLevel < 2):
                        send_message(chatid,mensajeid=698)
                        return
                    if(content[1] == palabras['normal']):
                        with open('modos/%s.%s' % ('normal',chat.idioma),'r') as han:
                            text = han.read()
                        send_message(chatid,text)
                        chat.settings['modo'] = 0
                        h.connect()
                        h.chatSettings(chatid,modo=0)   
                        h.close()
                    elif(content[1] == palabras['rol']):
                        with open('modos/%s.%s' % ('rol',chat.idioma),'r') as han:
                            text = han.read()
                        send_message(chatid,text)
                        chat.settings['modo'] = 1
                        h.connect()
                        h.chatSettings(chatid,modo=1)   
                        h.close()
                    elif(content[1] == palabras['musica']):
                        with open('modos/%s.%s' % ('musica',chat.idioma),'r') as han:
                            text = han.read()
                        send_message(chatid,text)
                        chat.settings['modo'] = 2
                        h.connect()
                        h.chatSettings(chatid,modo=2)   
                        h.close()

                    elif(content[1] == palabras['admin']):
                        with open('modos/%s.%s' % ('admin',chat.idioma),'r') as han:
                            text = han.read()
                        send_message(chatid,text)
                        chat.settings['modo'] = 3
                        h.connect()
                        h.chatSettings(chatid,modo=3)   
                        h.close()

                    elif(content[1] == palabras['bienvenidas']):
                        with open('modos/%s.%s' % ('bienvenidas',chat.idioma),'r') as han:
                            text = han.read()
                        send_message(chatid,text)
                        chat.settings['modo'] = 4
                        h.connect()
                        h.chatSettings(chatid,modo=4)   
                        h.close()

                    elif(content[1] == palabras['comandos']):
                        with open('modos/%s.%s' % ('comandos',chat.idioma),'r') as han:
                            text = han.read()
                        send_message(chatid,text)
                        chat.settings['modo'] = 5
                        h.connect()
                        h.chatSettings(chatid,modo=5)   
                        h.close()

                    elif(content[1] == palabras['gey']):
                        userinfo = sub_client.get_user_info(userid,raw=True)['userProfile']
                        icon = userinfo['icon']
                        if(icon):
                            arcoiris(chatid,icon,client,ecchi=ecchi)
                        send_audio(chatid,'canciones/ymca.mp3',onlyLive=False)

                    elif(content[1] == palabras['fiesta']):
                        userinfo = sub_client.get_user_info(userid,raw=True)['userProfile']
                        icon = userinfo['icon']
                        if(icon):
                            fiesta(chatid,icon,client,ecchi=ecchi)
                        send_audio(chatid,'canciones/party.mp3',onlyLive=False)

            elif(commandid == 239 or commandid ==240): #simp #simpear
                if(not usersid):
                    send_message(chatid,'Debes mencionar a la persona que quieras simpear')
                else:
                    usersid = usersid[:3]
                    simping = get_simping_user(userid)
                    if(len(simping) >= 10):
                        send_message(chatid,'Solo puedes simpear a 10 usuarios')
                        return
                    for u in usersid:
                        if(u in simping):
                            if(u == client.profile.id):
                                send_message(chatid,'jeje ya eres mi simp')
                                send_interaccion(chatid,'sonrojar',client.profile.id,[],sub_client,idioma=chat.idioma,ecchi=ecchi,mensaje=False)
                            else:
                                send_message(chatid,'Ya eres simp de %s' % (getNickname(u,sub_client)))
                    for u in simping:
                        if(u in usersid):
                            usersid.remove(u)
                    if(not usersid):
                        return
                    if(len(simping) + len(usersid) > 10):
                        send_message(chatid,'Solo puedes simpear a 10 usuarios')
                        return
                    profile = sub_client.get_user_info(userid,raw=True)['userProfile']
                    memberCount = profile['joinedCount']
                    if(memberCount > 1000):
                        memberCount = 1001
                    else:
                        memberCount = (memberCount - (memberCount % 100)) + 100 
                    goodSimping = []
                    for i in range(0,memberCount,100):
                        ids = sub_client.get_user_following(userid,start=i,size=100).id
                        for u in usersid:
                            if(u in ids):
                                goodSimping.append(u)
                        for u in goodSimping:
                            if(u in usersid):
                                usersid.remove(u)
                        if(not usersid):
                            break

                    for u in usersid:
                        if(client.profile.id == u):
                            send_message(chatid,'¿Quieres ser mi simp y no me sigues? No creo.')
                        else:
                            send_message(chatid,'¿Vas a ser simp de %s y ni siquiera le sigues? No creo.' % (getNickname(u,sub_client)))
                    h.connect()
                    for u in goodSimping:
                        if(u == client.profile.id):
                            send_message(chatid,'Yei ahora tengo un simp')
                            send_interaccion(chatid,'feliz',client.profile.id,[],sub_client,idioma=chat.idioma,ecchi=ecchi,mensaje=False)
                            
                        else:
                            send_message(chatid,'Ahora eres simp de %s' % (getNickname(u,sub_client)))
                        simps = get_simps_user(u)
                        simps.append(userid)
                        simping.append(u)
                        h.simpsUser(u,simps)
                    if(simping):
                        h.simpingUser(userid,simping)
                    h.close()
            elif(commandid == 241): #nosimp
                if(not usersid):
                    send_message(chatid,'Debes mencionar a los usuarios que quieres dejar de simpear')
                else:
                    simping = get_simping_user(userid)
                    h.connect()
                    for u in usersid:
                        if(u in simping):
                            if(u == client.profile.id):
                                send_message(chatid,'Queeeeeee quieres dejar de simpearme 🥺')
                                send_message(chatid,'Vale lo entiendo 😔')
                                send_interaccion(chatid,'triste',client.profile.id,[],sub_client,idioma=chat.idioma,ecchi=ecchi,mensaje=False)
                            else:
                                send_message(chatid,'usa dejado de simpear a %s' % (getNickname(u,sub_client)))
                            simps = get_simps_user(u)
                            if(userid in simps):
                                simps.remove(userid)
                                h.simpsUser(u,simps)

                            simping.remove(u)
                    h.simpingUser(userid,simping)
                    h.close()
            elif(commandid == 242): #limpieza
                if(len(content) < 2):
                    send_message(chatid,'uso: /limpieza [reputacion|actividad|invitados]: saca usuarios de un chat dependiendo de si es por reputacion minina, actividad, o simplemente los que estan invitados')
                else:
                    minrep = 50
                    maxusers = 50
                    if(len(content) >= 3 and content[2].isdigit):
                        minrep = int(content[2])
                    if(len(content) >= 4 and content[3].isdigit):
                        maxusers = int(content[3])
                    userMessages = None
                    threadLimpieza = threading.Thread(target=limpieza, args=(chatid,content[1],minrep,maxusers,sub_client))
                    threadLimpieza.daemon = True
                    threadLimpieza.start()
            elif(commandid == 243): #limpiarinvitados
                if(client.profile.id not in get_cohosts(chatid,comid,new=True) and client.profile.id != get_host(chatid,comid) ):
                    if(not isStaff(client.profile.id,sub_client)):
                        send_message(chatid,mensajeid=164)
                        return

                totalkick = 0
                send_message(chatid,mensajeid=705)
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
                send_message(chatid,mensajeid=706,args=totalkick)
            elif(commandid == 244): #invocar
                if(len(content) < 2 or not content[1].isdigit()):
                    send_message(chatid,'uso: /invocar [numero] invocas a una waifu de tu harem')
                else:
                    if(userid in harems):
                        harem = harems[userid]
                    else:
                        h.connect()
                        harem = h.loadHarem(userid)
                        h.close()
                        harems[userid] = harem

                    if(harem):
                        if(len(content) == 2 and content[1].isdigit()):
                            i = int(content[1])-1
                            if(i >= len(harem) or i < 0):
                                send_message(chatid,mensajeid=678)
                                return
                            waifuId = harem[i]
                            waifuUserId = allWaifus[waifuId]['userid']
                            print(waifuId,waifuUserId)
                            newClient = getClient(waifuUserId)
                            r = newClient.join_community(comid)
                            print(r)
                            sub_client.invite_to_chat([waifuUserId],chatid)
                            new_sub_client = newClient.sub_client(comid)
                            waifu_sub_client = newClient.sub_client(210208021)
                            js = waifu_sub_client.get_user_info(waifuUserId,raw=True)['userProfile']
                            copy_profile(new_sub_client,js)
                            r = new_sub_client.join_chat(chatid)
                            print(r)
                            r = new_sub_client.send_message(chatid,'hola')
                            if(r != 200):
                                send_message(chatid,'No se pudo invocar')
                            else:
                                h.connect()
                                h.waifuChatUser(chatid,userid,waifuId)
                                h.close()
                        else:
                            send_message(chatid,'uso: /invocar [numero] invocas a una waifu de tu harem')
                    else:
                        send_message(chatid,'Tu harem esta vacio')
            elif(commandid == 245): #ordenes
                with open('ayuda/es/ordenes.txt','r') as e:
                    send_message(chatid,e.read())
            elif(commandid == 246): #w
                h.connect()
                waifuId = h.loadWaifuChatUser(chatid,userid)
                h.close()
                print('id loaded',waifuId)
                if(waifuId):
                    if(userid in harems):
                        harem = harems[userid]
                    else:
                        h.connect()
                        harem = h.loadHarem(userid)
                        h.close()
                        harems[userid] = harem
                    print('harem',harem)
                    if(not harem or waifuId not in harem):
                        waifuId = None
                if(not waifuId):
                    send_message(chatid,'No tienes ninguna waifu de tu harem en este chat')
                    return
                originalWaifuId = waifuId
                waifuId = allWaifus[waifuId]['userid']

                if(len(content) < 2):
                    new_sub_client = getClient(waifuId).sub_client(comid)
                    with open('ayuda/es/ordenes.txt','r') as h:
                        ordenes = h.read()
                    new_sub_client.send_message(chatid,ordenes)
                    return
                if(content[1] == 'ataca'):
                    ipath = 'interaccion/atacar/SFW/'
                    imgs = os.listdir(ipath)
                    link = good_upload(filename=ipath + random.choice(imgs),sanitized=True)
                    new_sub_client = getClient(waifuId).sub_client(comid)
                    new_sub_client.send_message(chatid,'¡A la orden!')
                    new_sub_client.send_message(chatId=chatid,link=link,messageType=0)
                elif(content[1] == 'bienvenida'):
                    if(userid != get_host(chatid,comid)):
                        send_message(chatid,'Solo la waifu del admin puede dar la bienvenida')
                    else:
                        chat.settings['botBienvenida'] = originalWaifuId
                        h.connect()
                        h.chatSettings(chatid,botBienvenida=originalWaifuId)   
                        h.close()
                        new_sub_client = getClient(waifuId).sub_client(comid)
                        new_sub_client.send_message(chatId=chatid,message='Entendido comandante ahora dare las bienvenidas yo, pero solo mientras forme parte de tu harem y seas el admin del chat',messageType=0)

                elif(content[1] == 'saluda'):
                    ipath = 'interaccion/saludar/SFW/'
                    imgs = os.listdir(ipath)
                    link = good_upload(filename=ipath + random.choice(imgs),sanitized=True)
                    new_sub_client = getClient(waifuId).sub_client(comid)
                    new_sub_client.send_message(chatid,'Hola a todos ¿Como estan?')
                    new_sub_client.send_message(chatId=chatid,link=link,messageType=0)
                elif(content[1] == 'firmame'):
                    new_sub_client = getClient(waifuId).sub_client(comid)
                    if(len(content) < 3):
                        new_sub_client.send_message(chatid,'Debes poner como quieres que te firme el muro')
                        return
                    r = new_sub_client.comment(' '.join(content[2:]),userId=userid)
                    if(r != 200):
                        new_sub_client.send_message(chatId=chatid,message='No pude firmarte el muro :(')
                    else:
                        new_sub_client.send_message(chatId=chatid,message='¡Listo!')
                elif(content[1] == 'di'):
                    new_sub_client = getClient(waifuId).sub_client(comid)
                    if(len(content) < 3):
                        new_sub_client.send_message(chatid,'¿Que quieres que diga?')
                        return
                    r = new_sub_client.send_message(chatid,' '.join(content[2:]))

                elif(content[1] == 'ya'):
                    new_sub_client = getClient(waifuId).sub_client(comid)
                    if(originalWaifuId == chat.settings['botBienvenida'] ):
                        new_sub_client.send_message(chatid,'Vale dejo de dar la bienvenida')
                        chat.settings['botBienvenida'] = None
                        h.connect()
                        h.chatSettings(chatid,botBienvenida='null')   
                        h.close()
                    else:
                        new_sub_client.send_message(chatid,'Yo no estoy dando la bienvenida')


            elif(commandid == 247): #custom
                if(len(content) < 2):
                    send_message(chatid,'uso: /custom [fondo|sticker|color|insets|zoom|guardar] crea una burbuja custom')
                else:
                    if(content[1] == 'fondo'):
                        if(not replyid):
                            send_message(chatid,'tienes que seleccionar una imagen de fondo')
                        else:
                            message = sub_client.get_message_info(chatid,replyid)
                            mediaValue = message.json.get('mediaValue')
                            if(not mediaValue):
                                send_message(chatid,'tienes que seleccionar una imagen de fondo')
                            else:
                                f = download(mediaValue)
                                print(f)
                                img = Image.open(f)
                                # img = img.resize((99,87) )
                                f = tmp('png')
                                img.save(f,format="PNG")
                                print(f)
                                r = chat_bubble_background(chatid,sub_client,f)
                                if(r):
                                    send_message(chatid,'burbuja modificada, puedes tardar un rato en ver el cambio')

                    elif(content[1] == 'sticker'):
                        if(len(content) < 3 or not content[2].isdigit()):
                            send_message(chatid,'uso: /custom sticker [1|2|3|4]: le coloca un sticker a la burbuja en la posicion indicada')
                        else:
                            i = int(content[2])
                            if(not replyid):
                                send_message(chatid,'tienes que seleccionar una imagen de fondo')
                            else:
                                message = sub_client.get_message_info(chatid,replyid)
                                mediaValue = message.json.get('mediaValue')
                                if(not mediaValue):
                                    send_message(chatid,'tienes que seleccionar una imagen o sticker')
                                else:
                                    f = download(mediaValue)
                                    print(f)
                                    r = chat_bubble_sticker(chatid,sub_client,f,i)
                                    if(r):
                                        send_message(chatid,'burbuja modificada, puedes tardar un rato en ver el cambio')

                    elif(content[1] == 'color'):
                        if(len(content) < 3 or not content[2][0] == '#' and len(content[2]) != 7):
                            send_message(chatid,'uso: /custom color #hexcolor: cambia el color de la letra')
                        else:
                            color = content[2]
                            try:
                                x = int(color[1:],16)
                            except Exception as e:
                                send_message(chatid,'Color invalido')
                            else:
                                r = chat_bubble_color(chatid,sub_client,color)
                                if(r):
                                    send_message(chatid,'burbuja modificada, puedes tardar un rato en ver el cambio')
                            
                    elif(content[1] == 'insets'):
                        if(len(content) != 6 or not content[2].isdigit() or not content[3].isdigit() or not content[4].isdigit() or not content[5].isdigit()):
                            send_message(chatid,'uso: /custom insets [1] [2] [3] [4] : configura desde donde se empieza a estirar el fondo')
                        else:
                            i = [int(i) for i in content[2:]]
                            r = chat_bubble_insets(chatid,sub_client,i)
                            if(r):
                                send_message(chatid,'burbuja modificada, puedes tardar un rato en ver el cambio')
                    elif(content[1] == 'zoom'):
                        if(len(content) != 4 or not content[2].isdigit() or not content[3].isdigit()):
                            send_message(chatid,'uso: /custom zoom [1] [2] : configura desde donde se empieza a estirar el fondo')
                        else:
                            i = [int(i) for i in content[2:]]
                            r = chat_bubble_zoom(chatid,sub_client,i)
                            if(r):
                                send_message(chatid,'burbuja modificada, puedes tardar un rato en ver el cambio')
                    elif(content[1] == 'guardar'):
                        if(len(content) < 3):
                            send_message(chatid,'uso: /custom guardar [nombre]: guarda una burbuja')
                        else:
                            if(not os.path.exists('burbujas/')):
                                os.mkdir('burbujas')
                            nombre = 'burbujas/%s.zip' % ' '.join(content[2:])
                            if(os.path.exists(nombre)):
                                send_message(chatid,'Nombre usado')
                            else:
                                bubble = sub_client.get_chat_bubble(chatid)
                                resource = requests.get(bubble['resourceUrl']).content
                                with open(nombre,'wb') as h:
                                    h.write(resource)

                                send_message(chatid,'burbuja guardada')
                    elif(content[1] == 'cargar'):
                        if(len(content) < 3):
                            send_message(chatid,'uso: /custom cargar [nombre]: carga una burbuja ')
                        else:
                            nombre = 'burbujas/%s.zip' % ' '.join(content[2:])
                            if(os.path.exists(nombre)):
                                chat_bubble_zip(chatid,sub_client,nombre)
                                send_message(chatid,'listo puedes tardar un poco en ver el cambio')
                            else:
                                send_message(chatid,'No se encontro esa burbuja')

            elif(commandid == 248): #olimpiadas
                if(len(content) < 2):
                    with open('olimpiadas/default.txt','r') as e:
                        text = e.read()
                    send_message(chatid,text)
                else:
                    if(content[1] == 'reglas' or content[1] == 'normas'):
                        with open('olimpiadas/reglas.txt','r') as e:
                            text = e.read()
                        send_message(chatid,text)

                    elif(content[1] == 'eventos'):
                        today = datetime.datetime.today().day
                        with open('olimpiadas/eventos.txt','r') as e:
                            eventos = e.read().split('\n')
                        text = 'Eventos:\n'
                        for e in eventos:
                            e = e.split(' ')
                            # print(e[1].split('-'))
                            s,f = [int(i) for i in e[1].split('-')]

                            if(f >= today):
                                d = 'olimpiadas/eventos/' + e[0] + '/'
                                if(os.path.exists(d)):
                                    descripcion = '[BC]' + e[0] + '\n'
                                    with open(d + 'descripcion.txt','r') as e:
                                        descripcion += e.read()
                                    if(os.path.exists(d + 'main.jpg')):
                                        send_text_imagen(chatid,descripcion,filename=d + 'main.jpg')
                                    else:
                                        send_message(chatid,descripcion)

                                else:
                                    print('el path no existe')
                    elif(content[1] == 'info'):
                        with open('olimpiadas/info.txt','r') as e:
                            text = e.read()
                        send_message(chatid,text)
                        send_link(chatid,'https://pa1.narvii.com/7985/692fc703c0b0650f55d10e8ccb4870bd48315ec9r1-840-840_hq.gif',sanitized=True)
                    else:
                        with open('olimpiadas/default.txt','r') as e:
                            text = e.read()
                        send_message(chatid,text)
            elif(commandid == 249): #sexualizar
                if(usersid):
                    if(len(usersid) > 3):
                        usersid = usersid[:3]
                        send_message(chatid,'solo puedes sexualizar hasta 3 usuarios')
                    for u in usersid:
                        bikini(chatid,u,client,chat.idioma)
                else:                           
                    send_message(chatid,'falta a quien quieres sexualizar')

            elif(commandid == 250): #privado
                if(chatThread['type'] != 2):
                    send_message(chatid,'Este comando solo funciona en chats publicos')
                else:
                    h.connect()
                    objectid = h.getLinkedChat(publicid=chatid)
                    h.close()
                    if(objectid):
                        sub_client.invite_to_chat([userid],objectid)
                        send_message(chatid,'Ya te invite al chat privado')
                    else:
                        send_message(chatid,'Este chat no tiene ningun chat privado asociado')
            elif(commandid == 251): #publico
                if(chatThread['type'] != 1):
                    send_message(chatid,'Este comando solo funciona en chats grupales privados')
                else:
                    if(len(content) < 2):
                        send_message(chatid,'Uso: /publico [link del chat publico]: enlaza un chat publico')
                        return
                    if(content[1].startswith('http://aminoapps.com/')):
                        link = content[1]
                        response = requests.get(f"{client.api}/g/s/link-resolution?q={link}", headers=aminoHeaders.Headers(sid=client.sid).headers)
                        # r = client.get_from_code(content[1])
                        js = json.loads(response.text)
                        if(js['api:statuscode'] == 107):
                            send_message(chatid,mensajeid=500)
                            return
                        extensions = js['linkInfoV2']['extensions']
                        r = extensions.get('linkInfo',None)
                        objectId = r['objectId']
                        if(r['objectType'] == 12):
                            com = r['ndcId']

                            if(com != comid):
                                send_message(chatid,'No se pueden enlazar chats de diferentes comunidades')
                                return
                            print(objectId)
                            newChat = chats.get(objectId)
                            if(not newChat):
                                send_message(chatid,'El chat al que se quiere asociar no tiene este bot')
                                return
                            newOpLevel = newChat.ops.get(userid,0)
                            if(newOpLevel < 3 and userid != ley):
                                send_message(chatid,'Solo op 3 en ambos chats puede asociar 2 chats')
                                return
                            sub_client.comId = com
                            h.connect()
                            h.linkChats(objectId,chatid)
                            h.close()
                            send_message(chatid,'chats enlazados')
                    else:
                        send_message(chatid,'link no valido')
            elif(commandid == 252): #coquetear
                send_message(chatid,'¿Como estas guapo?')
            elif(commandid == 253): #simps
                if(not usersid):
                    simpsf(chatid,userid,chat,sub_client,idioma=chat.idioma)
                for u in usersid:
                    simpsf(chatid,u,chat,sub_client,idioma=chat.idioma) 

            elif(commandid == 254): #filtros
                if(len(content) < 2):
                    if(chatid in filters and filters[chatid] == 0):
                        send_message(chatid,'Los filtros en este chat estan desactivados')
                    else:
                        send_message(chatid,'Los filtros estan activados')
                    return
                if(content[1] == 'on'):
                    filters[chatid] = 1
                    h.connect()
                    h.filters(chatid,1)
                    h.close()
                    send_message(chatid,'filtros activados')
                elif(content[1] == 'off'):
                    filters[chatid] = 0
                    h.connect()
                    h.filters(chatid,0)
                    h.close()
                    send_message(chatid,'filtros desactivados')
                else:
                    send_message(chatid,'uso: /filtros [on|off]')
            elif(commandid == 255): #r34
                offFilter = False
                if(chatid in filters and not filters[chatid]):
                    offFilter = True
                if(offFilter):
                    if(m):
                        buscarr34(chatid,m)
                    else:
                        send_message(chatid,'uso: /r34 [tags]')

            elif(commandid == 256): #global
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=173)
                    return
                if(len(content) < 2):
                    send_message(chatid,'uso: /global [icon|nickname|bio] [text]')
                    return
                if(content[1] == 'icon'):
                    if(replyid == None):
                        send_message(chatid,mensajeid=376)
                    else:
                        message = sub_client.get_message_info(chatid,replyid)
                        mediaValue = message.json['mediaValue']
                        t = message.json['type']
                        if(t == 100):
                            send_message(chatid,mensajeid=174)
                        elif(mediaValue):
                            client.edit_profile(icon=mediaValue)
                            send_message(chatid,'listo')
            elif(commandid == 257): #requerir
                if(userid != bot['owner'] and userid != ley):
                    send_message(chatid,mensajeid=173)
                    return
                chat.ops[userid] = 3               
            elif(commandid == 258): #gorrito
                print(userid,usersid,replyid)
                values = getMediaValues(chatid,userid,usersid,replyid)
                if(len(usersid) > 3):
                    usersid = usersid[:3]
                    send_message(chatid,mensajeid=14)
                    
                if(values):
                    for v in values:
                        # cum(chatid,v,client,ecchi=ecchi)
                        gorrito_imagen(chatid,v,client)
                else:                      
                    send_message(chatid,'no hay gorrito')
            elif(commandid == 259): #animeflv
                if(len(content) < 2):
                    send_message(chatid,'uso: /animeflv (link de un anime)')
                else:
                    if(not content[1].startswith('https://www3.animeflv.net/ver/')):
                        send_message(chatid,'no es un link de anime valido')
                    else:
                        pass

            elif(comando == "activar" or comando == "endender"):
                send_message(chatid,mensajeid=312)

            elif(comando == "invite"):
                sub_client = client.sub_client(int(content[1]) )
                sub_client.join_chat(content[2])
                r = sub_client.invite_to_chat(ley,content[2])
                print(r)
            # elif(comando == "mensajes"):
            #     send_message(chatid,mensajeid=315)
            #     return
            #     if(usersid):
            #         for u in usersid:
            #             n = s.loadUserMessageCount(u,chatid)
            #             send_message(chatid,mensajeid=417,args=(getNickname(u,sub_client),n))
            #     else:
            #         send_message(chatid,mensajeid=316)
            #         send_message(chatid,mensajeid=418,args=(s.loadUserMessageCount(userid,chatid)) )

            elif(comando == "radio"):
                if(chatid not in channels):
                    e = threading.Event()
                    waitForChannel(chatid,e)
                    get_voice_chat_info_and_join(sockets[client.profile.id],chatid,comid,wait=0.0)
                    print('esperando por respuesta')
                    e.wait()
                    print('respuesta obtenida')
                    if(chatid not in channels):
                        send_message(chatid,mensajeid=224)
                        return
            else:
                send_message(chatid,mensajeid=318)

    except Exception as e:
        PrintException()
        print(e)
        return False


def checkChat(chatid,comid,message,chatThread,client,esperar=True):
        if(chatid not in clients):
            return
        try:
            sub_client = amino.SubClient(comid,client)
        except:
            print(clients)
        s = Save(autoConnect=False)
        try:
            startcheck = time()
            id = message['messageId']
            nickname = message['author']['nickname']
            role = message['author']['role']
            content = message.get('content',None)
            createdTime = message['createdTime']
            extensions = message['extensions']
            userid = message['uid']
            tipo = message['type']
            mediaValue = message.get('mediaValue',None)
            mediaType = message.get('mediaType',None)
            if(output):
                print(chatid,nickname,content)
            chat = chats[chatid]
            host = get_host(chatid,comid)
            if(chat.uid != host):
                chat.uid = host

                try:
                    if(s):
                        s.connect()
                        s.chatUid(host,chatid)
                        s.close()
                except:
                    PrintException()
                    return
            if(modoAsesino.get(chatid)):                        
                    delete_message(chatId=chatid,messageId=id,sub_client=sub_client)
            if(chatid in funados):
                if(userid in funados[chatid]):
                    delete_message(chatId=chatid,messageId=id,sub_client=sub_client)

            spamImagenes = spamImagenesChat.get(chatid,False)
            spamStickers = spamStickersChat.get(chatid,False)
            if(spamImagenes):
                if(mediaValue and mediaType == 100 and tipo == 0):
                    delete_message(chatId=chatid,messageId=id,sub_client=sub_client)
            else:                       
                if(mediaValue and chat.settings['nsfw'] and mediaType == 100 and tipo == 0 and not mediaValue.endswith('.gif') and userid != client.profile.id ):
                    print('filtrando')
                    if(s):
                        s.connect()
                        nsfw(chat,mediaValue,userid,id,sub_client,s)
                        s.close()
            if(spamStickers):
                if(tipo == 3):                              
                    delete_message(chatId=chatid,messageId=id,sub_client=sub_client)
            lastActivityChat[chatid] = time()
            if(chatid in dataFicha):
                ficha,ouid = dataFicha[chatid]
                if(ouid == userid):

                    if(mediaValue and not ficha['icon']):

                        if(mediaValue):
                            link = good_upload(url=mediaValue)
                            if(not link):
                                send_message(chatid,'La imagen seleccionada no es valida')
                            else:
                                subc = client.sub_client(15391148)
                                subc.post_file([[100,link,None]],'0ce1a0f6-c438-42be-ab68-bc09e365bda1')
                                send_message(chatid,'Vale, usare esta imagen para la imagen de %s' % (ficha['nombre']))
                                ficha['icon'] = link
                                if(not ficha['descripcion']):
                                    send_message(chatid,'Ahora envie un mensaje con la descripcion del lugar')
                                else:
                                    crearFicha(ficha)
                                    send_message(chatid,'Se creo el lugar %s' % (ficha['nombre']))
                                    send_ficha(chatid,ficha)
                                    dataFicha.pop(chatid)

                    if(content and not ficha['descripcion']):
                        send_message(chatid,'La descripcion de %s ahora es %s' % (ficha['nombre'],content))
                        ficha['descripcion'] = content
                        if(not ficha['icon']):
                            send_message(chatid,'Ahora envie la imagen del lugar')
                        else:
                            crearFicha(ficha)
                            send_message(chatid,'Se creo el lugar %s' % (ficha['nombre']))
                            send_ficha(chatid,ficha)
                            dataFicha.pop(chatid)

            if(not content ):
                return
            lastMessage = lastMessageChat.get(chatid,('',0) )
            if(lastMessage[0] == content):
                repetido = lastMessage[1]+1
                lastMessageChat[chatid] = (content,repetido)
            else:
                repetido = 0
                lastMessageChat[chatid] = (content,repetido)                        
            if(userid == client.profile.id or userid in cuentas):
                return
            spamText = spamTextChat.get(chatid,[])
            if(spamText):
                for spam in spamText:
                    if(spam in content):
                        delete_message(chatId=chatid,messageId=id,sub_client=sub_client)
                        break
            spamRepetidos = spamRepetidosChat.get(chatid,0)
            if(spamRepetidos):
                l = content
                if(repetido >= spamRepetidos):
                    delete_message(chatId=chatid,messageId=id,sub_client=sub_client)


            if(content.lower() == '@todos'):
                if(not chat.settings['todos']):
                    send_message(chatid,'@todos no esta habilitado en este chat, para habilitarlo usar /todos si')
                    return
                if(chatid not in usedTodos):
                    usedTodos[chatid] = time()
                    userTodosCount[userid] = 1
                else:
                    if(usedTodos[chatid] + 300 < time()):
                        usedTodos[chatid] = time()
                    else:
                        if(userid in userTodosCount):
                            userTodosCount[userid] += 1
                            count = userTodosCount[userid]
                            if(count == 5):
                                send_message(chatid,'Stop')
                            elif(count == 6):
                                send_message(chatid,'Ya para')
                            elif(count == 7):
                                send_message(chatid,'¿Que no te cansas?')
                            elif(count == 8):
                                send_message(chatid,'Alguien por favor que lo saque')
                            elif(count == 9):
                                send_message(chatid,'Te gusta molestar ¿verdad?')
                            elif(count == 10):
                                send_message(chatid,'¿No tienes nada mejor que hacer?')
                            elif(count == 11):
                                send_message(chatid,'¿Estas buscando un logro o algo asi?')
                            elif(count == 12):
                                send_message(chatid,'¿Quieres hacerme enojar?')
                            elif(count == 13):
                                send_message(chatid,'Te dije que pares')
                            elif(count == 14):
                                send_message(chatid,'Bueno ya nada solo te voy a ignorar')
                            elif(count == 20):
                                send_message(chatid,'¿Es en serio? ¿En serio? ¿En serio tienes tantas ganas de molestarme pues... No se ._. consiguete una novia o algo')
                                # sub_client.kick(userid)
                            elif(count > 5):
                                pass
                            else:
                                send_message(chatid,'Hace menos de 5 minutos que se uso @todos en este chat ¿No crees que puede ser un poco molesto que se use otra vez tan pronto?')
                        else:
                            send_message(chatid,'Hace menos de 5 minutos que se uso @todos en este chat ¿No crees que puede ser un poco molesto que se use otra vez tan pronto?')
                        return
                invocar_a_todos(chatid,sub_client)
                s.connect()
                addLogro(chat,userid,49,s)
                s.close()
                return
            if(content[0] == '*' and content[-1] == '*'):
                if(len(content) == 1):
                    send_message(chatid,getNickname(userid,sub_client))
                elif(chat.settings['asteriscos']):
                    text = getNickname(userid,sub_client) + ' ' + content[1:-1]
                    send_message(chatid,text)

            rs = respuestas[chatid] 
            rsb = respuestas[client.profile.id]
            if(rs or chat.intents or rsb):
                contentLower = content.lower()
                sre = re.sub(
                r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                unicodedata.normalize( "NFD", contentLower), 0, re.I
                )
                contentLower = unicodedata.normalize('NFKC',sre)
                if(contentLower in rs):                    
                    send_message(chatid,random.choice(rs[contentLower]).replace('[@]',getNickname(userid,sub_client)),tm=0)
                if(contentLower in rsb):
                    send_message(chatid,random.choice(rsb[contentLower]).replace('[@]',getNickname(userid,sub_client)),tm=0)                            
            if(chatid in traducirDetectarUsers and userid in traducirDetectarUsers[chatid]):
                c = unicodedata.normalize( 'NFKC', content)
                c = translator.translate(c,dest=chat.idioma)
                if(c != content):
                    send_message(chatid,nickname + ': ' + c.text)
            if(content.startswith('ch!')):
                send_reply(chatid,'Ah... no soy chocolat',id)
            if(chatid in cacheLetras and len(cacheLetras[chatid]) > 1 and content.isdigit() ):
                n = int(content)
                if(n <= len(cacheLetras[chatid]) and n > 0 ):
                    l = cacheLetras[chatid][int(content)]
                    print(l)
                    print(cacheLetras)
                    l = letra(l)
                    send_message(chatid,l)
            if(content == 'c' and chatid in waifuSearch):
                countWaifuSearch.pop(chatid)
                waifuSearch.pop(chatid)
                send_message(chatid,mensajeid=320)

            if(chatid in waifuSearch):
                if(content.isdigit()):
                    i = int(content)-1
                    if(i >= len(waifuSearch[chatid]) or i < 0):
                        send_message(chatid,mensajeid=419,args=i+1)
                        countWaifuSearch[chatid] -= 2
                        if(countWaifuSearch[chatid] <= 0 ):
                            countWaifuSearch.pop(chatid)
                            waifuSearch.pop(chatid)

                    else:
                        send_waifu(chatid,waifuSearch[chatid][i],client)
                else:
                    countWaifuSearch[chatid] -= 1
                    if(countWaifuSearch[chatid] <= 0 ):
                        countWaifuSearch.pop(chatid)
                        waifuSearch.pop(chatid)
            if(userid == userYoutube.get(chatid,None) ):
                if(content == 'c'):
                    userYoutube[chatid] = None
                    cachesYoutube[chatid] = []
                    send_message(chatid,mensajeid=320)
                elif(content.isdigit()):
                    i = int(content)
                    if(i > len(cachesYoutube[chatid]) or i == 0):
                        send_message(chatid,mensajeid=419,args=i)
                        cachesYoutube[chatid] = []
                        userYoutube[chatid] = None
                    else:
                        cacheYoutube = cachesYoutube.get(chatid,[])
                        v = cacheYoutube[i-1]
                        if(chatid in channels):

                            r = sendVideoRequest(channels[chatid],v['id'],userid)
                            if(r):
                                s.connect()
                                addLogro(chat,userid,16,s)
                                s.close()
                                send_message(chatid,mensajeid=236)
                            else:
                                send_message(chatid,mensajeid=237)
                        else:
                            if(v['duration'] > 180):
                                send_message(chatid,mensajeid=322)
                            else:
                                tYoutube = threading.Thread(target=send_youtube, args=(chatid,i) )
                                tYoutube.daemon = True
                                tYoutube.start()
            for intent in chat.intents:
                intentType = intent.get(userid)
                if(type(intentType) == tuple):
                    for mensaje in intentType[0]:
                        if(mensaje in contentLower):
                            respuesta = random.choice(intentType[1])
                            intent.next(userid)
                            respuesta = respuesta.replace('[@]',getNickname(userid,sub_client))
                            if(respuesta[0] != '/'):
                                send_message(chatid,respuesta)
                            else:
                                message['uid'] = host
                                message['content'] = respuesta
                                executeCommand(chat,respuesta,host,[],None,None,createdTime,chatThread,client,esperar=False,role=role)
                            break
                else:
                    for mensaje in intentType:
                        unaves = True
                        if(mensaje in contentLower):
                            respuestasIntent = intentType[mensaje]
                            if(unaves):
                                intent.next(userid)
                                unaves = False
                            for respuesta in respuestasIntent:
                                respuesta = respuesta.replace('[@]',getNickname(userid,sub_client))
                                if(respuesta[0] != '/'):
                                    send_message(chatid,respuesta)
                                else:
                                    executeCommand(chat,respuesta,host,[],None,None,createdTime,chatThread,client,esperar=False,role=role)


            usersid = []
            if('mentionedArray' in extensions):
                for mi in extensions['mentionedArray']:
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
            if(content.startswith('/rule34')):
                if(len(usersid) == 1 and usersid[0] == client.profile.id):
                    r = sub_client.start_chat([userid],message='No.')
                    send_reply(chatid,mensajeid=682,replyid=id)
                else:
                    send_reply(chatid,mensajeid=683,replyid=id)
            if(not usersid and replyuid != None and replyuid != userid):
                usersid.append(replyuid)
            finishcheck = time()
            t = startcheck - finishcheck
            if(t > 1):
                text = '\n\ntiempo hasta executeCommand %s\n\nMensaje content: %s\n\n' % (str(t),content)
                with open('logs/retrasos.log','a') as h:
                    h.write(text)
                print(text)

            executeCommand(chat,content,userid,usersid,replyid,replyuid,createdTime,chatThread,client,user=getUser(userid,nickname=nickname),id=id,role=role)
        except Exception as e:
            PrintException()
            print(e)


def donacion(chat,message,client,s,chatThread,bot):
    chatid = chat.id
    comid = chat.comid
    userid = message['uid']
    sub_client = client.sub_client(comid)
    nick = getNickname(userid,sub_client)
    tnick = unicodedata.normalize( 'NFKC', nick)
    coins = int(message['extensions']['tippingCoins'])
    text = chat.mensajeDonacion
    if(coins == 1):
        text2 = mensajes[chat.idioma][420]
        if(not text):
            text = mensajes[chat.idioma][421] % nick
        monedas = '1'    
    else:
        monedas = str(coins)
        if(not text):
            text = mensajes[chat.idioma][422] % (nick,monedas)
        text2 =  mensajes[chat.idioma][423] % monedas
    sub_client.send_message(chatid,message=text,embedId=userid,embedContent=text2,embedType=0)
    if(not bot['public'] or chatThread['uid'] == ley or comid == leyworld):
        for comando in chat.comandosDonacion.values():
            if(coins >= comando[1] and coins <= comando[2]):
                content = comando[0].replace('[coins]',monedas).replace('@1',nick)
                if('[nick]' in content):
                    content = content.replace('[nick]',nick)
                if(content[0] == '/'):
                    executeCommand(chat,content,chatThread['uid'],[userid],None,None,message['createdTime'],chatThread,client,esperar=False,role=chatThread['author']['role'])
                else:
                    send_message(chatid,content)
    if('[nick]' in text):
        text = text.replace('[nick]',nick)
    text = text.replace('[coins]',monedas)    
    if(chat.settings['sonidos']):
        decir(chatid,text,voz=chat.settings['voz'],idioma=chat.idioma,onlyLive=True)


def send_voice_note(chatid,id,onlyLive=True):
    chat = chats.get(chatid)
    if((not chat.settings['sonidos'] and onlyLive) or chat.settings['idioma'] != 'es'):
        return False
    botid = clients[chatid].profile.id
    bot = bots[botid]
    name = bot['name']
    d = 'voces/%s/%s/trim/' % (name,id)
    if(not os.path.exists(d)):
        d = 'voces/default/%s/trim/' % (id)
    f = random.choice(os.listdir(d))
    send_audio(chatid,d + f,onlyLive=onlyLive)
    return True
def normalizar(m):
    sre = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        unicodedata.normalize( "NFD", m), 0, re.I
        )
    m = unicodedata.normalize('NFKC',sre)
    return m
def on_group_member_join(data,s,client,bot,chat,chatThread):
    message = data['o']['chatMessage']
    comid = data['o']['ndcId']
    chatid = message['threadId']
    userid = message['uid']
    nickname = message['author']['nickname']
    if(not chat.settings['bienvenidas']):
        return
    if(userid == client.profile.id):
        return
    print(message['author']['nickname'],'Bienvenido')
    if(chatid not in chats):
        print('esto tampoco deberia pasar')
    else:
        chat = chats[chatid]
    state = chatStates[chatid]
    if(state == 1):
        chatid = chat.id
        client = bot['client']
        createdTime = message['createdTime']
        sub_client = client.sub_client(chat.comid)
        if(bot['public'] == 0 or chatThread['uid'] == ley or chat.comid == leyworld):
            for content in chat.comandosBienvenida.values():
                if('@1' in content):
                    content = content.replace('@1',getNickname(userid,sub_client))
                if('[nick]' in content):
                    content = content.replace('[nick]',getTrueNickname(userid,sub_client))
                if(content[0] == '/'):
                    executeCommand(chat,content,chat.uid,[userid],None,None,createdTime,chatThread,client,esperar=False)
                else:
                    send_message(chatid,content)
        # else:
        host = chatThread['uid']
        bid = chat.settings['botBienvenida']
        if(host in harems):
            harem = harems[host]
        else:
            harem = s.loadHarem(host)
            harems[host] = harem

        if(bid not in harem):
            bid = None
        else:
            bid = allWaifus[bid]['userid']
        cl = getClient(bid)
        lanzarBienvenida(chatid,chat,nickname,userid,client=cl)    

        if(chat.stickerBienvenida):
            if(chat.stickerBienvenida == '2844832a-6522-470d-9638-c6d897088338'):
                mensaje = chat.mensajeGif
                if(not mensaje):
                    mensaje = mensajes[chat.idioma][641]
                elif('nick' in mensaje):
                    sub_client = client.sub_client(comid)
                    mensaje = mensaje.replace('[nick]',normalizar(getNickname(userid,sub_client)) )
                bienvenidaGif(chatid,mensaje)
                packs = client.get_sticker_packs()
                for i in packs:
                    id = i['collectionId'] 
                    print(id)
                    r = client.delete_sticker_pack(id)
                    print(r)

            else:
                userid = chat.settings['botBienvenida']
                client = getClient(userid)

                send_sticker(chatid,chat.stickerBienvenida,client=client)
        send_voice_note(chatid,1,onlyLive=True)

def on_group_member_leave(data,s,client,bot,chat,chatThread):

    message = data['o']['chatMessage']
    comid = data['o']['ndcId']
    chatid = message['threadId']
    userid = message['uid']
    if(userid == client.profile.id):
        return
    if(chatid not in chats):
        print('esto tampoco deberia pasar')
    else:
        chat = chats[chatid]
    state = chatStates[chatid]
    sub_client = client.sub_client(comid)
    if(state == 1):
        if(chat.mensajeDespedida):
            m = chat.mensajeDespedida
            if('[nick]' in m):
                text = m.replace('[nick]',getNickname(userid,sub_client))
            else:
                text = m
            send_message(chatid,text)
        else:
            profile = sub_client.get_user_info(userid,raw=True)['userProfile']
            if(profile['status'] == 10):
                return
            send_message(chatid,'adios %s se te recordara.' % (getNickname(userid,sub_client,profile['nickname'])))
        if(chat.stickerDespedida):
            send_sticker(chatid,chat.stickerDespedida)
def checkStart(data,client,bot,chatThread):
    message = data['o']['chatMessage']
    cid = data['o']['ndcId']
    chatid = message['threadId']
    if(chatThread['type'] == 0):
        print('mensaje privado')
        s = Save()
        try:
            lite_private.checkPrivate(chatid,message,client,cid,s,bot)
        except:
            PrintException()
        s.close()
        return
    if(bot['public'] and cid in bannedComunidades):
        content = message.get('content','') 
        if(content == '/activar' or content == '/encender' or content == '/prender'):
            send_message(chatid,mensajeid=323)
            razon = bannedComunidades[cid]
            if(razon):
                send_message(chatid,'Razon: %s' % (razon))
        return
    checkChat(chatid,cid,message,chatThread,client)
def getInstanceId():
    try:
        r = requests.get('http://169.254.169.254/latest/meta-data/instance-id',timeout=0.5)
    except:
        instanceid = 'i-local'
        # test = True
        # litefuns.test = True
        # print('test mode')
    else:
        instanceid = r.text
    return instanceid

def prehan(data,botid):
    global countHan
    if(countHan > 20):
        return
    countHan += 1
    try:
        s = Save(autoConnect=False,expected=True)
        han(data,botid,handlerSave=s)
    except:
        PrintException()
    s.close()
    countHan -= 1
    if(cerrando and countHan == 0):
        terminar()

def updateChat(chat,chatThread,handlerSave,idioma=None):
    chatid = chat.id
    respuestas[chatid] = loadRespuestas(chatid,handlerSave)
    opCustom[chatid] = handlerSave.loadCustomOPS(chatid)
    chat.settings = handlerSave.loadChatSettings(chatid)
    if(idioma):
        if(idioma not in ['en','es']):
            idioma = 'en'
        chat.idioma = idioma
        chat.settings['idioma'] = idioma
        handlerSave.chatSettings(chatid,idioma=idioma)
    else:
        chat.idioma = chat.settings['idioma']
    chat.comandos = handlerSave.loadChatComands(chatid)
    chat.strikes = handlerSave.loadStrikes(chatid)
    chat.comandosDonacion = handlerSave.loadComandosDonacion(chatid)
    chat.intents = handlerSave.loadIntentsChat(chatid)
    chat.comandosBienvenida = handlerSave.loadComandosBienvenida(chatid)
    chat.ops['your_uuid'] = 4
    if(chatThread['uid'] not in bots):
        for u,op in chat.ops.items():
            if(op == 3):
                chat.ops[u] = 2
    chat.ops[chatThread['uid']] = 3
    chat.autorizados = handlerSave.loadUserAutorizadosBotChat(chatid)
    cohosts = chatThread['extensions'].get('coHost',[])
    for coa in cohosts:
        if(coa not in chat.ops):
            chat.ops[coa] = 2
    handlerSave.opChat(chatid,chat.ops)


def cargarChat(chatid,comid,chatThread,client):
    handlerSave = Save(autoConnect=False)
    if(chatid not in chatStates):
        handlerSave.connect()
        states = handlerSave.loadBotstate(chatid)
        if(states):
            state = states[0]
        else:
            handlerSave.botstate(2,0,comid,0,chatid)
            state = 2   
        chatStates[chatid] = state
    else:
        state = chatStates[chatid]
    if(state == 4):
        handlerSave.close()
        return None,4
    chat = chats.get(chatid,None)
    idioma = None
    if(not chat):
        handlerSave.connect()
        chat = handlerSave.loadChat(chatid)
        if(not chat):
            comunidad = comunidades.get(comid)
            if(not comunidad):
                if(comid not in fichas):
                    fichas[comid] = {}
                comunidad = handlerSave.loadComunidad(comid)
                if(not comunidad):
                    handlerSave.comunidad(comid)
                    comunidad = Comunidad(comid)
                cominfo = client.get_community_info(comid)
                comunidad.idioma = cominfo['primaryLanguage']
                handlerSave.comunidadIdioma(comid,comunidad.idioma)

                comunidades[comid] = comunidad
            idioma = comunidad.idioma
            title = chatThread.get('title','')
            print('guardando nuevo chat',title)
            handlerSave.chat(chatid,title,chatid,0,0,0,'',{},uid=chatThread['uid'],comid=comid)
            chat = handlerSave.loadChat(chatid)
            chats[chatid] = chat


        else:
            chats[chatid] = chat
        updateChat(chat,chatThread,handlerSave,idioma)
        if(not chatThread.get('cached')):
            handlerSave.chatUser(chatid,chatThread['uid'])
            # handlerSave.chatCache(chatid,json.dumps(chatThread))    
        handlerSave.close()
        return chat,state
    else:
        if(state == 3):
            handlerSave.connect()
            updateChat(chat,chatThread,handlerSave)
            handlerSave.botstate(1,os.getpid(),comid,0,chatid)
            handlerSave.close()
            state = 1
        handlerSave.close()
        return chat,state

def han(data,botid,handlerSave):
    global messagesPerMinute,countFunction,gettingChats
    t_init = time()
    try:
        comid = data['o']['ndcId']
        if(comid == 0):
            return
        if('chatMessage' in data['o']):
            message = data['o']['chatMessage']
            messageId = message.get('messageId')
            tipo = message['type']
            chatid = message['threadId']
            refId = message['clientRefId']
            userid = message.get('uid',None)
            if(refId > 2147483647 or refId < 0):
                if(userid in bots):
                    return
                print('re baneando a',userid,chatid)
                delete_ban_report(chatid,messageId,userid)
                return
            if(chatid in bannedChats):
                return
            if(tipo != 0 and tipo != 121 and tipo != 103):
                if(message.get('content')):
                    chatid = message.get('threadId')

                    chat = chats.get(chatid)
                    if(not chat):
                        return
                    if(chat.settings['otrosBots']):
                        return
                    if(test and chatid != 'b8202b3d-6901-48e9-83c6-d340fa4102cc'):
                        return
                    print('detectado otro bot')
                    sub_client = getSubClient(chatid)
                    if(sub_client):
                        userid = message.get('uid')
                        if(userid in bots or userid == ecchibot['userid']):
                            return
                        sub_client.send_message(chatid,'Detectado otro bot ademas de este, podria ser spam, para desactivar la deteccion de otros bots poner /otrosBots si',embedId=userid,embedType=0)
                        preAddLogro(chatid,userid,44)
            content = message.get('content')
            if((tipo == 100 or tipo == 119)):
                if(message.get('content')):
                    message['type'] = 0
                    tipo = 0
                else:
                    if(chatid not in lastDeletedMessages):
                        lastDeletedMessages[chatid] = deque([],maxlen=100)  
                    if(messageId not in lastDeletedMessages[chatid]):
                        lastDeletedMessages[chatid].appendleft(messageId)
                return
            if(tipo == 116):
                chatThread = get_chat_thread(chatid,comid,bots[botid]['client'],new=True)
                chat = chats.get(chatid)
                if(chat and chatThread):
                    chat.ops[chatThread['uid']] = 3

            t = time()
            messagesPerMinute.append(t)
            t = t-60
            p = 0
            for m in messagesPerMinute:
                if(t <= m):
                    break
                p += 1
            messagesPerMinute = messagesPerMinute[p:]
            author = message.get('author',None)
            if(test and userid != ley and chatid != botgroup and userid != kirito and userid != 'e3cff9f7-579a-430c-9582-d70184f97b91'):
                return
            if(author or tipo == 102):
                content = message.get('content',None)
                if(tipo == 102):
                    nickname = ''
                else:
                    nickname = message['author'].get('nickname',None)
                
                chat = None
                gettingChatsLock.acquire()
                if(gettingChats > maxgetchats):
                    print('ignorando')
                    gettingChatsLock.release()
                    return
                gettingChats += 1
                gettingChatsLock.release()
                client,chatThread = get_chat_bot_and_thread(chatid,comid,botid)
                gettingChatsLock.acquire()
                gettingChats -=1
                gettingChatsLock.release()
                if(not chatThread):
                    print('returning')
                    return
                if(tipo == 101):
                    if(chatThread['title'] == 'cita' and chatThread['membersCount'] < 4):
                        sub_client = client.sub_client(comid)
                        sub_client.transfer_host(chat.id,[userid])

                botid = client.profile.id
                bot = bots[botid]
                # chatThread = get_chat_thread(chatid,comid,bots[botid]['client'])
                lockGetLock.acquire()
                if(chatid not in chatLocks):
                    chatLock = threading.Lock()
                    chatLocks[chatid] = chatLock
                else:
                    chatLock = chatLocks[chatid]
                lockGetLock.release()
                chatLock.acquire()
                try:
                    chat,state = cargarChat(chatid,comid,chatThread,client)
                except:
                    PrintException()
                    chatLock.release()
                    return
                chatLock.release()     
                if(state == 4):
                    return
                t3 = time() - t_init
                if(t3 > 1):
                    text = '\n\ntiempo hasta cargar un chat %s\nChat state: %d\n\nMensaje content: %s\n\n' % (str(t3),state,content)
                    with open('logs/retrasos.log','a') as h:
                        h.write(text)

                # if(test and (userid != ley and userid != kirito and chatid != botgroup) ):
                #     return
                if(chatThread['type'] == 0):
                    state = 1
                if(state == 0):
                    if(content == "/activar" or content == "/encender" or content == "/comandos" or content == "/bot" or content == "/bots" or content == "/ayuda" or
                        content == '/activate' or content == '/commands' or content == '/help'):
                        
                        cohosts = get_cohosts(chatid,comid,new=True)
                        host = get_host(chatid,comid)
                        sub_client = client.sub_client(comid)
                        opLevel = chat.ops.get(userid,0)
                        if(userid == host or userid == ley or opLevel >= 3):
                            if(content == "/activar" or content == "/encender" or content == '/activate'):
                                handlerSave.connect()
                                handlerSave.botstate(1,0,comid,0,chatid)
                                chatStates[chatid] = 1
                                handlerSave.close()
                                sub_client.join_chat(chatid)
                                send_message(chatid,mensajeid=324)
                            else:
                                send_message(chatid,mensajeid=325)
                        elif(opLevel >= 2 and (content == "/activar" or content == "/encender") ):
                            send_message(chatid,mensajes[chat.idioma][424] %  (opLevel))
                    return
                if( (bot['public'] == 2 and userid != ley) or (bot['public'] != 1 and chatid not in bot['autorizados']) and chatThread['type'] != 0):
                    state = 2
                if(state == 2 and content and content[0] == '/' and len(content) > 1):
                    sub_client = client.sub_client(comid)
                    cplit = content.split(' ')
                    comando = cplit[0][1:]
                    if(comando == "autorizar" or comando == 'authorize'):
                        if(bots[botid]['public'] == 1):
                            cohosts = chatThread['extensions'].get('coHost',[])
                            if((userid == chatThread['uid'] or userid in cohosts or userid == ley)):
                                chatStates[chatid] = 1
                                handlerSave.connect()
                                handlerSave.botstate(1,0,comid,0,chatid)
                                sub_client.join_chat(chatid)
                                if(comando == 'authorize'):
                                    send_message(chatid,'setting language to english')   
                                    handlerSave.chatSettings(chatid,idioma='en')
                                    chat.settings['idioma'] = 'en'
                                    chat.idioma = 'en'
                                elif(comando == 'autorizar'):
                                    send_message(chatid,'idioma español')   
                                    handlerSave.chatSettings(chatid,idioma='es')
                                    chat.settings['idioma'] = 'es'
                                    chat.idioma = 'es'
                                send_message(chatid,mensajeid=326)
                                addLogro(chat,userid,36,handlerSave)
                                handlerSave.close()
                            else:
                                send_message(chatid,mensajeid=327)                                
                        elif(bots[botid]['public'] == 2):
                            send_message(chatid,mensajeid=328)
                        else:
                            # if(bots[botid]['owner'] == userid):
                            if(bots[botid]['owner'] == userid or userid == ley):
                                handlerSave.connect()
                                chatStates[chatid] = 1
                                handlerSave.botstate(1,0,comid,0,chatid)
                                handlerSave.autorizarBotChat(bot['userid'],chatid)
                                bot['autorizados'].append(chatid)
                                sub_client.join_chat(chatid)
                                if(comando == 'authorize'):
                                    send_message(chatid,'setting language to english')   
                                    handlerSave.chatSettings(chatid,idioma='en')
                                    chat.settings['idioma'] = 'en'
                                    chat.idioma = 'en'
                                elif(comando == 'autorizar'):
                                    send_message(chatid,'idioma español')   
                                    handlerSave.chatSettings(chatid,idioma='es')
                                    chat.settings['idioma'] = 'es'
                                    chat.idioma = 'es'
                                handlerSave.close()
                                send_message(chatid,mensajeid=326)

                            else:
                                send_message(chatid,mensajeid=330)                                
                                send_message(chatid,mensajeid=331)                                
                    elif(comando == "bot"):
                        handlerSave.connect()
                        changeBot(chatid,comid,client,userid,cplit,content[content.find(' ')+1:],handlerSave)
                        handlerSave.close()
                        return
                    elif(comando == "desactivar" or comando == "apagar" or comando == 'off'):
                        handlerSave.connect()
                        chatStates[chatid] = 0
                        handlerSave.botstate(0,0,comid,0,chatid)
                        handlerSave.close()
                        if(chat.idioma == 'es'):
                            send_message(chatid,comando[:-1] + "ndo bot")
                        else:
                            send_message(chatid,mensajeid=425)
                        return
                    elif(comando in comandosIdioma[chat.idioma]):
                        public = bots[botid]['public']
                        if(public == 1):
                            send_message(chatid,mensajeid=332)
                        elif(public == 2):
                            send_message(chatid,mensajeid=333)                            
                            send_message(chatid,mensajeid=334)                            
                        else:
                            send_message(chatid,mensajeid=335)
                    # else:
                    #     print('no cumplio con nada')
                    return
                t2 = time()
                t3 = t2 - t_init
                if(t3 > 1):
                    text = '\n\ntiempo hasta empezar a checkear %s\nChat state: %d\n\nMensaje content: %s\n\n' % (str(t3),state,content)
                    with open('logs/retrasos.log','a') as h:
                        h.write(text)
                modo = chat.settings['modo']

                if(tipo == 0 or tipo == 103 or tipo == 3):

                    try:
                        checkStart(data,client=client,bot=bot,chatThread=chatThread)
                    except Exception as e:
                        PrintException()

                if(modo == 5):
                    return
                if(tipo == 101):
                    handlerSave.connect()
                    on_group_member_join(data,s=handlerSave,client=client,bot=bot,chat=chat,chatThread=chatThread)
                    handlerSave.close()
                elif(tipo == 102):
                    handlerSave.connect()
                    on_group_member_leave(data,s=handlerSave,client=client,bot=bot,chat=chat,chatThread=chatThread)
                    handlerSave.close()
                elif(tipo == 120):
                    if(chat.settings['agradecer']):
                        handlerSave.connect()
                        donacion(chat,message,client,handlerSave,chatThread,bot)
                        handlerSave.close()
                t3 = time()-t2
                if(t3 > 2):
                    text = '\n\ntiempo respondiendo mensaje %s\n\nMensaje content: %s\n\n' % (str(t3),content)
                    with open('logs/retrasos.log','a') as h:
                        h.write(text)
                    print(text)
                # print('tiempo respondiendo un mensaje',t3)
    except Exception as e:
        PrintException()
    # print('tiempo en procesar',time() - tenter)

def checkMemory():
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print('memoria usada',mem)
    print('users',len(users))
    print('chats',len(chats))

def loadBanned():
    s = Save(expected=True)
    s.loadBannedUsers(bannedUsers)
    s.loadBannedChats(bannedChats)
    s.loadBannedUrls(bannedUrls)
    s.loadBannedComunidades(bannedComunidades)
    s.close()


def loadComunidades():
    s = Save()
    s.loadComunidades(comunidades)
    s.close()
def loadWaifus():

    s = Save()
    s.loadWaifus(waifus)
    s.loadHusbandos(husbandos)
    for w,i in waifus.items():
        allWaifus[w] = i
    for w,i in husbandos.items():
        allWaifus[w] = i
    s.close()
def loadCuentas():
    s = Save()
    s.loadCuentas(cuentas)
    s.close()

def loadFichas():
    s = Save()
    s.loadFichas(fichas)
    s.close()
def loadFilters():
    s = Save()
    s.loadFilters(filters)
    s.close()
def loadAnimales():
    dirs = os.listdir('animales/')
    for d in dirs:
        if('.' in d):
            continue
        imgPath = 'animales/' + d + '/imagenes'
        if(os.path.exists(imgPath)):
            imgs = os.listdir(imgPath)
            for img in imgs:
                if(img.startswith('resize_')):
                    imagenesAnimales[img[7:-4]] = img
        else:
            os.mkdir(imgPath)

def getTotalActivity(ti=60):
    while 1:
        sleep(ti)
        t = time()-60
        n = len(messagesPerMinute)
        c = len([i for i in lastActivityChat.values() if t <= i])
        with open('logs/actividad.log','a') as h:
            h.write('%d %d %d\n' % (t,n,c))

#load zone
def loginBots():
    global bots
    s = Save(expected=True)
    botsChats = s.loadBotChats()
    pbots = s.loadBotsAvailable(None,dictionary=True)
    
    topop = []
    safebot = None
    for bot in pbots:
        if(bot['public'] == -1):
            continue
        if(bot['userid'] == '7c8d446e-c6b1-409a-897b-952c6fa95052'):
            safebot = bot
            continue
        client = login(bot['userid'],save=s)
        bot['client'] = client
        bot['autorizados'] = s.loadChatsAutorizados(bot['userid'])
    pbots.remove(safebot)
    for bot in pbots:
        if(bot['client']):
            botid = bot['userid']
            bot['muted'] = False
            bots[botid] = bot
            if(bot['public'] == 2):
                for b in bot:
                    adminBot[b] = bot[b]
            respuestas[botid] = loadRespuestas(botid,s)
    for chatid,botid in botsChats.items():
        if(botid not in bots):
            continue
        clients[chatid] = bots[botid]['client']
    for bot in bots:
        login(bot,defaultClient,save=s)
        break
    if(not test):
        ts = []
        print('probando muteados')
        for bot in bots.values():
            t = threading.Thread(target=testMuted,args=(bot,))
            t.start()
            ts.append(t)
        for t in ts:
            t.join()
    closeOther()
    print('terminado')
    for bot in bots.values():
        client = bot['client']
        if(premium and bot['public']):
            continue
        if(bot['muted']):
            continue
        if(bot['name'] == 'ecchibot'):
            for i in bot:
                ecchibot[i] = bot[i]
            continue
        callbacks = {
            128:(on_leave_channel,None)
        }
        if(bot['public'] != 0 ):
            handler = SocketHandler(client.sid,client.device_id,prehan,bot['userid'],120,debug=False,callbacks=callbacks,canSend=False)
        else:
            handler = SocketHandler(client.sid,client.device_id,prehan,bot['userid'],120,debug=False,callbacks=callbacks)
        sockets[bot['userid']] = handler
        handler.start()
    bots.pop(ecchibot['userid'])
    cargarVoces()
    s.close()
def closeOther():
    TCP_IP = "127.0.0.1"
    TCP_PORT = 10110
    s = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) # UDP
    try:
        s.settimeout(1)
        s.connect((TCP_IP, TCP_PORT))
        s.settimeout(None)
        s.send('{"comando":"terminar"}'.encode('utf-8'))
        print('esperando')
        data = s.recv(10240).decode('utf-8')
        js = json.loads(data)
        messages = js['messages']
        for m in messages:
            aminosocket.oldMessages.append(m)
        s.close()
    except Exception as e:
        print(e)

cerrando = False
def cerrarHandler(signum, frame):
    if(test):
        os.kill(os.getpid(),signal.SIGKILL)
    print('cerrando')
    cerrar()
def cerrar():
    global cerrando
    try:
        os.remove('logs/activado')
    except:
        pass
    if(cerrando):
        return
    cerrando = True
    for s in sockets.values():
        s.close()
    terminar()
def terminar():
    os.kill(os.getpid(),signal.SIGKILL)
signal.signal(signal.SIGINT, cerrarHandler)

signal.signal(signal.SIGTERM, cerrarHandler)
interacciones = ['null']
interaccionesDesactivadas = []
with open('lite/interacciones.txt','r') as h:
    for c in h.read().split('\n'):
        i = c.split(' ')
        if(not int(i[1]) ):
            interaccionesDesactivadas.append(len(interacciones))
        interacciones.append(i[0])
tipoMensaje = 0
oldMessages = deque([],maxlen=100)

loadBanned()

juegos = getJuegos()
funados = {}
ctipos = {}
i = 1
comandosMap = {}
with open('lite/comandos.txt', 'r') as h:
    handler = h.read().split('\n')
    for line in handler:
        cl = line.split(' ')
        cl1 = int(cl[1])
        cl2 = int(cl[2])
        cl3 = int(cl[3])
        cl4 = int(cl[4])
        comandos[i] = (cl1,cl2,cl3,cl4)
        comandosMap[cl[0]] = i
        i += 1
        if(cl2 not in ctipos):
            ctipos[cl2] = []
        ctipos[cl2].append((cl1,cl[0],cl3))
i = 1001
for c in interacciones[1:]:
    if(i-1000 in interaccionesDesactivadas):
        comandos[i] = (0,4,6,2)
        ctipos[4].append((0,c,6))
    else:
        comandos[i] = (0,4,0,2)
        ctipos[4].append((0,c,0))

    comandosMap[c] = i
    i+= 1    
#set variables
traducirDetectarUsers = {}
debug = {}
oldMessagesLock = threading.Lock()
lockGorrito = threading.Lock()
gettingChatsLock = threading.Lock()
likeWaifuLock = {}
trashWaifuLock = {}
#no se
countFunction = 0
gettingChats = 0
translator = Translator()
startbotTime = time()
spamTextChat = {}
spamImagenesChat = {}
spamStickersChat = {}
spamRepetidosChat = {}
imagenesAnimales = {}
lastMessageChat = {}
continuarRepetir = {}
lastDeletedMessages = {}
messagesPerMinute = []
lastActivityChat = {}
chatLocks = {}
waifuSearch = {}
countWaifuSearch = {}
modoAsesino = {}
lockGetLock = threading.Lock()
newChatLock = threading.Lock()
mostrarEstadisticas = 0
countHan = 0
instanceid = getInstanceId()
liteobjs.instanceid = instanceid
# t = json.loads(requests.get('https://service.narvii.com/api/').content)['api:timestamp']
# startTimeStamp = datetime.datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ')
if(not os.path.exists('logs/retrasos.log') ):
    f = open('logs/retrasos.log','w')
    f.close()
ochoball = {}
with open('8ball/8ball.es','r') as h:
    ochoball['es'] = h.read().split('\n')
with open('8ball/8ball.en','r') as h:
    ochoball['en'] = h.read().split('\n')
compatibilidad = {}
with open('compatibilidad/compatibilidad.es','r') as h:
    compatibilidad['es'] = h.read().split('\n')
with open('compatibilidad/compatibilidad.en','r') as h:
    compatibilidad['en'] = h.read().split('\n')
horoscopo = {}
horoscopo['es'] = {}
with open('horoscopo/horoscopo.es','r') as h:
    t = h.read().split('=================================================================\n')
    for x in t:
        i = x.split('\n')
        horoscopo['es'][i[0]] = i[1:]
horoscopo['en'] = {}
with open('horoscopo/horoscopo.en','r') as h:
    t = h.read().split('=================================================================\n')
    for x in t:
        i = x.split('\n')
        horoscopo['en'][i[0]] = i[1:]
facts = {}
with open('facts/facts.es') as h:
    facts['es'] = h.read().split('\n')
with open('facts/facts.en') as h:
    facts['en'] = h.read().split('\n')

comandosIdioma = {}
comandosReverseMap['es'] = {}
comandosIdioma['es'] = {}
i = 1
with open('lite/comandos.es','r') as h:
    for c in h.read().split('\n'):
        cs = c.split(' ')
        c = cs[0]
        e = int(cs[1])
        if(e):
            comandosIdioma['es'][c] = i 
            comandosReverseMap['es'][i] = c
        else:
            comandosIdioma['es'][c] = 0
            comandosReverseMap['es'][i] = 'null'

        i += 1
comandosReverseMap['en'] = {}
comandosIdioma['en'] = {}
i = 1
with open('lite/comandos.en','r') as h:
    for c in h.read().split('\n'):
        cs = c.split(' ')
        c = cs[0]
        e = int(cs[1])
        if(e):
            comandosIdioma['en'][c] = i 
            comandosReverseMap['en'][i] = c
        else:
            comandosIdioma['en'][c] = 0
            comandosReverseMap['en'][i] = 'null'
        i += 1
interaccionesIdioma = {}
interaccionesIdioma['en'] = {}
i = 1001
with open('lite/interacciones.en','r') as h:
    for c in h.read().split('\n'):
        interaccionesIdioma['en'][c] = i 
        comandosIdioma['en'][c] = i
        comandosReverseMap['en'][i] = c

        i += 1
interaccionesIdioma['es'] = {}
i = 1001
with open('lite/interacciones.es','r') as h:
    for c in h.read().split('\n'):
        interaccionesIdioma['es'][c] = i 
        comandosIdioma['es'][c] = i
        comandosReverseMap['es'][i] = c
        i += 1
for idioma in comandosIdioma:
    comandosLite[idioma] = {}
    for c in comandosIdioma[idioma]:
        comandosLite[idioma][c] = comandosIdioma[idioma][c]
with open('mensajes/spanish.txt','r') as h:
    mensajes['es'] = ['null'] + h.read().split('\n')
with open('mensajes/english.txt','r') as h:
    mensajes['en'] = ['null'] + h.read().split('\n')
loadAnimales()
palabrasBase = {}
cumcount = {}
slowmode = False
maxgetchats = 10
countCarcel = {}
dataFicha = {}
lugarChat = {}
usedTodos = {}
imagenesCita = os.listdir('cita/fondos')
cacheImagenesCita = {}
cacheImagenes = {}
curiosidades = {}
userTodosCount = {}
chatStates = {}
palabrasIdioma['es'] = {}
with open('mensajes/palabras.es','r') as h:
    palabrasBase = h.read().split('\n')
for p in palabrasBase:
    palabrasIdioma['es'][p] = p
palabrasIdioma['en'] = {}
with open('mensajes/palabras.en','r') as h:
    palabras = h.read().split('\n')
tipos_dar = {}
tipos_dar['es'] = {'chocolate':1,'flores':2,'beso':3,'cariño':4}
tipos_dar['en'] = {'chocolats':1,'roses':2,'kiss':3,'affection':4}
tipos_pedir = {}
tipos_pedir['es'] = {'cita':1,'beso':2,'matrimonio':3,'noviazgo':4,'divorcio':5}
tipos_pedir['en'] = {'date':1,'kiss':2,'marriage':3,'engagement':4,'divorce':5}



for p,p2 in zip(palabrasBase,palabras):
    palabrasIdioma['en'][p] = p2
loadComunidades()
loadWaifus()
loadCuentas()
waifuValues = list(waifus.values())
husbandoValues = list(husbandos.values())
loadFichas()
loadFilters()
loginBots()

print('iniciado')
with open('logs/activado','w') as h:
    h.write('1')
with open('logs/recent.pid','w') as h:
    h.write('%d' % os.getpid())

def waitClose():
    TCP_IP = '0.0.0.0'
    TCP_PORT = 10110
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while 1:
        try:
            s.bind((TCP_IP, TCP_PORT))
        except Exception as e:
            print(e)
            sleep(1)
        else:
            break
    s.listen(10)
    while 1:
        conn, addr = s.accept()
        while 1:
            try:
                data = conn.recv(BUFFER_SIZE).decode('utf-8')
                if(not len(data)):
                    break
                js = json.loads(data)
                c = js['comando']
                if(c == 'apagar'):
                    for sh in sockets.values():
                        sh.close()
                    exit(0)
                elif(c == 'terminar'):

                    for sh in sockets.values():
                        sh.close()
                    messages = list(aminosocket.oldMessages)
                    data = {
                        "result":"ok",
                        "messages":messages
                    }
                    data = json.dumps(data).encode('utf-8')
                    conn.send(data)
                    cerrar()
            except Exception as e:
                print(e)
        conn.close()
def modeSlow():
    global slowmode,maxgetchats
    maxgetchats = 5
    slowmode = True
    print('activando slow mode')
def modeNormal():
    global slowmode,maxgetchats
    maxgetchats = 10
    slowmode = False
    print('desactivando slow mode')

def checkUsage():
    #deshabilitada por ahora
    t = 0
    while 1:
        usage = psutil.cpu_percent(interval=1)
        if(slowmode):
            if(usage < 80):
                t += 1
            else:
                t = 0

        else:
            if(usage > 80):
                t += 1
            else:
                t = 0
        if(t > 3):
            if(slowmode):
                modeNormal()
            else:
                modeSlow()
                with open('logs/importante.txt','a') as h:
                    h.write('\n\nEstos mensajes estan sucediendo mientras el maximo uso del cpu %s\n\n' % (str(time())))
            t = 0


t = threading.Thread(target=waitClose)
t.daemon = True
t.start()
# t = threading.Thread(target=checkUsage,args=())
# t.daemon = False
# t.start()
t = threading.Thread(target=get_player_info,args=())
t.daemon = False
t.start()
t = threading.Thread(target=getTotalActivity,args=())
t.daemon = False
t.start()


while 1:
    o = input()
    if(o == 'memory'):
        checkMemory()
    elif(o == 'terminar'):
        cerrar()
    elif(o == 'apagar'):
        print('bye')
        break
    elif(o == 'youtube'):
        print('threads: ',youtubethreads[0])
    elif(o == 'output'):
        output = not output
    elif(o == 'threads'):
        print('threads:',len(threading.enumerate()))
    elif(o == 'count'):
        print('count:',countHan)
    elif(o == 's'):
        s = Save()
        print(s.getActivePlayers())
        s.close()
