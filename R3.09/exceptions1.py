def divEntier(x: int, y: int) -> int:
    """
    Ce code effectue une simple division de deux nombre entiers et revoie un nombre entier.
    """
    if x < 0 or y < 0:
        raise ValueError("Les nombres doivent être positifs")
    elif y == 0:
        raise ZeroDivisionError("Erreur de division par zero")
    elif x < y:
        return 0
    else:
        x = x - y
    
    return divEntier(x, y) + 1


if __name__ == "__main__":
    try:
        x = int(input("Saisissez la valeur à diviser : "))
        y = int(input("Saisissez le diviseur : "))
        print(divEntier(x,y))
    except ValueError as err:
        # On ajoute une ValueError si la personne entre par exemple des lettres
        print(f"Une des valeurs entrées n'est pas valide {err}")
    except ZeroDivisionError as err:
        print(f"y est égal à 0, l'opération n'est donc mathématiquement pas possible : {err}")
        