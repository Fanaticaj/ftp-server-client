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

# Gobal mutex
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

def main ():
    
    address = '127.0.0.1'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(colors.OKGREEN + "[+] Socket created succesfully." + colors.ENDC)

    s.connect((address, CONTROLLED_PORT))
    print(colors.OKGREEN + "[+] Connected to server successfully..." + colors.ENDC)

    print(colors.OKBLUE + "Please enter a command..." + colors.ENDC)
    while True:
        user_input = input()
        list_user_input = user_input.split(' ')
        s.send(str(user_input).encode())
        time.sleep(1)

        # GET will accept a file that is hosted on the server as an argument and download the file to the client-files directory 
        if user_input.startswith("GET"):
            s_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(colors.OKGREEN + "[+] Data Socket created successfully." + colors.ENDC)
            s_data.connect((address, DATA_PORT))
            print(colors.OKGREEN + "[+] Data port connected to server successfully..." + colors.ENDC)

            fileName = list_user_input[1].strip()  # Ensure no leading/trailing spaces
            filePath = os.path.join("./client-files", fileName)
    
            try:
                with open(filePath, "wb") as f:  # Use binary mode for universal compatibility
                    fileData = recvAll(s_data, BUFFER_SIZE)  # Assuming BUFFER_SIZE is the correct size
                    f.write(fileData.encode('utf-8'))  # If data is text, encode it to bytes

                    print(f"New file: {fileName} was added to the client-files directory")
                    f.close()
            except IOError as e:
                print(f"Error writing to file: {e}")

            s_data.close()
            print(colors.OKGREEN + "[+] File received successfully." + colors.ENDC)


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
                    sendData = data[i:(i + BUFFER_SIZE - 35)]
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
                    sendData = FileStr + dataSizeStr + sendData
                    c_data.send(sendData.encode())
                    if fileSize < i:
                        break
                    if (i + BUFFER_SIZE - 35 > fileSize):
                        print("Sent the first ", fileSize, "bytes")
                    else:
                        print("Sent the first ", i + BUFFER_SIZE - 35, "bytes")
                    i += BUFFER_SIZE - 35
                    # response = c_data.recv(1024).decode()
                    # print(response)
                # for _ in range(5):
                #     # Send "hello world" to the server
                #     message = "hello world"
                #     c_data.send(message.encode('utf-8'))
                #     print(f"Sent message to server: {message}")

                #     # Receive response from the server
                #     response = c_data.recv(1024).decode('utf-8')
                #     print(f"Received response from server: {response}")
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