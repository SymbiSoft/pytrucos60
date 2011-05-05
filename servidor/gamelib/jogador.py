#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Mar 03, 2011

@author: Wander Jardim
'''


import threading


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
class Jogador(threading.Thread):
    def __init__ (self,socket,client_info):
        threading.Thread.__init__(self)
        self.socket = socket
        self.client_info = client_info
        #self.quem = quem
        #self.isRunning = threading.Event()
        #self.isRunning.clear()

    def run(self):
        try:
            while True:
                self.socket.send('teste')
                data = self.socket.recv(1024)
                if len(data) == 0: break
                print self.client_info, ": recebido [%s]" % data
                self.socket.send(data)
                print self.client_info, ": enviado [%s]" % data
        except IOError:
            print "Deu urm erro aqui 123!"
        self.socket.close()
        print self.client_info, ": desconectado"
                
