#!/usr/bin/env python

__author__ = 'Phil Schwartz'

# gitignore-grabber.py - Grabs gitignore generated files from gitignore.io depending on the programming language arg given

import sys
import os
import urllib

def grab_and_save(url, repoDir):
    if repoDir[len(repoDir)-1] == "/":
        repoDir = repoDir + "/.gitignore"
    else:
        repoDir = repoDir + ".gitignore"

    #grab text and save to repoDir
    urllib.urlretrieve(url, repoDir, reporthook=None, data=None)


s = sys.argv
s.remove(s[0]) #remove script name from args

#help
if s[0] == "-h":
    print "Grab gitignore for the specified language from gitignore.io."
    print "Syntax: User$ python gitignore-grabber.py language repoDirectory"
    sys.exit()


plang = str.lower(s[0]) #grab programming language to grab gitio for
saveDir = str(s[1])
gitio = "http://www.gitignore.io/api/" + str(plang) #append lowercase language name to url

if not os.path.isdir(saveDir):
    print "Repo Path entered is not a directory. Retry!"
    sys.exit(1)

try:
    grab_and_save(gitio, saveDir)
except:
    print "Error downloading and saving .gitignore file..."
    sys.exit(1)

print "File saved to: " + saveDir + "successfully."
sys.exit()