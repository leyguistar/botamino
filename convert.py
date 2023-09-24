from PIL import Image
from liteobjs import EDIT_SERVER_IP
from time import time
import socket
import ujson as json
import requests
def download(url):
    img = requests.get(url).content
    f = tmp(url[url.rfind('.'):])
    with open(f,'wb') as h:
        h.write(img)
    return f

def tmp(type):
    return '/tmp/' + str(time()).replace('.','') + '.' + type

def convert(filename=None,url=None,output=None):
    data = {
        "comando":"convert"
    }

    if(url):
        data['type'] = 'url'
        data['url'] = url
        b = editRequest(data,output=output)
        if(not b):
            filename = download(url)

            b = localConvert(filename,output=output)
    else:
        b = localConvert(filename,output=output)
    return b

def localConvert(filename,output=None):
    img = Image.open(filename)
    m = max(img.size)
    x,y = img.size
    r = 1000/m
    img = img.resize((int(x*r),int(r*y) ) )
    if(output):
    	f = output
    else:
    	f = tmp(filename[filename.find('.')+1:])
    img.save(f,format="PNG")
    return f

def editRequest(data,output=None):
    TCP_IP = EDIT_SERVER_IP
    TCP_PORT = 10005
    print('conectando con',EDIT_SERVER_IP,TCP_PORT)
    url = None
    filename = None
    s = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) # UDP
    s.settimeout(3)    
    try:
        s.connect((TCP_IP, TCP_PORT))
    except:
        return None
    s.send(json.dumps(data).encode('utf-8'))
     
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
        if(output):
        	file = output
        else:
        	file = tmp(t)
        with open(file,'wb') as h:
            h.write(data)
        files.append(file)
    s.close()
    if(len(files) == 1):
        return files[0]
    else:
        return files[0],files[1]
