import socket
import multiprocessing as mp
import os
import time

# Constants
BUFFER_SIZE = 1024
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

# Create socket and connects to address the Control port is defined in the Contants section
def init_ftp_controlled_socket(tuple_address_port):
    
    # Create TCP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)
    
    except socket.error as err:
        print(colors.FAIL + "[-] Socket creation failed - " + err + colors.ENDC)
        return FAIL
 
    # Connect to TCP socket
    try:
        s.connect(tuple_address_port)
        print(colors.OKGREEN + "[+] Connected to server successfully..." + colors.ENDC)
        s.send(str(tuple_address_port).encode())
        return s

    except socket.error as err:
        print(colors.FAIL + "[-] Connecting to server failed" + colors.ENDC)
        print(err)
        return FAIL

def init_ftp_data_socket(tuple_address_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)
    
    except socket.error as err:
        print(colors.FAIL + "[-] Socket creation failed - " + err + colors.ENDC)
        return FAIL
 
    # Connect to TCP socket
    try:
        s.connect(tuple_address_port)
        print(colors.OKGREEN + "[+] Connected to server successfully..." + colors.ENDC)
        s.send(str(tuple_address_port).encode())
        return s

    except socket.error as err:
        print(colors.FAIL + "[-] Connecting to server failed" + colors.ENDC)
        print(err)
        return FAIL

def main ():
    
    address = '127.0.0.1'

    c_controlled = init_ftp_controlled_socket((address, CONTROLLED_PORT))

    print(colors.OKBLUE + "Please enter a command..." + colors.ENDC)
    while True:
        user_input = input()
        c_controlled.send(str(user_input).encode())

        if user_input.startswith("PUT"):
            list_user_input = user_input.split(' ')
            c_data = init_ftp_data_socket((address, DATA_PORT))
            time.sleep(1) # Wait for server to start up

            with open("client-files/" + list_user_input[1], "rb") as f:
                data = f.read()
                print(data)
                c_data.send(str(data).encode())
                f.close()
                print(colors.OKBLUE + "File Sent to Server" + colors.ENDC)

        data = c_controlled.recv(1024).decode()
        print(data)

if __name__ == "__main__":
    main()