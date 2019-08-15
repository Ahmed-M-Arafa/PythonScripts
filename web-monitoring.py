#!/bin/env python3

#import pdb; pdb.set_trace()

import pymsgbox
import os
import sys
import urllib.request
from urllib.parse import urlparse
import logging
import socket
import requests
import time
from time import gmtime, strftime


#Alert POPUP
def AlertBox(URL):
    pymsgbox.alert(text='Check %s' %URL, title='SOS')

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
    #except socket.gaierror:
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


def Process(URL):
    NetStatus = NetworkStatus()
    if NetStatus == "On":
        URL = UrlParser(URL)
        p = urlparse("%s" %URL)
        if p.scheme:
            DNS(URL)
            Code = StatusCode(URL)
            if Code == 200:
                time = strftime("%a %d-%b-%Y %H:%M:%S", gmtime())
                print ("%s %s is UP" %(time, URL))
            elif Code == 403:
                print ("%s %s is Forbidden" %(time, URL))
            elif Code == 500:
                print ("%s %s can't handle request" %(time, URL))
            else:
                print ("%s %s is DOWN" %(time, URL))
    else:
        print ("No internet, Check your network connection")



'''
Script starts Here
'''


LogsDir()

LogFormat = logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


if len(sys.argv) > 1:
    URL = sys.argv[1]
    while True:
        Process(URL)
        #time.sleep ( 5 )
else:
    URL = input ("URL: ")
    while True:
        Process(URL)
        #time.sleep ( 5 )
