# Arquivo: src/__init__.py

# Expõe as funções utilitárias importantes e TODAS as CONSTANTES de cor
# do módulo utils para importação direta através do pacote 'src'.
from .utils import (
    desenhar_texto, 
    desenhar_barra_saude, 
    carregar_fonte, 
    carregar_imagem, 
    carregar_som, # <<< EXPORTANDO carregar_som
    PRETO, 
    BRANCO, 
    VERMELHO, 
    VERDE, 
    AMARELO,
    AZUL_CEU
)