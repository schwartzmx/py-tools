#!/usr/bin/env python

# Simple script to Download an Image (Backgrounds) from the Web and Save to /Pictures Folder
# with the specified name.  Instead of the usual download into /Downloads folder w/ a random name, rename,
# move to /Pictures. This makes it one easy commandline script w/ the picture url, and imageNameToSave
# Also specify whether to set image as current background
# http://imgur.com/a/akHsJ -> 575 Desktop Backgrounds no watermarks


__author__ = 'Phil Schwartz'

# python dl-image.py full-url.jpg savedImageName

import os
from os.path import expanduser
import argparse
import sys
import urllib
from Foundation import *


def dl_and_save_image(url, imageName, saveFilePath):
    imageName = os.path.join(saveFilePath, imageName)
    urllib.urlretrieve(url, imageName, reporthook=None, data=None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a specified image and save as a specified name.  Also specify whether to set as current background.")
    parser.add_argument("url", help="Specify a url.")
    parser.add_argument("save_name", help="Enter a file save name. Ex: Background")
    parser.add_argument("-s", help="Set downloaded image to current background.", action="store_true")
    args = parser.parse_args()

    # get home directory and save to Pictures dir
    home = expanduser("~")
    saveFilePath = home + "/Pictures/"

    #find the extension of the picture file and append to the imageName
    urlList = args.url.split(".")
    extension = "." + urlList[len(urlList) - 1]
    imageName = args.save_name + str(extension)

    if args.url and args.save_name:
        try:
            dl_and_save_image(args.url, imageName, saveFilePath)
            print "Success!  File saved to: " + saveFilePath + " as " + imageName
        except:
            print "Error downloading and saving image..."
            sys.exit(1)
    else:
        print parser.usage

    if args.s:
        print "Setting " + saveFilePath+imageName + " to current background..."
        s = NSAppleScript.alloc().initWithSource_("tell app \"Finder\" to set desktop picture to POSIX file \"{}\"".format(saveFilePath+imageName))
        s.executeAndReturnError_(None)
        print "Finished."

    sys.exit()
