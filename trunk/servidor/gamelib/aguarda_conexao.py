#-*- coding: utf-8 -*-
#!/usr/bin/env python


import cocos
from cocos.menu import *
from cocos.text import Label
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import *
from cocos.scenes.transitions import *

import jogo
from hud import Hud
import constantes
from jogador import JogadorBT
from conexao import ConexaoBT



class MenuIniciaPartida(Menu):
    def __init__(self):
        super( MenuIniciaPartida, self).__init__() 
        self.font_item['font_size'] = 16
        self.font_item['color'] = (189,190,190,255)
        self.font_item_selected['font_size'] = 24
        self.font_item_selected['color'] = (128,16,32,255)
        
        items = []
        items.append( MenuItem('Iniciar Partida', self.inicia_partida) )
        self.create_menu(items)

    def inicia_partida(self):
        # called by esc
        director.push(Scene (jogo.run()))

    def on_quit(self):
        # called by esc
        director.scene.end()


class TelaConexoes(cocos.layer.Layer):


    def __init__(self, tipo_conexao):
        super( TelaConexoes, self).__init__()
        
        self.nrJogadores=0
        self.tipo_conexao = tipo_conexao
        self.partidaIniciada = False
        
        print "tipo de conexao => %s " % self.tipo_conexao
        
        # Configurando camadas
        # HUD
        self.hud = Hud(self)
        
        self.add(self.hud, z=-1)
        
        
        self.jogadores = Label("Aguardando conexao", font_name='Times New Roman',
            font_size=23,
            x=30, y=600,
            anchor_x='left', anchor_y='top')
        
        
        self.add(self.jogadores)
        
        
        self.jogadores = []
        if self.tipo_conexao == 'bluetooth':
            self.conexao = ConexaoBT()
            self.conexao.socket_servidor()
            self.conecta_jogadoresBT()
        else:
            socket = None
        self.nrJogador=0
        
        
    
        
        
    def conecta_jogadoresBT(self):
        self.nrJogador = 0
        while not self.partidaIniciada:
            print "Rodei pela %sa. vez" % self.nrJogador
            self.jogadores.append(JogadorBT(self.conexao, self.hud, self.nrJogador))
            self.jogadores[self.nrJogador].setDaemon(True)
            self.jogadores[self.nrJogador].start()
            self.nrJogador+=1
            
            if len(self.jogadores)>=2:
                self.partidaIniciada = True
        self.nrJogadores = len(self.jogadores)        



        
        
    


def get_menu_conexao(tipo_conexao):
    scene = Scene()
    scene.add( MultiplexLayer(
                    TelaConexoes(tipo_conexao) 
                    ),
                z=2 )
    
    scene.add( MenuIniciaPartida(), z=0 )
    
    return scene
        
        
        
        