#!/usr/bin/python3

import argparse
import os.path
import re
import subprocess
import sys

omxplayer_args = "omxplayer -b -o both --no-osd --no-keys --layer 1 {crop} {file}"

def file_exists(file):
    return os.path.isfile(file)

def get_dimensions(file):
    '''Get the video dimensions from the file'''
    if file_exists(file):
        result = subprocess.run(["omxplayer", "--info", file], capture_output=True)
        dimensions = re.search(' (\d+)x(\d+)[ ,]', str(result.stderr))
        if dimensions is not None:
            width = int(dimensions.group(1))
            height = int(dimensions.group(2))
            return(width, height)
    return (None, None)

def create_carousel(videos):
    '''Build list of OMXplayer commands to play the carousel'''

    carousel = []
    for video in videos:
        video = video.strip()
        if len(video) == 0 or video.startswith("#"):
          continue
        crop=""
        parts=video.split()
        if "shift-" in parts[0]:
            video = parts[1]
            (width, height) = get_dimensions(video)
            if width is not None:
                if "-right" in parts[0]:
                    crop_x2 = int(width * 0.75)
                    crop = "--crop 0,0,{x2},{y2}".format(x2=crop_x2, y2=height)

                if "-left" in parts[0]:
                    crop_x1 = int(width * 0.25)
                    crop = "--crop {x1},{y1},{x2},{y2}".format(x1=crop_x1, y1=0, x2=width, y2=height)

        if file_exists(parts[-1]):
            print("Adding {file}".format(file=parts[-1]))
            carousel.append(omxplayer_args.format(file=video, crop=crop))

    return carousel

parser = argparse.ArgumentParser(description='OMX Carousel Player')
parser.add_argument('--dir',      dest="directory", default="./",       help='base directory for the playlist')
parser.add_argument('--playlist', dest='playlist',  default="playlist", help='Name of the playlist file')

args = parser.parse_args()

try:
    subprocess.run("tput clear > /dev/tty1", shell=True)
    os.chdir(args.directory)

    playlist = open(args.playlist, 'r')
    videos = playlist.readlines();
    playlist.close()

    carousel = create_carousel(videos)

    print("Playing carousel")
    while True:

        for video in carousel:
            print(video)
            subprocess.run(video, shell=True, capture_output=True)
            subprocess.run("tput clear > /dev/tty1", shell=True)

except KeyboardInterrupt:
    pass
