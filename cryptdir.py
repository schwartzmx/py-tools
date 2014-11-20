#!/usr/bin/env python
__author__ = 'Phil'

# cryptdir.py - Encrypt/Decrypt a single file or entire contents of a directory+subdirectories w/ AES CBC

import sys
import os
import random
import argparse

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(key, file):
    if key != 1:
        CHUNK_SIZE = 64 * 1024
        split = file.split('.')
        extension = split[len(split)-1]

        #Skip DS_Store as it causes problems when encrypting/decrypting multiple times
        if extension == "DS_Store" or extension == "cd":
            return

        outputFile = "temp."+extension
        fileSize = str(os.path.getsize(file)).zfill(16)  # fill left side of string with 0s
        IV = ''
        #print fileSize

        for i in range(16):
            IV += chr(random.randint(0, 0xFF))

        encryptor = AES.new(key, AES.MODE_CBC, IV)  # chained cypher block

        # open and read file in binary
        with open(file, 'rb') as infile:
            #open and write file in binary
            with open(outputFile, 'wb') as outfile:
                outfile.write(fileSize)
                outfile.write(IV)

                while True:
                    chunk = infile.read(CHUNK_SIZE)

                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - (len(chunk) % 16))

                    outfile.write(encryptor.encrypt(chunk))

            #copy tmp file to original file name
            with open(outputFile, 'rb') as infile:

                with open(file, 'wb') as outfile:
                    while True:
                        chunk = infile.read(CHUNK_SIZE)

                        if len(chunk) == 0:
                           break

                        outfile.write(chunk)

            #remove tmp file
            os.remove(outputFile)
    else:
        print "Unable to Encrypt."


def decrypt(key, file):
    if key != 1:
        CHUNK_SIZE = 64 * 1024
        split = file.split('.')
        extension = split[len(split)-1]

        #Skip DS_STORE as it causes problems when encrypting/decrypting multiple times
        if extension == "DS_Store" or extension == "cd":
            return


        outputFile = "temp."+extension

        with open(file, 'rb') as infile:
            fileSize = long(infile.read(16))

            IV = infile.read(16)

            decryptor = AES.new(key, AES.MODE_CBC, IV)

            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(CHUNK_SIZE)

                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - (len(chunk) % 16))

                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(fileSize)  # truncates all padding added at encryption

            #copy tmp file to original file name
            with open(outputFile, 'rb') as infile:

                with open(file, 'wb') as outfile:
                    while True:
                        chunk = infile.read(CHUNK_SIZE)

                        if len(chunk) == 0:
                            break

                        outfile.write(chunk)

                    #fileSize = os.path.getsize(file)
                    outfile.truncate(fileSize)

            #remove tmp file
            os.remove(outputFile)
    else:
        print "Unable to Decrypt."


def get_key(password, path, eod):
    hasher = SHA256.new(password)

    if eod == "encrypt" and os.path.exists(path+'.cd'):
        os.remove(path+'.cd')


    compare = pass_cmp(password, path)

    if compare == True:
        return hasher.digest()
    else:
        print "Invalid Password entered!"
        sys.exit(1)

def pass_cmp(password, path):
    if path[:-1] != '/':
        path = path+'/'

    if os.path.exists(path+'.cd'):
        with open(path+'.cd', 'r') as efile:
            p = efile.readline()
            if password == p:
                return True
            else:
                return False
    else:
        with open(path+'.cd', 'w') as nfile:
            nfile.write(str(password))
            nfile.close()

        return True


def main():
    parser = argparse.ArgumentParser(description="Encrypt/Decrypt a single file or entire directory (along w/ subdirectories) using AES Chained Block Cypher."
        "\n Specifics: Uses a '.cd' file, within the directory or file directory to log your password and compare for decryption purposes. This could be later changed.")
    parser.add_argument("file", help="file or directory")
    parser.add_argument("-e", action="store_true", help="encrypt")
    parser.add_argument("-d", action="store_true", help="decrypt")
    args = parser.parse_args()

    if args.file:
        fpath = args.file.split('/')
        apath = fpath[:-1]
        path = ''
        i = 0
        while i < len(apath):
            path = path + apath[i]+'/'
            i += 1

    #Encrypt
    if args.e:
        if not os.path.isdir(args.file):
            if os.path.isfile(args.file):
                #print "-->File"  #test
                print "WARNING: Ensure that you write down and remember this for decryption purposes!"
                password = raw_input("Enter a password: ")
                encrypt(get_key(password, path, 'encrypt'), args.file)
                print "Encryption completed."
            else:
                print "Error: File entered does not exist! Exiting..."


        else:  #is a directory
            #print "-->Directory"  #test
            if os.path.isdir(args.file):
                print "WARNING: Ensure that you write down and remember this for decryption purposes!"
                password = raw_input("Enter a password: ")
                print "Encrypting..."
                for subdir, dirs, files in os.walk(args.file):
                    if subdir:
                        print "   >"+subdir
                        for file in files:
                            print "     --"+file
                            encrypt(get_key(password, args.file, 'encrypt'), os.path.join(args.file, subdir, file))
                print "Encryption completed."

            else:
                print "Error: File or Directory does not exist! Exiting..."


    #Decrypt
    elif args.d:
        if not os.path.isdir(args.file):
            if os.path.isfile(args.file):
                print "WARNING: Ensure that you enter in the exact password that you encrypted with!"
                password = raw_input("Enter password: ")
                decrypt(get_key(password, path, False), args.file)
                print "Decryption completed."
            else:
                print "Error: File entered does not exist! Exiting..."


        else:  #is a directory
            if os.path.isdir(args.file):
                print "WARNING: Ensure that you enter in the exact password that you encrypted with!"
                password = raw_input("Enter password: ")
                print "Decrypting..."
                for subdir, dirs, files in os.walk(args.file):
                    if subdir:
                        print "   >"+subdir
                        for file in files:
                            print "     --"+file
                            decrypt(get_key(password, args.file, True), os.path.join(args.file, subdir, file))

                print "Decryption completed."

            else:
                print "Error: File or Directory does not exist! Exiting..."

    else:
        print parser.usage





if __name__ == "__main__":
    main()

