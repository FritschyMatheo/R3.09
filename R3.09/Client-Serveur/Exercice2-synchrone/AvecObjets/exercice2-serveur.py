import socket
import time

# Fichier de la classe Serveur

class Serveur():

    def __init__(self,nom :str, ip :str = "127.0.0.1", port :int = 1000):
        self.__nom = nom
        self.__ip :str = ip
        self.__port :int = port
        self.__socket :socket = socket.socket()
        self.__socket.bind((self.__ip, self.__port))
        self.__socket.listen(1)

    def __str__(self) -> str:
        return f"Le serveur {self.nom} a comme ip : {self.ip} et utilise le port : {self.port}"

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def ip(self) -> str:
        return self.__ip
    
    @property
    def port(self) -> int:
        return self.__port
    
    @property
    def socket(self):
        return self.__socket
    
    
    def connexion(self):
        """
        Fonction d'un serveur qui attend une connexion et qui valide vers le client quand c'est bon.
        """
        print("En attente de connexion...")
        conn, address = self.__socket.accept()
        print(f"Client {address} connecté")
        acceptation = f"Connexion au serveur acceptée au serveur {self.nom} ({self.ip}), vous pouvez communiquer."
        conn.send(acceptation.encode())
        return conn
    
    def ecoute(self, conn):
        message = conn.recv(1024).decode()
        print(f"Client : {message}")
        return message
    
    def ecrit(self, conn):
        reply = input("Serveur : ")
        conn.send(reply.encode())
        return reply
    
    def byeclient(self, conn):
        #print(f"Fermeture de la connexion du client : {clientaddr}")
        bye = "Au revoir client"
        print(f"Serveur : {bye}")
        conn.send(bye.encode())
        conn.close()

    def arret(self, conn):
        print("Fermeture de la connexion du client")
        deco = "Vous allez être déconnecté"
        print(f"Serveur : {deco}")
        conn.send(deco.encode())
        time.sleep(1.5)
        conn.close()
        print("Fermeture du serveur")
        self.__socket.close()
        
if __name__ == "__main__":

    message = "start"
    reply = "start"

    serveur = Serveur("Serveur test")

    while message != "arret" and reply != "arret":

        message = "start"
        reply = "start"

        conn = serveur.connexion()

        while message != "bye" and message != "arret" and reply != "bye" and reply != "arret":
            message = "start"
            reply = "start"

            message = serveur.ecoute(conn)
            if message == "bye":
                serveur.byeclient(conn)
            elif message == "arret":
                serveur.arret(conn)
            else:
                reply = serveur.ecrit(conn)
                if reply == "arret":
                    serveur.arret(conn)
                elif reply == "bye":
                    serveur.byeclient(conn)
