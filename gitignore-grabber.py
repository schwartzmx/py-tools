#!/usr/bin/env python

__author__ = 'Phil Schwartz'

# gitignore-grabber.py - Grabs gitignore generated files from gitignore.io depending on the programming language and/or IDE and/or OS args given

import sys
import os
import urllib


def grab_and_save(url, repoDir):
    if repoDir[len(repoDir) - 1] == "/":
        repoDir = repoDir + ".gitignore"
    else:
        repoDir = repoDir + "/.gitignore"

    # remove old .gitignore if it exists
    if os.path.isfile(repoDir):
        os.remove(repoDir)

    #grab text and save to repoDir
    urllib.urlretrieve(url, repoDir, reporthook=None, data=None)


if __name__ == "__main__":
    s = sys.argv
    s.remove(s[0])  # remove script name from args

    # help
    if str.lower(s[0]) == "-h":
        print "Grab gitignore for the specified language from gitignore.io. Min. of one for first argument."
        print "Syntax: User$ python gitignore-grabber.py language,IDE,OS repoDirectory"
        print "Example:User$ python gitignore-grabber.py Python,PyCharm,OSX /User/ProjectDir/"
        sys.exit()

    try:
        plang = str.lower(s[0])  #grab programming language to grab gitio for
        saveDir = str(s[1])
        gitio = "http://www.gitignore.io/api/" + str(plang)  #append lowercase language name to url
    except:
        print "Invalid arguments, use -h for syntax example"
        sys.exit(1)

    if not os.path.isdir(saveDir):
        print "Repo Path entered is not a directory. Retry!"
        sys.exit(1)

    try:
        grab_and_save(gitio, saveDir)
    except:
        print "Error downloading and saving .gitignore file..."
        sys.exit(1)

    print "File saved to: " + saveDir + " successfully."
    sys.exit()