#-*- coding: utf-8 -*-
import appuifw
from graphics import Image
import e32
import sys
import os
import key_codes


PYTRUCOS60_UID = u"ef080808"

PYTRUCOS60_PATH1 = "\\Python\\"
PYTRUCOS60_PATH2 = "\\Data\\python\\"
PYTRUCOS60_PATH3 = "\\Private\\ef0b4099\\"

def get_path(app_name):
    drives_list = e32.drive_list()
    #Gives preference to load from drive 'E:'
    drives_list.reverse()
    for drive in [str(x) for x in drives_list]:
        if os.path.isfile(os.path.join(drive, PYTRUCOS60_PATH1, app_name)):
            return os.path.join(drive, PYTRUCOS60_PATH1)
        elif os.path.isfile(os.path.join(drive, PYTRUCOS60_PATH2, app_name)):
            return os.path.join(drive, PYTRUCOS60_PATH2)
        elif os.path.isfile(os.path.join(drive, PYTRUCOS60_PATH3, app_name)):
            return os.path.join(drive, PYTRUCOS60_PATH3)
    return None


full_path = get_path('testeTelaCartas.py') 
if full_path == None:
    full_path = get_path('testeTelaCartas.py')
    if full_path == None:
        appuifw.note(u'Usando fallback path')
        full_path = u'C:\\' + u'Private' + u'\\' + PYTRUCOS60_UID + u'\\'

sys.path.append(os.path.join(full_path, "gamelib"))
arq_log = open(os.path.join(full_path,'Meu_error2.log'), 'w')
arq_log.close()


import util
from constantes import *


# disable directional pad
appuifw.app.directional_pad = False



class Carta(object):
    def __init__(self, pos_mesa, source, pos_marca_selecao, valor):
        self.posicao_mesa = pos_mesa
        self.rect = (self.posicao_mesa, (self.posicao_mesa[0]+LARGU_CARTA, self.posicao_mesa[1]+ALTUR_CARTA))
        self.source = source
        self.pos_marca_selecao = pos_marca_selecao
        self.imagem = Image.new((LARGU_CARTA,ALTUR_CARTA))
        self.valor = valor
        self.marcada = False
        self.selecionada = False
    
    




class Jogo:
    def __init__(self):
        appuifw.app.orientation = 'landscape'
        file_erro = open('E:\\Python\\Meu_error2.log', 'r+')
        self.largura_tela, self.altura_tela = util.getTamanho_tela()
        self.render = 0
        self.telajogo = Image.new((self.largura_tela,self.altura_tela))
        self.espacoCartas = None
        
        appuifw.app.exit_key_handler = self.quit
        appuifw.app.title = u"Teste tela Cartas"
        #Verificando a versão do pys60 instalada para saber se oferece suporte ao touch e desabilitando o joystick.
        if e32.pys60_version_info > (1,9):
            appuifw.app.directional_pad = False
            if appuifw.touch_enabled():
                appuifw.app.screen= 'full' #'large' #
                TOUCH_ENABLED = True
            else:
                appuifw.note(u"Touch screen nao encontrado", "error")
        
        
        self.matrizCartas = util.cria_imagem('cartasteste.png')

                

               

        #variavel de teste para simular os valores das cartas recebiba pelo bluetooth:
        self.cartas_recebidas = ['3e', '2e', 'ac']
        #Criando as cartas:
        self.cartas = []
        for i in range(len(self.cartas_recebidas)):
            self.cartas.append(Carta(posCartas[i], dictCartas[self.cartas_recebidas[i]], posCartasSelec[i], self.cartas_recebidas[i]))
        
        self.canvas = appuifw.Canvas(event_callback = self.handle_event,
                                     redraw_callback = self.handle_redraw)
        appuifw.app.body = self.canvas
        self.render = 1

        self.fundoMesa = util.cria_imagem('fundoMesa.png')
        rect_bot_sair = ((608, 336),(624, 350)) 
        self.fundoMesa.rectangle(rect_bot_sair, outline=RGB_BLUE, width=1)
        self.canvas.bind(key_codes.EButton1Up, self.quit, rect_bot_sair)
        
        espacoCartas = util.cria_imagem('espacoCartas.png')
        self.espacoCartas = Image.new(espacoCartas.size) #espacoCartas.size)
        self.maskCartas = Image.new(espacoCartas.size, 'L') #tons de cinza 8-bits
        self.maskCartas.blit(espacoCartas)
        
        self.telajogo.blit(self.fundoMesa)
        self.canvas.blit(self.telajogo)
        
        #Botão Descartar
        rect_botao_descartar = ((514,106),(628,197))
        self.canvas.bind(key_codes.EButton1Down, self.descartar, rect_botao_descartar)
        self.desenhaCartas()



    def desenhaCartas(self):
        #mask = util.cria_imagem('mascaraCartas.png')
        #self.maskCarta = Image.new(mask.size, 'L') #tons de cinza 8-bits
        #self.maskCarta.blit(mask) 
        for carta in self.cartas:
            self.carregaCarta(carta)
            self.canvas.blit(carta.imagem, target = carta.posicao_mesa)
            #self.canvas.bind(key_codes.EButton1Up, self.seleciona_carta, carta.rect)
            #self.canvas.bind(key_codes.EButton1Down, self.deseleciona_carta, carta.rect)        
            



    def carregaCarta(self, carta):
        carta.imagem.blit(self.matrizCartas, target=(0, 0), source=carta.source)


    def tocou_na_carta(self, pos, carta):
        if  pos[0] >= carta[0][0] and pos[0] <  carta[1][0]\
        and pos[1] >= carta[0][1] and pos[1] <  carta[1][1]:
            return True
        return False
        
    
    def deseleciona_carta(self, pos):
        for carta in self.cartas:
            if self.tocou_na_carta(pos, carta.rect):
                self.espacoCartas.clear(0)
                if carta.marcada:
                    self.espacoCartas.rectangle(carta.pos_marca_selecao, outline=RGB_RED, width=3, fill=RGB_RED)
                    self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)
            else:
                carta.marcada = False
        
    def seleciona_carta(self, pos):
        ''' Seleciona carta '''
        for i in range(len(self.cartas)):
            if self.tocou_na_carta(pos, self.cartas[i].rect):
                self.espacoCartas.clear(0)
                if self.cartas[i].selecionada:
                    self.espacoCartas.rectangle(self.cartas[i].pos_marca_selecao, outline=RGB_BLUE, width=3, fill=RGB_BLUE)
                    self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)
                #self.cartas[i].selecionada = True
                break

    def descartar(self, pos):
        for carta in self.cartas:
            if carta.selecionada:
                print "Descartei: %s" % carta.valor
                self.cartas.remove(carta)
                print "Tamanho de Cartas: %s" % len(self.cartas)
                self.espacoCartas.clear(0)
                self.handle_redraw()
                

    def handle_event(self, evento):
        #evento['type'] == 257 #down
        #evento['type'] == 263 #drag
        #evento['type'] == 258 #up
        #evento = {'modifiers':0, 'type': 263, 'pos':(165,209)}

        
        
        if evento['type'] == 257:
            for carta in self.cartas:
                carta.marcada = False
                if self.tocou_na_carta(evento['pos'], carta.rect):
                    carta.marcada = True
                    #self.espacoCartas.clear(0)
                    #self.espacoCartas.rectangle(carta.pos_marca_selecao, outline=RGB_RED, width=3, fill=RGB_RED)
                    #self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)
                    
                else:
                    carta.marcada = False
        if evento['type'] == 258:
            for carta in self.cartas:
                carta.selecionada = False
                
                if self.tocou_na_carta(evento['pos'], carta.rect):
                    if carta.marcada:
                        carta.selecionada = True
                        #self.espacoCartas.clear(0)
                        #self.espacoCartas.rectangle(carta.pos_marca_selecao, outline=RGB_BLUE, width=3, fill=RGB_BLUE)
                        #self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)
                        
                    else:
                        carta.selecionada = False
                        
                    carta.marcada = False
                        
            #if carta.marcada.rect != carta.selecionada.rect:
                #self.espacoCartas.rectangle(ultimaCartaSelecionada.pos_marca_selecao, outline=RGB_BLUE, width=3, fill=RGB_BLUE)
        self.espacoCartas.clear(0)
        for carta in self.cartas: 
            if carta.marcada:
                self.espacoCartas.rectangle(carta.pos_marca_selecao, outline=RGB_RED, width=3, fill=RGB_RED)
            if carta.selecionada:
                self.espacoCartas.rectangle(carta.pos_marca_selecao, outline=RGB_BLUE, width=3, fill=RGB_BLUE)
                            
        
        
        self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)
         
         
          
        #print evento
        

    def handle_redraw(self, rect=None):
        if self.telajogo:
            self.canvas.blit(self.telajogo)
            self.desenhaCartas()
        if self.espacoCartas:
            self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)




    def quit(self, pos=(0,0)):
        """Function called when the user requests exit"""
        global app_lock
        appuifw.app.exit_key_handler = None
        app_lock.signal()








app = Jogo()

#app.desenhaCartas()



app_lock = e32.Ao_lock()
app_lock.wait()

