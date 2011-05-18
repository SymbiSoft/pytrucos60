#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Jan 05, 2011

@author: Wander Jardim
'''

import threading, sys

import cocos
#from cocos.text import Label
from bluetooth import *
#from tile_layer import TileHandeler



class ConexaoBT(): #threading.Thread):

    
    def __init__(self):
        self.conn = "Ninguem"
        self.addr = None
        self.event = None
        self.status = u'Iniciado'
        self.conexao = None
        self.socket = None


    def socket_servidor(self):
        """Cria um servidor Bluetooth com o socket RFCOMM ligado a um determinado canal.
        """
        self.socket = BluetoothSocket(proto=RFCOMM)
        self.socket.bind(("", PORT_ANY))
        self.socket.listen(1)
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        advertise_service(self.socket, "PyTruco4S60",
                          service_id = uuid,
                          service_classes = [ uuid, SERIAL_PORT_CLASS ],
                          profiles = [SERIAL_PORT_PROFILE])



    def conectaJogador(self, socket):
        print "Aguardando conexão: "
        (client, addr) = socket.accept()
        print addr
        print "  î Conectado!"
        return (client, addr)


    def recebe_comando(self):
        print "To esperando um comando"
        dados = self.socket.recv(1024)
        return dados
        
        
    
    def envia_comando(self, cmd, jogador):
        """
            Recebe como parametro cmd = o comando a ser enviado
                                  jogador: instacia da thread jogador
        """
        jogador.envia_comando(cmd)


    def obtem_nome(self, endereco):
        return lookup_name(address=endereco)




    def on_quit(self):
        msg = 0
        self.socket.close()
        print "Fechei Conexão!"

    def get_event(self):
        try:
            yield self.event
        except:
            pass

    @staticmethod
    def is_connected():
        return False



