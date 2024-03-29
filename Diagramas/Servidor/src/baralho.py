#######################################################
# 
# baralho.py
# Python implementation of the Class Baralho
# Generated by Enterprise Architect
# Created on:      29-jul-2011 20:20:04
# Original author: Wander Jardim
# 
#######################################################


from random import shuffle


class Baralho(object):
    __cartasJogo = []
    cartas = []
    
    def __init__(self):
        self.__cartasJogo = []
        for valor in xrange(1,11):
            for naipe in xrange(4):
                self.__cartasJogo.append(Carta(valor,naipe))
        self.__cartasJogo = self.__cartasJogo
        shuffle(self.__cartasJogo)
        self.cartas = self.__cartasJogo[:]
        
    def ordenar(self):
        cartas = self.cartas
        
        def pegaValorCarta(carta):
            return carta.valorJogo
        self.cartas.sort(key=pegaValorCarta)

    def embaralhar(self):
        shuffle(self.cartas)

    def recolherCartas1(self):
        self.cartas = []
        for valor in xrange(1,11):
            for naipe in xrange(4):
                self.cartas.append(Carta(valor,naipe))
        self.cartas = self.cartas
        shuffle(self.cartas)

    def recolherCartas(self, jogadores):
        for jogador in jogadores:
            if jogador.mao:
                jogador.mao = []
        
        self.cartas = self.__cartasJogo[:]
        
        for carta in self.cartas:
            carta.imagem.position = (0,0)

    def repartir_mao(self, jogador):
        for i in xrange(3):
            if len(jogador.mao) < 3: 
                jogador.receberCarta(self.cartas.pop())
            else:
                print "Calma! J� tenho tres cartas :)" 