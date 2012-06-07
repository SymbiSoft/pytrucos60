#######################################################
# 
# telaAguardaConexao.py
# Python implementation of the Class TelaAguardaConexao
# Generated by Enterprise Architect
# Created on:      29-jul-2011 20:10:58
# Original author: Wander Jardim
# 
#######################################################

from cocos.layer import *


class TelaAguardaConexao(Layer):
    def __init__(self, tipo_conexao):
        super( TelaConexoes, self).__init__()
        
        self.nrJogadores=0
        self.tipo_conexao = tipo_conexao
        self.partidaIniciada = False
        self.jogadores = []
        
        print "tipo de conexao => %s " % self.tipo_conexao
        
        # Configurando camadas
        # HUD
        self.hud = Hud(self)
        
        self.add(self.hud, z=-1)
        
        
        self.titulo = Label("Aguardando conexao", font_name='Times New Roman',
            font_size=23,
            x=30, y=600,
            anchor_x='left', anchor_y='top')
        
        
        self.add(self.titulo)
        
        
        if self.tipo_conexao == 'bluetooth':
            self.conexao = ConexaoBT()
            self.conexao.socket_servidor()
            threadConexao = Thread( target=self.conecta_jogadoresBT)
            threadConexao.start()
        else:
            socket = None

    def conecta_jogadoresBT(self):
        nrJogador = 0
        while not self.partidaIniciada:
            
            self.jogadores.append(JogadorBT(self.conexao, nrJogador, self.hud))
            self.jogadores[nrJogador].setDaemon(True)
            self.jogadores[nrJogador].start()
            print self.jogadores[nrJogador]
            time.sleep(1)
            
            try:
                while not self.jogadores[nrJogador].conectou():
                    if self.partidaIniciada:
                        print "Abortou conexao!!"
                        break
                
                self.jogadores[nrJogador].conectou()
            except IndexError:
                pass
            else:
                if self.jogadores[nrJogador].conectou():
                    time.sleep(1)
                    print "Jogador %s Conectado!!!" % self.jogadores[nrJogador].nome
                    self.jogadores[nrJogador].envia_comando("cmd:jogadoresconectado")
                    print  self.jogadores[nrJogador].recebe_comando()
                    
                    cmd = ''
                    for jogador in self.jogadores:
                        cmd += jogador.nome + ':' + str(jogador.numero) + "|"
                    self.jogadores[nrJogador].envia_comando("%s"%cmd)
                    for jogador in self.jogadores:
                        jogador.envia_comando("jogadorcnt:%s:%s" % (self.jogadores[nrJogador].nome, nrJogador))
                    
                nrJogador+=1
                
                if len(self.jogadores)==4:
                    self.partidaIniciada = True
            
            
            
    def obtemJogadores(self):
        return self.jogadores
        

    def montaMenuIniciaPartida(self):
        pass

        
        
        