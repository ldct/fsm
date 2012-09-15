Filesystem Music Player
=======================

fsm organizes your music by the folders the audio files actually reside in on disk. Perfect for people (like me!) whose music does not naturally follow the album/artist organization that most music players rely on. Also takes album art from associated folder.

![screenshot](https://raw.github.com/zodiac/fsm/master/screenshot.jpg)

Every thumbnail in the above screenshot corresponds to a folder in the music directory.

Installation
------------

Clone this repository, ```cd``` into it and run 

```python ./fsm.py```

By default fsm plays songs from ~/Music. Edit fsm.py to change it to your music directory of choice.

Requirements
------------

fsm is written in python and uses the GTK toolkit for its gui and the GStreamer python bindings for audio playback. If your python can successfully import the gtk and gst modules it should work. fsm was developed and tested on linux and should work on windows; if you do manage to get it to work (or encounter problems), please tell me!

Why?
----

Many music players assume that songs should be grouped together according to albums and that the same album will have the same artists. While this might be fine for most music it fails quite badly for audio files that don't fit into this mould. Use cases include

- Compilation albums
- Songs where the artist field lists individual band members involved
- Classical music
- Files with broken metadata - "Unknown Artist"
- Individual ~~downloads~~ purchases which result in singleton album entries

While there are workarounds for the above problems at some point one wonders if the album/artist categorization was really worth that much trouble; hence was fsm born. Another advantage is that you can control exactly how you want your music to be grouped and displayed by moving the underlying files around. As an example in the above screenshot I have a folder of songs by a single artist (Paul Okenfold), a discography folder (Symphony X), as well as more traditional albums.

Known Bugs
----------

reproccesses all album art on startup, which takse a very long time
