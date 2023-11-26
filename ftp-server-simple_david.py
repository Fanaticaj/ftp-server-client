import socket
import multiprocessing as mp
import os
import time

# Constants
CONTROLLED_PORT = 1026
DATA_PORT = 1025
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

def main ():
    
    address = '127.0.0.1'
    tuple_address_port = (address, CONTROLLED_PORT)
    tuple_data_port = (address, DATA_PORT)
    clients = []
    clients_data = []
    
    # Create, Bind, and Listen on the Control Socket
    s_controlled = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_controlled.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # added to fix the address already in use issue
    print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)
    s_controlled.bind(tuple_address_port)
    print(colors.OKGREEN + "[+] Socket bound succesfully." + colors.ENDC)
    s_controlled.listen()
    print(colors.OKGREEN + "[+] Awaiting client connections..." + colors.ENDC)

    # TODO: Currently, only accepts a single single client I think we may need to go multi-threaded / multi-process to accept multile clients
    # After the control socket is created and bound, we listen and accept client connections.
    while len(clients) != 1:
            con, c_addr = s_controlled.accept()
            clients.append(con)
            print(colors.OKBLUE + "[+] Client connected, total Clients: " + colors.ENDC + str(len(clients)))
    
    # Command decoding section
    while True:        
        data = con.recv(1024).decode()

        # LS sends a list of files located in the server-files direcory
        if data == "LS":
            print(data)
            con.send(str(os.listdir("./server-files")).encode())

        #TODO: Allow GET To accept arguments for specific files in the direcory. Also, get the data sending working.
        # GET creates, a new data socket, waits for the client to connect and sends the desired file to the clients.
        if data.startswith("GET"):

            list_data = data.split(' ')
            s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print(colors.OKGREEN + "[+] Data Socket created succesfully." + colors.ENDC)
            s_data.bind(tuple_data_port)
            print(colors.OKGREEN + "[+] Data Socket bound succesfully." + colors.ENDC)
            s_data.listen()
            print(colors.OKGREEN + "[+] Data Socket awaiting client connections..." + colors.ENDC)

            while len(clients_data) != 1:
                con_data, c_addr_data = s_data.accept()
                clients_data.append(con_data)
                print(colors.OKBLUE + "[+] Client connected to data port, total Clients: " + colors.ENDC + str(len(clients_data)))

            with open("server-files/" + list_data[1], "r") as f:
                data = f.read(BUFFER_SIZE)
                print(data)
                dataSizeStr = str(len(data))
                while len(dataSizeStr) < 10:
                       dataSizeStr = "0" + dataSizeStr
                FileName = list_data[1]
                if (len(FileName) > 25):
                        print("File name is too large")
                        break
                FileStr = FileName
                while len(FileStr) < 25:
                           FileStr = " " + FileStr
                data = FileStr + dataSizeStr + data
                con_data.send(data.encode())    # Close the server socket
                f.close()
                print(colors.OKBLUE + "File Sent to Client" + colors.ENDC)

        # PUT will allow the client to upload a file to the server.
        if data.startswith("PUT"):
            clients_data = []
            s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # added to fix the address already in use issue
            print(colors.OKGREEN + "[+] Data Socket created successfully." + colors.ENDC)
            s_data.bind(tuple_data_port)
            print(colors.OKGREEN + "[+] Data Socket bound successfully." + colors.ENDC)
            s_data.listen()
            print(colors.OKGREEN + "[+] Data Socket awaiting client connections..." + colors.ENDC)

            while len(clients_data) != 1:
                con_data, c_addr_data = s_data.accept()
                clients_data.append(con_data)
                print(colors.OKBLUE + "[+] Client connected to data port, total Clients: " + colors.ENDC + str(len(clients_data)))

            file_data = con_data.recv(BUFFER_SIZE)
            fileName = recvAll(con_data, 25)
            fileName = fileName.replace(" ", "")
            print("File name is: ", fileName)
            newFile = open("server-files/" + fileName, "wb")
            # size of the file
            fileSizeBuff = recvAll(con_data, 10)
            # Get the file size
            fileSize = int(float(fileSizeBuff))
            print("The file size is ", fileSize)
            # Get the file data
            fileData = recvAll(con_data, fileSize)
            newFile.write(fileData)
            print("New file: " + fileName + " was added to the server")
            newFile.close()

            # con_data.shutdown(socket.SHUT_RDWR)
            con_data.close()  # Close the connection socket after receiving data
            # s_data.shutdown(socket.SHUT_RD)
            # print(s_data.type)
            s_data.close()    # Close the server socket
            # print("closed successfully")

            print(colors.OKGREEN + "[+] File received successfully." + colors.ENDC)

            
if __name__ == "__main__":
    main()