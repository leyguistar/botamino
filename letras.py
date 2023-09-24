import html2text
import re
import urllib.request
from urllib.parse import unquote
from urllib.parse import quote
import requests
import ujson as json
cacheLetras = {}

def letra(id):
    print('https://www.musica.com/letras.asp?letra=' + id)
    html = urllib.request.urlopen('https://www.musica.com/letras.asp?letra=' + id).read().decode('utf-8')
    letra = html2text.html2text(html)
    with open('result.txt','w') as h:
        h.write(letra)
    r4 = re.compile(r'<title>(.*)</title>',re.DOTALL)
    try:
        rLetra = re.compile(r'\[\]\(https://i\.musicaimg\.com/im/a-menos\.svg\)\s(.*)_fuente:',re.DOTALL)
        l = rLetra.findall(letra)[0]
    except:
        rLetra = re.compile(r'\[\]\(https://i\.musicaimg\.com/im/a-menos\.svg\)\s(.*)_musica\.com_',re.DOTALL)
        l = rLetra.findall(letra)[0]

    title = r4.findall(html)[0]
    title = title[:title.rfind('|')] + '\n'
    l = title + l
    return l

def buscar(name,chatid,idioma='es'):
    text = html2text.html2text(urllib.request.urlopen('https://www.musica.com/letras.asp?t2=' + quote(name)).read().decode('utf-8'))
    r3 = re.compile(r'\(https://www.musica.com/letras.asp\?letra=(\d*)\)\|',re.DOTALL)
    ids = r3.findall(text)
    if(idioma == 'es'):
        text = 'Resultados:\n'
        cacheLetras[chatid] = ['0']
        nombres = ['0']
        for i in ids:
            letra = urllib.request.urlopen('https://www.musica.com/letras.asp?letra=' + i).read().decode('utf-8')
            r4 = re.compile(r'<title>(.*)</title>',re.DOTALL)
            title = r4.findall(letra)[0]
            title = title[:title.rfind('|')]
            nombres.append(title)
            text += title + ' (%s)\n' % (len(cacheLetras[chatid]))
            cacheLetras[chatid].append(i)
        if(not ids):
            response = requests.get('https://some-random-api.ml/lyrics?title=' + quote(name) )
            if(response.status_code == 200):
                data = json.loads(response.text)
                return {"result":"lyrics","lyrics":data}
            else:
                return {"result":"Fail"}
        else:
            return {"result":"letras","letras":nombres}
    else:
        response = requests.get('https://some-random-api.ml/lyrics?title=' + quote(name) )
        if(response.status_code == 200):
            data = json.loads(response.text)
            return {"result":"lyrics","lyrics":data}
        else:
            return {"result":"Fail"}
