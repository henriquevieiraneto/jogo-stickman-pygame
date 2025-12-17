import pygame
import random

class Particle:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor
        self.velocidade_y = random.uniform(-4, -1)
        self.velocidade_x = random.uniform(-2, 2)
        self.vida = 255  # Opacidade (Alpha)
        self.tamanho = random.randint(3, 7)

    def update(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        self.vida -= 10  # Desvanece rápido
        if self.tamanho > 0.2:
            self.tamanho -= 0.1

    def draw(self, surface):
        if self.vida > 0:
            # Desenha um círculo com transparência
            p_surf = pygame.Surface((self.tamanho*2, self.tamanho*2), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*self.cor, self.vida), (self.tamanho, self.tamanho), self.tamanho)
            surface.blit(p_surf, (self.x - self.tamanho, self.y - self.tamanho))