import threading, time, os, json, logging, curses, random, time, argparse
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Shut up scapy!
from scapy.all import *

parser = argparse.ArgumentParser(
    usage="piLocatR.py interface target-mac")
parser.add_argument("interface", help='interface for capturing the packets')
parser.add_argument("target_mac", help='mac address of target device')
args = parser.parse_args()

# STATUS VARIABLES
scanningForNearbyDevices = False
scanMode = 0
searchMode = 0
deviceLocated = False
channelLocated = False
scanningForDevice = False
currentChannel = False
deviceChannel = False
latestRSSI = False
noDataSinceScans = 0
monitorModeError = False
target = False
deviceLostTimer = 0
rssiList = []
apChannels = []
interface = args.interface
# /STATUS VARIABLES

os.system("sudo ifconfig " + interface + " down")
os.system("sudo iwconfig " + interface + " mode monitor")
os.system("sudo ifconfig " + interface + " up")

def getNearbyDevices():
    global interface
    devices = []
    currentChannel = 1
    while currentChannel <= 11:
        os.system("sudo iwconfig " + interface + " channel " + str(currentChannel))
        try:
            packetList = sniff(iface=interface, timeout=1, store=0)
        except:
            return
        for packet in packetList:
            if str(packet.addr2) != "None":
                if packet.haslayer(Dot11):
                    try:
                        sig_str = -(256 - packet.notdecoded[-2])
                    except:
                        continue
                    alreadyInList = False
                    for device in devices:
                        if str(packet.addr2) == device[0]:
                            alreadyInList = True
                    if alreadyInList == False:
                        devices.append([str(packet.addr2), sig_str])
        currentChannel += 1
    devices = sorted(devices, key=lambda x: x[1], reverse=True)
    return devices[:10]

def resetVars():
    global scanMode
    global deviceLocated
    global channelLocated
    global scanningForDevice
    global currentChannel
    global deviceChannel
    global latestRSSI
    global noDataSinceScans
    global monitorModeError
    global target
    global rssiList
    global apChannels
    global searchMode

    scanMode = 0
    searchMode = False
    deviceLocated = False
    channelLocated = False
    scanningForDevice = False
    currentChannel = False
    deviceChannel = False
    latestRSSI = False
    noDataSinceScans = 0
    monitorModeError = False
    target = False
    rssiList = []
    apChannels = []

def getIfMacInList(packetList):
    global target
    for packet in packetList:
        if packet.haslayer(Dot11):
            if packet.addr2 == target:
                if packet.type == 0 and packet.subtype == 4:
                    pass
                else:
                    return True
    return False

def getIfAPInList(packetList):
    for pkt in packetList:
        if pkt.haslayer(Dot11) :
            if pkt.type == 0 and pkt.subtype == 8 :
        	       return True
    return False

def getAPChannels():
    global apChannels
    global currentChannel
    global interface

    currentChannel = 1

    while currentChannel <= 11:
        os.system("sudo iwconfig " + interface + " channel " + str(currentChannel))
        try:
            packetList = sniff(iface=interface, timeout=0.5, store=0)
        except:
            continue
        apInList = getIfAPInList(packetList)
        if apInList:
            apChannels.append(currentChannel)
        currentChannel += 1

def getChannel():
    global currentChannel
    global scanningForDevice
    global interface
    global apChannels
    global searchMode

    scanningForDevice = True
    searchMode = 0
    deviceFound = False

    getAPChannels()

    searchMode = 1

    while True:
        if searchMode == 1:
            timeout = 1
        if searchMode == 2:
            timeout = 15

        for channel in apChannels:
            currentChannel = channel
            os.system("sudo iwconfig " + interface + " channel " + str(channel))
            try:
                packetList = sniff(iface=interface, timeout=timeout, store=0)
            except:
                continue
            deviceFound = getIfMacInList(packetList)
            if deviceFound:
                break
        if deviceFound:
            scanningForDevice = False
            return channel
        else:
            if searchMode == 2:
                scanningForDevice = False
                return False
            else:
                searchMode = 2

def pktHandler(pkt):
    global scanMode
    global target
    global rssiList
    global monitorModeError

    if pkt.haslayer(Dot11):
        if pkt.addr2 == target:
            if pkt.type == 0 and pkt.subtype == 4:
                try:
                    sig_str = -(256 - pkt.notdecoded[-2])
                except:
                    monitorModeError = True
                if sig_str > -150:
                    rssiList.append(sig_str)
            else:
                try:
                    sig_str = -(256 - pkt.notdecoded[-2])
                except:
                    monitorModeError = True
                if sig_str > -150:
                    rssiList.append(sig_str)

def getRSSI():
    global rssiList
    global channelLocated
    global deviceChannel
    global latestRSSI
    global noDataSinceScans
    global deviceLocated
    global scanMode
    global target
    global deviceLostTimer

    if target == False:
        return

    if deviceLocated == False and channelLocated == True:
        if deviceLostTimer >= 5:
            channelLocated = False
        else:
            deviceLostTimer += 1

    if not channelLocated:
        deviceChannel = getChannel()
        channelLocated = True
        deviceLocated = True
        if deviceChannel == False:
            scanMode = 1

    avgList = rssiList[-10:]
    if len(avgList) > 0:
        deviceLocated = True
        average = int(sum(avgList) / float(len(avgList)))
        rssiList = []
        latestRSSI = average
        noDataSinceScans = 0
    else:
        noDataSinceScans += 1
        if scanMode == 1:
            if noDataSinceScans >= 120:
                deviceLocated = False
        else:
            if noDataSinceScans >= 50:
                deviceLocated = False

# THREAD FUNCTIONS

def sniffThread():
    global interface
    global curren
    global deviceLocated

    while True:
        if deviceLocated:
            try:
                sniff(iface=interface, prn=pktHandler, store=0)
            except:
                os.system("sudo ifconfig " + interface + " down")
                os.system("sudo iwconfig " + interface + " mode monitor")
                os.system("sudo ifconfig " + interface + " up")
                os.system("sudo iwconfig " + interface + " channel " + str(currentChannel))

def chopperThread():
    global currentChannel
    global scanMode
    global interface
    while True:
        if scanMode == 1:
            os.system("sudo iwconfig " + interface + " channel 1")
            currentChannel = 1
            time.sleep(5)
            os.system("sudo iwconfig " + interface + " channel 6")
            currentChannel = 6
            time.sleep(5)
            os.system("sudo iwconfig " + interface + " channel 11")
            currentChannel = 11
            time.sleep(5)
        else:
            time.sleep(1)

def mainThread():
    while True:
        getRSSI()
        time.sleep(1)

# STARTING BACKGROUND THREADS

st = threading.Thread(target=sniffThread)
st.daemon = True
st.start()

mt = threading.Thread(target=mainThread)
mt.daemon = True
mt.start()

ct = threading.Thread(target=chopperThread)
ct.daemon = True
ct.start()

# MANAGEMENT FUNCTIONS:

def stopScan():
    resetVars()
    return "success"

def getStatus():
    global deviceLocated
    global channelLocated
    global scanningForDevice
    global currentChannel
    global deviceChannel
    global latestRSSI
    global apChannels
    global noDataSinceScans
    global target
    global scanMode
    global searchMode
    global rssiList
    global deviceLostTimer

    data = {}
    data['deviceLocated'] = deviceLocated
    data['channelLocated'] = channelLocated
    data['scanningForDevice'] = scanningForDevice
    data['currentChannel'] = currentChannel
    data['deviceChannel'] = deviceChannel
    data['latestRSSI'] = latestRSSI
    data['apChannels'] = apChannels
    data['noDataSinceScans'] = noDataSinceScans
    data['deviceLostTimer'] = deviceLostTimer
    data['target'] = target
    data['scanMode'] = scanMode
    data['searchMode'] = searchMode
    data['rssiList'] = rssiList
    return data

def scanForDevies():
    global target
    global scanningForNearbyDevices
    if scanningForNearbyDevices == False:
        target = False
        scanningForNearbyDevices = True
        result = json.dumps(getNearbyDevices())
        scanningForNearbyDevices = False
        return result
    else:
        return "error"

def setTarget(mac):
    global target
    resetVars()
    target = str(mac)
    return "success"

def getStatusHumanReadable():
    dataObject = getStatus()

    if dataObject["target"] == False:
        return "No target set..."

    if dataObject["scanningForDevice"] == True:
        if dataObject["searchMode"] == 0:
            return "Searching for nearby AP channels..."
        elif dataObject["searchMode"] == 1:
            return "Searching for device..."
        elif dataObject["searchMode"] == 2:
            return "Device not found with fast scan, trying longer scan..."
    elif dataObject["scanMode"] == 0:
        if dataObject["channelLocated"] == False:
            return "Target set. Starting scan..."
    elif dataObject["scanMode"] == 1:
        return "Device still not found. Falling back to probe request scan..."

    if dataObject["deviceLocated"] == True:
        if dataObject["latestRSSI"] == False:
            return "Device located, no packets yet..."
        else:
            return "RSSI: " + str(dataObject["latestRSSI"])
    else:
        if dataObject["scanningForDevice"] == False:
            if dataObject["channelLocated"] == True:
                return "Device lost. Restarting scan in a few seconds..."
    return "I have no idea whats happening..."

def getCurrentChannel():
    dataObject = getStatus()
    if dataObject["currentChannel"] != False:
        return str(dataObject["currentChannel"])
    else:
        return False

def getDBI():
    dataObject = getStatus()
    return dataObject["latestRSSI"]

def getIfScanning():
    dataObject = getStatus()
    return dataObject["scanningForDevice"]

# SCREEN:

loadingFrame = 0

def getPowerBar(dbi):

    if dbi < -90:
        bars = 1
    elif dbi > -50:
        bars = 40
    else:
        bars = 40 - (int(dbi) + 50)*-1

    line = []
    line.append("      ┌──────────────────────────────────────────┐      ")
    line.append(" -90  │ " + "█"*bars + " "*(40-bars) + " │ -50  ")
    line.append("  dBi │ " + "█"*bars + " "*(40-bars) + " │  dBi ")
    line.append("      └──────────────────────────────────────────┘      ")

    return line

def loading():
    global loadingFrame

    if loadingFrame == 0:
        line = []
        line.append("      ┌──────────────────────────────────────────┐      ")
        line.append(" -90  │  ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ │ -50  ")
        line.append("  dBi │ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒  │  dBi ")
        line.append("      └──────────────────────────────────────────┘      ")
        loadingFrame = 1
        return line
    elif loadingFrame == 1:
        line = []
        line.append("      ┌──────────────────────────────────────────┐      ")
        line.append(" -90  │ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒  │ -50  ")
        line.append("  dBi │  ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ │  dBi ")
        line.append("      └──────────────────────────────────────────┘      ")
        loadingFrame = 0
        return line

def banner():
    line = []

    line.append("       _ _                     _  ______  ")
    line.append("      (_| |                   | | | ___ \\ ")
    line.append(" _ __  _| |     ___   ___ __ _| |_| |_/ / ")
    line.append("| '_ \| | |    / _ \ / __/ _` | __|    /  ")
    line.append("| |_) | | |___| (_) | (_| (_| | |_| |\ \  ")
    line.append("| .__/|_\_____/\___/ \___\__,_|\__\_| \_| ")
    line.append("| |      v1.0 by David Schütz (@xdavidhu) ")
    line.append("|_|                                       ")
    return line

def main(screen):
    global interface
    screen.clear()
    curses.curs_set(0)

    while True:
        try:
            # Get the y,x of the window
            dims = screen.getmaxyx()
            # Get the center of the window
            center = (dims[0]//2), (dims[1]//2)
            screen.border()

            lines = banner()
            screen.addstr(center[0]-8, center[1] - int(len(lines[0]) / 2), lines[0])
            screen.addstr(center[0]-7, center[1] - int(len(lines[1]) / 2), lines[1])
            screen.addstr(center[0]-6, center[1] - int(len(lines[2]) / 2), lines[2])
            screen.addstr(center[0]-5, center[1] - int(len(lines[3]) / 2), lines[3])
            screen.addstr(center[0]-4, center[1] - int(len(lines[4]) / 2), lines[4])
            screen.addstr(center[0]-3, center[1] - int(len(lines[5]) / 2), lines[5])
            screen.addstr(center[0]-2, center[1] - int(len(lines[6]) / 2), lines[6])
            screen.addstr(center[0]-1, center[1] - int(len(lines[7]) / 2), lines[7])

            printtext = "Status:"
            screen.addstr(center[0], center[1] - int(len(printtext) / 2), printtext)
            printtext = getStatusHumanReadable()
            screen.addstr(center[0]+1, center[1] - int(len(printtext) / 2), printtext)

            if getIfScanning() or getDBI() == False:
                lines = loading()
            else:
                lines = getPowerBar(getDBI())

            screen.addstr(center[0]+3, center[1] - int(len(lines[0]) / 2), lines[0])
            screen.addstr(center[0]+4, center[1] - int(len(lines[1]) / 2), lines[1])
            screen.addstr(center[0]+5, center[1] - int(len(lines[2]) / 2), lines[2])
            screen.addstr(center[0]+6, center[1] - int(len(lines[3]) / 2), lines[3])

            if getDBI() == False:
                printtext = "- dBi"
            else:
                printtext = str(getDBI()) + " dBi"
            screen.addstr(center[0]+7, center[1] - int(len(printtext) / 2), printtext)
            printtext = "iface: " + str(interface) + " - channel: " + str(getChannel())
            screen.addstr(center[0]+8, center[1] - int(len(printtext) / 2), printtext)

            time.sleep(0.5)
            screen.refresh()
            screen.clear()
        except KeyboardInterrupt:
            curses.endwin()
            os.system("clear")
            print("[I] Stopping...")
            exit()
        except:
            curses.endwin()
            os.system("clear")
            print("[!] Terminal screen too small... Please try again.")
            exit()

if __name__ == "__main__":
    setTarget(args.target_mac)
    curses.wrapper(main)
