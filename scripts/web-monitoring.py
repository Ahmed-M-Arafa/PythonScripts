#!/bin/env python3

#import pdb; pdb.set_trace()         #Debugger

import pymsgbox                      #For POPUP
import os                            #System Commands
import sys, traceback                #KeyboardInterrupt
import urllib.request                #In parsing
from urllib.parse import urlparse    #Parser
import logging                       #Logging
import socket                        #In DNS "Get DOmain's IP"
import requests                      #Website requests
import time                          #Timing
from time import gmtime, strftime    #Timig
import pyttsx3                       #Convert Text to Speach


#Alert POPUP
def AlertBox(URL, Msg):
    pymsgbox.alert(text="%s %s" %(URL, Msg), title='SOS')

#Create "logs" drectory if not found
def LogsDir():
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

#Make sure the URL entered is in the proper format
def UrlParser(URL):
    p = urlparse("%s" %URL)
    if p.scheme:
        ParsedUrl = p.geturl()
        return ParsedUrl
    else:
        ParsedUrl = "http://%s" %p.geturl()
        return ParsedUrl

#Check network connection
def NetworkStatus():
    try:
        socket.create_connection(('google.com',80)) 
        Network = "On"
        return Network
    except socket.error as msg:
        Network = "Down"
        return Network

#Strip scheme from URL
def stripper(ParsedUrl):
    parsed = urlparse(ParsedUrl)
    scheme = "%s://" % parsed.scheme
    Url = parsed.geturl().replace(scheme, '', 1)
    return Url

#DNS Query
def query(Url):
    try:
        IP = socket.gethostbyname(Url)
        return IP
    except (socket.error, socket.gaierror) as ex:
        IP = "ERROR: No records found OR wrong domain"
        return IP

#Check DNS 
def DNS(ParsedUrl):
    p = urlparse("%s" %ParsedUrl)
    if p.scheme:
        StrippedUrl = stripper(ParsedUrl)
        query(StrippedUrl)
    else:
        query(ParsedUrl)

#Get website Error Code
def StatusCode(URL):
    Status = requests.get(URL).status_code
    return Status

#Process steps
def Process(URL):
    NetStatus = NetworkStatus()
    if NetStatus == "On":
        URL = UrlParser(URL)
        p = urlparse("%s" %URL)
        if p.scheme:
            DNS(URL)
            Code = StatusCode(URL)
            if Code == 200:
                now = strftime("%d-%m-%Y %H:%M:%S", time.localtime())
                print ("%s %s is UP" %(now, URL))
                logging.debug("%s %s is UP" %(now, URL))
            elif Code == 403:
                now = strftime("%d-%m-%Y %H:%M:%S", time.localtime())
                print ("%s %s is Forbidden" %(now, URL))
                Msg = ("is 403 Forbidden")
                VoiceAlert()
                AlertBox(URL, Msg)
            elif Code == 500:
                now = strftime("%d-%m-%Y %H:%M:%S", time.localtime())
                print ("%s %s can't handle request" %(now, URL))
                Msg = ("is 500 Error")
                VoiceAlert()
                AlertBox(URL, Msg)
            else:
                now = strftime("%d-%m-%Y %H:%M:%S", time.localtime())
                print ("%s %s is DOWN" %(now, URL))
                Msg = ("is DOWN")
                VoiceAlert()
                AlertBox(URL, Msg)
    else:
        now = strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        print ("%s No internet, Check your network" %now)
        Msg = (": No internet, Check your network")
        AlertBox(URL, Msg)

#Countdown timer
def timer(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

#Voice Alert
def VoiceAlert():
    engine = pyttsx3.init()
    engine.say("Check Website")
    engine.runAndWait()

#Create Log File
def LogFile(FileName):
    try:
        f = open('%s.log' %FileName,'r')
    except FileNotFoundError:
        f = open('%s.log' %FileName,'w')

    return f


'''
Script starts Here
'''
#LogsDir()
#LogFormat = logging.basicConfig(filename='%s' %FileName,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


if len(sys.argv) > 1:
    URL = sys.argv[1]
    while True:
        try:
            Process(URL)
            timer (20)
        except KeyboardInterrupt:
            print ("\nStop monitoring ...")
            print ("Bye")
            sys.exit(0)
else:
    try:
        URL = input ("URL: ")
        FileName = stripper(URL) 
        while True:
            try:
                Process(URL)
                timer (20)
            except KeyboardInterrupt:
                print ("\nStop monitoring ...")
                print ("Bye")
                sys.exit(0)
    except KeyboardInterrupt:
        print ("\nExit ...")
        print ("\nBye")
        sys.exit(0)
