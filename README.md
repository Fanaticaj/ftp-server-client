
---

# Simple FTP Server and Client

## Project Members
Anthony Grippi - agrippi@csu.fullerton.edu  
Ethan Jones - ejonest@csu.fullerton.edu  
David Nguyen - dnguyen271@csu.fullerton.edu

## Overview
This project provides a simple FTP server and client implementation in Python. It also includes a Windows batch script for easy execution of the programs.

## Contents
1. **ftp-server-simple.py**: A Python script for the FTP server. It uses socket programming to listen for client connections and handles commands like 'LS' (to list server directory files) and 'GET' (to send files to the client).
2. **ftp-client-simple.py**: A Python script for the FTP client. It connects to the FTP server and sends commands. It supports receiving files from the server with the 'GET' command.
3. **run-simple.bat**: A Windows batch script that starts both the server and client scripts in separate command prompt windows.

## Requirements
- Python 3.x installed on your machine.
- A Windows environment to execute the batch script.

## Usage
**Running the Batch Script**:
   - Double-click on `run-simple.bat`.
   - The script opens two command prompt windows: one for the server and another for the client.
   - The server starts first, followed by the client. You may then provide the client with the following commands:
      - PUT <filename>
      - GET <filename>
      - LS
      - QUIT  
*Note: if you want to change the port number, please go in and alter the number on the port if you are using the
     batch script
**Alternatively**:
   - Open two terminals, each open to the directory that hosts the source code.
   - In the first terminal, run the following command: python3 ftp-server-simple.py <port number>
   - In the second terminal run the following command: python3 ftp-server-client.py '<IP address> <port number>'
   - You may then provide the client with the following commands:
         - PUT <filename>
         - GET <filename>
         - LS
         - QUIT
*Note: the '' in the command for the client is important 
     
### Server Implementation
#### 1. PUT
- The `PUT` command allows the client to upload a file to the server.
- The server creates a data socket and binds it to a specific port to handle file transfer.
- It accepts a connection from the client on this data socket.
- The server then receives the file name and file size from the client.
- The file data is received in chunks and written to a new file in the server's directory (`server-files/`).
- This process continues until the entire file is received and saved.

#### 2. GET
- The `GET` command is not explicitly implemented in the server code snippet provided. However, it is typically used to send a file from the server to the client upon request.

#### 3. LS
- The implementation details for the `LS` command are not visible in the provided code snippet. Generally, `LS` is used to list the files available in the server's directory.

#### 4. QUIT
- The `QUIT` command implementation is not directly visible in the server code. Typically, this command would close the connection with the client.

### Client Implementation

#### 1. PUT
- The `PUT` command functionality is to upload a file from the client to the server.
- The client sends the `PUT` command along with the file name and size to the server.
- It then reads the file and sends its data in chunks to the server.
- Once the file transfer is complete, the client prints a confirmation message.

#### 2. GET
- The `GET` command requests a file from the server.
- The client sends the `GET` command along with the file name to the server.
- It receives the file size and then starts receiving the file data in chunks.
- The received data is written to a file in the client's directory (`client-files/`).
- On completion, the client prints a success message.

#### 3. LS
- The `LS` command requests a list of files from the server.
- The server then responds with a full list of all the files in its directory.

#### 4. QUIT
- The `QUIT` command is used to close the connection with the server.
- On entering `QUIT`, the client closes the data socket and prints a message indicating that the connection is closed and the program is terminating.
