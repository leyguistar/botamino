import os
import amino
from collections import deque
cachesYoutube = {}
userYoutube = {}
chatThreads = {}
users = {}
marcos = []
bienvenidas = []
clients = {}
comidChat = {}
comandosComunidad = {}
bots = {}
defaultClient = amino.Client()
imgdir = 'imgs/'
tipoMensaje = 0
comandosLite = {}
youtubeLists = {}
youtubethreads = [0]
voces = []
chatsSettings = {}
chats = {}
filters = {}
harems = {}
tipoMensajeChat = {}
aliasesChat = []
lastUserCommand = {}
respuestas = {}
comandos = {}
opCustom = {}
adminBot = {}
bannedChats = {}
bannedUsers = {}
sentBooru = {}
bannedUrls = []
rolesComunidad = {}
rolesUser = {}
bannedComunidades = {}
comunidades = {}
sockets = {}
channels = {}
ecchibot = {}
telefonos = {}
waifus = {}
husbandos = {}
allWaifus = {}
lastWaifu = {}
likesWaifu = {}
trashWaifu = {}
waifusChats = {}
cancelarLimpieza = {}
seguirLimpiando = {}
cuentas = {}
fichas = {}
simps = {}
simping = {}
media = {}
fichas[0] = {}
resultadosTelefonos = {}
telefonosInternacionales = {}
resultadosTelefonosInternacional = {}
# VOICE_SERVER_IP = '127.0.0.1'
instanceid = None
# VOICE_SERVER_IP = '172.31.75.178'
VOICE_SERVER_IP = '44.238.148.202'
VOICE_SERVER_PORT = 10105 
NUDE_DETECT_IP = '44.238.148.202'
EDIT_SERVER_IP = '44.238.148.202'
bucket = 'leybot-data'
testBot = 'f20a4e41-ceca-437e-a6e7-a0d0dbc2447d'
confidence = 0.1
chatSugerencias = '7e19a4ce-f2de-45b5-b706-746aacf0e846'
tipos_comandos  = {}
with open('lite/tipos_comandos.txt','r') as h:
	tipos_comandos['base'] = [i.split(' ')[0] for i in h.read().split('\n')]
with open('lite/tipos_comandos.es','r') as h:
	tipos_comandos['es'] = [i.split(' ')[0] for i in h.read().split('\n')]
with open('lite/tipos_comandos.en','r') as h:
	tipos_comandos['en'] = [i.split(' ')[0] for i in h.read().split('\n')]
modos  = {}
with open('lite/modos.es','r') as h:
	modos['es'] = [i.split(' ')[0] for i in h.read().split('\n')]
with open('lite/modos.en','r') as h:
	modos['en'] = [i.split(' ')[0] for i in h.read().split('\n')]
tipos_items = {}
with open('tienda/tipos_items.txt','r') as h:
	tipos_items['base'] = [i.split(' ')[0] for i in h.read().split('\n')]
with open('tienda/tipos_items.es','r') as h:
	tipos_items['es'] = [i.split(' ')[0] for i in h.read().split('\n')]

with open('tienda/tipos_items.en','r') as h:
	tipos_items['en'] = [i.split(' ')[0] for i in h.read().split('\n')]
with open('logros.txt','r') as h:
	data = h.read().split('\n')
logros = ['null']
for l in data:
	l = l[l.find('. ')+2:]
	nombre = l[:l.find(': ')]
	l = l[l.find(': ')+2:]
	descripcion = l[:l.find('. ')+1]
	l = l[l.find('. ')+2:]
	
	puntos = int(l)
	logros.append({"nombre":nombre,"descripcion":descripcion,"puntos":puntos})
# tipos_comandos = ['ayuda','admin','configuracion','diversion','interaccion','utiles','informacion','busqueda','edits','variado','dueño','secreto','ley','chat']
safeMessageType = [57]
ley = 'your_uuid'
leybot = 'd1de419e-f3f9-4aa1-95b0-241ab9938b17'
botgroup = '33240b89-b34f-4485-a123-b4a98503d381'
kirito = 'b8d2f2da-b099-4aa1-b649-6179f7fbbe2d'
shita = 'c4f05d54-62cc-4e2d-8690-706a2c634a4c'
testBot = 'f20a4e41-ceca-437e-a6e7-a0d0dbc2447d'
privadoPruebas = '1fe5b31c-a4fd-4665-9d68-d47c09fcff4a'
comidChat[botgroup] = 76772297
leyworld = 76772297
mensajes = {}
comandosReverseMap = {}
palabrasIdioma = {}

temporadas = {'invierno':'winter','primavera':'spring','verano':'summer','otoño':'fall'}
dias = {'lunes':'monday','martes':'tuesday','miercoles':'wednesday','thursday':'jueves','viernes':'friday','sabado':'saturday','domingo':'sunday'}
tzs = {}
tzs['es'] = ('America/Caracas','America/Buenos_Aires',
'America/Bogota','America/Mexico_City','America/Lima',
'America/Tijuana','America/Santiago','Europe/Madrid')
palabrasjum = ['pene','vagina','culo','trasero','teta','bolas']
tzs['en'] = ('America/Chicago','America/New_York','America/Indiana/Indianapolis','Pacific/Honolulu',
	'America/Indiana/Knox','America/Detroit','America/Denver','America/Los_Angeles','Europe/London')
with open('marcos.txt', 'r') as handler:
    buf = [line.rstrip() for line in handler]
    for i in range(0,len(buf),2):
        marcos.append((buf[i],buf[i+1]))
with open('bienvenidas.txt', 'r') as handler:
    bienvenidas = [line.rstrip() for line in handler]
with open('deviceids.txt','r') as h:
	deviceids = h.read().split('\n')