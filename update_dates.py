#!/usr/bin/env python3

from save import Save

s = Save()
s.cursor.execute('show tables where Tables_in_amino like "messages%";')
tables = s.cursor.fetchall()
for table in tables:
	table = table[0]
	print(table)
	try:
		s.cursor.execute('select createdTime from ' + table + ';')
		fechas = s.cursor.fetchall()
		i = 0
		for f in fechas:
			i += 1
			f = f[0]
			if('T' in f):
				s.cursor.execute('update %s set createdTime="%s" where createdTime="%s";' % (table,f.replace('T',' ').replace('Z',''),f ) ) 
			if(i%100 == 0):
				print(i)
				s.db.commit()
		s.cursor.execute('ALTER TABLE '+ table +' MODIFY createdTime datetime;')
		s.db.commit()
	except:
		print('ignorando ' + table)