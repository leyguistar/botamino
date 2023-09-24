#!/usr/bin/env python3
import amino
from save import Save
client = amino.Client()
client.login(secret='31 IIMPhiXM 1e6ee751-012c-4426-b7a6-6bc1ecad48ee 3.233.211.164 0e4a69d1b3066ca9a127890a5531929f3818f16b 1 1615275128 N0Bje4x89jBogAemAAcUYgLx62g')
sub_client = client.sub_client(103238282)
chatid = 'c77d6f8e-9c5e-40ae-811d-bc000400996b'
messageList = sub_client.get_chat_messages(chatId=chatid,size=100,raw=True)['messageList']  # Gets messages of each chat
while(messageList):
    for m in messageList:
        sub_client.delete_message(chatid,m['messageId'],asStaff=True)
    messageList = sub_client.get_chat_messages(chatId=chatid,size=100,raw=True)['messageList']  # Gets messages of each chat

exit()
