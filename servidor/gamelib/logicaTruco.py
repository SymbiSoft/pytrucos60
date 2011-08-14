#-*- coding: utf-8 -*-

from random import shuffle, randint, randrange
import cocos



class Carta(object):
    def __init__(self, valor, naipe):
        self.__valores = [None, '4', '5', '6', '7', 'Dama', 'Valete', 'Rei', 'As', '2', '3', 'Pica Fumo', 'Espadilha', 'Escopeta', 'Zap']
        self.__manilhas = ['Pica Fumo', 'Espadilha', 'Escopeta', 'Zap']
        self.__naipes = ['Ouros','Espadas', 'Copas', 'Paus']
        self.__dir_imagens = "data/imagens/"
        self.valorJogo = valor
        self.valorPadrao = valor
        self.valorCarta = self.__valores[self.valorJogo]
        self.__indice_naipe = naipe
        self.naipe = self.__naipes[naipe]
        self.valorBT = "%s%s" % (self.valorCarta[0].isdigit() and self.valorCarta[0] or self.valorCarta[0].lower(), self.naipe[0].lower())
        self.nomeCartaPadrao = "%s de %s" % (self.__valores[self.valorPadrao], self.naipe)
        self.ehmanilha = False
        self.imagem = cocos.sprite.Sprite(self.__dir_imagens + self.montaNomeArq())
        
    def __repr__(self):
        if self.ehmanilha:
            return '%s' % self.__valores[self.valorJogo]
        else:
            return '%s de %s'%(self.__valores[self.valorJogo], self.__naipes[self.__indice_naipe])

    def montaNomeArq(self):
        return '%s-%s.gif'%(self.__valores[self.valorJogo], self.__naipes[self.__indice_naipe])


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

    def maoBT(self):
        return [i.valorBT for i in self.mao]

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
        self.jogadoresEmOrdemMesa = jogadores
        self.equipes = []
        self.vira=None


    def definirEquipes(self):
        equipe1Temp = [jogador for jogador in self.jogadores if jogador.getEquipe() == 1]
        equipe2Temp = [jogador for jogador in self.jogadores if jogador.getEquipe() == 2]
        self.equipes.append(Equipe(equipe1Temp))
        self.equipes.append(Equipe(equipe2Temp))
        #self.equipe = 1
    
    def distrubuirCartas(self):
        #self.baralho.recolherCartas()
        
        for jogador in self.jogadores:
            if jogador.mao:
                jogador.limparCartas()
            
            self.baralho.repartir_mao(jogador)


    def definir1aOrdemJogadores(self):
        
        print "Jogadores antes de ordenar:"
        print self.jogadores
        jogadoresMesa = []
        
        for i in range(len(self.jogadores)):
            if i % 2 == 0:
                jogadoresMesa.append(self.jogadores[i])
        for i in range(len(self.jogadores)):
            if i % 2 != 0:
                jogadoresMesa.append(self.jogadores[i])
        self.jogadores = jogadoresMesa



    def definirOrdemJogadores(self, novaMao):
        novaLista = []
        
        indiceGanhador = None
        indiceIniciouPartida = None

        
        if novaMao:
            for i in range(len(self.jogadoresEmOrdemMesa)):
                if self.jogadoresEmOrdemMesa[i].iniciouUltimaPartida:
                    indiceIniciouPartida = i
            
            if indiceIniciouPartida != None:
                for i in range(len(self.jogadoresEmOrdemMesa)):
                    if i == 0:
                        novoIndice = indiceIniciouPartida+1
                        if novoIndice > 3:
                            novoIndice = 0
                        novaLista.append(self.jogadoresEmOrdemMesa[novoIndice])
                        
                    else:
                        novoIndice = novoIndice + 1
                        if novoIndice > 3:
                            novoIndice = 0
                            
                        novaLista.append(self.jogadoresEmOrdemMesa[novoIndice])
                
                for j in novaLista:
                    if j.iniciouUltimaPartida:
                        j.iniciouUltimaPartida = False
                
                novaLista[0].iniciouUltimaPartida = True
                
                self.jogadores = novaLista
                
            
        else:
            for i in range(len(self.jogadores)):
                if self.jogadores[i].ganhadorUltimaRodada:
                    indiceGanhador = i
        
            if indiceGanhador != None:
                for i in range(len(self.jogadores)):
                    if i == 0:
                        novaLista.append(self.jogadores[indiceGanhador])
                    else:
                        novoIndice = indiceGanhador + i
                        if novoIndice > 3:
                            novoIndice = novoIndice - len(self.jogadores)
                            
                        novaLista.append(self.jogadores[novoIndice])
            
                self.jogadores = novaLista
                
        for j in self.jogadores:
            if j.ganhadorUltimaRodada:
                j.ganhadorUltimaRodada = False

            
        print "Jogadores depois de ordenar:"
        print self.jogadores
        
        
                
 
    def limpar(self):     
        self.cartas = []

    def compararCartas(self, cartas):
        maior = 0
        cango = 0
        vencedor = 0
        for i in range (0 ,len(cartas)):
            if cartas[i].valorJogo == maior:
                if (vencedor-i)==-1 or (vencedor-i)==-3:
                    cango = 1

            if cartas[i].valorJogo > maior:
                maior = cartas[i].valorJogo
                vencedor = i
                cango = 0

        if cango:
            print "Cangô!"
            return None
        else:
            return vencedor


    def defineManilhas(self,baralho):
        
        self.zeraManilhas(baralho)
        
        self.vira=baralho.cartas.pop(randint(1,len(baralho.cartas)-1))

        if self.vira.valorJogo == 10:
                self.vira.valorJogo = 1
        self.manilhas = []
        for carta in baralho.cartas:
            if carta.valorJogo == (self.vira.valorJogo + 1): 
                self.manilhas.append(carta)
                carta.ehmanilha = True

        for manilha in self.manilhas:
            if manilha.naipe == 'Ouros':
                manilha.valorJogo = 11
            elif manilha.naipe == 'Espadas':
                manilha.valorJogo = 12
            elif manilha.naipe == 'Copas':
                manilha.valorJogo = 13
            elif manilha.naipe == 'Paus':
                manilha.valorJogo = 14

    def zeraManilhas(self, baralho):
        for carta in baralho.cartas:
            if carta.ehmanilha:
                carta.valorJogo = carta.valorPadrao
                carta.ehmanilha = False



