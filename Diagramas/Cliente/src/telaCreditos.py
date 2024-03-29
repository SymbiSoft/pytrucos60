#-*- coding: utf-8 -*-
#######################################################
# 
# telaCreditos.py
# Python implementation of the Class TelaCreditos
# Generated by Enterprise Architect
# Created on:      30-mai-2011 14:41:20
# Original author: Wander Jardim
# 
#######################################################

import sysinfo
from graphics import Image

from constantes import *

class TelaCreditos:
    """Classe que mostra as tela de créditos
    """
    imagens = None
    def __init__(self):
        self.largura_tela, self.altura_tela = self.__getTamanho_tela()
        self.espacamento_linha = int(self.altura_tela/16)
        
    def __getTamanho_tela(self):
        return sysinfo.display_pixels()
    
    def carregarImagem(self):
        pass

    def fecharTela(self):
        pass


    def desenha_tela(self, estado_atual, toque):
        self.toque = toque
        self.estado_atual = estado_atual
        telaCreditos = Image.new((self.largura_tela,self.altura_tela))
        mascaraCreditos = Image.new((self.largura_tela,self.altura_tela), 'L')
        telaCreditos.clear((15,126,0)) #Define a cor verde de fundo 0x0f7e00

        if not self.toque.has_key('state') or self.toque['state'] != self.estado_atual:
            if self.toque.has_key('botoes'): del self.toque['botoes'][:]
            self.toque['botoes'] = [((190,self.altura_tela-50),(self.largura_tela-190,self.altura_tela-10))]
            self.toque['state'] = self.estado_atual

        for i in range(len(self.toque['botoes'])):
            telaCreditos.rectangle(self.toque['botoes'][i],outline=0x000000, width=2)
        
        if self.toque.has_key('down') :
            item = self.toque['down']
            telaCreditos.rectangle(self.toque['botoes'][item],outline=0x000000, fill=RGB_LIGHT_BLUE, width=2)

        telaCreditos.text( ( 20, self.altura_tela-300 ) , u' -*- PyTruco4S60 -*- ', 0x000000, "normal")
        telaCreditos.text( ( 20, self.altura_tela-270 ) , u'Autor: Wander Jardim', 0x000000, "normal")
        telaCreditos.text( ( 20, self.altura_tela-240 ) , u'Versão: 1.0', 0x000000, "normal")
        telaCreditos.text( ( 20, self.altura_tela-210 ) , u'E-Mail: wanderjardim@gmail.com', 0x000000, "normal")

        telaCreditos.text( ( self.toque['botoes'][0][0][0] + 30, self.toque['botoes'][0][0][1] + self.espacamento_linha ) , u'Voltar...', 0x000000, "normal")

        return telaCreditos

    def tocou_no_botao(self,pos, botao):
        if  pos[0] >= botao[0][0] and pos[0] <  botao[1][0]\
        and pos[1] >= botao[0][1] and pos[1] <  botao[1][1]:
            return True
        return False

    def voltar_menu(self, pos=(0, 0)):
        "Detecta qual botão foi pressionado"
        if self.toque.has_key('botoes'):
            for i in range(len(self.toque['botoes'])):
                if self.tocou_no_botao(pos, self.toque['botoes'][i]):
                    self.toque['down'] = i
                    break

