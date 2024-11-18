import Client
import threading

message = "start"
reply = "start"

client = Client.Client("Client test")

client.connexion()
while message != "arret" and reply != "arret" and message != "bye" and reply != "bye":
    threadServeur = threading.Thread(target=client.ecrit)
    message = threadServeur.start()
    if message == "bye":
            client.bye()
            break
    elif message == "arret":
        client.arretserv()
        break
    else:
        reply = client.ecoute()
        if reply == "arret":
            client.arretserv()
            break
        elif reply == "bye":
            client.bye()
            break