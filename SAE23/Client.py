import socket
from PyQt6.QtWidgets import *
import time

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
    
    @property
    def socket(self) -> str:
        return self.__socket
    
    @property
    def connecte(self) -> bool:
        return self.__connecte
    
    def connexion(self, ip, port):
        """
        Fonction d'un client qui tente de se connecter à un serveur
        """
        try:
            self.__socket.connect((ip, port))
            self.__connecte = True
        except Exception as erreur:
            raise erreur
    
    def envoyerDemande(self, demande):
        if self.__connecte == False:
            raise ConnectionError("Le client doit d'abord se connecter à un serveur.")
        else:
            self.__socket.send(demande.encode())

    def ecoute(self):
        reply = self.socket.recv(1024).decode()
        return reply
        
    def razSocket(self):
        self.__socket = socket.socket()

    def bye(self):
        self.socket.close()
        self.razSocket()
        self.__connecte = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = Client()
        self.setWindowTitle("Affichage client")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.ecranConnexion()
        self.ecranConnecte()
        self.stack.addWidget(self.widgetConnexion)
        self.stack.addWidget(self.widgetConnecte)
        self.stack.setCurrentWidget(self.widgetConnexion)

    def ecranConnexion(self):

        # Ecran de connexion
        self.widgetConnexion = QWidget()
        self.stack.addWidget(self.widgetConnexion)
        self.grid = QGridLayout(self.widgetConnexion)

        lab1 = QLabel("Configuration de connexion :")
        lab2 = QLabel("Ip du serveur :")
        lab3 = QLabel("Port du serveur :")
        self.ip = QLineEdit("127.0.0.1")
        self.port = QLineEdit("50000")
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

    def ecranConnecte(self):
        
        # Ecran connecté
        self.widgetConnecte = QWidget()
        self.stack.addWidget(self.widgetConnecte)
        self.grid2 = QGridLayout(self.widgetConnecte)

        self.lab4 = QLabel("Choisissez un fichier")
        self.editFichier = QPlainTextEdit()
        self.chargerFichier = QPushButton("Choisir fichier")
        self.envoyer = QPushButton("Envoyer")
        self.envoyer.setEnabled(False)
        self.arret = QPushButton("Eteindre serveur")
        self.deco = QPushButton("Se déconnecter")

        self.grid2.addWidget(self.lab4, 0, 0, 1, 2)
        self.grid2.addWidget(self.editFichier, 1, 0, 1, 2)
        self.grid2.addWidget(self.chargerFichier, 2, 0)
        self.grid2.addWidget(self.envoyer, 2, 1)
        self.grid2.addWidget(self.deco, 3, 0)
        self.grid2.addWidget(self.arret, 3, 1)


        self.chargerFichier.clicked.connect(self.__actionCharger)
        self.envoyer.clicked.connect(self.__actionEnvoyer)
        self.arret.clicked.connect(self.__actionArret)
        self.deco.clicked.connect(self.__actionDeco)



    def __actionConnexion(self):
        ip = self.ip.text()
        port = self.port.text()
        try:
            port = int(port)
            self.client.connexion(ip, port)
            retourserv = self.client.socket.recv(1024).decode()
            QMessageBox.information(self, "Connexion au serveur", retourserv)
            if retourserv == "Le serveur est occupé, veuillez reessayer plus tard ou vous connecter à un autre serveur":
                self.port.setText("")
                self.client.bye()
            else:
                self.stack.setCurrentWidget(self.widgetConnecte)

        except ValueError:
            QMessageBox.warning(self, "Erreur port", "Le port doit être un entier")
            self.port.setText("")
        except Exception as erreur:
            QMessageBox.critical(self, "Erreur de connexion", str(erreur))
            self.port.setText("")

    def __actionCharger(self):
        fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier à exécuter", "", "Source Files (*.py *.c *.cpp *.cc *.java)")
        self.editFichier.setEnabled(True)
        self.lab4.setText("Fichier chargé")
        if fichier:
            try:
                with open(fichier, "r", encoding="utf-8") as fich:
                    contenu = fich.read()
                self.editFichier.setPlainText(contenu)
                self.nomfichier = fichier.split("/")[-1]
                self.fichier = contenu
                self.envoyer.setEnabled(True)
                QMessageBox.information(self, "Fichié chargé", f"Le fichier {self.nomfichier} a bien été chargé !")
            except Exception as erreur:
                QMessageBox.critical(self, "Erreur de chargement du fichier", str(erreur))
                self.envoyer.setEnabled(False)
        else:
            self.editFichier.setPlainText("Aucun fichier sélectionné")
            self.envoyer.setEnabled(False)

    def __actionEnvoyer(self):
        self.fichier = self.editFichier.toPlainText()
        self.editFichier.setEnabled(False)
        self.client.socket.send("envoie fichier".encode())

        confirmation = QMessageBox(self)
        confirmation.setWindowTitle("Confirmation envoi de fichier")
        confirmation.setText(f"Voulez vous bien envoyer le fichier {self.nomfichier} ?")
        
        boutonOui = QPushButton("Oui")
        boutonAnnuler = QPushButton("Annuler")
        confirmation.addButton(boutonOui, QMessageBox.ButtonRole.YesRole)
        confirmation.addButton(boutonAnnuler, QMessageBox.ButtonRole.NoRole)

        retourConfirmation = confirmation.exec()

        if confirmation.clickedButton() == boutonOui:
            try:
                self.client.socket.send(self.nomfichier.encode())
                self.client.socket.send(self.fichier.encode())
                QMessageBox.information(self, "Envoie réussi", f"Le fichier {self.nomfichier} a été envoyé au serveur.")
                start = time.perf_counter()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'envoi du fichier : {str(e)}")
            try:
                self.editFichier.setPlainText("En attente du résultat du serveur...")
                resultat = self.client.ecoute()
                end = time.perf_counter()
                QMessageBox.information(self, "Résultat du code", f"Le code a été exécuté et est revenu en {round(end - start, 2)} seconde(s) !")
                self.editFichier.setPlainText(resultat)
                self.lab4.setText("Retour serveur")
                self.envoyer.setEnabled(False)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la reception du résultat du code : {str(e)}")
        else:
            self.client.socket.send("annuler".encode())
            self.lab4.setText("Choisir fichier ou envoyer celui ci")
            QMessageBox.information(self, "Annulation", "Envoi de fichier annulé.")


    def __actionQuitter(self):
        QApplication.exit(0)

    def __actionArret(self):
        self.client.socket.send("arret".encode())
        self.client.bye()
        self.port.setText("")
        self.stack.setCurrentWidget(self.widgetConnexion)

    def __actionDeco(self):
        self.client.socket.send("bye".encode())
        self.client.bye()
        self.port.setText("")
        self.stack.setCurrentWidget(self.widgetConnexion)