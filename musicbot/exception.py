#!/usr/bin/env python3
import linecache
import traceback
import sys
from time import time
def PrintException(file=None):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    traceback.print_exc()
    with open('errores.txt','a') as h:

        h.write(f'time {time()}\n')
        if(file):
            h.write(f'file {file}')
        else:
            h.write(f'file {__file__}')

        h.write('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
        traceback.print_exc(file=h)
