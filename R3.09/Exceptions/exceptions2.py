
def lireFichier():
    x = input("Entrer le nom du fichier à lire : ")
    try:      
        with open(x, "r") as f:
            for l in f:
                l = l.rstrip("\n\r")
                print(l)
    except FileNotFoundError:
        return "Le fichier n'a pas été trouvé"
    finally:
        print("\nFin de la lecture du fichier.")
    
if __name__ == "__main__":
    print(lireFichier())