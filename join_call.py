import websocket
from time import time,sleep
import json
import threading
def join_voice_chat(client,chatid,comid,joinRole=1):
	headers = {
		"NDCDEVICEID": client.device_id,
		"NDCAUTH": f"sid={client.sid}"
	}

	data = {
		"o":{
			"ndcId":comid,
			"threadId":chatid,
			"id":'143245',
			"joinRole":joinRole
		},
		"t":112
	}
	data = json.dumps(data)
	socket = websocket.WebSocketApp(
		f"wss://ws1.narvii.com/?signbody={client.device_id}%7C{int(time() * 1000)}",
		header = headers,
	)
	threading.Thread(target = socket.run_forever, kwargs = {"ping_interval": 60}).start()
	result = True
	for i in range(10): #only 10 attempts (5 seconds to connect)
		try:
			sleep(0.5)
			socket.send(data.encode('utf-8'))
		except:
			pass
		else:
			break
	else:
		result = False
	try:
		socket.close()
	except:
		pass 
	return result	