import pygame
import random
from src.utils import carregar_imagem
from src.classes.kiblast import KiBlast

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_aliado_ki, nivel=1):
        super().__init__()
        # --- STATUS ESCALONÁVEIS ---
        self.nivel = nivel
        self.saude_max = 100 + (nivel - 1) * 50  # +50 HP por nível
        self.saude_atual = self.saude_max
        self.ki_max = 100 + (nivel - 1) * 20    # Relevante para sua defesa R1
        self.dano_tiro = 10 + (nivel * 2)
        self.velocidade = 2 + (nivel * 0.5)
        
        # --- SISTEMA DE TESTE ---
        self.travado = False  # Modo Debug
        
        self.grupo_aliado_ki = grupo_aliado_ki
        self.image = carregar_imagem('freeza.png', (80, 110), inverter_x=True)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.ultimo_ataque = pygame.time.get_ticks()
        self.intervalo_ataque = max(500, 2000 - (nivel * 100)) # Fica mais rápido

    def levar_dano(self, dano):
        if self.travado: return False # Não toma dano se estiver travado
        self.saude_atual -= dano
        return self.saude_atual <= 0

    def update(self):
        if self.travado: 
            return # Se estiver travado, não se move nem atira

        # IA Simples
        self.rect.y += random.choice([-self.velocidade, 0, self.velocidade])
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > 600: self.rect.bottom = 600
        
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque > self.intervalo_ataque:
            ki = KiBlast(self.rect.left, self.rect.centery, 'esquerda', dano=self.dano_tiro)
            self.grupo_aliado_ki.add(ki)
            self.ultimo_ataque = agora