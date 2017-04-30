#!/router/bin/python3           
# This is server.py file

from socket import *                         # Import socket module
from threading import Thread                 # Import Thread module
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)
RECV_BUFFER_LIMIT = 2048
first_response = str("SERVER>>").encode('ascii')

clients = []
groups = {}

def joinGroup(client, request):
    if request in groups:
        clientList = groups[request]
        if client not in clientList:
            clientList.append(client)
    else:
         groups[request] = [client]
         broadcastGroups(client, str(client) + " joined the group")

def broadcastGroups(client, msg):
    msg = str(msg).encode('ascii')
    for client in clients:
        client.send(msg)

def multicastGroups(client, msg):
    msg = str(msg).encode('ascii') 
 
def panicHandler(client, request):
    msg = "Invalid Request: " + str(request)
    msg = msg.encode('ascii')
    client.send(msg)            

def processInput(client, request):
    msgList  = request.split(" ",1)
    key = int(msgList[0])
    msg = str(msgList[-1])
    switcher = { 
        0: joinGroup,
        1: broadcastGroups,
#        2: multicastGroups,
 #       3: privateMsg
    }
    function = switcher.get(key, panicHandler)
    function(client, msg)
      
def server(address):
    sock = socket(AF_INET, SOCK_STREAM)          # Create a socket object
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Set socket options
    sock.bind(address)                           # Bind to the port
    sock.listen(5)                               # Now wait for client connection.
    while True:
        client, addr = sock.accept()      # Establish connection with client.
        print("Connection to ",addr);
        clients.append(client)
        Thread(target=client_handler, args=(client,), daemon=True).start()


def client_handler(client):
    while True:
        client.send(first_response)
        request = client.recv(RECV_BUFFER_LIMIT)
        if not request:
            print("Closing connection")
            break
        processInput(client, request.decode('utf-8'))
    print("Done!")

server(('',12345))

