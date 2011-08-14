#######################################################
# 
# jogadorWiFi.py
# Python implementation of the Class JogadorWiFi
# Generated by Enterprise Architect
# Created on:      29-jul-2011 23:10:50
# Original author: Wander Jardim
# 
#######################################################
import Jogador

class JogadorWiFi(Jogador, threading.Thread):
    def __init__ (self, conexao, num, hud):
        threading.Thread.__init__(self)
        self.conexao = conexao
        self.numero = num
        self.estahRodando = False
        self.hud = hud
        self.socket = None
        
    def run(self):
        self.conecta_jogadores()