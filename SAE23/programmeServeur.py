import Serveur as Serveur
import threading
import sys

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Il manque un ou plusieurs argument\nFormat attendu :\n   python mainServeur.py <IP> <Port>")
        sys.exit(1)
    elif len(sys.argv) > 3:
        print("Il y a trop d'arguments")
        sys.exit(1)

    ipserveur = sys.argv[1]
    try:
        portserveur = int(sys.argv[2])
    except ValueError:
        print("Le port doit être un entier.")
        sys.exit(1)

    serveur = Serveur.Serveur("Serveur test", ipserveur, portserveur)

    while serveur.consigne != "arret":
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
            print(f"Erreur : {e}")