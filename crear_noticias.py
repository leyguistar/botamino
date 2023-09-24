#!/usr/bin/env python3
import os
import sys
import mysql.connector
from save import Save
from time import time
from time import sleep
import threading
import signal
import datetime
import pytz
from datetime import datetime
s = Save()
print('el nombre la noticia:')
nombre = input()
print('el nombre del archivo de contenido')
n = input()
with open(n,'r') as h:
	text = h.read()
print('tipo de noticia')
tipo = int(input())
s.noticias(nombre,text,tipo,pytz.timezone('America/Caracas').localize(datetime.utcnow()))
