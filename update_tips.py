#!/usr/bin/env python3

from save import Save
import amino
import datetime
s = Save()
login = s.loginInfo(alias='ley')
ley = 'your_uuid'
leybot = '4882156e-efce-4a4b-88ca-02baff4d5e89'
client = amino.Client()
client.login(email=login[0],password=login[1])
sub_client = amino.SubClient(comId='67',profile=client.profile)
data = sub_client.get_tipped_users(size=50,chatId='e1ed3d4b-d58a-4209-ab1e-69218df1c3c6')
tips = {} 		
for uid,coins,t in zip(data.author.id,data.totalTippedCoins,data.lastTippedTime):
	coins = int(coins)
	t = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
	tips[uid] = (coins,t)
tips = {k: v for k, v in sorted(tips.items(), key=lambda item: item[1],reverse=True)}
s.chatTips(tips,'e1ed3d4b-d58a-4209-ab1e-69218df1c3c6')
client.logout()