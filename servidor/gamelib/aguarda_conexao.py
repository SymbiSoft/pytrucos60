#-*- coding: utf-8 -*-
#!/usr/bin/env python

import time
import os

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
from jogador import JogadorBT, GerenciaJogadores
from conexao import ConexaoBT
from bg_layer import BGLayer
import janela_erros



class MenuIniciaPartida(Menu):
    def __init__(self, tipo_conexao, tc):
        super( MenuIniciaPartida, self).__init__() 
        self.font_item['font_size'] = 16
        self.font_item['color'] = (189,190,190,255)
        self.font_item_selected['font_size'] = 24
        self.font_item_selected['color'] = (128,16,32,255)
        self.position=(-150,-210)
        
        
        
        self.tc = tc
        items = []
        items.append( MenuItem('Iniciar Partida', self.inicia_partida) )
        self.create_menu(items)
        


    def inicia_partida(self):
        jogadores = self.tc.obtemJogadores()
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
                    print jogador.recebe_comando()
                    cmd = ''
                    for jogador in jogadores:
                        cmd += jogadorCPU + ':' + str(nrJogadorCPU) + "|"
                    for jogador in jogadores:
                        jogador.envia_comando("%s:" % cmd)
                        print "comando enviado >> %s:" % cmd
                    #print jogador.recebe_comando()
                    
                nrJogadorCPU += 1
            #time.sleep(10)
        director.push(Scene (jogo.run(jogadores)))

    def on_quit(self):
        # called by esc
        director.scene.end()


class TelaConexoes(cocos.layer.Layer):
    
    def __init__(self, tipo_conexao):
        super( TelaConexoes, self).__init__()
        
        self.nrJogadores=0
        self.tipo_conexao = tipo_conexao
        self.partidaIniciada = False
        
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
        
        
        self.jogadores = []
        if self.tipo_conexao == 'bluetooth':
            self.conexao = ConexaoBT()
            self.conexao.socket_servidor()
            self.conecta_jogadoresBT()
        else:
            socket = None
        self.nrJogador=0
        
    def conecta_jogadoresBT(self):
        if not self.partidaIniciada:
            self.gerenteConexao = GerenciaJogadores(self.conexao, self.hud, self.jogadores)
            self.gerenteConexao.setDaemon(True)
            self.gerenteConexao.start()
            
            #print gerenteConexao.jogadores
            #self.partidaIniciada = gerenteConexao.status
            
    def obtemJogadores(self):
        return self.gerenteConexao.jogadores
        





def get_menu_conexao(tipo_conexao):
    scene = Scene()
    try:
        tc = TelaConexoes(tipo_conexao)
        scene.add(BGLayer("conexao"))
        scene.add( MultiplexLayer(tc), z=2 )
        mip = MenuIniciaPartida(tipo_conexao, tc)
        scene.add( mip, z=0 )
        return scene
    except:
        msgErro =  "Erro com o dispositivo de bluetooth"
        print msgErro
        erro = Scene(janela_erros.get_janela(msgErro))
        return erro
    
    try:
        tc = TelaConexoes(tipo_conexao)
        scene.add(BGLayer("conexao"))
        scene.add( MultiplexLayer(tc), z=2 )
        mip = MenuIniciaPartida(tipo_conexao, tc)
        scene.add( mip, z=0 )
        return scene
    except:
        msgErro =  "Erro com o dispositivo de bluetooth"
        print msgErro
        erro = Scene(janela_erros.get_janela(msgErro))
        return erro

