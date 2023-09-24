#!/usr/bin/env python3
import boto3
import os
import requests
from botocore.exceptions import ClientError
from save import Save
from exception import PrintException
from time import sleep
s3 = boto3.resource('s3')
s = Save(file='default.set')


def upload_file_s3(file_name, object_name=None,bucket='leybot-data'):
	if object_name is None:
		object_name = file_name

	# Upload the file
	s3_client = boto3.client('s3')
	try:
		response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL': 'public-read'})
	except:
		PrintException()        
		return False
	return True

def getTables(tables):
	for t in tables:
		chatid = t[11:].replace('_','-')  
		s.cursor.execute('alter table %s change nombre name varchar(50);' % (t) )  
		s.cursor.execute('alter table %s change type tipo int;' % (t) )  
		try:
			s.cursor.execute('select name,content,tipo from %s;' % (t) )  
		except Exception as e:
			print(e)
			s.cursor.execute('select count(*) from %s;' % (t))
			r = s.cursor.fetchone()[0]
			if(r == 0):
				s.cursor.execute('drop table %s;' % (t) )
			continue
		ms = s.cursor.fetchall()
		for m in ms:
			if(m[2] == 2):
				try:
					url = m[1].replace('leybot-amino-data-data.s3.','leybot-amino-data.s3.')

					data = requests.get(url).content
					ftmp = '/tmp/' + url[url.rfind('/')+1:]
					with open(ftmp,'wb') as h:
						h.write(data)
					upload_file_s3(file_name=ftmp,object_name=url.replace('https://leybot-amino-data.s3.amazonaws.com/',''))
					s.cursor.execute('update %s set content="%s" where name="%s"' % (t,url.replace('leybot-amino-data.s3.','leybot-data.s3.'),m[0]))
					print('update %s set content="%s" where name="%s"' % (t,url.replace('leybot-amino-data.s3.','leybot-data.s3.'),m[0]))
					# sleep(5)
				except FileNotFoundError as e:
					print('no se encontro equisde',e)
				except Exception as e:
					PrintException()
	s.db.commit()
# s.cursor.execute('show tables where Tables_in_amino like "media_chat_%"')
# tables = [i[0] for i in s.cursor.fetchall()]
# print(tables)
# getTables(tables)
s.cursor.execute('show tables where Tables_in_amino like "saved_user_%"')
tables = [i[0] for i in s.cursor.fetchall()]
print(tables)
getTables(tables)