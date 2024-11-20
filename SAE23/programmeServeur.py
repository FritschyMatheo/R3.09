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
    consigneclient = "start"
    consigneserveur = "start"

    serveur = Serveur.Serveur("Serveur test", ipserveur, portserveur)

    while consigneclient != "arret" and consigneserveur != "arret":
        try :
            conn = serveur.connexion()
            consigneclient = ""
            consigneserveur = ""
            threadEcoute = threading.Thread(target=serveur.ecoute, args=[conn])
            threadEcoute.start()
        except KeyboardInterrupt:
            print("Arrêt manuel du serv")
        except Exception as e:
            print(f"Erreur : {e}")
        while consigneclient != "arret" and consigneclient != "bye" and consigneserveur != "arret" and consigneserveur != "bye":
            consigneserveur = serveur.ecrit(conn)
            if consigneclient == "bye" or consigneserveur == "bye":
                serveur.byeclient(conn)
            elif consigneclient == "arret" or consigneserveur == "arret":
                serveur.arret(conn)