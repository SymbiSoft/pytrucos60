#-*- coding: utf-8 -*-
'''
Created on Fev 24, 2011

@author: Wander Jardim
'''
import logging
log = logging.getLogger('hud')
log.debug("imported")
import time
import cocos
from cocos.text import Label
from cocos.actions import *
from bg_layer import BGLayer
from cocos.director import director
import game_audio

class Hud(cocos.layer.Layer):
    #is_event_handler = False
    def __init__(self, jogo):
        super(Hud, self).__init__()

        self.game = jogo
        #self.game.push_handlers(self.on_gamer_connect, self.on_server_status)#self.on_game_over,  self.on_xp_gain,  self.on_game_win,  self.on_game_start , self.on_complete_level)
        
        #self.add(BGLayer("TEMP_HUD"))

        self.timer = Label("Time: 0.0 s", font_name='Forte',
            font_size=16, color=(75,135,73,255),
            x=700, y=600)

        self.jogadoresConctados=[]
        posY=500
        for jogador in range(4):
            indiceJog = jogador+1
            self.jogadoresConctados.append(Label("Jogador %s: "%indiceJog, font_name='Forte',
            font_size=40, color=(75,135,73,255),
            x=120, y=posY,
            anchor_x='left', anchor_y='top'))
            posY -=50 
            
        cocos.actions.FadeOut(0)
        for LabJogador in self.jogadoresConctados:
            self.add(LabJogador)
        
            
        self.add(self.timer)
        self.start_time = time.time()
        self.clock = time.time()
        self.schedule(self.update_time)
        
        
        
    def update_time(self, dt=0):
        self.clock = time.time()
        self.timer.element.text = "Tempo: %0.1f s" % (self.clock-self.start_time)

    def update_jogador(self, jogador, posicao):
        if posicao == 0:
            self.jogadoresConctados[0].element.color = (0,0,255,255)
            self.jogadoresConctados[0].element.text = "Jogador 1: %s Conectado!" % jogador
        elif posicao == 1:
            self.jogadoresConctados[1].element.color = (0,255,0,255)
            self.jogadoresConctados[1].element.text = "Jogador 2: %s Conectado!" % jogador
        elif posicao == 2:
            self.jogadoresConctados[2].element.color = (0,0,255,255)
            self.jogadoresConctados[2].element.text = "Jogador 3: %s Conectado!" % jogador
        elif posicao == 3:
            self.jogadoresConctados[3].element.color = (0,255,0,255)
            self.jogadoresConctados[3].element.text = "Jogador 4: %s Conectado!" % jogador



    def informaJogador(self, nomeJogador, posicao):
        self.schedule(lambda upJog:self.update_jogador(nomeJogador,posicao))


    def desconectaJogador(self, nomeJogador):
        self.schedule(lambda upJog:self.on_game_over(nomeJogador))


    def on_gamer_connect(self, nomeJogador):
        jogador = Label("O Jogador %s se conectou ao servidor" % nomeJogador, font_name='Times New Roman',
            font_size=25,
            anchor_x='center', anchor_y='center')
        self.add(jogador)

    def on_server_status(self):
        LabStatus = Label(u"Status da conexao: ", font_name='Times New Roman',
            font_size=25,
            anchor_x='center', anchor_y='center')
        self.add(LabStatus)

    def on_complete_level(self):
        self.on_good_condition("Level Complete")
        
    def on_game_over(self, nomeJogador):
        x,y = director.get_window_size()
        loose = Label("Jogador %s desconectado!!" % nomeJogador, font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')
        self.add(loose)
        loose.do(MoveTo((x/3,y/2), 3) | ScaleBy( 2, 3 ) )
            
    def on_game_start(self):
        self.do(FadeIn(2))
        self.on_xp_gain()
        self.start_time = time.time()
        self.clock = self.start_time
        
    def on_game_win(self):
        self.on_good_condition("You Winnar")
        
    def on_good_condition(self, message):
        self.unschedule(self.update_time)
        game_audio.play_song('music_victory.ogg')
        x,y = director.get_window_size()
        self.timer.do(MoveTo((x/3,y/2), 3)  )
        loose = Label(message, font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')
        self.add(loose)
        loose.do(MoveTo((x/3,y/3), 3) )
