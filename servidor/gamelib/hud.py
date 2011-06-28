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
        self.larguraTela =  jogo.larguraTela
        self.alturaTela = jogo.alturaTela
        self.alturaCarta= jogo.alturaCarta
        self.larguraCarta= jogo.larguraCarta
        
        #self.game.push_handlers(self.on_gamer_connect, self.on_server_status)#self.on_game_over,  self.on_xp_gain,  self.on_game_win,  self.on_game_start , self.on_complete_level)
        
        #self.add(BGLayer("TEMP_HUD"))

        self.jogador1 = Label("Partida Iniciada", font_name='Times New Roman',
            font_size=23,
            x=30, y=560,
            anchor_x='left', anchor_y='top')

        self.jogador1 = Label("Jogador 1: ", font_name='Times New Roman',
            font_size=23,
            x=30, y=560,
            anchor_x='left', anchor_y='top')


        self.jogador2 = Label("Jogador 2: ", font_name='Times New Roman',
            font_size=23,
            x=30, y=530,
            anchor_x='left', anchor_y='top')

        self.jogador3 = Label("Jogador 3: ", font_name='Times New Roman',
            font_size=23,
            x=30, y=500,
            anchor_x='left', anchor_y='top')

        self.jogador4 = Label("Jogador 4: ", font_name='Times New Roman',
            font_size=23,
            x=30, y=470,
            anchor_x='left', anchor_y='top')

        self.qtdJogadores = Label("Numero de Jogadores conectados: 0", font_name='Times New Roman',
            font_size=30,
            x=200, y=340,
            anchor_x='left', anchor_y='top')


        cocos.actions.FadeOut(0)


        #self.add(self.desenhaJogadores(1,"Wander"))
        #self.add(self.desenhaJogadores(2,"Marluce"))
        #self.add(self.desenhaJogadores(3,"Luana"))
        #self.add(self.desenhaJogadores(4,"Ataide"))



    def desenhaJogadores(self, numero, equipe, nome):
        
        if equipe == 1:
            pos1 = (self.larguraTela/2)
            ancora_x = 'center'
            if numero == 1:
                pos2 = self.alturaTela
                ancora_y = 'top'
            elif numero == 2:
                pos2 = self.alturaCarta + 55
                ancora_y = 'bottom'
        elif equipe == 2:
            pos2 = self.alturaTela/2+self.alturaCarta/2
            ancora_y = 'bottom'
            if numero == 1:
                pos1 = self.larguraTela
                ancora_x = 'right'
            elif numero == 2:
                pos1 = 0
                ancora_x = 'left'
                
        
              
        jogador = Label("Jogador: %s" % nome, font_name='Times New Roman',
        font_size=23,
        x=pos1, y=pos2,
        anchor_x=ancora_x, anchor_y=ancora_y)
        
        self.add(jogador)

    def update_jogador(self, jogador, posicao):
        if posicao == 0:
            self.jogador1.element.color = (0,0,255,255)
            self.jogador1.element.text = "Jogador 1: %s Conectado!" % jogador
        elif posicao == 1:
            self.jogador2.element.color = (0,255,0,255)
            self.jogador2.element.text = "Jogador 2: %s Conectado!" % jogador
        elif posicao == 2:
            self.jogador3.element.color = (0,0,255,255)
            self.jogador3.element.text = "Jogador 3: %s Conectado!" % jogador
        elif posicao == 3:
            self.jogador4.element.color = (0,255,0,255)
            self.jogador4.element.text = "Jogador 4: %s Conectado!" % jogador


    def informaQtdJogador(self, qtde):
        self.schedule(lambda qtJog:self.update_QtdJogador(qtde))


    def update_QtdJogador(self, qtde):
        self.qtdJogadores.element.text = "Numero de Jogadores conectados: %s" % qtde

    
    def posicionaJogadores(self, posicao, nomeJogador):
        self.schedule(lambda posJog:self.desenhaJogadores(posicao, nomeJogador))
    

    def informaJogador(self, nomeJogador, posicao):
        self.schedule(lambda upJog:self.update_jogador(nomeJogador,posicao))


    def update_figura(self):
        self.sprite = cocos.sprite.Sprite('imagens/3-Espadas.gif')
        self.sprite.position = 320,240
        self.add(self.sprite)

    def mostraDessenhoTeste(self):
        self.schedule(lambda upJog:self.update_figura())

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
    
    def on_xp_gain(self):
        log.info("on_xp_gain")
        self.exp.element.text = "Exp: %d" % self.game.player.exp
            
    def on_game_start(self):
        print "teste do start hehehe"
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
