import socket
import multiprocessing as mp
import os

# Constants
CONTROLLED_PORT = 21
DATA_PORT = 20
FAIL = -1
BUFFER_SIZE = 4096 

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

def main ():
    
    address = '127.0.0.1'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)

    s.connect((address, CONTROLLED_PORT))
    print(colors.OKGREEN + "[+] Connected to server successfully..." + colors.ENDC)
    #s.send(str((address, CONTROLLED_PORT)).encode())

    print(colors.OKBLUE + "Please enter a command..." + colors.ENDC)
    while True:
        user_input = input()
        s.send(str(user_input).encode())

        if user_input == "GET":
            with open("received_test.txt", "wb") as f:  # "received_test.txt" is the name of the file where you'll save the received data
                data = s.recv(BUFFER_SIZE)
                print(data)
                while data:
                    f.write(data)
                    data = s.recv(BUFFER_SIZE)
                f.close()
            print(colors.OKGREEN + "[+] File received successfully." + colors.ENDC)
        else:
            data = s.recv(1024).decode()
            print(data)

if __name__ == "__main__":
    main()