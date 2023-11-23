import socket
import multiprocessing as mp
import os
import time

# Constants
CONTROLLED_PORT = 21
DATA_PORT = 20
FAIL = -1
BUFFER_SIZE = 1024 

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

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)

    s.connect((address, CONTROLLED_PORT))
    print(colors.OKGREEN + "[+] Connected to server successfully..." + colors.ENDC)

    print(colors.OKBLUE + "Please enter a command..." + colors.ENDC)
    while True:
        user_input = input()
        s.send(str(user_input).encode())
        time.sleep(1)

        if user_input == "GET":

            s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(colors.OKGREEN + "[+] Data Socket created succesfully." + colors.ENDC)
            s_data.connect((address, DATA_PORT))
            print(colors.OKGREEN + "[+] Data port connected to server successfully..." + colors.ENDC)
            print(data)
            with open("./client-files/received_test.txt", "wb") as f:
                while True:
                    data = s_data.recv(BUFFER_SIZE)
                    if not data:
                        break
                f.write(data)

            print(colors.OKGREEN + "[+] File received successfully." + colors.ENDC)
            s_data.close()

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
        else:
            data = s.recv(1024).decode()
            print(data)

if __name__ == "__main__":
    main()