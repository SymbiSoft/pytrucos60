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
        
        while max(self.placarPartida) < 12: #Voltar para 12 assim q terminar os testes
            self.novaMao = True
            self.iniciaMao()
            
            print "#########################################"
            print "########### PLACAR DA PARTIDA ###########"
            print self.placarPartida
            print "%s - %s X %s - %s" % (self.mesa.equipes[0], self.mesa.equipes[0].pontos, self.mesa.equipes[1].pontos, self.mesa.equipes[1])
            print "#########################################"
            self.hud.mostraPlacar(self.placarPartida)
            
    
    
            
    def iniciaPartida(self): #, dt):
        
        self.placarPartida = (0,0)

        
        if not self.partidaIniciada:
            self.baralho.embaralhar()
            self.mesa.definirEquipes()
            self.mesa.definir1aOrdemJogadores()
                
                
            for equipe in self.mesa.equipes:
                print "Equipe: %s - Jogador: %s" % (equipe, equipe.jogadores[0].nome)
                equipe.jogadores[0].setNumero(1)
                print "Número: %s - Num. Equipe: %s" % (equipe.jogadores[0].getNumero(),equipe.jogadores[0].getEquipe())
                
            for equipe in self.mesa.equipes:
                print "Equipe: %s - Jogador: %s" % (equipe, equipe.jogadores[1].nome)
                equipe.jogadores[1].setNumero(2)
                print "Número: %s - Num. Equipe: %s" % (equipe.jogadores[1].getNumero(),equipe.jogadores[1].getEquipe())
                
            for jogador in self.mesa.jogadores:
                self.hud.desenhaJogadores(jogador.getNumero(), jogador.getEquipe(), jogador.nome)
                
                
                
                
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
        
        #Feito somente para testes retirar após o dicionário de posições estiver completo e descomentar a linha acima.
        #cartaBT = ['3e', '2e', 'ac']
        #cartas_enviadas = "cartas:" + "/".join(cartaBT)
        
        


        for jogador in self.mesa.jogadores:
            respJogador = {}
            self.desenhaCartasJogadores(jogador)
            jogador.envia_comandoJS(jogador.maoJS())
            time.sleep(1)
            while 'OK' not in respJogador:
                respJogador = jogador.recebe_comandoJS()
                while not respJogador:
                    pass
            
            
            

        status = ''
        while max(self.placarMao) < 2 :#or status != 'fim':
            self.mesa.definirOrdemJogadores(self.novaMao)
            #status = 
            self.jogarRodada()
            print "########################################"
            print "########### PLACAR DA RODADA ###########"
            print self.placarMao
            print "%s - %s X %s - %s" % (self.mesa.equipes[0], self.mesa.equipes[0].pontosMao, self.mesa.equipes[1].pontosMao, self.mesa.equipes[1])
            print "########################################"
            
            self.novaMao = False
            
        
        for equipe in self.mesa.equipes:
            if equipe.pontosMao >= 2:
               equipe.pontos += self.valorMao
               equipeGanhadora = equipe
        
        self.placarPartida = (self.mesa.equipes[0].pontos, self.mesa.equipes[1].pontos)
        self.informaFimMao(equipeGanhadora)
        
        
        self.baralho.recolherCartas(self.mesa.jogadores)
        
        for jogador in self.mesa.jogadores:
            for carta in jogador.mao:
                self.remove(carta.imagem)
        
        self.remove(self.mesa.vira.imagem)
        self.mesa.zeraManilhas(self.baralho)
        self.equipeGanhadora1aRodada = None
        
        
            

    def informaFimMao(self, equipe):
        print "Vou informar do fim da Mão!"
        for jogador in self.mesa.jogadores:
            respFimMao = {}
            if equipe.ehDaEquipe(jogador):
                jogador.envia_comandoJS({'fim-mao':['ganhou', equipe.pontos]})
            else:
                jogador.envia_comandoJS({'fim-mao':['perdeu', equipe.pontos]})
            while 'OK' not in respFimMao:
                respFimMao = jogador.recebe_comandoJS()
                while not respFimMao:
                    pass
            
        
        
        


    def jogarRodada(self):
        
        
        trucoFugido = False
        seisFugido = False
        print "Irá começar um ciclo de %s rodadas" % len(self.mesa.jogadores)
        
        for jogador in self.mesa.jogadores:
            if jogador.vezDeJogar:
                jogador.vezDeJogar = False
        
        for ordem in range(len(self.mesa.jogadores)):
            self.mesa.jogadores[ordem].vezDeJogar = True
                
            
            jogadorTrucador = None
            for jogador in self.mesa.jogadores:
                if jogador.vezDeJogar:
                    jogadorDaVez = jogador
                    
            self.hud.informaVezJogador(jogadorDaVez)
            
            jogadorDaVez.envia_comandoJS({'vez':'sua'})
            
            print "Jogador da vez: %s" % jogadorDaVez.nome
            
            for jogador in self.mesa.jogadores:
                if not jogador.vezDeJogar:
                    jogador.envia_comandoJS({'vez':jogadorDaVez.nome})
            
            cmd =''
            cmd = jogadorDaVez.recebe_comandoJS()

            while not cmd:
               pass
            
            
            print " +== Comando recebido: ==+ "
            print cmd
            print type(cmd)
            
            if 'truco' in cmd:
                if cmd['truco'] == 'pedido':
                    
                    print "Pediu-se Trucoo!!"
                    print "Status da Mao: %s" % self.statusMao
                    jogadorTrucador = jogadorDaVez
                    
                    if self.statusMao == 0:
                        
                        print "Teste lista Jogadores q não estao da vez:"
                        for jogador in self.mesa.jogadores:
                            if not jogador.vezDeJogar:
                                print jogador.nome
                                
                        for jogador in self.mesa.jogadores:
                            if not jogador.vezDeJogar:
                                resp = ''
                                jogador.envia_comandoJS({'truco':":%s" %jogadorDaVez.nome})
                                resp = jogador.recebe_comandoJS()
                                while not resp:
                                    pass
                                print resp
                            else:
                                jogador.envia_comandoJS({'truco':"Enviado"})
                        
                        proximoJogador = ordem+1
                        if proximoJogador>len(self.mesa.jogadores)-1:
                            proximoJogador = 0
                        
                        cmd1 = ''
                        self.mesa.jogadores[proximoJogador].envia_comandoJS({'truco':'aceita?'})
                        
                        
                        cmd1 = self.mesa.jogadores[proximoJogador].recebe_comando()
                        while not cmd1:
                            pass
                        print cmd1
                        
                        if cmd1 == 'sim':
                            
                            self.statusMao = 1
                            self.valorMao = 3
                            
                            proximoJogador = ordem + 1
                            if proximoJogador > len(self.mesa.jogadores)-1:
                                proximoJogador = 0
                                
                            for jogador1 in self.mesa.jogadores:
                                #if not jogador.vezDeJogar:
                                respOK = ''
                                jogador1.envia_comandoJS({'truco':'aceitou:%s' % self.mesa.jogadores[proximoJogador].nome}) 
                                print "estou esperando de %s" % jogador1.nome
                                respOK = jogador1.recebe_comandoJS()
                                print respOK
                                while not respOK:
                                    pass
                                print respOK
                                
                                
                            jogadorDaVez.envia_comandoJS({'vez':'sua'})
                            
                            cmd = ''
                            print "esperando de %s" % jogadorDaVez.nome
                            cmd = jogadorDaVez.recebe_comandoJS()
                            while not cmd:
                                pass
                            print cmd
                            
                        
                        elif cmd1 == 'seis':
                            for jogador in self.mesa.jogadores:
                                if not jogador is self.mesa.jogadores[ordem+1]:
                                    jogador.envia_comando("jogador %s pediu seis" % self.mesa.jogadores[ordem+1].nome)
                            
                            jogadorDaVez.envia_comando('aceita seis?')
                            
                            cmd2 = jogadorDaVez.recebe_comando()
                            
                            if cmd2 == 'sim':
                                self.statusMao = 2
                                self.valorMao = 6
                                for jogador in self.mesa.jogadores:
                                    if not jogador.vezDeJogar:
                                        jogador.envia_comando("jogador %s aceitou o seis" % jogadorDaVez.nome)
                                
                                jogadorDaVez.envia_comando('descarte!')
                                
                                cmd = jogadorDaVez.recebe_comando()
                                
                                
                            elif cmd2 == 'nove':
                                for jogador in self.mesa.jogadores:
                                    if not jogador.vezDeJogar:
                                        jogador.envia_comando("jogador %s pediu nove" % jogadorDaVez.nome)
                                
                                self.mesa.jogadores[ordem+1].envia_comando('aceita nove?')
                                
                                cmd3 = self.mesa.jogadores[ordem+1].recebe_comando()
                                
                                if cmd3 == 'sim':
                                    self.statusMao = 3
                                    self.valorMao = 9
                                    for jogador in self.mesa.jogadores:
                                        if not jogador is self.mesa.jogadores[ordem+1]:
                                            jogador.envia_comando("jogador %s aceitou o nove" % self.mesa.jogadores[ordem+1].nome)
                                    
                                    jogadorDaVez.envia_comando('descarte!')
                                    
                                    cmd = jogadorDaVez.recebe_comando()
                                    
                                
                                elif cmd3 == 'doze':
                                    for jogador in self.mesa.jogadores:
                                        if not jogador.vezDeJogar:
                                            jogador.envia_comando("jogador %s pediu doze" % self.mesa.jogadores[ordem+1].nome)
                                        
                                    jogadorDaVez.envia_comando('aceita doze?')
                                    
                                    cmd4 = jogadorDaVez.recebe_comando()
                                    
                                    if cmd4 == 'sim':
                                        self.statusMao = 4
                                        self.valorMao = 12
                                        for jogador in self.mesa.jogadores:
                                            if not jogador.vezDeJogar:
                                                jogador.envia_comando("jogador %s aceitou o doze" % jogadorDaVez.nome)
                                        
                                        jogadorDaVez.envia_comando('descarte!')
                                        cmd = jogadorDaVez.recebe_comando()
                                        
                                    elif cmd4 == 'nao':
                                        break
                                    
                                elif cmd3 == 'nao':
                                    break
                                
                            elif cmd2 == 'nao':
                                break
                                
                        elif cmd1 == 'nao': # negando pedido de truco
                            trucoFugido = True
                            break
                        
                    else: 
                        print "Partida não pode ser trucada!"
                    
                    
                        
            elif 'seis' in cmd:
                if self.statusMao == 1:
                    for jogador in self.mesa.jogadores:
                        if not jogador.vezDeJogar:
                            jogador.envia_comando("jogador %s pediu seis" % jogadorDaVez.nome)
                    
                    self.mesa.jogadores[ordem+1].envia_comando('aceita seis?')
                    cmd1 = self.mesa.jogadores[ordem+1].recebe_comando()
                    if cmd1 == 'sim':
                        self.statusMao = 2
                        self.valorMao = 6
                        for jogador in self.mesa.jogadores:
                            if not jogador is self.mesa.jogadores[ordem+1]:
                                jogador.envia_comando("jogador %s aceitou o seis" % self.mesa.jogadores[ordem+1].nome)
                        
                        jogadorDaVez.envia_comando('descarte!')
                        cmd = jogadorDaVez.recebe_comando()
                    
                    elif cmd1 == 'nove':
                        for jogador in self.mesa.jogadores:
                            if not jogador is self.mesa.jogadores[ordem+1]:
                                jogador.envia_comando("jogador %s pediu nove" % self.mesa.jogadores[ordem+1].nome)
                            
                        jogadorDaVez.envia_comando('aceita nove?')
                        cmd2 = jogadorDaVez.recebe_comando()
                        if cmd2 == 'sim':
                            self.statusMao = 3
                            self.valorMao = 9
                            for jogador in self.mesa.jogadores:
                                if not jogador.vezDeJogar:
                                    jogador.envia_comando("jogador %s aceitou o nove" % jogadorDaVez.nome)
                            
                            jogadorDaVez.envia_comando('descarte!')
                            cmd = jogadorDaVez.recebe_comando()
                        
                        elif cmd2 == 'doze':
                            for jogador in self.mesa.jogadores:
                                if not jogador.vezDeJogar:
                                    jogador.envia_comando("jogador %s pediu doze" % jogadorDaVez.nome)
                                
                            self.mesa.jogadores[ordem+1].envia_comando('aceita doze?')
                            cmd3 = self.mesa.jogadores[ordem+1].recebe_comando()
                            
                            if cmd3 == 'sim':
                                self.statusMao = 4
                                self.valorMao = 12
                                for jogador in self.mesa.jogadores:
                                    if not jogador is self.mesa.jogadores[ordem+1]:
                                        jogador.envia_comando("jogador %s aceitou o doze" % self.mesa.jogadores[ordem+1].nome)
                                
                                jogadorDaVez.envia_comando('descarte!')
                                cmd = jogadorDaVez.recebe_comando()
                                
                            if cmd3 == 'nao':
                                break
                        
                        elif cmd2 == 'nao':
                            break
                    
                    elif cmd1 == 'nao': # negando pedido de meio pau
                        seisFugido = True
                        break
                else:
                    print "Partida não pode valer seis!"
                    
            
            elif 'nove' in cmd:
                if self.statusMao == 2:
                    for jogador in self.mesa.jogadores:
                        if not jogador.vezDeJogar:
                            jogador.envia_comando("jogador %s pediu nove" % jogadorDaVez.nome)
                    
                    self.mesa.jogadores[ordem+1].envia_comando('aceita nove?')
                    cmd1 = self.mesa.jogadores[ordem+1].recebe_comando()
                    if cmd1 == 'sim':
                        self.statusMao = 3
                        self.valorMao = 9
                        for jogador in self.mesa.jogadores:
                            if not jogador is self.mesa.jogadores[ordem+1]:
                                jogador.envia_comando("jogador %s aceitou o nove" % self.mesa.jogadores[ordem+1].nome)
                        
                        jogadorDaVez.envia_comando('descarte!')
                        cmd = jogadorDaVez.recebe_comando()
                        
                    elif cmd1 == 'doze':
                        for jogador in self.mesa.jogadores:
                            if not jogador is self.mesa.jogadores[ordem+1]:
                                jogador.envia_comando("jogador %s pediu doze" % self.mesa.jogadores[ordem+1].nome)
                            
                        jogadorDaVez.envia_comando('aceita doze?')
                        cmd2 = jogadorDaVez.recebe_comando()
                        
                        if cmd2 == 'sim':
                            self.statusMao = 4
                            self.valorMao = 12
                            for jogador in self.mesa.jogadores:
                                if not jogador.vezDeJogar:
                                    jogador.envia_comando("jogador %s aceitou o doze" % jogadorDaVez.nome)
                            
                            jogadorDaVez.envia_comando('descarte!')
                            cmd = jogadorDaVez.recebe_comando()
                        
                        elif cmd2 == 'nao':
                            print "Jogador %s não aceitou o pedido de doze" % jogadorDaVez.nome
                            break
                    
                    elif cmd1 == 'nao':
                        print "Jogador %s não aceitou o pedido de nove" % self.mesa.jogadores[ordem+1].nome
                        break
                    
                else:
                    print "Partida não pode valer nove!"
                
            elif 'doze' in cmd:
                if self.statusMao == 3:
                    for jogador in self.mesa.jogadores:
                        if not jogador.vezDeJogar:
                            jogador.envia_comando("jogador %s pediu doze" % jogadorDaVez.nome)
                        
                    self.mesa.jogadores[ordem+1].envia_comando('aceita doze?')
                    cmd1 = self.mesa.jogadores[ordem+1].recebe_comando()
                    
                    if cmd1 == 'sim':
                        self.statusMao = 4
                        self.valorMao = 12
                        for jogador in self.mesa.jogadores:
                            if not jogador is self.mesa.jogadores[ordem+1]:
                                jogador.envia_comando("jogador %s aceitou o doze" % self.mesa.jogadores[ordem+1].nome)
                        
                        jogadorDaVez.envia_comando('descarte!')
                        cmd = jogadorDaVez.recebe_comando()
                        
                    if cmd1 == 'nao':
                        break
                else:
                    print "Partida não pode valer doze!"
                    
                    
                    
            if 'carta' in cmd:
                strCarta = cmd['carta']
                carta = jogadorDaVez.descartaBT(strCarta)
                self.animaDescartar(carta, jogadorDaVez)
                print "%s jogou a carta %s na mesa." % (jogadorDaVez.nome, carta)
                self.mesa.cartas.append(carta)
                
            
            #if jogadorDaVez.nome.startswith("CPU"):
            time.sleep(3)
                
                
            for jogador in self.mesa.jogadores:
                if jogador.vezDeJogar:
                    jogador.vezDeJogar = False
                

            
            print "Cartas na mesa:"
            print self.mesa.cartas
            
            
        indiceJogadorGanhador = None
        

        
        if len(self.mesa.cartas) == 4:
            print "[%s, %s, %s, %s]" % (self.mesa.cartas[0].valorJogo, self.mesa.cartas[1].valorJogo, self.mesa.cartas[2].valorJogo, self.mesa.cartas[3].valorJogo)
            indiceJogadorGanhador = self.mesa.compararCartas(self.mesa.cartas)
            if indiceJogadorGanhador != None:
                jogadorGanhador = self.mesa.jogadores[indiceJogadorGanhador]
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
            
            time.sleep(5)
            

            
            
            
            
        else:
            if len(self.mesa.cartas) < 4:
                if trucoFugido:
                    print "O truco foi fugido!!!"
                    equipeGanhadora = jogadorTrucador.getEquipe()
                    self.mesa.equipes[equipeGanhadora-1].pontosMao += 2
                    self.placarMao = (self.mesa.equipes[0].pontosMao, self.mesa.equipes[1].pontosMao)
                    
                    #return 'fim'
                    
                
            
            else:    
                print "#################################################################################"
                print "################ Problemas com o numero de cartas na mesa!!! ####################"
                print "#################################################################################"
                
        if equipeGanhadora == None:
            equipeGanhadora = "cango"
        
        for carta in self.mesa.cartas:
            self.remove(carta.imagem)
        
        self.mesa.limpar()
        self.hud.removeSeta()
        
     
        self.informaPontosMao(equipeGanhadora)
        
        #return 'ok'
        
        
    
    def informaPontosMao(self, equipeGanhadora):
        for jogador in self.mesa.jogadores:
            if equipeGanhadora == "cango":
                jogador.envia_comandoJS({'pontos':'cango'})
            else:
                if self.mesa.equipes[equipeGanhadora-1].ehDaEquipe(jogador):
                    jogador.envia_comandoJS({'pontos':'nosso'})
                else:
                    jogador.envia_comandoJS({'pontos':'outros'})
            
        
    
    
    def iniciaRodada(self):
        print "passei por aqui %s vezes!" % self.cont
        self.cont +=1
        
        if not self.rodadaIniciada:
            #jogador.envia_comando(jogador.formata_cartas_BT())
            for jogador in self.mesa.jogadores:
                jogador.envia_comando(cartas_enviadas)
            #print jogador.recebe_comando()
            self.rodadaIniciada = True
        
        

 
    def desenhaCartaVira(self):
        if self.mesa.vira:
            print self.mesa.vira
            self.mesa.vira.imagem.position = 100, 125
            self.add(self.mesa.vira.imagem, z=1 )

       
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
            if jogador.getNumero() == 2:
                pos1 = self.larguraTela - (5*self.larguraCarta)/2
            elif jogador.getNumero() == 1:
                pos1 = self.larguraCarta/2
                
        for carta in jogador.mao:        
            print "Carta: %s - Posicao: (%s,%s)" % (carta, pos1, pos2)
            
            carta.imagem.position = pos1, pos2
            self.add(carta.imagem, z=carta.valorJogo )
            pos1 += self.larguraCarta + 2
       
       
    def animaDistribuirCartas(self, jogador):
       pass
       

    def animaDescartar(self, carta, jogador):
        if jogador.getEquipe() == 1:
            posDesc1 = self.larguraTela/2
            if jogador.getNumero() == 1:
                posDesc2 = self.alturaTela/2 + self.alturaCarta/2 
            elif jogador.getNumero() == 2:
                posDesc2 = self.alturaTela/2 - self.alturaCarta/2 
        elif jogador.getEquipe() == 2:
            posDesc2 = self.alturaTela/2
            if jogador.getNumero() == 2:
                posDesc1 = self.larguraTela/2 + self.larguraCarta/2 
            elif jogador.getNumero() == 1:
                posDesc1 = self.larguraTela/2 - self.larguraCarta/2 
            
            
            
                
        move = MoveTo((posDesc1,posDesc2), duration=3)
        carta.imagem.do(move)
        print "Amimei o descarte da carta!!!!!"
       
       
    def desenhaMesaJogo(self):
       pass





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
                for i in self.mesa.jogadores:
                    self.mesa.jogadores[i].envia_comando(msg)
                
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
    