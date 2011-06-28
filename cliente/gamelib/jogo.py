# -*- coding: utf-8 -*-
#######################################################
# 
# jogo.py
# Python implementation of the Class Jogo
# Generated by Enterprise Architect
# Created on:      31-mai-2011 15:43:56
# Original author: Wander Jardim
# 
#######################################################

import appuifw
import sysinfo
from graphics import Image
import traceback

import clienteBT
from constantes import *
import util

class Jogo:
    def __init__(self, conexao):
        self.render=0
        file_erro = open('E:\\Python\\Meu_error2.log', 'r+')
        self.conexao = conexao
        self.largura_tela, self.altura_tela = util.getTamanho_tela()
        self.telajogo = Image.new((self.largura_tela,self.altura_tela))
        
        self.canvas = appuifw.Canvas(event_callback = None,
                                     redraw_callback = self.event_redraw)
        appuifw.app.body = self.canvas
        self.render=1

        self.fundoMesa = util.cria_imagem('fundoMesa.png')
        self.telajogo.blit(self.fundoMesa)
        # mostra a imagem na tela
        self.canvas.blit(self.telajogo)



    def mostra_cartas(self):    
        
        if self.conexao.esta_conectado():
            pos = 95
            while True:
                data = self.conexao.recebe_comando()
                if data == '':
                    break
                elif data=='dsd##%#%s':
                    self.conexao.envia_comando("OK")
                else:
                    self.telajogo.text((10, pos), u"recv >> %s" % data, fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
                    self.canvas.blit(self.telajogo)
                pos += 15

    def event_redraw(self, other):
        if self.render == 0:
            self.canvas.clear()
            self.telajogo.clear((15,126,0))
            self.canvas.blit(self.telajogo)

    def desenha_mesa(self):
        self.mesa=self.load_image(self.path_imgs + "\\fundoMesa.png")
        self.canvas.blit(self.telajogo)

    def desenha_cartas(self):
        self.splash=self.load_image(self.path_imgs + "\\splash.png")



    #Calculates aspect ratio and resize original image
    def load_image(self, filename):
        #Carrega imagem referente ao parametro passado. Se a imagem não existir no diretório, retorna vazio.
        canvas = appuifw.Canvas(None, None)
        self.lagura_tela,self.altura_tela = self.screen_size()
        canvas = None
        border_perc = None
        try:
            img = Image.open(filename)
            return img
        except:
            print "Imagem não encontrada!"
            return None
