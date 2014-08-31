TitleLab
========

Automatically generates QLab Titles cues from a text file. This makes it much easier to use QLab for surtitles and
similar uses.

Requirements
------------
Requires Python (tested with 3.4.1) and QLab 3.1. All required python modules are listed in `requirements.txt` and can
be installed thus:

    $ pip install -r requirements.txt

Usage
-----
While running QLab with the cue list in which you want to insert the title cues open:

    $ python titlelab.py [--server qlab_server_address] [--passcode qlab_passcode] file
    
The file should have one title per line. To have a multiline title (e.g. for lyrics in a duet) put the lines which
should appear together on a single line, separated by a slash:

    Valjean: Believe of me what you will/Javert: Men like you can never change
    
The cue list will be set up such that each 'GO' triggers the previous title to stop and the next one to start
simultaneously. To separate this so that the previous title is stopped with one 'GO' and the next title started with
another (leaving the screen blank in between), put a line containing only a period between the two titles:

    One day more!
    .
    INTERMISSION
    
The file should end with a blank line. A brief example of an input file demonstrating the syntax can be found in
`example-input.txt`.

Troubleshooting
---------------
Ensure QLab is running on the machine specified with `--server` (localhost by default). Check that you are using QLab
3.1. Check that OSC control is enabled in QLab, and if QLab is set to use a passcode, be sure to pass the correct one to
this script with `--passcode`. Be sure to have an empty cue list open as this script numbers its cues from 1, which may
conflict with existing cues.

Limitations
-----------
Currently every cue generated will use the default settings for title cues (font, geometry, etc.).  This is not ideal.
The best workaround for now is to use existing batch cue-editing scripts. An example can be found
[here](http://wiki.figure53.com/Script+-+batch+adjust+selected).