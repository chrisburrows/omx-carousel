# omx-carousel
Simple carousel player for a Raspberry Pi using omxplayer for HDMI output. Useful to play halloween or Christmas video loops via a projector.

The carousel is a playlist file of videos to be played in sequence. Filenames can be any content supported by omxplayer. 
Local file names are interpreted relative to the --dir argument or the current directory if --dir isn't specified.

The lines in the playlist may be prefixed with either "shift-left" or "shift-right" in which case the video will be cropped by removing 25% off 
the right or left side on order to move the centre of the action left or right. This is a specific customisation to deal with my windows being 
four narrow panes which results in the centre of the content being blocked by the centre window frame.

