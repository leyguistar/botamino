#!/usr/bin/env python3
import subprocess

import socket
import gzip
from time import time
from time import sleep
import json
import ssl
from urllib.parse import unquote
from urllib.parse import quote
import os

ip = '104.26.0.100'
port = 443
HOST = 'www3.animeflv.net'
def tmp(type):
    return '/tmp/' + str(time()).replace('.','') + '.' + type

def addHeaders(path):
	with open('animeflvheaders.txt','r') as h:
		headers = h.read() % (path)
		headers = headers.split('\n')
	message = ''
	for h in headers:
		message += h + '\r\n' 
	message += '\r\n'
	return message
def get(path):
	message = addHeaders(path)
	context = ssl.create_default_context()
	s = socket.create_connection((HOST, 443))
	# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s_sock = context.wrap_socket(s, server_hostname=HOST)
	# s_sock.connect((HOST,port))
	s_sock.send(message.encode('utf-8'))
	print(message)
	
	r = b''
	while True:
		data = s_sock.recv(2048)
		r += data
		# print(data,end='')
		print(len(data))
		if ( len(data) < 10 ) :
			break
		# if(len(data) < 2048):
		# 	break
	# print(data)
	s_sock.close()
	body = r[r.find(b'\r\n\r\n')+4:]
	body = body.decode('utf-8')
	with open('anime.html','w') as h:
		h.write(body)

	return body

def buscar(anime):
	html = get('/browse?q=' + quote(anime).replace('%20','+') )
	# with open('anime.html','r') as h:
	# 	html = h.read()
	t = html
	names = {}
	while 1:
		p = t.find('<h3 class="Title">')
		if(p < 0):
			break
		t = t[p+18:]
		f = t.find('</h3>')
		name = t[:f]
		t = t[f+5:]
		p = t.find('<a class="Button Vrnmlk" href="')
		t = t[p+31:]
		f = t.find('">VER ANIME</a>')
		link = t[:f]
		t = t[f+15:]
		names[name] = link
	print(names)
	return names
def getanime(link):

	html = get(link)
	p = html.find('https://mega.nz/')
	if(p < 0):
		print('no encontre link de mega')
		return
	t = html[p:]
	link = t[:t.find('"')]
	ns = 'VPN' + str(time()).replace('.','')
	os.environ["NETNS"] = ns
	vpn = subprocess.Popen(['openvpn-netns', '/etc/openvpn/surfshark/us-mia.prod.surfshark.com_udp.ovpn'])
	# out, err = vpn.communicate()
	# print(out)
	# print(err)
	sleep(5)
	t = tmp('mp4') 
	args = ["ip", "netns", "exec", ns , "megadl", "--path",t, link]
	print(args)
	cmd = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = cmd.communicate()
	print(out)
	print(err)
	print(t)
	vpn.terminate()
	return t		