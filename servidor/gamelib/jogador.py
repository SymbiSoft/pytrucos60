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
    
    def conectaJogador_temp(self):
        if self.tipo_conexao == 'bluetooth':
            
            JogadorBT()



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
            if len(jogadores)>1:
                jogadores[self.nrJogador].envia_comando("cmd:ehmaiorq1")
                print jogadores[self.nrJogador].recebe_comando()
                cmd = ''
                for jogador in jogadores:
                    
                    jogador.envia_comando("jogadorcnt:%s:%s" % (jogadores[self.nrJogador].nome, self.nrJogador))
                    print "Enviei jogadorcnt:%s:%s" % (jogadores[self.nrJogador].nome, self.nrJogador)
                    cmd += jogador.nome + ':' + str(jogador.numero) + "|"
                jogadores[self.nrJogador].envia_comando("cmd:%s"%cmd)
            else:
                print "eh o primeiro"
                jogadores[self.nrJogador].envia_comando("cmd:primeiro")
                print "Enviei cmd:primeiro para %s" % jogadores[self.nrJogador].nome
                print jogadores[self.nrJogador].recebe_comando()
                infoJogador1 = "%s:%s" % (jogadores[self.nrJogador].nome, self.nrJogador)
                jogadores[self.nrJogador].envia_comando(infoJogador1)

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



#JogadorThread
class JogadorBT_old(Jogador, threading.Thread):
    def __init__ (self,conexao, hud, num):
        threading.Thread.__init__(self)
        self.numero = num
        self.conexao = conexao
        self.hud = hud
        self.nome = "Jogador"
        self.sock = None
        self.info = None
        #self.quem = quem
        #self.isRunning = threading.Event()
        #self.isRunning.clear()





    def run(self):
        try:
            
            self.conecta_jogador(self.conexao)

            
            
            """
            self.envia_comando(self.name)
            time.sleep(8)
            print "essa é a thread: %s \n" % self.getName()
            
            
                #data = self.socket.recv(1024)
                #if len(data) == 0: break
                #print self.client_info, ": recebido [%s]" % data
                #self.socket.send(data)
                #print self.client_info, ": enviado [%s]" % data
                
            """
        except IOError:
            print "Deu um erro aqui 123!"
        #self.socket.close()
        #print self.client_info, ": desconectado"



    def conecta_jogador(self,conexao):
        self.sock, self.info = conexao.conectaJogador(conexao.socket)
        self.nome = conexao.obtem_nome(self.info[0])
        print "Jogador %s Conectado: %s - %s" % (self.numero, self.nome, self.info)
        
        print 'meu nome é: %s' % self.nome
        self.hud.informaJogador(self.nome, self.numero)
        self.hud.informaQtdJogador(self.numero+1)
        self.envia_comando("%s Conectado!" % self.nome)
        print self.info
        



    def envia_comando(self, cmd):
        self.sock.send(cmd)

    def recebe_comando(self):
        return self.sock.recv(1024)
    
    def desconecta(self):
        self.sock.close()
        print self.client_info, ": desconectado"
    
    



