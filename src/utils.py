# Arquivo: src/utils.py
import pygame
import os

# --- CONFIGURAÇÕES DE COR GLOBAIS ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL_CEU = (0, 150, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

# Caminho base para os recursos
# CORREÇÃO: Navega apenas um nível acima (de src/ para o diretório principal do projeto)
PASTA_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') 

PASTA_GRAFICOS = os.path.join(PASTA_BASE, 'assets', 'graphics')
PASTA_FONTES = os.path.join(PASTA_BASE, 'assets', 'fonts')
PASTA_SONS = os.path.join(PASTA_BASE, 'assets', 'sounds')

def carregar_imagem(nome_arquivo, escala=None, inverter_x=False):
    """Carrega uma imagem com tratamento de erro e redimensionamento."""
    caminho = os.path.join(PASTA_GRAFICOS, nome_arquivo)
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        if escala:
            imagem = pygame.transform.scale(imagem, escala)
        if inverter_x:
             imagem = pygame.transform.flip(imagem, True, False)
        return imagem
    except pygame.error as e:
        print(f"ERRO: Não foi possível carregar a imagem '{caminho}'. {e}")
        # Retorna uma superfície simples em caso de erro
        superficie_erro = pygame.Surface((60, 90))
        superficie_erro.fill(VERMELHO)
        return superficie_erro

def carregar_fonte(nome_arquivo, tamanho):
    """Tenta carregar uma fonte TTF."""
    if nome_arquivo is None:
        # Usa a fonte padrão do Pygame (quando nome_arquivo é None)
        return pygame.font.Font(None, tamanho)
        
    caminho = os.path.join(PASTA_FONTES, nome_arquivo)
    try:
        return pygame.font.Font(caminho, tamanho)
    except FileNotFoundError:
        # Tenta carregar a fonte padrão do sistema se a fonte temática não for encontrada
        print(f"AVISO: Fonte '{nome_arquivo}' não encontrada em {caminho}. Usando fonte padrão.")
        return pygame.font.Font(None, tamanho)

def carregar_som(nome_arquivo):
    """Carrega um arquivo de som com tratamento de erro."""
    caminho = os.path.join(PASTA_SONS, nome_arquivo)
    try:
        # Garante que o mixer esteja inicializado antes de carregar o som
        if not pygame.mixer.get_init():
             pygame.mixer.init()
        som = pygame.mixer.Sound(caminho)
        return som
    except pygame.error as e:
        print(f"AVISO: Não foi possível carregar o som '{caminho}'. {e}")
        return None # Retorna None se falhar

def desenhar_texto(surface, texto, fonte, x, y, cor=BRANCO):
    """Renderiza e desenha o texto na tela usando a fonte fornecida."""
    text_surface = fonte.render(texto, True, cor)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def desenhar_barra_saude(surface, x, y, hp, hp_max, comprimento=100, altura=10):
    """Desenha uma barra de saúde na tela."""
    if hp < 0: hp = 0
    
    fundo_rect = pygame.Rect(x, y, comprimento, altura)
    pygame.draw.rect(surface, PRETO, fundo_rect, 1)
    
    largura_atual = (hp / hp_max) * comprimento
    if hp / hp_max > 0.6:
        cor = VERDE
    elif hp / hp_max > 0.3:
        cor = AMARELO
    else:
        cor = VERMELHO
        
    saude_rect = pygame.Rect(x, y, largura_atual, altura)
    pygame.draw.rect(surface, cor, saude_rect)