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
            if serveur.occupe == False:
                print("Lancement du thread de gestion du client")
                serveur.occupe == True
                conn.send("La connexion au serveur a bien été acceptée !".encode())
                threadGestionClient = threading.Thread(target=serveur.gestionClient, args=[conn])
                threadGestionClient.start()
            else:
                print("Le serveur est déjà occupé, rejet du client")
                # Reponse au client
                conn.send("Le serveur est occupé, veuillez reessayer plus tard ou vous connecter à un autre serveur".encode())
                conn.close()
        except KeyboardInterrupt:
            print("Arrêt manuel du serv")
        except Exception as e:
            print(f"Erreur : {e}")