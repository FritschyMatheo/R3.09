import socket
import time
import threading

# Fichier de la classe Serveur

class Serveur():

    def __init__(self,nom :str, ip :str = "127.0.0.1", port :int = 1000, occupe :bool = False, consigne :str = ""):
        self.__nom :str = nom
        self.__ip :str = ip
        self.__port :int = port
        self.__socket :socket = socket.socket()
        self.__socket.bind((self.__ip, self.__port))
        self.__socket.listen(1)
        self.__occupe = occupe
        self.__consigne = consigne
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
    def socket(self) -> socket:
        return self.__socket
    
    @property
    def occupe(self) -> bool:
        return self.__occupe
    
    @occupe.setter
    def occupe(self, etat):
        self.__occupe = etat

    @property
    def consigne(self) -> str:
        return self.__consigne
    
    @consigne.setter
    def consigne(self, cons):
        self.__consigne = cons
    
    
    def connexion(self):
        """
        Fonction d'un serveur qui attend une connexion et qui valide vers le client quand c'est bon.
        """
        try:
            print("En attente de connexion...")
            conn, address = self.__socket.accept()
            print(f"Client {address} connecté")
            return conn
        except KeyboardInterrupt:
            print("Arrêt manuel du serv")
            self.consigne = "arret"
    

    def gestionClient(self, conn):
        consigneclient = "start"
        try:
            while consigneclient != "arret" and consigneclient != "bye":
                consigneclient = conn.recv(1024).decode()
                if not consigneclient:
                    print("Client déconnecté")
                    break
                elif consigneclient == "bye":
                    self.byeclient(conn)
                elif consigneclient == "arret":
                    self.arret(conn)
                elif consigneclient == "envoie fichier":
                    self.gestionFichier(conn)
                else:
                    print(f"Le client a envoyé : {consigneclient}")

        except ConnectionAbortedError:
            print("Connexion au client fermée")
            self.occupe = False
        except ConnectionError:
            print("Connexion stopée de manière inattendue")
            self.__socket.close()
            self.occupe = False
        finally:
            print("Déconnexion du client.")

    def gestionFichier(self, conn):
        self.occupe = True
        print("En attente du fichier client")
        test = conn.recv(1024).decode()
        if test == "annuler":
            print("Opération annulée")
            self.occupe = False
        else:
            nomFichier = test
            print("Fichier recu : ", nomFichier, "\n")
            fichier = conn.recv(1024).decode()
            resultatCode = self.executionCode(fichier)
            self.envoie(conn, resultatCode)
            self.occupe = False


    def executionCode(self, code):
        return str(f"resultat code :\n{(code)}")
    
    def envoie(self, conn, resultat):
        print("Envoie du resultat du code exécuté")
        conn.send(str(resultat).encode())
    
    def byeclient(self, conn):
        conn.close()
        self.occupe = False
        print("Connexion au client terminée")

    def arret(self, conn):
        print("Fermeture de la connexion du client")
        time.sleep(1)
        self.byeclient(conn)
        print("Connexion au client fermée")
        print("Fermeture du serveur")
        self.__socket.close()
        self.consigne = "arret"