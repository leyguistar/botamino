#!/usr/bin/env python3
import sys
import os
sys.stdout = open('/editserver.log','w')
sys.stderr = open('/editserver.err','w')
print('comenzado')
sys.stdout.flush()
sys.stderr.flush()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath )
os.chdir(dname)
print('directory: ' +  dname)

import socket
from PIL import Image, ImageDraw, ImageSequence,ImageFont
from time import time,sleep
import os
import threading

try:
	from exception import PrintException
except Exception as e:
	print(e)
sys.stdout.flush()
sys.stderr.flush()
import ujson as json
import io
import requests
import base64
print('pasados los import')
sys.stdout.flush()
sys.stderr.flush()

imgdir = 'imgs/'
def tmp(type):
    return '/tmp/' + str(time()).replace('.','') + '.' + type
def download(url,save=False):
    print(url)
    for i in range(5):
        response = requests.get(url)
        if(response.status_code == 200):
            break
    else:
        return None
    if(not save):
        return io.BytesIO(response.content)

    f = tmp(url[url.rfind('.')+1:])
    with open(f,'wb') as h:
        h.write(response.content)
    return f

def jail(icon):
    try:
        im3 = Image.open(icon)
        im1 = Image.open(imgdir + 'carcel2_resize.jpg')
        im2 = Image.open(imgdir + 'jail_bars2.png')
        loli = Image.open(imgdir + 'jail_loli.png')
        im1.paste(im3,(150,160))
        final_img = Image.new('RGBA',im1.size,(0,0,0,0))
        final_img.paste(im1,(0,0))
        final_img.paste(loli,(0,0),loli)
        b = io.BytesIO()
        final_img.save(b,format="png")
        return b
    except:
        PrintException()
    return None
def patear(icon):
    perfil = Image.open(icon)
    patada = Image.open(imgdir + 'patada.gif')
    perfil = square(perfil)
    perfil = perfil.resize((80,80))
    frames = []
    positions = [(232,78),(190,100),(236,90),(57,125),(83,125),(1,185)]
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

    b = io.BytesIO()
    frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:],loop=0)
    return b
def killMinecraft(score,level):
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
    b = io.BytesIO()
    img.save(b,format="png")    
    return b
def cum(img):
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
    b = io.BytesIO()
    frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=80)
    return b
def applygif(file,img,alpha=0,duration=0):
    cum = Image.open(file)
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
    b = io.BytesIO()
    frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=duration)
    return b
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

def licencia(l,name,icon,creatorName,creatorIcon):
    botimg = Image.open(creatorIcon)
    img = Image.open(icon)
    print('todo listo') #207 79 365 243
    print('comenzando licencia')
    sys.stdout.flush()
    try:
        im1 = Image.open(imgdir + 'licencia2.png')
        final_img = Image.new('RGBA',im1.size,(0,0,0,0))
        final_img.paste(im1,(0,0))
    except Exception as e:
        print('error ' + str(e))
        sys.stdout.flush()

    print(1)
    sys.stdout.flush()
    
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
    print(2)
    sys.stdout.flush()

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
    print(3)
    sys.stdout.flush()

    final_img.paste(botimg,(668,752)) #1825 1215
    t = 'autorizado\npor\n%s' % (creatorName)
    r = d.textbbox((560,752),t, font=font3,align ="right")
    w = r[2] - r[0]
    d.text((656-w,752),t,(0x00,0x00,0x00), font=font3,align ="right")
    final_img = final_img.rotate(10,Image.NEAREST)

    b1 = io.BytesIO()
    print(4)
    sys.stdout.flush()

    final_img.save(b1,format="png")
    
    m = max(final_img.size)
    x,y = final_img.size
    r = 1000/m
    final_img = final_img.resize((int(x*r),int(r*y) ) )
    b2 = io.BytesIO()
    print(5)
    sys.stdout.flush()

    final_img.save(b2,format="png")
    print(6)
    sys.stdout.flush()

    return b1,b2

def writeWikipedia(title,content):
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
    b = io.BytesIO()
    img.save(b,format="png")
    return b
def gif8bits(mensaje):
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

    b = io.BytesIO()
    duration = 100

    frames[0].save(b,format="GIF", save_all=True, append_images=frames[1:],loop=0,duration=duration)
    return b

def convert(filename):
    img = Image.open(filename)
    m = max(img.size)
    x,y = img.size
    r = 1000/m
    img = img.resize((int(x*r),int(r*y) ) )
    b = io.BytesIO()
    img.save(b,format="PNG")
    return b

def checkMessage(conn):
    try:
        data = conn.recv(1024).decode('utf-8')
        if(not len(data)):
            return
        print('llego request',data)
        js = json.loads(data)
        sys.stdout.flush()
        comando = js['comando']
        if(comando == 'jail'):
            t = js['type']
            if(t == 'url'):
                file = download(js['url'])
            else:
                file = js['file']

            b = jail(file)

            r =  b.getvalue()
            r = b"\x01" + len(r).to_bytes(4,'big') + r
            conn.send(r)
            # conn.send(('{"result":"ok","size":"%s"}' % (len(r)) ).encode('utf-8') + r)
        elif(comando == 'patear'):
            t = js['type']
            if(t == 'url'):
                file = download(js['url'])
            else:
                file = js['file']
            b = patear(file)
            r = b.getvalue()            
            r = b"\x01" + len(r).to_bytes(4,'big') + r
            conn.send(r)

        elif(comando == 'convert'):
            t = js['type']
            if(t == 'url'):
                file = download(js['url'])
            else:
                file = js['file']
            b = convert(file)
            r = b.getvalue()            
            r = b"\x01" + len(r).to_bytes(4,'big') + r
            conn.send(r)

        elif(comando == 'killMinecraft'):
            score = js['score']
            level = js['level']
            b = killMinecraft(score,level)
            r = b.getvalue()            
            r = b"\x01" + len(r).to_bytes(4,'big') + r
            conn.send(r)
        elif(comando == 'cum'):
            t = js['type']
            if(t == 'url'):
                file = download(js['url'])
                delete = True
            else:
                file = js['file']
            b = cum(file)
            r = b.getvalue()
            r = b"\x01" + len(r).to_bytes(4,'big') + r
            conn.send(r)
        elif(comando == 'licencia'):
            l = js['text']
            name = js['name']
            creatorName = js['creatorName']
            icon = js['icon']
            creatorIcon = js['creatorIcon']
            icon = download(js['iconUrl'])
            creatorIcon = download(js['creatorIconUrl'])
            print('haciendo licencia')
            sys.stdout.flush()
            b1,b2 = licencia(l,name,icon,creatorName,creatorIcon)
            print('enviando resultados de licencia',len(b1.getvalue()),len(b2.getvalue()))

            sys.stdout.flush()
            r1 = b1.getvalue()           
            r2 = b2.getvalue()            
            r = b"\x02" + len(r1).to_bytes(4,'big') + r1 + len(r2).to_bytes(4,'big') + r2
            conn.send(r)
        elif(comando == 'wikipedia'):
            title = js['title']
            content = js['content']
            b = writeWikipedia(title,content)
            r = b.getvalue()
            r = b"\x01" + len(r).to_bytes(4,'big') + r
            conn.send(r)
        elif(comando == 'gif8bits'):
            text = js['text']
            b = gif8bits(text)
            r = b.getvalue()            
            r = b"\x01" + len(r).to_bytes(4,'big') + r
            conn.send(r)
        elif(comando == 'applygif'):
            t = js['type']
            if(t == 'url'):
                file = download(js['url'])
            else:
                file = js['file']
            f = js['gifimg']
            alpha = js['alpha']
            duration = js['duration']
            print(js)
            b = applygif(f,file,alpha,duration)
            r = b.getvalue()       
            r = b"\x01" + len(r).to_bytes(4,'big') + r
            conn.send(r)

        else:
            print('comando desconocido')
        print('todo enviado')
    except Exception as e:
        PrintException()
def request():
    TCP_IP = '0.0.0.0'
    TCP_PORT = 10005
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while 1:
        try:
            s.bind((TCP_IP, TCP_PORT))
        except:
            sleep(1)
        else:
            break
    s.listen(10)
    print('en espera de requests',TCP_IP,TCP_PORT)
    sys.stdout.flush()
    sys.stderr.flush()
    while 1:
        try:
            conn, addr = s.accept()
            t = threading.Thread(target=checkMessage,args=(conn,))
            t.start()
        except KeyboardInterrupt:
            break
        except:
            PrintException()
        sys.stdout.flush()
        sys.stderr.flush()
request()