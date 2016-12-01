print("       ____                 _ _        \n" +
      "  __ _|  _ \ ___  ___ _   _| | |_ ___  \n" +
      " / _` | |_) / _ \/ __| | | | | __/ __| \n" +
      "| (_| |  _ <  __/\__ \ |_| | | |_\__ \ \n" +
      " \__, |_| \_\___||___/\__,_|_|\__|___/ \n" +
      " |___/                1.0 by @xdavidhu \n")

import inspect, os
import sys
try:
    from urllib.request import Request, urlopen
except:
    print("\n[E] Make sure to use Python3 to run this application.\n")
    exit()
try:
    from bs4 import BeautifulSoup
except:
    print("\n[E] BeautifulSoup is needed for this application to work.\n    Please install it with 'pip3 install beautifulsoup4', and try again\n")
    exit()
import re
lang_code = "en"
print("Please enter the wordlist's location:")

list = input()
tempList = list
tempList = tempList.replace('.txt', '')
tempList = tempList.replace('/', '-')
print()
tempResultFileName = "gResults" + tempList + ".txt"

try:
    wordlist = open(list, 'r')
except:
    print("[E] Wordlist not found. Try again with an another location.\n")
    exit()


print("[I] Wordlist detected...\n")

print("[Q] Do you want to save the results in a text file? Y/n")
textQuestion = input()
textQuestion = textQuestion.lower()
if textQuestion == "y":
    resultFile = open(tempResultFileName, 'w+')
print()


for word in wordlist.readlines():
    word = word.split('\n')
    word = word[0]

    tempWord = word

    word = word.lower()
    tempQuery = ""

    for c in word:
        if c == " ":
            c = "+"
        tempQuery = tempQuery + c

    webpage = ""
    if not re.match("^[a-zA-Z0-9_+]*$", tempQuery):
        print("[E] Please do not use any special characters in the wordlist.\n")
        exit()
    try:
        url = 'https://www.google.com/search?q=' + tempQuery + "&hl=" + lang_code
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        utfPage = webpage.decode(encoding='UTF-8')
        soup = BeautifulSoup(utfPage, "html.parser")
    except KeyboardInterrupt:
        print("\nStopping...\n")
        wordlist.close()
        if textQuestion == "y":
            location = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            if sys.platform == 'win32':
                location = location + "\\" + tempResultFileName
            else:
                location = "'" + location + "/" + tempResultFileName + "'"

            print("[I] Result saved in file: " + location + "\n")

            resultFile.close()
            exit()
    except:
        print("[E] Error while downloading the results. Do you have a working internet connection?\n")
        exit()
    try:
        data = str(soup.find('div', {'class': 'sd'}).text)
    except KeyboardInterrupt:
        print("\nStopping...\n")
        wordlist.close()
        if textQuestion == "y":
            location = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            if sys.platform == 'win32':
                location = location + "\\" + tempResultFileName
            else:
                location = "'" + location + "/" + tempResultFileName + "'"

            print("[I] Result saved in file: " + location + "\n")

            resultFile.close()
            exit()
    except:
        print("[E] Cannot load results. Is Google blocked you?\n")
        exit()

    data = data.replace('About ', '')
    data = data.replace(' results', '')

    tempPrintData = tempWord + " ==> " + data
    print(tempPrintData)
    if textQuestion == "y":
        resultFile.write(tempPrintData + '\n')

print()

wordlist.close()

if textQuestion == "y":
    location = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    if sys.platform == 'win32':
        location = location + "\\" + tempResultFileName
    else:
        location = "'" + location + "/" + tempResultFileName + "'"

    print("[I] Result saved in file: " + location + "\n")

resultFile.close()
