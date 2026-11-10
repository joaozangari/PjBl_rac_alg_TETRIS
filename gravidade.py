from pecas import Peca

INTERVALO_QUEDA = 500

class pecaMovi(Peca):
    
    def _init_(self, x = 3, y = 0):
        super().__init__(x, y)

    def colide(self, matriz, px, py):
   
        linhas = len(matriz)
        colunas = len(matriz[0])
        for l, linha in enumerate(self.matriz):
            for c, valor in enumerate(linha):
                if valor:
                    x = px + c
                    y = py + l
                    if x < 0 or x >= colunas or y >= linhas:
                        return True
                    if y >= 0 and matriz[y][x] != 0:
                        return True
        return False

    def fixar_peca(self, matriz):
    
        for l, linha in enumerate(self.matriz):
            for c, valor in enumerate(linha):
                if valor:
                    matriz[self.y + l][self.x + c] = valor

    def mover_horizontal(self, matriz, direcao):
    
        if not self.colide(matriz, self.x + direcao, self.y):
            self.x += direcao

    def aplicar_gravidade(self, matriz):
    
        if not self.colide(matriz, self.x, self.y + 1):
            self.y += 1
            return True
    
        self.fixar_peca(matriz)
        return False
