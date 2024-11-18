import socket
import time

# Fichier de la classe Client

class Client():

    def __init__(self, nom :str):
        self.__nom = nom
        self.__socket :socket = socket.socket()
    
    def __str__(self) -> str:
        return f"Client : {self.nom}"

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def socket(self):
        return self.__socket
    
    def connexion(self):
        """
        Fonction d'un client qui tente de se connecter à un serveur
        """
        connexion = False
        while connexion == False:
            ip = input("Entrez l'adresse IP du serveur (format x.x.x.x): ")
            try:
                port = int(input("Entrez le port du serveur : "))
            except ValueError:
                print("Le port doit être un entier.")
                continue
            try:
                self.socket.connect((ip, port))
                retourco = self.socket.recv(1024).decode()
                print(retourco)
                connexion = True
            except Exception as erreur:
                print(f"Erreur de connexion : {erreur}")

    def ecoute(self):
        reply = self.__socket.recv(1024).decode()
        print(f"Server : {reply}")
        return reply
    
    def ecrit(self):
        message = input("Client : ")
        self.__socket.send(message.encode())
        return message

    
    def bye(self):
        reply = self.socket.recv(1024).decode()
        print(f"Server : {reply}")
        print("(Fermeture de la connexion client)")
        self.socket.close()

    def arretserv(self):
        print("(Le serveur va s'arrêter)")
        reply = self.socket.recv(1024).decode()
        print(f"Server : {reply}")
        time.sleep(1)
        print("Déconnecté du serveur")