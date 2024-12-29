import Serveur as Serveur
from Serveur import PortError
import threading
import sys

if __name__ == "__main__":
    """
    Format de la commande pour lancer le serveur :

    "python programmeServeur.py <port compris entre 49152 et 65535>"

    """

    ipserveur = "127.0.0.1"

    if len(sys.argv) == 1:
        portserveur = 50000
    elif len(sys.argv) == 2:
        try:
            portserveur = int(sys.argv[1])
        except ValueError:
            print(f"Le port {sys.argv[1]} n'est pas un entier.")
            sys.exit(1)
        try:
            if portserveur < 49152 or portserveur > 65535:
                raise PortError
        except PortError:
            print(f"Le port {portserveur} n'est pas dans la plage dynamique des ports (49152 à 65535).")
            sys.exit(1)
    elif len(sys.argv) > 2:
        print("Il y a trop d'arguments")
        sys.exit(1)

    serveur = Serveur.Serveur("Serveur", ipserveur, portserveur)

    while serveur.consigne != "arret":
        #threadCommande = threading.Thread(target=serveur.commande)
        #threadCommande.start()
        try :
            conn = serveur.connexion()
            if serveur.occupe == False:
                print("Lancement du thread de gestion du client")
                conn.send("La connexion au serveur a bien été acceptée !".encode())
                threadGestionClient = threading.Thread(target=serveur.gestionClient, args=[conn])
                threadGestionClient.start()
            else:
                print("Le serveur est déjà occupé, rejet du client")
                conn.send("Le serveur est occupé, veuillez reessayer plus tard ou vous connecter à un autre serveur".encode())
                conn.close()
        except KeyboardInterrupt:
            print("Arrêt manuel du serv")
            serveur.consigne = "arret"
        except Exception as e:
            print("Arrêt  du serveur suite à :")
            print(f"Erreur : {e}")
            serveur.consigne = "arret"
    #threadCommande.join()