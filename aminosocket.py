#!/usr/bin/env python3
import time
import websocket
import threading
import contextlib
import ujson as json
import simplejson
from collections import deque
from exception import PrintException
import requests
from hashlib import sha1
import hmac
import base64
import time

class SocketHandler:
    def __init__(self,sid,device_id, handle_message, userid=None, reconnectTime = 600,socket_trace = False, debug = False,allMessages=False,callbacks=None,canSend=True):
        print('iniciando socket')
        websocket.enableTrace(True)
        self.socket_url = "wss://ws4.narvii.com"
        self.sid = sid
        self.userid = userid
        self.device_id = device_id
        self.debug = debug
        self.handle_message = handle_message
        self.active = False
        self.headers = None
        self.socket = None
        self.socket_thread = None
        self.reconnect = True
        self.socket_stop = False
        self.socketDelayFetch = reconnectTime  # Reconnects every 120 seconds.
        self.e = threading.Event()
        self.thread = None
        self.closing = False
        self.allMessages = allMessages
        self.events = {}
        self.canSend = canSend
        if(not callbacks):
            self.callbacks = {}
        else:
            self.callbacks = callbacks

        websocket.enableTrace(socket_trace)

    def __del__(self):
        self.close()

    def on_open(self):
        if(not self.reconnect):
            self.close()
        if self.debug is True:
            print("[socket][on_open] Socket Opened")

    def on_close(self):
        if self.debug is True:
            print("[socket][on_close] Socket Closed")

        self.active = False

    def on_ping(self, data):
        if self.debug is True:
            print("[socket][on_ping] Socket Pinged")
        if(self.socket and self.socket.sock):
            contextlib.suppress(self.socket.sock.pong(data))
        elif(not self.socket):
            print('Error el socket es None')
        else:
            print("Error socket.sock es None")
    def send(self, data):
        if(not self.canSend):
            return
        if self.debug is True:
            print(f"[socket][send] Sending Data : {data}")
        print(self.userid,'sending:',data)
        self.socket.send(data)
    def setCallBack(self,t,fun,extra=None):
        self.callbacks[t] = (fun,extra)
    def setEvent(self,id,events):
        self.events[id] = events
    def handlerLauncher(self,data):
        try:
            data = simplejson.loads(data)
        except ValueError:
            print('detectado ultra bug')
            if('"clientRefId":,' in data):
                data = data.replace('"clientRefId":,','"clientRefId":-1,')
                try:
                    data = json.loads(data)
                except ValueError:
                    print('value error')
                    return
                except:
                    PrintException()
                else:
                    tChat = threading.Thread(target=self.handle_message, args=(data,self.userid))
                    tChat.daemon = True
                    tChat.start()

            return
        except:
            return

        t = data['t']
        if(self.allMessages):
            try:
                tChat = threading.Thread(target=self.handle_message, args=(data,self.userid))
                tChat.daemon = True
                tChat.start()
            except:
                PrintException()
                return
        if(data['t'] == 1000):
            try:
                if('chatMessage' in data['o']):
                    message = data['o']['chatMessage']
                    messageId = message.get('messageId')
                    tipo = message['type']
                    oldMessagesLock.acquire()
                    if((tipo != 100 and tipo != 119)):
                        if(messageId in oldMessages):
                            oldMessagesLock.release()
                            return
                        oldMessages.append(messageId)
                    else:
                        if(messageId in deleteMessages):
                            oldMessagesLock.release()
                            return
                        deleteMessages.append(messageId)
                    oldMessagesLock.release()
                else:
                    return
            except Exception as e:
                PrintException()
            tChat = threading.Thread(target=self.handle_message, args=(data,self.userid))
            tChat.daemon = True
            tChat.start()
            return
        if(t in self.callbacks):
            tChat = threading.Thread(target=self.callbacks[t][0], args=(data,self.userid,self.callbacks[t][1]))
            tChat.daemon = True
            tChat.start()
        if('id' in data['o'] and self.events):
            i = data['o']['id']
            if(i in self.events):
                if(t in self.events[i]):
                    self.events[i][t][1]['data'] = data
                    self.events[i][t][0].set()
                    self.events[i].pop(t)
                    if(not self.events[i]):
                        self.events.pop(i)


    def get_socket_url(self):
        cookies = {
            'sid': self.sid
        }
        headers = {
            'Host': 'aminoapps.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
            'accept': '*/*',
            'referer': 'https://aminoapps.com/partial/main-chat-window?ndcId=86797652&source=sidebar_community_list&action=click',
            'accept-language': 'en-US,en;q=0.9',
        }
        response = requests.get('https://aminoapps.com/api/chat/web-socket-url', headers=headers, cookies=cookies)
        response = json.loads(response.text)
        url=response['result']['url']
        return url
    def start(self):
        if self.debug is True:
            print(f"[socket][start] Starting Socket")
        if(self.thread):
            return
        now = int(time.time() * 1000)
        self.headers = {
            "NDC-MSG-SIG": base64.b64encode(b"\x42" + hmac.new(bytes.fromhex("F8E7A61AC3F725941E3AC7CAE2D688BE97F30B93"), f"{self.device_id}|{now}".encode(), sha1).digest()).decode(),
            "NDCDEVICEID": self.device_id,
            "NDCAUTH": f"sid={self.sid}"
        }
        if(self.socket):
            self.socket.close()
            if(self.socket.keep_running):
                return
        self.socket = websocket.WebSocketApp(
            f"{self.socket_url}/?signbody={self.device_id}%7C{now}",
            # f"{self.socket_url}/?signbody={self.device_id}%7C{int(time.time() * 1000)}",
            on_message = self.handlerLauncher, #aqui esta lo interesante
            on_open = self.on_open,
            on_close = self.on_close,
            on_ping = self.on_ping,
            header = self.headers
        )
        print('creando hilo')
        self.socket_thread = threading.Thread(target = self.hilo, args = ())
        self.socket_thread.start()
        self.active = True

    def hilo(self):
        while not self.closing:
            self.socket.run_forever(ping_interval=60,max_active_time=self.socketDelayFetch)
            now = int(time.time() * 1000)
            self.socket.url = f"{self.socket_url}/?signbody={self.device_id}%7C{now}"
            self.headers = {
                "NDC-MSG-SIG": base64.b64encode(b"\x32" + hmac.new(bytes.fromhex("fbf98eb3a07a9042ee5593b10ce9f3286a69d4e2"), f"{self.device_id}|{now}".encode(), sha1).digest()).decode(),
                "NDCDEVICEID": self.device_id,
                "NDCAUTH": f"sid={self.sid}"
            }
            self.socket.header = self.headers 


    def close_socket(self):
        if(self.socket):
            self.socket.keep_running = False 
            self.socket.close()

    def close(self):
        if(not self.active):
            return
        if self.debug is True:
            print(f"[socket][close] Closing Socket")
        self.closing = True
        self.reconnect = False
        self.active = False
        self.socket_stop = True
        self.e.set()
        self.close_socket()
oldMessages = deque([],maxlen=5000)
oldMessagesLock = threading.Lock()
deleteMessages = deque([],maxlen=500)
