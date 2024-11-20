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
        print(f"--- Serveur {self.__nom} crée ---\nIP : {self.__ip}\nPort : {self.__port}")

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
    
    
    def connexion(self):
        """
        Fonction d'un serveur qui attend une connexion et qui valide vers le client quand c'est bon.
        """
        print("En attente de connexion...")
        conn, address = self.__socket.accept()
        print(f"Client {address} connecté")
        threadEcoute = threading.Thread(target= self.ecoute, args=[conn])
        threadEcoute.start()
        #acceptation = f"Connexion au serveur {self.nom} acceptée ({self.ip}), vous pouvez communiquer."
        #conn.send(acceptation.encode())
        return conn
    
    def ecoute(self, conn):
        consigneclient = "start"
        consigneserveur = "start"
        if self.occupe:
            servoccupe = "Désolé mais le serveur est occupé."
            conn.send(servoccupe.encode())
            return servoccupe
        else:
            try:
                while consigneclient != "arret" and consigneclient != "bye" and consigneserveur != "arret" and consigneserveur != "bye":
                    consigneclient = conn.recv(1024).decode()
                    if message == "bye":
                        self.byeclient(conn)
                    elif message == "arret":
                        self.arret(conn)
                    else:
                        print(f"Client : {message}")
                    #return message
            except ConnectionAbortedError:
                print("Connexion au client fermée")
            except ConnectionError:
                print("Connexion stopée de manière inattendue")
            finally:
                conn.close()
                print("Fermeture du serveur")
                
    
    def ecrit(self, conn):
        reply = input("Serveur : ")
        conn.send(reply.encode())
        return reply
    
    def byeclient(self, conn):
        bye = "Au revoir client"
        print(f"Serveur : {bye}")
        conn.send(bye.encode())
        conn.close()
        print("Connexion au client terminée")

    def arret(self, conn):
        print("Fermeture de la connexion du client")
        deco = "Vous allez être déconnecté"
        conn.send(deco.encode())
        time.sleep(1)
        conn.close()
        print("Connexion au client fermée")
        print("Fermeture du serveur")
        self.__socket.close()