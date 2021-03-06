#!/usr/bin/python3

from collections import Counter
import collections
import datetime
import operator
import os
import pprint
import re
import string
import sys


found = []
lines = []
text = []
rtsp_found = []
fwversion = [1,2,3,4]
derror_found = []
hd_status = []
datedic = {}
datedic1 = {}
exception_found = []
timedict = {}
timedict1 = {}
derror_dic = {}
errordict = {}

# flist = sys.argv[1] # receives the target directory from the CLI argument

os.chdir(os.path.abspath(sys.argv[1]))  # Changes the present working directory to the one from the CLI argument
'''
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
'''

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
    fw_version(flist1)
    hdd_lot_status(flist1, fwversion)
    reboots(flist1)
    if 'A4' not in str(fwversion[2]):
        connect_rtsp(flist1)
        compare(datedic, datedic1, timedict, timedict1)
        decode_error(flist1)
    hd_status(flist1, fwversion)
    # exception(flist1, exception_found, datedic)
    # if len(sys.argv) > 2:
      # terms = sys.argv[2]
      # searchargv(terms, flist1, found)
    # else:
      # terms = ['watchdog', 'Unhandled fault', 'Failed to authenticate', 'Link is', 'Ping overdue','ValidateAndUpdateStreams:Writing Configuration', 'Started at', 'CameraDescriptor:', 'Current boot version:','rebootSystem', 'set resolution to', 'Decode error', 'Overdue', 'Video Present', 'Video Lost','Timeout during', 'Connecting to rtsp:', 'RTSP \[[0-3]\]', 'Fps', 'Bitrate']
      # searchterms(terms, flist1, found)
    # text = pyperclip.paste()

def fw_version(flist1):
    '''Finds and prints the FW version and the SN fo the device
    '''
    global fwversion
    date_value1 = [] #using to hold date time value from the log lines.
   # with open("device_info.txt", "w") as devinfo: #open file to hold the found log lines
    for fname in flist1: #next three lines open the log files to be searched. Exlude health_mon logs
        if 'syslog' in str(fname):
            with open(fname, "r", encoding="ISO-8859-1") as file: #below we extract the Serial number, the Model and type of the device - blade or stand-alone
                #   print('\r', "File name is ", fname)
                for line in file:
                    if "Current boot version" in line.strip():
                       # devinfo.write(line)
                        fwholder = line.split(':')
                        fwholder1 = fwholder[4]
                        fwholder1 = fwholder1.strip()
                        if fwholder1 not in fwversion:
                            fwversion[0] = fwholder1
                    if "Serial=" in line.strip():
                       # devinfo.write(line)
                        fwholder = line.split('=')
                        fwholder1 = fwholder[1]
                        fwholder1 = fwholder1.strip()
                        if fwholder1 not in fwversion:
                            fwversion[1] = fwholder1
                    if "Model=" in line.strip():
                        #devinfo.write(line)
                        fwholder = line.split('=')
                        fwholder1 = fwholder[1]
                        fwholder1 = fwholder1.strip()
                        if fwholder1 not in fwversion:
                            fwversion[2] = fwholder1
                    if "hdspinup" in line.strip():
                        #devinfo.write(line)
                        fwholder1 = 'stand-alone'
                        if fwholder1 not in fwversion:
                            fwversion[3] = fwholder1
                    #print("This is a stand-alone Rialto")
                    elif "nas_mount" in line.strip():
                       # devinfo.write(line)
                        fwholder1 = 'blade'
                        if fwholder1 not in fwversion:
                            fwversion[3] = fwholder1
                        
                            
    print("Firmware version: ", fwversion[0])
    print("Serial Number: ", fwversion[1])
    print("Model number:", fwversion[2])
    print("Model type:", fwversion[3])
    print("="*80)
    return fwversion                 

def searchargv(terms, flist1, found):
    '''Search using term from the command line arguments'''
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
def reboots(flist1):
    # date_line = []
    date_value = []
   # with open("reboots.txt", "w") as ffound:
    for fname in flist1:
        if 'syslog' in str(fname):
            with open(fname, "r", encoding="ISO-8859-1") as file:
                #   print('\r', "File name is ", fname)
                for line in file:
                    if "restart" in str.lower(line):
                        #ffound.write(line)
                        date_line = line.split(' ') #next four lines extract the date and time from the log line.
                        date_v1 = (date_line[0] + " " + date_line[1])
                        date_time = line.split(' ')[1]
                        date_date = line.split(' ')[0]
                        if date_v1 not in date_value:
                            date_value.append(date_v1)
                            found.append(line)  # add the rtsp_found lines to the rtsp_found list

                            '''
                            add the line with time stamp (date_time) and the log line (date_line[-1]) as a sub dictionary, timestamp will be the key, date (date_date) is the key for the main dict
                            '''
                            datedic1.setdefault(date_date, {})[date_time] = date_line[-1]
                            c = collections.Counter(datedic1) #not sure what I am going to use this for

    print("found ", len(found), " restarts in the log files")
    date_value.sort()
    #ffound.close()
    #print(len(date_value))
    '''
    The part below is analysing the content of the datedict1 for various correlations
    '''
    key_dict1 = datedic1.keys() 
    mdate = min(sorted(key_dict1))
    mxdate = max(sorted(key_dict1))
    print("The oldest entry is from {date1} \nThe last enty is from {date2}".format(date1 = mdate, date2 = mxdate))
                                           # Isolate the dates of the reconnects
    for n in sorted(key_dict1):                                         #iterate through the dict by dates so we can investigate each day in turn
        time1 = list(sorted(datedic1[n].keys()))                         #find the times of the reconnects within a given day
        lentime1 = int(len(time1))                                             # how many times in a day the reconnect occured. counts the times stamps that are shown as key of the sub-dictionary
        timedict1.setdefault(n, []).append(lentime1)                      # Created timedict dictionary to hold the day as key and the number of re-connects as values.

    resultmax = max(timedict1.items(), key=operator.itemgetter(1))[0]       # Finds the day with most re-connects
    resultmin = min(timedict1.items(), key=operator.itemgetter(1))[0]    #supposetly finds the day with least re-connect but not clear what's the procedure if two days have the same number of reconnects
    x = timedict1[resultmax]
    y = timedict1[resultmin]
    print("Most restarts in a day -", x[0], "happened on", resultmax)
    print("="*80)
 #   print("Least restarts -", y[0], "happened on", resultmin)
    
    #for day in sorted(timedict1, key=timedict1.get, reverse=True):        #print the number of reconnects per day for each day sorted descenting by number of reconnects
    #    print("Date ", day, ": restarts per day ", timedict1[day])
    return datedic1
    return timedict1

'''Search for rtsp connections'''
def connect_rtsp(flist1):
    iphist = {}
    rtsp_ip = []
    ipdict = {}
    rtspip = []
    date_value1 = [] #using to hold date time value from the log lines.
    #with open("rtsp_connections.txt", "w") as ffound1: #open file to hold the found log lines
    for fname in flist1: #next three lines open the log files to be searched. Exlude health_mon logs
        if 'syslog' in str(fname):
            with open(fname, "r", encoding="ISO-8859-1") as file:
                #   print('\r', "File name is ", fname)
                for line in file:
                    if "connecting to rtsp" in str.lower(line):
                        #ffound1.write(line)
                        date_line = line.split(' ') #next four lines extract the date and time from the log line.
                        date_v1 = (date_line[0] + " " + date_line[1])
                        date_time = line.split(' ')[1]
                        date_date = line.split(' ')[0]
                        #channelnum = line.split(' ')[6]
                        if date_v1 not in date_value1:
                            rtsp_ip = line.split('/')
                            rtspip = rtsp_ip[2].strip()
                            channelnum = line.split(' ')[6]
                            #print("IP is", rtsp_ip[2])
                            date_value1.append(date_v1)
                            rtsp_found.append(line)  # add the rtsp_found lines to the rtsp_found list
                            '''
                            add the line with time stamp (date_time) and the log line (date_line[-1]) as a sub dictionary, timestamp will be the key, date (date_date) is the key for the main dict
                            '''
                            datedic.setdefault(date_date, {})[date_time] = date_line[-1]
                            iphist[rtspip] = iphist.get(rtspip, 0) + 1
                            ipdict.setdefault(channelnum, []).append(rtspip)
                            c = collections.Counter(datedic) #not sure what I am going to use this for
                        #else:
                        #    ffound1.close()
                        #    print("This must be an Analog Rialto", '\n')
                        #    return datedic
    print("found ", len(rtsp_found), " rtsp connections in the log files")
    ''' 
        The section below prints the IP and the channels of the connected cameras
        This can be used for more 
    '''
    # TODO: need to fix the printing
    for ch, ip in sorted(ipdict.items()):
        ips = list(sorted(set(ip)))
        print("Channel {channel} has IP {IP}".format(channel = ch, IP = ips))
    date_value1.sort()
    #ffound1.close()
    #print(len(date_value1))

    '''
    The part below is analysing the content of the datedict1 for various correlations
    '''
    for k in sorted(iphist, key=iphist.get, reverse=True):                  # Print the histogram sorted in reverse order by frequency of errors
        print("IP ", k, "reconnected", iphist[k], "times")
    key_dict = datedic.keys()                                         # Isolate the dates of the reconnects
    mdate = min(sorted(key_dict))
    mxdate = max(sorted(key_dict))  
    print("The oldest entry is from {date1} \nThe last enty is from {date2}".format(date1 = mdate, date2 = mxdate))
    for n in sorted(key_dict):                                              #iterate through the dict by dates so we can investigate each day in turn
        time = list(sorted(datedic[n].keys()))                         #find the times of the reconnects within a given day
        lentime = int(len(time))                                             # how many times in a day the reconnect occured. counts the times stamps that are shown as key of the sub-dictionary
        timedict.setdefault(n, []).append(lentime)                      # Created timedict dictionary to hold the day as key and the number of re-connects as values.

    resultmax = max(timedict.items(), key=operator.itemgetter(1))[0]       # Finds the day with most re-connects
    resultmin = min(timedict.items(), key=operator.itemgetter(1))[0]    #supposetly finds the day with least re-connect but not clear what's the procedure if two days have the same number of reconnects
    x = timedict[resultmax]
    y = timedict[resultmin]
    print("Most reconnects in a day -", x[0], "happened on", resultmax)
    print("="*80)
   # print("Least reconnects -", y[0], "happened on", resultmin)
    
    #for day in sorted(timedict, key=timedict.get, reverse=True):        #print the number of reconnects per day for each day sorted descenting by number of reconnects
    #    print("Date ", day, ": connections per day ", timedict[day])
    
    return datedic
    return timedict

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
    print("="*80)
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
def compare(datedic, datedic1, timedict, timedict1):
    for day in sorted(timedict, key=timedict.get, reverse=True):        #print the number of reconnects per day for each day sorted descenting by number of reconnects
       # print("Date ", day, ": connections per day ", timedict[day])
       hey_days = timedict1.keys()
       print("="*80)

       if day in sorted(hey_days):
            print("Date", day, "device restarts: ", timedict1[day], "rtsp connections: ", timedict[day])

       #for day1 in sorted(timedict1, key=timedict1.get, reverse=True):        #print the number of reconnects per day for each day sorted descenting by number of reconnects
       #     if day == day1:
       #         print("Date", day, "reconnects: ", timedict1[day], "rtsp connections: ", timedict[day])
    # input('Press any key to continue')
       elif day not in sorted(hey_days):
           print("date", day, "has", timedict[day], "rtsp reconnects and NO reboots")
    print("="*80)

def decode_error(flist1):
    ''' Analysing the Decode Errors in the syslog files, if any'''
    hist = {}
    date_value3 = [] #using to hold date time value from the log lines.
    date_value4 = []
    with open("rtsp_connections.txt", "w") as ffound3: #open file to hold the found log lines
        for fname in flist1: #next three lines open the log files to be searched. Exlude health_mon logs
            if 'syslog' in str(fname):
                with open(fname, "r", encoding="ISO-8859-1") as file:
                    #   print('\r', "File name is ", fname)
                    for line in file:
                        if "decode error" in str.lower(line.strip()):
                            ffound3.write(line)
                            date_line = line.split(' ') #next four lines extract the date and time from the log line.
                            date_v1 = (date_line[0] + " " + date_line[1])
                            date_time = line.split(' ')[1]
                            date_date = line.split(' ')[0]
                            derrname = (date_line[7] + " " + date_line[8])  # Just the field "Decode ERROR"
                            derrvalue = date_line[9]
                            derrvalue = derrvalue.strip()                   # the Decode Error value without new line
                            camchannel = date_line[6]                       # the channel of the affected camera
                            hist[derrvalue] = hist.get(derrvalue, 0) + 1    # Histogram of the varios decode errors
                            # print("Camera ", camchannel, "has ", derrname, derrvalue)
                            if date_time not in date_value3:
                                date_value3.append(date_v1)
                                derror_found.append(line)  # add the Decode Error lines to the derror_found list
                                '''
                                add the line with time stamp (date_time) and the log line (date_line[-1]) as a sub dictionary, timestamp will be the key, date (date_date) is the key for the main dict
                                '''
                                derror_dic.setdefault(date_date, {})[date_time] = date_line[-1]
                                c = collections.Counter(derror_dic) #not sure what I am going to use this for
                        #else:
                        #    ffound3.close()
                        #    print("No Decode Errors found in syslog*", '\n')
                        #    return
    ffound3.close()
    print("found ", len(derror_found), " Decode Errors in the log files")
    date_value3.sort()
    # pprint.pprint(hist)
    '''
    The part below is analysing the content of the derror_dict1 for various correlations
    ''' 
    for k in sorted(hist, key=hist.get, reverse=True):                  # Print the histogram sorted in reverse order by frequency of errors
        print("Decode Error", k, "happened", hist[k], "times")
    print("="*80)
    key_dict = derror_dic.keys()                                       
    for n in sorted(key_dict):                                         #iterate through the dict by dates so we can investigate each day in turn
        time = list(sorted(derror_dic[n].keys()))                         #find the times of the reconnects within a given day
        lentime = int(len(time))                                             # how many times in a day the reconnect occured. counts the times stamps that are shown as key of the sub-dictionary
        errordict.setdefault(n, []).append(lentime)                      # Created errordict dictionary to hold the day as key and the number of re-connects as values.

    resultmax = max(errordict.items(), key=operator.itemgetter(1))[0]       # Finds the day with most re-connects
    resultmin = min(errordict.items(), key=operator.itemgetter(1))[0]    #supposetly finds the day with least re-connect but not clear what's the procedure if two days have the same number of reconnects
    x = errordict[resultmax]
    print("Most Decode Errors in a day -", x[0], "happened on", resultmax)
    print("="*80)     
    return derror_dic
    return errordict       

def hd_status(flist1, fwversion):
    ''' Analysing the HDD info in healt_mon.log and in syslog(?) in the syslog files, if any'''
    hist = {}
    usage = []
    date_value3 = [] #using to hold date time value from the log lines.
    date_value4 = []
    for fname in flist1: #next three lines open the log files to be searched. Exlude health_mon logs
        if 'health' in str(fname):
            with open(fname, "r", encoding="ISO-8859-1") as file:
                text = file.read()
                #START = "Filesystem"
                #END = "##"
                #m = re.compile(r'%s.*?%s' %(START,END),re.S)
                m = re.compile('DF(.*?)##', re.S)
                lpr = m.search(text)
                if lpr:
                    lpr1 = lpr.group(1)
                    #print(lpr1)
                    if fwversion[3] is 'blade':
                        for line in lpr1.split('\n'):
                            if "FVS_BLADE" in line:
                                line = line.split('/')
                                slot = line[3]
                            if "/mnt/hd" in line:
                                line = line.split()
                                usage = line[3]
                                #usage = usage.strip('%')
                                hist[usage] = hist.get(usage, 0) + 1
                    else:
                        for line in lpr1.split('\n'):
                            if "/mnt/hd" in line:
                                line = line.split()
                                usage = line[4]
                                hist[usage] = hist.get(usage, 0) + 1
                                slot = False
                else:
                    print('Not found')
        
        
                            
    if slot is not False:
        print("blade in slot:", slot)
    for k in sorted(hist, key=hist.get, reverse=True):                  # Print the histogram sorted in reverse order by frequency of errors
        print("HDD usage was at", k, hist[k], "times")
    print("="*80)

    

def hdd_lot_status(flist1, fwversion):
    hdd_dict = {} 
    for fname in flist1: #next three lines open the log files to be searched. Exlude health_mon logs
        if 'syslog' in str(fname):
            with open(fname, "r", encoding="ISO-8859-1") as file1:
                if fwversion[3] is not 'blade':
                    for line1 in file1:
                        if "hdd slot" in str.lower(line1.strip()):
                            hdd_status = line1.split()
                            hdd_status8 = hdd_status[8]
                            hdd_status8 = hdd_status8.strip()
                            if hdd_status8 != '2':
                                hdd_dict[hdd_status8] = hdd_dict.get(hdd_status8, 0) + 1
    for y in sorted(hdd_dict, key=hdd_dict.get, reverse=True):
        print('HDD status was: "'+ y +'"', hdd_dict[y], "times") 
    print("="*80)
'''call the main function'''
if __name__ == "__main__": main()

'''
TODO: How to group lines by time stamp?
TODO: Investigate the time between the Rialto lost connection and the reboot
TODO: Use dictionaries for data correlations
TODO: Investigate Camera connection quality
TODO: Correlation between date-time of reboots and rtsp connections
TODO: Determine whether the rtsp connection is a result of lost connection or reboot
TODO: Investigate Decoder errors
TODO: Check for Calibration resets
TODO: Figure out how to do date based correlations
TODO: decide what to do with the output = format it better, output it to a file?
TODO: find a way to page the output on the screen
TODO: combine searchargv and searchterms ?
'''
# pyperclip.copy(text)
