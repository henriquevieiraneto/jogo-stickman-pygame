import pygame
import sys
import random
from src.classes.guerreiro import Guerreiro
from src.classes.inimigo import Inimigo
from src import (desenhar_texto, desenhar_barra_saude, carregar_fonte, 
                 carregar_som, AZUL_CEU, AMARELO, BRANCO, PRETO)

class DragonBallGame:
    def __init__(self):
        pygame.init()
        self.LARGURA, self.ALTURA = 900, 650
        self.TELA = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("DBZ: Ultra Engine Pro")
        self.CLOCK = pygame.time.Clock()
        
        self.shake = 0
        self.pausado = False
        self.nivel_global = 1
        
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks: j.init()
        
        self.inicializar_entidades()

    def inicializar_entidades(self):
        self.g_ki_aliado = pygame.sprite.Group()
        self.g_ki_inimigo = pygame.sprite.Group()
        self.g_inimigos = pygame.sprite.Group()
        
        self.goku = Guerreiro(200, 325, self.LARGURA, self.ALTURA, self.g_ki_aliado)
        self.freeza = Inimigo(700, 325, self.g_ki_inimigo, self.nivel_global)
        self.g_inimigos.add(self.freeza)

    def processar_eventos(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.JOYBUTTONDOWN:
                if ev.button == 9: self.pausado = not self.pausado
                if ev.button in [10, 11]: self.freeza.travado = not self.freeza.travado
                
                if not self.pausado:
                    if ev.button == 1: # Bolinha
                        if self.goku.atirar_ki(): carregar_som('tiro_ki.wav').play()
                    if ev.button == 2: # Quadrado
                        if self.goku.socar(self.g_inimigos):
                            carregar_som('soco.wav').play()
                            self.shake = 15
                            pygame.time.delay(40)
                    if ev.button == 3: # Triângulo
                        if self.goku.transformar():
                            carregar_som('transformar.wav').play()
                            self.shake = 20

    def atualizar(self):
        if self.pausado: return

        dx, dy = 0, 0
        if self.joysticks:
            joy = self.joysticks[0]
            if abs(joy.get_axis(0)) > 0.3: dx = 1 if joy.get_axis(0) > 0 else -1
            if abs(joy.get_axis(1)) > 0.3: dy = 1 if joy.get_axis(1) > 0 else -1
            
            self.goku.bloqueando = joy.get_button(5) # R1
            if joy.get_button(0): self.goku.carregar_ki()
            elif self.goku.estado == 'carregando': self.goku.estado = 'parado'

        self.goku.mover(dx, dy, self.freeza.rect)
        self.goku.update()
        self.freeza.update()
        self.g_ki_aliado.update()
        self.g_ki_inimigo.update()

        # Colisões e Progressão
        for ki in self.g_ki_inimigo:
            if self.goku.rect.colliderect(ki.rect):
                ki.kill()
                self.shake = 10
                if self.goku.levar_dano(15, self.freeza.ki_max):
                    self.nivel_global = 1
                    self.inicializar_entidades()

        if self.freeza.saude_atual <= 0:
            self.nivel_global += 1
            self.inicializar_entidades()

    def desenhar(self):
        off = (random.randint(-self.shake, self.shake), random.randint(-self.shake, self.shake))
        if self.shake > 0: self.shake -= 1

        self.TELA.fill((10, 10, 15))
        cenario = pygame.Surface((self.LARGURA, self.ALTURA))
        cenario.fill(AZUL_CEU)
        
        # Ordem de renderização
        for img, pos, alpha in self.goku.rasto_movimento:
            img.set_alpha(alpha); cenario.blit(img, pos)
        for p in self.goku.particles: p.draw(cenario)
        
        self.g_ki_aliado.draw(cenario)
        self.g_ki_inimigo.draw(cenario)
        self.g_inimigos.draw(cenario)
        cenario.blit(self.goku.image, self.goku.rect)

        if self.goku.bloqueando:
            pygame.draw.circle(cenario, (255, 255, 255), self.goku.rect.center, 78, 4)

        self.TELA.blit(cenario, off)
        self.renderizar_hud()
        
        if self.pausado:
            overlay = pygame.Surface((self.LARGURA, self.ALTURA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.TELA.blit(overlay, (0,0))
            desenhar_texto(self.TELA, "JOGO PAUSADO", carregar_fonte(None, 60), 450, 325, BRANCO)

        pygame.display.flip()

    def renderizar_hud(self):
        pygame.draw.rect(self.TELA, (15, 15, 20), (20, 20, 300, 100), border_radius=10)
        desenhar_barra_saude(self.TELA, 35, 35, self.goku.saude_atual, self.goku.saude_max, 260)
        
        ki_p = (self.goku.ki_atual / self.goku.ki_max) * 260
        pygame.draw.rect(self.TELA, (0, 0, 60), (35, 60, 260, 12))
        pygame.draw.rect(self.TELA, (0, 180, 255), (35, 60, ki_p, 12))
        
        info = f"{self.goku.nomes_formas[self.goku.nivel]} | LVL {self.nivel_global}"
        if self.freeza.travado: info += " [TRAVA ON]"
        desenhar_texto(self.TELA, info, carregar_fonte(None, 18), 35, 85, AMARELO)
        
        # Barra do Inimigo
        desenhar_barra_saude(self.TELA, 620, 35, self.freeza.saude_atual, self.freeza.saude_max, 250)
        desenhar_texto(self.TELA, f"FREEZA HP: {int(self.freeza.saude_atual)}", carregar_fonte(None, 18), 620, 65, BRANCO)

    def executar(self):
        while True:
            self.processar_eventos(); self.atualizar(); self.desenhar()
            self.CLOCK.tick(60)

if __name__ == "__main__":
    DragonBallGame().executar()