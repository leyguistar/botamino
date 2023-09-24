#!/usr/bin/env python3
from save import Save
import boto3
from botocore.exceptions import ClientError
import os
s = Save(file='default.set')

def upload_file_s3(file_name, object_name=None,bucket='leybot-amino-data'):
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL': 'public-read'})
    except ClientError as e:
        print(e)
        return False
    return True
#media
s.cursor.execute('show tables where Tables_in_amino like "media_chat_%"')
tables = [i[0] for i in s.cursor.fetchall()]
for t in tables:
    s.cursor.execute('ALTER TABLE %s modify COLUMN content text;' % (t))
    chatid = t[11:].replace('_','-')
    mediaPath = os.environ.get('MEDIADIR','media') + '/' + chatid + '/'
    s.cursor.execute('select name,content,tipo from %s;' % (t) )  
    ms = s.cursor.fetchall()
    for m in ms:
        if(m[2] == 2):
            try:
                upload_file_s3(mediaPath + m[1],'media/' + chatid + '/' + m[1])
                s.cursor.execute('update %s set content="%s" where name="%s"' % (t,'https://leybot-amino-data.s3.amazonaws.com/media/%s/%s' % (chatid,m[1]),m[0] ))
                print('update %s set content="%s" where name="%s"' % (t,'https://leybot-amino-data.s3.amazonaws.com/media/%s/%s' % (chatid,m[1]),m[0] ))
            except FileNotFoundError as e:
                print('no se encontro equisde',e)
            except Exception as e:
                print(e)
savesdir = os.environ.get('SAVESDIR','saves') + '/'

#saves
s.cursor.execute('show tables where Tables_in_amino like "saved_user_%"')
tables = [i[0] for i in s.cursor.fetchall()]
for t in tables:
    userid = t[11:].replace('_','-')
    s.cursor.execute('select nombre,content,type from %s;' % (t) )  
    ms = s.cursor.fetchall()
    for m in ms:
        if(m[2] == 2):
            try:
                upload_file_s3(savesdir + m[1],'saves/' + userid + '/' + m[1])
                s.cursor.execute('update %s set content="%s" where nombre="%s"' % (t,'https://leybot-amino-data.s3.amazonaws.com/saves/%s/%s' % (userid,m[1]),m[0] ))
                print('update %s set content="%s" where nombre="%s"' % (t,'https://leybot-amino-data.s3.amazonaws.com/saves/%s/%s' % (userid,m[1]),m[0] ))
            except FileNotFoundError as e:
                print('no se encontro equisde',e)
            except Exception as e:
                print(e)
s.db.commit()