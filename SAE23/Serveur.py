import socket
import time
import threading

# Fichier de la classe Serveur

class Serveur():

    def __init__(self,nom :str, ip :str = "127.0.0.1", port :int = 1000, occupe :bool = False):
        self.__nom :str = nom
        self.__ip :str = ip
        self.__port :int = port
        self.__socket :socket = socket.socket()
        self.__socket.bind((self.__ip, self.__port))
        self.__socket.listen(1)
        self.__occupe = occupe
        print(self)

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
    
    @property
    def occupe(self) -> bool:
        return self.__occupe
    
    @occupe.setter
    def occupe(self, etat):
        self.__occupe = etat    
    
    
    def connexion(self):
        """
        Fonction d'un serveur qui attend une connexion et qui valide vers le client quand c'est bon.
        """
        print("En attente de connexion...")
        conn, address = self.__socket.accept()
        print(f"Client {address} connecté")
        return conn
    
    def gestionClient(self, conn):
        consigneclient = "start"
        try:
            while consigneclient != "arret" and consigneclient != "bye":
                consigneclient = conn.recv(1024).decode()
                if consigneclient == "bye":
                    self.byeclient(conn)
                elif consigneclient == "arret":
                    self.arret(conn)
                else:
                    print(f"Le client a envoyé : {consigneclient}")

        except ConnectionAbortedError:
            print("Connexion au client fermée")
            self.occupe = False
        except ConnectionError:
            print("Connexion stopée de manière inattendue")
            self.__socket.close()
        finally:
            conn.close()
            print("Fermeture du serveur")

    def executionCode(self):
        pass
    
    def envoie(self, conn, resultat):
        print("Envoie du resultat du code exécuté")
        conn.send(resultat.encode())
    
    def byeclient(self, conn):
        conn.close()
        self.occupe = False
        print("Connexion au client terminée")

    def arret(self, conn):
        print("Fermeture de la connexion du client")
        time.sleep(1)
        conn.close()
        print("Connexion au client fermée")
        print("Fermeture du serveur")
        self.__socket.close()