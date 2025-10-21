from socket import socket, AF_INET,SOCK_STREAM
import random 
import threading

serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen()

print ("The Server is running ... ")


def handle_client(connectionSocket, addr):
    print(f"Thread started to handle client {addr}")
    secretNumber = random.randint(1,100)

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


while True:
    connectionSocket, addr = serverSocket.accept()
    
    thread_handler = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    thread_handler.start() 