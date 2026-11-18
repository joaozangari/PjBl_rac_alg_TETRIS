import pygame
import sys

from pecas import gerar_nova_peca

from gravidade import INTERVALO_QUEDA

from ranking import criar_tabela, pontos, pontos_recorde

from sons import preparar_audio, carregar_sons, tocar, musica

LARGURA_TELA = 500
ALTURA_TELA = 600
TAMANHO_BLOCO = 30
COLUNAS = 10
LINHAS = 20

PRETO = (0, 0, 0)
CINZA = (50, 50, 50)
BRANCO = (255, 255, 255)
DOURADO = (255, 215, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

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

def tela_inicial(tela, fonte_titulo_inicial, fonte_texto_inicial, relogio, fonte_numero):
    
    jogar = pygame.Rect(150, 340, 200, 100)
    
    sair = pygame.Rect(150, 465, 200, 60)
    
    menu = True
    
    while menu:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "jogar"

                elif evento.key == pygame.K_ESCAPE:
                    return "sair"
        
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:

                    if jogar.collidepoint(evento.pos):
                        return "jogar"

                    elif sair.collidepoint(evento.pos):
                        return "sair"
                    
        tela.fill((10, 10, 10))

        tela_menu = pygame.Rect(50, 50, 400, 500)
    
        pygame.draw.rect(tela, PRETO, tela_menu, border_radius=15)

        blocos_t = [
            (0, 0, (0, 0, 200)),
            (1, 0, (200, 0, 0)),
            (2, 0, (0, 200, 0)),
            (1, 1, (200, 200, 0)),
        ]


        tamanho = 120
        inicio_x = (LARGURA_TELA - 3 * tamanho) // 2
        inicio_y = 65

        for coluna, linha, cor in blocos_t:
            x = inicio_x + coluna * tamanho
            y = inicio_y + linha * tamanho

            retangulo = pygame.Rect(x, y, tamanho, tamanho)

            pygame.draw.rect(tela, cor, retangulo)
            pygame.draw.rect(tela, CINZA, retangulo, 2)
        
        titulo = fonte_titulo_inicial.render("TETRIS", True, BRANCO)
        tela.blit(titulo, titulo.get_rect(center=(250, 145)))
        
        numero = fonte_numero.render("2", True, BRANCO)
        tela.blit(numero, numero.get_rect(center=(250, 265)))
    
        mouse = pygame.mouse.get_pos()

        cor_jogar = VERDE if jogar.collidepoint(mouse) else (0, 120, 0)
        pygame.draw.rect(tela, cor_jogar, jogar, border_radius=8)
        pygame.draw.rect(tela, BRANCO, jogar, 2, border_radius=8)

        texto_jogar = fonte_texto_inicial.render("JOGAR", True, BRANCO)
        tela.blit(texto_jogar, texto_jogar.get_rect(center=jogar.center))

        cor_sair = VERMELHO if sair.collidepoint(mouse) else (140, 0, 0)
        pygame.draw.rect(tela, cor_sair, sair, border_radius=8)
        pygame.draw.rect(tela, BRANCO, sair, 2, border_radius=8)

        texto_sair = fonte_texto_inicial.render("SAIR", True, BRANCO)
        tela.blit(texto_sair, texto_sair.get_rect(center=sair.center))

        pygame.display.flip()
        relogio.tick(60)

    return "sair"


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
        
def linhas_game_over(tela, grade, peca):
    
    linhas_colisao = set()
    
    for l_idx, linha in enumerate(peca.matriz):
        for c_idx, valor in enumerate(linha):
            
            if valor != 0:
                coluna = peca.x + c_idx
                linha_nova = peca.y + l_idx
                
                if (0 <= coluna < COLUNAS and 0 <= linha_nova < LINHAS):
                    
                    if grade[linha_nova][coluna] != 0:
                        linhas_colisao.add(linha_nova)
    
    for frame_anim in range(12):
        tela.fill((0, 0, 0))
        
        desenhar_grade(tela, grade)
        
        for linha in linhas_colisao:
            for coluna in range(COLUNAS):
                x = coluna * TAMANHO_BLOCO
                y = linha * TAMANHO_BLOCO
                cor = VERMELHO if frame_anim % 4 < 2 else (200, 200, 200)

                pygame.draw.rect(tela, cor, pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
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

    texto_next = fonte.render("NEXT: ", True, BRANCO)
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
        
def desenhar_melhor_score(tela, fonte_placar, recorde, fonte_recorde):
    
    texto_score = fonte_placar.render(f"SCORE {str(score).zfill(4)}", True, BRANCO)
    posicao_x_placar = (COLUNAS * TAMANHO_BLOCO) + 20
    tela.blit(texto_score, (posicao_x_placar, 20))
    
    melhor = max(recorde, score)
    texto_melhor = fonte_recorde.render("MELHOR", True, DOURADO)
    texto_melhor_valor = fonte_recorde.render(str(melhor).zfill(4), True, DOURADO)
    tela.blit(texto_melhor, (posicao_x_placar, ALTURA_TELA - 70))
    tela.blit(texto_melhor_valor, (posicao_x_placar, ALTURA_TELA - 40))
    
def desenhar_game_over(tela, fonte_titulo_game_over, fonte_texto_game_over, score, recorde):
    
    tela.fill((10, 10, 10))

    tela_game_over = pygame.Rect(50, 50, 400, 500)
    
    pygame.draw.rect(tela, PRETO, tela_game_over, border_radius=15)
    
    titulo = fonte_titulo_game_over.render("GAME OVER", True, VERMELHO)
    posicao_titulo = titulo.get_rect(center=(250, 180))
    tela.blit(titulo, posicao_titulo)
    
    texto_game_score = fonte_texto_game_over.render(f"SCORE: {score}", True, BRANCO)
    posicao_score = texto_game_score.get_rect(center=(250,270))
    tela.blit(texto_game_score, posicao_score)
    
    texto_recorde = fonte_texto_game_over.render(f"MELHOR SCORE: {recorde}", True, DOURADO)
    posicao_recorde = texto_recorde.get_rect(center=(250,320))
    tela.blit(texto_recorde, posicao_recorde)
    
    botao_reiniciar = pygame.Rect(150, 390, 200, 50)
    botao_sair = pygame.Rect(150, 465, 200, 50)

    mouse = pygame.mouse.get_pos()

    cor_reiniciar = VERDE if botao_reiniciar.collidepoint(mouse) else (0, 120, 0)
    cor_sair = VERMELHO if botao_sair.collidepoint(mouse) else (140, 0, 0)

    pygame.draw.rect(tela, cor_reiniciar, botao_reiniciar, border_radius=8)
    pygame.draw.rect(tela, BRANCO, botao_reiniciar, 2, border_radius=8)

    texto_reiniciar = fonte_texto_game_over.render("TENTAR NOVAMENTE", True, BRANCO)
    tela.blit(texto_reiniciar, texto_reiniciar.get_rect(center=botao_reiniciar.center))

    pygame.draw.rect(tela, cor_sair, botao_sair, border_radius=8)
    pygame.draw.rect(tela, BRANCO, botao_sair, 2, border_radius=8)

    texto_sair = fonte_texto_game_over.render("SAIR", True, BRANCO)
    tela.blit(texto_sair, texto_sair.get_rect(center=botao_sair.center))

    return botao_reiniciar, botao_sair

def main():
    global score, linhas_totais
    
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Tetris RA - Sprint 1")
    relogio = pygame.time.Clock()

    fonte_placar = pygame.font.SysFont("consolas", 28, bold=True)
    fonte_recorde = pygame.font.SysFont("consolas", 24, bold=True)
    fonte_titulo_inicial = pygame.font.SysFont("Consolas", 110, bold=True)
    fonte_texto_inicial = pygame.font.SysFont("Consolas", 50, bold=True)
    fonte_titulo_game_over = pygame.font.SysFont("Consolas", 70, bold=True)
    fonte_texto_game_over = pygame.font.SysFont("Consolas", 22, bold=True)
    fonte_numero = pygame.font.SysFont("Consolas", 130, bold=True)
    
    opcao = tela_inicial(tela, fonte_titulo_inicial, fonte_texto_inicial, relogio, fonte_numero)

    if opcao == "sair":
        pygame.quit()
        sys.exit()
    
    criar_tabela()
    
    while True:
        
        preparar_audio()
            
        carregar_sons()
            
        musica()
        
        recorde = pontos()

        grade = criar_matriz()
        tempo = pygame.time.get_ticks()
        
        botao_reiniciar = pygame.Rect(100, 390, 300, 55)
        botao_sair = pygame.Rect(100, 465, 300, 55)
        
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
                
                linhas_game_over(tela, grade, peca_atual)
                
                game_over = True
                recorde = pontos_recorde(score)
                tocar("game_over")
                
        peca_segura()

        rodando = True
        
        reiniciar = False
        
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                if evento.type == pygame.KEYDOWN:
                    if game_over:
                        if evento.key == pygame.K_RETURN:
                            reiniciar = True
                            rodando = False

                        elif evento.key == pygame.K_ESCAPE:
                            rodando = False
                    
                    else:
                            
                            if evento.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                                direcao = -1 if evento.key in (pygame.K_LEFT, pygame.K_a) else 1
                                x_antes = peca_atual.x
                                peca_atual.mover_horizontal(grade, direcao)
                                if peca_atual.x != x_antes:
                                    tocar("mover")
                            
                            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                                if not peca_atual.aplicar_gravidade(grade):
                                    processar_linhas_completas(tela, grade)
                                    peca_segura()
                                                
                            elif evento.key in (pygame.K_UP, pygame.K_w):
                                peca_atual.rotacionar(grade)
                                tocar("girar")
                                    
                                    
                            elif evento.key == pygame.K_SPACE:
                                while peca_atual.aplicar_gravidade(grade):
                                    pass
                                processar_linhas_completas(tela, grade)
                                peca_segura()
                                tocar("linha")
                                
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if game_over and evento.button == 1:
                        if botao_reiniciar.collidepoint(evento.pos):
                            reiniciar = True
                            rodando = False

                        elif botao_sair.collidepoint(evento.pos):
                            rodando = False
                    
                    
            tempo_atual = pygame.time.get_ticks()

            if not game_over:
                if tempo_atual - tempo >= INTERVALO_QUEDA:
                    if not peca_atual.aplicar_gravidade(grade):
                        processar_linhas_completas(tela, grade)
                        tocar("linha")
                        peca_segura()
                        
                    tempo = tempo_atual
                    
            if game_over:
                
                desenhar_game_over(tela, fonte_titulo_game_over, fonte_texto_game_over, score, recorde)
            
            else:

                tela.fill(PRETO)
                desenhar_grade(tela, grade)
                desenhar_peca_fantasma(tela, peca_atual, grade)
                desenhar_peca_ativa(tela, peca_atual)
                desenhar_melhor_score(tela, fonte_placar, recorde, fonte_recorde)
                desenhar_proxima_peca(tela, peca_proxima, fonte_placar)

            pygame.display.flip()
            relogio.tick(60)
        
        if reiniciar:
            continue
            
        break
    
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()