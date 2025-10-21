from socket import socket, AF_INET,SOCK_STREAM
import random 

serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print ("The Server is running ... ")
secretNumber = random.randint(1,100)
while 1:
    connectionSocket, addr = serverSocket.accept()
    
    while 1:
        clientMessageBytes = connectionSocket.recv(1024)

        if not clientMessageBytes:
           print("Client disconnected")
           break
        

        clientMessageStr = clientMessageBytes.decode()
        serverResponse = ""
        
        try:
          clientMessageInt = int(clientMessageStr)
              
          print ("Received: ", clientMessageStr)
          if clientMessageInt == secretNumber:
              serverResponse = "You're correct"
          elif clientMessageInt < secretNumber:
              serverResponse = "Too Low"
          else:
              serverResponse = "Too High"
             
          print ("Sent: ", serverResponse)
        except Exception as e:
          serverResponse = "Invalid number entered"
        try: 
          connectionSocket.send(bytes(serverResponse, "utf-8"))
        except Exception as e:
           print("Client disconnected")
           break