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


from hud import Hud
import game_audio
from bg_layer import BGLayer
from logicaTruco import *





class Jogo(cocos.layer.Layer, EventDispatcher): # must be layer - scene causes anims/actions to fail
    def __init__(self, jogadores):
        super(Jogo, self).__init__()
        self.nrJogadores=0
        self.partidaIniciada = False
        self.rodadaIniciada = False
        self.jogadores = jogadores
        self.larguraTela, self.alturaTela = director.get_window_size()
        
        self.baralho = Baralho()
        
        cartaModelo = self.baralho.cartas[0]
        rectSprites = cartaModelo.imagem.get_rect()
        self.alturaCarta=rectSprites.height
        self.larguraCarta=rectSprites.width
        
        # Configurando camadas
        # HUD
        self.hud = Hud(self)
        #game_audio.next_song()
        self.add(self.hud, z=-1)
        #self.hud = None
        #self.do(Delay(3) +CallFunc(self.dispatch_event,'on_game_start') )
        #game_audio.play_song('music_background1.ogg')
        
        
        
        self.mesa = Mesa(self.jogadores, self.baralho)
        for jogador in self.jogadores:
            jogador.envia_comando("iniciaPartida")
        
        for jogador in self.jogadores:
            jogador.recebe_comando()
            
        self.cont = 0
        #self.schedule(self.iniciaPartida) 
        self.iniciaPartida()
        
        threadLoopJogo = Thread( target=self.loop_jogo)
        threadLoopJogo.start()

    
       
    def iniciaPartida(self): #, dt):
        

        if not self.partidaIniciada:
            self.baralho.embaralhar()
            self.mesa.definirEquipes()
            self.mesa.definirOrdemJogadores()
        
            for equipe in self.mesa.equipes:
                print "Equipe: %s - Jogador: %s" % (equipe, equipe.jogadores[0].nome)
                equipe.jogadores[0].setNumero(1)
                print "Número: %s - Num. Equipe: %s" % (equipe.jogadores[0].getNumero(),equipe.jogadores[0].getEquipe())
                
            for equipe in self.mesa.equipes:
                print "Equipe: %s - Jogador: %s" % (equipe, equipe.jogadores[1].nome)
                equipe.jogadores[1].setNumero(2)
                print "Número: %s - Num. Equipe: %s" % (equipe.jogadores[1].getNumero(),equipe.jogadores[1].getEquipe())
            self.partidaIniciada = True
            
            self.hud.desenhaJogadores(jogador.getNumero(), jogador.getEquipe(), jogador.nome)
    
    def iniciaMao(self):
        self.placarMao = (0,0)
        
        for equipe in mesa.equipes:
            equipe.pontosMao = 0
            
        mesa.baralho.embaralhar()
        self.mesa.distrubuirCartas()
        
        #Feito somente para testes retirar após o dicionário de posições estiver completo e descomentar a linha acima.
        cartaBT = ['3e', '2e', 'ac']
        cartas_enviadas = "cartas:" + "/".join(cartaBT)

        for jogador in self.jogadores:
            self.desenhaCartasJogadores(jogador)
            jogador.envia_comando(cartas_enviadas)

        while max(self.placarMao) < 2:
            self.jogarRodada()
            

    def jogarRodada(self):
        
        self.mesa.definirOrdemJogadores()
        for ordem in range(len(self.jogadores)):
            self.jogadores[ordem].vezDeJogar = True
            
            for jogador in self.jogadores:
                if jogador.vezDeJogar:
                    jogadorDaVez = jogador
                    jogador.envia_comando("Sua Vez!")
                    
            for jogador in self.jogadores:
                if not jogador.vezDeJogar:
                    jogador.envia_comando("vez de %s jogar" % jogadorDaVez.nome)
            
            
            cmd = jogadorDaVez.recebe_comando()
            if cmd == 'truco':
                for jogador in self.jogadores:
                    if not jogador.vezDeJogar:
                        jogador.envia_comando("jogador %s pediu truco" % jogadorDaVez.nome)
                    
                        
            
            
            
            self.mesa.cartas.append()
        
        indiceJogadorGanhador = self.mesa.compararCartas(self.mesa.cartas)
        jogadorGanhador = self.jogadores[indiceJogadorGanhador]
        
        equipeGanhadora = jogadorGanhador.getEquipe()
        
        self.mesa.equipes[equipeGanhadora-1].pontosMao += 1
            
            
            
                
            
                    
                
            
            
            
                
    
    
    
    def iniciaRodada(self):
        print "passei por aqui %s vezes!" % self.cont
        self.cont +=1
        
        
        if not self.rodadaIniciada:
        
            
            
            #jogador.envia_comando(jogador.formata_cartas_BT())
            
            
            
            for jogador in self.jogadores:
                jogador.envia_comando(cartas_enviadas)
        
            #print jogador.recebe_comando()
            self.rodadaIniciada = True
        
        
       
       
    def desenhaCartasJogadores(self, jogador):
        print "Jogador - %s:" % jogador.nome
        print "Número: %s Equipe: %s" % (jogador.getNumero(), jogador.getEquipe())
        
        self.alturaTela 
        self.larguraTela
        
        self.alturaCarta
        self.larguraCarta
        
        
        if jogador.getEquipe() == 1:
            pos1 = (self.larguraTela/2) - self.larguraCarta
            if jogador.getNumero() == 1:
                pos2 = self.alturaTela-100
            elif jogador.getNumero() == 2:
                pos2 = self.alturaCarta/2 + 50
        elif jogador.getEquipe() == 2:
            pos2 = self.alturaTela/2
            if jogador.getNumero() == 1:
                pos1 = self.larguraTela - (5*self.larguraCarta)/2
            elif jogador.getNumero() == 2:
                pos1 = self.larguraCarta/2
                
        for carta in jogador.mao:        
            print "Carta: %s - Posicao: (%s,%s)" % (carta, pos1, pos2)
            
            carta.imagem.position = pos1, pos2
            self.add(carta.imagem, z=1 )
            pos1 += self.larguraCarta + 2
       
       
    def animaDistribuirCartas(self, jogador):
       pass
       

       
       
    def desenhaMesaJogo(self):
       pass




    def loop_jogo(self):
        
        for jogador in self.jogadores:
           
        
        
        
        
        if self.partidaIniciada:
            self.iniciaRodada()
            
        #while not self.fimPartida:
        #    cmd = jogador.recebe_comando()


    def aguarda_comando(self, jogador):
        i = 0
        print "Jogador [%s] diga alguma coisa: " % jogador.nome
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
        


Jogo.register_event_type('on_game_start')   
Jogo.register_event_type('on_xp_gain')   
Jogo.register_event_type('on_game_over')
Jogo.register_event_type('on_gamer_connect')
Jogo.register_event_type('on_server_status')




class ComandosJogador(threading.Thread):
    def __init__ (self, jogador):
        threading.Thread.__init__(self)
        self.jogador = jogador
        
    def run(self):
        self.jogador.estahRodando = True
        print self.jogador.recebe_comando()


def run(jogadores): 
    s = cocos.scene.Scene()
    jogo =  Jogo(jogadores)
    s.add( jogo, z=1, name='ctrl')
    s.add(BGLayer("mesa"))
    #hud = Hud(jogo)
    #s.add( hud, z=10, name='hud' )
    #jogo.hud = hud

    return s





if __name__ == '__main__':

    director.init(width=640, height=480, do_not_scale=True)    
    director.run(run())
    