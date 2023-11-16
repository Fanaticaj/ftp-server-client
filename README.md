
---

# Simple FTP Server and Client

## Overview
This package contains a simple FTP server and client implementation written in Python, along with a batch script to run both the server and the client on a Windows system.

## Files Description
1. **ftp-server-simple.py** - This Python script sets up a basic FTP server. It listens for client connections and can handle commands such as 'LS' (to list files in the server directory) and 'GET' (to send a file to the client). The script uses socket programming and is designed to run on a single client.

2. **ftp-client-simple.py** - The client script connects to the FTP server and sends commands to it. Currently, it supports receiving files from the server using the 'GET' command. The script demonstrates basic socket programming in Python.

3. **start-ftp.bat** - A batch script for Windows that automates the process of starting the server and client scripts. It opens two command prompt windows: one for the server and another for the client, ensuring that the server starts first.

## Usage
1. **Running the Batch Script**: 
   - Ensure Python is installed on your Windows machine.
   - Double-click on `run-simple.bat` to start both the server and client.
   - The script opens two command prompt windows, one for the server and one for the client.
   - The server will start first, followed by the client after a short delay.

2. **Server Operations**:
   - The server script will display status messages as it performs operations like socket creation, binding, and listening for client connections.
   - Once a client connects, it waits for commands like 'LS' and 'GET'.

3. **Client Operations**:
   - After starting, the client can send commands to the server.
   - Enter 'GET' to receive a file from the server. The file will be saved in a specified directory on the client-side.
   - Enter 'LS' to list files available on the server.

## Notes
- The server is currently set to handle only one client connection.
- The 'PUT' command for uploading files to the server is not implemented yet.
- Error handling and multi-client support can be added in future updates.

---