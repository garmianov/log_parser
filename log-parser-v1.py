#!python

# paste-split.py - Adds Wikipedia bullet points to the start of each line of text in the clipboard

# ''' should be used for the log parsing script.'''

# TODO: replace pyperclip references with controls to open and read log files.

# import pyperclip
import os
import sys
import pprint


# terms = 'mon.log'w
terms = ['watchdog', 'Unhandled fault', 'Failed to authenticate', 'Link is', 'Ping overdue',
         'ValidateAndUpdateStreams:Writing Configuration', 'Started at', 'CameraDescriptor:', 'Current boot version:',
         'rebootSystem', 'set resolution to', 'Decode error', 'Overdue', 'Video Present', 'Video Lost',
         'Timeout during', 'Connecting to rtsp:', 'RTSP \[[0-3]\]', 'Fps', 'Bitrate', 'ERROR', 'error']

# text = pyperclip.paste()

# for arg in sys.argv: # read the argument from the command line
#     print(arg)
found=[]
lines = []
text = []

flist = sys.argv[1] # receives the target directory from the CLI argument
# print("flsit is ", flist)
# flist = os.system(sys.argv[2])
flist1 = os.listdir(flist) # Changes the present working directory to the one from the CLI argument
# print("Argument is ", flist1)
# wait = input('waiting for ENTER')
os.chdir(sys.argv[1])
for fname in flist1:
    file = open(fname, "r")
    # separate lines
    lines = file.readlines()
    # text = file.read()
    # lines = text.split('\n')
    # print("THIS IS THE FILE: ", lines)

    for i in range(len(lines)):  # loop through all indexes in the "lines" list
        for y in terms:
#            y = str(y)
#            y = y.lower()
            if y in str(lines[i]):
                found.append(lines[i]) # add the found lines to the FOUND list
                # pprint.pprint(lines[i])
                # else:
                #     lines[i] = '* ' + lines[i] # add star to each string in "lines" list
#    text = '\r '.join(found)
    pprint.pprint(found)
    file.close()
# TODO decide what to do with the output = format it better, output it to a file?
# TODO find a way to page the output on the screen

# pyperclip.copy(text)
