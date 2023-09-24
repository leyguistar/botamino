import requests
from urllib.parse import unquote
from urllib.parse import quote
import ujson as json
import random
from liteobjs import defaultClient,confidence,bannedUrls,sentBooru,mensajes
from litefuns import nudeDetect,good_upload,urlAmino,send_link,send_message
from litefuns import send_booru
from exception import PrintException

def buscarLoli(chatid,m='',idioma='es',ecchi=False,offFilter=False):
    if(offFilter):
        print('offFilter')
        tags = 'order%3Arank'
        sanitized = True
    else:

        sanitized = False
        print('with filters')
        tags = 'rating%3As+order%3Arank'
    if(m):
        m = '+'.join([quote(i) for i in m.split(' ')])
        result = requests.get(f'https://lolibooru.moe/post.json?limit=100&tags={tags}+{m}').text
    else:
        result = requests.get(f'https://lolibooru.moe/post.json?limit=100&tags={tags}').text
    link = None
    res = False
    result = json.loads(result)
    if(result):
        for i in range(10):
            try:
                r = random.choice(result)
                url = r['sample_url']
                if(url in bannedUrls):
                    continue
                res = send_booru(chatid,url,r['file_url'],mensajes[idioma][489],ecchi=ecchi,sanitized=sanitized)
                if(res):
                    break
            except Exception as e:
                print(e)
                print('reintentando')
    else:
        send_message(chatid,mensajeid=490,ecchi=ecchi)
        send_link(chatid,'http://st1.narvii.com/7680/d0b72bcf6e50745f0256acaf27770b2b8d70b763r5-184-180_00.jpeg',sanitized=True,ecchi=ecchi)

def buscarChica(chatid,m='',idioma='es',ecchi=False,offFilter=False):
    if(offFilter):
        print('offFilter')
        tags = 'order%3Arank'
        sanitized = True
    else:

        sanitized = False
        print('with filters')
        tags = 'rating%3As+order%3Arank'

    if(m):
        m = '+'.join([quote(i) for i in m.split(' ')])
        result = requests.get(f'https://yande.re/post.json?limit=100&tags={tags}+{m}').text
    else:
        result = requests.get(f'https://yande.re/post.json?limit=100&tags={tags}').text
    link = None
    result = json.loads(result)
    if(result):
        for i in range(10):
            try:
                r = random.choice(result)
                url = r['sample_url']
                if(url in bannedUrls):
                    continue
                if(m):
                    text = mensajes[idioma][491] % (m)
                else:
                    text = 'tags: ' + r['tags']
                res = send_booru(chatid,url,r['file_url'],text,ecchi=ecchi,sanitized=sanitized)
                if(res):
                    break
            except Exception as e:
                PrintException()
                print('reintentando')
    if(link):
        response = send_link(chatid,link,sanitized=True,ecchi=ecchi)
        if(response):
            sentBooru[response['messageId']]  = url
def buscarDanbooru(chatid,m="",idioma='es',ecchi=False,offFilter=False):
    client = defaultClient
    if(offFilter):
        print('offFilter')
        tags = 'order%3Arank'
        sanitized = True
    else:

        sanitized = False
        print('with filters')
        tags = 'rating%3As+order%3Arank'
    if(m):
        m = '+'.join([quote(i) for i in m.split(' ')])
        result = requests.get(f'https://danbooru.donmai.us/posts.json?limit=100&tags={tags}+{m}').text
    else:
        result = requests.get(f'https://danbooru.donmai.us/posts.json?limit=100&tags={tags}').text
    link = None
    result = json.loads(result)
    if(result):
        for i in range(10):
            try:
                r = random.choice(result)
                url = r['file_url']
                if(url in bannedUrls):
                    continue
                if(m):
                    text = mensajes[idioma][491] % (m)
                else:
                    text = 'tags: ' + r['tag_string_general']

                res = send_booru(chatid,url,r['file_url'],text,ecchi=ecchi,sanitized=sanitized)
                if(res):
                    break
            except Exception as e:
                PrintException()
                print('reintentando')
    if(link):
        response = send_link(chatid,link,sanitized=True,ecchi=ecchi)
        if(response):
            sentBooru[response['messageId']]  = url

def buscarMoe(chatid,m="",idioma='es',ecchi=False,offFilter=False):
    if(offFilter):
        print('offFilter')
        tags = 'order%3Arank'
        sanitized = True
    else:

        sanitized = False
        print('with filters')
        tags = 'rating%3As+order%3Arank'

    client = defaultClient
    if(m):
        m = '+'.join([quote(i) for i in m.split(' ')])
        result = requests.get(f'https://konachan.com/post.json?limit=100&tags={tags}+{m}').text
    else:
        result = requests.get(f'https://konachan.com/post.json?limit=100&tags={tags}').text
    link = None
    result = json.loads(result)
    if(result):
        for i in range(10):
            try:
                r = random.choice(result)
                url = r['sample_url']
                if(url in bannedUrls):
                    continue
                if(m):
                    text = mensajes[idioma][491] % (m)
                else:
                    text = 'tags: ' + r['tags']

                res = send_booru(chatid,url,r['file_url'],text,ecchi=ecchi,sanitized=sanitized)
                if(res):
                    break
            except Exception as e:
                PrintException()
                print('reintentando')
    if(link):
        response = send_link(chatid,link,sanitized=True,ecchi=ecchi)
        if(response):
            sentBooru[response['messageId']]  = url
def buscarr34(chatid,m=""):
    client = defaultClient
    m = '+'.join([quote(i) for i in m.split(' ')])
    result = requests.get(f'https://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&tags={m}').text
    link = None
    result = json.loads(result)
    if(result):
        for i in range(10):
            try:
                r = random.choice(result)
                url = r['sample_url']
                text = mensajes['es'][491] % (m)
                res = send_booru(chatid,url,r['file_url'],text,ecchi=False,sanitized=True)
                if(res):
                    break
            except Exception as e:
                PrintException()
                print('reintentando')

