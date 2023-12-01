import socket
import multiprocessing as mp
import os
import time
import threading
import argparse

# Constants
CONTROLLED_PORT = 1026
DATA_PORT = 1025
FAIL = -1
BUFFER_SIZE = 45 

# Gobal mutex
mutex = threading.Lock()

# Portnumber stuff
parser = argparse.ArgumentParser()
parser.add_argument('port_number', metavar='N', type=int,
                    nargs=1, default=CONTROLLED_PORT)
args = parser.parse_args()

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
        print(colors.OKGREEN + "[+] Data Socket created succesfully." + colors.ENDC)
    
    except socket.error as err:
        print(colors.FAIL + "[-] Data Socket creation failed - " + err + colors.ENDC)
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

def recvAll(sock, numBytes):
	# The buffer
	recvBuff = ""
	# The temporary buffer
	tmpBuff = ""
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes).decode()
		# The other side has closed the socket
		if not tmpBuff:
			break
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	return recvBuff

def request_get(server_connection, filename):
    # Send GET command
    server_connection.sendall(f'GET {filename}'.encode() + b'\n')

    # Receive file size
    file_size = int(server_connection.recv(1024).decode().strip())

    if file_size == 0:
        print(f"File not found: {filename}")
        return

    # Receive file data
    received_size = 0
    file_data = b''
    while received_size < file_size:
        chunk = server_connection.recv(1024)
        if not chunk:
            break 
        file_data += chunk
        received_size += len(chunk)

    if file_data == "File transfer from server failed...":
        return False
    
    with open('./client-files/' + filename, 'wb') as file:
        file.write(file_data)
        print("File size is: " + str(file_size))
        print("New File: " + filename + " was added to the Client")
        return True

def validate_input(user_input):
    if(user_input == 'QUIT' or user_input == 'LS' or user_input == 'GET' or user_input == 'PUT'):
        return True
    else:
        print(colors.WARNING + "[-] Invalid input" + colors.ENDC)
        return False
                


def main ():
    
    address = '127.0.0.1'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)

    s.connect((address, args.port_number[0]))
    print(colors.OKGREEN + "[+] Connected to server successfully..." + colors.ENDC)

    print(colors.OKBLUE + "Please enter a command..." + colors.ENDC)
    while True:
    
        valid_input = False

        while valid_input != True:
            user_input = input()
            list_user_input = user_input.split(' ')
            valid_input = validate_input(list_user_input[0])

        s.send(str(user_input).encode())
        time.sleep(1)

        if user_input.startswith("GET"):

            c_data = init_ftp_data_socket((address, DATA_PORT))
            if (request_get(c_data, list_user_input[1])): 
                c_data.close()

            else:
                 print(colors.FAIL + "File transfer from server failed.." + colors.ENDC)
                 continue

        if user_input.startswith("PUT"):
            list_user_input = user_input.split(' ')
            c_data = init_ftp_data_socket((address, DATA_PORT))
            time.sleep(1) # Wait for server to start up

            with open("client-files/" + list_user_input[1], "r") as f:
                i = 0
                data = f.read()
                fileSize = len(data)
                print("File size is: ", fileSize)
                
                while True:
                    if (i + BUFFER_SIZE - 35 > fileSize):
                         sendData = data[i:fileSize]
                    elif (i + BUFFER_SIZE - 35 < fileSize):
                        sendData = data[i:(i + BUFFER_SIZE - 35)]
                    else:
                        #  print("break 1")
                         break
                    # print(f'Send data is {sendData}')
                    dataSizeStr = str(fileSize)
                    if (len(dataSizeStr) >= 10):
                        print(colors.FAIL + "[-] File size too big" + colors.ENDC)
                        break
                    while len(dataSizeStr) < 10:
                        dataSizeStr = "0" + dataSizeStr
                    FileName = list_user_input[1]
                    if (len(FileName) > 25):
                            print("File name is too large")
                            break
                    FileStr = FileName
                    while len(FileStr) < 25:
                            FileStr = " " + FileStr
                    if fileSize < i:
                        # print("break 2")
                        break
                    sendData = FileStr + dataSizeStr + sendData
                    # print(f"Send data is: {sendData}")
                    if (i + BUFFER_SIZE - 35 > fileSize):
                        print("Sent the first ", fileSize, "bytes")
                    else:
                        print("Sent the first ", i + BUFFER_SIZE - 35, "bytes")
                    i += BUFFER_SIZE - 35
                    c_data.send(sendData.encode())
                    # response = c_data.recv(4).decode()
                    # print(response)
                f.close()
                print(colors.OKBLUE + "File Sent to Server" + colors.ENDC)

        elif user_input == "QUIT":
             c_data.close()
             print(colors.OKGREEN + "[+] Connection closed" + colors.ENDC)
             print(colors.OKGREEN + "[+] Closing Program..." + colors.ENDC)
             break

        else:
            data = s.recv(1024).decode()
            print(data)
    print(colors.OKGREEN + "[+] Goodbye" + colors.ENDC)

if __name__ == "__main__":
    main()