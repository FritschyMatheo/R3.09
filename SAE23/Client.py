import socket
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QMetaObject, Qt, Q_ARG, pyqtSignal
import time
import threading

# Fichier de la classe Client

class Client():
    """
    Classe de construction d'un client au format graphique qui possède les attributs suivants :
        nom :str
        etatconnexion :bool
        socketClient :socket
    """
    def __init__(self, nom :str = "Client", etatconnexion :bool = False, socketClient :socket = socket.socket()):
        self.__nom = nom
        self.__connecte = etatconnexion
        self.__socket = socketClient
    
    def __str__(self) -> str:
        return f"Client : {self.nom}"

    # Les getters des attributs de la classe Client

    @property
    def nom(self) -> str:
        return self.__nom
    
    @property
    def socket(self) -> str:
        return self.__socket
    
    @property
    def connecte(self) -> bool:
        return self.__connecte
    
    def connexion(self, ip :str, port :int):
        """
        Méthode d'un client qui tente de se connecter à un serveur via son port et son ip
        """
        try:
            self.__socket.connect((ip, port))
            self.__connecte = True
        except Exception as erreur:
            raise erreur
    
    def envoyerDemande(self, demande :str):
        """
        Méthode qui permet d'envoyer un message/une demande à un serveur si le client est bien connecté, sinon renvoie une erreur de connexion.
        """
        if self.__connecte == False:
            raise ConnectionError("Le client doit d'abord se connecter à un serveur.")
        else:
            self.__socket.send(demande.encode())

    def ecoute(self):
        """
        Méthode qui permet au client de recevoir un message d'un serveur, retourne la réponse.
        """
        reply = self.socket.recv(1024).decode()
        return reply
        
    def razSocket(self):
        """
        Méthode qui remet le socket du client à zéro en cas de déconnexion pour permettre à ce dernier de se reconnecter à un serveur qui aurait fermé ce socket ou s'il a eu une erreur.
        """
        self.__socket = socket.socket()

    def bye(self):
        """
        Méthode qui déconnecte le client d'un serveur et qui appelle la remise à zero du socket du client.
        """
        self.socket.close()
        self.razSocket()
        self.__connecte = False


class MainWindow(QMainWindow):
    """
    Classe qui initialise la partie graphique du client grâce à la librairie PyQt6.
    """
    receptionResultat = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.client = Client()
        self.setWindowTitle("Affichage client")
        self.setWindowIcon(QIcon("altodisicon.png"))

        # Partie timer d'attente du résultat du code
        self.receptionResultat.connect(self.__actionResultat)
        self.stopAttente = False
        self.tempsExec = 0

        # Partie graphique
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.ecranConnexion()
        self.ecranConnecte()
        self.stack.addWidget(self.widgetConnexion)
        self.stack.addWidget(self.widgetConnecte)
        self.stack.setCurrentWidget(self.widgetConnexion)

    def ecranConnexion(self):
        """
        Méthode qui créée l'écran de connexion du client au serveur et qui permet d'entrer l'ip et le port du serveur, de se connecter et de quitter.
        """
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
        """
        Méthode qui créée la fenêtre du client quand il est connecté au serveur.
        """
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
        """
        Cette action appelle la méthode de classe connexion du client et lui donne les paramètres ip et port depuis les emplacements de texte de la partie graphique connexion.
        """
        ip = self.ip.text()
        port = self.port.text()
        try:
            port = int(port)
            self.client.connexion(ip, port)
            retourserv = self.client.socket.recv(1024).decode()
            if retourserv == "Le serveur est occupé, veuillez reessayer plus tard ou vous connecter à un autre serveur":
                self.port.setText("")
                QMessageBox.information(self, "Connexion au serveur", retourserv)
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
        fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier à exécuter", "", "Source Files (*.py *.c *.cpp *.cc *.java *.txt)")
        self.editFichier.setEnabled(True)
        self.lab4.setText("Fichier chargé")
        if fichier:
            try:
                with open(fichier, "r", encoding="utf-8") as fich:
                    contenu = fich.read()
                self.editFichier.setPlainText(contenu)
                self.nomfichier = fichier.split("/")[-1]
                self.cheminfichier = fichier
                self.fichier = contenu
                self.envoyer.setEnabled(True)
                #QMessageBox.information(self, "Fichié chargé", f"Le fichier {self.nomfichier} a bien été chargé !")
            except Exception as erreur:
                QMessageBox.critical(self, "Erreur de chargement du fichier", str(erreur))
                self.envoyer.setEnabled(False)
        else:
            self.editFichier.setPlainText("Aucun fichier sélectionné")
            self.envoyer.setEnabled(False)

    def __actionEnvoyer(self):
        self.fichier = self.editFichier.toPlainText()
        self.client.socket.send("envoie fichier".encode())

        etatServeur = self.client.ecoute()
        if etatServeur == "libre":
            confirmation = QMessageBox(self)
            confirmation.setWindowTitle("Confirmation envoi de fichier")
            confirmation.setText(f"Voulez vous bien envoyer le fichier {self.nomfichier} ?")

            boutonOui = QPushButton("Oui")
            boutonAnnuler = QPushButton("Annuler")
            confirmation.addButton(boutonOui, QMessageBox.ButtonRole.YesRole)
            confirmation.addButton(boutonAnnuler, QMessageBox.ButtonRole.NoRole)
            
            confirmation.exec()

            if confirmation.clickedButton() == boutonOui:
                try:
                    if not self.fichier.strip():
                        self.client.socket.send("annuler".encode())
                        self.lab4.setText("Envoie du fichier annulé car il était vide.")
                        self.editFichier.setPlainText("")
                        raise ValueError
                    else:
                        self.client.socket.send(self.cheminfichier.encode())
                        self.client.socket.send(self.fichier.encode())
                        #QMessageBox.information(self, "Envoie réussi", f"Le fichier {self.nomfichier} a été envoyé au serveur.")
                    self.envoyer.setEnabled(False)
                    self.editFichier.setPlainText("En attente du résultat du serveur...")
                    self.arret.setEnabled(False)
                    self.deco.setEnabled(False)
                    self.receptionResultat.connect(self.__actionResultat)
                    threadEcoute = threading.Thread(target=self.__attendreResultat)
                    threadEcoute.start()
                    self.envoyer.setEnabled(False)
                except ValueError:
                    QMessageBox.critical(self, "Erreur", "Erreur lors de l'envoi du fichier, ce dernier est vide.")
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Erreur lors de l'envoi du fichier : {str(e)}")

            else:
                self.client.socket.send("annuler".encode())
                self.lab4.setText("Envoie du fichier annulé")
                #QMessageBox.information(self, "Annulation", "Envoi de fichier annulé.")
        else:
            QMessageBox.information(self, "Retour du serveur", f"Le serveur est {etatServeur}, veuillez reessayer plus tard ou vous connecter à un autre serveur")
            self.editFichier.setPlainText(f"Serveur {etatServeur}")
            self.envoyer.setEnabled(False)

    def __attendreResultat(self):
        self.stopAttente = False
        threadAttente = threading.Thread(target=self.__tempsAttente)
        threadAttente.start()
        try:
            print("Attente de la réponse du serveur...")
            resultat = self.client.ecoute()
            if "non prise en charge" in resultat:
                print("Type de fichier non pris en charge")
                QMessageBox.critical(self, "Erreur", "Erreur, le type de fichier n'est pas pris en compte.")
            else:
                print("Recu")
            self.stopAttente = True
            #print(resultat)
            self.receptionResultat.emit(resultat)
        
        except Exception as e:
            self.stopAttente = True
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'attente du résultat du code : {str(e)}")
    
    def __tempsAttente(self):
        start = time.perf_counter()
        temps = 0
        while self.stopAttente == False:
            temps = round(time.perf_counter() - start, 2)
            QMetaObject.invokeMethod(
                self.lab4,
                "setText",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, f"Temps depuis l'envoi : {temps} s")
            )
            time.sleep(0.02)
        QMetaObject.invokeMethod(
            self.arret,
            "setEnabled",
            Qt.ConnectionType.QueuedConnection,
            Q_ARG(bool, True)
        )
        QMetaObject.invokeMethod(
            self.deco,
            "setEnabled",
            Qt.ConnectionType.QueuedConnection,
            Q_ARG(bool, True)
        )
        QMetaObject.invokeMethod(
                self.lab4,
                "setText",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, f"Résultat serveur ({temps} s):")
            )
        self.tempsExec = temps
        print(temps,"s")
    
    def __actionResultat(self, resultat):
        self.editFichier.setPlainText(resultat)
        self.envoyer.setEnabled(False)

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