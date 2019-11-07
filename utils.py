# Verifica se a SAI atual possui vizinhos validos
def isValidSAI(x, y):
    if x == 0 or x == 14:
       return False
    if y == 0 or y == 14:
        return False
    if y == 1 or y == 13:
        if x < 4 or x > 10:
            return False
    if x == 1 or x == 13:
        if y < 3 or y > 11:
            return False
    return True

