import Serveur
import socket
import threading
import time





serveur = Serveur.Serveur("Serveur")

message = "start"
reply = "start"

#Etablissement de la connexion


while message != "arret" and reply != "arret":
    serveur.connexion()