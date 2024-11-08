import socket

client_socket = socket.socket()

port = 10000
print("Connexion au serveur")
client_socket.connect(("127.0.0.1", port))
message = "Hello!"
print(f"Envoie du message {message}")
client_socket.send(message.encode())
reply = client_socket.recv(1024).decode()
print(f"Reception réponse {reply}")
print("Fermeture de la connexion")
client_socket.close()