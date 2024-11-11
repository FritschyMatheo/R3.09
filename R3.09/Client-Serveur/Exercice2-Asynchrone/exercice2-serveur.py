import socket
import time

def arret():
    """
    Fonction qui ferme la connexion client et eteint le serveur.
    """
    print("\nFermeture de la connexion du client")
    conn.close()
    print("Fermeture du serveur")
    serveur_socket.close()

#Configuration connexion
serveur_socket = socket.socket()
port = 10000
ip = "127.0.0.1"

#Etablissement de la premiere connexion
serveur_socket.bind((ip, port))
serveur_socket.listen(1)
print("En attente de connexion...")

conn, address = serveur_socket.accept()
acceptation = "Connexion au serveur acceptée, vous pouvez communiquer."
conn.send(acceptation.encode())
print("Client connecté")

time.sleep(0.5)
#Phase de messages
message = conn.recv(1024).decode()
print(f"Client : {message}")

time.sleep(0.5)
reply = "Salut client !"
conn.send(reply.encode())
print(f"Server : {reply}")

#Message bye
time.sleep(1)
message = conn.recv(1024).decode()
print(f"Client : {message}")
print("Fermeture de la connexion du client")
conn.close()

#Seconde connexion
print("En attente de connexion...")

conn, address = serveur_socket.accept()
acceptation = "Connexion au serveur acceptée, vous pouvez communiquer."
conn.send(acceptation.encode())
print("Client connecté")

time.sleep(0.7)

#Phase de messages
message = conn.recv(1024).decode()
print(f"Client : {message}")

reply = "Salut client 2 !"
conn.send(reply.encode())
print(f"Server : {reply}")

time.sleep(0.2)
#Message arret
message = conn.recv(1024).decode()
print(f"Client : {message}")

arret()