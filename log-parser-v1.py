#!python

# paste-split.py - Adds Wikipedia bullet points to the start of each line of text in the clipboard

# ''' should be used for the log parsing script.'''

# TODO: replace pyperclip references with controls to open and read log files.

# import pyperclip
import os
import sys
import pprint


terms = ['watchdog', 'Unhandled fault', 'Failed to authenticate', 'Link is', 'Ping overdue',
         'ValidateAndUpdateStreams:Writing Configuration', 'Started at', 'CameraDescriptor:', 'Current boot version:',
         'rebootSystem', 'set resolution to', 'Decode error', 'Overdue', 'Video Present', 'Video Lost',
         'Timeout during', 'Connecting to rtsp:', 'RTSP \[[0-3]\]', 'Fps', 'Bitrate', 'ERROR', 'error']

# text = pyperclip.paste()
found=[]
lines = []
# text = []
i = 0
flist = sys.argv[1] # receives the target directory from the CLI argument
flist1 = os.listdir(flist)
os.chdir(sys.argv[1]) # Changes the present working directory to the one from the CLI argument
for fname in flist1:
    if 'health' not in str(fname):
        with open(fname, "r", encoding="ISO-8859-1") as file:
            print('\r', "File name is ", fname)
            # wait = input('waiting for ENTER')
            # lines = file.read()
            # text = file.read()
            # lines = text.split('\r')
            # lines = text
            for line in file:
#            for i in range(len(lines)):  # loop through all indexes in the "lines" list
                # lines = line.split('\r')
                for y in terms:
        #            y = str(y)
        #            y = y.lower()
                    if y in line:
                        found.append(line) # add the found lines to the FOUND list
                        # print(line)
#                i = i + 1

text = '\n'.join(found)
pprint.pprint(text)
# print(text)
# TODO decide what to do with the output = format it better, output it to a file?
# TODO find a way to page the output on the screen


# pyperclip.copy(text)
