import socket
import multiprocessing as mp
import os
import time

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

def command_listener(s_controlled, clients):
    
    print()
   # while True:
            

def main ():
    
    address = '127.0.0.1'
    tuple_address_port = (address, CONTROLLED_PORT)
    clients = []
    

    s_controlled = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)
    s_controlled.bind(tuple_address_port)
    print(colors.OKGREEN + "[+] Socket bound succesfully." + colors.ENDC)
    s_controlled.listen()
    print(colors.OKGREEN + "[+] Awaiting client connections..." + colors.ENDC)

    while len(clients) != 1:
            con, c_addr = s_controlled.accept()
            clients.append(con)
            print(colors.OKBLUE + "[+] Client connected, total Clients: " + colors.ENDC + str(len(clients)))
    
    while True:        
        data = con.recv(1024).decode()
        if data == "LIST":
             con.send(str(os.listdir("./files")).encode())

        if data == "GET":
            with open("files/test.txt", "rb") as f:
                file_data = f.read(BUFFER_SIZE)
                print(file_data)
                while file_data:
                    con.send(file_data)
                    file_data = f.read(BUFFER_SIZE)
                f.close()

            print(colors.OKGREEN + "[+] File sent successfully." + colors.ENDC)
            
if __name__ == "__main__":
    main()