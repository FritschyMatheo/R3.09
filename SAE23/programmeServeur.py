import Serveur as Serveur
import threading
import sys

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Il manque un ou plusieurs argument")
        sys.exit(1)

    ipserveur = sys.argv[1]
    try:
        portserveur = int(sys.argv[2])
    except ValueError:
        print("Le port doit être un entier.")
        sys.exit(1)

    connexions = []
    consigneclient = ""
    consigneserveur = ""

    serveur = Serveur.Serveur("Serveur test", ipserveur, portserveur)

    while consigneclient != "arret" and consigneserveur != "arret":
        conn = serveur.connexion()
        while consigneclient != "arret" and consigneclient != "bye" and consigneserveur != "arret" and consigneserveur != "bye":
            threadEcoute = threading.Thread(target= serveur.ecoute, args=[conn])
            message = threadEcoute.start()
            if message == "arret":
                serveur.arret()