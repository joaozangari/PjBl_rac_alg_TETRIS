import pygame
import sys

from pecas import gerar_nova_peca

from gravidade import INTERVALO_QUEDA

from ranking import criar_tabela, pontos, pontos_recorde

LARGURA_TELA = 500
ALTURA_TELA = 600
TAMANHO_BLOCO = 30
COLUNAS = 10
LINHAS = 20

PRETO = (0, 0, 0)
CINZA = (50, 50, 50)
BRANCO = (255, 255, 255)

PECAS = {
    0: (0, 0, 0),       # Preto
    1: (0, 255, 255),   # Ciano
    2: (255, 255, 0),   # Amarelo
    3: (160, 0, 240),   # Roxo
    4: (240, 160, 0),   # Laranja
    5: (0, 0, 240),     # Azul
    6: (0, 255, 0),     # Verde
    7: (255, 0, 0)      # Vermelho
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
                    
def pontuar_linhas_com_animacao(tela, grade, linhas_completas):
    for frame_anim in range(12):
        tela.fill((0, 0, 0))
        
        desenhar_grade(tela, grade)
        
        for linha in linhas_completas:
            for coluna in range(COLUNAS):
                x = coluna * TAMANHO_BLOCO
                y = linha * TAMANHO_BLOCO
                cor_flash = (255, 255, 255) if frame_anim % 4 < 2 else (200, 200, 200)
                pygame.draw.rect(tela, cor_flash, pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                pygame.draw.rect(tela, CINZA, pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

        pygame.display.flip()
        pygame.time.delay(30)

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

def desenhar_peca_fantasma(tela, peca, grade):
    y_fantasma = peca.obter_posicao_fantasma(grade)
    
    for l_idx, linha in enumerate(peca.matriz):
        for c_idx, valor in enumerate(linha):
            if valor != 0:
                coluna_grid = peca.x + c_idx
                linha_grid = y_fantasma + l_idx
                
                if 0 <= coluna_grid < COLUNAS and 0 <= linha_grid < LINHAS:
                    x = coluna_grid * TAMANHO_BLOCO
                    y = linha_grid * TAMANHO_BLOCO
                    
                    retangulo = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
                    cor_fantasma = PECAS.get(valor, BRANCO)
                    
                    pygame.draw.rect(tela, cor_fantasma, retangulo, 2)

def desenhar_proxima_peca(tela, peca_proxima, fonte):
    pos_x_caixa = (COLUNAS * TAMANHO_BLOCO) + 20
    pos_y_caixa = 120

    texto_next = fonte.render("Next: ", True, BRANCO)
    tela.blit(texto_next, (pos_x_caixa, pos_y_caixa))

    largura_caixa = 140
    altura_caixa = 120
    retangulo_caixa = pygame.Rect(pos_x_caixa, pos_y_caixa + 35, largura_caixa, altura_caixa)

    pygame.draw.rect(tela, (30, 30, 45), retangulo_caixa)
    pygame.draw.rect(tela, CINZA, retangulo_caixa, 2)

    for l_idx, linha in enumerate(peca_proxima.matriz):
        for c_idx, valor in enumerate(linha):
            if valor != 0:
                offset_x = pos_x_caixa + 35 + (c_idx * 25)
                offset_y = pos_y_caixa + 65 + (l_idx * 25)

                corPeca = PECAS.get(valor, BRANCO)
                retangulo_bloco = pygame.Rect(offset_x, offset_y, 24, 24)

                pygame.draw.rect(tela, corPeca, retangulo_bloco)
                pygame.draw.rect(tela, CINZA, retangulo_bloco, 1)


def processar_linhas_completas(tela, grade):
    linhas_completas = [i for i, linha in enumerate(grade) if 0 not in linha]
    if linhas_completas:
        pontuar_linhas_com_animacao(tela, grade, linhas_completas)
        linhas_pontos = pontuar_linhas(grade)
        atualizar_score(linhas_pontos)


def main():
    global score, linhas_totais
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Tetris RA - Sprint 1")
    relogio = pygame.time.Clock()

    fonte_placar = pygame.font.SysFont("consolas", 28, bold=True)
    
    criar_tabela()
    recorde = pontos()

    grade = criar_matriz()
    tempo = pygame.time.get_ticks()
    
    score = 0
    linhas_totais = 0
    game_over = False

    peca_atual = None
    peca_proxima = gerar_nova_peca()

    def peca_segura():
        nonlocal peca_atual, peca_proxima, game_over, recorde
        peca_atual = peca_proxima
        peca_proxima = gerar_nova_peca()
        
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
                        processar_linhas_completas(tela, grade)
                        peca_segura()
                elif evento.key in (pygame.K_UP, pygame.K_w):
                    peca_atual.rotacionar(grade)
                elif evento.key == pygame.K_SPACE:
                    while peca_atual.aplicar_gravidade(grade):
                        pass
                    processar_linhas_completas(tela, grade)
                    peca_segura()
                
        tempo_atual = pygame.time.get_ticks()

        if not game_over:
            if tempo_atual - tempo >= INTERVALO_QUEDA:
                if not peca_atual.aplicar_gravidade(grade):
                    processar_linhas_completas(tela, grade)
                    peca_segura()
                tempo = tempo_atual

        tela.fill(PRETO)
        desenhar_grade(tela, grade)
        desenhar_peca_fantasma(tela, peca_atual, grade)
        desenhar_peca_ativa(tela, peca_atual)

        texto_score = fonte_placar.render(f"SCORE {str(score).zfill(4)}", True, BRANCO)
        posicao_x_placar = (COLUNAS * TAMANHO_BLOCO) + 20
        tela.blit(texto_score, (posicao_x_placar, 20))

        desenhar_proxima_peca(tela, peca_proxima, fonte_placar)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()