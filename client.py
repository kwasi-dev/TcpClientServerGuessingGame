from socket import socket, AF_INET,SOCK_STREAM
import threading


serverName = "localhost"
serverPort=12009

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

def handle_server_messages(socket):
    while True:
        svrResp = clientSocket.recv(1024)
        svrRespStr = svrResp.decode()
        print ("Received from Server: ", svrRespStr)



thread_handler = threading.Thread(target=handle_server_messages, args=(clientSocket,))
thread_handler.start() 
 
while 1:
    numStr = input(f"(Input: ")

    clientSocket.send(bytes(numStr, "utf-8"))

clientSocket.close()
