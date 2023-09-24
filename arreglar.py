#!/usr/bin/env python3
from save import Save
import threading
from exception import PrintException
from time import time
s = Save(file='default.set')
with open('tables2.txt','r') as h:
	tables = h.read().split('\n')
for t in tables:

	s.cursor.execute('create table ' + t)
	# print('create table ' + t)
s.db.commit()
exit()

# tables = s.cursor.fetchall()
# tables = [t[0] for t in tables]
# with open('tables.txt','w') as h:
# 	h.write('\n'.join(tables))
# exit()
# i = 1
# comandosids = {}
# with open('lite/comandos.txt','r') as h:
# 	for c in h.read().split('\n'):
# 		c = c.split(' ')
# 		comandosids[c[0]] = i
# 		i+=1
# i = 1001
# with open('lite/interacciones.txt','r') as h:
# 	for c in h.read().split('\n'):
# 		c = c.split(' ')
# 		comandosids[c[0]] = i
# 		i+=1
# print(comandosids)
# s.cursor.execute('show tables where Tables_in_amino like "custom_op_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# for t in tables:
# 	s.cursor.execute('select comando from %s;' % (t))
# 	comandos = [i[0] for i in s.cursor.fetchall()]
# 	for c in comandos:
# 		if(c not in comandosids):
# 			print('borrando',c)
# 			s.cursor.execute('delete from %s where comando="%s";' % (t,c))
# 		else:
# 			s.cursor.execute('update %s set comando="%d" where comando="%s";' % (t,comandosids[c],c))
# 	s.cursor.execute('alter table %s modify comando int;' % (t))
# 	print('alter table %s modify comando int;' % (t))
def drop(table):
	s = Save()
	s.cursor.execute(f'show tables where Tables_in_amino like "{table}%";')
	tables = [i[0] for i in s.cursor.fetchall()]
	for t in tables:
		s.cursor.execute('drop table %s;' % (t))
		print('drop table %s;' % (t))
	s.db.commit()
def dropEmpty(tables):
	s = Save()

	for t in tables:
		s.cursor.execute('select * from %s limit 10;' % (t))
		r = s.cursor.fetchall()
		if(len(r) < 1):
			try:
				s.cursor.execute('drop table %s;' % (t))
				print('drop table %s;' % (t))
			except:
				pass
	s.db.commit()
	s.close()
def chatOp(tables):
	s = Save()
	# s.cursor.execute(f'show tables where Tables_in_amino like "{table}%";')

	lastStart = time()
	for t in tables:
		if(time() > lastStart + 260):
			s.db.commit()
			s.close()
			s.connect()
			lastStart = time()
		# s.cursor.execute('select id,level from %s;' % (t))
		# chatid = t[4:].replace('_','-')
		# ops = s.cursor.fetchall()
		# data = b''
		# for l,v in ops:
		# 	l = l.replace('-','')
		# 	b = bytes.fromhex(l)
		# 	data += b
		# 	data += v.to_bytes(4,'big')
		# text = data.decode('latin1').replace("\\","\\\\").replace('"','\\"')
		# s.cursor.execute('insert into ops (chatid,ops) values ("%s","%s");' % (chatid,text))
		# print('insert into ops (chatid,ops) values ("%s","%s");' % (chatid,text))

		print('drop table %s;' % (t))
		s.cursor.execute('drop table %s;' % (t))
	s.db.commit()
	s.close()

def chatCustomOp(tables):
	s = Save()
	# s.cursor.execute(f'show tables where Tables_in_amino like "{table}%";')
	lastStart = time()
	for t in tables:
		if(time() > lastStart + 260):
			s.db.commit()
			s.close()
			s.connect()
			lastStart = time()
		if('premium' in t):
			print('drop table %s;' % (t))
			s.cursor.execute('drop table %s;' % (t))
		else:
			chatid = t[10:].replace('_','-')
			s.cursor.execute('select comando,op from %s;' % (t))
			ops = dict(s.cursor.fetchall())
			if(ops):
				lock.acquire()
				print(ops)
				s.customOP(chatid,ops)
				lock.release()
		print('drop table %s' % (t))
		s.cursor.execute('drop table %s' % (t))


	s.db.commit()
	s.close()

def media(tables):
	s = Save()
	# s.cursor.execute(f'show tables where Tables_in_amino like "{table}%";')
	lastStart = time()
	for t in tables:
		if('media_user' in t):
			print('drop table %s' % (t))
			s.cursor.execute('drop table %s' % (t))
			continue
		objectid = t.replace('media_chat_','').replace('saved_user_','').replace('_','-')
		if(time() > lastStart + 260):
			s.db.commit()
			s.close()
			s.connect()
			lastStart = time()
		else:
			chatid = t[10:].replace('_','-')
			try:
				s.cursor.execute('select name,content,tipo from %s;' % (t))
			except:
				pass
			else:
				ops = s.cursor.fetchall()
				if(ops):
					for m in ops:
						s.media(objectid,m[0],m[1],m[2])
		print('drop table %s' % (t))
		s.cursor.execute('drop table %s' % (t))


	s.db.commit()
	s.close()

def comandos(tables):
	s = Save()
	lastStart = time()
	for t in tables:
		objectid = t.replace('comandos_bienvenida_','').replace('_','-')
		if(time() > lastStart + 260):
			s.db.commit()
			s.close()
			s.connect()
			lastStart = time()
		else:
			chatid = t[10:].replace('_','-')
			s.cursor.execute('select comando from %s;' % (t))
			comando = s.cursor.fetchall()
			for c in comando:
				if(c[0] == '/recibir'):
					continue
				s.comandoBienvenida(objectid,c[0])
		print('drop table %s' % (t))
		s.cursor.execute('drop table %s' % (t))


	s.db.commit()
	s.close()
def comandos2(tables):
	s = Save()
	lastStart = time()
	for t in tables:
		objectid = t.replace('comandos_donaciones_','').replace('_','-')
		if(time() > lastStart + 260):
			s.db.commit()
			s.close()
			s.connect()
			lastStart = time()
		else:
			chatid = t[10:].replace('_','-')
			s.cursor.execute('select comando,min,max from %s;' % (t))
			comando = s.cursor.fetchall()
			for c in comando:
				s.comandoDonacion(objectid,c[0],c[1],c[2])
		print('drop table %s' % (t))
		s.cursor.execute('drop table %s' % (t))


	s.db.commit()
	s.close()
def comandos3(tables):
	s = Save()
	lastStart = time()
	for t in tables:
		if('comandos_comunidad' in t or 'comandos_bienvenida' in t or 'comandos_donacion' in t or 'comandos_creados' in t):
			continue
		objectid = t.replace('comandos_','').replace('_','-')
		if(time() > lastStart + 260):
			s.db.commit()
			s.close()
			s.connect()
			lastStart = time()
		else:
			chatid = t[10:].replace('_','-')
			s.cursor.execute('select nombre,comando,descripcion,uid from %s;' % (t))
			comando = s.cursor.fetchall()
			for c in comando:
				s.chatComand(c[0],c[1],c[2],c[3],objectid)
		print('drop table %s' % (t))
		s.cursor.execute('drop table %s' % (t))


	s.db.commit()
	s.close()


def comandosComunidad(tables):
	s = Save()
	# s.cursor.execute(f'show tables where Tables_in_amino like "{table}%";')
	lastStart = time()
	for t in tables:
		if(time() > lastStart + 260):
			s.db.commit()
			s.close()
			s.connect()
			lastStart = time()
		comid = int(t[19:])
		s.cursor.execute('select comando,op from %s;' % (t))
		ops = dict(s.cursor.fetchall())
		if(ops):
			lock.acquire()
			print(ops)
			s.comandoComunidad(comid,ops)
			lock.release()
		# print('drop table %s' % (t))
		# s.cursor.execute('drop table %s' % (t))
	s.db.commit()
	s.close()
def respuestas(tables):
	s = Save()
	# s.cursor.execute(f'show tables where Tables_in_amino like "{table}%";')

	lastStart = time()
	for t in tables:
		if(time() > lastStart + 260):
			s.db.commit()
			s.close()
			s.connect()
			lastStart = time()
		objectid = t[11:].replace('_','-')
		s.cursor.execute('select mensaje,respuesta from %s;' % (t))
		res = dict(s.cursor.fetchall())
		if(res):
			lock.acquire()
			print(objectid,res)
			s.respuestas(objectid,res)
			lock.release()
		# print('drop table %s' % (t))
		# s.cursor.execute('drop table %s' % (t))
	s.db.commit()
	s.close()

def unsimp():
	s.cursor.execute('select userid,simping from simps where length(simping) > 160;')
	simpings = s.cursor.fetchall()
	for simping in simpings:
		userid = simping[0]
		simping = simping[1]
		simping = simping[:160]
		try:
			s.cursor.execute('update simps set simping="%s" where userid="%s";' % (simping.replace("\\","\\\\").replace('"','\\"'),userid))
		except:
			PrintException()

	s.cursor.execute('select userid from simps;')
	usersid = s.cursor.fetchall()
	simps = {}
	simping = {}
	for u in usersid:
		u = u[0]
		s1,s2 = s.loadSimps(u)
		simps[u] = s1
		simping[u] = s2
	for u in simps:
		fakesimps = []
		for simp in simps[u]:
			if(u not in simping[simp]):
				fakesimps.append(simp)
		for simp in fakesimps:
			simps[u].remove(simp)
		s.simpsUser(u,simps[u])
	s.db.commit()
def chunks(lst,n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
# drop('user_autorizados')
# drop('messages_')
# drop('chats_user_')
# drop('strikes_')
drop('simple_messages')
drop('chats_user_')
# t = threading.Thread(target=dropEmpty,args=('respuestas_',))
# t.start()
# t = threading.Thread(target=dropEmpty,args=('custom_op_',))
# t.start()
lock = threading.Lock()
# exit()
# s.cursor.execute(f'show tables where Tables_in_amino like "ops_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# chatOp(tables)
# s.cursor.execute(f'show tables where Tables_in_amino like "custom_op_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# chatCustomOp(tables)
# s.cursor.execute(f'show tables where Tables_in_amino like "comandos_comunidad_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# comandosComunidad(tables)
# s.cursor.execute(f'show tables where Tables_in_amino like "respuestas_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# respuestas(tables)
# ts = []
# s.cursor.execute(f'show tables where Tables_in_amino like "media_chat_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# print(len(tables))
# if(tables):
# 	if(len(tables) < 32):
# 		media(tables)
# 	else:
# 		li = list(chunks(tables,len(tables)//32))
# 		for l in li: 
# 			t = threading.Thread(target=media,args=(l,))
# 			t.start()
# 			ts.append(t)
# 		for t in ts:
# 			t.join()
# s.close()
# s.connect()
# ts = []
# s.cursor.execute(f'show tables where Tables_in_amino like "saved_user_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	if(len(tables) < 32):
# 		media(tables)
# 	else:
# 		li = list(chunks(tables,len(tables)//32))
# 		for l in li: 
# 			t = threading.Thread(target=media,args=(l,))
# 			t.start()
# 			ts.append(t)
# 		for t in ts:
# 			t.join()
# s.close()
# s.connect()
# s.cursor.execute(f'show tables where Tables_in_amino like "comandos_bienvenida_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	if(len(tables) < 32):
# 		comandos(tables)
# 	else:
# 		li = list(chunks(tables,len(tables)//32))
# 		for l in li: 
# 			t = threading.Thread(target=comandos,args=(l,))
# 			t.start()
# 			ts.append(t)
# 		for t in ts:
# 			t.join()
# s.close()
# s.connect()
# s.cursor.execute(f'show tables where Tables_in_amino like "comandos_donaciones_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	if(len(tables) < 32):
# 		comandos2(tables)
# 	else:
# 		li = list(chunks(tables,len(tables)//32))
# 		for l in li: 
# 			t = threading.Thread(target=comandos2,args=(l,))
# 			t.start()
# 			ts.append(t)
# 		for t in ts:
# 			t.join()
# s.close()

# s.connect()
# s.cursor.execute(f'show tables where Tables_in_amino like "bienvenida_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	if(len(tables) < 32):
# 		comandos2(tables)
# 	else:
# 		li = list(chunks(tables,len(tables)//32))
# 		for l in li: 
# 			t = threading.Thread(target=drop,args=(l,))
# 			t.start()
# 			ts.append(t)
# 		for t in ts:
# 			t.join()
# s.close()

# s.connect()
# s.cursor.execute(f'show tables where Tables_in_amino like "comandos_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	if(len(tables) < 32):
# 		comandos2(tables)
# 	else:
# 		li = list(chunks(tables,len(tables)//32))
# 		for l in li: 
# 			t = threading.Thread(target=comandos3,args=(l,))
# 			t.start()
# 			ts.append(t)
# 		for t in ts:
# 			t.join()
# s.close()


# s.connect()
# ts = []
# s.cursor.execute(f'show tables where Tables_in_amino like "strikes_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# drop(tables)
# # if(tables):
# # 	li = list(chunks(tables,len(tables)//32))
# # 	for l in li: 
# # 		t = threading.Thread(target=drop,args=(l,))
# # 		t.start()
# # 		ts.append(t)
# # 	for t in ts:
# # 		t.join()
# s.close()
# exit()
# s.connect()
# s.cursor.execute(f'show tables where Tables_in_amino like "ops_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	li = list(chunks(tables,len(tables)//32))
# 	for l in li: 
# 		t = threading.Thread(target=chatOp,args=(l,))
# 		t.start()
# 		ts.append(t)
# 	for t in ts:
# 		t.join()
# ts = []
# s.close()
# s.connect()
# s.cursor.execute(f'show tables where Tables_in_amino like "custom_op_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	li = list(chunks(tables,len(tables)//32))
# 	for l in li: 
# 		t = threading.Thread(target=chatCustomOp,args=(l,))
# 		t.start()
# 		ts.append(t)
# 	for t in ts:
# 		t.join()

# ts = []
# s.close()
# s.connect()
# s.cursor.execute(f'show tables where Tables_in_amino like "comandos_comunidad_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	li = list(chunks(tables,len(tables)//32))
# 	for l in li: 
# 		t = threading.Thread(target=comandosComunidad,args=(l,))
# 		t.start()
# 		ts.append(t)
# 	for t in ts:
# 		t.join()

# ts = []
# s.close()
# s.connect()
# s.cursor.execute(f'show tables where Tables_in_amino like "respuestas_%";')
# tables = [i[0] for i in s.cursor.fetchall()]
# if(tables):
# 	li = list(chunks(tables,len(tables)//32))
# 	for l in li: 
# 		t = threading.Thread(target=respuestas,args=(l,))
# 		t.start()
# 		ts.append(t)
# 	for t in ts:
# 		t.join()



# dropEmpty('respuestas_')
# dropEmpty('custom_op_')
# dropEmpty('user_autorizados_chat_')
s.db.commit()