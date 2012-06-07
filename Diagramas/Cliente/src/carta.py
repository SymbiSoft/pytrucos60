#######################################################
# 
# carta.py
# Python implementation of the Class Carta
# Generated by Enterprise Architect
# Created on:      26-jul-2011 17:35:58
# Original author: Wander Jardim
# 
#######################################################
from constantes import *

class Carta(object):
    posicao_mesa = None
    rect = None
    source = None
    pos_marca_selecao = None
    imagem = None
    valor = None
    selecionada = None
    
    def __init__(self, pos_mesa, source, pos_marca_selecao, valor):
        self.posicao_mesa = pos_mesa
        self.rect = (self.posicao_mesa, (self.posicao_mesa[0]+LARGU_CARTA, self.posicao_mesa[1]+ALTUR_CARTA))
        self.source = source
        self.pos_marca_selecao = pos_marca_selecao
        self.imagem = Image.new((LARGU_CARTA,ALTUR_CARTA))
        self.valor = valor
        self.selecionada = False