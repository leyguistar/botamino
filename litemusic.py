import subprocess
from exception import PrintException
import os
import signal
from channel import Channel
def killPlayer(chatid):
    proc = subprocess.Popen(["ps","ax"],stdout=subprocess.PIPE)
    r = proc.communicate()
    l = r[0].decode('utf-8').split('\n')
    for i in l:
        if(chatid in i):
            print(i)
            try:
                try:
                    pid = int(i.split(' ')[0])
                except:
                    pid = int(i.split(' ')[1])
            except:
                PrintException()
            try:
                os.kill(pid,signal.SIGKILL)
            except Exception as e:
                print(e)
def waitClose(child):
    streamdata = child.communicate()[0]

def play_audio(channel,playid):
    token = channel.token
    name = channel.name
    uid = channel.uid
    volume = channel.volume
    t = channel.type
    streams = [playid]
    killPlayer(channel.chatid)
    args = ["wine64",simplePlayer,name,token,str(uid),str(volume),"1" ] + streams
    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
    data = proc.communicate()[0]


simplePlayer = 'musicbot/simpleplay.exe'