import os
import gtk

from random import randint

from constants import *

album_art = {}

def choose(a,dnr):
    if len(a) == 1:
        return a[0]
    else:
        r = [p for p in a if not (p == dnr)]
        return r[randint(0,len(r)-1)]

def get_album_art(d,dnr = None):
    print "getting album art..."
    if not (d in album_art.keys()):
        fill_album_art(d)            
        
    return choose(album_art[d],dnr)
    
    
QUICK = 0
def fill_album_art(d):
    pics = []
    for root, dirs, files in os.walk(d):
        if QUICK == 1: break
        for name in files:
            if name[-3:] == "jpg" or name[-4:] == "jpeg":
                fullpath = os.path.join(root, name)
                pics.append(gtk.gdk.pixbuf_new_from_file(fullpath).scale_simple(ALBUMARTLENGTH,ALBUMARTLENGTH,gtk.gdk.INTERP_BILINEAR))            
    
    if len(pics) == 0:
        pics = [gtk.gdk.pixbuf_new_from_file("/home/xuanji/fsm/Octavarium.jpg").scale_simple(ALBUMARTLENGTH,ALBUMARTLENGTH,gtk.gdk.INTERP_BILINEAR)]
    
    album_art[d] = pics
