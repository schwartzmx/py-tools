#!/usr/bin/env python

# Download an Image (Backgrounds) from the web to Home Pictures Folder

__author__ = 'Phil Schwartz'

# python dl-image.py full-url.jpg savedImageName

import os
from os.path import expanduser
import sys
import urllib


def dl_and_save_image(url, imageName, saveFilePath):
	imageName = os.path.join(saveFilePath, imageName)
	urllib.urlretrieve(url, imageName, reporthook=None, data=None)


s = sys.argv
s.remove(s[0]) #remove script from args

if s[0] == "-h":
	print "Download an image from the internet into User Home Pictures Folder."
	print "Syntax: User$ python dl-image.py URL ImageNameToSave"
	sys.exit()

#url and imageNameToSave from commandLine Args
url = str(s[0])
imageName = str(s[1])

#get home directory and save to Pictures dir
home = expanduser("~")
saveFilePath = home + "/Pictures/"

#find the extension of the picture file and append to the imageName
urlList = url.split(".")
extension = "." + urlList[len(urlList)-1]
imageName = imageName + str(extension)

try:
	dl_and_save_image(url, imageName, saveFilePath)
except:
	print "Error downloading and saving image..."
	sys.exit(1)

print "Success!  File saved to: " + saveFilePath + " as " + imageName
sys.exit()