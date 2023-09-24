#!/usr/bin/env python3
import socket
from time import sleep
import threading
from exception import PrintException
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
    while 1:
        try:
            conn, addr = s.accept()
            t = threading.Thread(target=checkMessage,args=(conn,))
            t.start()
        except KeyboardInterrupt:
            break
        except:
            PrintException()
request()