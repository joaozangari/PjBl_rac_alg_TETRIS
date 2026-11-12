import random
import copy

PECAS_MATRIZES = {
    'I': [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    'O': [
        [2, 2],
        [2, 2]
    ],
    'T': [
        [0, 3, 0],
        [3, 3, 3],
        [0, 0, 0]
    ],
    'L': [
        [0, 0, 4],
        [4, 4, 4],
        [0, 0, 0]
    ],
    'J': [
        [5, 0, 0],
        [5, 5, 5],
        [0, 0, 0]
    ],
    'S': [
        [0, 6, 6],
        [6, 6, 0],
        [0, 0, 0]
    ],
    'Z': [
        [7, 7, 0],
        [0, 7, 7],
        [0, 0, 0]
    ]
}

class Peca:
    def __init__(self, x=3, y=0):
        self.tipo = random.choice(list(PECAS_MATRIZES.keys()))
        self.matriz = copy.deepcopy(PECAS_MATRIZES[self.tipo])
        self.x = x 
        self.y = y 

    def colide(self, grade, novo_x, novo_y, matriz=None):
        matriz_a_testar = matriz if matriz is not None else self.matriz
        for l_idx, linha in enumerate(matriz_a_testar):
            for c_idx, valor in enumerate(linha):
                if valor != 0:
                    coluna_grid = novo_x + c_idx
                    linha_grid = novo_y + l_idx

                  
                    if coluna_grid < 0 or coluna_grid >= len(grade[0]) or linha_grid >= len(grade):
                        return True
                   
                    if linha_grid >= 0 and grade[linha_grid][coluna_grid] != 0:
                        return True
        return False

    def mover_horizontal(self, grade, direcao):
        novo_x = self.x + direcao
        if not self.colide(grade, novo_x, self.y):
            self.x = novo_x

    def aplicar_gravidade(self, grade):
        novo_y = self.y + 1
        if not self.colide(grade, self.x, novo_y):
            self.y = novo_y
            return True
        else:

            for l_idx, linha in enumerate(self.matriz):
                for c_idx, valor in enumerate(linha):
                    if valor != 0:
                        gx = self.x + c_idx
                        gy = self.y + l_idx
                        if 0 <= gy < len(grade) and 0 <= gx < len(grade[0]):
                            grade[gy][gx] = valor
            return False

    def rotacionar(self, grade):

        matriz_rotacionada = [list(linha) for linha in zip(*self.matriz[::-1])]
        

        if not self.colide(grade, self.x, self.y, matriz_rotacionada):
            self.matriz = matriz_rotacionada
        else:
            for ajuste in [1, -1, 2, -2]:
                if not self.colide(grade, self.x + ajuste, self.y, matriz_rotacionada):
                    self.x += ajuste
                    self.matriz = matriz_rotacionada
                    break

    def obter_posicao_fantasma(self, grade):
        y_fantasma = self.y
        while not self.colide(grade, self.x, y_fantasma + 1):
            y_fantasma += 1
        return y_fantasma

def gerar_nova_peca():
    return Peca(x=3, y=0)