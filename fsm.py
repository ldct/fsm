#!/usr/bin/env python

import sys, os, thread, time
import pygtk, gtk, gobject
import gtk.glade
import pygst
pygst.require("0.10")
import gst

def cut(s, l):
    return s[0:l]
    if len(s) < l:
        return s
    else:
        return s[0:l] + '\n' + cut(s[l:], l)

class GTK_Main:
    
    def __init__(self):
        
        filename = "main.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(filename)
        self.builder.connect_signals(self)
                
        self.builder.get_object("fsm-audioplayer").show()
        
        self.player = gst.element_factory_make("playbin2", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        
        self.builder.get_object("album-view").set_text_column(0)
        self.builder.get_object("album-view").set_pixbuf_column(1)
        
        #self.builder.get_object("song-view").set_text_column(1)

        self.an_image = gtk.gdk.pixbuf_new_from_file("/home/xuanji/fsm/20.jpg").scale_simple(120,120,gtk.gdk.INTERP_BILINEAR)
        self.bn_image = gtk.gdk.pixbuf_new_from_file("/home/xuanji/fsm/Octavarium.jpg").scale_simple(120,120,gtk.gdk.INTERP_BILINEAR)
        self.fill_store()

        self.respond_to_slider = False

        col = gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=0)
        self.builder.get_object("song-view").append_column(col)
        
    #/home/xuanji/Music/Symphony X Complete Discography @ 320 kbps/Symphony X - 2007 - Paradise Lost/05. Paradise Lost.mp3

    def get_icon(self, name):
        theme = gtk.icon_theme_get_default()
        return theme.load_icon(name, 48, 0)
        
    def fill_store(self):
        self.builder.get_object("album-store").clear()
        for fl in os.listdir("/home/xuanji/Music"):
            self.builder.get_object("songs-store").append([fl])
            if not fl[0] == '.': 
                if os.path.isdir(os.path.join("/home/xuanji/Music", fl)):
                    self.builder.get_object("album-store").append([cut(fl,10),self.bn_image, os.path.join("/home/xuanji/Music", fl)])
                else:
                    self.builder.get_object("album-store").append([cut(fl,10),self.an_image, os.path.join("/home/xuanji/Music", fl)])

    def play_pause(self, w):
        if w.get_active():
            filepath = self.builder.get_object("entry").get_text()
            if os.path.isfile(filepath):
                self.player.set_property("uri", "file://" + filepath)
                self.player.set_state(gst.STATE_PLAYING)
                thread.start_new_thread(self.time_callback, ())
                
        else:
            self.player.set_state(gst.STATE_PAUSED)

            
    def rewind_callback(self, w):
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
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
        self.builder.get_object("entry").set_text(s)
        
    def playback_callback(self, w):
        if self.respond_to_slider:
            dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
            new_pos = dur_int * w.get_value() / 100.
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, new_pos)
        
    def time_callback(self):
    
        def convert_ns(t):
            s,ns = divmod(t, 1000000000)
            m,s = divmod(s, 60)

            if m < 60:
                return "%02i:%02i" %(m,s)
            else:
                h,m = divmod(m, 60)
                return "%i:%02i:%02i" %(h,m,s)
    
        while True:
        
            time.sleep(0.2)
            
            try:
                pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
                dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
            except gst.QueryError:
                continue
            
            gtk.gdk.threads_enter()
            self.builder.get_object("time-label").set_text(convert_ns(pos_int) + " / " + convert_ns(dur_int))
            self.respond_to_slider = False
            self.builder.get_object("playback-adjustment").set_value((float(pos_int) / float(dur_int)) * 100.)
            self.respond_to_slider = True
            gtk.gdk.threads_leave()
                        
    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.button.set_label("Start")
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.button.set_label("Start")

app = GTK_Main()
gtk.gdk.threads_init()
gtk.main()
