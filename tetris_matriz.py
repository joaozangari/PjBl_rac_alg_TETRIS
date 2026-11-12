import pygame
import sys

from pecas import gerar_nova_peca

from gravidade import INTERVALO_QUEDA

from ranking import criar_tabela, pontos, pontos_recorde

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

PONTOS = {
    1: 100,
    2: 300,
    3: 500,
    4: 800,
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
                    
def pontuar_linhas(matriz):
    
    linhas_inicio = len(matriz)
    
    matriz[:] = [
        linha for linha in matriz
        if 0 in linha
    ]
    
    linhas_pontos = linhas_inicio - len(matriz)
    
    for _ in range(linhas_pontos):
        matriz.insert(0, [0 for _ in range(COLUNAS)])

    return linhas_pontos

def atualizar_score(linhas_pontos):
    global score, linhas_totais
    
    if linhas_pontos > 0:
        
        linhas_totais += linhas_pontos
        
        score += PONTOS.get(linhas_pontos, 0)

def main():
    global score, linhas_totais
    # pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Tetris RA - Sprint 1")
    relogio = pygame.time.Clock()

    fonte_placar = pygame.font.SysFont("consolas", 28, bold=True)
    fonte_game_over =  pygame.font.SysFont("consolas", 40, bold=True)
    fonte_fim =  pygame.font.SysFont("consolas", 28, bold=True)
    
    criar_tabela()
    
    recorde = pontos()

    grade = criar_matriz()
    
    tempo = pygame.time.get_ticks()
    
    score = 0
        
    linhas_totais = 0
    
    game_over = False
    
    peca_atual = None
    
    def peca_segura():
        nonlocal peca_atual, game_over, recorde
        
        peca_atual = gerar_nova_peca()
        
        if peca_atual.colide(grade, peca_atual.x, peca_atual.y):
            game_over = True
            recorde = pontos_recorde(score)
            
    peca_segura()

    rodando = True
    
    while rodando:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

           
            if evento.type == pygame.KEYDOWN and not game_over:
                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    peca_atual.mover_horizontal(grade, -1)
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    peca_atual.mover_horizontal(grade, 1)
                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    
                    if not peca_atual.aplicar_gravidade(grade):
                        linhas_pontos = pontuar_linhas(grade)
                        atualizar_score(linhas_pontos)
                        peca_segura()
                    
                elif evento.key == pygame.K_SPACE:
                    
                    while peca_atual.aplicar_gravidade(grade):
                        pass
                    
                    linhas_pontos = pontuar_linhas(grade)
                    atualizar_score(linhas_pontos)
                    peca_segura()
                
        tempo_atual = pygame.time.get_ticks()

        if not game_over:
        
            if tempo_atual - tempo >= INTERVALO_QUEDA:
                
                if not peca_atual.aplicar_gravidade(grade):
                    linhas_pontos = pontuar_linhas(grade)
                    atualizar_score(linhas_pontos)
                    peca_segura()
                
                tempo = tempo_atual

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