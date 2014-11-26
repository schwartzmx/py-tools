#!/usr/bin/env python

# Simple script to Download an Image (Backgrounds) from the Web and Save to /Pictures Folder
# with the specified name.  Instead of the usual download into /Downloads folder w/ a random name, rename,
# move to /Pictures. This makes it one easy commandline script w/ the
# picture url, and imageNameToSave

__author__ = 'Phil Schwartz'

# python dl-image.py full-url.jpg savedImageName

import os
from os.path import expanduser
import sys
import urllib


def dl_and_save_image(url, imageName, saveFilePath):
    imageName = os.path.join(saveFilePath, imageName)
    urllib.urlretrieve(url, imageName, reporthook=None, data=None)


if __name__ == "__main__":
    s = sys.argv
    s.remove(s[0])  # remove script from args

    if s[0] == "-h":
        print "Download an image from the internet into User Home Pictures Folder."
        print "Syntax: User$ python dl-image.py URL ImageNameToSave(No extension)"
        sys.exit()

    # url and imageNameToSave from commandLine Args
    try:
        url = str(s[0])
        imageName = str(s[1])
    except:
        print "Invalid arguments, use -h for syntax example"
        sys.exit(1)

    # get home directory and save to Pictures dir
    home = expanduser("~")
    saveFilePath = home + "/Pictures/"

    # find the extension of the picture file and append to the imageName
    urlList = url.split(".")
    extension = "." + urlList[len(urlList) - 1]
    imageName = imageName + str(extension)

    try:
        dl_and_save_image(url, imageName, saveFilePath)
    except:
        print "Error downloading and saving image..."
        sys.exit(1)

    print "Success!  File saved to: " + saveFilePath + " as " + imageName
    sys.exit()
