#-*- coding: utf-8 -*-
# Author: Wander Jardim
# email: wanderjardim@gmail.com
#        Copyright 2011
# About: The main application class, will hold event processing
# code as also objects to represent windows.
# TODO:
# 
# 
# 



'''
/*  Copyright (C) 2011  Wander Jardim <wanderjardim@gmail.com>
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; by version 2 of the License.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */
'''


import appuifw
import e32
from threading import Thread
import traceback

from configure import *

from menu import *
from btclient import BluetoothError
import btclient 

from constantes import *

class Game:
    background = None
    help_screen = None
    bt = None
    keyboard = None
    configuracao = None
    img = None
    def __init__(self, app_path):
        self.path = app_path
        self.current_stateMenu = "splash"
        appuifw.app.title = u'PyTruco4S60'
        appuifw.app.exit_key_handler = self.quit
        self.largura_tela,self.altura_tela = self.screen_size()
        self.configuracao = configure(self.path)
        self.conexao = None
        

        #definindo o orientação da tela como paisagens, ou seja a teal deitada.
        appuifw.app.orientation = 'landscape'
        #Verificando a versão do pys60 instalada para saber se oferece suporte ao touch e desabilitando o joystick.
        if e32.pys60_version_info > (1,9):
            appuifw.app.directional_pad = False
            if appuifw.touch_enabled():
                appuifw.app.screen= 'large'  # self.configuracao.pref['game_screen']
                TOUCH_ENABLED = True
            else:
                appuifw.note(u"Touch screen nao encontrado", "error")

        self.running = 0
        self.canvas=appuifw.Canvas(event_callback=self.callback,
               redraw_callback=lambda rect:self.draw_stateMenu(self.current_stateMenu))
        
        appuifw.app.body = self.canvas
        
        
        
        self.reset()
        
    #Redefini a aplicação ao seu estado inicial
    def reset(self, jaRodou=0):
        #Definindo o titulo da aplicação
        if jaRodou:
            self.running = 0
            self.canvas=appuifw.Canvas(event_callback=self.callback,
                                       redraw_callback=lambda rect:self.draw_stateMenu(self.current_stateMenu))
            appuifw.app.body = self.canvas
        appuifw.app.title=unicode(self.configuracao.pref['titulo_jogo'])
        
        self.running = 0
        
        self.menu = menu(self.path+'\\imgs', self.current_stateMenu)
        self.desenha_splash()
        self.current_stateMenu = 'menu'
        self.carrega_menu()
        
        appuifw.app.body = self.canvas
        
        self.running = self.menu.running


    def carrega_menu(self):
        
        tela_menu =self.menu.desenha_menu()
        self.canvas.blit(tela_menu) # mostra a imagem na tela
        
        # bind the tapping areas
        for i in range(len(self.menu.touch['buttons'])):
            self.canvas.bind(key_codes.EButton1Down, self.touch_down_menu_cb, self.menu.touch['buttons'][i] )
            self.canvas.bind(key_codes.EButton1Up, self.touch_up_menu_cb, self.menu.touch['buttons'][i] )

    def callback(self, event):
        # Criado para manipular eventos
        #print event
        self.draw_stateMenu(self.current_stateMenu)



    def draw_stateMenu(self, current_stateMenu):
        """Desenha a tela da seleção atual"""
        self.current_stateMenu = current_stateMenu
        if self.current_stateMenu == 'menu':
            self.carrega_menu()
            #appuifw.note(u"Menu", "info")
        elif self.current_stateMenu == 'jogar':
            #self.jogar()
            try:
                jogo = Jogar()
                jogo.conexoes()
                appuifw.note(u"passei de jogo.conexoes" , "info")
                self.running = jogo.running
            except Exception, exc:
                open("E:\\Python\\pytruco\\Meu_error.log", "w").write(traceback.format_exc())
                raise
            #appuifw.note(u"Jogar", "info")

        elif self.current_stateMenu == 'conexao':
            self.conexoes()
            #appuifw.note(u"Conexão", "info")

        elif self.current_stateMenu == 'opcoes':
            self.opcoes()
            #appuifw.note(u"Opções", "info")
        elif self.current_stateMenu == 'creditos':
            self.creditos()
            #appuifw.note(u"Créditos", "info")
        elif self.current_stateMenu == 'instrucoes':
            self.instrucoes()
            #appuifw.note(u"Instruções", "info")
        elif self.current_stateMenu == 'sair':
            self.quit()
            #appuifw.note(u"Sair", "info")



    def desenha_splash(self):
        tela_splash = Image.new((self.largura_tela,self.altura_tela))
        mascaraSplash = Image.new((self.largura_tela,self.altura_tela), 'L')
        for i in range(0,26):
            fond=0
            texte=(10*i)
            #texte=255-(10*i)
            mascaraSplash.clear((texte,texte,texte))
            tela_splash.clear((fond,fond,fond))
            tela_splash.blit(self.menu.splash,mask=mascaraSplash)
            self.canvas.blit(tela_splash) # mostra a imagem na tela
            e32.ao_sleep(0.06)
        e32.ao_sleep(0.5)
        #self.draw_stateMenu('menu')




    def opcoes(self): 
        appuifw.note(u"Função Opções", "error")
        self.current_stateMenu = 'menu'

    
    def creditos(self):
        import creditos
        creditos = creditos.Creditos()
        tela_creditos = creditos.desenha_tela(self.menu.touch, self.current_stateMenu)
        self.canvas.blit(tela_creditos) # mostra a imagem na tela
        
        #bind the tapping areas
        for i in self.menu.touch['buttons']:
            self.canvas.bind(key_codes.EButton1Down, self.touch_down_creditos_cb, i )
            self.canvas.bind(key_codes.EButton1Up, self.touch_up_creditos_cb, i )
        #self.current_stateMenu = 'menu'

    def touch_down_creditos_cb(self, pos=(0, 0)):
        "detecta qual butão foi pressionado"
        if self.menu.touch.has_key('buttons'):
            for i in range(len(self.menu.touch['buttons'])):
                if self.tocou_no_botao(pos, self.menu.touch['buttons'][i]):
                    self.menu.touch['down'] = i
                    break

    def touch_up_creditos_cb(self, pos=(0, 0)):
        if self.menu.touch.has_key('down'):
            if self.menu.touch['down'] == 0:
                self.current_stateMenu = 'menu'
                #self.draw_stateMenu()

            del self.menu.touch['down']



    def instrucoes(self):
        print "To em instrucoes!!!"
        self.current_stateMenu = 'menu'




    def touch_down_menu_cb(self, pos=(0, 0)):
        if self.tocou_no_botao(pos, self.menu.touch['buttons'][0]) :
            self.menu.touch['main_down'] = 'jogar'
        elif self.tocou_no_botao(pos, self.menu.touch['buttons'][1]) :
            self.menu.touch['main_down'] = 'conexao'
        elif self.tocou_no_botao(pos, self.menu.touch['buttons'][2]):
            self.menu.touch['main_down'] = 'opcoes'
        elif self.tocou_no_botao(pos, self.menu.touch['buttons'][3]) :
            self.menu.touch['main_down'] = 'creditos'
        elif self.tocou_no_botao(pos, self.menu.touch['buttons'][4]) :
            self.menu.touch['main_down'] = 'instrucoes'
        elif self.tocou_no_botao(pos, self.menu.touch['buttons'][5]) :
            self.menu.touch['main_down'] = 'sair'

    def touch_up_menu_cb(self, pos=(0, 0)):
        if self.menu.touch.has_key('main_down'):
            if self.menu.touch['main_down'] == 'jogar':
                self.current_stateMenu = 'jogar'
                self.draw_stateMenu(self.current_stateMenu)
            elif self.menu.touch['main_down'] == 'conexao':
                self.current_stateMenu = 'conexao'
                self.draw_stateMenu(self.current_stateMenu)
            elif self.menu.touch['main_down'] == 'opcoes':
                self.current_stateMenu = 'opcoes'
                self.draw_stateMenu(self.current_stateMenu)
            elif self.menu.touch['main_down'] == 'creditos':
                self.current_stateMenu = 'creditos'
                self.draw_stateMenu(self.current_stateMenu)
            elif self.menu.touch['main_down'] == 'instrucoes':
                self.current_stateMenu = 'instrucoes'
                self.draw_stateMenu(self.current_stateMenu)
            elif self.menu.touch['main_down'] == 'sair':
                self.current_stateMenu = 'sair'
                self.draw_stateMenu(self.current_stateMenu)

            del self.menu.touch['main_down']


    def tocou_no_botao(self,pos, button):
        if  pos[0] >= button[0][0] and pos[0] <  button[1][0]\
        and pos[1] >= button[0][1] and pos[1] <  button[1][1]:
            return True

        return False

    #Função Auxiliar, retorna o tamanho da tela
    def screen_size(self):
        return sysinfo.display_pixels()


        




# *******Inicio****** To vendo agora sobre canvas - em 28/04/11 **************







    def jogar(self):
        #appuifw.note(u"Inicia a pardida", "info")
        #self.current_stateMenu = 'menu'
        #prepare canvas for drawing
        #
        
        #self.canvas=appuifw.Canvas(event_callback=None, #self.callbackJogo,
        #                           redraw_callback=lambda rect:self.draw_stateJogo(self.current_stateJogo))
        
        self.cont = 0
        self.canvas = appuifw.Canvas(event_callback = None,
                                     redraw_callback = self.event_redraw)
        
        appuifw.app.body = self.canvas
        
        appuifw.app.exit_key_handler = self.quit
        
        self.current_stateJogo = 'teste'
        self.conexoes()
        #appuifw.note(u"Inicia a pardida", "info")
        
        
        
        #self.tela_aguarda_conexoes()


    def conexoes(self): 
        opcoes_conexoes = [u"Bluetooth", u"WI-FI", u"GPRS", u"Voltar"]
        conexaoEscolhida = appuifw.popup_menu(opcoes_conexoes, u"Tipo de conexão")
        if conexaoEscolhida == 0:
            try:
                print "vai comecar a conexao:"
                self.conexao = btclient.BluetoothClient()
                print "outra linha de conexao"
                self.connectBT()
                print "socket dentro de conexoes:"
                print self.conexao.socket
                print "passei pela conexao:"
                self.current_stateJogo = 'conectado'
                print "Vou chamar tela_aguarda_conexoes()"
                
                self.conexao.send_command("Entrei no Jogooo!! wander - 1")
                self.tela_aguarda_conexoes("Dentro de cnx")
            except Exception, exc:
                open("E:\\Python\\errorTestAplic.log", "w").write(traceback.format_exc())
                raise
            #appuifw.note(u"Vou me conectar por Bluetooth" , "info")
            #self.desenha_botoes()

            print "Falow, Abraço!!"

        elif conexaoEscolhida == 1:
            #wifi()
            appuifw.note(u"Vou me conectar por wifi" , "info")
        elif conexaoEscolhida == 2:
            #gprs()
            appuifw.note(u"Vou me conectar por gprs" , "info")
        elif conexaoEscolhida == 3:
            self.current_stateMenu = 'menu'
            #self.draw_stateMenu()
        del conexaoEscolhida


            #self.desconectar()

    def draw_stateJogo(self, current_stateJogo):
        """Desenha a tela da seleção atual"""
        self.current_state = current_stateJogo
        if self.current_state == 'teste':
            self.event_redraw()
        elif self.current_stateJogo == 'conectado':
            self.tela_aguarda_conexoes()
            
            #self.jogar()


    def callbackJogo(self, event):
        # Criado para manipular eventos
        #print event
        self.draw_stateJogo(self.current_stateJogo)

    
    def tela_aguarda_conexoes(self, controle=None):
        self.cont
        print "To dentro de tela_aguarda_conexoes()"
        self.canvas.clear()
        lado1 = self.largura_tela/3
        lado2 = self.altura_tela/5
        myscreen = Image.new((self.largura_tela,self.altura_tela))
        myscreen.clear((15,126,0))
        
        if controle:
            myscreen.text((lado1-10,lado2+140), u"Chamada direta: %s" % controle , fill = RGB_RED,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))  
            self.canvas.blit(myscreen)
        
        myscreen.text((lado1,lado2), u"Aguardando Jogadores", fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))  
        print "passei por aki t_a_c"
        
        #Texto de controde de vezes q passa
        myscreen.text((lado1,lado2+120), u"Essa é a %s vez que passo aki" % self.cont, fill = RGB_RED,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))  
        self.canvas.blit(myscreen)
        self.cont += 1
        
        if self.conexao.is_connected():
            # Retangulo Vermelho - DRAG Event
            '''Desenha um retangulo vermelho e o texto'''
            myscreen.rectangle(((5,10+lado2), (5+lado1,(2*lado2)+10)), fill=RGB_RED, width=5)
            myscreen.text((20,lado2+45), u"Desconectar", fill = RGB_BLACK,font=(u'Nokia Hindi S60',10,appuifw.STYLE_BOLD))  
            '''Vincula a função DRAG ao retangulo vermelho'''
            self.canvas.bind(key_codes.EButton1Up, self.desconectar, ((5,10+lado2), (5+lado1,(2*lado2)+10)))
            
            # Retangulo Lilas - TAP Event
            '''Desenha um retangulo lilaz e o texto'''
            myscreen.rectangle(((10+lado1,10+lado2), (10+2*lado1,(2*lado2)+10)), fill=RGB_PURPLE, width=5)
            myscreen.text((20+lado1,lado2+45), u"Mandar msg", fill = RGB_BLACK,font=(u'Nokia Hindi S60',10,appuifw.STYLE_BOLD))  
            '''Vincula a função TAP ao retangulo Lilas'''
            self.canvas.bind(key_codes.EButton1Up, self.enviaPosicao, ((10+lado1,10+lado2), (10+2*lado1,(2*lado2)+10)))

            
            self.canvas.blit(myscreen)
        
        
        pos = 115
        while self.conexao.is_connected():
            print "aguardando o comando"
            myscreen.text((lado1+10,lado2+130), u"Aguardando um comando", fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
            self.canvas.blit(myscreen)
            
            self.conexao.send_command("Entrei no Jogooo!! wander - 2")
            data = self.conexao.recebe_comando()
            print "Vou imprimir o q recebi: %s" % data
            myscreen.text((lado1+10,lado2+pos), u"%s" % data, fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
            self.canvas.blit(myscreen)
            pos += 15
            #appuifw.note(u"%s" % data)


    def desenha_botoes(self):
        self.canvas.clear()
        lado1 = self.largura_tela/3
        lado2 = self.altura_tela/5
        
        myscreen = Image.new((self.largura_tela,self.altura_tela))
        myscreen.clear((15,126,0))

        # Retangulo Lilas - TAP Event
        '''Desenha um retangulo lilaz e o texto'''
        myscreen.rectangle(((10+lado1,10+lado2), (10+2*lado1,(2*lado2)+10)), fill=RGB_PURPLE, width=5)
        myscreen.text((20+lado1,lado2+45), u"Mandar msg", fill = RGB_BLACK,font=(u'Nokia Hindi S60',10,appuifw.STYLE_BOLD))  
        '''Vincula a função TAP ao retangulo Lilas'''
        self.canvas.bind(key_codes.EButton1Up, self.enviaPosicao, ((10+lado1,10+lado2), (10+2*lado1,(2*lado2)+10)))

        # Retangulo Azul - Evento DOWN
        '''Desenha um retangulo azul e o texto'''
        myscreen.rectangle(((5,5), (5+lado1,5+lado2)), fill=RGB_BLUE, width=5)
        myscreen.text((20,40), u"Envia texto", fill = RGB_BLACK,font=(u'Nokia Hindi S60',10,appuifw.STYLE_BOLD)) 
        '''Vincula a função DOWN ao retangulo azul'''
        self.canvas.bind(key_codes.EButton1Down, self.enviaTexto, ((5,5), (lado1,lado2)))

        # Retangulo Vermelho - DRAG Event
        '''Desenha um retangulo vermelho e o texto'''
        myscreen.rectangle(((5,10+lado2), (5+lado1,(2*lado2)+10)), fill=RGB_RED, width=5)
        myscreen.text((20,lado2+45), u"Desconectar", fill = RGB_BLACK,font=(u'Nokia Hindi S60',10,appuifw.STYLE_BOLD))  
        '''Vincula a função DRAG ao retangulo vermelho'''
        self.canvas.bind(key_codes.EDrag, self.desconectar, ((5,10+lado2), (5+lado1,(2*lado2)+10)))
        
        self.canvas.blit(myscreen) # show the image on the screen

        while self.conexao.is_connected():
            data = self.conexao.recebe_comando()
            appuifw.note(u"%s" % data)

    def enviaPosicao(self, event):
        self.conexao.send_command(str(event))


    def desconectar(self, event):
        txtDescon = "sair"
        print txtDescon
        self.conexao.send_command(txtDescon)
        self.disconnect()
        
        #self.canvas.clear()
        #self.reset()

    def enviaTexto(self, event):
        txtEnviar = "s"
        self.conexao.send_command(txtEnviar)


    #Redraw function, used as a callback for canvas events.
     

    def event_redraw(self, other):
        
        #self.desenha_botoes()
        #self.tela_aguarda_conexoes()
        print "event_redraw"
        """
        try:
            if self.conexao.is_connected():
                self.tela_aguarda_conexoes()
                
            print "Ta conectado?"
            print self.conexao.is_connected()
            print "Tem certeza??"
            print self.conexao.socket
                
        except:
        """
        self.canvas.clear()
        lado1 = self.largura_tela/3
        lado2 = self.altura_tela/5
        myscreen = Image.new((self.largura_tela,self.altura_tela))
        myscreen.clear((15,126,0))
        self.canvas.blit(myscreen)
        #print "event_redraw except"
        print other
        
        try:
            teste = self.conexao.is_connected()
            self.tela_aguarda_conexoes()
        except:
            print "event_redraw except"
            
        
        



# *******/Fim****** To vendo agora sobre canvas - em 28/04/11 *****************




# Retirado por conta do teste -> To vendo agora sobre canvas  - em 28/04/11 **
    def conexoes_old(self): 
        opcoes_conexoes = [u"Bluetooth", u"WI-FI", u"GPRS", u"Voltar"]
        conexao = appuifw.popup_menu(opcoes_conexoes, u"Tipo de conexão")
        if conexao == 0:
            try:
                self.conexao = btclient.BluetoothClient()
                self.connectBT()
            except Exception, exc:
                open("E:\\Python\\pytruco\\Meu_error.log", "w").write(traceback.format_exc())
                raise
            #appuifw.note(u"Vou me conectar por Bluetooth" , "info")
            while True:
                msg = raw_input('Digite aki ->>> ')
                if len(msg) == 0 or msg == 'x': 
                    self.conexao.send_command(msg)
                    print "Tchauuu!"
                    break
                self.disconnect()
                print msg

            print "Falow, Abraço!!"
            self.disconnect()




            
        elif conexao == 1:
            #wifi()
            appuifw.note(u"Vou me conectar por wifi" , "info")
        elif conexao == 2:
            #gprs()
            appuifw.note(u"Vou me conectar por gprs" , "info")
        elif conexao == 3:
            self.current_stateMenu = 'menu'
            #self.draw_stateMenu()
        del conexao


    def disconnect(self):
        """Disconnects from the server.
        """
        try:
            self.conexao.close()
            if self.conexao:
                print "ainda tinha o socket: %s" % self.conexao
                del self.conexao
        except BluetoothError, e:
            appuifw.note(e.msg, "error")



    def connectBT(self):
        """Conecta ao servidor.
        """
        try:
            self.conexao.connect()
            print "socket dentro de connectBT:"
            print self.conexao.socket
        except BluetoothError, e:
            appuifw.note(u"Erro na execução do Bluetooth %s"%e, "error")




    #Exit function
    def quit(self):
        print "Sairrrr"
        self.running = -1
        if self.conexao != None:
            print u'EXIT'
            self.conexao.send_command(u'CONN_CLOSE')
            self.conexao.close()
        #lock = e32.Ao_lock() 
        #self.lock.signal()
        #appuifw.app.set_exit() #TODO:Voltar essa linha quando for compilar para SIS.




class Jogar:
    def __init__(self):
        self.cont = 0
        self.render=0
        self.running = 0
        self.largura_tela,self.altura_tela = self.screen_size()
        self.myscreen = Image.new((self.largura_tela,self.altura_tela))
        self.canvas = appuifw.Canvas(event_callback = None,
                                     redraw_callback = self.event_redraw)
        
        appuifw.app.body = self.canvas
        appuifw.app.exit_key_handler = self.quit
        self.render=1


    def conexoes(self): 
        opcoes_conexoes = [u"Bluetooth", u"WI-FI", u"GPRS", u"Voltar"]
        conexaoEscolhida = appuifw.popup_menu(opcoes_conexoes, u"Tipo de conexão")
        if conexaoEscolhida == 0:
            try:
                self.conexao = btclient.BluetoothClient()
                self.connectBT()
                self.current_stateJogo = 'conectado'            
                self.tela_aguarda_conexoes()
            except Exception, exc:
                open("E:\\Python\\errorTestAplic.log", "w").write(traceback.format_exc())
                raise

        elif conexaoEscolhida == 1:
            #wifi()
            appuifw.note(u"Vou me conectar por wifi" , "info")
        elif conexaoEscolhida == 2:
            #gprs()
            appuifw.note(u"Vou me conectar por gprs" , "info")
        elif conexaoEscolhida == 3:
            self.current_stateMenu = 'menu'
            #self.draw_stateMenu()
        del conexaoEscolhida


    def connectBT(self):
        """Conecta ao servidor.
        """
        try:
            self.conexao.connect()
            print "socket dentro de connectBT:"
            print self.conexao.socket
        except BluetoothError, e:
            appuifw.note(u"Erro na execução do Bluetooth %s"%e, "error")



    def tela_aguarda_conexoes(self):
        self.cont += 1
        #self.canvas.clear()
        lado1 = self.largura_tela/3
        lado2 = self.altura_tela/5
        #self.myscreen = Image.new((self.largura_tela,self.altura_tela))
        #self.myscreen.clear((15,126,0))
        
        self.myscreen.text((lado1,lado2), u"Aguardando Jogadores", fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))  
        #Texto de controde de vezes q passa
        self.myscreen.text((10,40), u"Essa é a %s vez que passo aki" % self.cont, fill = RGB_RED,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))  
        self.canvas.blit(self.myscreen)      
        if self.conexao.is_connected():
            pos = 115
            #self.conexao.send_command("cmd:qtdJogador")
            while True:
                self.myscreen.text((lado1,3*lado2), u"Aguardando comando:", fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
                self.myscreen.text((lado1-10,4*lado2), u"Comando Recebido!!", fill = (15,126,0),font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
                self.canvas.blit(self.myscreen)
                data = self.conexao.recebe_comando()
                self.myscreen.text((lado1,3*lado2), u"Aguardando comando:", fill = (15,126,0),font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
                self.myscreen.text((lado1-10,4*lado2), u"Comando Recebido!!", fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
                self.canvas.blit(self.myscreen)
                if data == '':
                    break
                elif data=='cmd:jogadoresconectado':
                    self.conexao.send_command("OK:jogadoresconectado")
                    cmd = self.conexao.recebe_comando()
                    infoJogadores = cmd.split('|')
                    self.mostraJogadoresConectados(infoJogadores)
                elif data.startswith('jogadorcnt:'):
                    dadosJogadorConectado = data.split(':')
                    self.desenhaNomeJogador(dadosJogadorConectado[1],dadosJogadorConectado[2])
                elif data.startswith('jogadorcpucnt:'):
                    self.conexao.send_command("OK:jogadorcpucnt")
                    dadosJogadorCPU = data.split(':')
                    self.desenhaNomeJogador(dadosJogadorCPU[1],dadosJogadorCPU[2])
                elif data=='iniciaPartida':
                    self.iniciaPartica()
                else:
                    print "Vou imprimir o q recebi: %s" % data
                    #self.log_file.write("Vou imprimir o q recebi: %s\n" % data)
                    self.myscreen.text((lado1+10,lado2+pos), u"Recebi: %s" % data, fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
                    self.canvas.blit(self.myscreen)
                pos += 15
                    #appuifw.note(u"%s" % data)


    def mostraJogadoresConectados(self, infoJogadores):
        pos = 0
        for infoJogador in infoJogadores:
            dadosJogador = infoJogador.split(':')
            if dadosJogador!= ['']: 
                self.desenhaNomeJogador(dadosJogador[0], dadosJogador[1])
            
            
            

    def desenhaNomeJogador(self, nome, pos):
        bordaDir = self.largura_tela - 190
        bordaEsq = 30
        bordaTop = 30
        bordaPe = self.altura_tela - 30
        meioH = self.largura_tela / 2
        meioV = self.altura_tela / 2
        
        if pos == '0':
            self.myscreen.text((meioH, bordaPe), u"%s" % nome, fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
        elif pos =='1':
            self.myscreen.text((bordaEsq,meioV), u"%s" % nome, fill = RGB_BLUE,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
        elif pos == '2':
            self.myscreen.text((meioH,bordaTop), u"%s" % nome, fill = RGB_RED,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
        elif pos =='3':
            self.myscreen.text((bordaDir,meioV), u"%s" % nome, fill = RGB_PURPLE,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
        
        self.canvas.blit(self.myscreen)
            


    def event_redraw(self, other):
        print "event_redraw"
        if self.render == 0:
            self.canvas.clear()
            lado1 = self.largura_tela/3
            lado2 = self.altura_tela/5
            
            self.myscreen.clear((15,126,0))
            self.canvas.blit(self.myscreen)
        try:
            teste = self.conexao.is_connected()
            self.tela_aguarda_conexoes()
        except Exception, exc:
            open("E:\\Python\\pytruco\\Meu_error.log", "w").write(traceback.format_exc())
            print "event_redraw except"


    #TODO:
    def iniciaPartica(self):
        meioH = self.largura_tela / 2
        meioV = self.altura_tela / 2
        #self.canvas.clear()
        self.myscreen.clear((253,126,0))
        self.myscreen.text((meioH, meioV), u"Vai começar a Jogatina", fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
        self.canvas.blit(self.myscreen)



    def enviaPosicao(self, event):
        self.conexao.send_command(str(event))


    def desconectar(self, event):
        txtDescon = "sair"
        print txtDescon
        self.conexao.send_command(txtDescon)
        self.disconnect()


    def disconnect(self):
        """Disconnects from the server.
        """
        try:
            self.conexao.close()
            if self.conexao:
                print "ainda tinha o socket: %s" % self.conexao
                #self.log_file.write("ainda tinha o socket: %s\n" % self.conexao)
                del self.conexao
        except BluetoothError, e:
            appuifw.note(e.msg, "error")



    #Exit function
    def quit(self):
        print "Sairrrr"
        self.running = -1
        if self.conexao != None:
            print u'EXIT'
            #self.log_file.write("EXIT\n")
            self.conexao.send_command(u'sair')
            self.conexao.close()
            #self.log_file.close() 
        


    #Função Auxiliar, retorna o tamanho da tela
    def screen_size(self):
        return sysinfo.display_pixels()
