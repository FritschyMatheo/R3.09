import Client
import threading

consigneclient = "start"
consigneserveur = "start"

client = Client.Client("Client test")

client.connexion()

threadEcoute = threading.Thread(target=client.ecoute)
threadEcoute.start()

while consigneclient != "arret" and consigneserveur != "arret" and consigneclient != "bye" and consigneserveur != "bye":
    consigneclient = client.ecrit()

    if consigneclient == "bye":
            client.bye()
    elif consigneclient == "arret":
        client.arretserv()

threadEcoute.join()