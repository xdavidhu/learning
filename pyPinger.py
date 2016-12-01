#!/usr/bin/env python3

import time
from subprocess import check_output, DEVNULL
from datetime import datetime
import smtplib
import linecache

hostsUp = []
hostsDown = []
hostsDownWarning = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printOut(text, color):
    now = datetime.now()
    tempText = color + "[" + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "|" + str(
        now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] " + text + bcolors.ENDC
    print(tempText)

def sendMail(text):
    try:
        cfg = open("email.cfg")
    except:
        printOut("Mail config file error.", bcolors.FAIL)
        return None

    smtp_server = linecache.getline("email.cfg", 1)
    smtp_server = smtp_server.replace("smtp server = ", "")
    smtp_server = smtp_server.replace("\n", "")

    smtp_port = linecache.getline("email.cfg", 2)
    smtp_port = smtp_port.replace("smtp port = ", "")
    smtp_port = smtp_port.replace("\n", "")

    smtp_user = linecache.getline("email.cfg", 3)
    smtp_user = smtp_user.replace("smtp user = ", "")
    smtp_user = smtp_user.replace("\n", "")

    smtp_pass = linecache.getline("email.cfg", 4)
    smtp_pass = smtp_pass.replace("smtp password = ", "")
    smtp_pass = smtp_pass.replace("\n", "")

    to = linecache.getline("email.cfg", 5)
    to = to.replace("to = ", "")
    to = to.replace("\n", "")

    gmail_user = smtp_user
    gmail_pwd = smtp_pass
    FROM = smtp_user
    TO = to if type(to) is list else [to]
    SUBJECT = "pyPinger STATUS REPORT"
    TEXT = text

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        printOut("[OK] Mail successfully sent.", bcolors.OKGREEN)
        log("[OK] Mail successfully sent.")
    except:
        printOut("[E] Failed to send mail.", bcolors.WARNING)
        log("[E] Failed to send mail.")

def ping(hostname):
    try:
        check_output(["ping", "-c1", hostname], stderr=DEVNULL).decode("UTF-8")
        return True
    except:
        return False

def importFile(file):
    with open(file) as f:
        for line in f:
            line = line.replace('\n', '')
            hostsAll = hostsUp + hostsDown
            addToHosts = True
            for i in hostsAll:
                if i == line:
                    addToHosts = False
            if addToHosts:
                printOut("Adding host '" + line + "' to database.", "")
                hostsUp.append(line)

def deleteHost(file):
    tempHosts = []
    with open(file) as f:
        for line in f:
            line =line.replace("\n", "")
            tempHosts.append(line)

    hostsAll = hostsUp + hostsDown
    delArray = [x for x in hostsAll if x not in tempHosts]

    for i in delArray:
        try:
            hostsUp.remove(i)
            printOut("Host '" + i + "' removed from the database.", bcolors.WARNING)
        except:
            hostsDown.remove(i)
            printOut("Host '" + i + "' removed from the database.", bcolors.WARNING)

def log(text):
    logFile = open("pyPinger_latest.log", 'a')
    now = datetime.now()
    text ="[" + str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "|" + str(
        now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] " + text + "\n"
    try:
        logFile.write(text)
        logFile.close()
    except:
        return None

# MAIN

print('                                                                   \n' +
      '                   /$$$$$$$ /$$                                    \n' +
      '                  | $$__  $|__/                                    \n' +
      '  /$$$$$$ /$$   /$| $$  \ $$/$$/$$$$$$$  /$$$$$$  /$$$$$$  /$$$$$$ \n' +
      ' /$$__  $| $$  | $| $$$$$$$| $| $$__  $$/$$__  $$/$$__  $$/$$__  $$\n' +
      '| $$  \ $| $$  | $| $$____/| $| $$  \ $| $$  \ $| $$$$$$$| $$  \__/\n' +
      '| $$  | $| $$  | $| $$     | $| $$  | $| $$  | $| $$_____| $$      \n' +
      '| $$$$$$$|  $$$$$$| $$     | $| $$  | $|  $$$$$$|  $$$$$$| $$      \n' +
      '| $$____/ \____  $|__/     |__|__/  |__/\____  $$\_______|__/      \n' +
      '| $$      /$$  | $$                     /$$  \ $$                  \n' +
      '| $$     |  $$$$$$/                    |  $$$$$$/                  \n' +
      '|__/      \______/                      \______/   1.2 by @xdavidhu\n\n')


printOut("Opening config files...", "")

try:
    logFile = open("pyPinger_latest.log", 'w+')
    printOut("[OK] Log created.", bcolors.OKGREEN)
    logFile.close()
except:
    printOut("[E] Log error. Maybe no permission?", bcolors.FAIL)

log("pyPinger started...")

pleaseEdit = False
try:
    hostList = open("hosts.list", 'r')
    printOut("[OK] Hosts list found.", bcolors.OKGREEN)
    log("[OK] Hosts list found.")
except:
    printOut("[W] Hosts list not found. Creating...", bcolors.WARNING)
    log("[W] Hosts list not found. Creating...")
    hostList = open("hosts.list", 'w+')
    pleaseEdit = True
hostList.close()

try:
    mailCfg = open("email.cfg", 'r')
    printOut("[OK] Email config file found.", bcolors.OKGREEN)
    log("[OK] Email config file found.")
except:
    printOut("[W] Email config file not found. Creating...", bcolors.WARNING)
    log("[W] Email config file not found. Creating...")
    mailCfg = open("email.cfg", 'w+')
    mailCfg.write("smtp server = \nsmtp port = \nsmtp user = \nsmtp password = \nto = ")
    pleaseEdit = True
mailCfg.close()

if pleaseEdit:
    print()
    printOut("Please edit the newly created config files, and start pyPinger again.", bcolors.WARNING)
    log("Config files created, waiting for user restart...")
    exit()

importFile("hosts.list")
tempHosts = 0
for i in hostsUp:
    tempHosts += 1
printOut("[I] " + str(tempHosts) + " host imported from the 'hosts.list' file.", bcolors.OKBLUE)

while True:
    try:
        for host in hostsUp:
            isUp = ping(host)
            if not isUp:
                hostsDown.append(host)

                if host in hostsDownWarning:
                    hostsUp.remove(host)
                    hostsDownWarning.remove(host)
                    printOut("[W] Host '" + host + "' went down.", bcolors.FAIL)
                    log("[W] Host '" + host + "' went down.")
                    sendMail("Warning! '" + host + "' WENT DOWN!")
                else:
                    hostsDownWarning.append(host)
            else:
                if host in hostsDownWarning:
                    hostsDownWarning.remove(host)


        for host in hostsDown:
            isUp = ping(host)
            if isUp:
                hostsUp.append(host)
                hostsDown.remove(host)
                printOut("[OK] Host '" + host + "' is online again.", bcolors.OKGREEN)
                log("[OK] Host '" + host + "' is online again.")
                sendMail("Hurray! '" + host + "' IS ONLINE AGAIN!")

        importFile("hosts.list")
        deleteHost("hosts.list")

        time.sleep(30)

    except KeyboardInterrupt:
        print()
exit(printOut("Exiting...", bcolors.FAIL))
