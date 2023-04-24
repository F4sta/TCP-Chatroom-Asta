import socket
import threading
from sys import exit as sysExit
from sys import argv
from os import system
import logging
import json

def server():
    DYNAMICHOST = socket.gethostbyname(socket.gethostname())
    try:
        PORT = int(argv[1])
    except:
        PORT = 10000

    system("mode 100, 40")
    system("cls")
    print(
        '___________________________________________________________________________________________________\n'
        '                                                                                                   \n'
        '                         ░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░                         \n'
        '                         ██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗                         \n'
        '                         ╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝                         \n'
        '                         ░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗                         \n'
        '                         ██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║                         \n'
        '                         ╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝                         \n'
        '___________________________________________________________________________________________________\n'
        f'                         Host: {DYNAMICHOST}:{PORT}\n'
    )

    #setting up logger
    logging.basicConfig(level=logging.INFO, format="|%(asctime)s| %(message)s")
    logger = logging.getLogger("Asta")
    fileHandler = logging.FileHandler("log/log.log")
    fileHandler.setLevel(level=logging.INFO)
    logger.addHandler(fileHandler)
    formatter = logging.Formatter("|%(asctime)s| %(message)s")
    fileHandler.setFormatter(formatter)

    #hosting server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((DYNAMICHOST, PORT))
        server.listen()
    except:
        print('Couldnt start server, because the port is already in used.')
        sysExit()
        exit()

    class Data():

        def export_data(json_data):
            with open("data/data.json", "w", encoding="utf-8") as data_file:
                json.dump(json_data, data_file, indent=4)
        
        def import_data():
            with open("data/data.json", "r", encoding="utf-8") as data_file:
                data = json.load(data_file)
                return data

    class Users:
        def register(database, username : str, password : str, uuid : str, rank : str):
            user_data = {
                "Username" : username,
                "Password" : password,
                "Rank" : rank,
                "uuid" : uuid
            }
            database.append(user_data)

        def check(database, username : str, password : str, uuid : str):
            for i in range(len(data)):
                if uuid == database[i]["uuid"]:
                    if username == database[i]["Username"]:
                        if password == database[i]["Password"]:
                            return True
                        else:
                            return False
                    else:
                        return False
            return False

        def check_rank(database, username, uuid):
            for i in range(len(database)):
                if uuid == database[i]["uuid"]:
                    if username == database[i]["Username"]:
                        return database[i]["Rank"]


    class OnlineUsers():
        def get(username, client):
            online_users = {usernames[i]: addresses[i] for i in range(len(usernames))}
            return online_users

        def display(online_users, client):
            if str(online_users.keys()) == "dict_keys([])":
                client.send('|Server| There are no online users.'.encode('utf-8'))
            else:
                client.send('|Server| Online Users:'.encode('utf-8'))
                for i , l in online_users.items():
                    client.send(f'   {i} ({l})'.encode('utf-8'))

    class Rank():
        class Admin():
            def help():
                pass
            def ban():
                pass
            def unban():
                pass
            def kick():
                pass
            def status():
                pass
            def online_users():
                pass
            def leave():
                pass
            
            def delete_server(self):
                pass
            
            def commands(c):
                if c == "/delete-server":
                    pass
                else:
                    pass
            
        class User():
            def help():
                pass
            def online_users():
                pass
            def leave():
                pass
            def commands(c):
                print('commands has been executed')

    clients = []
    usernames = []
    addresses = []
    try:
        data = Data.import_data()
    except:
        data = []
        Data.export_data(data)

    def broadcast(message, username, uuid):
        decoded_message = message.decode('utf-8')
        logger.info("|Chat| " + decoded_message)
        
        #Check for command
        c = decoded_message[(len(username) + 2):]
        if c.startswith("/"):
            print("command type've been found")
            if Users.check_rank(data, username, uuid) == "Admin":
                Rank.Admin.commands(c)
            
            elif Users.check_rank(data, username, uuid) == "User":
                Rank.User.commands(c)
            
            else:
                logger.info("|Server| ERROR:DIDNT FIND RANK")
        else:
            for client in clients:
                client.send(("|Chat| " + decoded_message).encode('utf-8'))

    def disconnect(client):
        index = clients.index(client)
        clients.remove(client)
        client.close()
        username = usernames[index]
        address = addresses[index]
        logger.info("|Server| " + f"{username} disconnected!")
        for client in clients:
            client.send(("|Server| " + f"{username} disconnected!").encode('utf-8'))
        usernames.remove(username)
        addresses.remove(address)

    def handle(client, username, uuid):
        while True:
            try:
                message = client.recv(1024)
                broadcast(message, username, uuid)
            except:
                disconnect(client)
                break

    def receive():
        while True:
            try:
                client, address = server.accept()
                ip, pid = address
                
                logger.info(f"|Server| {address[0]} connected to the server.")

                #Request uuid/username/password
                client.send('UUID'.encode('utf-8'))
                uuid = client.recv(1024).decode('utf-8')
                client.send('USERNAME'.encode('utf-8'))
                username = client.recv(1024).decode('utf-8')
                client.send('PASSWORD'.encode('utf-8'))
                password = client.recv(1024).decode('utf-8')
                #login
                if Users.check(data, username, password, uuid):
                    client.send('|Server| Connected to server!'.encode('utf-8'))
                else:
                    Users.register(data, username, password, uuid, rank="User")
                    
                    client.send('|Server| You didnt had an account yet, but we created it for you.'.encode('utf-8'))
                    client.send(f'|Server| Username: {username} | Password: {password}'.encode('utf-8'))
                    Data.export_data(data)
                
                usernames.append(username)
                clients.append(client)
                addresses.append(ip)

                logger.info(f"|Server| {address[0]} logged in")
                logger.info(f"|Server| {address[0]} name is {username}")
                OnlineUsers.display(OnlineUsers.get(username, client), client)
                logger.info("|Server| " + f"{username} joined!")
                for client in clients:
                    client.send(("|Server| " + f"{username} joined!").encode('utf-8'))

                thread = threading.Thread(target=lambda: handle(client, username, uuid))
                thread.start()
            except:
                pass
    
    receive()

if __name__ == '__main__':
    server()