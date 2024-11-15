import socket

def bye():
    """
    Fonction qui ferme la connexion du client.
    """
    print("Fermeture de la connexion client")
    fermeture = "Fermeture de la connexion client"
    client_socket.send(fermeture.encode())
    client_socket.close()

#Configuration connexion
client_socket = socket.socket()
port = 10000
ip = "127.0.0.1"

#Etablissement de la connexion
print("Connexion au serveur...")
client_socket.connect((ip, port))
testco = client_socket.recv(1024).decode()
print(testco)

#Phase de messages
message = "Hello!"
print(f"Client : {message}")
client_socket.send(message.encode())

reply = client_socket.recv(1024).decode()
print(f"Server : {reply}")

message = "bye"
print(f"Client : {message}")
client_socket.send(message.encode())
bye()