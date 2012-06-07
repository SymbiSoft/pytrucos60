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
from hudTC import Hud
import constantes
from jogador import JogadorBT, JogadorCPU, GerenciaJogadores
from conexao import ConexaoBT
from bg_layer import BGLayer
import janela_erros



class ConexaoCPUs(cocos.layer.Layer): # must be layer - scene causes anims/actions to fail
    def __init__(self, jogadores):
        super( ConexaoCPUs, self).__init__()
        
        # Configurando camadas
        # HUD
        self.hud = Hud(self)
        
        self.add(self.hud, z=-1)
        
        
        self.titulo = Label("Aguardando conexao", font_name='Times New Roman',
            font_size=23,
            x=30, y=600,
            anchor_x='left', anchor_y='top')
        
        
        self.add(self.titulo)
        
    


    def mostraConexaoCpus(self, jogadores):
        #self.tc.partidaIniciada = True
        
        #jogadores = self.tc.obtemJogadores()
        
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
                self.hud.informaJogador(jogadorCPU , nrJogadorCPU)
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
            #time.sleep(10)
        #director.push( FadeTransition(jogo.run(jogadores), 1.0 ) )
        
        #director.push(Scene (BGLayer("mesa"),jogo.run(jogadores)))

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
        
        
        self.titulo = Label("Aguardando conexao", font_name='Times New Roman',
            font_size=23,
            x=30, y=600,
            anchor_x='left', anchor_y='top')
        
        
        self.add(self.titulo)
        
        
        if self.tipo_conexao == 'bluetooth':
            self.conexao = ConexaoBT()
            self.conexao.socket_servidor()
            threadConexao = Thread( target=self.conecta_jogadoresBT)
            threadConexao.start()
        else:
            socket = None

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
        
def run(jogadores): 
    s = cocos.scene.Scene()
    telaConexCpus =  ConexaoCPUs(jogadores)
    s.add( telaConexCpus, z=1, name='ctrl')
    s.add(BGLayer("conexao"))
    telaConexCpus.mostraConexaoCpus(jogadores)
    #hud = Hud(jogo)
    #s.add( hud, z=10, name='hud' )
    #jogo.hud = hud

    return s



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
        mip = MenuIniciaPartida(tipo_conexao, tc)
        scene.add( mip, z=0 )
        return scene
    except Exception, e:
        msgErro =  "Erro com o dispositivo de bluetooth"
        print msgErro
        print e
        erro = Scene(janela_erros.get_janela(msgErro))
        return erro


