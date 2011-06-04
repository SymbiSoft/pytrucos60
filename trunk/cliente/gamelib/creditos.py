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
from graphics import *
import sysinfo
from constantes import *


class Creditos:
    def __init__(self):
        #self.event = onevent
        self.touch = None
        self.lagura_tela,self.altura_tela = self.screen_size()
        self.line_spacing = int(self.altura_tela/16)


    def desenha_tela(self,touch,current_state):
        self.touch = touch
        self.current_state = current_state
        telaCreditos = Image.new((self.lagura_tela,self.altura_tela))
        mascaraCreditos = Image.new((self.lagura_tela,self.altura_tela), 'L')
        telaCreditos.clear((15,126,0)) #Define a cor verde de fundo 0x0f7e00

        if not self.touch.has_key('state') or self.touch['state'] != self.current_state:
            try: del self.touch['buttons'][:]
            except: pass
            self.touch['buttons'] = [((190,self.altura_tela-50),(self.lagura_tela-190,self.altura_tela-10))]
            self.touch['state'] = self.current_state

        for i in range(len(touch['buttons'])):
            telaCreditos.rectangle(touch['buttons'][i],outline=0x000000, width=2)

        if self.touch.has_key('down') :
            item = self.touch['down']
            telaCreditos.rectangle(self.touch['buttons'][item],outline=0x000000, fill=RGB_LIGHT_BLUE, width=2)

        #for i in range(0,300):
        #telaCreditos.clear((15,126,0)) #Define a cor verde de fundo 0x0f7e00
        telaCreditos.text( ( 20, self.altura_tela-300 ) ,    u' -*- PyTruco4S60 -*- ', 0x000000, "normal")
        telaCreditos.text( ( 20, self.altura_tela-270 ) , u'Autor: Wander Jardim', 0x000000, "normal")
        telaCreditos.text( ( 20, self.altura_tela-240 ) , u'Versão: 1.0', 0x000000, "normal")
        telaCreditos.text( ( 20, self.altura_tela-210 ) , u'E-Mail: wanderjardim@gmail.com', 0x000000, "normal")

        telaCreditos.text( ( self.touch['buttons'][0][0][0] + 30, self.touch['buttons'][0][0][1] + self.line_spacing ) , u'Voltar...', 0x000000, "normal")

        return telaCreditos

        #self.canvas.blit(telaCreditos) # mostra a imagem na tela


    #Função Auxiliar, retorna o tamanho da tela
    def screen_size(self):
        return sysinfo.display_pixels()






















