#!/usr/bin/env python

import sys, os, thread, time
import pygtk, gtk, gobject
import gtk.glade
import pygst
pygst.require("0.10")
import gst

class GTK_Main:
    
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Audio-Player")
        window.set_default_size(500, -1)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        vbox = gtk.VBox()
        window.add(vbox)
        self.entry = gtk.Entry()
        vbox.pack_start(self.entry, False)
        hbox = gtk.HBox()
        vbox.add(hbox)
        buttonbox = gtk.HButtonBox()
        hbox.pack_start(buttonbox, False)
        
        rewind_button = gtk.Button("Rewind")
        rewind_button.connect("clicked", self.rewind_callback)
        buttonbox.add(rewind_button)
                
        self.button = gtk.Button("Start")
        self.button.connect("clicked", self.start_pause)
        buttonbox.add(self.button)
        
        forward_button = gtk.Button("Forward")
        forward_button.connect("clicked", self.forward_callback)
        buttonbox.add(forward_button)
        
        playback_scale = gtk.HScale()
        #forward_button.connect("clicked", self.forward_callback)
        buttonbox.add(playback_scale)

        
        self.time_label = gtk.Label()
        self.time_label.set_text("00:00 / 00:00")
        hbox.add(self.time_label)
        
        window.show_all()
        
        self.player = gst.element_factory_make("playbin2", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        
    #/home/xuanji/Music/Symphony X Complete Discography @ 320 kbps/Symphony X - 2007 - Paradise Lost/05. Paradise Lost.mp3

    def start_pause(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text()
            if os.path.isfile(filepath):
                self.button.set_label("Pause")
                self.player.set_property("uri", "file://" + filepath)
                self.player.set_state(gst.STATE_PLAYING)
                thread.start_new_thread(self.time_callback, ())
                
        else:
            self.player.set_state(gst.STATE_PAUSED)
            self.button.set_label("Start")

            
    def rewind_callback(self, w):
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        seek_ns = pos_int - (10 * 1000000000)
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)
        
    def forward_callback(self, w):
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        seek_ns = pos_int + (10 * 1000000000)
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)
        
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
            
            pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
            dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
            
            gtk.gdk.threads_enter()
            self.time_label.set_text(convert_ns(pos_int) + " / " + convert_ns(dur_int))
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

GTK_Main()
gtk.gdk.threads_init()
gtk.main()
