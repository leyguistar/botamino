#!/usr/bin/env python3
from save import Save
s = Save(file='default.set')
r = s.loadAllOPS()
for chatid,ops in r.items():
    print(chatid)
    remove = []
    for u,o in ops.items():
        if(o == 3):
            remove.append(u)
    for u in remove:
        ops.pop(u)
    
    s.opChat(chatid,ops)
exit()