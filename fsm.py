#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class GTK_Main:
	
	def __init__(self):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Audio-Player")
		window.set_default_size(300, -1)
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		self.entry = gtk.Entry()
		vbox.pack_start(self.entry, False, True)
		self.button = gtk.Button("Start")
		self.button.connect("clicked", self.start_stop)
		vbox.add(self.button)
		window.show_all()
		
		self.player = gst.element_factory_make("playbin2", "player")
		fakesink = gst.element_factory_make("fakesink", "fakesink")
		self.player.set_property("video-sink", fakesink)
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_message)
		
	def start_stop(self, w):
		if self.button.get_label() == "Start":
			filepath = self.entry.get_text()
			if os.path.isfile(filepath):
				self.button.set_label("Stop")
				self.player.set_property("uri", "file://" + filepath)
				self.player.set_state(gst.STATE_PLAYING)
		else:
			self.player.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
						
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
