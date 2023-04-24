import socket
import threading
from sys import exit as sysExit
from sys import argv
from os import system
from time import sleep
from subprocess import check_output

def client():
    system("mode 100, 40")
    system("cls")
    print(
        '___________________________________________________________________________________________________\n'
        '                                                                                                   \n'
        '               ░█████╗░██╗░░██╗░█████╗░████████╗██████╗░░█████╗░░█████╗░███╗░░░███╗                \n'
        '               ██╔══██╗██║░░██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗████╗░████║                \n'
        '               ██║░░╚═╝███████║███████║░░░██║░░░██████╔╝██║░░██║██║░░██║██╔████╔██║                \n'
        '               ██║░░██╗██╔══██║██╔══██║░░░██║░░░██╔══██╗██║░░██║██║░░██║██║╚██╔╝██║                \n'
        '               ╚█████╔╝██║░░██║██║░░██║░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝██║░╚═╝░██║                \n'
        '               ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝                \n'
        '___________________________________________________________________________________________________\n'       
    )


    try:
        host = argv[1]
        port = argv[2]
    except:
        host = input('Ip: ')
        port = input("Port: ")

    uuid = check_output('wmic csproduct get uuid').decode('utf-8').split('\n')[1].strip()

    try:
        username = argv[3]
        password = argv[4]
    except:
        username = input('Username: ')
        password = input('Password: ')

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
                if message == 'UUID':
                    server.send(uuid.encode('utf-8'))
                elif message == 'USERNAME':
                    server.send(username.encode('utf-8'))
                elif message == 'PASSWORD':
                    server.send(password.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Error")
                server.close()
                sysExit()
                exit()
            
    def write():
        while True:
            Input = input()
            message = f'{username}: {Input}'
            server.send(message.encode('utf-8'))
            
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    sleep(0.5)

    write_thread = threading.Thread(target=write)
    write_thread.start()
    
if __name__ == '__main__':
    client()