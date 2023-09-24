#!/usr/bin/env python3
import socket
import sys
import json
TCP_IP = "127.0.0.1"
TCP_PORT = 15150
m = sys.argv[1].encode('utf-8')

s = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP
s.connect((TCP_IP, TCP_PORT))
s.send(m)
data = s.recv(1024)
data = json.loads(data.decode('utf-8'))
print(list(data.values())[0])
s.close()
