from socket import socket, AF_INET,SOCK_STREAM, SOL_SOCKET, SO_REUSEPORT
import random 
import threading
from datetime import datetime

rooms = {}


serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
serverSocket.bind(("",serverPort))
serverSocket.listen()

print ("The Server is running ... ")


def handle_client(connectionSocket, addr):
    print(f"Thread started to handle client {addr}")

    while 1:
      clientMessageBytes = connectionSocket.recv(1024)

      if not clientMessageBytes:
          print("Client disconnected")
          break

      clientMessageStr = clientMessageBytes.decode()
      messageParts = clientMessageStr.split(",")

      if (messageParts[0] == "/create"):
          room_id = messageParts[1]
          if room_id in rooms:
            connectionSocket.send(bytes("The room already exists. Try another", "utf-8"))
          else:
            rooms[room_id] = {
                "participants": [],
                "messages": [],
                "sockets": []
            }
            connectionSocket.send(bytes("Successfully created room", "utf-8"))
      if (messageParts[0] == "/join"):
          room_id = messageParts[1]
          if not room_id in rooms:
            connectionSocket.send(bytes("The room does not exist. Try another", "utf-8"))
          else:
            rooms[room_id]["participants"].append(addr)
            rooms[room_id]["sockets"].append(connectionSocket)
            connectionSocket.send(bytes("Successfully joined room", "utf-8"))
      if (messageParts[0] == "/message"):
          room_id = messageParts[1]
          message = messageParts[2]
          if not room_id in rooms:
            connectionSocket.send(bytes("The room does not exist. Try another", "utf-8"))
            continue

          room = rooms[room_id]
          if not addr in rooms[room_id]['participants']:
              connectionSocket.send(bytes("You're not a member of that room, cant message","utf-8"))
              continue
          for ps in room['sockets']:
            ps.send(bytes(message,"utf-8"))
           


while True:
    connectionSocket, addr = serverSocket.accept()
    
    thread_handler = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    thread_handler.start() 