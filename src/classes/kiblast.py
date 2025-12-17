# Arquivo: src/classes/kiblast.py
import pygame
from src.utils import carregar_imagem, PRETO, VERMELHO

class KiBlast(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao, dano=10):
        super().__init__()
        self.velocidade = 12
        self.dano = dano
        self.direcao = direcao
        
        # Carrega a imagem e inverte se for um tiro do inimigo
        inverter = (direcao == 'esquerda')
        self.image = carregar_imagem('kiblast.png', escala=(25, 25), inverter_x=inverter)

        # Se o carregamento falhou, garante que seja um círculo com cor
        if self.image.get_width() <= 10:
             self.image = pygame.Surface([25, 25], pygame.SRCALPHA)
             cor_ki = (0, 255, 255) if direcao == 'direita' else VERMELHO
             pygame.draw.circle(self.image, cor_ki, (12, 12), 12)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if self.direcao == 'direita':
            self.rect.x += self.velocidade
        else: 
            self.rect.x -= self.velocidade
        
        # Remove KiBlasts que saíram da tela (assumindo LARGURA global no arquivo principal)
        # Como LARGURA não está definida aqui, vamos simplificar a remoção para o arquivo principal.
        pass