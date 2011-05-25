#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Mar 03, 2011

@author: Wander Jardim
'''


import threading
import time

class Jogador:
    """Objeto Jogador
    """
    def __init__(self, tipo_conexao, conexao, hud ):
        self.nome = "Jogador"
        self.cartasMao = []
        self.equipe = None
        self.tipo_conexao = tipo_conexao
        self.ehRemoto = False
        self.conexao = conexao 
        self.hud = hud
        self.sock = None
        self.info = None



class GerenciaJogadores(threading.Thread):
    def __init__ (self, conexao, hud, jogadores):
        threading.Thread.__init__(self)
        self.conexao = conexao
        self.hud = hud
        self.jogadores = []
        
    def run(self):
        self.jogadores = self.conecta_jogadores()
        
    def conecta_jogadores(self):
        partidaIniciada = False
        self.nrJogador = 0
        jogadores = []
        while not partidaIniciada:
            print "Rodei pela %sa. vez" % self.nrJogador
            (sock, info) = self.conexao.conectaJogador(self.conexao.socket)
            jogadores.append(JogadorBT(self.conexao, sock, info, self.nrJogador))
            print "Iniciei um jogador"
            self.hud.informaJogador(jogadores[self.nrJogador].nome, self.nrJogador)
            jogadores[self.nrJogador].envia_comando("cmd:jogadoresconectado")
            print jogadores[self.nrJogador].recebe_comando()
            cmd = ''
            for jogador in jogadores:
                cmd += jogador.nome + ':' + str(jogador.numero) + "|"
            jogadores[self.nrJogador].envia_comando("%s"%cmd)
            for jogador in jogadores:
                jogador.envia_comando("jogadorcnt:%s:%s" % (jogadores[self.nrJogador].nome, self.nrJogador))
                print "Enviei jogadorcnt:%s:%s" % (jogadores[self.nrJogador].nome, self.nrJogador)    
            self.nrJogador+=1
            if len(jogadores)==2:
                partidaIniciada = True       
        self.nrJogadores = len(jogadores) 
        return jogadores       



class JogadorBT(Jogador):
    def __init__ (self, conexao, sock, info, num):
        self.socket = sock
        self.info = info
        self.numero = num
        self.nome = conexao.obtem_nome(self.info[0])
        self.estahRodando = False
        
        
    def envia_comando(self, cmd):
        self.socket.send(cmd)    
        
    def recebe_comando(self):
        return self.socket.recv(1024)
    
    def desconecta(self):
        self.socket.close()
        print self.nome, ": desconectado"



class JogadorCPU(Jogador):
    def __init__ (self, conexao, sock, info, num):
        pass