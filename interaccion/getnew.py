#!/usr/bin/env python3
import os
import requests
import threading
import sys
import ujson as json
def save(name,n,url):
    r = requests.get(url)
    with open('%s/SFW/%d.gif' % (name,n),'wb') as h:
    	h.write(r.content)
    print('guardado',n)
def getGif(name,m,n=1):
	tenorapikey = "23TJ3291LB82"
	r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=50" % (m, tenorapikey))
	link = None
	t = [int(i.replace('.gif','')) for i in os.listdir(name + '/SFW')]
	if(t):
		n = max(t)
	print('n:',n)
	if(r.status_code == 200):
		js = json.loads(r.text)
		for r in js['results']:
			media = r['media'][0]
			url = media['gif']['url']
			print(url)
			t = threading.Thread(target=save,args=(name,n,url))
			t.start()
			n += 1


print('nombre: ',end='',flush=True)
name = input()
try:
	os.mkdir(name)
	os.mkdir(name + '/SFW')
	os.mkdir(name + '/NSFW')
	os.mkdir(name + '/SFWL')
except FileExistsError:
	print('warning los archivos existen')
print('gif search: ',end='',flush=True)
if(len(sys.argv) == 2 ):
	n = int(sys.argv)
n=1
gif = input()
getGif(name,gif,n)
os.system('subl ' + name + '/mensajes1.es ' + name + '/mensajes2.es ')
os.system('subl ' + name + '/mensajes1.en ' + name + '/mensajes2.en ')
os.system('nautilus ' + name + '/SFW')