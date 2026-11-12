import array
import math
import random

import pygame


efeitos = {}


def preparar_audio():
    pygame.mixer.pre_init(22050, -16, 1, 512)


def criar_tom(freq_ini, freq_fim, duracao, onda="seno", volume=0.4):
    taxa, _, canais = pygame.mixer.get_init()
    total = int(taxa * duracao)
    amostras = array.array("h")
    fase = 0.0

    for i in range(total):
        progresso = i / total
        freq = freq_ini + (freq_fim - freq_ini) * progresso
        fase += 2 * math.pi * freq / taxa

        if onda == "quadrada":
            valor = 1.0 if math.sin(fase) >= 0 else -1.0
        elif onda == "ruido":
            valor = random.uniform(-1, 1)
        else:
            valor = math.sin(fase)

        entrada = min(1.0, i / (taxa * 0.003))
        saida = 1.0 - progresso
        valor = valor * entrada * saida * volume

        for _ in range(canais):
            amostras.append(int(valor * 32767))

    return amostras


def juntar_tons(*tons):
    amostras = array.array("h")
    for tom in tons:
        amostras.extend(tom)
    return pygame.mixer.Sound(buffer=amostras.tobytes())


def carregar_sons():
    efeitos.clear()

    if pygame.mixer.get_init() is None:
        return

    efeitos["mover"] = juntar_tons(criar_tom(330, 330, 0.03, "quadrada", 0.12))

    efeitos["girar"] = juntar_tons(criar_tom(500, 800, 0.06, "quadrada", 0.18))

    efeitos["fixar"] = juntar_tons(criar_tom(170, 50, 0.14, "seno", 0.7))

   
    efeitos["linha"] = juntar_tons(
        criar_tom(523, 523, 0.08, "quadrada", 0.2),
        criar_tom(659, 659, 0.08, "quadrada", 0.2),
        criar_tom(784, 784, 0.08, "quadrada", 0.2),
        criar_tom(1047, 1047, 0.18, "quadrada", 0.2),
    )


    efeitos["game_over"] = juntar_tons(
        criar_tom(400, 380, 0.2, "quadrada", 0.2),
        criar_tom(320, 300, 0.2, "quadrada", 0.2),
        criar_tom(240, 220, 0.2, "quadrada", 0.2),
        criar_tom(200, 80, 0.5, "quadrada", 0.2),
    )


def tocar(nome):
    if nome in efeitos:
        efeitos[nome].play()