#!python

# paste-split.py - Adds Wikipedia bullet points to the start of each line of text in the clipboard

''' should be used for the log parsing script.'''

# TODO: replace pyperclip references with controls to open and read log files.

import pyperclip

text = pyperclip.paste()

#separate lines and add stars

lines = text.split('\n')
for i in range(len(lines)): # loop through all indexes in the "lines" list
    lines[i] = '* ' + lines[i] # add star to each string in "lines" list
text='\n'.join(lines)
pyperclip.copy(text)
