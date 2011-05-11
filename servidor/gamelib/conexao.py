#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Jan 05, 2011

@author: Wander Jardim
'''

import threading, sys

import cocos
from cocos.text import Label
from bluetooth import *
from tile_layer import TileHandeler



class Conexao_old(threading.Thread):
    status= "Iniciando"
    event="Vazio"

    """
    def __init__(self, tipo_conexao):
        #super(Conexao, self).__init__()
        threading.Thread.__init__(self)
        
        self.socket = None
        self.conn = None
        self.addr = None
        self.event = None
        self.status = u'Iniciado'
        self.conexao = tipo_conexao
    """
    def run(self):
        if self.conexao == 'bluetooth':
            #socketBt = self.conexaoBluetooth()
            MyThread().start()
            
        elif self.conexao == 'gprs':
            #import gprs
            print "if é gprs"
        elif self.conexao == 'wireless':
            #import wireless
            print "if é wireless"
        return socketBt
        
        #self.run()






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
                          profiles = [SERIAL_PORT_PROFILE]
                          )



    def conectaJogador(self, socket):
        print "Aguardando conexão: "
        (client, addr) = socket.accept()
        return (client, addr)


    def recebe_comando(self):
        print "To esperando um comando"
        return self.socket.recv(1024)
        
        
    
    def envia_comando(self, cmd, jogador):
        """
            Recebe como parametro cmd = o comando a ser enviado
                                  jogador: instacia da thread jogador
        """
        jogador.envia_comando(cmd)


    def obtem_nome(self, endereco):
        return lookup_name(address=endereco)


    def iniciaServidor(self):
        """Inicia o servidor.
        """

        print "Aguardando conexao"
        
        print "Vai ser agora: "
        (client, addr) = self.conectaJogador(socket)
        #(client, addr) = socket.accept()
        
        self.conn = addr[0]
        self.hud.informaJogador(self.conn)
        try:
            cmd = None
            print " Conexao aceita:\n %s conectado" % addr[0]
            self.status = u'Conexao aceita:\n %s conectado' % addr[0]
            while True:
                
                msg = client.recv(1024)
                if not msg:
                    break
                else:
                    
                    if msg == 'g': 
                        self.event = 'goAhead'
                        self.status = u'goAhead'
                    elif msg == 's':
                        self.event = 'goTras'
                        self.status = u'goTras'
                        self.hud.mostraDessenhoTeste()
                    elif msg == 'l':
                        self.event = 'toLeft'
                        self.status = u'toLeft'
                    elif msg == 'r':
                        self.event = 'toRight'
                        self.status = u'toRight'
                    elif msg == 'x' or msg == '' or msg == 0:
                        self.hud.desconectaJogador()
                        print "Encerrando conexao!"
                        break
                    print msg
                    print self.event
            
            if socket:
                socket.close()

        except BluetoothError:
            print "Conexao finalizada: \n %s desconectado!" % addr[0]
            self.status = u'Conexao finalizada: \n %s desconectado!' % addr[0]
        except:
            print "Error Inesperado"
            self.status = u'Error Inesperado'


                


    def conexaoBluetooth(self):
        try:
            if sys.platform == 'win32':
                # se o S.O for Windows utiliza a biblioteca PyBluez
                import bluetooth
                self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.socket.bind(("",bluetooth.PORT_ANY))
                self.socket.listen(1)
                port = self.socket.getsockname()[1]
                uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
                bluetooth.advertise_service(self.socket, "PyTruco4S60 PyBluez",
                                            service_id = uuid,
                                            service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                                            profiles = [bluetooth.SERIAL_PORT_PROFILE],
                                            #protocols = [OBEX_UUID]
                                            )

            else:
                # Senão for Windows utiliza a biblioteca Lightblue
                import lightblue
                self.socket = lightblue.socket()
                self.socket.bind(("",0))
                self.socket.listen(1)
                lightblue.advertise("PyTruco4S60 lightblue", self.socket, lightblue.RFCOMM)


            self.status = u'Serviço Disponível'
            self.status = u'Aguardando uma Conexão lala....'
            self.conn, self.addr = self.socket.accept()
            self.status = u'Conectado!'
            print self.status, self.conn


            try:
                msg = self.conn.recv(1024)
            except Exception, erro:
                print erro 
                msg = 0
                self.status = u'Fechado'
                
            if msg == 'G': 
                self.event = 'goAhead'
                self.status = u'goAhead'
            elif msg == 'S':
                self.event = 'goTras'
                self.status = u'goTras'
            elif msg == 'L':
                self.event = 'toLeft'
                self.status = u'toLeft'
            elif msg == 'R':
                self.event = 'toRight'
                self.status = u'toRight'
            elif msg == 'x' or msg == '' or msg == 0:
                msg =0
                self.status = u'Fechado'
            print msg
            print self.event
        

        except Exception, erro:
            print erro
            self.status == 'Fechado'
            print self.status
        
        return msg


        while self.status != u'Fechado':
            self.recebeMensagem()

    
    def recebeMensagem(self):
        pass



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



