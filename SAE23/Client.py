import socket
import time
from PyQt6.QtWidgets import *

# Fichier de la classe Client

class Client():

    def __init__(self, nom :str = "Client", etatconnexion :bool = False):
        self.__nom = nom
        self.__socket :socket = socket.socket()
        self.__connecte = etatconnexion
    
    def __str__(self) -> str:
        return f"Client : {self.nom}"

    @property
    def nom(self) -> str:
        return self.__nom
    
    def connexion(self, ip, port):
        """
        Fonction d'un client qui tente de se connecter à un serveur
        """
        try:
            self.__socket.connect((ip, port))
            self.__connecte = True
        except Exception as erreur:
            raise erreur
    
    def envoyer(self, demande):
        if self.__connecte == False:
            raise ConnectionError("Le client doit d'abord se connecter à un serveur.")
        try:
            self.__socket.send(demande.encode())
            return self.__socket.recv(1024).decode()
        except Exception as e:
            print(f"Erreur lors de l'envoi du fichier : {e}")

    def bye(self):
        self.__socket.close()

    def arretserv(self):
        print("(Le serveur va s'arrêter)")
        reply = self.socket.recv(1024).decode()
        print(f"Server : {reply}")
        time.sleep(1)
        print("Déconnecté du serveur")

    def ecoute(self):
        reply = self.__socket.recv(1024).decode()
        print(f"Server : {reply}")
        return reply


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = Client()
        self.setWindowTitle("Affichage client")
        self.ecranConnexion()

    def ecranConnexion(self):
        # Ecran de connexion
        self.widgetConnexion = QWidget()
        self.setCentralWidget(self.widgetConnexion)
        self.grid = QGridLayout(self.widgetConnexion)


        lab1 = QLabel("Configuration de connexion :")
        lab2 = QLabel("Ip du serveur :")
        lab3 = QLabel("Port du serveur :")
        self.ip = QLineEdit("127.0.0.1")
        self.ip.setEnabled(False)
        self.port = QLineEdit("")
        self.connexion = QPushButton("Se connecter")
        self.quit = QPushButton("Quitter")

        # Ajouter les composants au grid ayout
        self.grid.addWidget(lab1, 0, 0, 1, 2)
        self.grid.addWidget(lab2, 1, 0)
        self.grid.addWidget(self.ip, 1, 1)
        self.grid.addWidget(lab3, 2, 0)
        self.grid.addWidget(self.port, 2, 1)
        self.grid.addWidget(self.connexion, 3, 0)
        self.grid.addWidget(self.quit, 3, 1)

        self.connexion.clicked.connect(self.__actionConnexion)
        self.quit.clicked.connect(self.__actionQuitter)

        # Ecran connecté
        self.widgetConnecte = QWidget()
        self.grid2 = QGridLayout(self.widgetConnecte)

        lab4 = QLabel("Fichier choisi")
        self.editFichier = QPlainTextEdit()
        self.chargerFichier = QPushButton("Choisir fichier")
        self.envoyer = QPushButton("Envoyer")
        #self.deco

        self.grid2.addWidget(lab4, 0, 0, 1, 2)
        self.grid2.addWidget(self.editFichier, 1, 0, 1, 2)
        self.grid2.addWidget(self.chargerFichier, 2, 0)
        self.grid2.addWidget(self.envoyer, 2, 1)

        self.chargerFichier.clicked.connect(self.__actionCharger)
        self.envoyer.clicked.connect(self.__actionEnvoyer)


    def __actionConnexion(self):
        ip = self.ip.text()
        port = self.port.text()
        try:
            #Ajouter des teste si le port est valide
            port = int(port)
            self.client.connexion(ip, port)
            QMessageBox.information(self, "Connexion au serveur", "La connexion au serveur a fonctionné !")
            self.setCentralWidget(self.widgetConnecte )
        except ValueError:
            QMessageBox.warning(self, "Erreur port", "Le port doit être un entier")
        except Exception as erreur:
            QMessageBox.critical(self, "Erreur de connexion", str(erreur))

    def __actionQuitter(self):
        QApplication.exit(0)

    def __actionCharger(self):
        fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier", "", "Source Files (*.py *.c *.cpp *.cc *.java)")
        if fichier:
            try:
                with open(fichier, "r", encoding="utf-8") as fich:
                    contenu = fich.read()
                self.file_edit.setPlainText(contenu)
                QMessageBox.information(self, "Fichié chargé", "Le fichier a bien été chargé !")
            except Exception as erreur:
                QMessageBox.critical(self, "Erreur de chargement du fichier", str(erreur))
        else:
            self.file_edit.setPlainText("Aucun fichier sélectionné")

    def __actionEnvoyer(self):
        pass
