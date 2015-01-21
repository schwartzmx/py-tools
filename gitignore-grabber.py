#!/usr/bin/env python

__author__ = 'Phil Schwartz'

# gitignore-grabber.py - Grabs gitignore generated files from gitignore.io depending on the programming language
# and/or IDE and/or OS args given (comma separated).

# python gitignore-grabber.py language,IDE,OS repoDirectory

import sys
import os
import urllib
import argparse

def grab_and_save(url, repoDir):
    if repoDir[len(repoDir) - 1] == "/":
        repoDir = repoDir + ".gitignore"
    else:
        repoDir = repoDir + "/.gitignore"
    # remove old .gitignore if it exists
    if os.path.isfile(repoDir):
        os.remove(repoDir)
    # grab text and save to repoDir
    urllib.urlretrieve(url, repoDir, reporthook=None, data=None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grab gitignore files from gitignore.io and save to the specified directory.", usage="Usage example: ./gitignore-grabber.py -a OSX Java Eclipse -d home/User/Repo")
    parser.add_argument("-a", "--args", help="Specify programming language(s), OS(s), or others.", action="store")
    parser.add_argument("-r", "--repo", help="Enter the path to save .gitignore file to.", action="store")
    args = parser.parse_args()

    if args.args and args.repo:
        try:
            plang = args.args.replace(' ', ',')  # grab programming language to grab gitio for
            saveDir = args.repo
            # append lowercase language name to url
            gitio = "http://www.gitignore.io/api/" + str(plang)
            if not os.path.isdir(saveDir):
                print "Repo Path entered is not a directory. Retry!"
                sys.exit(1)
            try:
                grab_and_save(gitio, saveDir)
            except:
                print "Error downloading and saving .gitignore file..."
                sys.exit(1)
            print "File saved to: " + saveDir + " successfully."
        except:
            print "Invalid arguments, use -h for syntax example"
    else:
        print parser.usage