import socket
import time

# Fichier de la classe Client

class Client():

    def __init__(self, nom):
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
    
    def connexion(self, ip :str, port :int):
        """
        Fonction d'un client qui tente de se connecter à un serveur
        """
        print(f"Connexion au serveur {ip} sur le port {port}...")
        try:
            self.socket.connect((ip, port))
            retourco = self.socket.recv(1024).decode()
            print(retourco)
        except Exception as erreur:
            print(f"Erreur de connexion : {erreur}")

    
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

if __name__ == "__main__":

    client = Client("Client test")
    print(client)
    client.connexion("127.0.0.1", 1000)