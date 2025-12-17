import pygame
import random
from src.classes.particle import Particle
from src.classes.kiblast import KiBlast

class Guerreiro(pygame.sprite.Sprite):
    def __init__(self, x, y, largura_tela, altura_tela, grupo_aliado_ki):
        super().__init__()
        # --- STATUS BASE ---
        self.saude_max = 100
        self.saude_atual = self.saude_max
        self.ki_max = 100
        self.ki_atual = 0
        self.dano_base = 25
        self.velocidade = 8
        self.nivel = 0
        self.nomes_formas = ["Base", "SSJ", "SSJ2", "SSJ3", "SSJ4", "God", "Blue", "UI"]
        
        # --- VISUAIS ---
        self.particles = []
        self.rasto_movimento = []
        self.cores_aura = [
            (255, 255, 255), (255, 255, 0), (255, 255, 150), (255, 215, 0),
            (200, 0, 0), (255, 50, 50), (0, 150, 255), (200, 200, 255)
        ]
        
        # --- ESTADOS ---
        self.bloqueando = False
        self.socando = False
        self.tempo_soco = 0
        self.direcao_olhando = 'direita'
        self.estado = 'parado'
        
        self.LARGURA, self.ALTURA = largura_tela, altura_tela
        self.grupo_ki = grupo_aliado_ki
        self.carregar_assets()
        self.rect = self.image.get_rect(center=(x, y))

    def carregar_assets(self):
        from src.utils import carregar_imagem
        escala = (85, 115)
        self.animacao = {
            'parado': [carregar_imagem('goku_parado_1.png', escala), carregar_imagem('goku_parado_2.png', escala)],
            'andando': [carregar_imagem('goku_andando_1.png', escala), carregar_imagem('goku_andando_2.png', escala)],
            'carregando': [carregar_imagem('goku_parado_1.png', escala)]
        }
        self.frame_atual = 0
        self.image = self.animacao['parado'][0]

    def mover(self, dx, dy, inimigo_rect):
        if not self.bloqueando:
            if dx != 0 or dy != 0:
                self.estado = 'andando'
                antigo_rect = self.rect.copy()
                self.rect.x += dx * self.velocidade
                self.rect.y += dy * self.velocidade
                
                if self.rect.colliderect(inimigo_rect):
                    self.rect = antigo_rect
                
                # Rasto profissional (Motion Blur)
                if random.random() > 0.6:
                    self.rasto_movimento.append([self.image.copy(), self.rect.topleft, 160])
            else:
                if self.estado != 'carregando': self.estado = 'parado'
            
            self.direcao_olhando = 'direita' if self.rect.centerx < inimigo_rect.centerx else 'esquerda'

    def levar_dano(self, dano, ki_max_adv):
        if self.bloqueando:
            if self.ki_max < ki_max_adv:
                dano *= 0.2
                self.ki_atual = max(0, self.ki_atual - 3)
            elif self.ki_max == ki_max_adv:
                dano = 0
                self.ki_atual = max(0, self.ki_atual - 1)
            else: dano = 0 
        self.saude_atual -= dano
        return self.saude_atual <= 0

    def socar(self, grupo_inimigos):
        self.socando = True
        self.tempo_soco = pygame.time.get_ticks()
        hitbox = self.rect.inflate(80, 30)
        hitbox.x += 50 if self.direcao_olhando == 'direita' else -50
        for inimigo in grupo_inimigos:
            if hitbox.colliderect(inimigo.rect):
                return inimigo.levar_dano(self.dano_base)
        return False

    def carregar_ki(self):
        if self.ki_atual < self.ki_max:
            self.ki_atual += 2.5
            self.estado = 'carregando'
            cor = self.cores_aura[self.nivel]
            for _ in range(5):
                px = self.rect.centerx + random.randint(-40, 40)
                py = self.rect.bottom - random.randint(0, 15)
                self.particles.append(Particle(px, py, cor))

    def transformar(self):
        if self.ki_atual >= self.ki_max and self.nivel < 7:
            self.nivel += 1
            self.ki_atual = 0
            self.saude_max += 100
            self.saude_atual = self.saude_max
            self.ki_max += 50
            self.dano_base += 15
            self.velocidade += 1
            return True
        return False

    def atirar_ki(self):
        if self.ki_atual >= 15:
            self.ki_atual -= 15
            pos_x = self.rect.right if self.direcao_olhando == 'direita' else self.rect.left
            self.grupo_ki.add(KiBlast(pos_x, self.rect.centery, self.direcao_olhando, self.dano_base))
            return True
        return False

    def update(self):
        for r in self.rasto_movimento[:]:
            r[2] -= 20
            if r[2] <= 0: self.rasto_movimento.remove(r)
        for p in self.particles[:]:
            p.update()
            if p.vida <= 0: self.particles.remove(p)

        tempo = pygame.time.get_ticks()
        if self.socando and tempo - self.tempo_soco > 200: self.socando = False
        self.frame_atual = (tempo // 120) % len(self.animacao[self.estado])
        img = self.animacao[self.estado][self.frame_atual]
        self.image = pygame.transform.flip(img, True, False) if self.direcao_olhando == 'esquerda' else img
        self.rect.clamp_ip(pygame.Rect(0, 0, self.LARGURA, self.ALTURA))