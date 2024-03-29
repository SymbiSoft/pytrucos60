#-*- coding: utf-8 -*-
#!/usr/bin/env python

import time
import os
from threading import Thread

import cocos
from cocos.menu import *
from cocos.text import Label
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import *
from cocos.scenes.transitions import *

import jogo
import conexaoCPUs
from hudTC import Hud
import constantes
from jogador import JogadorBT, JogadorCPU, GerenciaJogadores
from conexao import ConexaoBT
from bg_layer import BGLayer
import janela_erros



class MenuIniciaPartida(Menu):
    def __init__(self, tipo_conexao, tc):
        super( MenuIniciaPartida, self).__init__() 
        self.font_item['font_size'] = 40
        self.font_item['font_name'] = 'Forte'
        self.font_item['color'] = (75,135,73,255)
        
        self.font_item_selected['font_size'] = 40
        self.font_item_selected['font_name'] = 'Forte'
        self.font_item_selected['color'] = (75,135,73,255)
        
        self.position=(-50,-250)
        
        self.tc = tc
        items = []
        items.append( MenuItem('Iniciar Partida', self.inicia_partida) )
        self.create_menu(items)
        

    def inicia_partida(self):
        
        
        self.tc.partidaIniciada = True
        
        jogadores = self.tc.obtemJogadores()
        

        qtdJogadoresBT = len(jogadores)
        if qtdJogadoresBT < 4:
            print "Socket do jogador que vai ser banido: %s" % str(jogadores[-1].socket)
            if not jogadores[-1].socket:
                print "Socket do jogador banido: %s" % jogadores[-1].socket
                print "Jogador nao inciado: %s" % jogadores.pop()
        
        qtdJogadoresBT = len(jogadores)
        print "qtdJogadoresBT: ", qtdJogadoresBT
        nrJogadorCPU = qtdJogadoresBT
        if qtdJogadoresBT < 4:
            print "eh menor q 4"
           
            while nrJogadorCPU < 4:
                print "imprimindo CPUs"
                jogadorCPU = "CPU %s" % nrJogadorCPU
                self.tc.hud.informaJogador(jogadorCPU , nrJogadorCPU)
                print "nrJogadorCPU: %s" % nrJogadorCPU
                
                for jogador in jogadores:
                    jogador.envia_comando("cmd:jogadoresconectado")
                    jogador.recebe_comando()
                    
                    
                cmd = jogadorCPU + ':' + str(nrJogadorCPU) + "|"
                for jogador in jogadores:
                    jogador.envia_comando("%s:" % cmd)
                    #print jogador.recebe_comando()
                jogadores.append(JogadorCPU(jogadorCPU , nrJogadorCPU))
                nrJogadorCPU += 1

        equipe = 1
        for jogador in jogadores:
            jogador.setEquipe(equipe)
            equipe += 1
            if equipe == 3:
                equipe = 1
        
        
        print "qtdJogadoresCPU: ", len(jogadores) - qtdJogadoresBT
        print "qtdJogadoresTotais: ", len(jogadores)
            
        
        director.push( FadeTransition(jogo.run(jogadores), 1.0 ) )


    def on_quit(self):
        # called by esc
        director.scene.end()


class TelaConexoes(cocos.layer.Layer):
    
    def __init__(self, tipo_conexao):
        super( TelaConexoes, self).__init__()
        
        self.nrJogadores=0
        self.tipo_conexao = tipo_conexao
        self.partidaIniciada = False
        self.jogadores = []
        
        print "tipo de conexao => %s " % self.tipo_conexao
        
        # Configurando camadas
        # HUD
        self.hud = Hud(self)
        
        self.add(self.hud, z=-1)
        
        
        self.titulo = Label("Aguardando Conexoes:", font_name='Forte',
            font_size=60, color = (75,135,73,255),
            x=100, y=650,
            anchor_x='left', anchor_y='top')
        
        
        self.add(self.titulo)
        
        
        if self.tipo_conexao == 'bluetooth':
            self.conexao = ConexaoBT()
            self.conexao.socket_servidor()
            threadConexao = Thread( target=self.conecta_jogadoresBT)
            threadConexao.start()
        else:
            socket = None

        #self.add(ClickableLabel("Iniciar Partida", self.inicaThread, (720, 600-30)), z = 1)


    def conecta_jogadoresBT(self):
        nrJogador = 0
        while not self.partidaIniciada:
            
            self.jogadores.append(JogadorBT(self.conexao, nrJogador, self.hud))
            self.jogadores[nrJogador].setDaemon(True)
            self.jogadores[nrJogador].start()
            print self.jogadores[nrJogador]
            time.sleep(1)
            
            try:
                while not self.jogadores[nrJogador].conectou():
                    if self.partidaIniciada:
                        print "Abortou conexao!!"
                        break
                
                self.jogadores[nrJogador].conectou()
            except IndexError:
                pass
            else:
                if self.jogadores[nrJogador].conectou():
                    time.sleep(1)
                    print "Jogador %s Conectado!!!" % self.jogadores[nrJogador].nome
                    self.jogadores[nrJogador].envia_comando("cmd:jogadoresconectado")
                    print  self.jogadores[nrJogador].recebe_comando()
                    
                    cmd = ''
                    for jogador in self.jogadores:
                        cmd += jogador.nome + ':' + str(jogador.numero) + "|"
                    self.jogadores[nrJogador].envia_comando("%s"%cmd)
                    for jogador in self.jogadores:
                        jogador.envia_comando("jogadorcnt:%s:%s" % (self.jogadores[nrJogador].nome, nrJogador))
                    
                nrJogador+=1
                
                if len(self.jogadores)==4:
                    self.partidaIniciada = True
            
            
    def obtemJogadores(self):
        return self.jogadores


def get_menu_conexao(tipo_conexao):
    scene = Scene()
    try:
        tc = TelaConexoes(tipo_conexao)
    except Exception, e:
        print "Erro em Tela Conexoes"
        print e
    try:
        scene.add(BGLayer("conexao"))
        scene.add( MultiplexLayer(tc), z=2 )
        scene.add(tc, z=2 )
        mip = MenuIniciaPartida(tipo_conexao, tc)
        scene.add( mip, z=0 )
        return scene
    except Exception, e:
        msgErro =  "Erro com o dispositivo de bluetooth"
        print msgErro
        print e
        erro = Scene(janela_erros.get_janela(msgErro))
        return erro