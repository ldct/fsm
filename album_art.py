import os
import pygtk, gtk, gobject
import gtk.glade
import pygst
pygst.require("0.10")
import gst

from random import randint

from constants import *

album_art = {}

def get_album_art(d):
    print "getting album art..."
    if not (d in album_art.keys()):
        fill_album_art(d)            
        
    pics = album_art[d]
    
    return pics[randint(0,len(pics)-1)]
    
def fill_album_art(d):
    print "filling album art..."
    pics = []
    for root, dirs, files in os.walk(d):
        for name in files:
            if name[-3:] == "jpg" or name[-4:] == "jpeg":
                fullpath = os.path.join(root, name)
                pics.append(gtk.gdk.pixbuf_new_from_file(fullpath).scale_simple(ALBUMARTLENGTH,ALBUMARTLENGTH,gtk.gdk.INTERP_BILINEAR))
    
    if len(pics) == 0:
        pics = [gtk.gdk.pixbuf_new_from_file("/home/xuanji/fsm/Octavarium.jpg").scale_simple(ALBUMARTLENGTH,ALBUMARTLENGTH,gtk.gdk.INTERP_BILINEAR)]
    
    album_art[d] = pics
