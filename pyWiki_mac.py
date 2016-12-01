
print("           __        ___ _    _ \n" +
      " _ __  _   \ \      / (_) | _(_)\n" +
      "| '_ \| | | \ \ /\ / /| | |/ / |\n" +
      "| |_) | |_| |\ V  V / | |   <| |\n" +
      "| .__/ \__, | \_/\_/  |_|_|\_\_|\n" +
      "|_|    |___/    1.0 by @xdavidhu\n")

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
import os

while True:
    print("Please enter a search query: ")
    os.system("say Please enter a search query")
    query = input()
    query = query.lower()
    tempQuery = ""

    #Replaceing the spaces with "+" for the google search URL
    for c in query:
        if c == " ":
            c = "+"
        tempQuery = tempQuery + c

    #Check for any special characters
    if not re.match("^[a-zA-Z0-9_+]*$", tempQuery):
        print("\n[E] Please do not use any special characters.\n")
        continue

    #Downloading the html page with the results
    os.system("say One moment, searching")
    try:
        url = 'https://www.google.com/search?q=' + tempQuery + "&hl=en"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
    except:
        print("\n[E] Error while downloading the results. Do you have a working internet connection?\n")
        continue

    #Converting it to UTF-8
    utfPage = webpage.decode(encoding='UTF-8')

    #Initializing BeautifulSoup for the HTML parsing
    soup = BeautifulSoup(utfPage, "html.parser")

    #Finding the information card's description div
    data = str(soup.find('div', {'class':'_tXc'}))

    #If there is no information card
    if data == "None":
        print("\n[W] Sorry, there are no results for this query\n")
        os.system("say Sorry, there are no results for this query.")
        continue
    #Else, get the content of the span wich has the text in it
    else:
        soup2 = BeautifulSoup(data, "html.parser")
        data2 = str(soup2.find('span').text)
        data2 = data2.replace('\n', '')

        #Remove "Wikipedia" from the end of the text
        data2 = data2.replace('Wikipedia', '')
        print("")
        print(data2)
        print("")
        os.system("say " + data2)

        #Check if the user wants to search again
        print("Do You want to search again? Yes / No")
        os.system("say Do you want to search again?")
        again = input()
        again = again.lower()
        if again == "yes":
            print("")
            continue
        else:
            print("Goodbye!")
            os.system("say Goodbye!")
break
