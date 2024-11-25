import socket
from PyQt6.QtWidgets import *

import socket
import threading
import sys

class Serveur():

    def __init__(self,nom :str, ip :str = "localhost", port :int = 4200, consigne :str = ""):
        self.__nom :str = nom
        self.__ip :str = ip
        self.__port :int = port
        self.__socket :socket = socket.socket()
        self.__socket.bind((self.__ip, self.__port))
        self.__socket.listen(1)
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
    
    @ip.setter
    def ip(self, ip):
        self.__ip = ip
    
    @property
    def port(self) -> int:
        return self.__port
    
    @port.setter
    def port(self, port):
        self.__port = port
    
    @property
    def socket(self) -> socket:
        return self.__socket

    @property
    def consigne(self) -> str:
        return self.__consigne
    
    @consigne.setter
    def consigne(self, cons):
        self.__consigne = cons
    
    
    def connexion(self):
        try:
            print("En attente de connexion...")
            conn, address = self.__socket.accept()
            print(f"Client {address} connecté")
            acceptation = f"Connexion au serveur acceptée au serveur {self.nom} ({self.ip}), vous pouvez communiquer."
            threadEcoute = threading.Thread(target=self.ecoute, args=[conn])
            threadEcoute.start()
            message = threadEcoute
            conn.send(acceptation.encode())
            return conn
        except KeyboardInterrupt:
            print("Arrêt manuel du serv")
            self.consigne = "arret"
    
    def gestionClient(self, conn):
        self.consigne = "En marche"
        try:
            while self.consigne != "arret":
                message = conn.recv(1024).decode()
                print(f"Le client a envoyé : {message}")

        except ConnectionAbortedError:
            print("Connexion au client fermée")
            self.occupe = False
        except ConnectionError:
            print("Connexion stopée de manière inattendue")
            self.__socket.close()
            self.occupe = False
        finally:
            conn.close()
            self.occupe = False
            print("Déconnexion du client.")
    
    def ecoute(self, conn):
        message = conn.recv(1024).decode()
        return message
    
    def byeclient(self, conn):
        conn.close()
        self.occupe = False
        print("Connexion au client terminée")

    def arret(self, conn):
        conn.close()
        self.__socket.close()
        self.consigne = "arret"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Le serveur de tchat")
        self.ecranServeur()

    def ecranServeur(self):
        self.widgetServeur = QWidget()
        self.setCentralWidget(self.widgetServeur)
        self.grid = QGridLayout(self.widgetServeur)


        lab1 = QLabel("Serveur")
        self.ip = QLineEdit("localhost")
        lab2 = QLabel("Port")
        self.port = QLineEdit("4200")
        lab3 = QLabel("Nombre de clients maximum")
        self.clientsmax = QLineEdit("5")
        self.demarrer = QPushButton("Démarrage du serveur")
        self.arret = QPushButton("Arret du serveur")
        self.chat = QPlainTextEdit()
        self.chat.setReadOnly(True)
        self.quit = QPushButton("Quitter")
        
        self.grid.addWidget(lab1, 0, 0)
        self.grid.addWidget(self.ip, 0, 1)
        self.grid.addWidget(lab2, 1, 0)
        self.grid.addWidget(self.port, 1, 1)
        self.grid.addWidget(lab3, 2, 0)
        self.grid.addWidget(self.clientsmax, 2, 1)
        self.grid.addWidget(self.demarrer, 3, 0, 1, 2)
        self.grid.addWidget(self.chat, 4, 0, 1, 2)
        self.grid.addWidget(self.quit, 5, 0, 1, 2)

        self.demarrer.clicked.connect(self.__actionDemarrer)
        self.quit.clicked.connect(self.__actionQuitter)
        self.arret.clicked.connect(self.__actionArret)

        #self.arret.clicked.connect(self.__actionArret)
        #self.deco.clicked.connect(self.__actionDeco)



    def __actionDemarrer(self):
        def RetourChat(self, message):
            self.chat.setPlainText(message)
        ip = self.ip.text()
        try:   
            port = int(self.port.text())
            self.serveur = Serveur("Serveur de tchat", ip, port)
            self.grid.removeWidget(self.demarrer)
            self.grid.addWidget(self.arret, 3, 0, 1, 2)
        except ValueError:
            QMessageBox.warning(self, "Erreur port", "Le port doit être un entier")
            self.port.setText("")
        while self.serveur.consigne != "arret":
            threadAccept = threading.Thread(target= self.__accept)
            threadAccept.start()
        threadAccept.join()

    def __accept(self):
        conn = self.serveur.accept()

    def __actionQuitter(self):
        QApplication.exit(0)

    def __actionArret(self, conn):
        self.grid.removeWidget(self.arret)
        self.grid.addWidget(self.demarrer, 3, 0, 1, 2)
        self.serveur.consigne = "arret"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()