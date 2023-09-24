from PIL import Image
import os

def convert_small_png(filename,output):
    img = Image.open(filename)
    m = max(img.size)
    x,y = img.size
    # if(m > 1000):
    r = 1000/m
    img = img.resize((int(x*r),int(r*y) ) )
    img.save(output,format="PNG")
    return output
files = os.listdir('waifus')
for f in files:
	if('resize' in f):
		continue
	if(os.path.exists('waifus/resize_' + f)):
		continue
	convert_small_png('waifus/' + f,'waifus/resize_' + f)
	print(f)