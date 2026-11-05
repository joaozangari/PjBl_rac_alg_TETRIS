import pygame
import sys

from pecas import gerar_nova_peca

# background
LARGURA_TELA = 500
ALTURA_TELA = 600
TAMANHO_BLOCO = 30
COLUNAS = 10
LINHAS = 20

# rgb
PRETO = (0, 0, 0)
CINZA = (50, 50, 50)
BRANCO = (255, 255, 255)

PECAS = {
    #Preto
    0: (0, 0, 0),
    #Azul
    1: (0, 0, 255),
    #Verde
    2: (0, 255, 0),
    #Vermelho
    3: (255, 0, 0),
    #Amarelo
    4: (255, 255, 0),
    #Ciano
    5: (0, 255, 255)
}


def criar_matriz():
    return [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]


def desenhar_grade(tela, matriz):
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = coluna * TAMANHO_BLOCO
            y = linha * TAMANHO_BLOCO

            numeroPeca = matriz[linha][coluna]
            corPeca = PECAS[numeroPeca]

            retangulo = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)

            pygame.draw.rect(tela, corPeca, retangulo)
            pygame.draw.rect(tela, CINZA, retangulo, 1)



def desenhar_peca_ativa(tela, peca):
    for l_idx, linha in enumerate(peca.matriz):
        for c_idx, valor in enumerate(linha):
            if valor != 0:
                coluna_grid = peca.x + c_idx
                linha_grid = peca.y + l_idx

               
                if 0 <= coluna_grid < COLUNAS and 0 <= linha_grid < LINHAS:
                    x = coluna_grid * TAMANHO_BLOCO
                    y = linha_grid * TAMANHO_BLOCO

                    corPeca = PECAS.get(valor, BRANCO)
                    retangulo = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)

                    pygame.draw.rect(tela, corPeca, retangulo)
                    pygame.draw.rect(tela, CINZA, retangulo, 1)


def main():
    # pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Tetris RA - Sprint 1")
    relogio = pygame.time.Clock()

    fonte_placar = pygame.font.SysFont("consolas", 28, bold=True)
    score = 0

    grade = criar_matriz()

   
    peca_atual = gerar_nova_peca()

    rodando = True
    while rodando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

           
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    peca_atual.x -= 1
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    peca_atual.x += 1
                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    peca_atual.y += 1
                elif evento.key == pygame.K_SPACE:
                   
                    peca_atual = gerar_nova_peca()

        tela.fill(PRETO)

    
        desenhar_grade(tela, grade)

    
        desenhar_peca_ativa(tela, peca_atual)

      
        texto_score = fonte_placar.render(f"SCORE {str(score).zfill(4)}", True, BRANCO)
        posicao_x_placar = (COLUNAS * TAMANHO_BLOCO) + 20
        tela.blit(texto_score, (posicao_x_placar, 20))

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()