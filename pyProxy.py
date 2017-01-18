import socket, sys
from thread import *

canBreak = False
while not canBreak:
    try:
        listening_port = int(raw_input("[*] Enter listening port number: "))
        canBreak = True
    except KeyboardInterrupt:
        print "\n[*] KeyboardInterrupt - exiting..."
        sys.exit()

max_conn = 5
buffer_size = 8192

def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "[*] Socket initialized..."
        s.bind(('', listening_port))
        s.listen(max_conn)
        print "[*] Socket binded to port " + str(listening_port) + "..."
    except Exception, e:
        print "[*] Failed to initialize socket, exiting..."
        sys.exit(2)

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            start_new_thread(conn_string, (conn,data,addr))
        except KeyboardInterrupt:
            print "\n[*] KeyboardInterrupt - exiting..."
            sys.exit()

def conn_string(conn, data, addr):
    try:
        first_line = data.split("\n")[0]
        url = first_line.split(" ")[1]
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos+3):]

        port_pos  = temp.find(':')

        webserver_pos  = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver  = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        proxy_server(webserver, port, conn, addr, data)
    except Exception, e:
        pass

def proxy_server(webserver, port, conn, addr, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)

        print "[*] Request sent: \n" + data

        while True:
            reply = s.recv(buffer_size)
            if len(reply) > 0:
                conn.send(reply)
                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print "[*] Request done to %s => %s <=" % (str(webserver), str(dar))
            else:
                break
        s.close()
        print "[*] Closing a socket..."
        conn.close()
    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit()

start()