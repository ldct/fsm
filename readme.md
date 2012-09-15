Filesystem Music Player
=======================

fsm organizes your music by folders instead of the usual jumble of albums, artists etc. Perfect for people (like me!) whose music does not naturally follow the album/artist organization that most music players rely on. Also takes album art from associated folder.

![screenshot](https://raw.github.com/zodiac/fsm/master/screenshot.jpg)

Every thumbnail in the above screenshot corresponds to a folder in the music directory.

Installation and Usage
----------------------

Clone this repository, cd into it and run 

```python ./fsm.py```

By default fsm plays songs from ~/Music. Edit fsm.py to change it to your music directory of choice.

fsm is written in python andThank you for signing up for Algorithms: Design and Analysis, Part 2!  Part 2 of Algorithms: Design and Analysis will be action-packed with great topics: the greedy algorithm design paradigm, with applications to computing good network backbones and good codes for data compression; the tricky yet widely applicable dynamic programming algorithm design paradigm, with applications to routing in the Internet and sequencing genome fragments; NP-completeness and the famous “P vs. NP” problem and what they mean for the algorithm designer; and strategies for dealing with hard (i.e., NP-complete) problems , including the design and analysis of heuristics.   We expect the class to be offered in October of 2012. We'll notify you again when the class starts. uses the GTK toolkit for its gui and the GStreamer python bindings for audio playback. If your python can successfully import the gtk and gst modules it should work. fsm was developed and tested on linux and should work on windows; if you do manage to get it to work (or encounter problems), please tell me!

Known Bugs
----------

reproccesses all album art on startup, which takse a very long time
