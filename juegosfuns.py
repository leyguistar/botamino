import amino
from save import Save
import ujson as json
import random
from time import time
from exception import PrintException
import requests
from PIL import Image
import threading
from channel import Channel
from channel import waitForChannel
from time import sleep
import os
class Juego:
    def __init__(self,juego,chatid,comid,jugadores,botid,client,admins,on_close):
        self.juego = juego
        self.chatid = chatid
        self.comid = comid
        self.jugadores = jugadores
        self.botid = botid
        self.client = client
        self.admins = admins
        self.limite = 0
        self.lock = threading.Lock()

        self.lastActive = time()
        self.iniciado = False
        self.on_close = on_close
    def add(self,userid,nickname):
        if(userid not in self.jugadores):
            self.jugadores.append(userid)
            send_message(self.chatid,'%s se ha unido al juego' % nickname)

def getNickname(userid):
	return nicknames.get(userid,'')
def send_message(chatid,message,):
    juego = jugando.get(chatid)
    if(not juego):
        return
    sub_client = juego.client.sub_client(juego.comid)
    message = '[c]' + message.replace('\n','\n[c]')
    r = sub_client.send_message(chatid,message)
    if(r != 200):
        print(r)
def send_marco(chatid,mensaje):
	m = marcos[0] + '\n\n' + mensaje + '\n\n' + marcos[1]
	send_message(chatid,m)	
def send_imagen(chatid,link=None,file=None):
    juego = jugando[chatid]
    sub_client = juego.client.sub_client(juego.comid)
    for i in range(5):
        if(link!=None):
            r = sub_client.send_message(chatId=chatid,link=link)
        else:
            r = sub_client.send_message(chatId=chatid,filePath=file)
        if(r == 200):
            break
def set_channel_info(data,userid):
    data = data['o']
    chatid = data['threadId']
    comid = data['ndcId']
    print('recibida informacion de channel')
    print(data)
    if('exception' in data):
        return False
    print(data)
    name = data['channelName']
    token = data['channelKey']
    uid = data['channelUid']
    print('registrando channel')
    print(name,token,uid)
    t = 1
    channels[chatid] = Channel(chatid,name,token,uid,t,userid,volume=100)
    return channels[chatid] 

def get_channel_info(socket,chatid,comid):
    id = str(int(time()*100)%1000000)
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":id
        },
        "t":200
    }
    d = json.dumps(data)
    e = threading.Event()
    data = {}
    e = threading.Event()
    events = {
        201:(e,data)
    }
    socket.setEvent(id,events)
    socket.send(d.encode('utf-8'))
    e.wait(5)
    if(e.is_set()):
        data = data['data']
        channel = set_channel_info(data,socket.userid)
        return channel
    else:
        return False

def detect_or_join_channel(socket,chatid,comid):
    id = str(int(time()*100)%1000000)
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":id
        },
        "t":100
    }
    d = json.dumps(data)
    e = threading.Event()
    data = {}
    e = threading.Event()
    events = {
        101:(e,data)
    }
    
    socket.setEvent(id,events)
    socket.send(d.encode('utf-8'))
    e.wait(5)
    userid = socket.userid
    if(e.is_set()):
        data = data['data']
        userList = data['o']['userList']
        if(not userList):
            return False
        elif(userid in userList):
            return get_channel_info(socket,chatid,comid)
        else:
            join_voice_chat(socket,chatid,comid,1)
            return get_channel_info(socket,chatid,comid)
def join_voice_chat(socket,chatid,comid,joinRole):
    id = str(int(time()*100)%1000000)
    data = {
        "o":{
            "ndcId":comid,
            "threadId":chatid,
            "id":id,
            "joinRole":joinRole
        },
        "t":112
    }
    d = json.dumps(data)
    socket.send(d.encode('utf-8'))

def sendAudioRequest(channel,playid,type,text,idioma,s=None):
    saver = s
    if(not s):
        saver = Save()
    name = channel.name
    token = channel.token
    uid = channel.uid
    type = channel.type
    botid = channel.botid
    volume = channel.volume
    chatid = channel.chatid
    print(chatid,channel,token,uid,type,volume,botid)
    while 1:
        try:
            actives = saver.getActivePlayers()
        except Exception as e:
            PrintException()
            sleep(2)
        else:
            break
    if(not actives):
        return False
    saver.setChannelInfo(chatid,name,token,uid,type,volume,botid)
    count = len(saver.loadQueue(channel.chatid))
    if(count > 0):
        saver.close()
        return False
    saver.addAudioRequest(chatid,playid,2,text,idioma)
    saver.close()
    return True

def send_audio_thread(chatid,file,onlyLive=False):
    juego = jugando[chatid]
    sub_client = juego.client.sub_client(juego.comid)
    channel = detect_or_join_channel(sockets[juego.botid],chatid,juego.comid)
    if(channel):
        sendAudioRequest(channel,file,2,'audio','es')
        return
    elif(not onlyLive):
        if(file.startswith('http')):
            path = '/tmp/' + file[file.rfind('/')+1:]
            if(not os.path.exists(path)):
                c = requests.get(file).content
                with open(path, 'wb') as h:
                    h.write(c)
        else:
            path = file
        for i in range(3):
            r = sub_client.send_message(chatId=chatid,filePath=path)
            if(r == 200):
                break
        return r

def send_audio(chatid,file,onlyLive=False,esperar=False):
    if(esperar):
        return send_audio_thread(chatid,file,onlyLive)
    else:
        t = threading.Thread(target=send_audio_thread,args=(chatid,file,onlyLive))
        t.start()


def send_text_imagen(chatid,message,url=None,filename=None):
    juego = jugando[chatid]
    sub_client = juego.client.sub_client(juego.comid)
    client = juego.client
    if(not filename):
        filename = '/tmp/' + url[url.rfind('/')+1:]
        response = requests.get(url)
        if(response.status_code != 200):
            return False
        data = response.content
        with open(filename,'wb') as h:
            h.write(data)
    if(not url):
        url = client.upload_media(f=filename)
    img = Image.open(filename)
    m = max(img.size)
    x,y = img.size
    r = 1000/m
    img = img.resize((int(x*r),int(r*y) ) )
    filename = "/tmp/" + filename[filename.rfind('/')+1:] + '.png'
    img.save(filename,format="PNG")
    message = '[c]' + message.replace('\n','\n[c]')
    r = sub_client.send_message(chatid,fileEmbedImage=filename,fileEmbedType='image/png',message=message,fileEmbedImageLink=url,withResponse=True)
    # print(r)
    if(r['api:statuscode'] != 0):
        return False
    return True
def relogin(client,secret,device_id):
    while 1:
        sleep(28800)
        client.login(secret=secret,device_id=device_id)

def login(userid=None,client=None,save=None,alias=None):
    if(not save):
        s = Save(expected=True)
    else:
        s = save
    try:
        if(not client):
            client = amino.Client()
        if(userid):
            login = s.loginInfo(id=userid,dictionary=True)
        elif(alias):
            login = s.loginInfo(alias=alias,dictionary=True)
            userid = login['id']
        else:
            if(s != save):
                s.close()
                del s
            return None
        device_id = random.choice(deviceids)

        if(login['jsonResponse'] and login['lastLogin']+28800 > time()):
            print('inicio cache')
            secret = json.loads(login['jsonResponse'])['secret']
            client.login_cache(login['jsonResponse'])
            # client.login(secret=secret )
            # s.newSecret(userid,secret)
        elif(login['secret']  ):
            print('iniciando secret')
            r = client.login(secret=login['secret'],get=True,error=True,device_id=device_id)
            r1 = json.loads(r[1])
            secret = login['secret']
            r1['userProfile']['content'] = 'cache'
            r1['secret'] = secret
            r1 = json.dumps(r1)
            s.newLogin(id=client.profile.id,jsonResponse=r1)

        else:
            print('iniciando normal')
            r = client.login(email=login['email'],password=login['password'],get=True,error=True)

            if(type(r) == dict or r[0] != 200):
                print(userid)
                print(r)
                if(s != save):
                    s.close()
                    del s

                return None
            r1 = json.loads(r[1])
            r1['userProfile']['content'] = 'cache'
            secret = r1['secret']

            r1 = json.dumps(r1)
            s.newLogin(id=client.profile.id,jsonResponse=r1)
            s.newSecret(id=client.profile.id,secret=secret)
    except:
        PrintException()
    if(s != save):
        s.close()
        del s
    t = threading.Thread(target=relogin,args=(client,secret,device_id))
    return client
with open('deviceids.txt','r') as h:
	deviceids = h.read().split('\n')
nicknames = {}
jugando = {}
sockets = {}
clients = {}
channels = {}
marcos = ['╭╊━━╾❋╼━━╉╮','╰╊━━╾❋╼━━╉╯']
juegosApa = ['aa2','aa3','aa4','apa','apa2','pelis','pelis2']