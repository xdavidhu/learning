import hashlib, sqlite3, time, threading

chainContents = ["We're no strangers to love", "You know the rules and so do I", "A full commitment's what I'm thinking of", "You wouldn't get this from any other guy", \
                "I just want to tell you how I'm feeling", "Gotta make you understand", "Never gonna give you up, never gonna let you down", "Never gonna run around and desert you", \
                "Never gonna make you cry, never gonna say goodbye", "Never gonna tell a lie and hurt you"]

diff = 5

currentHash = ""
currentIndex = 0

def miningAnimation():
    import sys
    global stopAnimation
    global currentIndex
    try:
        i = 0
        spinnerCounter = 0
        while True:
            spinner = ["|", "/", "-", "\\"]
            text = "[" + spinner[spinnerCounter] + "] Mining block #" + str(currentIndex) + " - Current hash: " + currentHash + "\r"
            if i == 0:
                spinnerCounter += 1
                if spinnerCounter > 3:
                    spinnerCounter = 0
            sys.stdout.write(text)
            sys.stdout.flush()
            time.sleep(0.05)
            i += 1
            if i >= 2:
                i = 0
    except:
        raise SystemExit

def validateHashDiff(blockhash):
    if str(blockhash[:diff]) != "0" * diff:
        return False
    else:
        return True

def generateHash(index, previoushash, timestamp, data):
    global currentHash
    nonce = 0
    while True:
        nonce += 1
        dataToHash = str(index) + str(previoushash) + str(timestamp) + str(data) + str(nonce)
        hash_object = hashlib.sha256(dataToHash.encode())
        hex_dig = hash_object.hexdigest()
        currentHash = str(hex_dig)
        if validateHashDiff(hex_dig):
            break
    return [hex_dig, nonce]

def createDB():
    conn = sqlite3.connect('miniBlockchain.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'blockchain' ( 'blockid' INT, 'previoushash' TEXT, 'timestamp' TEXT, 'data' TEXT, 'hash' TEXT, 'nonce' TEXT)")
    conn.commit()
    conn.close()

def mineGenesisBlock():
    index = 0
    timestamp = int(time.time())
    previoushash = "0"
    data = "Hello World!"

    hashnonce = generateHash(index, previoushash, timestamp, data)

    conn = sqlite3.connect('miniBlockchain.db')
    c = conn.cursor()
    c.execute("INSERT INTO blockchain VALUES (?, ?, ?, ?, ?, ?);", [index, str(previoushash), str(timestamp), str(data), str(hashnonce[0]), str(hashnonce[1])])
    conn.commit()
    conn.close()
    print("\033[KGenesis Block mined! - '" + str(data) + "' - " + str(hashnonce[1]))
    #print(str(index) + " | " + str(previoushash) + " | " + str(timestamp) + " | " + str(data) + " | " + str(hashnonce[0]) + " | " + str(hashnonce[1]))

def mineBlock(data):
    global stopAnimation
    global currentIndex

    conn = sqlite3.connect('miniBlockchain.db')
    c = conn.cursor()
    c.execute("SELECT * FROM blockchain ORDER BY blockid DESC LIMIT 1;")
    latestblock = c.fetchall()
    latestblock = latestblock[0]

    index = latestblock[0] + 1
    currentIndex = index
    timestamp = int(time.time())
    previoushash = latestblock[4]

    hashnonce = generateHash(index, previoushash, timestamp, data)

    conn = sqlite3.connect('miniBlockchain.db')
    c = conn.cursor()
    c.execute("INSERT INTO blockchain VALUES (?, ?, ?, ?, ?, ?);", [index, str(previoushash), str(timestamp), str(data), str(hashnonce[0]), str(hashnonce[1])])
    conn.commit()
    conn.close()
    print("\033[K#" + str(index) + " Block mined! - '" + str(data) + "' - " + str(hashnonce[1]))
    #print(str(index) + " | " + str(previoushash) + " | " + str(timestamp) + " | " + str(data) + " | " + str(hashnonce[0]) + " | " + str(hashnonce[1]))

createDB()
conn = sqlite3.connect('miniBlockchain.db')
c = conn.cursor()
c.execute("select * from blockchain")
data = c.fetchall()

t = threading.Thread(target=miningAnimation)
t.daemon = True
t.start()

if len(data) == 0:
    mineGenesisBlock()

for line in chainContents:
    mineBlock(line)

print("Done!")
