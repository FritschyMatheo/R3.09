import socket
import time
#import threading
import os
import subprocess

# Fichier de la classe Serveur

# Classes d'erreurs personnalisées pour la compilation/exécution des fichiers C et C++ et pour le port du serveur.
class CompilationError(Exception):
    # En cas d'erreur de compilation
    pass

class ExecutionError(Exception):
    # En cas d'erreur d'exécution'
    pass

class PortError(Exception):
    # Quand le port n'est pas dans la plage
    pass

class Serveur():

    def __init__(self,nom :str, ip :str = "127.0.0.1", port :int = 1000, occupe :bool = False, consigne :str = ""):
        self.__nom :str = nom
        self.__ip :str = ip
        self.__port :int = port
        self.__socket :socket = socket.socket()
        self.__socket.bind((self.__ip, self.__port))
        self.__socket.listen(1)
        self.__occupe = occupe
        self.__consigne = consigne
        print(self)

    def __str__(self) -> str:
        return f"Le serveur {self.nom} a comme ip : {self.ip} et utilise le port : {self.port}"

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def ip(self) -> str:
        return self.__ip
    
    @property
    def port(self) -> int:
        return self.__port
    
    @property
    def socket(self) -> socket:
        return self.__socket
    
    @property
    def occupe(self) -> bool:
        return self.__occupe
    
    @occupe.setter
    def occupe(self, etat):
        self.__occupe = etat

    @property
    def consigne(self) -> str:
        return self.__consigne
    
    @consigne.setter
    def consigne(self, cons):
        self.__consigne = cons
    
    
    def connexion(self):
        """
        Fonction d'un serveur qui attend une connexion et qui valide vers le client quand c'est bon.
        """
        try:
            print("En attente de connexion...")
            conn, address = self.__socket.accept()
            print(f"Client {address} connecté")
            return conn
        except KeyboardInterrupt:
            print("Arrêt manuel du serv")
            self.consigne = "arret"
    

    def gestionClient(self, conn):
        consigneclient = "start"
        try:
            while consigneclient != "arret" and consigneclient != "bye":
                consigneclient = conn.recv(1024).decode()
                if not consigneclient:
                    consigneclient = "arret"
                elif consigneclient == "bye":
                    self.byeclient(conn)
                elif consigneclient == "arret":
                    self.arret(conn)
                elif consigneclient == "envoie fichier":
                    if self.occupe == True:
                        print("Envoie occupé")
                        self.envoie(conn, "Occupé")
                    else:
                        print("Envoie libre")
                        self.envoie(conn, "libre")
                        self.gestionFichier(conn)
                else:
                    print(f"Le client a envoyé : {consigneclient}")

        except ConnectionAbortedError:
            print("Connexion au client fermée")
            self.occupe = False
        except ConnectionError:
            print("Connexion stopée de manière inattendue")
            self.__socket.close()
            self.occupe = False
        finally:
            print("Déconnexion du client.")
    
    def commande(self):
        commande = ""
        try:
            while commande != "arret":
                commande = input()
            self.consigne = "arret"
        except KeyboardInterrupt:
            print("Arrêt manuel du serv")
            self.consigne = "arret"
        except Exception as e:
            print("Arrêt  du serveur suite à :")
            print(f"Erreur : {e}")
            self.consigne = "arret"

    def gestionFichier(self, conn):
        self.occupe = True
        print("En attente du fichier client")
        test = conn.recv(1024).decode()
        if test == "annuler":
            print("Opération annulée")
            self.occupe = False
        else:
            nomFichier = test
            fichier = conn.recv(1024).decode()
            print("Fichier recu : ", nomFichier, "\n")
            print("Contenu : ", fichier)
            nomFichier, extension = os.path.splitext(nomFichier)
            print("Chemin du fichier :", nomFichier)
            print("Extension du fichier :", extension)
            try:
                if extension == ".txt":
                    print("Fichier texte détecté")
                    #time.sleep(1)
                    resultatCode = fichier
                elif extension == ".py":
                    print("fichier Python détecté")
                    resultatCode = self.executionCodePython(fichier)
                elif extension == ".c":
                    print("fichier C détecté")
                    resultatCode = self.executionCodeC(fichier)
                elif extension == ".cpp":
                    print("fichier C++ détecté")
                    resultatCode = self.executionCodeCpp(fichier)
                elif extension == ".java":
                    print("fichier Java détecté")
                    resultatCode = self.executionCodeJava(fichier, nomFichier)
                else:                    
                    print("Extension non supportée :", extension)
                    resultatCode = f"Extension du fichier {extension} non prise en charge"
                self.envoie(conn, resultatCode)
            except Exception as e:
                print("Problème d'exécution du code :")
                print(f"Erreur : {e}")
            finally:
                self.occupe = False
            
    def executionCodePython(self, code):
        print("Execution du code Python...")
        start = time.perf_counter()
        #time.sleep(2)
        try:
            resultat = subprocess.run(["python", "-c", code], text=True, capture_output=True, check=True)
            end = time.perf_counter()
            print("resultat :", resultat.stdout)
            resultatFinal = resultat.stdout
            print(f"Temps d'exécution du code : {round(end - start, 2)} seconde(s)")
        except subprocess.CalledProcessError as e:
            resultatFinal = f"Erreur lors de l'exécution du code :\n{e}\n\n{e.stderr}"
        if not resultatFinal.strip():
            resultatFinal = "Le programme ne renvoie rien."
        return resultatFinal
    
    def executionCodeC(self, code):
        print("Execution du code C...")
        start = time.perf_counter()
        #time.sleep(3)
        fichierTemporraire = "TEMPORRAIRE.c"
        executable = "EXECUTABLE-C.exe"
        
        try:
            with open(fichierTemporraire, "w") as f:
                f.write(code)

            compilation = subprocess.run(["gcc", fichierTemporraire, "-o", executable], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text = True)
            if compilation.returncode != 0:
                raise CompilationError(f"Erreur rencontrée lors de la compilation du code : {compilation.stderr}")
            executionCodeCompile = subprocess.run([f"./{executable}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text = True)
            if executionCodeCompile.returncode != 0:
                raise ExecutionError(f"Erreur rencontrée lors de l'exécution du code : {executionCodeCompile.stderr}")
            resultatFinal = executionCodeCompile.stdout
            end = time.perf_counter()
            print(f"Temps d'exécution du code : {round(end - start, 2)} seconde(s)")
        except FileNotFoundError:
            resultatFinal = "Erreur : Le compilateur de fichiers C (gcc) n'est pas installé ou configuré correctement."
        except CompilationError as e:
            resultatFinal = str(e)
        except ExecutionError as e:
            resultatFinal = str(e)
        except Exception as e:
            resultatFinal = f"Erreur lors de la gestion du code :\n{e}"
        finally:
            if os.path.exists(fichierTemporraire):
                os.remove(fichierTemporraire)
            if os.path.exists(executable):
                os.remove(executable)
        if not resultatFinal.strip():
            resultatFinal = "Le programme ne renvoie rien."
        return resultatFinal
    
    def executionCodeCpp(self, code):
        print("Execution du code C++...")  
        start = time.perf_counter()
        #time.sleep(3.6)
        fichierTemporraire = "TEMPORRAIRE.cpp"
        executable = "EXECUTABLE-CPP.exe"

        try:
            with open(fichierTemporraire, "w") as f:
                f.write(code)
            compilation = subprocess.run(["g++", fichierTemporraire, "-o", executable], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text = True)
            if compilation.returncode != 0:
                raise CompilationError(f"Erreur rencontrée lors de la compilation du code : {compilation.stderr}")
            executionCodeCompile = subprocess.run([f"./{executable}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text = True)
            if executionCodeCompile.returncode != 0:
                raise ExecutionError(f"Erreur rencontrée lors de l'exécution du code : {executionCodeCompile.stderr}")
            resultatFinal = executionCodeCompile.stdout
            end = time.perf_counter()
            print(f"Temps d'exécution du code : {round(end - start, 2)} seconde(s)")
        except FileNotFoundError:
            resultatFinal = "Erreur : Le compilateur de fichiers C++ (g++) n'est pas installé ou configuré correctement."
        except CompilationError as e:
            resultatFinal = str(e)
        except ExecutionError as e:
            resultatFinal = str(e)
        except Exception as e:
            resultatFinal = f"Erreur lors de la gestion du code :\n{e}"
        finally:
            if os.path.exists(fichierTemporraire):
                os.remove(fichierTemporraire)
            if os.path.exists(executable):
                os.remove(executable)
        if not resultatFinal.strip():
            resultatFinal = "Le programme ne renvoie rien."
        return resultatFinal
    
    def executionCodeJava(self, code, nomFichier):
        print("Execution du code Java...")

        try:
            subprocess.run(["javac", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text = True)
        except FileNotFoundError:
            resultatFinal = "Erreur : Java n'est pas installé ou configuré correctement."
            print(resultatFinal)
            return resultatFinal
        
        start = time.perf_counter()
        #time.sleep(2.2)
        classe = str(nomFichier).split("/")[-1]
        fichierTemporraire = f"{classe}.java"
        
        try:
            with open(fichierTemporraire, "w") as f:
                f.write(code)
            compilation = subprocess.run(["javac", fichierTemporraire], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text = True)
            if compilation.returncode != 0:
                raise CompilationError(f"Erreur rencontrée lors de la compilation du code : \n{compilation.stderr}")
            executionTemp = subprocess.run(["java", classe], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text = True)
            if executionTemp.returncode != 0:
                raise ExecutionError(f"Erreur rencontrée lors de l'exécution du code : \n{executionTemp.stderr}")
            resultatFinal = executionTemp.stdout
            end = time.perf_counter()
            print(f"Temps d'exécution du code : {round(end - start, 2)} seconde(s)")
        except CompilationError as e:
            resultatFinal = str(e)
            print(resultatFinal)
        except ExecutionError as e:
            resultatFinal = str(e)
            print(resultatFinal)
        except Exception as e:
            resultatFinal = f"Erreur lors de la gestion du code :\n{e}"
            print(resultatFinal)
        finally:
            if os.path.exists(fichierTemporraire):
                os.remove(fichierTemporraire)
            if os.path.exists(f"{classe}.class"):
                os.remove(f"{classe}.class")
            if not resultatFinal.strip():
                resultatFinal = "Le programme ne renvoie rien."
            print("Resultat :\n", resultatFinal)
            return resultatFinal
    
    def envoie(self, conn, message):
        print(f"Envoie de : {message}")
        conn.send(str(message).encode())
    
    def byeclient(self, conn):
        conn.close()
        #self.occupe = False
        print("Connexion au client terminée")

    def arret(self, conn):
        print("Fermeture de la connexion du client")
        time.sleep(1)
        self.byeclient(conn)
        print("Connexion au client fermée")
        print("Fermeture du serveur")
        self.__socket.close()
        self.consigne = "arret"