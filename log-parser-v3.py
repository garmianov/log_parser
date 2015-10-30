#!/bin/python3

# paste-split.py - Adds Wikipedia bullet points to the start of each line of text in the clipboard

# ''' should be used for the log parsing script.'''

# import pyperclip
import os
import sys
import pprint
import datetime
import collections
import operator

'''defining variables'''
found = []
lines = []
text = []
rtsp_found = []
datedic = {}
datedic1 = {}
exception_found = []

# flist = sys.argv[1] # receives the target directory from the CLI argument

os.chdir(os.path.abspath(sys.argv[1]))  # Changes the present working directory to the one from the CLI argument

if os.path.exists("./sresults"):  # check whether sresults exists and delete it so it is not mixing results
    os.remove("./sresults")
    print("Removing sresults file")

if os.path.exists("./reboots.txt"):  # check whether sresults exists and delete it so it is not mixing results
    os.remove("./reboots.txt")
    print("Removing reboots.txt file")

if os.path.exists("./exceptions.txt"):  # check whether sresults exists and delete it so it is not mixing results
    os.remove("./exceptions.txt")
    print("Removing exceptions.txt file")

if os.path.exists("./rtsp_connections.txt"):  # check whether sresults exists and delete it so it is not mixing results
    os.remove("./rtsp_connections.txt")
    print("Removing rtsp_connections.txt file")

''' Creates list of files in the directory form argv[1]'''
flist1 = os.listdir(sys.argv[1])

''' Dictionary to be used for log parsing (not sure yet how)'''
DIRECTIVE_MAP = {
                 '%t': 'time_stamp',
                 '%h': 'host_name',
                 '%m': 'message',
                }

''' Main function which at the moment calls pre-defined searches'''
def main():
    reboots(flist1, found)
    connect_rtsp(flist1, rtsp_found, datedic, datedic1)
    # exception(flist1, exception_found, datedic)
    # if len(sys.argv) > 2:
      # terms = sys.argv[2]
      # searchargv(terms, flist1, found)
    # else:
      # terms = ['watchdog', 'Unhandled fault', 'Failed to authenticate', 'Link is', 'Ping overdue','ValidateAndUpdateStreams:Writing Configuration', 'Started at', 'CameraDescriptor:', 'Current boot version:','rebootSystem', 'set resolution to', 'Decode error', 'Overdue', 'Video Present', 'Video Lost','Timeout during', 'Connecting to rtsp:', 'RTSP \[[0-3]\]', 'Fps', 'Bitrate']
      # searchterms(terms, flist1, found)
    # text = pyperclip.paste()

''' Search using term from the command line arguments'''
def searchargv(terms, flist1, found):
    with open("sresults", "w") as ffound:
        for fname in flist1:
            if 'health' not in str(fname):
                with open(fname, "r", encoding="ISO-8859-1") as file:
                    print('\r', "File name is ", fname)
                    for line in file:
                        if terms in line:
                            ffound.write(line)
                            found.append(line)  # add the found lines to the FOUND list
    ffound.close()
    text = '\n'.join(found)
    print(text)


''' Search using terms from the terms variable above '''
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
                                found.append(line)  # add the found lines to the FOUND list
    ffound.close()
    text = '\n'.join(found)
    print(text)

''' Search for reboots entries '''
def reboots(flist1, found):
    # date_line = []
    date_value = []
    with open("reboots.txt", "w") as ffound:
        for fname in flist1:
            if 'health' not in str(fname):
                with open(fname, "r", encoding="ISO-8859-1") as file:
                    #   print('\r', "File name is ", fname)
                    for line in file:
                        if "Restart" in line:
                            ffound.write(line)
                            date_line = line.split(' ')
                            date_v1 = (date_line[0] + " " + date_line[1])
                            if date_v1 not in date_value:
                                date_value.append(date_v1)
                                found.append(line)  # add the found lines to the FOUND list
                            #   print("Rialto rebooted on the following dates and times: ", date_v1)
    print("found ", len(found), "reboots in the log files")
    date_value.sort()
    ffound.close()
    text = '\n'.join(found)
    #    print(len(text))
    #    print(text)
    #    date_v = '\n'.join(date_value)
    for i in range(len(date_value)):
        print("date and time of the reboot: ", date_value[i])
    print(len(date_value))

'''Search for rtsp connections'''
def connect_rtsp(flist1, rtsp_found, datedic, datedic1):
    timedict = {}
    date_value = [] #using to hold date time value from the log lines.
    with open("rtsp_connections.txt", "w") as ffound1: #open file to hold the found log lines
        for fname in flist1: #next three lines open the log files to be searched. Exlude health_mon logs
            if 'health' not in str(fname):
                with open(fname, "r", encoding="ISO-8859-1") as file:
                    #   print('\r', "File name is ", fname)
                    for line in file:
                        if "connecting to rtsp" in str.lower(line):
                            ffound1.write(line)
                            date_line = line.split(' ') #next four lines extract the date and time from the log line.
                            date_v1 = (date_line[0] + " " + date_line[1])
                            date_time = line.split(' ')[1]
                            date_date = line.split(' ')[0]
                            if date_v1 not in date_value:
                                date_value.append(date_v1)
                                rtsp_found.append(line)  # add the rtsp_found lines to the rtsp_found list
                                '''
                                add the line with time stamp (date_time) and the log line (date_line[-1]) as a sub dictionary, timestamp will be the key, date (date_date) is the key for the main dict
                                '''
                                datedic1.setdefault(date_date, {})[date_time] = date_line[-1]
                                c = collections.Counter(datedic1) #not sure what I am going to use this for

    print("found ", len(rtsp_found), " rtsp connections in the log files")
    if len(rtsp_found) == 0:
        print("This must be an Analog Rialto", '\n')
    date_value.sort()
    ffound1.close()
    print(len(date_value))
    '''
    The part below is analysing the content of the datedict1 for various correlations
    '''
    key_dict1 = datedic1.keys()                                         # Isolate the dates of the reconnects
    for n in sorted(key_dict1):                                         #iterate through the dict by dates so we can investigate each day in turn
        time = list(sorted(datedic1[n].keys()))                         #find the times of the reconnects within a given day
        lentime = len(time)                                             # how many times in a day the reconnect occured. counts the times stamps that are shown as key of the sub-dictionary
        timedict.setdefault(n, []).append(lentime)                      # Created timedict dictionary to hold the day as key and the number of re-connects as values.
    result = max(timedict.items(), key=operator.itemgetter(1))[0]       # Finds the day with most re-connects
    resultmin = min(timedict.items(), key=operator.itemgetter(1))[0]    #supposetly finds the day with least re-connect but not clear what's the procedure if two days have the same number of reconnects
    x = timedict[result]
    y = timedict[resultmin]
    print("Most reconnects -", x[0], "happened on", result)
    print("Least reconnects -", y[0], "happened on", resultmin)
  
   # input('Press any key to continue')
    '''
    for k, v in sorted(datedic1.items()):
        #pprint.pprint(k)
        #pprint.pprint(v)
        #for time, memo in sorted(v.items()):
         #  print(k, "+++>", time, "=>", memo)
        n = 0
        for time in sorted(v.keys()):
           n += 1
    '''
    #pprint.pprint(datedic1)
    #    print(n)
    #yield datedic1
    #pprint.pprint(t)
    '''
    for key in sorted(datedic1):
        print(key, '=> ',datedic1[key])
    '''

'''Search for exceptions'''
def exception(flist1, exception_found, datedic):
    # date_line = []
    date_value = []
    with open("exceptions.txt", "w") as ffound1:
        for fname in flist1:
            if 'health' not in str(fname):
                with open(fname, "r", encoding="ISO-8859-1") as file:
                    #   print('\r', "File name is ", fname)
                    for line in file:
                        if "exception" in str.lower(line):
                            ffound1.write(line)
                            # date_line = line.split(' ')
                            # date_v1 = (date_line[0] + " " + date_line[1])
                            if line not in date_value:
                                date_value.append(line)
                                exception_found.append(line)  # add the exception_found lines to the exception_found list
                              #  datedic.setdefault(date_v1, []).append(date_line[-1])
                              #  datedic.setdefault('logdate', []).append(date_v1)
                              #  datedic.setdefault('logtime', []).append(date_line[1])
#                        else:
#                            print("No RTSP connection requests. This is Analog Rialto")
    print("found ", len(exception_found), " Exceptions in the log files")
    date_value.sort()
    ffound1.close()
    # text = '\n'.join(exception_found)
    #    print(len(text))
    #    print(text)
    #    date_v = '\n'.join(date_value)
    for i in range(len(date_value)):
        print("date and time of the exception: ", date_value[i])
    print(len(date_value))
    # pprint.pprint(datedic)
    # yield datedic

'''
class LogLineGenerator:
    def __init__(self, log_format=None, flist1):
        #Standard log format "%t, %h:, %m
        if not log_format:
            self.format_string = '%t %h %m'
        else:
            self.format_string = log_format
        self.log_file = flist1
#        self.re_tsquote = re.compile(r'(\[|\])')
        self.field_list = []
        for directive in self.format_string.split(''):
            self.field_list.append(DIRRECTIVE_MAP[directive])
#    def _quote_translator(self, file_name):
#        with open(fname, "r", encoding="ISO-8859-1") as file:
#            for line in file:
#            yield self.re_tsquote.sub('"', line)
'''

'''call the main function'''
if __name__ == "__main__": main()

'''
TODO How to group lines by time stamp?
TODO Investigate the time between the Rialto lost connection and the reboot
TODO Use dictionaries for data correlations
TODO Investigate Camera connection quality
TODO Correlation between date-time of reboots and rtsp connections
TODO Determine whether the rtsp connection is a result of lost connection or reboot
TODO Investigate Decoder errors
TODO Check for Calibration resets
TODO Figure out how to do date based correlations
TODO decide what to do with the output = format it better, output it to a file?
TODO find a way to page the output on the screen
TODO combine searchargv and searchterms ?
'''
# pyperclip.copy(text)
