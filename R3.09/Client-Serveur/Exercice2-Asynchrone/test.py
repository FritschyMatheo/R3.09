import Serveur
import Client

serveur = Serveur.Serveur("Test")

print(serveur)
print(serveur.socket)

client = Client.Client("Client")

print(client)