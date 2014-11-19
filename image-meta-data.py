#!/usr/bin/env python
__author__ = 'Phil'

# image-meta-data.py - Get image metadata from file, also specify -gl to retrieve geolocation data of image if it exists

import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import urllib
import os


def getMD(img, out, gl):
    try:
        metaData = {}

        imgFile = Image.open(img)
        print "Getting Meta Data..."
        inf = imgFile._getexif()
        if inf:
            print "Found Meta Data."
            for (tag, value) in inf.items():
                t_name = TAGS.get(tag, tag)
                metaData[t_name] = value
                if not out:
                    print "\t"+ t_name, value

                if out:
                    print "Outputting to file..."
                    with open(out, 'w') as outFile:
                        for (t_name, v) in metaData.items():
                            outFile.write(str(t_name)+"\t"+str(v)+"\n")
        else:
            print "No Meta Data Found."
        try:
            if not gl:
                return
            elif gl:
                lat = [float(x)/float(y) for x, y in inf['GPSInfo'][2]]
                latref = inf['GPSInfo'][1]
                lon = [float(x)/float(y) for x, y in inf['GPSInfo'][4]]
                lonref = inf['GPSInfo'][3]

                lat = lat[0] + lat[1]/60 + lat[2]/3600
                lon = lon[0] + lon[1]/60 + lon[2]/3600
                if latref == 'S':
                    lat = -lat
                if lonref == 'W':
                    lon = -lon

                print "DD GeoLocation Coords: " +lat+", "+lon
        except:
            print "Failed to get DD Geolocation from GPSInfo."

    except:
        print "Failed to get Meta Data."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="image file")
    parser.add_argument("-url", help="url of image file")
    parser.add_argument("--output", "-o", help="dump contents to file")
    parser.add_argument("-gl", action="store_true", help="get dd geolocation of image")
    args = parser.parse_args()

    if args.f:
        getMD(args.f, args.output, args.gl)

    elif args.url:
        urlList = args.url.split(".")
        extension = "." + urlList[len(urlList) - 1]
        tempfile = "mdtemp"+extension
        try:
            urllib.urlretrieve(args.url, filename=tempfile, reporthook=None, data=None)
        except:
            print "Error retrieving image from url."

        if os.path.exists(tempfile):
            getMD(tempfile, args.output, args.gl)
            os.remove(tempfile)

    else:
        print parser.usage

if __name__ == '__main__':
    main()