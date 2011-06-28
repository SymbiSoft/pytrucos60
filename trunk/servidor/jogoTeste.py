#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Jan 05, 2011

@author: Wander Jardim
'''
import os
import sys

def prepara_path():
    """Carrega o diretório fonte no sys.path.

    Isso só será necessário quando estiver executando uma distribuição fonte. 
    Distribuições binária já garantem que o caminho do módulo contém os módulos 
    de qualquer maneira.

    """
    try:
        __file__
    except NameError, e:
        print e
    else:
        rel = lambda s: os.path.abspath(os.path.join(os.path.dirname(__file__), s))
        sys.path.insert(0, rel("lib.zip"))
    
    
    if os.path.exists("gamelib"):
        sys.path.insert(1, "gamelib")


prepara_path()



import logging
log = logging.getLogger('jogo')
log.debug("importado")

import cocos
from cocos.director import director
from cocos.actions import *
from cocos.scene import Scene

from pyglet.event import EventDispatcher
import pyglet


from hud import Hud
import game_audio

from bg_layer import BGLayer
from logicaTruco import *



class JogoT(cocos.layer.Layer):
    def __init__(self):
        super(JogoT, self).__init__()

        # Configurando camadas
        # HUD
        self.hud = Hud(self)
        self.add(self.hud, z=-1)
        self.alturaTela, self.larguraTela = director.get_window_size()
        print "Altura: %s - Largura: %s" %(self.alturaTela, self.larguraTela)
        baralho = Baralho()
        baralho.embaralhar()
        
        jogador1 = Jogador("Wander", 1)
        jogador2 = Jogador("Luana", 2)
        jogador3 = Jogador("Marluce", 1)
        jogador4 = Jogador("Ataide", 2)
        
        jogadoresGlobal = [jogador1, jogador2, jogador3, jogador4]
        
        mesa = Mesa(jogadoresGlobal, baralho)
        mesa.definirEquipes()
        mesa.definirOrdemJogadores()
        
        mesa.distrubuirCartas()
        rectSprites = jogador1.mao[0].imagem.get_rect()
        
        Sprite1 = jogador1.mao[0].imagem
        Sprite1.position = 0,0
        Sprite1.image_anchor_x = 0
        Sprite1.image_anchor_y = 0
        
        
        Sprite2 = jogador1.mao[2].imagem
        Sprite2.position = 0,0
        Sprite2.image_anchor_x = -100
        Sprite2.image_anchor_y = -100
        
        
        self.add(Sprite1, z=1 )
        self.add(Sprite2, z=1 )
        
        print "Rect carta:"
        print rectSprites
        pos = 325
        for carta in jogador1.mao:
            #carta.imagem.position = (12, 10)
            #carta.imagem.anchor_x = "top"
            #self.add(carta.imagem, z=1 )
            pos += 76
            
            rectSprites = carta.imagem.get_rect()
            print "Rect carta:"
            print "Largura: %s " % rectSprites.width
            print "Altura: %s" % rectSprites.height
            
        
        #cartaJogador1 = jogador1.jogarCarta(randrange(0, len(mesa.equipes[0].jogadores[0].mao)))
        #mesa.cartas.append(cartaJogador1)
        
                
        #self.remove(testeImg)
   
    def desenhaMesaJogo(self):
       pass


        
    def on_quit(self):
        # called by esc
        director.scene.end()
        director.scene.end()
        


def run():
    return JogoT()


if __name__ == '__main__':

    director.init(width=800, height=600, do_not_scale=True)  
    main_scene = Scene (BGLayer("mesa"), run())
  
    
    director.run(main_scene)