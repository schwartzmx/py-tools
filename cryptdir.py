#!/usr/bin/env python
__author__ = 'Phil'

# cryptdir.py - Encrypt/Decrypt a single file or entire contents of a directory+subdirectories w/ AES CBC

import sys
import os
import random

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(key, file):
    CHUNK_SIZE = 64 * 1024
    split = file.split('.')
    extension = split[len(split)-1]

    #Skip DS_Store as it causes problems when encrypting/decrypting multiple times
    if extension == "DS_Store":
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


def decrypt(key, file):
    CHUNK_SIZE = 64 * 1024
    split = file.split('.')
    extension = split[len(split)-1]

    #Skip DS_STORE as it causes problems when encrypting/decrypting multiple times
    if extension == "DS_Store":
        return


    outputFile = "temp."+extension

    with open(file, 'rb') as infile:
        fileSize = long(infile.read(16))
        #print fileSize
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


def get_key(password):
    hasher = SHA256.new(password)
    return hasher.digest()


def main():
    s = sys.argv
    # s.remove(s[0]) #remove script name

    #Help
    if str.lower(s[1]) == "-h":
        print "Encrypt/Decrypt a File or Entire Directory."
        print "Encrypt: User$ python cryptdir.py -e"
        print "Decrypt: User$ python cryptdir.py -d"

    #Encrypt
    elif str.lower(s[1]) == "-e":
        file_or_directory = raw_input("Enter a directory or file name: ")
        if not os.path.isdir(file_or_directory):
            if os.path.isfile(file_or_directory):
                #print "-->File"  #test
                print "WARNING: Ensure that you write down and remember this for decryption purposes!"
                password = raw_input("Enter a password: ")
                encrypt(get_key(password), file_or_directory)
                print "Encryption completed."
            else:
                print "Error: File entered does not exist! Exiting..."
                sys.exit(1)

        else:  #is a directory
            #print "-->Directory"  #test
            if os.path.isdir(file_or_directory):
                print "WARNING: Ensure that you write down and remember this for decryption purposes!"
                password = raw_input("Enter a password: ")
                print "Encrypting..."
                for subdir, dirs, files in os.walk(file_or_directory):
                    if subdir:
                        print "   >"+subdir
                        for file in files:
                            print "     --"+file
                            encrypt(get_key(password), os.path.join(file_or_directory, subdir, file))

                print "Encryption completed."

            else:
                print "Error: File or Directory does not exist! Exiting..."
                sys.exit(1)

    #Decrypt
    elif str.lower(s[1]) == "-d":
        file_or_directory = raw_input("Enter a directory or file name: ")
        if not os.path.isdir(file_or_directory):
            if os.path.isfile(file_or_directory):
                #print "-->File"  #test
                print "WARNING: Ensure that you enter in the exact password that you encrypted with!"
                password = raw_input("Enter password: ")
                decrypt(get_key(password), file_or_directory)
                print "Decryption completed."
            else:
                print "Error: File entered does not exist! Exiting..."
                sys.exit(1)

        else:  #is a directory
            #print "-->Directory"  #test
            if os.path.isdir(file_or_directory):
                print "WARNING: Ensure that you enter in the exact password that you encrypted with!"
                password = raw_input("Enter password: ")
                print "Decrypting..."
                for subdir, dirs, files in os.walk(file_or_directory):
                    if subdir:
                        print "   >"+subdir
                        for file in files:
                            print "     --"+file
                            decrypt(get_key(password), os.path.join(file_or_directory, subdir, file))

                print "Decryption completed."

            else:
                print "Error: File or Directory does not exist! Exiting..."
                sys.exit(1)

    #None
    else:
        print "No option entered! Exiting..."
        sys.exit(1)

    sys.exit()


if __name__ == "__main__":
    main()

