#-*- coding: utf-8 -*-
'''
Created on 04/06/2011

@author: wander
'''


from random import shuffle, randint, randrange
from Tkinter import *

dir_imagens = "/media/ZDK16GB/TCC/repostcc/src/img/cartas_gif/"

class Carta(object):
    
    def __init__(self, valor, naipe):
        self.__valores = [None, '4', '5', '6', '7', 'Dama', 'Valete', 'Rei', 'As', '2', '3', 'Pica Fumo', 'Espadilha', 'Escopeta', 'Zap']
        self.__manilhas = ['Pica Fumo', 'Espadilha', 'Escopeta', 'Zap']
        self.__naipes = ['Ouros','Espadas', 'Copas', 'Paus']
        self.__dir_imagens = "/media/ZDK16GB/TCC/repostcc/src/img/cartas_gif/"
        self.valor = valor
        self.naipe = naipe
        self.ehmanilha = False
        self.imagem = PhotoImage(file = self.__dir_imagens + self.montaNomeArq())

    def __repr__(self):
        if self.ehmanilha == True:
            return '%s' % self.__valores[self.valor]
        else:
            return '%s de %s'%(self.__valores[self.valor], self.__naipes[self.naipe])

    def montaNomeArq(self):
        return '%s-%s.gif'%(self.__valores[self.valor], self.__naipes[self.naipe])



class Baralho(object):
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
            return carta.valor
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

    def recolherCartas(self):
        self.cartas = self.__cartasJogo[:]

    def repartir_mao(self, jogador):
        for i in xrange(3):
            if len(jogador.mao) < 3: 
                jogador.receberCarta(self.cartas.pop())
            else:
                print "Calma! Já tenho tres cartas :)" 

    

class Jogador(object):
    def __init__(self, nome, equipe, pontos=0):
        self.nome = nome
        self.mao = []
        self.equipe = equipe
        self.pontos = pontos
        self.numero = 0

    def  limparCartas(self):
        self.mao = []

    def receberCarta(self, carta):
        self.mao.append(carta)

    def verCarta(self):
        var = self.mao
        return var

    def jogarCarta(self, num):
        var = self.mao[num]
        self.mao.remove(var)
        return var

    def setNumero(self, numero):
        self.numero = numero



class Equipe(object):
    def __init__(self, jogadores):
        self.jogadores = jogadores
        self.pontos = 0
        self.pontosMao = 0
    
    def __repr__(self):
        return '%s e %s' % (self.jogadores[0].nome, self.jogadores[1].nome)
    
    def setPontos(self, pontos):
        self.pontos += pontos
    
    def getPontos(self):
        return self.pontos
    
    def ehDaEquipe(self, jogadorE):
        for jogador in self.jogadores:
            if jogadorE is jogador:
                return True
        return False



class Mesa(object):
    def __init__(self, jogadores, baralho):
        self.cartas = []
        self.baralho = baralho
        self.jogadores = jogadores
        self.equipes = []


    def definirEquipes(self):
        equipe1Temp = [jogador for jogador in self.jogadores if jogador.equipe == 1]
        equipe2Temp = [jogador for jogador in self.jogadores if jogador.equipe == 2]
        self.equipes.append(Equipe(equipe1Temp))
        self.equipes.append(Equipe(equipe2Temp))
        self.equipe = 1
    
    def distrubuirCartas(self):
        self.baralho.recolherCartas()
        
        for jogador in self.jogadores:
            if jogador.mao:
                jogador.limparCartas()
            
            self.baralho.repartir_mao(jogador)

    def definirOrdemJogadores(self):
        jogadoresMesa = []
        for i in range(len(self.jogadores)):
            if i % 2 == 0:
                jogadoresMesa.append(self.jogadores[i])
        for i in range(len(self.jogadores)):
            if i % 2 != 0:
                jogadoresMesa.append(self.jogadores[i])
        self.jogadores = jogadoresMesa

    def limpar(self):
        self.cartas = []

    def compararCartas(self, cartas):
        maior = 0
        cango = 0
        vencedor = 0
        for i in range (0 ,len(cartas)):
            if cartas[i].valor == maior:
                if (vencedor-i)==1: 
                    cango = 1

            if cartas[i].valor > maior:
                maior = cartas[i].valor
                vencedor = i
                cango = 0

        if cango:
            print "Cangô!"
            return None
        else:
            return vencedor



root = Tk()
root.title("PyTruco4S60 - Testando!")

photo1 = PhotoImage(file=dir_imagens+"2-Paus.gif")
# make canvas 5 times the width of a card + 100
width1 = 4 * photo1.width() + 100
height1 = 3 * photo1.height() + 30
canvas = Canvas(width=width1, height=height1)
canvas.pack()

baralho = Baralho()
baralho.embaralhar()



jogador1 = Jogador("Wander", 1)
jogador2 = Jogador("Luana", 2)
jogador3 = Jogador("Marluce", 1)
jogador4 = Jogador("Ataide", 2)

jogadoresGlobal = [jogador1, jogador2, jogador3, jogador4]

mesa = Mesa(jogadoresGlobal, baralho)
mesa.definirEquipes()
mesa.definirOrdemJogadores()



def jogarRodada():
    if mesa.cartas:
        mesa.limpar()
    
    cartaJogador1 = mesa.equipes[0].jogadores[0].jogarCarta(randrange(0, len(mesa.equipes[0].jogadores[0].mao)))
    mesa.cartas.append(cartaJogador1)
    print "Jogador %s Jogou a carta %s" % (mesa.equipes[0].jogadores[0].nome, cartaJogador1)
    
    cartaJogador2 = mesa.equipes[1].jogadores[0].jogarCarta(randrange(0, len(mesa.equipes[1].jogadores[0].mao)))
    mesa.cartas.append(cartaJogador2)
    print "Jogador %s Jogou a carta %s" % (mesa.equipes[1].jogadores[0].nome, cartaJogador2)
    
    cartaJogador3 = mesa.equipes[0].jogadores[1].jogarCarta(randrange(0, len(mesa.equipes[0].jogadores[1].mao)))
    mesa.cartas.append(cartaJogador3)
    print "Jogador %s Jogou a carta %s" % (mesa.equipes[0].jogadores[1].nome, cartaJogador3)
    
    cartaJogador4 = mesa.equipes[1].jogadores[1].jogarCarta(randrange(0, len(mesa.equipes[1].jogadores[1].mao)))
    mesa.cartas.append(cartaJogador4)
    print "Jogador %s Jogou a carta %s" % (mesa.equipes[1].jogadores[1].nome, cartaJogador4)
    
    print "Cartas na mesa:"
    print mesa.cartas
    pos2 =0
    for carta in mesa.cartas:
        pos1 = 0
        canvas.create_image(5+pos1, 5+pos2, image=carta.imagem, anchor=NW)
        pos1 += 65
    pos2 += 70
    
    
    
    ganhador = mesa.compararCartas(mesa.cartas)
    
    if mesa.equipes[0].ehDaEquipe(mesa.jogadores[ganhador]):
        equipeGanhadora = mesa.equipes[0]
        equipeGanhadora.pontosMao += 1
        print "Parabens Equipe %s voces ganharam a rodada, com a carta %s do jogador %s." % (mesa.equipes[0], mesa.cartas[ganhador] , mesa.jogadores[ganhador].nome)
    elif mesa.equipes[1].ehDaEquipe(mesa.jogadores[ganhador]):
        equipeGanhadora = mesa.equipes[1]
        equipeGanhadora.pontosMao += 1
        print "Parabens Equipe %s voces ganharam a rodada, com a carta %s do jogador %s." % (mesa.equipes[1], mesa.cartas[ganhador] , mesa.jogadores[ganhador].nome)
    else:
        print "A Partida esta empatada. Quem jogar a maior carta ganha!"
        mesa.equipes[0].pontosMao += 1
        mesa.equipes[1].pontosMao += 1

        
    print "Placar da Mão: \n Equipe1 %s X %s Equipe2" % (mesa.equipes[0].pontosMao, mesa.equipes[1].pontosMao)
    
    mesa.limpar()
    return equipeGanhadora
    


def jogarMao(truco=False, seis=False, nove=False, doze=False):
    placar = 0
    
    for equipe in mesa.equipes:
        equipe.pontosMao = 0
    mesa.distrubuirCartas()
    mesa.baralho.embaralhar()
    
    

    
    while placar < 2:
        equipeGanhadora = jogarRodada()
        placar = equipeGanhadora.pontosMao
        print "Placar: (%s)" % placar
    
    if truco:
        equipeGanhadora.pontos += 3
    elif seis:
        equipeGanhadora.pontos += 6
    elif nove:
        equipeGanhadora.pontos += 9
    elif doze:
        equipeGanhadora.pontos += 12
    else:
        equipeGanhadora.pontos += 1
    
    print "Placar da Partida:"
    print "Equipe 1 %s X %s Equipe 2" % (mesa.equipes[0].pontos, mesa.equipes[1].pontos)
    
    return equipeGanhadora


def JogarPartida():
    for equipe in mesa.equipes:
        equipe.pontos = 0
    fimPartida = False
    while not fimPartida:
        equipeGanhadora = jogarMao()
        if equipeGanhadora.pontos >=12:
            fimPartida = True
            
    print "PARABENS A EQUIPE %s, QUE GANHOU A PARTIDA COM %s PONTOS!!!" % (equipeGanhadora, equipeGanhadora.pontos)




JogarPartida()



  
    
    

#from logicaTrucoTestes import *


