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
from pyglet.event import EventDispatcher
from cocos.actions import *
import pyglet

from jogador import JogadorBT

import threading
from threading import Thread, Timer
from hud import Hud

from conexao import ConexaoBT

import game_audio


import time



class Jogo(cocos.layer.Layer, EventDispatcher): # must be layer - scene causes anims/actions to fail
    eh_manipuador_eventos = True # for actions to work

    def __init__(self, jogadores): #, tipo_conexao):
        super(Jogo, self).__init__()
        self.nrJogadores=0
        self.tipo_conexao = 'ooo' #tipo_conexao
        self.partidaIniciada = False

        print "tipo de conexao => %s " % self.tipo_conexao


        # Configurando camadas
        # HUD
        self.hud = Hud(self)

        game_audio.next_song()
        
        self.add(self.hud, z=-1)


        self.do(Delay(3) +CallFunc(self.dispatch_event,'on_game_start') )
        
        game_audio.play_song('music_background1.ogg')
        
        
        print jogadores[0].sock
        
        if jogadores == []:
            print "Jogadores veio vazio!"
        else:
            print "tamanho jogadores:"
            print len(jogadores)
            for i in jogadores:
                print i
                print i.nome
                print i.sock
                i.envia_comando("Bem Vindo ao Jogo!!")
        
        
        print "Vai começar a recepção:"
        while True:
            msg = jogadores[0].recebe_comando()
            
            if msg == "sair":
                break
            else:
                print msg
                jogadores[1].envia_comando(msg)

        """
        
        print "Vai começar a recepção:"
        """
        
        """
        while True:
            msg = self.jogador_sock.recv(1024)
            if msg == "sair":
                break
            else:
                print msg
                self.jogadores[1].envia_comando(msg)
                
        
        
        """
        #for j in self.jogadores:
        #    j.desconecta()
        
        
        
    def teste_thread(self, tempo, vez):
        time.sleep(tempo)
        self.hud.informaJogador("Teste Jogador 1234", vez)
        self.jogadores.append(tempo)
        
        



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
        
    def on_quit(self):
        # called by esc
        director.scene.end()
        director.scene.end()
        

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

