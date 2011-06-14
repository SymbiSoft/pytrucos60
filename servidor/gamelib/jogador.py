#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Mar 03, 2011

@author: Wander Jardim
'''


import threading
import time

class Jogador(object):
    """Objeto Jogador
    """
    nome = None
    __numero = None
    mao = []
    __equipe = None
    __pontos = 0
    tipo_conexao = ""
    ehRemoto = False
    sock = None
    info = None
    
    def setPontos(self, pontos):
        self.__pontos = pontos
    
    def getPontos(self):
        return self.__pontos

    def setEquipe(self, equipe):
        self.__equipe = equipe
    
    def getEquipe(self):
        return self.__equipe 
    
    def setNumero(self, numero):
        self.__numero = numero

    def getNumero(self):
        return self.__numero 

    def  limparCartas(self):
        self.mao = []

    def receberCarta(self, carta):
        self.mao.append(carta)

    def verCartas(self):
        var = self.mao
        return var

    def jogarCarta(self, num):
        var = self.mao[num]
        self.mao.remove(var)
        return var



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
    def __init__ (self, nome, num):
        self.numero = num
        self.nome = nome
    
    def envia_comando(self, cmd):
        print cmd    
        
    def recebe_comando(self):
        return "Nada!"
    