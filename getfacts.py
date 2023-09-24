#!/usr/bin/env python3
import requests
from time import sleep
from googletrans import Translator
translator = Translator()

with open('facts/facts.en','r') as h:
	facts = h.read().split('\n')
translated = []
for f in facts:
	traduccion = translator.translate(f,dest='es')
	translated.append(traduccion.text)
	print(traduccion.text)
with open('facts/facts.es','w') as h:
	h.write('\n'.join(translated) )
