#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Mar 03, 2011

@author: Wander Jardim
'''


import threading
import time
from random import randrange

import jsons60 as json


class Jogador(object):
    """Objeto Jogador
    """
    nome = "None"
    __numero = None
    mao = []
    __equipe = None
    __pontos = 0
    ehRemoto = False
    sock = None
    info = None
    vezDeJogar = False
    ganhadorUltimaRodada = False
    iniciouUltimaPartida = False

    def __repr__(self):
        return self.nome
        
        
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
    
    def maoJS(self):
        return  {"cartas": [i.valorBT for i in self.mao] }


    def conecta_jogadores(self):
        pass

    def descartaBT(self, carta):
        for i in range(len(self.mao)):
            if self.mao[i].valorBT == carta:
                #indice = i
                carta = self.mao[i]#ndice]
        self.mao.remove(carta)
        
        return carta


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

          

    def envia_comando(self, cmd, statusMao=0):
        self.socket.send(cmd)
        print "enviei: %s" % cmd

    def envia_comandoJS(self, cmd, statusMao=0, podeIncrementar=1):
        self.socket.send(json.write(cmd))
        print "Eu %s envieiJS: %s" % (self.nome, cmd)

    def recebe_comandoJS(self):
        print "esperando comando:"
        rec = json.read(self.socket.recv(1024))
        print "Eu %s recebiJS: %s" % (self.nome, rec)
        return rec
  
    def recebe_comando(self):
        print "esperando comando:"
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
    
    def envia_comando(self, cmd, statusMao=0):
        try:           
            self.cmd = json.read(cmd)
        except:
            self.cmd = cmd
        print "Jogador: %s - Enviou: %s" % (self.nome, cmd)

    def envia_comandoJS(self, cmd, statusMao, podeIncrementar=0):
        try:           
            self.cmd = json.read(cmd)
        except:
            self.cmd = cmd
        
        self.statusMao = int(statusMao)
        self.podeIncrementar = podeIncrementar
        print "Jogador: %s - Recebeu o comando: %s" % (self.nome, cmd)
        print "Pode Incrementar?"


    def recebe_comandoJS(self):
        carta = {'xxx':'xxx'}
        resp = carta
        if self.cmd:
            if 'vez' in self.cmd:
                if self.cmd['vez'] == 'sua':
                    if self.mao:
                        print "statusMao em r_bJS: %s" % self.statusMao
                        print type(self.statusMao)
                        if self.statusMao == 0:
                            print "Posso pedir Truco"
                            decisaoTruco = randrange(0, 10)
                            if decisaoTruco > 1:
                                resp = {'truco':'pedido'}
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                        
                        elif self.statusMao == 1:

                            if self.podeIncrementar:
                                print "Posso pedir Seis"
                                decisaoSeis = randrange(0, 10)
                                if decisaoSeis > 2:
                                    resp = {'seis':'pedido'}
                                else:
                                    cartaInstance = self.mao[randrange(0, len(self.mao))]
                                    carta = {"carta": cartaInstance.valorBT}
                                    resp = carta
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                        
                        elif self.statusMao == 2:
                            if self.podeIncrementar:
                                print "Posso pedir Nove"
                                decisaoNove = randrange(0, 10)
                                if decisaoNove > 3:
                                    resp = {'nove':'pedido'}
                                else:
                                    cartaInstance = self.mao[randrange(0, len(self.mao))]
                                    carta = {"carta": cartaInstance.valorBT}
                                    resp = carta
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                        
                        elif self.statusMao == 3:
                            if self.podeIncrementar:
                                print "Posso pedir Doze"
                                decisaoDoze = randrange(0, 10)
                                if decisaoDoze > 4:
                                    resp = {'doze':'pedido'}
                                else:
                                    cartaInstance = self.mao[randrange(0, len(self.mao))]
                                    carta = {"carta": cartaInstance.valorBT}
                                    resp = carta
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                        else:
                            print "O status ta bugado"
                            cartaInstance = self.mao[randrange(0, len(self.mao))]
                            carta = {"carta": cartaInstance.valorBT}
                            resp = carta
                            
                    else:
                        print "Eu %s não tenho mais cartas!" % self.nome
            elif 'cartas' in self.cmd:
                resp =  {'OK':'Cartas Recebidas'}
            
            elif 'fim-mao' in self.cmd:
                resp =  {'OK':'Fim Mao'}
            
            elif 'truco' in self.cmd:
                if self.cmd['truco'].startswith(':'): 
                    resp =  {'OK':'Pedido de Truco  Recebido'}
                elif self.cmd['truco'] == 'aceita?':
                    opcoesTruco = ['nao', 'sim', 'seis']
                    resp =  opcoesTruco[randrange(0, len(opcoesTruco))]
                    
                elif self.cmd['truco'].startswith('aceitou') :
                    nomeJogadorAceitouTruco =  self.cmd['truco'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Truco' % nomeJogadorAceitouTruco}
            
            elif 'seis' in self.cmd:
                if self.cmd['seis'].startswith(':'): 
                    resp =  {'OK':'Pedido de Meio Pau  Recebido'}
                elif self.cmd['seis'] == 'aceita?':
                    opcoesMeioPau = ['nao', 'sim', 'nove']
                    resp =  opcoesMeioPau[randrange(0, len(opcoesMeioPau))]
                    
                elif self.cmd['seis'].startswith('aceitou') :
                    nomeJogadorAceitouSeis =  self.cmd['seis'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Meio Pau' % nomeJogadorAceitouSeis}



            elif 'nove' in self.cmd:
                if self.cmd['nove'].startswith(':'): 
                    resp =  {'OK':'Pedido de Nove  Recebido'}
                elif self.cmd['nove'] == 'aceita?':
                    opcoesNove = ['nao', 'sim', 'doze']
                    resp =  opcoesNove[randrange(0, len(opcoesNove))]
                    
                elif self.cmd['nove'].startswith('aceitou') :
                    nomeJogadorAceitouNove =  self.cmd['nove'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Nove' % nomeJogadorAceitouNove}



            elif 'doze' in self.cmd:
                if self.cmd['doze'].startswith(':'): 
                    resp =  {'OK':'Pedido de Doze  Recebido'}
                elif self.cmd['doze'] == 'aceita?':
                    opcoesDoze = ['nao', 'sim']
                    resp =  opcoesDoze[randrange(0, len(opcoesDoze))]
                    
                elif self.cmd['doze'].startswith('aceitou') :
                    nomeJogadorAceitouDoze =  self.cmd['doze'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Doze' % nomeJogadorAceitouDoze}


            
            else:
                resp =  'Sem resposta!'
            
        print "cmd: %s" % self.cmd
        self.cmd = None
        print "Jogador %s enviou o comando %s." % (self.nome, resp)
        time.sleep(1)
        return resp




    def recebe_comando(self):
        carta = {'xxx':'xxx'}
        resp = carta
        if self.cmd:
            if 'vez' in self.cmd:
                if self.cmd['vez'] == 'sua':
                    if self.mao:
                        print "statusMao em r_bJS: %s" % self.statusMao
                        print type(self.statusMao)
                        if self.statusMao == 0:
                            print "Posso pedir Truco"
                            decisaoTruco = randrange(0, 10)
                            if decisaoTruco > 1:
                                resp = {'truco':'pedido'}
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                        
                        elif self.statusMao == 1:

                            if self.podeIncrementar:
                                print "Posso pedir Seis"
                                decisaoSeis = randrange(0, 10)
                                if decisaoSeis > 2:
                                    resp = {'seis':'pedido'}
                                else:
                                    cartaInstance = self.mao[randrange(0, len(self.mao))]
                                    carta = {"carta": cartaInstance.valorBT}
                                    resp = carta
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                        
                        elif self.statusMao == 2:
                            if self.podeIncrementar:
                                print "Posso pedir Nove"
                                decisaoNove = randrange(0, 10)
                                if decisaoNove > 3:
                                    resp = {'nove':'pedido'}
                                else:
                                    cartaInstance = self.mao[randrange(0, len(self.mao))]
                                    carta = {"carta": cartaInstance.valorBT}
                                    resp = carta
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                        
                        elif self.statusMao == 3:
                            if self.podeIncrementar:
                                print "Posso pedir Doze"
                                decisaoDoze = randrange(0, 10)
                                if decisaoDoze > 4:
                                    resp = {'doze':'pedido'}
                                else:
                                    cartaInstance = self.mao[randrange(0, len(self.mao))]
                                    carta = {"carta": cartaInstance.valorBT}
                                    resp = carta
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                        else:
                            print "O status ta bugado"
                            cartaInstance = self.mao[randrange(0, len(self.mao))]
                            carta = {"carta": cartaInstance.valorBT}
                            resp = carta
                            
                    else:
                        print "Eu %s não tenho mais cartas!" % self.nome
            elif 'cartas' in self.cmd:
                resp =  {'OK':'Cartas Recebidas'}
            
            elif 'fim-mao' in self.cmd:
                resp =  {'OK':'Fim Mao'}
            
            elif 'truco' in self.cmd:
                if self.cmd['truco'].startswith(':'): 
                    resp =  {'OK':'Pedido de Truco  Recebido'}
                elif self.cmd['truco'] == 'aceita?':
                    opcoesTruco = ['nao', 'sim', 'seis']
                    resp =  opcoesTruco[randrange(0, len(opcoesTruco))]
                    
                elif self.cmd['truco'].startswith('aceitou') :
                    nomeJogadorAceitouTruco =  self.cmd['truco'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Truco' % nomeJogadorAceitouTruco}
            
            elif 'seis' in self.cmd:
                if self.cmd['seis'].startswith(':'): 
                    resp =  {'OK':'Pedido de Meio Pau  Recebido'}
                elif self.cmd['seis'] == 'aceita?':
                    opcoesMeioPau = ['nao', 'sim', 'nove']
                    resp =  opcoesMeioPau[randrange(0, len(opcoesMeioPau))]
                    
                elif self.cmd['seis'].startswith('aceitou') :
                    nomeJogadorAceitouSeis =  self.cmd['seis'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Meio Pau' % nomeJogadorAceitouSeis}



            elif 'nove' in self.cmd:
                if self.cmd['nove'].startswith(':'): 
                    resp =  {'OK':'Pedido de Nove  Recebido'}
                elif self.cmd['nove'] == 'aceita?':
                    opcoesNove = ['nao', 'sim', 'doze']
                    resp =  opcoesNove[randrange(0, len(opcoesNove))]
                    
                elif self.cmd['nove'].startswith('aceitou') :
                    nomeJogadorAceitouNove =  self.cmd['nove'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Nove' % nomeJogadorAceitouNove}



            elif 'doze' in self.cmd:
                if self.cmd['doze'].startswith(':'): 
                    resp =  {'OK':'Pedido de Doze  Recebido'}
                elif self.cmd['doze'] == 'aceita?':
                    opcoesDoze = ['nao', 'sim']
                    resp =  opcoesDoze[randrange(0, len(opcoesDoze))]
                    
                elif self.cmd['doze'].startswith('aceitou') :
                    nomeJogadorAceitouDoze =  self.cmd['doze'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Doze' % nomeJogadorAceitouDoze}


            
            else:
                resp =  'Sem resposta!'
            
        print "cmd: %s" % self.cmd
        self.cmd = None
        print "Jogador %s enviou o comando %s." % (self.nome, resp)
        time.sleep(1)
        return resp



    def recebe_comandoXX(self):
        carta = {'zzz':'zzz'}
        resp = carta
        if self.cmd:
            if 'vez' in self.cmd:
                if self.cmd['vez'] == 'sua':
                    if self.mao:   
                        print "statusMao em rb: %s" % self.statusMao
                        if self.statusMao == 0:
                            decisaoTruco = randrange(0, 10)
                            if decisaoTruco > 5:
                                resp = {'truco':'pedido'}
                            else:
                                cartaInstance = self.mao[randrange(0, len(self.mao))]
                                carta = {"carta": cartaInstance.valorBT}
                                resp = carta
                                
                        else:
                            cartaInstance = self.mao[randrange(0, len(self.mao))]
                            carta = {"carta": cartaInstance.valorBT}
                            resp = carta
                    else:
                        print "Eu %s não tenho mais cartas!" % self.nome
            elif 'cartas' in self.cmd:
                resp =  {'OK':'Cartas Recebidas'}
            
            elif 'fim-mao' in self.cmd:
                resp =  {'OK':'Fim Mao'}
            
            elif 'truco' in self.cmd:
                if self.cmd['truco'].startswith(':'): 
                    resp =  {'OK':'Pedido de Truco  Recebido'}
                elif self.cmd['truco'] == 'aceita?':
                    opcoesTruco = ['seis']  #, 'nao', 'sim']
                    resp =  opcoesTruco[randrange(0, len(opcoesTruco))]
                    
                elif self.cmd['truco'].startswith('aceitou') :
                    nomeJogadorAceitouTruco =  self.cmd['truco'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Truco' % nomeJogadorAceitouTruco}

            elif 'seis' in self.cmd:
                if self.cmd['seis'].startswith(':'): 
                    resp =  {'OK':'Pedido de Meio Pau Recebido'}
                elif self.cmd['seis'] == 'aceita?':
                    opcoesMeioPau = ['nove'] # 'nao', 'sim']
                    resp =  opcoesMeioPau[randrange(0, len(opcoesMeioPau))]
                    
                elif self.cmd['seis'].startswith('aceitou') :
                    nomeJogadorAceitouSeis =  self.cmd['seis'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Meio Pau' % nomeJogadorAceitouSeis}

            
            elif 'nove' in self.cmd:
                if self.cmd['nove'].startswith(':'): 
                    resp =  {'OK':'Pedido de Nove  Recebido'}
                elif self.cmd['nove'] == 'aceita?':
                    opcoesNove = ['doze'] #'sim'] #, 'nao', 
                    resp =  opcoesNove[randrange(0, len(opcoesNove))]
                    
                elif self.cmd['nove'].startswith('aceitou') :
                    nomeJogadorAceitouNove =  self.cmd['nove'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Nove' % nomeJogadorAceitouNove}



            elif 'doze' in self.cmd:
                if self.cmd['doze'].startswith(':'): 
                    resp =  {'OK':'Pedido de Doze  Recebido'}
                elif self.cmd['doze'] == 'aceita?':
                    opcoesDoze = ['nao'] #'sim', 
                    resp =  opcoesDoze[randrange(0, len(opcoesDoze))]
                    
                elif self.cmd['doze'].startswith('aceitou') :
                    nomeJogadorAceitouDoze =  self.cmd['doze'].split(':')[1]
                    resp =  {'OK':'O Jogador %s aceitou o Doze' % nomeJogadorAceitouDoze}


            
            else:
                resp =  'Sem resposta!'
            
                
            
        print "cmd: %s" % self.cmd
        self.cmd = None
        print "Jogador %s enviou o comando %s." % (self.nome, resp)
        time.sleep(1)
        return resp


    def formata_cartas_BT(self):
        cartaBT = []
        for carta in self.mao:
            cartaBT.append(carta.valorBT)
            
        return "cartas:" + "/".join(cartaBT)
        
        