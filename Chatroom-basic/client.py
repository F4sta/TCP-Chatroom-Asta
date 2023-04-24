import socket
import threading
from sys import exit as sysExit
from sys import argv
from os import system
from time import sleep

system("cls")
print(
    '____________________________________________________________________\n'
    '\n'
    '░█████╗░██╗░░██╗░█████╗░████████╗██████╗░░█████╗░░█████╗░███╗░░░███╗\n'
    '██╔══██╗██║░░██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗████╗░████║\n'
    '██║░░╚═╝███████║███████║░░░██║░░░██████╔╝██║░░██║██║░░██║██╔████╔██║\n'
    '██║░░██╗██╔══██║██╔══██║░░░██║░░░██╔══██╗██║░░██║██║░░██║██║╚██╔╝██║\n'
    '╚█████╔╝██║░░██║██║░░██║░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝██║░╚═╝░██║\n'
    '░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝\n'
    '____________________________________________________________________\n'
)

nickname = input('Choose your nickname: ')

try:
    host = argv[1]
    port = argv[2]
except:
    host = input('Ip: ')
    port = input("Port: ")
    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    port = int(port)
    server.connect((host, port))
except:
    print("Connecting failed.")
    sysExit()
    exit()

def receive():
    while True:
        try:
            message = server.recv(1024).decode('utf-8')
            if message == 'NICK':
                server.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occured!")
            server.close()
            break
        
def write():
    while True:
        Input = input()
        if Input.lower == "exit":
            sysExit()
            exit()
        else:
            message = f'{nickname}: {Input}'
            server.send(message.encode('utf-8'))
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

sleep(0.5)

write_thread = threading.Thread(target=write)
write_thread.start()