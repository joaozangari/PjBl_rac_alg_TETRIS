import random

PECAS_MATRIZES = {
    'I': [
        [0, 9, 0, 0],
        [0, 9, 0, 0],
        [0, 9, 0, 0],
        [0, 9, 0, 0]
    ],
    'O': [
        [7, 7],
        [7, 7]
    ],
    'T': [
        [0, 2, 0],
        [2, 2, 2],
        [0, 0, 0]
    ],
    'L': [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 0]
    ],
    'J': [
        [0, 0, 4],
        [0, 0, 4],
        [0, 4, 4]
    ]
}

class Peca:
    def __init__(self, x=3, y=0):
        self.tipo = random.choice(list(PECAS_MATRIZES.keys()))
        self.matriz = PECAS_MATRIZES[self.tipo]
        self.x = x 
        self.y = y 

def gerar_nova_peca():
    return Peca(x=3, y=0)