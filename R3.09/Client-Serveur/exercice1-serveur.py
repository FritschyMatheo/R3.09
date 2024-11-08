import socket

serveur_socket = socket.socket()
port = 10000
ip = "127.0.0.1"

serveur_socket.bind((ip, port))
serveur_socket.listen(1)
print("En attente de connexion...")

conn, address = serveur_socket.accept()
acceptation = "La connexion a bien été acceptée"

conn.send(acceptation.encode())
print("Connexion acceptée, attente du message")

message = conn.recv(1024).decode()
print(f"Message recu : {message}")

reply = "Yo, j'ai bien recu le message"
print(f"Envoie réponse : {reply}")
conn.send(reply.encode())
print("Réponse envoyée")

print("Fermeture de la connexion")
conn.close()
serveur_socket.close()