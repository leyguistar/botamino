from jikanpy import Jikan
import jikanpy
from googletrans import Translator
from litefuns import send_message,send_link,send_text_imagen
from liteobjs import temporadas,dias
from litefuns import addLogro
from exception import PrintException
import requests
from time import sleep
from liteobjs import defaultClient,mensajes
jikan = Jikan()
translator = Translator()

def buscarAnime(chatid,m,client,idioma='es'):
    jikanError = True
    text = ''
    for i in range(5):
        try:
            if(m.isdigit()):
                result = jikan.anime(int(m))
            elif(m):
                text = mensajes[idioma][361] + '\n'
                search_result = jikan.search('anime', m, page=1)
                r = search_result['results'][0]
                # print(result)
                for result in search_result['results'][:10]:
                    text += result['title'] + ' (%d)\n' % (result['mal_id'])
                result = r
                send_message(chatid,text.replace('\n','\n\n'))
                text = ''

        except jikanpy.exceptions.APIException as e:
            sleep(1)
        except:
            PrintException()

        else:
            text += (mensajes[idioma][353] % result['title']) + '\n'
            synopsis = result['synopsis']
            text += mensajes[idioma][354] % (synopsis if idioma == 'en' else translator.translate(synopsis,src='en',dest=idioma).text )
            text += '\n'
            text += mensajes[idioma][355] % (result['episodes']) + '\n'
            if('rating' in result):
                rating = result['rating']
            elif('rated' in result):
                rating = result['rated']
            else:
                rating = 'desconocido'

            text += 'Rating: ' + rating + '\n'
            if('aired' in result):
                text += mensajes[idioma][356] % result['aired']['from'].split('T')[0] + '\n'
                if(result['aired']['to']!= None):
                    text += mensajes[idioma][357] % result['aired']['to'].split('T')[0] + '\n'

            if('Hentai' in rating or rating.startswith('Rx')):
                send_message(chatid,text.replace('\n','\n\n'))
                send_message(chatid,mensajeid=358)
                jikanError = False
                return 'h'
            else:
                send_text_imagen(chatid,text.replace('\n','\n\n'),result['image_url'])
                jikanError = False
            break
    if(jikanError):
        send_message(chatid,mensajeid=359)


def temporada(chatid,content,idioma='es'):
    if(len(content) < 2):
        text = mensajes[idioma][360].replace('\\','\n')
        send_message(chatid,text)
    else:
        if(idioma != 'es'):
            temporadas2 = list(temporadas.values())
        else:
            temporadas2 = temporadas
        if(content[1].isdigit() and content[2] in temporadas2):
            jikanError = True
            for i in range(5):
                try:
                    if(idioma == 'es'):
                        temp = jikan.season(year=int(content[1]),season=temporadas[content[2]] )
                    else:
                        temp = jikan.season(year=int(content[1]),season=content[2] )

                except jikanpy.exceptions.APIException as e:
                    # PrintException()
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
                send_message(chatid,mensajeid=364)
def emision(chatid,content,idioma='es'):
    if(len(content) != 2):
        text = mensajes[idioma][363].replace('\\','\n')
        send_message(chatid,text)
    else:
        if(idioma != 'es'):
            dias2 = list(dias.values())
        else:
            dias2 = dias
        if( content[1] in dias2):
            jikanError = True
            for i in range(5):
                try:
                    if(idioma == 'es'):
                        day = dias[content[1]]
                    else:
                        day = content[1]
                    temp = jikan.schedule(day=day)
                    # temp = jikan.season(year=int(content[1]),season=temporadas[content[2]] )
                except jikanpy.exceptions.APIException as e:
                    # PrintException()
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
                send_message(chatid,mensajeid=362)

def openings(chatid,content,m,client,idioma='es'):
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
                sleep(1)
            except:
                PrintException()

                text += '\n\n'.join(result['opening_themes'])
                if('rating' in result):
                    rating = result['rating']
                elif('rated' in result):
                    rating = result['rated']
                else:
                    rating = 'desconocido'
                if('Hentai' in rating or rating.startswith('Rx')):
                    send_message(chatid,text.replace('\n','\n\n'))
                    send_message(chatid,mensajeid=358)
                else:
                    send_text_imagen(chatid,text.replace('\n','\n\n'),result['image_url'])

                
                jikanError = False
                break
        if(jikanError):
            send_message(chatid,mensajeid=365)
    else:
        send_message(chatid,mensajeid=366)
def endings(chatid,content,m,client,idioma='es'):
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

                text = 'Endings: '+ result['title'] +'\n\n'
            except jikanpy.exceptions.APIException as e:
                print(e)
                sleep(1)
            else:
                text += '\n\n'.join(result['ending_themes'])
                if('rating' in result):
                    rating = result['rating']
                elif('rated' in result):
                    rating = result['rated']
                else:
                    rating = 'desconocido'
                if('Hentai' in rating or rating.startswith('Rx')):
                    send_message(chatid,text.replace('\n','\n\n'))
                    send_message(chatid,mensajeid=358)
                else:
                    send_text_imagen(chatid,text.replace('\n','\n\n'),result['image_url'])
                jikanError = False
                break
        if(jikanError):
            send_message(chatid,mensajeid=366)

    else:
        send_message(chatid,mensajeid=367)

def manga(chatid,content,m,client,idioma='es'):
    if(len(content) >= 2 ):
        jikanError = True
        text = ''
        for i in range(5):
            try:
                if(m.isdigit()):
                    result = jikan.manga(int(m))
                elif(m):
                    text = mensajes[idioma][361] +'\n'
                    search_result = jikan.search('manga', m.lstrip(), page=1)
                    r = search_result['results'][0]
                    print(r)
                    for result in search_result['results'][:10]:
                        text += result['title'] + ' (%d)\n' % (result['mal_id'])
                    result = r
                    send_message(chatid,text.replace('\n','\n\n'))
                    text = ''

            except jikanpy.exceptions.APIException as e:
                # PrintException()
                print(e)
                sleep(1)
            else:
                text += mensajes[idioma][353] % result['title'] + '\n'
                synopsis = result['synopsis']
                text += mensajes[idioma][354] % (synopsis if idioma == 'en' else translator.translate(synopsis,src='en',dest=idioma).text )
                text += '\n'
                if(result['chapters'] != None):
                    text += mensajes[idioma][369] % result['chapters'] + '\n'
                if('published' in result):
                    text += mensajes[idioma][356] % result['published']['from'].split('T')[0] + '\n'
                    if(result['published']['to']!= None):
                        text += mensajes[idioma][357] + result['published']['to'].split('T')[0] + '\n'
                send_text_imagen(chatid,text.replace('\n','\n\n'),result['image_url'])
                jikanError = False
                break
        if(jikanError):
            send_message(chatid,mensajeid=365)
    else:
        send_message(chatid,mensajeid=368)

def personaje(chatid,content,m,client,idioma='es'):
    if(len(content) >= 2 ):
        jikanError = True
        text = ''
        for i in range(5):
            try:
                if(m.isdigit()):
                    result = jikan.character(int(m))
                elif(m):
                    text = mensajes[idioma][361] + '\n'
                    search_result = jikan.search('character', m, page=1)
                    r = search_result['results'][0]
                    print(r)
                    for result in search_result['results'][:10]:
                        text += (mensajes[idioma][370] % result['name']) + ' (%d)\n\n' % (result['mal_id'])
                        if(len(result['anime']) > 0):
                            text += 'anime: ' + result['anime'][0]['name'] + '\n'
                        if(len(result['manga']) > 0):
                            text += 'manga: ' + result['manga'][0]['name'] + '\n'
                        text += '\n'
                    result = jikan.character(r['mal_id'])
                    send_message(chatid,text.replace('\n','\n\n'))
                    text = ''

            except jikanpy.exceptions.APIException as e:
                print(e)
                sleep(1)
            else:
                text += mensajes[idioma][370] % (result['name']) + '\n'
                synopsis = result['about']
                text += mensajes[idioma][354] % (synopsis if idioma == 'en' else translator.translate(synopsis,src='en',dest=idioma).text )
                text += '\n'

                send_text_imagen(chatid,text.replace('\\ n','').replace('\\',''),result['image_url'])
                jikanError = False
                break
        if(jikanError): 
            send_message(chatid,'Error id no encontrado')
    else:
        send_message(chatid,'uso: /personaje id: da informacion de el personaje con ese id (resultado de la busqueda)')
