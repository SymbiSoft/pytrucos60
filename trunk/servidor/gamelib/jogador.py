#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Mar 03, 2011

@author: Wander Jardim
'''


import threading
import time

class Jogador_temp:
    """Objeto Jogador
    """
    def __init__(self, tipo_conexao):
        self.nome = "Jogador"
        self.cartasMao = []
        self.equipe = None
        self.ehRemoto = False
    
    def conectaJogador(self):
        pass




#JogadorThread
class JogadorBT(threading.Thread):
    def __init__ (self,conexao, hud, num):
        threading.Thread.__init__(self)
        self.nome = 'sem nome'
        self.numero = num
        self.conexao = conexao
        self.sock = None
        self.info = None
        self.hud = hud
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
        print self.info
        



    def envia_comando(self, cmd):
        self.socket.send(cmd)

    def recebe_comando(self):
        return self.socket.recv(1024)
    
    def desconecta(self):
        self.socket.close()
        print self.client_info, ": desconectado"
    
    


