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
    vezDeJogar = False
    ganhadorUltimaRodada = False

    def run(self):
        self.jogadores = self.conecta_jogadores()

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

    def conecta_jogadores(self):
        pass



class GerenciaJogadores():
    def __init__ (self, conexao, hud, jogadores):
        threading.Thread.__init__(self)
        self.conexao = conexao
        self.hud = hud
        self.jogadores = []
        

        
     



class JogadorBT(Jogador, threading.Thread):
    def __init__ (self, conexao, num, hud):
        threading.Thread.__init__(self)
        self.conexao = conexao
        self.numero = num
        self.estahRodando = False
        self.hud = hud
        self.socket = None
        
    def run(self):
        self.conecta_jogadores()



    def conecta_jogadores(self):
        (self.socket, self.info) = self.conexao.conectaJogador(self.conexao.socket)
        self.nome = self.conexao.obtem_nome(self.info[0])
        print "Iniciei um jogador: %s" % self.nome
        self.hud.informaJogador(self.nome, self.numero)

          

    def envia_comando(self, cmd):
        self.socket.send(cmd)
        print "enviei: %s" % cmd
        
    def recebe_comando(self):
        rec = self.socket.recv(1024)
        print "recebi: %s" % rec
        return rec

    def conectou(self):
        return self.socket != None


    def desconecta(self):
        self.socket.close()
        print self.nome, ": desconectado"

    def formata_cartas_BT(self):
        cartaBT = []
        for carta in self.mao:
            cartaBT.append(carta.valorBT)
            
        return "cartas:" + "/".join(cartaBT)

            

class JogadorCPU(Jogador):
    def __init__ (self, nome, num):
        self.numero = num
        self.nome = nome
    
    def envia_comando(self, cmd):
        print cmd    
        
    def recebe_comando(self):
        return "Nada!"
    
    def formata_cartas_BT(self):
        cartaBT = []
        for carta in self.mao:
            cartaBT.append(carta.valorBT)
            
        return "cartas:" + "/".join(cartaBT)
        
        