Filesystem Music Player
=======================

fsm organizes your music by folders instead of the usual jumble of albums, artists etc. Perfect for people (like me!) whose music does not naturally follow the album/artist organization that most music players rely on. Also takes album art from associated folder.

![screenshot](https://raw.github.com/zodiac/fsm/master/screenshot.jpg)

Every thumbnail in the above screenshot corresponds to a folder in the music directory.

Installation
------------

Clone this repository, cd into it and run 

```python ./fsm.py```

By default fsm plays songs from ~/Music. Edit fsm.py to change it to your music directory of choice.

Requirements
------------

fsm is written in python and uses the GTK toolkit for its gui and the GStreamer python bindings for audio playback. If your python can successfully import the gtk and gst modules it should work. fsm was developed and tested on linux and should work on windows; if you do manage to get it to work (or encounter problems), please tell me!

Known Bugs
----------

reproccesses all album art on startup, which takse a very long time
