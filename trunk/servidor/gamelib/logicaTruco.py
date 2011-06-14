#-*- coding: utf-8 -*-

from random import shuffle, randint, randrange
import cocos



class Carta(object):
    
    def __init__(self, valor, naipe):
        self.__valores = [None, '4', '5', '6', '7', 'Dama', 'Valete', 'Rei', 'As', '2', '3', 'Pica Fumo', 'Espadilha', 'Escopeta', 'Zap']
        self.__manilhas = ['Pica Fumo', 'Espadilha', 'Escopeta', 'Zap']
        self.__naipes = ['Ouros','Espadas', 'Copas', 'Paus']
        self.__dir_imagens = "data/imagens/"
        self.valor = valor
        self.naipe = naipe
        self.ehmanilha = False
        self.imagem = cocos.sprite.Sprite(self.__dir_imagens + self.montaNomeArq())



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
        self.__equipe = equipe
        self.pontos = pontos

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
    
    def setEquipe(self, equipe):
        self.__equipe = equipe
    
    def getEquipe(self):
        return self.__equipe 


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
        equipe1Temp = [jogador for jogador in self.jogadores if jogador.getEquipe() == 1]
        equipe2Temp = [jogador for jogador in self.jogadores if jogador.getEquipe() == 2]
        self.equipes.append(Equipe(equipe1Temp))
        self.equipes.append(Equipe(equipe2Temp))
        #self.equipe = 1
    
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