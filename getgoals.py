#!/usr/bin/env python3
import requests
import os
from PIL import Image
with open('goals.txt','r') as h:
	goals = h.read().split('\n')
try:
	os.mkdir('goals')
except:
	pass
try:
	os.mkdir('goals/original')
except:
	pass
try:
	os.mkdir('goals/png')
except:
	pass
for g in goals:
	if(not g):
		continue
	if(os.path.exists("goals/png/" + g + '.png')):
		continue
	p = g.rfind('.')
	ext = g[p:]
	id = g[g.find('_')+1:p]
	print(id,ext)
	r = requests.get('https://data.whicdn.com/images/%s/original%s' % (id,ext))
	with open('goals/original/' + g,'wb') as h:
		h.write(r.content)
	img = Image.open('goals/original/' + g)
	m = max(img.size)
	x,y = img.size
	r = 1000/m
	img = img.resize((int(x*r),int(r*y) ) )
	filename = "goals/png/" + g + '.png'
	img.save(filename,format="PNG")
	# with open('goals/url/','w') as h:
	# 	h.write()
