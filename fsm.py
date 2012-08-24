#!/usr/bin/env python

import sys, os, thread, time
import gtk, gst

from constants import *
from album_art import get_album_art

def list_files(d):
    for root, dirs, files in os.walk(d):
        for name in files:
            ext = name[-4:]
            if ext in [".ogg", ".mp3", "flac"]:
                filename = os.path.join(root, name)
                yield filename

def cut(s):
    words = s.split()
    lines = [""]
    
    while len(words) > 0:
        if len(words[0]) + len(lines[-1]) < LINELENGTH:
            lines[-1] = lines[-1] + " " + words[0]
            words = words[1:]
        else:
            lines.append(words[0][:LINELENGTH])
            words[0] = words[0][LINELENGTH:]
    return '\n'.join([l for l in lines if l != ""][:MAXLINES])
        
def convert_ns(t):
    s,ns = divmod(t, 1000000000)
    m,s = divmod(s, 60)

    if m < 60:
        return "%02i:%02i" %(m,s)
    else:
        h,m = divmod(m, 60)
        return "%i:%02i:%02i" %(h,m,s) 

class GTK_Main:

    music_directory = "/home/xuanji/Music"
    builder = gtk.Builder()
    album_art = {}
    
    def __init__(self):
        
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(self)
        
        self.player = gst.element_factory_make("playbin2", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        
        self.builder.get_object("album-view").set_text_column(0)
        self.builder.get_object("album-view").set_pixbuf_column(1)

        self.an_image = gtk.gdk.pixbuf_new_from_file("/home/xuanji/fsm/20.jpg").scale_simple(120,120,gtk.gdk.INTERP_BILINEAR)
        self.bn_image = gtk.gdk.pixbuf_new_from_file("/home/xuanji/fsm/Octavarium.jpg").scale_simple(120,120,gtk.gdk.INTERP_BILINEAR)
        self.fill_store()

        self.respond_to_slider = False

        col = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=0)
        self.builder.get_object("song-view").append_column(col)
        
        thread.start_new_thread(self.time_cron, ())
        
        self.builder.get_object("fsm-audioplayer").show()

    def get_icon(self, name):
        theme = gtk.icon_theme_get_default()
        return theme.load_icon(name, 48, 0)
        
        
    def fill_store(self):
        self.builder.get_object("album-store").clear()
        for fl in os.listdir(self.music_directory):
            self.builder.get_object("songs-store").append([fl])
            if not fl[0] == '.':
                fullpath = os.path.join(self.music_directory, fl)
                if os.path.isdir(fullpath):
                    self.builder.get_object("album-store").append([cut(fl),get_album_art(fullpath), fullpath])

    def load_new_file(self, filepath):
        if os.path.isfile(filepath):
            self.player.set_state(gst.STATE_READY)
            self.player.set_property("uri", "file://" + filepath)
            self.player.set_state(gst.STATE_PLAYING)  

    def play_pause(self, w):
        if w.get_active():
            self.player.set_state(gst.STATE_PLAYING)
        else:
            self.player.set_state(gst.STATE_PAUSED)
        self.update_time()

    def rewind_callback(self, w):
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        seek_ns = pos_int - (10 * 1000000000)
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)
        
    def forward_callback(self, w):
        print "forward"
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        seek_ns = pos_int + (10 * 1000000000)
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)
        
    def album_view_item_activated_callback(self, w, path):
        i = self.builder.get_object("album-store").get_iter(path)
        s = self.builder.get_object("album-store").get(i,2)[0]
        p = self.builder.get_object("album-store").get(i,1)[0]
        self.builder.get_object("selected-album").set_text(s)
        
        print "album selected - " +s
        
        self.builder.get_object("album-store").set(i,1,get_album_art(s,p))
        
        self.builder.get_object("songs-store").clear()
        for f in list_files(s):
            self.builder.get_object("songs-store").append([f])
            
    def song_view_row_activated_callback(self, treeview, path, view_column):
    
        i = self.builder.get_object("songs-store").get_iter(path)
        s = self.builder.get_object("songs-store").get(i,0)[0]

        self.load_new_file(s)
        self.builder.get_object("play_pause_toggle").set_active(True)

        
    def playback_callback(self, w):
        if self.respond_to_slider:
            dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
            new_pos = dur_int * w.get_value() / 100.
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, new_pos)
        
    def update_time(self):
        try:
            pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
            dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
        except gst.QueryError:
            return
        
        self.builder.get_object("time-label").set_text(convert_ns(pos_int) + " / " + convert_ns(dur_int))
        self.respond_to_slider = False
        self.builder.get_object("playback-adjustment").set_value((float(pos_int) / float(dur_int)) * 100.)
        self.respond_to_slider = True
        
    def time_cron(self):
    
        print "hi"
        count = 0
    
        while True:
        
            print count
            count += 1
        
            time.sleep(1.0)
            gtk.gdk.threads_enter()
            self.update_time()
            gtk.gdk.threads_leave()

                        
    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.builder.get_object("play_pause_toggle").set_label("Start")
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.builder.get_object("play_pause_toggle").set_label("Start")

app = GTK_Main()
gtk.gdk.threads_init()
gtk.main()
