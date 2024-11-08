import socket

serveur_socket = socket.socket()
port = 10000
serveur_socket.bind(("127.0.0.1", port))
serveur_socket.listen(1)
print("En attente de connexion")
conn, address = serveur_socket.accept()
print("Connexion acceptée, attente du message")
message = conn.recv(1024).decode()
print(f"Message recu : {message}")
reply = "Yo"
print(f"Envoie réponse : {reply}")
conn.send(reply.encode())
print("Réponse envoyée")
print("Fermeture de la connexion")
conn.close()
serveur_socket.close()