import socket
import time

def bye():
    """
    Fonction qui ferme la connexion du client.
    """
    reply = client_socket.recv(1024).decode()
    print(f"Server : {reply}")
    fermeture = "(Fermeture de la connexion client)"
    print(fermeture)
    #client_socket.send(fermeture.encode())
    client_socket.close()

def arretserv():
    """
    Fonction qui gère l'arret du serveur
    """
    print("(Le serveur va s'arrêter)")
    reply = client_socket.recv(1024).decode()
    print(f"Server : {reply}")
    time.sleep(1)
    print("Déconnecté du serveur")


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
while True:
    message = input("Client : ")
    client_socket.send(message.encode())
    if message == "bye":
        time.sleep(0.2)
        bye()
        break
    elif message == "arret":
        arretserv()
        break
    else:
        reply = client_socket.recv(1024).decode()
        print(f"Server : {reply}")
        if reply == "arret":
            arretserv()
            break
        elif reply == "bye":
            bye()
            break