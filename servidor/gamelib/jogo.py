#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Jan 05, 2011

@author: Wander Jardim
'''
import logging
log = logging.getLogger('jogo')
log.debug("importado")

import cocos
from cocos.director import director
from cocos.actions import *

from pyglet.event import EventDispatcher
import pyglet

import threading
from threading import Thread, Timer
import time

from jogador import JogadorBT
from hud import Hud
from conexao import ConexaoBT
import game_audio






class Jogo(cocos.layer.Layer, EventDispatcher): # must be layer - scene causes anims/actions to fail
    def __init__(self, jogadores):
        super(Jogo, self).__init__()
        self.nrJogadores=0
        self.partidaIniciada = False
        self.jogadores = jogadores
        # Configurando camadas
        # HUD
        self.hud = Hud(self)
        game_audio.next_song()
        self.add(self.hud, z=-1)
        self.do(Delay(3) +CallFunc(self.dispatch_event,'on_game_start') )
        game_audio.play_song('music_background1.ogg')
        if self.jogadores == []:
            print "Jogadores veio vazio!"
        else:
            for i in self.jogadores:
                th = Thread(target=self.aguarda_comando, args=(i,))
                th.setDaemon(True)
                th.start()
                i.envia_comando("Bem Vindo ao Jogo!!")
                time.sleep(2)
                i.envia_comando("iniciaPartida")
        print "Vai começar a recepção:"
   
        
    def aguarda_comando(self, jogador):
        i = 0
        while True:
            msg = jogador.recebe_comando()
            print "Recebi isso: "
            print msg
            if msg == "sair":
                break
            elif msg.startswith("bcst"):
                for i in self.jogadores:
                    self.jogadores[i].envia_comando(msg)
                
            else:
                print "Recebi isso mesmo: "
                print msg
        jogador.desconecta()
        self.hud.desconectaJogador(jogador.nome)
        #director.pop()
        #director.pop()
        #ou
        #director.scene.end()
        
    def on_quit(self):
        # called by esc
        director.scene.end()
        director.scene.end()
        

class ComandosJogador(threading.Thread):
    def __init__ (self, jogador):
        threading.Thread.__init__(self)
        self.jogador = jogador
        
    def run(self):
        self.jogador.estahRodando = True
        print self.jogador.recebe_comando()

Jogo.register_event_type('on_game_start')   
Jogo.register_event_type('on_xp_gain')   
Jogo.register_event_type('on_game_over')
Jogo.register_event_type('on_gamer_connect')
Jogo.register_event_type('on_server_status')

def run(jogadores): #tipo_conexao):
    return Jogo(jogadores) #tipo_conexao)

if __name__ == '__main__':

    director.init(width=640, height=480, do_not_scale=True)    
    director.run(run())