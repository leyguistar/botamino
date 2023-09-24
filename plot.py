#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from time import time
import os
def plotActividad(chat=False,nombre='logs/actividad.png'):
	mensajes = []
	chats = []
	if(os.path.exists(nombre) and time() < os.path.getmtime(nombre) + 60):
		return nombre
	with open('logs/actividad.log','r') as h:
		lines = h.read().split('\n')
	t = time()-3600
	for line in lines:
		if(line):
			i = line.split(' ')
			if(int(i[0]) < t):
				continue
			mensajes.append(int(i[1]) )
			if(chat):
				chats.append(int(i[2]) )
	x = np.array(list(range(1,len(mensajes)+1 )))
	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	if(chat):
		ax.plot(x, np.array(chats), label="chats")
	ax.plot(x, np.array(mensajes), label="mensajes")
	ax.set_title("actividad ultima hora")
	ax.legend()
	fig.savefig('logs/actividad.png',bbox_inches='tight')
	return 'logs/actividad.png'
