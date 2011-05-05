#-*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Created on Jan 05, 2011

@author: Wander Jardim
'''

import threading, sys

import cocos
from cocos.text import Label

from tile_layer import TileHandeler

class Conexao(threading.Thread):

    def __init__(self, tipo_conexao):
        #super(Conexao, self).__init__()
        threading.Thread.__init__(self)
        
        self.socket = None
        self.conn = None
        self.addr = None
        self.event = None
        self.status = u'Iniciado'
        self.conexao = tipo_conexao
    
    def run(self):
        if self.conexao == 'bluetooth':
            self.conexaoBluetooth()
        elif self.conexao == 'gprs':
            #import gprs
            print "if é gprs"
        elif self.conexao == 'wireless':
            #import wireless
            print "if é wireless"

        
        #self.run()

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
                bluetooth.advertise_service(self.socket, "PyTruco4S60 cocos2d PyBluez",
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
                lightblue.advertise("PyTruco4S60 cocos2d", self.socket, lightblue.RFCOMM)
                    
            self.status = u'Aguardando uma Conexão....'
            
            #self.statusLay = Label(self.status, font_name='Times New Roman',
            #font_size=16,
            #x=100, y=500,
            #anchor_x='center', anchor_y='center')
            #self.add(self.statusLay)
            
            print self.status
            self.conn, self.addr = self.socket.accept()
            self.status = u'Conectado!'
            
            #self.statusLay = Label(self.status, font_name='Times New Roman',
            #font_size=16,
            #x=100, y=500,
            #anchor_x='center', anchor_y='center')
            #self.add(self.statusLay)
            
            print self.status, self.conn
        
        except Exception, erro:
            print erro
            self.status == 'Fechado'
            print self.status
        #msg = 1
        while self.status != u'Fechado':
            self.recebeMensagem()
    
    def recebeMensagem(self):
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



