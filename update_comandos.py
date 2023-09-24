#!/usr/bin/env python3

from save import Save

s = Save()
s.cursor.execute('show tables where Tables_in_amino like "comandos_%";')
tables = s.cursor.fetchall()
for table in tables:
	table = table[0]

	print(table)
	comandos = 'comandos_' +table[8:]
	try:
		s.cursor.execute('alter table '+ table +' add op int')
		s.cursor.execute('alter table '+ table +' add uid varchar(50);')
		s.db.commit()
	except Exception as e:
		print(e)
		print('ignorando ' + table)