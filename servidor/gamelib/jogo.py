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
from cocos.scene import Scene
from cocos.scenes.transitions import *

from pyglet.event import EventDispatcher
import pyglet

import threading
from threading import Thread, Timer
import time


from hud import Hud
import game_audio
from bg_layer import BGLayer
from logicaTruco import *
import game_over




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
        
        self.__dir_imagens = "data/imagens/"
        self.balaoFala = cocos.sprite.Sprite(self.__dir_imagens + "balaoFala01.png")
        
        self.setaVezJogador = cocos.sprite.Sprite(self.__dir_imagens + "seta.png")
        
        self.falaTruco = cocos.sprite.Sprite(self.__dir_imagens + "FalaTruco.png", (0, 2))
        self.falaSeis = cocos.sprite.Sprite(self.__dir_imagens + "FalaSeis.png", (0, 2))
        self.falaNove = cocos.sprite.Sprite(self.__dir_imagens + "FalaNove.png", (0, 2))
        self.falaDoze = cocos.sprite.Sprite(self.__dir_imagens + "FalaDoze.png", (0, 2))
        self.falaDesce = cocos.sprite.Sprite(self.__dir_imagens + "FalaDesce.png", (0, 2))        
        self.falaCorro = cocos.sprite.Sprite(self.__dir_imagens + "FalaCorro.png", (0, 2))  
        
        
        # Configurando camadas
        # HUD
        self.hud = Hud(self)
        #game_audio.next_song()
        self.add(self.hud, z=-1)
        #self.hud = None
        #self.do(Delay(3) +CallFunc(self.dispatch_event,'on_game_start') )
        #game_audio.play_song('music_background1.ogg')
        
        
        
        self.mesa = Mesa(self.jogadores, self.baralho)
        for jogador in self.mesa.jogadores:
            jogador.envia_comando("iniciaPartida")
        
        for jogador in self.mesa.jogadores:
            jogador.recebe_comando()
            
        self.cont = 0

        #self.schedule(self.iniciaPartida) 
        
        self.iniciaPartida()
        
        
        threadLoopJogo = Thread( target=self.loop_jogo)
        threadLoopJogo.start()



    def loop_jogo(self):
        
        while max(self.placarPartida) < 1: #Voltar para 12 assim q terminar os testes
            
            self.novaMao = True
            self.iniciaMao()
            
            print "#########################################"
            print "########### PLACAR DA PARTIDA ###########"
            print self.placarPartida
            #print "%s - %s X %s - %s" % (self.mesa.equipes[0], self.mesa.equipes[0].pontos, self.mesa.equipes[1].pontos, self.mesa.equipes[1])
            print "#########################################"
            self.hud.mostraPlacar(self.placarPartida)
            
        
        menu_game_over = Scene(game_over.get_janela())
        director.push( FadeTransition(menu_game_over, 1.0 ) )
        #director.replace(FadeTransition( s, 1 ) )

    
    
    
            
    def iniciaPartida(self): #, dt):
        
        self.placarPartida = (0,0)
        
        
        if not self.partidaIniciada:
            self.baralho.embaralhar()
            self.mesa.definirEquipes()
            self.mesa.definir1aOrdemJogadores()
                
                
            for equipe in self.mesa.equipes:
                #print "Equipe: %s - Jogador: %s" % (equipe, equipe.jogadores[0].nome)
                equipe.jogadores[0].setNumero(1)
                #print "Número: %s - Num. Equipe: %s" % (equipe.jogadores[0].getNumero(),equipe.jogadores[0].getEquipe())
                
            for equipe in self.mesa.equipes:
                #print "Equipe: %s - Jogador: %s" % (equipe, equipe.jogadores[1].nome)
                equipe.jogadores[1].setNumero(2)
                #print "Número: %s - Num. Equipe: %s" % (equipe.jogadores[1].getNumero(),equipe.jogadores[1].getEquipe())
                
            for jogador in self.mesa.jogadores:
                self.hud.desenhaJogadores(jogador.getNumero(), jogador.getEquipe(), jogador.nome)
                
        
            for jogador in self.mesa.jogadores:
                respInformaEquipes = ''
                if jogador in self.mesa.equipes[0].jogadores:
                    jogador.envia_comandoJS({'equipes':[self.mesa.equipes[0].nomeJogadores(), self.mesa.equipes[1].nomeJogadores()]},statusMao=0)
                if jogador in self.mesa.equipes[1].jogadores:
                    jogador.envia_comandoJS({'equipes':[self.mesa.equipes[1].nomeJogadores(), self.mesa.equipes[0].nomeJogadores()]},statusMao=0)
                                             
                respInformaEquipes = jogador.recebe_comando()
                
                #por se tratar de uma thread foi necessario esse loop para esperar a resposta do jogador
                while not respInformaEquipes:
                    pass
                    
                print respInformaEquipes
        
        
                
            self.hud.desenhaPlacar(self.mesa.jogadores)    
            self.mesa.jogadores[-1].iniciouUltimaPartida = True
            self.partidaIniciada = True
            
            
    
    def iniciaMao(self):
        self.placarMao = (0,0)
        if max(self.placarPartida) == 11:
            self.valorMao = 3
        else:
            self.valorMao = 1
            
        self.statusMao = 0 #0-Normal, 1-Trucada, 2-Seis, 3-Nove, 4-Doze
        
        for equipe in self.mesa.equipes:
            equipe.pontosMao = 0
            
        self.baralho.embaralhar()
        self.mesa.defineManilhas(self.baralho)
        print "Vira: %s" % self.mesa.vira
        print "Manilhas: %s" % self.mesa.manilhas
        for manilha in self.mesa.manilhas:
            print manilha.nomeCartaPadrao
        
        
        self.desenhaCartaVira()
        self.mesa.distrubuirCartas()

        for jogador in self.mesa.jogadores:
            respJogador = {}
            self.animaDistribuirCartas(jogador)
            jogador.envia_comandoJS(jogador.maoJS(), self.statusMao)
            time.sleep(1)
            while 'OK' not in respJogador:
                respJogador = jogador.recebe_comandoJS()
                while not respJogador:
                    pass
        for jogador in self.mesa.jogadores:
            self.desenhaCartasJogadores(jogador)
        
        self.jogadorIncrementador = None    
        self.jogadorTrucador = None
        self.jogadorMeioPauador = None
        self.jogadorNoveador = None
        self.jogadorDozeador = None

        status = ''
        while max(self.placarMao) < 2 :#or status != 'fim':
            self.mesa.definirOrdemJogadores(self.novaMao)
            #status = 
            self.jogarRodada()
            print "########################################"
            print "########### PLACAR DA RODADA ###########"
            print self.placarMao
            #print "%s - %s X %s - %s" % (self.mesa.equipes[0], self.mesa.equipes[0].pontosMao, self.mesa.equipes[1].pontosMao, self.mesa.equipes[1])
            print "########################################"
            
            self.novaMao = False
            
        
        for equipe in self.mesa.equipes:
            if equipe.pontosMao >= 2:
               equipe.pontos += self.valorMao
               equipeGanhadora = equipe
        
        self.placarPartida = (self.mesa.equipes[0].pontos, self.mesa.equipes[1].pontos)
        self.hud.informaGanhadorMao(equipeGanhadora)
        self.informaFimMao(equipeGanhadora)
        self.hud.removeInformaGanhadorMao()
        
        
        
        self.baralho.recolherCartas(self.mesa.jogadores)
        
        for jogador in self.mesa.jogadores:
            for carta in jogador.mao:
                self.remove(carta.imagem)
        
        self.remove(self.mesa.vira.imagem)
        self.remove(self.baralho.imagem)
        self.mesa.zeraManilhas(self.baralho)
        self.equipeGanhadora1aRodada = None
        
        
            

    def informaFimMao(self, equipe):
        print "Vou informar do fim da Mão!"
        for jogador in self.mesa.jogadores:
            respFimMao = {}
            if equipe.ehDaEquipe(jogador):
                jogador.envia_comandoJS({'fim-mao':['ganhou', equipe.pontos]}, self.statusMao)
            else:
                jogador.envia_comandoJS({'fim-mao':['perdeu', equipe.pontos]}, self.statusMao)
            #while 'OK' not in respFimMao:
            respFimMao = jogador.recebe_comandoJS()
            while not respFimMao:
                pass
            

    def pedeIncremento1(self, incremento, jogadorIncrementador):
        for jogador in self.mesa.jogadores:
            resp = ''
            if not jogador.vezDeJogar:
                jogador.envia_comandoJS({incremento:":%s" %jogadorIncrementador.nome}, self.statusMao)
                resp = jogador.recebe_comandoJS()
                while not resp:
                    pass
                print resp
        respIncrem = ''
        self.mesa.jogadores[self.proximoJogador].envia_comandoJS({incremento:'aceita?'}, self.statusMao)
        respIncrem = self.mesa.jogadores[self.proximoJogador].recebe_comando()
        #por se tratar de uma thread foi necessario esse loop para esperar a resposta do jogador
        while not respIncrem:
            pass

        return respIncrem
        

    def pedeIncremento2(self, incremento, jogadorIncrementador):
        for jogador in self.mesa.jogadores:
            resp = ''
            jogador.envia_comandoJS({incremento:":%s" %jogadorIncrementador.nome}, self.statusMao)
            resp = jogador.recebe_comandoJS()
            while not resp:
                pass
            print resp

        respIncrem = ''
        self.jogadorDaVez.envia_comandoJS({incremento:'aceita?'}, self.statusMao)
        respIncrem = self.jogadorDaVez.recebe_comando()
        
        #por se tratar de uma thread foi necessario esse loop para esperar a resposta do jogador
        while not respIncrem:
            pass
            
        return respIncrem
        


    def pedeIncremento3(self, incremento, jogadorIncrementador):
        for jogador in self.mesa.jogadores:
            resp = ''
            jogador.envia_comandoJS({incremento:":%s" %jogadorIncrementador.nome}, self.statusMao)
            resp = jogador.recebe_comandoJS()
            while not resp:
                pass
            print resp

        respIncrem = ''
        
        self.mesa.jogadores[self.proximoJogador].envia_comandoJS({incremento:'aceita?'}, self.statusMao)
        respIncrem = self.mesa.jogadores[self.proximoJogador].recebe_comando()
        
        #por se tratar de uma thread foi necessario esse loop para esperar a resposta do jogador
        while not respIncrem:
            pass
            
        return respIncrem

        

    def defineOrdemJogadores(self,ordem):
        
        self.proximoJogador = ordem+1
        if self.proximoJogador>len(self.mesa.jogadores)-1:
            self.proximoJogador = 0

    def tiraVezJogar(self):
        for jogador in self.mesa.jogadores:
            if jogador.vezDeJogar:
                jogador.vezDeJogar = False



    def informaVezJogar(self, podeIncrementar): 
        cmd =''
        
        self.jogadorDaVez.envia_comandoJS({'vez':'sua'}, self.statusMao, podeIncrementar)
        print "Jogador da vez: %s" % self.jogadorDaVez.nome
        
        for jogador in self.mesa.jogadores:
            if not jogador.vezDeJogar:
                jogador.envia_comandoJS({'vez':self.jogadorDaVez.nome}, self.statusMao)

        cmd = self.jogadorDaVez.recebe_comandoJS()
        while not cmd:
           pass
        
        return cmd


    def enviaComandoTodosJogadores(self, comando, tipo):

        if tipo == 'info':
            for jogador in self.mesa.jogadores:
                respOK = ''
                jogador.envia_comandoJS(comando, self.statusMao) 
                respOK = jogador.recebe_comandoJS()
                print respOK
                #por se tratar de uma thread foi necessario esse loop para esperar a resposta do jogador
                while not respOK:
                    pass
                print respOK
                
        elif tipo == 'cmd':
            
            resp = 'lala'
            
            return resp



    def jogarRodada(self):
        
        
        trucoFugido = False
        seisFugido = False
        noveFugido = False
        dozeFugido = False
        
        print "Irá começar um ciclo de %s rodadas" % len(self.mesa.jogadores)
        
        self.tiraVezJogar()
        
        #Loop Principal do Jogo
        for ordem in range(len(self.mesa.jogadores)):
            
            print "###################"
            print "ordem da jogada: %d" % ordem
            print "###################"
            
            self.hud.mostraPontoMao(self.valorMao)
            
            self.mesa.jogadores[ordem].vezDeJogar = True
            
            
            for jogador in self.mesa.jogadores:
                if jogador.vezDeJogar:
                    self.jogadorDaVez = jogador
                    
            self.informaVezJogador(self.jogadorDaVez)
            self.defineOrdemJogadores(ordem)
            
            
            if self.jogadorIncrementador:
                podePedirIncremento = self.jogadorDaVez.getEquipe() != self.jogadorIncrementador.getEquipe() and 1 or 0
            else:
                podePedirIncremento = 1
            
            cmd = self.informaVezJogar(podePedirIncremento)
            
                                
            ###TABELA statusMao ###
            # statusMao = 0 -> Inicio de Partida, valendo 1 ponto
            # statusMao = 1 -> Partida Trucada, valendo 3 pontos
            # statusMao = 2 -> Partida em Meio-Pau, valendo 6 ponto
            # statusMao = 3 -> Partida em Nove, valendo 9 ponto
            # statusMao = 4 -> Partida em Doze, valendo 12 pontos
            
           
            if 'truco' in cmd:
                if cmd['truco'] == 'pedido':
                    
                    print "Pediu-se Trucoo!!"
                    print "Status da Mao: %s" % self.statusMao
                    
                    
                    
                    if self.statusMao == 0:
                        
                        self.jogadorTrucador = self.jogadorDaVez
                        self.jogadorIncrementador = self.jogadorTrucador
                        equipeTrucadora = self.jogadorTrucador.getEquipe()
                        #self.mostraBalao(self.jogadorTrucador)
                        
                        self.mostraBalao(self.jogadorTrucador, "truco")
                        
                        
                        respPedTruco = self.pedeIncremento1('truco', self.jogadorTrucador)
                        self.removeBalao()
                        
                        # O adversario aceitou o truco
                        if respPedTruco == 'sim':
                            cmd = ''
                            self.statusMao = 1 #Partida Trucada
                            self.valorMao = 3
                            
                            self.hud.mostraPontoMao(self.valorMao)
                            
                            self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "sim")
                            
                            self.enviaComandoTodosJogadores({'truco':'aceitou:%s' % self.mesa.jogadores[self.proximoJogador].nome},'info')
                            
                            
                            
                            cmd = self.informaVezJogar(podeIncrementar = 0)
                            self.removeBalao()
                            
                        elif respPedTruco == 'seis':
                            
                            self.statusMao = 1
                            self.valorMao = 3
                            
                            self.hud.mostraPontoMao(self.valorMao)
                            
                            self.jogadorMeioPauador = self.mesa.jogadores[self.proximoJogador]
                            self.jogadorIncrementador = self.jogadorMeioPauador
                            
                            self.mostraBalao(self.jogadorMeioPauador, "seis")
                            respPedSeis = self.pedeIncremento2('seis', self.jogadorMeioPauador)
                            self.removeBalao()
                                     
                            #Jogador aceitou o Pedido de Meis Pau - Seis  
                            if respPedSeis == 'sim':
                                cmd = ''
                                self.statusMao = 2
                                self.valorMao = 6
                                
                                self.hud.mostraPontoMao(self.valorMao)
                                
                                self.mostraBalao(self.jogadorDaVez, "sim")
                                
                                self.enviaComandoTodosJogadores({'seis':'aceitou:%s' % self.jogadorDaVez.nome},'info')
                                
                                self.removeBalao()
                                
                                cmd = self.informaVezJogar(0)
                                
                                if 'pedido' in cmd.values():
                                    print "################"
                                    print "aqui era a hora!"
                                    print "################"
                            
                            
                            
                            elif respPedSeis == 'nove':
                                
                                
                                self.statusMao = 2
                                self.valorMao = 6
                                
                                self.hud.mostraPontoMao(self.valorMao)
                                
                                self.jogadorNoveador = self.jogadorDaVez
                                self.jogadorIncrementador = self.jogadorNoveador
                                self.mostraBalao(self.jogadorNoveador, "nove")
                                respPedNove = self.pedeIncremento1('nove', self.jogadorNoveador)
                                self.removeBalao()
                                
                                #Jogador aceitou o Pedido de Meio Pau - Seis  
                                if respPedNove == 'sim':
                                    self.statusMao = 3
                                    self.valorMao = 9
                                    
                                    self.hud.mostraPontoMao(self.valorMao)
                                    
                                    self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "sim")
                                    self.enviaComandoTodosJogadores({'nove':'aceitou:%s' % self.mesa.jogadores[self.proximoJogador].nome},'info')
                                    cmd = self.informaVezJogar(0)
                                    self.removeBalao()

                                elif respPedNove == 'doze':
                                    self.statusMao = 3
                                    self.valorMao = 9
                                    
                                    self.hud.mostraPontoMao(self.valorMao)
                                    
                                    self.jogadorDozeador = self.mesa.jogadores[self.proximoJogador]
                                    self.jogadorIncrementador = self.jogadorDozeador
                                    self.mostraBalao(self.jogadorDozeador, "doze")
                                    respPedDoze = self.pedeIncremento2('doze', self.jogadorDozeador)
                                    self.removeBalao()
                                    
                                    if respPedDoze == 'sim':
                                        self.statusMao = 4
                                        self.valorMao = 12
                                        
                                        self.hud.mostraPontoMao(self.valorMao)
                                        
                                        self.mostraBalao(self.jogadorDaVez, "sim")
                                        self.enviaComandoTodosJogadores({'doze':'aceitou:%s' % self.jogadorDaVez.nome},'info')
                                        cmd = self.informaVezJogar(0)
                                        self.removeBalao()                      

                                    elif respPedDoze == 'nao':# negando pedido de Doze
                                        self.mostraBalao(self.jogadorDaVez, "nao")
                                        dozeFugido = True
                                        break
                                
                                elif respPedNove == 'nao':# negando pedido de Nove
                                    self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "nao")
                                    noveFugido = True
                                    break
        
                                
                            elif respPedSeis == 'nao': # negando pedido de Meio Pau
                                self.mostraBalao(self.jogadorDaVez, "nao")
                                seisFugido = True
                                break
                                
                        elif respPedTruco == 'nao': # negando pedido de truco
                            self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "nao")
                            trucoFugido = True
                            break
                        
                    else: 
                        print "Partida não pode ser trucada!"
                    

                        
            elif 'seis' in cmd:
                
                if cmd['seis'] == 'pedido':
                    
                    print "Pediu-se Meio Pau!!"
                    print "Status da Mao: %s" % self.statusMao
                    
                    
                
                    if self.statusMao == 1:
            
                        self.jogadorMeioPauador = self.jogadorDaVez
                        self.jogadorIncrementador = self.jogadorMeioPauador
                        self.mostraBalao(self.jogadorMeioPauador, "seis")
                        cmd1 = self.pedeIncremento1('seis', self.jogadorMeioPauador)
                        self.removeBalao()

                        if cmd1 == 'sim':
                            cmd = ''
                            self.statusMao = 2 #Partida em Meio Pau
                            self.valorMao = 6
                            
                            self.hud.mostraPontoMao(self.valorMao)
                            
                            self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "sim")
                            self.enviaComandoTodosJogadores({'seis':'aceitou:%s' % self.mesa.jogadores[self.proximoJogador].nome},'info')
                            cmd = self.informaVezJogar(0)
                            self.removeBalao()
                        
                        elif cmd1 == 'nove':
                            
                            
                            self.statusMao = 2
                            self.valorMao = 6
                            
                            self.hud.mostraPontoMao(self.valorMao)
                            
                            self.jogadorNoveador = self.mesa.jogadores[self.proximoJogador]
                            self.jogadorIncrementador = self.jogadorNoveador
                            self.mostraBalao(self.jogadorNoveador, "nove")
                            respPedNove = self.pedeIncremento2('nove', self.jogadorNoveador)
                            self.removeBalao()
                            
                                     
                            #Jogador aceitou o Pedido de Meis Pau - Seis  
                            if respPedNove == 'sim':
                                cmd = ''
                                self.statusMao = 3
                                self.valorMao = 9
                                
                                self.hud.mostraPontoMao(self.valorMao)

                                self.mostraBalao(self.jogadorDaVez, "sim")
                                self.enviaComandoTodosJogadores({'nove':'aceitou:%s' % self.jogadorDaVez.nome},'info')
                                self.removeBalao()
                                cmd = self.informaVezJogar(0)
                                
                                if 'pedido' in cmd.values():
                                    print "################"
                                    print "aqui era a hora!"
                                    print "################"                           
                                
                                
                            elif respPedNove == 'doze':
                                respPedDoze = ''
                                self.statusMao = 3
                                self.valorMao = 9
                                
                                self.hud.mostraPontoMao(self.valorMao)
                            
                                self.jogadorDozeador = self.jogadorDaVez
                                self.jogadorIncrementador = self.jogadorDozeador
                                self.mostraBalao(self.jogadorDozeador, "doze")
                                respPedDoze = self.pedeIncremento1('doze', self.jogadorDozeador)
                                self.removeBalao()
                                
                                #Jogador aceitou o Pedido de Meio Pau - Seis  
                                if respPedDoze == 'sim':
                                    self.statusMao = 4
                                    self.valorMao = 12
                                    
                                    self.hud.mostraPontoMao(self.valorMao)
                                    
                                    self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "sim")
                                    self.enviaComandoTodosJogadores({'doze':'aceitou:%s' % self.mesa.jogadores[self.proximoJogador].nome},'info')
                                    cmd = self.informaVezJogar(0)
                                    self.removeBalao()
                     

                                elif respPedDoze == 'nao':# negando pedido de Doze
                                    self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "nao")
                                    dozeFugido = True
                                    break


                            elif respPedNove == 'nao': # negando pedido de Nove
                                self.mostraBalao(self.jogadorDaVez, "nao")
                                noveFugido = True
                                break

                        elif cmd1 == 'nao': # negando pedido de meio pau
                            self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "nao")
                            seisFugido = True
                            break
                    else:
                        print "Partida não pode valer seis!"
                    
            
            elif 'nove' in cmd:
                
                if cmd['nove'] == 'pedido':
                    
                    print "Pediu-se Nove!!"
                    print "Status da Mao: %s" % self.statusMao
                    
                    if self.statusMao == 2:

                        self.jogadorNoveador = self.jogadorDaVez
                        self.jogadorIncrementador = self.jogadorNoveador
                        self.mostraBalao(self.jogadorNoveador, "nove")
                        cmd1 = self.pedeIncremento1('nove', self.jogadorNoveador)
                        self.removeBalao()
                    
                        if cmd1 == 'sim':
                            cmd = ''
                            self.statusMao = 3 #Partida em Nove
                            self.valorMao = 9
                            
                            self.hud.mostraPontoMao(self.valorMao)
                            
                            self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "sim")
                            self.enviaComandoTodosJogadores({'nove':'aceitou:%s' % self.mesa.jogadores[self.proximoJogador].nome},'info')
                            
                            cmd = self.informaVezJogar(0)
                            self.removeBalao()
                            
                        elif cmd1 == 'doze':
                            respPedDoze = ''
                            self.statusMao = 3
                            self.valorMao = 9
                            
                            self.hud.mostraPontoMao(self.valorMao)
                            
                            self.jogadorDozeador = self.mesa.jogadores[self.proximoJogador]
                            self.jogadorIncrementador = self.jogadorDozeador
                            self.mostraBalao(self.jogadorDozeador, "doze")
                            respPedDoze = self.pedeIncremento2('doze', self.jogadorDozeador)
                            self.removeBalao()
      
                            #Jogador aceitou o Pedido de Doze 
                            if respPedDoze == 'sim':
                                cmd = ''
                                self.statusMao = 4
                                self.valorMao = 12
                                
                                self.hud.mostraPontoMao(self.valorMao)

                                self.mostraBalao(self.jogadorDaVez, "sim")
                                self.enviaComandoTodosJogadores({'doze':'aceitou:%s' % self.jogadorDaVez.nome},'info')
                                self.removeBalao()
                                cmd = self.informaVezJogar(0)
  
                            elif respPedDoze == 'nao': # negando pedido de Doze
                                self.mostraBalao(self.jogadorDaVez, "nao")
                                dozeFugido = True
                                break
                            
                        elif cmd1 == 'nao': # negando pedido de Nove
                            self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "nao")
                            noveFugido = True
                            break

                    else:
                        print "Partida não pode valer Nove!"

            elif 'doze' in cmd:
                if cmd['doze'] == 'pedido':
                    
                    print "Pediu-se Doze!!"
                    print "Status da Mao: %s" % self.statusMao
                    
                    if self.statusMao == 3:

                        self.jogadorDozeador = self.jogadorDaVez
                        self.jogadorIncrementador = self.jogadorDozeador
                        self.mostraBalao(self.jogadorDozeador, "doze")
                        cmd1 = self.pedeIncremento1('doze', self.jogadorDozeador)
                        self.removeBalao()
                        
                        
                        if cmd1 == 'sim':
                            cmd = ''
                            self.statusMao = 4 #Partida em Doze
                            self.valorMao = 12
                            
                            self.hud.mostraPontoMao(self.valorMao)
                            
                            self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "sim")
                            self.enviaComandoTodosJogadores({'doze':'aceitou:%s' % self.mesa.jogadores[self.proximoJogador].nome},'info')
                            cmd = self.informaVezJogar(0)
                            self.removeBalao()
                            
                        elif cmd1 == 'nao': # negando pedido de Doze
                            self.mostraBalao(self.mesa.jogadores[self.proximoJogador], "nao")
                            dozeFugido = True
                            break
                
                    else:
                        print "Partida não pode valer Doze!"
                     
            if 'carta' in cmd:
                strCarta = cmd['carta']
                carta = self.jogadorDaVez.descartaBT(strCarta)
                self.animaDescartar(carta, self.jogadorDaVez)
                print "%s jogou a carta %s na mesa." % (self.jogadorDaVez.nome, carta)
                self.mesa.cartas.append(carta)
                 
            #if self.jogadorDaVez.nome.startswith("CPU"):
            time.sleep(3)
                        
            for jogador in self.mesa.jogadores:
                if jogador.vezDeJogar:
                    jogador.vezDeJogar = False
                
            print "Jogador Incrmentador:"
            if self.jogadorIncrementador:
                print self.jogadorIncrementador.nome
            print "Cartas na mesa:"
            print self.mesa.cartas
            
        indiceJogadorGanhador = None
        
        
            
        
        if len(self.mesa.cartas) == 4:
            print "[%s, %s, %s, %s]" % (self.mesa.cartas[0].valorJogo, self.mesa.cartas[1].valorJogo, self.mesa.cartas[2].valorJogo, self.mesa.cartas[3].valorJogo)
            indiceJogadorGanhador = self.mesa.compararCartas(self.mesa.cartas)
            if indiceJogadorGanhador != None:
                jogadorGanhador = self.mesa.jogadores[indiceJogadorGanhador]
                cartaGanhadora = self.mesa.cartas[indiceJogadorGanhador]
                self.efeitoCartaVencedora(cartaGanhadora)

                equipeGanhadora = jogadorGanhador.getEquipe()
                self.mesa.equipes[equipeGanhadora-1].pontosMao += 1
                jogadorGanhador.ganhadorUltimaRodada = True
                if self.placarMao == (0,0): 
                    self.equipeGanhadora1aRodada = self.mesa.equipes[equipeGanhadora-1]
                    print "Equipe ganhadora da 1a rodada: %s" % self.equipeGanhadora1aRodada
            else:
                if self.placarMao == (1,1):
                    self.equipeGanhadora1aRodada.pontosMao += 1
                    equipeGanhadora = None
                    
                    
                else:
                    if self.placarMao == (0,0):
                        self.equipeGanhadora1aRodada = None
                        
                    self.mesa.equipes[0].pontosMao += 1
                    self.mesa.equipes[1].pontosMao += 1
                    equipeGanhadora = None
                    

            self.placarMao = (self.mesa.equipes[0].pontosMao, self.mesa.equipes[1].pontosMao)
            
            time.sleep(10)
              
        else:
            if len(self.mesa.cartas) < 4:
                if trucoFugido:
                    print "O truco foi fugido!!!"
                    equipeGanhadora = self.jogadorTrucador.getEquipe()
                    self.mesa.equipes[equipeGanhadora-1].pontosMao += 2
                    self.placarMao = (self.mesa.equipes[0].pontosMao, self.mesa.equipes[1].pontosMao)
                if seisFugido:
                    print "O Meio Pau foi fugido!!!"
                    equipeGanhadora = self.jogadorMeioPauador.getEquipe()
                    self.mesa.equipes[equipeGanhadora-1].pontosMao += 2
                    self.placarMao = (self.mesa.equipes[0].pontosMao, self.mesa.equipes[1].pontosMao)
                if noveFugido:
                    print "O Nove foi fugido!!!"
                    equipeGanhadora = self.jogadorNoveador.getEquipe()
                    self.mesa.equipes[equipeGanhadora-1].pontosMao += 2
                    self.placarMao = (self.mesa.equipes[0].pontosMao, self.mesa.equipes[1].pontosMao)
                if dozeFugido:
                    print "O Doze foi fugido!!!"
                    equipeGanhadora = self.jogadorDozeador.getEquipe()
                    self.mesa.equipes[equipeGanhadora-1].pontosMao += 2
                    self.placarMao = (self.mesa.equipes[0].pontosMao, self.mesa.equipes[1].pontosMao)
                            
                self.removeBalao()

            else:    
                print "#################################################################################"
                print "################ Problemas com o numero de cartas na mesa!!! ####################"
                print "#################################################################################"
                
        if equipeGanhadora == None:
            equipeGanhadora = "cango"
        
        for carta in self.mesa.cartas:
            self.remove(carta.imagem)
        
        self.mesa.limpar()
        self.removeSeta()
        
        self.informaPontosMao(equipeGanhadora)
    

    def removeSeta(self):
        self.setaVezJogador.position = (9999, 9999)

    def informaVezJogador(self, jogador):
        if self.setaVezJogador.position != (0, 0):
            self.remove(self.setaVezJogador)
        equipe = jogador.getEquipe()
        numero = jogador.getNumero()
        if equipe == 1:
            pos1 = (self.larguraTela/2)
            if numero == 1:
                pos2 = self.alturaTela - 257
                angulo = 0
            elif numero == 2:
                pos2 = self.alturaTela - 577
                angulo = 180
        elif equipe == 2:
            pos2 = self.alturaTela/2 - 35
            if numero == 2:
                pos1 = 819
                angulo = 90
            elif numero == 1:
                pos1 = 206
                angulo = 270

        self.setaVezJogador.position = (pos1, pos2)
        self.setaVezJogador.rotation = angulo
        self.add(self.setaVezJogador, z=1)


    def removeBalao(self):
        self.balaoFala.position = (9999, 9999)
        self.fala.position = (9999, 9999)
    
      
    def mostraBalao(self, jogador, comando):
        
        self.fala = None
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
            self.fala = self.falaTruco
        elif comando == 'seis':
            self.fala = self.falaSeis
        elif comando == 'nove':
            self.fala = self.falaNove
        elif comando == 'doze':
            self.fala = self.falaDoze
        elif comando == 'sim':
            self.fala = self.falaDesce       
        elif comando == 'nao':
            self.fala = self.falaCorro        
              
        self.balaoFala.position = pos1, pos2
        self.balaoFala.rotation = angulo
        
        self.fala.position = pos1, pos2
        self.fala.rotation = angulo
        
        #self.balaoFala.add(self.fala, z=1)
        
        self.add(self.fala, z=999)
        self.add(self.balaoFala, z=998)
          
        
        
  
    def efeitoCartaVencedora(self, carta):
        carta = carta.imagem
        
        efeito = ScaleBy(2, duration=2) + Reverse(ScaleBy(2, duration=2)) + \
                 ScaleBy(2, duration=2) + Reverse(ScaleBy(2, duration=2))
                 
        carta.do(efeito)
        
        
    
    def informaPontosMao(self, equipeGanhadora):
        for jogador in self.mesa.jogadores:
            if equipeGanhadora == "cango":
                jogador.envia_comandoJS({'pontos':'cango'}, self.statusMao)
            else:
                if self.mesa.equipes[equipeGanhadora-1].ehDaEquipe(jogador):
                    jogador.envia_comandoJS({'pontos':'nosso'}, self.statusMao)
                else:
                    jogador.envia_comandoJS({'pontos':'outros'}, self.statusMao)
            
        
 
    def desenhaCartaVira(self):
        if self.mesa.vira:
            print self.mesa.vira
            self.larguraTela, self.alturaTela 
            self.mesa.vira.imagem.position = 201, self.alturaTela  - 561
            self.baralho.imagem.position = 182, self.alturaTela  - 601
            
            self.add(self.baralho.imagem, z=12 )
            self.add(self.mesa.vira.imagem, z=1 )

        
        
        
        
    def animaDistribuirCartas(self, jogador):
        print "Jogador - %s:" % jogador.nome
        print "Número: %s Equipe: %s" % (jogador.getNumero(), jogador.getEquipe())
        
        angulo = 0
        
        if jogador.getEquipe() == 1:
            pos1 = (self.larguraTela/2) - self.larguraCarta #eixo x
            if jogador.getNumero() == 1:
                pos2 = self.alturaTela-130 #eixo y
            elif jogador.getNumero() == 2:
                pos2 = 64 #eixo y
        elif jogador.getEquipe() == 2:
            pos2 = self.alturaTela/2 + (self.larguraCarta/2) #eixo y
            if jogador.getNumero() == 2:
                pos1 = self.larguraTela - self.alturaCarta/2 - 21 #eixo x=956
                angulo = 90
            elif jogador.getNumero() == 1:
                pos1 = self.alturaCarta/2 + 25 #eixo X=83
                angulo = 270
                

        for carta in jogador.mao:        
            print "Carta: %s - Posicao: (%s,%s)" % (carta, pos1, pos2)
            
            carta.imagem.position = pos1, pos2
            pos1Temp, pos2Temp = pos1, pos2
            carta.imagemCostas.position = 182, self.alturaTela  - 601 #-100, -100
            if jogador.getEquipe() == 2:
                pos2 -= self.larguraCarta + 2
            else:
                pos1 += self.larguraCarta + 2
            
            
            carta.imagem.rotation = angulo
            carta.imagemCostas.rotation = angulo
            
            self.add(carta.imagemCostas, z=900)
            
            move = MoveTo((pos1Temp,pos2Temp), duration=0.1)
            carta.imagemCostas.do(move)
            
            time.sleep(0.5)
            print "Amimei o distribuir cartas!!!!!"
            
        
       
    def desenhaCartasJogadores(self, jogador):


        angulo = 0
        
        if jogador.getEquipe() == 1:
            pos1 = (self.larguraTela/2) - self.larguraCarta #eixo x
            if jogador.getNumero() == 1:
                pos2 = self.alturaTela-130 #eixo y
            elif jogador.getNumero() == 2:
                pos2 = 64 #eixo y
        elif jogador.getEquipe() == 2:
            pos2 = self.alturaTela/2 + (self.larguraCarta/2) #eixo y
            if jogador.getNumero() == 2:
                pos1 = self.larguraTela - self.alturaCarta/2 - 21 #eixo x=956
                angulo = 90
            elif jogador.getNumero() == 1:
                pos1 = self.alturaCarta/2 + 25 #eixo X=83
                angulo = 270


        for carta in jogador.mao:
            self.add(carta.imagem, z=carta.valorJogo )
            #time.sleep(0.1)
            
            
       

    def animaDescartar(self, carta, jogador):
        
        self.remove(carta.imagemCostas)
        
        if jogador.getEquipe() == 1:
            posDesc1 = self.larguraTela/2
            if jogador.getNumero() == 1:
                posDesc2 = self.alturaTela/2 + self.alturaCarta/2 - 35
            elif jogador.getNumero() == 2:
                posDesc2 = self.alturaTela/2 - self.alturaCarta/2 - 35
        elif jogador.getEquipe() == 2:
            posDesc2 = self.alturaTela/2 - 40
            if jogador.getNumero() == 2:
                posDesc1 = self.larguraTela/2 + self.larguraCarta/2 
            elif jogador.getNumero() == 1:
                posDesc1 = self.larguraTela/2 - self.larguraCarta/2 
                
        move = MoveTo((posDesc1,posDesc2), duration=1)
        carta.imagem.do(move)
        print "Amimei o descarte da carta!!!!!"
       
       
    def desenhaMesaJogo(self):
       pass

        
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
    hud = Hud(jogo)
    s.add( hud, z=10, name='hud' )
    jogo.hud = hud

    return s





if __name__ == '__main__':

    director.init(width=1024, height=768, do_not_scale=True)    
    director.run(run())
    