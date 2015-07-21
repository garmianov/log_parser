#!python

# paste-split.py - Adds Wikipedia bullet points to the start of each line of text in the clipboard

# ''' should be used for the log parsing script.'''

# TODO: replace pyperclip references with controls to open and read log files.

# import pyperclip
import os
import sys
import pprint

found=[]
lines = []
text = []
flist = sys.argv[1] # receives the target directory from the CLI argument
flist1 = os.listdir(flist)
os.chdir(sys.argv[1]) # Changes the present working directory to the one from the CLI argument

def searchargv(terms, flist1, found):
    with open("sresults", "w") as ffound:
        for fname in flist1:
            if 'health' not in str(fname):
                with open(fname, "r", encoding="ISO-8859-1") as file:
                    print('\r', "File name is ", fname)
                    for line in file:
                        if terms in line:
                            ffound.write(line)
                            found.append(line) # add the found lines to the FOUND list
    ffound.close()
    text = '\n'.join(found)
    print(text)

def searchterms(terms, flist1, found):
    with open("sresults", "w") as ffound:
        for fname in flist1:
            if 'health' not in str(fname):
                with open(fname, "r", encoding="ISO-8859-1") as file:
                    print('\r', "File name is ", fname)
                    for line in file:
                        for y in terms:
                            if y in line:
                                ffound.write(line)
                                found.append(line) # add the found lines to the FOUND list
    ffound.close()
    text = '\n'.join(found)
    print(text)
    
if len(sys.argv) > 2:
    terms = sys.argv[2]
    searchargv(terms, flist1, found)
else:
    terms = ['watchdog', 'Unhandled fault', 'Failed to authenticate', 'Link is', 'Ping overdue','ValidateAndUpdateStreams:Writing Configuration', 'Started at', 'CameraDescriptor:', 'Current boot version:','rebootSystem', 'set resolution to', 'Decode error', 'Overdue', 'Video Present', 'Video Lost','Timeout during', 'Connecting to rtsp:', 'RTSP \[[0-3]\]', 'Fps', 'Bitrate']
    searchterms(terms, flist1, found)
# text = pyperclip.paste()





# TODO decide what to do with the output = format it better, output it to a file?
# TODO find a way to page the output on the screen
# pyperclip.copy(text)