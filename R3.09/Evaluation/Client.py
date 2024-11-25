import socket
import time

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
    
    def connexion(self, ip, port):
        print(f"Connexion au serveur {ip} sur le port {port}...")
        try:
            self.socket.connect((ip, port))
            retourco = self.socket.recv(1024).decode()
            print(retourco)
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
        print("(Fermeture de la connexion client)")
        self.socket.close()

    def arretserv(self):
        print("(Le serveur va s'arrêter)")
        reply = self.socket.recv(1024).decode()
        print(f"Server : {reply}")
        time.sleep(1)
        print("Déconnecté du serveur")

if __name__ == "__main__":

    message = "start"
    reply = "start"

    client = Client("Client eval R309")
    try:
        client.connexion("localhost", 4200)
        while message != "arret" and reply != "arret" and message != "bye" and reply != "bye":
            message = client.ecrit()
            if message == "bye":
                client.bye()
                break
            elif message == "arret":
                client.arretserv()
                break
    except Exception as erreur:
            raise erreur