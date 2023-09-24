#!/usr/bin/env python3
import amino
import os
import requests
client = amino.Client()
client.sid = 'AnsiMSI6IG51bGwsICIwIjogMiwgIjMiOiAwLCAiMiI6ICIxZTZlZTc1MS0wMTJjLTQ0MjYtYjdhNi02YmMxZWNhZDQ4ZWUiLCAiNSI6IDE2MTc3OTgzNTAsICI0IjogIjE4MS4yMDguMjUzLjE0MyIsICI2IjogMTAwfUoMlmFy0P3ajMzIEy38gcJlzYhG'
sub_client = client.sub_client(173269824)
dirs = os.listdir('interaccion')
dirs.remove('getnew.py')
dirs.remove('stats.en')
dirs.remove('stats.es')
inodes = {}
folders = sub_client.get_shared_folders(size=100)['folderList']
names = {}
for i in folders:
    names[i['title']] = i
for d in dirs:
    mediaList = []
    links = []
    try:
        gifs = os.listdir('interaccion/' + d + '/SFW/')
    except Exception as e:
        print(e)
        continue
    if(not gifs):
        continue
    # if(os.path.exists('interaccion/' + d + '/links.txt') and os.stat('interaccion/' + d + '/links.txt').st_size != 0):
    #     if(d not in names):
    #         r = sub_client.create_shared_folder(d)
    #         folderId = r['folder']['folderId']
    #         print(r)
    #     else:            
    #         n = names[d]['filesCount']
    #         if(n == 0):
    #             folderId = names[d]['folderId']
    #         elif(names[d]['filesCount'] != len(gifs)):
    #             folderId = names[d]['folderId']
    #             print('borrando',d)
    #             r = sub_client.delete_folder(folderId)
    #             print(r)
    #             r = sub_client.create_shared_folder(d)
    #             print(r)
    #             folderId = r['folder']['folderId']
    #         else:
    #             continue
    #     with open('interaccion/' + d + '/links.txt') as h:
    #         links = h.read().split('\n')
    #     for l in links:
    #         mediaList.append([100,l,None])
    #     r = sub_client.post_file(mediaList,folderId)
    #     print(r)
    #     if(r['fileIdList']):
    #         continue
    print(d)
    if(d in names):
        folderId = names[d]['folderId']
        n = names[d]['filesCount']
        print(d,n, len(gifs))
        if(n == 0):
            print('como esta vacia aprovechando para subir')
        else:
            r = sub_client.delete_folder(folderId)
            print(r)
            r = sub_client.create_shared_folder(d)
            print(r)
            folderId = r['folder']['folderId']

    else:
        print('creando',d)
        r = sub_client.create_shared_folder(d)

        folderId = r['folder']['folderId']
    # continue
    for gif in gifs:
        filename = 'interaccion/' + d + '/SFW/' + gif
        print(filename)
        inode = os.stat(filename).st_ino
        if(inode in inodes):
            link = inodes[inode]
        else:
            for i in range(10):
                try:
                    link = client.upload_media(f=filename,timeout=5)
                    if(type(link) == dict):
                        if(link['api:statuscode'] == 102):
                            print(link)
                            print(":\\")
                            input()
                        else:
                            print(link)
                            input()
                    #         link = client.upload_hd(f=filename)
                    #     else:
                    #         link = client.upload_media(f=filename,timeout=5)
                    # if(type(link) != str):
                except:
                    pass
                else:
                    break
            else:
                continue
            inodes[inode] = link
        print(link)
        links.append(link)
    try:
        mediaList = []
        badlinks = []
        for link in links:
        #     response = requests.get(link)
        #     if(response.status_code != 200):
        #         print('badlink',link)
        #         badlinks.append(link)
        #         continue
            mediaList.append([100,link,None])
        for link in badlinks:
            if(link in links):
                links.remove(link)
        ok = True
        r = sub_client.post_file(mediaList[:25],folderId)
        if(mediaList > 25):
            r = sub_client.post_file(mediaList[25:50],folderId)
            print(r)
        if(mediaList > 50):
            r = sub_client.post_file(mediaList[50:75],folderId)
            print(r)
        if(not ok):
            continue
    except Exception as e:
        print(e)
        try:
            r = sub_client.post_file(mediaList,folderId)
        except Exception as e:
            print(e)

    print(r)
    with open('interaccion/' + d + '/links.txt','w') as h:
        h.write('\n'.join(links) )
