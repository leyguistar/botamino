#!/usr/bin/env python3
import amino
import os
import sys
from time import time
import json
from save import Save
import threading
import requests
import googlesearch
client = amino.Client()
waifucomid = 210208021
def log_in(alias='bot',userid=None):
    if(userid):
        login = s.loginInfo(id=userid,dictionary=True)
    else:
        login = s.loginInfo(alias=alias,dictionary=True)
    # if(True):
    # if(False):
    if(login['jsonResponse'] and login['lastLogin'] + 3600*8 > time()):
        print('inicio cache')
        client.login_cache(login['jsonResponse'] )
    else:
        r = client.login(secret=login['secret'],get=True)
        # print('iniciando normal')
        # r = client.login(email=login[0],password=login[1],get=True)

        if(type(r) == dict or r[0] != 200):
            print(r)
            return None
        r1 = json.loads(r[1])
        r1['userProfile']['content'] = 'cache'
        r1['secret'] = login['secret']
        r1 = json.dumps(r1)
        s.newLogin(id=client.profile.id,jsonResponse=r1)
    return login
def curate_thread(wikiId,wiki):

    # r = sub_client.edit_wiki(wikiId,wiki)
    r = sub_client.edit_wiki(wikiId,{'keywords':wiki['keywords']})
    # print(r)
    # print(wiki['label'])
    r = sub_client.request_wiki_curation(wikiId,'Aceptala please')
    requestId = r['knowledgeBaseRequest']['requestId']
    if(wiki['keywords'] == 'waifu'):
        r = sub_client.accept_wiki_request(requestId,["68e6d772-7f30-4095-850a-2ee225334d1d"])
    elif(wiki['keywords'] == 'husbando'):
        r = sub_client.accept_wiki_request(requestId,["670df48a-6942-4759-b838-1dc3c44d87ce"])
    else:
        return
    # print(r)
    sub_client.hide(wikiId=wikiId)

def getGender(anime,name):
    i = 0
    searchs = googlesearch.search("site:{} {}".format('fandom.com', 'anime' + ' ' + name), stop=5)
    for url in searchs:
        url = url.replace('/es/','/')
        print(url)
        text = requests.get(url).text
        i+=1
        print(i)
        if('<div class="pi-data-value pi-font">Female</div>' in text):
            return 'waifu'
        elif('<div class="pi-data-value pi-font">Male</div>' in text):
            return 'husbando'
        else:
            text = text.replace(' ','').replace('\n','').replace('\r','')
            if('>Female<' in text and '>Male<' not in text):
                return 'waifu'
            elif('>Male<' in text and '>Female<' not in text):
                return 'husbando'
            else:
                if('/wiki/Category:Males' in text and '/wiki/Category:Females' not in text):
                    return 'husbando'
                elif('/wiki/Category:Females' in text and '/wiki/Category:Males' not in text):
                    return 'waifu'
                else:
                    continue
    return 'pendiente'

def props2dict(props):
    d = {}
    for p in props:
        d[p['title']] = p['value']
    return d
with open('deviceids.txt','r') as h:
	deviceids = h.read().split('\n')

s = Save(file='default.set')
log_in('moon')
sub_client = client.sub_client(waifucomid)
for start in range(0,601,100):
    wikis = sub_client.get_user_wikis(userId=client.profile.id,start=start,size=100,raw=True)['itemList']
    for wiki in wikis:
        if(wiki['status'] == 9):
            continue
        wikiId = wiki['itemId']
        keywords = wiki['keywords']
        if(keywords == 'pendiente'):
            props = props2dict(wiki['extensions']['props'])
            origen = props['origen']
            print(wikiId,wiki['mediaList'][0][1])
            # print()
            print(origen,wiki['label'])
            r = getGender(origen,wiki['label'])
            print(r)
            if(r == 'pendiente'):
                print(origen,wiki['label'],'(w,h,p,e): ',end='')
                i = input()
                wiki['keywords'] = r
                if(i == 'w'):
                    wiki['keywords'] = 'waifu'
                elif(i == 'h'):
                    wiki['keywords'] = 'husbando'
                elif(i == 'p'):
                    continue
                elif(i == 'e'):
                    r = sub_client.delete_wiki(wikiId)
                    print(r)
                    continue
                else:
                    print('invalida')
                    continue
            else:
                wiki['keywords'] = r
        else:
            continue
        t = threading.Thread(target=curate_thread,args=(wikiId,wiki))
        t.start()
        # r['']
        # nombre = wiki['label']
        # props = wiki['extensions']['props']
        # origen = None
        # for p in props:
        #     if(p['title'] == 'origen'):
        #         origen = p['value']
        #         break
        # tipo = wiki['keywords']
        # icon = 
        # s.addWaifu(nombre,origen,descripcion,wikiId,tipo,img=icon,mal_id=mal_id,)



exit()
