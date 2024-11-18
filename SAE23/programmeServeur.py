import Serveur as Serveur
import threading

message = "start"
reply = "start"

serveur = Serveur.Serveur("Serveur test")

connexions = []
running = True
while running:
    conn = serveur.connexion()
    threadEcoute = threading.Thread(target= serveur.ecoute(), args=[conn])
    message = threadEcoute.start()
    if message == "arret":
        serveur.arret()
        running = False