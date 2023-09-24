import amino
from time import time
import json
def login(s,userid=None,alias=None,client=None,validTime=3600):
    if(not client):
        client = amino.Client()
    if(userid):
    	login = s.loginInfo(id=userid)
    elif(alias):
    	login = s.loginInfo(alias=alias)
    else:
    	return None

    if(login[2] and login[3] + validTime > time()):
        print('inicio cache')
        client.login_cache(login[2] )
    else:
        print('iniciando normal')
        r = client.login(email=login[0],password=login[1],get=True)

        if(type(r) == dict or r[0] != 200):
            print(r)
            return None
        r1 = json.loads(r[1])
        r1['userProfile']['content'] = 'cache'
        r1 = json.dumps(r1)
        s.newLogin(id=client.profile.id,jsonResponse=r1)
    # print('client',id(client))
    return client