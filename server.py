import threading
import socket

# server address, local host
host = '127.0.0.1' 
port = 30001

# create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# assign IP and port to the server
server.bind((host, port))

# start server
server.listen()

# clients connected to the server
clients = []
# nicknames associated with clients
nicknames = []

# broadcast function / send a message to all the clients connected to this server
def broadcast(message):
    for client in clients:
        client.send(message)

# handle receiving messages from client
def handle(client):
    while True:
        try:
            # receive message
            message = client.recv(1024) # 1024 bytes

            # broadcast the message to all other clients
            broadcast(message)
        except: 
            # get index of the client
            index = clients.index(client)

            # remove client from the client list
            clients.remove(client)

            # close client connection
            client.close()
            
            # get client's nickname index 
            nickname = nicknames[index]

            # broadcast message that client left the chat
            broadcast(f"{nickname} left the chat!".encode('ascii'))

            # remove client's nickname
            nicknames.remove(nickname)
            break
# every client will be handled by his own thread that will listen to messages of this client,
# on error, the handle function disconnects the client.

# main method
def receive():
    # When clients connect, get the client and their address
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # prompt client to insert his nickname
        client.send("NICK".encode('ascii'))
        
        # receive the nickname and push it to the nicknames array
        # append client to the clients array
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # print who connected into console
        # broadcast message to all clients that new client connected to the chat
        print(f"Nickname of the client is: {nickname}")
        broadcast(f"{nickname} just joined to the chat!".encode('ascii'))

        # send welcome message
        client.send("Welcome to the chat!".encode('ascii'))

        # create thread for each client connected
        # if multiple clients send the messages, they need to be handled roughly at the same time
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# call main method

print(f"Server is listening at port: { port }")
receive()
