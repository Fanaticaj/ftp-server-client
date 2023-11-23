import socket
import multiprocessing as mp
import os
import time

# Constants
CONTROLLED_PORT = 21
DATA_PORT = 20
FAIL = -1

# Makes my strings pretty
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Create socket and binds to address the Control port is defined in the Contants section
def init_ftp_controlled_socket(tuple_address_port):
    
    # Create TCP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)
    
    except socket.error as err:
        print(colors.FAIL + "[-] Socket creation failed - " + err + colors.ENDC)
        return FAIL

    # Bind TCP socket
    try:
        s.bind(tuple_address_port)
        print(colors.OKGREEN + "[+] Socket bound succesfully." + colors.ENDC)
        return s

    except socket.error as err:
        print(colors.FAIL + "[-] Socket binding failed - " + str(err) + colors.ENDC)
        return FAIL

# Multiprocessing Client handler
def client_listener(s_controlled, clients):
    print(colors.OKGREEN + "[+] Awaiting client connections..." + colors.ENDC)
    
    while True:
            con, c_addr = s_controlled.accept()
            clients.append(con)
            print(colors.OKBLUE + "[+] Client connected, total Clients: " + colors.ENDC + str(len(clients)))
            
            try:
                data = con.recv(1024)

            except socket.error as err:
                print(colors.FAIL + "[-] Socket binding failed - " + str(err) + colors.ENDC)
                return FAIL

def command_listener(con, clients):
    
    while True:
        data = con.recv(1024)
        print()
            

def main ():
    
    address = '127.0.0.1'
    clients = []

    s_controlled = init_ftp_controlled_socket((address, CONTROLLED_PORT))
    s_controlled.listen()
    
    ctx = mp.get_context('spawn')
    p = ctx.Process(target=client_listener, args=(s_controlled, clients))
    p.start()

    ctx2 = mp.get_context('spawn')
    q = ctx2.Process(target=command_listener, args=(s_controlled, clients))
    q.start()
    q.join()

if __name__ == "__main__":
    main()