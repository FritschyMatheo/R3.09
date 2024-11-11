import socket
import time

#Configuration connexion
serveur_socket = socket.socket()
port = 10000
ip = "127.0.0.1"

#Etablissement de la connexion
serveur_socket.bind((ip, port))
serveur_socket.listen(1)
print("En attente de connexion...")

conn, address = serveur_socket.accept()
acceptation = "Connexion au serveur acceptée, vous pouvez communiquer."
conn.send(acceptation.encode())
print("Client connecté")

#Phase de messages
message = conn.recv(1024).decode()
print(f"Client : {message}")

reply = "Salut client !"
conn.send(reply.encode())
print(f"Server : {reply}")

message = conn.recv(1024).decode()
print(f"Client : {message}")
print("Fermeture de la connexion du client")
conn.close()

print("Fermeture du serveur")
serveur_socket.close()