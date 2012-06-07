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
from cocos.text import Label, RichLabel
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
        
        self.__dir_imagens = "data/imagens/"
        
        
        self.balaoFala = cocos.sprite.Sprite(self.__dir_imagens + "balaoFala01.png")
        self.fala = cocos.sprite.Sprite(self.__dir_imagens + "mouse.png", (0, 2) )
        self.balaoFala2 = cocos.sprite.Sprite(self.__dir_imagens + "balaoFala02.png")
        
        #self.game.push_handlers(self.on_gamer_connect, self.on_server_status)#self.on_game_over,  self.on_xp_gain,  self.on_game_win,  self.on_game_start , self.on_complete_level)
        
        #self.add(BGLayer("TEMP_HUD"))

        self.placar1 = Label("", font_name='Segoe Print',
            font_size=35, bold=False,
            x=76, y=self.alturaTela-105,
            anchor_x='center', anchor_y='center', color=(0,0,0,255))
        
        self.placar2 = Label("", font_name='Segoe Print',
            font_size=35, bold=False,
            x=162, y=self.alturaTela-105,
            anchor_x='center', anchor_y='center', color=(0,0,0,255))

        self.pontosMao = Label("", font_name='Segoe Print',
            font_size=40, bold=False,
            x=885, y=self.alturaTela-73,
            anchor_x='center', anchor_y='center', color=(0,0,0,255))


        self.parabens = Label("", font_name='Segoe Print',
                                  font_size=20, anchor_x='center', anchor_y='center', color = (0,255,255,255))


        self.add(self.placar1)
        self.add(self.placar2)
        #self.add(self.parabens, z=21)
        
        self.balaoFala2.position = (-1000,-1000)
        self.balaoFala2.add(self.parabens)
        self.add(self.balaoFala2, z=20)
        
        self.add(self.pontosMao)
        
        
        cocos.actions.FadeOut(0)


    def desenhaJogadores(self, numero, equipe, nome):
        angulo = 0
        if equipe == 1:
            pos1 = (self.larguraTela/2)
            if numero == 1:
                pos2 = self.alturaTela - 205
            elif numero == 2:
                pos2 = self.alturaTela - 615
        elif equipe == 2:
            if numero == 2:
                pos1 = self.alturaTela/2 - 35
                pos2 = -(self.larguraTela - self.alturaCarta - 50)
                angulo = -90
            elif numero == 1:
                pos1 = -self.alturaTela/2 + 35
                pos2 = self.alturaCarta + 50
                angulo = 90

        jogador = Label("%s" % (nome), font_name='Segoe Print',
        font_size=25,
        x=pos1, y=pos2,
        anchor_x='center', anchor_y='center')
        
        jogador.rotation=angulo
        
        self.add(jogador)


    def desenhaPlacar(self, jogadores):
        
        for jogador in jogadores:
            print "Equipe:"
            print jogador.getEquipe()
            print type(jogador.getEquipe())
            
            print "Numero:"
            print jogador.getNumero()
            print type(jogador.getNumero())
            if jogador.getEquipe() == 1:
                if jogador.getNumero() == 1:
                    jogador1 = jogador.nome.replace(' ', '_')
                elif jogador.getNumero() == 2:
                    jogador2 = jogador.nome.replace(' ', '_')
            elif jogador.getEquipe() == 2:
                if jogador.getNumero() == 1:
                    jogador3 = jogador.nome.replace(' ', '_')
                elif jogador.getNumero() == 2:
                    jogador4 = jogador.nome.replace(' ', '_')
        
        
        equipe1j1 = Label("%s" % jogador1, font_name='Segoe Print',
        font_size=14, x=40, y=self.alturaTela-45,
        anchor_x='left', anchor_y='top', color=(0,0,0,255), width=15)
        
        equipe1j2 = Label("%s" % jogador2, font_name='Segoe Print',
        font_size=14, x=40, y=self.alturaTela-65,
        anchor_x='left', anchor_y='top', color=(0,0,0,255), width=15)
        
        equipe2j3 = Label("%s" % jogador3, font_name='Segoe Print',
        font_size=14,
        x=130, y=self.alturaTela-45,
        anchor_x='left', anchor_y='top', color=(0,0,0,255), width=15)
        
        equipe2j4 = Label("%s" % jogador4, font_name='Segoe Print',
        font_size=14,
        x=130, y=self.alturaTela-65,
        anchor_x='left', anchor_y='top', color=(0,0,0,255), width=15)
        
        self.add(equipe1j1)
        self.add(equipe1j2)
        self.add(equipe2j3)
        self.add(equipe2j4)
        




    def removeBalaoBera(self):
        self.balaoFala.position = (9999, 9999)
        self.fala.position = (9999, 9999)


    def mostraBalaoBera(self, jogador, comando='truco'):

        if self.balaoFala.position != (0, 0):
            self.remove(self.balaoFala)
        
        equipe = jogador.getEquipe()
        numero = jogador.getNumero()
        
        
        if equipe == 1:
            pos1 = (self.larguraTela/2) #- (self.larguraCarta + self.larguraCarta/2)
            if numero == 1:
                pos2 = self.alturaTela - self.alturaCarta - 77
                angulo = 180
            elif numero == 2:
                pos2 = self.alturaCarta + 110
                angulo = 0
        elif equipe == 2:
            pos2 = self.alturaTela/2 #+self.alturaCarta/2
            if numero == 2:
                pos1 = self.larguraTela - (3 * self.larguraCarta) - 23
                angulo = 270
            elif numero == 1:
                pos1 = 3 * self.larguraCarta + 30
                angulo = 90
        
        
        if comando == 'truco':
            self.fala = cocos.sprite.Sprite(self.__dir_imagens + "mouse.png", (0, 2) )
        elif comando == 'seis':
            self.fala = cocos.sprite.Sprite(self.__dir_imagens + "FalaTruco.png", (0, 2))
        elif comando == 'nove':
            self.fala = cocos.sprite.Sprite(self.__dir_imagens + "FalaTruco.png", (0, 2))
        elif comando == 'doze':
            self.fala = cocos.sprite.Sprite(self.__dir_imagens + "FalaTruco.png", (0, 2))
        
        
              
        self.balaoFala.position = pos1, pos2
        self.balaoFala.rotation = angulo
        
        self.fala.position = pos1, pos2
        self.fala.rotation = angulo
        
        #self.balaoFala.add(self.fala, z=1)
        
        self.add(self.balaoFala, z=8)
        self.add(self.fala, z=9)

    
    
    def mostraBalaoSimTruco(self, jogador):
        if self.balaoFala.position != (0, 0):
            self.remove(self.balaoFala)
        
        equipe = jogador.getEquipe()
        numero = jogador.getNumero()
        
        
        if equipe == 1:
            pos1 = (self.larguraTela/2) #- (self.larguraCarta + self.larguraCarta/2)
            if numero == 1:
                pos2 = self.alturaTela - self.alturaCarta - 77
                angulo = 180
            elif numero == 2:
                pos2 = self.alturaCarta + 110
                angulo = 0
        elif equipe == 2:
            pos2 = self.alturaTela/2 #+self.alturaCarta/2
            if numero == 2:
                pos1 = self.larguraTela - (3 * self.larguraCarta) - 23
                angulo = 270
            elif numero == 1:
                pos1 = 3 * self.larguraCarta + 30
                angulo = 90
        
        
        self.fala = Label("DESCE SAFAAADOO!!", font_name='Times New Roman',
            font_size=25,
            x=0, y=0,
            anchor_x='left', anchor_y='top', color = (0,255,255,255))
        
        
        
        self.balaoFala.position = pos1, pos2
        self.balaoFala.rotation = angulo
        
        self.fala.rotation = angulo
        
        self.add(self.balaoFala)
        self.add(self.fala)  


    def removeInformaGanhadorMao(self):
        #self.remove(self.balaoFala2)
        self.schedule(lambda plca:self.atualizaRemoveInformaGanhadorMao())

    def atualizaRemoveInformaGanhadorMao(self):
        
        self.balaoFala2.position = (-10000,-10000)
        #self.parabens.position = (-10000,-10000)
        #self.remove(self.balaoFala2)


    def informaGanhadorMao(self, equipe):
        self.schedule(lambda plca:self.atualizaInformaGanhadorMao(equipe))
        
        


    def atualizaInformaGanhadorMao(self, equipe):
        self.balaoFala2.position = self.larguraTela/2, self.alturaTela/2
        #self.parabens.position = self.larguraTela/2, self.alturaTela/2
    
        jogadores = equipe.nomeJogadores()
        self.parabens.element.text = "A equipe %s e %s ganharam essa mao"%(jogadores[0], jogadores[1])
        



    def removeBalaoSim(self):
        self.balaoFala.position = (9999, 9999)



    def atualizaPlacar(self, placar):
        self.placar1.element.text = "%s" % placar[0]
        self.placar2.element.text = "%s" % placar[1]
        
    def mostraPlacar(self, placar):
        self.schedule(lambda plca:self.atualizaPlacar(placar))



    def atualizaPontoMao(self, pontos):
        self.pontosMao.element.text = "%s" % pontos

    def mostraPontoMao(self, pontos):
        self.schedule(lambda plca:self.atualizaPontoMao(pontos))
    
    def updateVezJogador(self):
        pass
    
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
