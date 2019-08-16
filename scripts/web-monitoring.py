#!/bin/env python3

# import pdb; pdb.set_trace()        # Debugger

import pymsgbox                      # For POPUP
import os                            # System Commands
import sys                           # KeyboardInterrupt
import traceback                     # KeyboardInterrupt
import urllib.request                # In parsing
from urllib.parse import urlparse    # Parser
import logging                       # Logging
import socket                        # In dns "Get DOmain's ip"
import requests                      # Website requests
import time                          # Timing
from time import gmtime, strftime    # Timig
import pyttsx3                       # Convert Text to Speach


# Alert POPUP
def alert_box(url, msg):
    pymsgbox.alert(text="%s %s" % (url, msg), title='SOS')


# Create "logs" drectory if not found
def log_dir():
    if not os.path.exists("./logs"):
        os.makedirs("./logs")


# Make sure the url entered is in the proper format
def usrl_parser(url):
    p = urlparse("%s" % url)
    if p.scheme:
        parsed_url = p.geturl()
        return parsed_url
    else:
        parsed_url = "http://%s" % p.geturl()
        return parsed_url


# Check network connection
def network_status():
    try:
        socket.create_connection(('google.com', 80))
        network = "On"
        return network
    except socket.error as msg:
        network = "Down"
        return network


# Strip scheme from url
def stripper(parsed_url):
    parsed = urlparse(parsed_url)
    scheme = "%s://" % parsed.scheme
    Url = parsed.geturl().replace(scheme, '', 1)
    return Url


# DNS Query
def query(Url):
    try:
        ip = socket.gethostbyname(Url)
        return ip
    except (socket.error, socket.gaierror) as ex:
        ip = "ERROR: No records found OR wrong domain"
        return ip


# Check DNS
def dns(parsed_url):
    p = urlparse("%s" % parsed_url)
    if p.scheme:
        stripped_url = stripper(parsed_url)
        query(stripped_url)
    else:
        query(parsed_url)


# Get website Error Code
def status_code(url):
    Status = requests.get(url).status_code
    return Status


# Display error code
def display(url, code):
    now = strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    if code == 200:
        msg = print ("%s %s is UP" %(now, url))
    elif code == 403:
        msg = print ("%s %s is Forbidden" % (now, url))
        msg_box = ("is 403 Forbidden")
        voice_alert()
        alert_box(url, msg_box)
    elif code == 500:
        msg = print ("%s %s can't handle request" % (now, url))
        msg_box = ("is 500 Error")
        voice_alert()
        alert_box(url, msg_box)
    else:
        msg_box = ("is DOWN")
        voice_alert()
        alert_box(url, msg_box)
    return msg


# process steps
def process(url):
    net_status = network_status()
    if net_status == "On":
        url = usrl_parser(url)
        p = urlparse("%s" % url)
        if p.scheme:
            dns(url)
            code = status_code(url)
            display(url, code)
    else:
        now = strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        print ("%s No internet, Check your network" % now)
        msg = (": No internet, Check your network")
        alert_box(url, msg)


# Countdown timer
def timer(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1


# Voice Alert
def voice_alert():
    engine = pyttsx3.init()
    engine.say("Check Website")
    engine.runAndWait()


# Create Log File
def log_file(file_name):
    try:
        f = open('%s.log' % file_name, 'r')
    except FileNotFoundError:
        f = open('%s.log' % file_name, 'w')

    return f


# Exit Messege
def exit_msg():
    bye = print ("\nStop Monitoring ...\nBye")
    sys.exit(0)
    return bye


'''
Script starts Here
'''
# log_dir()

if len(sys.argv) > 1:
    url = sys.argv[1]
    while True:
        try:
            process(url)
            timer(20)
        except KeyboardInterrupt:
            exit_msg()
else:
    try:
        url = input("URL: ")
        file_name = stripper(url)
        while True:
            try:
                process(url)
                timer(20)
            except KeyboardInterrupt:
                exit_msg()
    except KeyboardInterrupt:
        print ("\nExit")
        sys.exit(0)

