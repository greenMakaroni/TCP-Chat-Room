import socket
import threading

# prompt for nickname
nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect client to the server
client.connect(('127.0.0.1', 30001))

# receive and write to chat functions will run simultaneously, first listens for messages and the second expects an input and sends it

# receive messages
# listen for messages in an infinite loop
def receive():
    while True:
        try:
            # receive and decode the message
            message = client.recv(1024).decode('ascii')

            # check if the server asks for the nickname
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# write message
# run input function in an infinite loop 
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# create receive and write threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()