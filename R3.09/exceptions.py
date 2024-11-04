def divEntier(x: int, y: int) -> int:
    """
    Ce code effectue une simple division de deux nombre entiers.
    """
    if x < y:
        return 0
    else:
        x = x - y
    return divEntier(x, y) + 1