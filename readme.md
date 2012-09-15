Filesystem Music Player
=======================

![screenshot](https://raw.github.com/zodiac/fsm/master/screenshot.jpg)

fsm organizes your music by folders instead of the usual jumble of albums, artists etc. Perfect for people (like me!) whose music does not naturally follow the album/artist organization that most music players rely on. Also takes album art from associated folder.

By default fsm plays songs from ~/Music. Edit fsm.py to change it to your music directory of choice.

fsm is written in python and uses the GTK toolkit for its gui and the GStreamer python bindings for audio playback. If your python can successfully import the gtk and gst modules it should work. fsm was developed and tested on linux and has not yet been tested on windows.

Known Bugs
----------

reproccesses all album art on startup, which takse a very long time
