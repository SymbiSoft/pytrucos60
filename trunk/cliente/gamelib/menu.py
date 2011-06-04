#-*- coding: utf-8 -*-
# Author: Wander Jardim
# email: wanderjardim@gmail.com
#        Copyright 2011
# About: The main application class, will hold event processing
# code as also objects to represent windows.

'''
/*  Copyright (C) 2011  Wander Jardim <wanderjardim@gmail.com>
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; by version 2 of the License.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */
'''

import appuifw
from graphics import *
import sysinfo
import key_codes
import e32
#from game import *


class menu:
    buttons = {}
    
    def __init__(self, pathimgs, current_state):
        self.path_imgs = pathimgs
        self.touch = {}
        self.running = 0
        self.current_state = current_state
        self.lagura_tela,self.altura_tela = None,None
        self.cria_imagens_menu()
        # Enable these displays, now all prompts are over
        
        

    # Carrega as imagens dos botões e do fundo do menu inicial
    def cria_imagens_menu(self):
        #Carrega a imagem do splash (Imagem que aparece quando inicia a aplicação)
        self.splash=self.load_image(self.path_imgs + "\\splash.png")

        
        self.fundoMenu=self.load_image(self.path_imgs + "\\TelaMenu.png")

        #Carrega a imagem do botão Jogar. 
        self.buttons['jogar'] = self.load_image(self.path_imgs + "\\btn_jogar_off.png")
        self.buttons['jogar_down'] = self.load_image(self.path_imgs + "\\btn_jogar_on.png")

        #Carrega a imagem do botão Conexões. Se a imagem não existir no diretório, define como vazio.
        self.buttons['conexao'] = self.load_image(self.path_imgs + "\\btn_conexao_off.png")
        self.buttons['conexao_down'] = self.load_image(self.path_imgs + "\\btn_conexao_on.png")

        #Carrega a imagem do botão Conexões. Se a imagem não existir no diretório, define como vazio.
        self.buttons['opcoes'] = self.load_image(self.path_imgs + "\\btn_opcoes_off.png")
        self.buttons['opcoes_down'] = self.load_image(self.path_imgs + "\\btn_opcoes_on.png")

        #Carrega a imagem do botão Creditos. Se a imagem não existir no diretório, define como vazio.
        self.buttons['creditos'] = self.load_image(self.path_imgs + "\\btn_creditos_off.png")
        self.buttons['creditos_down'] = self.load_image(self.path_imgs + "\\btn_creditos_on.png")
        
        #Carrega a imagem do botão Instrucoes. Se a imagem não existir no diretório, define como vazio.
        self.buttons['instrucoes'] = self.load_image(self.path_imgs + "\\btn_instrucoes_off.png")
        self.buttons['instrucoes_down'] = self.load_image(self.path_imgs + "\\btn_instrucoes_on.png")
        
        #Carrega a imagem do botão Sair. Se a imagem não existir no diretório, define como vazio.
        self.buttons['sair'] = self.load_image(self.path_imgs + "\\btn_sair_off.png")
        self.buttons['sair_down'] = self.load_image(self.path_imgs + "\\btn_sair_on.png")


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




    def desenha_menu(self):
        telaMenu = Image.new((self.lagura_tela,self.altura_tela))
        telaMenu.clear((15,126,0)) #Define a cor verde de fundo 0x0f7e00
        telaMenu.blit(self.fundoMenu, target =(0,0))

        margem_botao_esq = self.lagura_tela/2+1
        margem_botao_dir = self.lagura_tela/2+153
        
        if not self.touch.has_key('state') or self.touch['state'] != self.current_state: # criar uma lista de novos botões
            but = []
            but.append( (( margem_botao_esq , 83), (margem_botao_dir, 127 )) )
            but.append( (( margem_botao_esq ,127), (margem_botao_dir, 171 )) )
            but.append( (( margem_botao_esq ,171), (margem_botao_dir, 215 )) )
            but.append( (( margem_botao_esq ,215), (margem_botao_dir, 259 )) )
            but.append( (( margem_botao_esq ,259), (margem_botao_dir, 303 )) )
            but.append( (( margem_botao_esq ,303), (margem_botao_dir, 345 )) )

            if self.touch.has_key('buttons'): del self.touch['buttons'][:]
            self.touch['state'] = self.current_state
            self.touch['buttons'] = but

        for i in range(len(self.touch['buttons'])):
            telaMenu.rectangle(self.touch['buttons'][i],outline=0x000000, width=2)

        def blit_button(name, xpos):
            if self.touch.has_key('main_down') and self.touch['main_down'] == name:
                name += '_down'

            if self.buttons[name]:
                telaMenu.blit(self.buttons[name], target = xpos ) #, scale = 2)

        blit_button('jogar',       self.touch['buttons'][0][0])
        blit_button('conexao',     self.touch['buttons'][1][0])
        blit_button('opcoes',      self.touch['buttons'][2][0])
        blit_button('creditos',    self.touch['buttons'][3][0])
        blit_button('instrucoes',  self.touch['buttons'][4][0])
        blit_button('sair',        self.touch['buttons'][5][0])
        
        return telaMenu


    #Função Auxiliar, retorna o tamanho da tela
    def screen_size(self):
        return sysinfo.display_pixels()

    #Exit function
    def quit(self):
        self.running = -1
        #if self.bt != None:
        #    print u'EXIT'
        #    self.bt.write_line(u'CONN_CLOSE')
        #    self.bt.close()
        #lock = e32.Ao_lock() 
        self.lock_menu.signal()
        print "tchau!"
        #appuifw.app.set_exit() #TODO:Voltar essa linha quando for compilar para SIS.