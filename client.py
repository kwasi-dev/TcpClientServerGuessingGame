from socket import socket, AF_INET,SOCK_STREAM

serverName = "localhost"
serverPort=12009

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

while 1:
    numStr = input(f"(Input a number: ")

    clientSocket.send(bytes(numStr, "utf-8"))

    print ("Sent to Server: ", numStr)

    svrResp = clientSocket.recv(1024)
    svrRespStr = svrResp.decode()
    print ("Received from Server: ", svrResp)

    if svrRespStr == "You're correct":
        break

clientSocket.close()
