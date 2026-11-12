import random

import copy

PECAS_MATRIZES = {
    'I': [
        [1],
        [1],
        [1],
        [1]
    ],
    'O': [
        [2, 2],
        [2, 2]
    ],
    'T': [
        [0, 3, 0],
        [3, 3, 3]
    ],
    'L': [
        [4, 0],
        [4, 0],
        [4, 4]
    ],
    'J': [
        [0, 5],
        [0, 5],
        [5, 5]
    ]
}

class Peca:
    def __init__(self, x=3, y=0):
        self.tipo = random.choice(list(PECAS_MATRIZES.keys()))
        self.matriz = copy.deepcopy(PECAS_MATRIZES[self.tipo])
        self.x = x 
        self.y = y 

def gerar_nova_peca():
    from gravidade import pecaMovi
    return pecaMovi(x=3, y=0)