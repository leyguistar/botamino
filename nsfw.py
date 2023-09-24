#!/usr/bin/env python3
from sightengine.client import SightengineClient
import requests
import ujson as json
def picpurify(url):
	picpurify_url = 'https://www.picpurify.com/analyse/1.1'
	API_KEY = 'Tyi76E6eMKvKq2lxsCHBni7CiEbdQD1C'
	result = requests.post(picpurify_url,data = {"url_image":url, "API_KEY":API_KEY, "task":"porn_moderation"})
	result = result.json()
	if(result['status'] == 'success'):
		porn = result['porn_moderation']
		if(porn['porn_content']):
			return True
		else:
			return False
	else:
		return None

def nudity(url):
	client = SightengineClient('201853789','UqNrasvdoG8nDJZC4AG2')
	output = client.check('nudity').set_url(url)
	if(output['status'] == 'sucess'):
		request = output['nudity']
		return 1-request['safe']
	return None

def deepAI(url):
	r = requests.post(
	    "https://api.deepai.org/api/nsfw-detector",
	    data={
	        'image': url,
	    },
	    headers={'api-key': '849ac977-4054-42d2-9540-98b7d0827fd8'}
	)
	json = r.json()
	return json['nsfw_score']

def nudeDetect(url):
	url = "https://netspark-nude-detect-v1.p.rapidapi.com/url/"+url

	headers = {
	    'x-rapidapi-key': "73bfa436f4mshb1f983a90555b54p1b5f3ejsnf1fb06ff42ef",
	    'x-rapidapi-host': "netspark-nude-detect-v1.p.rapidapi.com"
	    }

	response = requests.request("GET", url, headers=headers)
	response = json.loads(response.text)
	if(response['status'] == 'success'):
		return float(response['is nude']['confidence'].strip('%')) / 100
	else:
		return None

