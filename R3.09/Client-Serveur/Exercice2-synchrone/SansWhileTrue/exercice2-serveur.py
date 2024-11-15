import socket
import time

def byeclient():
    """
    Fonction qui dit aurevoir au client
    """
    print(f"Fermeture de la connexion du client : {address}")
    message = "Au revoir client"
    print(f"Serveur : {message}")
    conn.send(message.encode())
    conn.close()

def arret():
    """
    Fonction qui ferme la connexion client et eteint le serveur.
    """
    print("Fermeture de la connexion du client")
    deco = "Vous allez être déconnecté"
    print(f"Serveur : {deco}")
    conn.send(deco.encode())
    time.sleep(1)
    conn.close()
    print("Fermeture du serveur")
    serveur_socket.close()

#Configuration connexion
serveur_socket = socket.socket()
port = 10000
ip = "127.0.0.1"

message = "start"
reply = "start"

#Etablissement de la connexion
serveur_socket.bind((ip, port))
serveur_socket.listen(1)

while message != "arret" and reply != "arret":
    print("En attente de connexion...")
    conn, address = serveur_socket.accept()
    print(f"Client {address} connecté")
    acceptation = "Connexion au serveur acceptée, vous pouvez communiquer."
    conn.send(acceptation.encode())

    time.sleep(0.5)
#Phase de messages
    while message != "bye" and message != "arret" and reply != "bye" and reply != "arret":
        message = "start"
        reply = "start"
        message = conn.recv(1024).decode()
        print(f"Client : {message}")

        if message == "bye":
            #Message bye
            byeclient()
        elif message == "arret":
            arret()
        else:
            time.sleep(0.5)
            reply = input("Serveur : ")
            conn.send(reply.encode())
            if reply == "arret":
                arret()
            elif reply == "bye":
                byeclient()