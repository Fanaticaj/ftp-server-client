import socket
import multiprocessing as mp
import os
import time
import threading

# Constants
CONTROLLED_PORT = 1026
DATA_PORT = 1025
FAIL = -1
BUFFER_SIZE = 45 

# Global mutex
mutex = threading.Lock()

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
            tmpBuff =  sock.recv(numBytes).decode('utf-8')
            # The other side has closed the socket
            if not tmpBuff:
                break
            # Add the received bytes to the buffer
            recvBuff += tmpBuff
        response = "OK"
        sock.send(response.encode())
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

        # GET creates, a new data socket, waits for the client to connect and sends the desired file to the clients.
        if data.startswith("GET"):

            # Split the request from the Client to get the File the client the client is requesting
            list_data = data.split(' ')

            # Create a new data socket that the client will connect to
            s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_data.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print(colors.OKGREEN + "[+] Data Socket created succesfully." + colors.ENDC)
            s_data.bind(tuple_data_port)
            print(colors.OKGREEN + "[+] Data Socket bound succesfully." + colors.ENDC)
            s_data.listen()
            print(colors.OKGREEN + "[+] Data Socket awaiting client connections..." + colors.ENDC)

            # Accept the Clients connection
            while len(clients_data) != 1:
                con_data, c_addr_data = s_data.accept()
                clients_data.append(con_data)
                print(colors.OKBLUE + "[+] Client connected to data port, total Clients: " + colors.ENDC + str(len(clients_data)))

            # Open the requested file
            with open("server-files/" + list_data[1], "r") as f:
                data = f.read(BUFFER_SIZE) 
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
                con_data.send(data.encode())
                f.close()
                print(colors.OKBLUE + "File Sent to Client" + colors.ENDC)
                s_data.close()
                con_data.close()

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

            # Recieve first segment
            file_data = con_data.recv(BUFFER_SIZE)
            fileName = recvAll(con_data, 25)
            fileName = fileName.replace(" ", "")
            print("File name is: ", fileName)
            newFile = open("server-files/" + fileName, "w")
            # size of the file
            fileSizeBuff = recvAll(con_data, 10)
            # Get the file size
            fileSize = int(float(fileSizeBuff))
            print("The file size is ", fileSize)
            # Get the file data
            fileData = recvAll(con_data, BUFFER_SIZE - 35)
            newFile.write(fileData)
            print("Received the first ", BUFFER_SIZE - 35, "bytes")
            i = BUFFER_SIZE - 35
            newFile.close()
            newFile = open("server-files/" + fileName, "a")
            while(i < fileSize):
                    # Receive data
                    recvAll(con_data, 35)
                    if (i + BUFFER_SIZE - 35 < fileSize):
                          fileData = recvAll(con_data, BUFFER_SIZE - 35)
                    else:
                          fileData = recvAll(con_data, fileSize - BUFFER_SIZE - 35)
                    newFile.write(fileData)
                    if (i + BUFFER_SIZE - 35 > fileSize):
                        print("Received the first ", fileSize, "bytes")
                    else:
                        print("Received the first ", i + BUFFER_SIZE - 35, "bytes")
                    i += BUFFER_SIZE - 35
            # Print confirmation and close file
            print("New file: " + fileName + " was added to the server")
            newFile.close()
            # for _ in range(5):
            #     # Receive data from the client
            #     data = con_data.recv(1024).decode('utf-8')
            #     print(f"Received data from client: {data}")

            #     # Send an 'OK' response to the client
            #     response = "OK"
            #     con_data.send(response.encode('utf-8'))
            #     print(f"Sent response to client: {response}")

            # con_data.shutdown(socket.SHUT_RDWR)
            con_data.close()  # Close the connection socket after receiving data
            # s_data.shutdown(socket.SHUT_RD)
            # print(s_data.type)
            s_data.close()    # Close the server socket
            # print("closed successfully")

            print(colors.OKGREEN + "[+] File received successsfully." + colors.ENDC)

        if data == "QUIT":
                print("QUIT")
                print(colors.OKGREEN + "[+] Closing socket and connection." + colors.ENDC)
                s_controlled.close()
                print(colors.OKGREEN + "[+] Socket and connection closed succesfully." + colors.ENDC)
                print(colors.OKGREEN + "[+] Goodbye" + colors.ENDC)
                break

            
if __name__ == "__main__":
    main()