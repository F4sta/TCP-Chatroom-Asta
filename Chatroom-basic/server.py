import socket
import threading
from os import system
import logging
import time
DYNAMICHOST = socket.gethostbyname(socket.gethostname())
LOCALHOST = "127.0.0.1"
PORT = 10000

logging.basicConfig(level=logging.INFO, format="|%(asctime)s| %(message)s")
logger = logging.getLogger("Asta")
fileHandler = logging.FileHandler("log.log")
fileHandler.setLevel(level=logging.INFO)
logger.addHandler(fileHandler)
formatter = logging.Formatter("|%(asctime)s| %(message)s")
fileHandler.setFormatter(formatter)

system("cls")
print(
    '_________________________________________________\n'
    '\n'
    '░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░\n'
    '██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗\n'
    '╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝\n'
    '░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗\n'
    '██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║\n'
    '╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝\n'
    '_________________________________________________\n'
    '\n'
    f'  Host: {DYNAMICHOST}:{PORT}\n'
    '_________________________________________________\n'
)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((DYNAMICHOST, PORT))
server.listen()

clients = []
nicknames = []
addresses = []

def broadcast(message):
    decoded_message = message.decode('utf-8')
    logger.info("|Chat| " + decoded_message)
    for client in clients:
        client.send(("|Chat| " + decoded_message).encode('utf-8'))

def disconnect(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    logger.info("|Server| " + f"{nickname} disconnected!")
    for client in clients:
        client.send(("|Server| " + f"{nickname} disconnected!").encode('utf-8'))
    nicknames.remove(nickname)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            disconnect(client)
            break
        
def receive():
    while True:
        client, address = server.accept()
        logger.info(f"|Server| {address[0]} connected to the server.")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        ip, pid = address
        addresses.append(ip)

        logger.info(f"|Server| {address[0]} nickname is {nickname}")
        client.send('|Server| Connected to server!'.encode('utf-8'))
        
        online_users = {nicknames[i]: addresses[i] for i in range(len(nicknames))}
        del online_users[nickname]
        print(online_users.keys())
        if str(online_users.keys()) == "dict_keys([])":
            client.send('|Server| There are no online users.'.encode('utf-8'))
        else:
            client.send('|Server| Online Users:'.encode('utf-8'))
            for i , l in online_users.items():
                client.send(f'   {i} ({l})'.encode('utf-8'))
            
        for client in clients:
            logger.info("|Server| " + f"{nickname} joined!")
            client.send(("|Server| " + f"{nickname} joined!").encode('utf-8'))
        

        thread = threading.Thread(target=lambda: handle(client))
        thread.start()

if __name__ == '__main__':
    receive()