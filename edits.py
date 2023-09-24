import amino
from liteobjs import comidChat,imgdir,clients,bots,mensajes
import requests
import io
from litefuns import send_link,send_imagen,send_message,getNickname,nudeDetect
from litefuns import good_upload,create_sticker,send_sticker,send_text_imagen,send_text_imagen_raw
from PIL import Image, ImageDraw, ImageSequence,ImageFont
import subprocess
import ujson as json
import threading
from time import time,sleep
import random
import socket
from exception import PrintException
from liteobjs import EDIT_SERVER_IP
import os

server = True
def tmp(type):
    return '/tmp/' + str(time()).replace('.','') + '.' + type
def download(url):
    img = requests.get(url).content
    f = tmp(url[url.rfind('.'):])
    with open(f,'wb') as h:
        h.write(img)
    return f
def jail(chatid,userid,client,idioma):
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    info = sub_client.get_user_info(userId=userid)
    r = nudeDetect(info.icon)
    if(r > 0.8):
        send_message(chatid,mensajeid=426)
    else:
        icon = download(info.icon)
        
        data = {
            "comando":"jail",
            "type":"url",
            "file":icon,
            "url":info.icon
        }
        filename = editRequest(data)
        if(not filename):
            editLock.acquire()
            try:
                im1 = Image.open(imgdir + 'carcel2_resize.jpg')
                im2 = Image.open(imgdir + 'jail_bars2.png')
                im3 = Image.open(icon)
                loli = Image.open(imgdir + 'jail_loli.png')
                im1.paste(im3,(150,160))
                final_img = Image.new('RGBA',im1.size,(0,0,0,0))
                final_img.paste(im1,(0,0))
                # final_img.paste(im2,(0,0),mask=im2)
                final_img.paste(loli,(0,0),loli)

                filename = '/tmp/' + str(time()).replace('.','') + '.png'
                final_img.save(filename,format="png")
            except:
                PrintException()
            editLock.release()
        link = good_upload(filename=filename,sanitized=True)
        sub_client.send_message(chatid,fileEmbedImageLink=link, fileEmbedImage=filename,fileEmbedType='image/png',message=random.choice(carcelTexts[idioma]) % (getNickname(userid,sub_client)))
def bikini(chatid,userid,client,idioma):
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    info = sub_client.get_user_info(userId=userid)
    # r = nudeDetect(info.icon)
    # if(r > 0.8):
    #     send_message(chatid,mensajeid=426)
    # else:
    icon = download(info.icon)
    if(True):
        
        # data = {
        #     "comando":"bikini",
        #     "type":"url",
        #     "file":icon,
        #     "url":info.icon
        # }
        # filename = editRequest(data)
        filename = None
        if(not filename):
            editLock.acquire()
            try:
                im1 = Image.open(imgdir + 'bikini_resize.png')
                perfil = Image.open(icon)
                perfil = perfil.resize((120,120))
                final_img = Image.new('RGBA',im1.size,(0,0,0,0))
                final_img.paste(im1,(0,0))
                final_img.paste(perfil,(480,200))

                filename = '/tmp/' + str(time()).replace('.','') + '.png'
                final_img.save(filename,format="png")
            except:
                PrintException()
            editLock.release()
        print(filename)
        link = good_upload(filename=filename,sanitized=True)
        print(link)
        sub_client.send_message(chatid,fileEmbedImageLink=link, fileEmbedImage=filename,fileEmbedType='image/png',message='7u7')

def patear(chatid,userid,client):
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    info = sub_client.get_user_info(userId=userid)
    r = nudeDetect(info.icon)
    if(r > 0.8):
        send_message(chatid,mensajeid=426)
    else:
        icon = download(info.icon)
        data = {
            "comando":"patear",
            "type":"url",
            "file":icon,
            "url":info.icon
        }
        filename = editRequest(data)
        if(not filename):
            editLock.acquire()
            try:
                patada = Image.open(imgdir + 'patada.gif')
                perfil = Image.open(icon)
                # perfil = Image.open('imagenes/perfil.jpg')
                perfil = perfil.resize((80,80))
                # perfil2 = perfil.copy()
                frames = []
                positions = [(232,78),(190,100),(236,90),(57,125),(83,125),(1,185)]
                # positions2 = [(232,78),(201,100),(236,90),(57,125),(83,125),(1,185)]
                i = 0
                p = 0
                for frame in ImageSequence.Iterator(patada):
                    if(i%2):
                        i+=1
                        continue
                    f = Image.new('RGBA',frame.size,(0,0,0,0))
                    f.paste(frame)
                    if(p < len(positions) ):
                        f.paste(perfil,positions[p])
                        p+=1
                    i+=1
                    b = io.BytesIO()
                    f.save(b, format="GIF")
                    f = Image.open(b)
                    frames.append(f)
                # final_img.show()
                b = io.BytesIO()
                # frames[0].save('/tmp/patear.gif', save_all=True, append_images=frames[1:],loop=0,duration=120)
                # return 'gifs/kiri.gif'
                filename = tmp('gif')
                frames[0].save(filename,format="GIF", save_all=True, append_images=frames[1:],loop=0)
                # frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:],loop=0)
            except:
                PrintException()
            editLock.release()
        send_imagen(chatid,filename,sanitized=True)
def killMinecraft(score,level):
    data = {
        "comando":"killMinecraft",
        "score":score,
        "level":level
    }
    filename = editRequest(data)
    if(not filename):
        editLock.acquire()
        try:
            img = Image.open(imgdir + 'minecraft_death_score.png')
            d = ImageDraw.Draw(img)
            font = ImageFont.truetype('fonts/MinecraftRegular.otf',20)
            d.text((442,200),str(score),(63,63,21), font=font,align ="center")
            d.text((440,198),str(score),(255,255,85), font=font,align ="center")

            level = str(level)
            if(len(level) == 1):
                d.text((424,409),str(level),(0x47,0x18,0x18), font=font,align ="center")
                d.text((422,407),str(level),(0x7c,0x81,0x25), font=font,align ="center")
            else:
                d.text((414,409),str(level),(0x47,0x18,0x18), font=font,align ="center")
                d.text((412,407),str(level),(0x7c,0x81,0x25), font=font,align ="center")        
            filename = tmp('png')
            img.save(filename,format="png")
        except:
            PrintException()
        editLock.release()

    return filename

def killUser(chatid,userid,client):
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    info = sub_client.get_user_info(userId=userid)
    filename = killMinecraft(info.json['reputation'],info.json['level'])
    sub_client.send_message(chatid,message=getNickname(userid,sub_client) + " fell out of the world",fileEmbedImage=filename)
def getFaces(filename):
    if(filename.startswith('http')):
        name = download(filename)
    elif(not filename.startswith('/tmp')):
        name = '/tmp/' + filename[filename.rfind('/')+1:]
        with open(filename,'rb') as f1:
            with open('/tmp/' + name,'wb') as f2:
                f2.write(f1.read()) 
    else:
        name = filename
    try:
        faceLock.acquire()
        args = ["/anime-face-detector/detectFaces.py", name]
        print(args)
        cmd = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = cmd.communicate()
        print(out)
        faces = json.loads(out.decode('utf-8'))
    except:
        faces = []
    faceLock.release()
    return faces


def cum(chatid,mediaValue,client,ecchi=False):
    r = nudeDetect(mediaValue)
    if(r > 0.8):
        send_message(chatid,mensajeid=426,ecchi=ecchi)
    else:
        data = {
            "comando":"cum",
            "type":"url",
            "url":mediaValue
        }
        filename = editRequest(data)
        if(not filename):
            img = download(mediaValue)
            editLock.acquire()
            try:
                cum = Image.open(imgdir + 'cum.gif')
                perfil = Image.open(img)
                frames = []
                for frame in ImageSequence.Iterator(cum):
                    f = Image.new('RGBA',perfil.size,(0,0,0,0))
                    f.paste(perfil)
                    fr = frame.convert("RGBA").resize(perfil.size)
                    f.paste(fr,(0,0),fr)
                    b = io.BytesIO()
                    f.save(b, format="GIF")
                    f = Image.open(b)
                    frames.append(f)
                filename = tmp('gif')
                frames[0].save(filename,format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=80)
            except:
                PrintException()
            editLock.release()
        send_imagen(chatid,filename,sanitized=True,ecchi=ecchi)
def arcoiris(chatid,mediaValue,client,ecchi=False):
    file = download(mediaValue)
    img = Image.open(file)
    x,y = img.size
    if(x > y):
        gifimg = 'arcoiris.gif'
    elif(x < y):
        gifimg = 'arcoiris2.gif'
    else:
        gifimg = 'arcoiris3.gif'
    gifimg = imgdir + gifimg
    return applyGif(chatid,gifimg,mediaValue=mediaValue,client=client,ecchi=ecchi,alpha=100,duration=100,file=file)
def fiesta(chatid,mediaValue,client,ecchi=False):
    gifimg = imgdir + 'colores.gif'
    file = download(mediaValue)
    return applyGif(chatid,gifimg,mediaValue=mediaValue,client=client,ecchi=ecchi,alpha=100,duration=100,file=file)


def applyGif(chatid,gifimg,mediaValue=None,client=None,ecchi=False,alpha=0,duration=0,file=None):
    if(file):
        with open(file,'rb') as h:
            data = h.read()
        r = nudeDetect(data=data,ext=file[file.rfind('.'):])
    else:
        r = nudeDetect(mediaValue)
    if(r > 0.8):
        send_message(chatid,mensajeid=426,ecchi=ecchi)
    else:
        if(not file):
            img = download(mediaValue)
        else:
            img = file
        data = {
            "comando":"applygif",
            "type":"url",
            "url":mediaValue,
            "file":img,
            "gifimg":gifimg,
            "alpha":alpha,
            "duration":duration
        }
        filename = editRequest(data)
        if(not filename):
            editLock.acquire()
            try:
                cum = Image.open(gifimg)
                perfil = Image.open(img)
                frames = []
                for frame in ImageSequence.Iterator(cum):
                    f = Image.new('RGBA',perfil.size,(0,0,0,0))
                    f.paste(perfil)
                    fr = frame.convert("RGBA").resize(perfil.size)
                    if(alpha):
                        fr.putalpha(alpha)
                    f.paste(fr,(0,0),fr)
                    b = io.BytesIO()
                    f.save(b, format="GIF")
                    f = Image.open(b)
                    frames.append(f)
                filename = tmp('gif')
                frames[0].save(filename,format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=duration)
            except:
                PrintException()
            editLock.release()
        print(filename)
        send_imagen(chatid,filename,sanitized=True,ecchi=ecchi)

def gorrito(chatid,ori,gorrito,faces,client):
    client = clients[chatid]
    f = Image.new('RGBA',ori.size,(0,0,0,0))
    f.paste(ori)
    i = 0
    si = False
    if(not faces):
        send_message(chatid,'no pude encontrar ningun rostro anime')
        return None
    for face in faces:
        x, y, x2, y2 = face['bbox']
        w = x2 - x
        h = y2 - y
        if(face['score'] < 0.1):
            i+=1
            continue
        i+=1
        resized = gorrito.resize((int(w*1.5) ,int(h*1.1)) )
        print(resized.size)
        print(ori.size)
        print(x,y,w,h)
        f.paste(resized,(int(x)-int(w*0.01),int(y)-int(resized.size[1]*0.94)+int(h/3) ),resized)
        si = True

    if(not si):
        send_message(chatid,'no pude encontrar ningun rostro anime')
        return    
    b = io.BytesIO()    
    f.save(b,format="png")
    # try:
    #     link = client.upload_media(data=b.getvalue())
    #     print(link)
    #     send_link(chatid,link,sanitized=True)
    # except:
    t = tmp('png')
    f.save(t,format="png")
    # send_imagen(chatid,t)
    send_text_imagen(chatid,'Aqui tienes tu gorrito uwu',filename=t)
    return f
def pilImage(name):
    if(type(name) == str):
        if(name.startswith('http')):
            img = requests.get(name).content
            img = Image.open(io.BytesIO(img))
        else:
            img = Image.open(name)
    elif(type(name) == bytes):        
        img = Image.open(io.BytesIO(img))
    else:
        img = Image.open(name)
    return img
def square(img):
    width, height = img.size
    if height < width:
        # make square by cutting off equal amounts left and right
        left = (width - height) / 2
        right = (width + height) / 2
        top = 0
        bottom = height
        img = img.crop((left, top, right, bottom))

    elif width < height:
        # make square by cutting off bottom
        left = 0
        right = width
        top = 0
        bottom = width
        img = img.crop((left, top, right, bottom))
    return img
def crearLicencia(l,name,icon,creatorName,creatorIcon):
    botimg = Image.open(creatorIcon)
    img = Image.open(icon)
    print('todo listo') #207 79 365 243
    im1 = Image.open(imgdir + 'licencia2.png')
    final_img = Image.new('RGBA',im1.size,(0,0,0,0))
    final_img.paste(im1,(0,0))
    
    font = ImageFont.truetype('fonts/DejaVuSansCondensed.ttf',60)
    if(len(l) > 32):
        l = l[:39]
        font2 = ImageFont.truetype('fonts/DejaVuSansCondensed.ttf',97-(len(l)-32)*4)
    else:
        font2 = ImageFont.truetype('fonts/DejaVuSansCondensed.ttf',100)
        l = l[:32]
    if(len(l) < 30):
        font2 = ImageFont.truetype('fonts/DejaVuSansCondensed.ttf',100)

    font3 = ImageFont.truetype('fonts/DejaVuSansCondensed.ttf',32)
    img = square(img)

    img = img.resize((632,656))
    d = ImageDraw.Draw(final_img)
    name = name[:21]
    r = d.textbbox((100,360),name, font=font,align ="center") #125 430
    w = r[2] - r[0]
    d.text((406-w//2,360),name,(0x00,0x00,0x00), font=font,align ="center")
    r = d.textbbox((92,995),l, font=font2,align ="center")
    w = r[2] - r[0]
    d.text((794-w//2,995),l,(0xFF,0xFF,0xFF), font=font2,align ="center")

    final_img.paste(img,(828,316)) #1825 1215
    botimg = square(botimg)
    botimg = botimg.resize((152,152))

    final_img.paste(botimg,(668,752)) #1825 1215
    t = 'autorizado\npor\n%s' % (creatorName)
    r = d.textbbox((560,752),t, font=font3,align ="right")
    w = r[2] - r[0]
    d.text((656-w,752),t,(0x00,0x00,0x00), font=font3,align ="right")
    final_img = final_img.rotate(10,Image.NEAREST)

    b1 = io.BytesIO()
    f1 = tmp('png')
    final_img.save(f1,format="png")
    
    m = max(final_img.size)
    x,y = final_img.size
    r = 1000/m
    final_img = final_img.resize((int(x*r),int(r*y) ) )
    b2 = io.BytesIO()
    f2 = tmp('png')

    final_img.save(f2,format="png")

    return f1,f2

def licencia(chatid,userid,l,creatorId=None,idioma='es'):
    client = clients[chatid]
    sub_client = amino.SubClient(client=client,comId=comidChat[chatid])
    info = sub_client.get_user_info(userId=userid,raw=True)['userProfile']
    name = info['nickname']
    icon = info['icon']
    if(not creatorId):
        creatorName = bots[client.profile.id]['name']
        creatorId = client.profile.id
        info = sub_client.get_user_info(userId=creatorId,raw=True)['userProfile']
    else:
        info = sub_client.get_user_info(userId=creatorId,raw=True)['userProfile']
        creatorName = info['nickname']  
    creatorIconUrl = info['icon']  
    botimg = download(info['icon'])
    iconUrl = icon
    # print(json.dumps(info))
    r = nudeDetect(iconUrl)
    if(r > 0.8):
        send_message(chatid,mensajeid=426)
    else:
        icon = download(icon)
        data = {
            "comando":"licencia",
            "type":"url",
            "text":l,
            "name":name,
            "icon":icon,
            "iconUrl":iconUrl,
            "creatorIconUrl":creatorIconUrl,
            "creatorName":creatorName,
            "creatorIcon":botimg
        }
        result = editRequest(data)
        if(not result):
            editLock.acquire()
            try:
                filename1,filename2 = crearLicencia(l,name,icon,creatorName,botimg)
            except:
                PrintException()
            editLock.release()

        else:
            filename1 = result[0]
            filename2 = result[1]
        link = good_upload(filename=filename1,sanitized=True)
        t = mensajes[idioma][686]
        send_text_imagen_raw(chatid,t,url=link,filename=filename2)


def writeWikipedia(chatid,title,content,client):
    data = {
        "comando":"wikipedia",
        "type":"url",
        "title":title,
        "content":content
    }
    filename = editRequest(data)
    if(not filename):
        editLock.acquire()
        try:
            img = Image.open(imgdir + 'wikipedia.png')
            d = ImageDraw.Draw(img)
            font = ImageFont.truetype('fonts/wikipedia/LinLibertine_DR.ttf',100)
            d.text((44,410),title,(0x18,0x19,0x1a),font=font,align ="left")
            lines = []
            for line in content.split('\n'):
                i = 0
                o = 0
                while(i < len(line)):
                    i+=45
                    dr = 0
                    dl = 0
                    while (i+dr < len(line)):
                        if(line[i+dr].isspace()):
                            break
                        dr+=1
                    while (i-dl < len(line)):
                        if(line[i-dl].isspace()):
                            break
                        dl+=1
                    if(dr < dl):
                        i+=dr
                    else:
                        i -= dl         
                    lines.append(line[o:i].strip())
                    o = i
            content = '\n'.join(lines)
            font = ImageFont.truetype('fonts/wikipedia/LinLibertine_DR.ttf',50)
            d.text((44,696),content,(0x18,0x19,0x1a),font=font,align ="left")
            r = d.textbbox((44,696),content,font=font,align ="left")
            img2 = Image.open(imgdir + 'wiki_bottom.png')
            img3 = Image.open(imgdir + 'phone_bottom.png')
            img.paste(img2,(0,r[3]+20))
            img.paste(img3,(0,img.size[1]-img3.size[1]))
            filename = tmp('png')
            img.save(filename,format="png")
        except:
            PrintException()
        editLock.release()
    send_imagen(chatid,filename,sanitized=True)

def bienvenidaGif(chatid,mensaje):
    data = {
        "comando":"gif8bits",
        "text":mensaje
    }
    filename = editRequest(data)
    if(not filename):
        editLock.acquire()
        try:
            b = Image.open('imgs/bienvenida_retro.png')
            frames = []
            font1 = ImageFont.truetype('fonts/MinecraftBold.otf',30)
            font2 = ImageFont.truetype('fonts/MinecraftBold.otf',28)
            x = 50
            y = 36
            last = b
            duration = 0
            f = Image.new('RGBA',b.size,(0,0,0,0))
            f.paste(last)
                    
            frames.append(f)
            for l in mensaje:
                if(l.isspace() and x == 50):
                    continue
                if(l == '\n'):
                    x = 50
                    y += 36
                elif(l == ' '):
                    x += 20
                    if(x > 460):
                        x = 50
                        y += 36

                else:
                    f = Image.new('RGBA',b.size,(0,0,0,0))
                    f.paste(last)
                    d = ImageDraw.Draw(f)
                    r = d.textbbox((x,y),str(l), font=font1,align ="center")

                    d.text((x,y),str(l),(0x3c,0x2a,0x48), font=font1,align ="center")
                    d.text((x,y),str(l),(0xed,0xe0,0xb7), font=font2,align ="center")
                    x += r[2]-r[0]
                    if(x > 460):
                        x = 50
                        y += 36

                    bi = io.BytesIO()
                    f.save(bi, format="GIF")
                    f = Image.open(bi)
                    last = f
                    frames.append(f)
                duration += 1
                if(y > 154):
                    break
            frames.append(last)
            frames.append(last)
            frames.append(last)
            frames.append(last)
            frames.append(last)
            duration = 100
            filename = tmp('gif')
            frames[0].save(filename,format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=duration)
        except:
            PrintException()
        editLock.release()
    client = clients[chatid]

    stickerid = create_sticker(client,file=filename)
    send_sticker(chatid,stickerid)
    # frames[0].save('/tmp/bienvenida.gif',format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=duration)
editServerStartedTime = 0
EDIT_ACTUAL_IP = EDIT_SERVER_IP
def editRequest(data):
    global editServerStartedTime,EDIT_ACTUAL_IP
    TCP_IP = EDIT_ACTUAL_IP
    TCP_PORT = 10005
    url = None
    filename = None
    s = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) # UDP

    s.settimeout(3)
    try:
        print((TCP_IP, TCP_PORT))
        s.connect((TCP_IP, TCP_PORT))
    except (ConnectionRefusedError,socket.timeout) as e :
        if(EDIT_ACTUAL_IP != '127.0.0.1'):
            s = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_STREAM) # UDP
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(1)
            TCP_IP = '127.0.0.1'
            try:
                print((TCP_IP, TCP_PORT))
                s.connect((TCP_IP, TCP_PORT))
            except (ConnectionRefusedError,socket.timeout) as e:
                if(time () > editServerStartedTime + 300):
                    print('systemctl start editserver.service')
                    os.system('systemctl start editserver.service')
                    editServerStartedTime = time()
                    sleep(2)
                    s = socket.socket(socket.AF_INET, # Internet
                                         socket.SOCK_STREAM) # UDP
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.settimeout(1)

                    try:
                        s.connect((TCP_IP, TCP_PORT))
                    except (ConnectionRefusedError,socket.timeout) as e:
                        return None
                    else:
                        EDIT_ACTUAL_IP = TCP_IP
                else:
                    return None
            else:
                EDIT_ACTUAL_IP = TCP_IP
        else:
            return None
    s.settimeout(None)
    s.send(json.dumps(data).encode('utf-8'))
    print(json.dumps(data).encode('utf-8'))
    files = []
    r = s.recv(1)
    result = r[0]
    for i in range(result):
        r = s.recv(4)
        size = int.from_bytes(r,'big')
        data = b''
        while len(data) < size:
            data += s.recv(size-len(data))
        magic = data[:4]
        if(magic == b'\xFF\xD8\xFF\xDB'):
            t = 'jpg'
        elif(magic == b'\x89\x50\x4E\x47'):
            t = 'png'
        elif(magic == b'\x47\x49\x46\x38'):
            t = 'gif'
        file = tmp(t)
        with open(file,'wb') as h:
            h.write(data)
        files.append(file)
    s.close()
    if(len(files) == 1):
        return files[0]
    else:
        return files[0],files[1]


faceLock = threading.Lock()
carcelTexts = {}
with open('carcel/carcel.es','r') as h:
    carcelTexts['es'] = h.read().split('\n')
with open('carcel/carcel.en','r') as h:
    carcelTexts['en'] = h.read().split('\n')
editsCount = 0
maxedits = 3
editLock = threading.Lock()