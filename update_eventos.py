#!/usr/bin/env python3

from save import Save

s = Save()
s.cursor.execute('show tables where Tables_in_amino like "eventos%";')
tables = s.cursor.fetchall()
for table in tables:
	table = table[0]

	print(table)
	comandos = 'comandos_' +table[8:]
	try:
		s.cursor.execute('create table if not exists ' + comandos + '(nombre varchar(100) primary key,comando text,descripcion text);')
		s.cursor.execute('alter table '+ table +' add comando varchar(100);')
		s.cursor.execute('alter table '+ table +' add userid varchar(50);')

		s.cursor.execute('ALTER TABLE '+ table +' ADD CONSTRAINT FOREIGN KEY (comando) references '+comandos +' (nombre);')
		s.db.commit()
	except:
		print('ignorando ' + table)