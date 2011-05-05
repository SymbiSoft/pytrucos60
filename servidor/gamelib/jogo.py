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
from conexao import Conexao
from jogador import Jogador

import threading
from threading import Thread
from hud import Hud

import game_audio



class Jogo(cocos.layer.Layer, EventDispatcher): # must be layer - scene causes anims/actions to fail
    eh_manipuador_eventos = True # for actions to work

    def __init__(self, tipo_conexao):
        super(Jogo, self).__init__()
        self.nrJogadores=0
        self.tipo_conexao = tipo_conexao
        self.partidaIniciada = False

        print "tipo de conexao => %s " % tipo_conexao


        # Configurando camadas
        # HUD
        self.hud = Hud(self)

        game_audio.next_song()
        
        self.add(self.hud, z=-1)


        self.do(Delay(3) +CallFunc(self.dispatch_event,'on_game_start') )

        """
        self.jogadores = []
        if self.tipo_conexao == 'bluetooth':
            conexao = Conexao()
            socket = conexao.socket_servidor()
        else:
            socket = None
        self.nrJogador=0



        while not self.partidaIniciada:
            print "Rodei pela %sa. vez" % self.nrJogadores
            self.jogador_sock, self.jogador_info = conexao.conectaJogador(socket)
            print "Jogador %s Conectado: %s - %s" % (self.nrJogador, self.jogador_sock, self.jogador_info)
            self.hud.informaJogador(self.jogador_info, self.nrJogador)
            self.jogadores.append(Jogador(self.jogador_sock, self.jogador_info))
            self.jogadores[self.nrJogador].setDaemon(True)
            self.jogadores[self.nrJogador].start()
            self.nrJogador+=1
            if len(self.jogadores)>=3:
                self.partidaIniciada = True
        
        self.nrJogadores = len(self.jogadores)
        """

            
            

        
        #print "eh agora: %s " % conexao.status 
        
        #self.hud.on_server_status(conexao.status)
        #print "eh agora2: %s " % conexao.status
        #if conexao.status == u'Fechado':
        #    inicioPartida == True


        #self.add(self.conexao, z=-2)
        

        #self.do(Delay(3) +CallFunc(self.dispatch_event,'on_server_status') )
        

        
        #self.push_handlers(self.on_save_point, self.on_player_die, self.on_complete_level)
        
        game_audio.play_song('music_background1.ogg')


    def partidaIniciadaTemp(self):
        return True

Jogo.register_event_type('on_game_start')   
Jogo.register_event_type('on_xp_gain')   
Jogo.register_event_type('on_game_over')
Jogo.register_event_type('on_gamer_connect')
Jogo.register_event_type('on_server_status')


def run(tipo_conexao):

    
    return Jogo(tipo_conexao)

if __name__ == '__main__':



    director.init(width=640, height=480, do_not_scale=True)    
    director.run(run())

