# -*- coding: utf-8 -*-
#######################################################
# 
# jogo.py
# Python implementation of the Class Jogo
# Generated by Enterprise Architect
# Created on:      31-mai-2011 15:43:56
# Original author: Wander Jardim
# 
#######################################################

import appuifw
import sysinfo
from graphics import Image
import traceback
import key_codes

import clienteBT
from constantes import *
import util
import json

class Jogo:
    def __init__(self, conexao):
        try: 
            self.render=0
            self.file_erro = 'E:\\Python\\Meu_error2.log'
            self.conexao = conexao
            self.largura_tela, self.altura_tela = util.getTamanho_tela()
            self.telajogo = Image.new((self.largura_tela,self.altura_tela))
            self.espacoCartas = None
            self.cartas = None
            self.matrizCartas = util.cria_imagem('matrizCartas.png')
            
            
            
            self.canvas = appuifw.Canvas(event_callback = self.handle_event,
                                         redraw_callback = self.handle_redraw)
            appuifw.app.body = self.canvas
            #appuifw.app.menu = [(u"Descartar", self.descartar), (u"Envia qq coisa", self.enviaqqcoisa), (u'Envia um texto', self.enviatxtPerso) ]
            
            self.render=1
            
            self.fundoMesa = util.cria_imagem('fundoMesa.png')
            
            
            #Bot�o Sair
            self.quit = appuifw.app.exit_key_handler
            rect_bot_sair = ((5, 5),(25, 25)) 
            self.fundoMesa.rectangle(rect_bot_sair, outline=RGB_BLUE, width=1)
            self.canvas.bind(key_codes.EButton1Up, self.quit, rect_bot_sair)
            
            espacoCartas = util.cria_imagem('espacoCartas.png')
            self.espacoCartas = Image.new(espacoCartas.size) #espacoCartas.size)
            self.maskCartas = Image.new(espacoCartas.size, 'L') #tons de cinza 8-bits
            self.maskCartas.blit(espacoCartas)
            
            espacoInfos = util.cria_imagem('espacoInfos.png')
            self.espacoInfos = Image.new(espacoInfos.size) #espacoCartas.size)
            self.maskInfos = Image.new(espacoInfos.size, 'L') #tons de cinza 8-bits
            self.maskInfos.blit(espacoInfos)
            
            self.telajogo.blit(self.fundoMesa)
            # mostra a imagem na tela
            self.canvas.blit(self.telajogo)
    
            #Bot�o Descartar
            rect_botao_descartar = ((512,160),(630,200)) #((303,64),(452,114)) # 
            self.fundoMesa.rectangle(rect_botao_descartar, outline=RGB_BLUE, width=1)
            self.canvas.bind(key_codes.EButton1Down, self.descartar, rect_botao_descartar)
            
            #Bot�o Truco
            rect_botao_descartar = ((513,263),(630,301)) #((303,64),(452,114)) # 
            self.fundoMesa.rectangle(rect_botao_descartar, outline=RGB_BLUE, width=1)
            self.canvas.bind(key_codes.EButton1Down, self.pedirTuco, rect_botao_descartar)
            
        except Exception, erro:
            msgErro = "Erro no INIT: " + str(erro) + "\n"
            self.log(msgErro)
            raise
        
    
    def pedirTuco(self, rect):
        self.conexao.envia_comando(json.write({'truco':'pedido'}))
        data = json.read(self.conexao.recebe_comando())
        
        

    def enviatxtPerso(self):
        texto = appuifw.query("Digite o texto", 'text')
        textoEnviar = eval(texto)
        self.conexao.envia_comando(json.write(textoEnviar))

    def log(self, log):
        open(self.file_erro, 'a').write(log)


    def cria_cartas(self,cartas_recebidas):
        #Criando as cartas:
        self.cartas = []
        for i in range(len(cartas_recebidas)):
            self.cartas.append(Carta(posCartas[i], dictCartas[cartas_recebidas[i]], posCartasSelec[i], cartas_recebidas[i]))

    def desenhaCartas(self):
        #mask = util.cria_imagem('mascaraCartas.png')
        #self.maskCarta = Image.new(mask.size, 'L') #tons de cinza 8-bits
        #self.maskCarta.blit(mask) 
        for carta in self.cartas:
            self.carregaCarta(carta)
            self.canvas.blit(carta.imagem, target = carta.posicao_mesa)
            self.canvas.bind(key_codes.EButton1Up, self.seleciona_carta, carta.rect)
            self.canvas.bind(key_codes.EButton1Down, self.deseleciona_carta, carta.rect) 

    def carregaCarta(self, carta):
        carta.imagem.blit(self.matrizCartas, target=(0, 0), source=carta.source)


    def loop_jogo(self):    
        try: 
            if self.conexao.esta_conectado():
                pos = 95
                while True:
                    data = json.read(self.conexao.recebe_comando())
                    
                    
                    print data
                    self.log("recebido: %s \n" % data)
                    if not data :
                        break
                    else:
                        if 'cartas' in data: #startswith('cartas'):
                            #self.cartas = data['cartas']
                            #print "dados recebido (inicio cartas): %s" % data
                            #self.log("dados recebido (inicio cartas): %s" % data)
                            #dadosRecebidos = data.split(':')
                            self.cartas_recebidas = data['cartas'] #dadosRecebidos[1].split('/')
                            self.conexao.envia_comando(json.write({'OK':'Cartas Recebidas'}))
                            self.cria_cartas(self.cartas_recebidas)
                            self.desenhaCartas()
                        
                        
                        
                        elif 'truco' in data:
                            if data['truco'].startswith(":"):
                                self.informaPedidoTruco(data['truco'])
                                self.conexao.envia_comando(json.write({'OK':'Pedido Informado'}))
                                
                            elif data['truco'] == 'aceita?':
                                respTruco = self.mostarOpcoesTruco()
                                self.conexao.envia_comando(respTruco)
                                
                            
                            elif data['truco'] == '':
                                pass
                        
                        
                        elif 'fim' in data:
                            print "Recebi comando de fim de Mao"
                            if data['fim'] == 'mao':
                                self.telajogo.text((10, pos), u"recv >> %s" % data, fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
                                self.canvas.blit(self.telajogo)
                                self.handle_redraw()
                                self.limpaCartasMao()
                                self.conexao.envia_comando(json.write({'OK':'Fim Mao'}))
                            elif data['fim'] == 'partida':
                                self.informaFimPartida()
                                
                                
                            
                            
                            
                            
                        elif data == 1:
                            pass   
                        
                        
                        else:
                            self.mostraInfos(data)
                            
                            #self.telajogo.text((10, pos), u"recv >> %s" % data, fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
                            #self.canvas.blit(self.telajogo)
                            #self.handle_redraw()
                        pos += 15
        except Exception, erro:
            msgErro = "Erro do loop_jogo: " + str(erro) + "\n"
            self.log(msgErro)
            raise


    def mostraInfos(self, info):
        
        self.espacoInfos.clear(0)
        self.espacoInfos.text((5,10), u">> %s" % info, fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
        self.canvas.blit(self.espacoInfos, target = (40,40), mask=self.maskInfos)
        self.handle_redraw(((40,40),(300,110)))
        
    

    def informaPedidoTruco(self, nome):
        
        rectInfos = ((40,40),(300,110))
        self.telajogo.text((10, pos), u"recv >> %s" % data, fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
        self.canvas.blit(self.telajogo)
        self.handle_redraw()
        


    def limpaCartasMao(self):
        intervalo = len(self.cartas)
        for carta in range(intervalo):
            self.cartas.pop()


        self.espacoCartas.clear(0)
        self.telajogo.text((10, 20), u"FIM DA M�O", fill = RGB_BLACK,font=(u'Nokia Hindi S60',20,appuifw.STYLE_BOLD))
        self.canvas.blit(self.telajogo)
        self.handle_redraw()
    
    def informaFimPartida(self):
        pass


    def tocou_na_carta(self, pos, carta):
        if  pos[0] >= carta[0][0] and pos[0] <  carta[1][0]\
        and pos[1] >= carta[0][1] and pos[1] <  carta[1][1]:
            return True
        return False
        
    
    def deseleciona_carta(self, pos):
        for carta in self.cartas:
            if self.tocou_na_carta(pos, carta.rect):
                self.espacoCartas.clear(0)
                self.espacoCartas.rectangle(carta.pos_marca_selecao, outline=RGB_RED, width=3, fill=RGB_RED)
                self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)
            else:
                carta.selecionada = False
        
    def seleciona_carta(self, pos):
        ''' Seleciona carta '''
        for i in range(len(self.cartas)):
            if self.tocou_na_carta(pos, self.cartas[i].rect):
                self.espacoCartas.clear(0)
                
                self.espacoCartas.rectangle(self.cartas[i].pos_marca_selecao, outline=RGB_BLUE, width=3, fill=RGB_BLUE)
                self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)
                self.cartas[i].selecionada = True
                break

    def descartar(self, pos=None):
        for carta in self.cartas:
            if carta.selecionada == True:
                print "Descartei: %s" % carta.valor
                
                self.conexao.envia_comando(json.write({"carta":carta.valor}))
                self.cartas.remove(carta)
                print "Tamanho de Cartas: %s" % len(self.cartas)
                self.espacoCartas.clear(0)
                self.handle_redraw()



    def handle_event(self, evento):
        #print evento
        pass
        


    def handle_redraw(self, rect=None):
        if self.telajogo:
            self.canvas.blit(self.telajogo)
            if self.cartas:
                self.desenhaCartas()
                
        if self.espacoCartas:
            self.canvas.blit(self.espacoCartas, target = POS_ESPAC_CARTAS, mask=self.maskCartas)

    """
    def event_redraw(self, other):
        if self.render == 0:
            self.canvas.clear()
            self.telajogo.clear((15,126,0))
            self.canvas.blit(self.telajogo)
    """




class Carta(object):
    def __init__(self, pos_mesa, source, pos_marca_selecao, valor):
        self.posicao_mesa = pos_mesa
        self.rect = (self.posicao_mesa, (self.posicao_mesa[0]+LARGU_CARTA, self.posicao_mesa[1]+ALTUR_CARTA))
        self.source = source
        self.pos_marca_selecao = pos_marca_selecao
        self.imagem = Image.new((LARGU_CARTA,ALTUR_CARTA))
        self.valor = valor
        self.selecionada = False
