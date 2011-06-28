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



"""
# the initial timer is triggered, follow up the keys in the pressablekeys
# contribution by Makoto Sugano
def pressablekeys_followup():
    escancode_isdown = app.pressablekeys_isdown()
    if (escancode_isdown):
        timer.cancel()
        app.pressablekeys_process(escancode_isdown)
        timer.after(0.1, pressablekeys_followup)
    else:
        timer.cancel()
"""


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


# disable directional pad
appuifw.app.directional_pad = False



LARGU_CARTA = 153
ALTUR_CARTA = 220

POS_CARTA01 = (8,123)
POS_CARTA02 = (166,123)
POS_CARTA03 = (324,123)

RECT_CARTA01 = ( POS_CARTA01, (POS_CARTA01[0]+LARGU_CARTA, POS_CARTA01[1]+ALTUR_CARTA) )
RECT_CARTA02 = ( POS_CARTA02, (POS_CARTA02[0]+LARGU_CARTA, POS_CARTA02[1]+ALTUR_CARTA) )
RECT_CARTA03 = ( POS_CARTA03, (POS_CARTA03[0]+LARGU_CARTA, POS_CARTA03[1]+ALTUR_CARTA) )

SOURCE_CARTA01 = ((0,0), (LARGU_CARTA, ALTUR_CARTA))
SOURCE_CARTA02 = ((LARGU_CARTA,0), (2*LARGU_CARTA, ALTUR_CARTA))
SOURCE_CARTA03 = ((2*LARGU_CARTA,0), (3*LARGU_CARTA, ALTUR_CARTA))


RGB_BLUE = (0, 0, 255)


class Jogo:
    def __init__(self):
        appuifw.app.orientation = 'landscape'
        file_erro = open('E:\\Python\\Meu_error2.log', 'r+')
        self.largura_tela, self.altura_tela = util.getTamanho_tela()
        self.telajogo = Image.new((self.largura_tela,self.altura_tela))
        appuifw.app.exit_key_handler = self.quit
        self.toque = {}
        appuifw.app.title = u"Teste tela Cartas"
        #Verificando a versão do pys60 instalada para saber se oferece suporte ao touch e desabilitando o joystick.
        if e32.pys60_version_info > (1,9):
            appuifw.app.directional_pad = False
            if appuifw.touch_enabled():
                appuifw.app.screen= 'full' #'large' #
                TOUCH_ENABLED = True
            else:
                appuifw.note(u"Touch screen nao encontrado", "error")
        
        
        self.posCartas = []
        self.posCartas.append(POS_CARTA01)
        self.posCartas.append(POS_CARTA02)
        self.posCartas.append(POS_CARTA03)
        
        self.toque['posicao'] =  self.posCartas
        
        
        self.rectCartas = []
        self.rectCartas.append(RECT_CARTA01)
        self.rectCartas.append(RECT_CARTA02)
        self.rectCartas.append(RECT_CARTA03)
        self.toque['rectCartas'] = self.rectCartas


        self.sourceCartas = []
        self.sourceCartas.append(SOURCE_CARTA01)
        self.sourceCartas.append(SOURCE_CARTA02)
        self.sourceCartas.append(SOURCE_CARTA03)        
        self.toque['sourceCartas'] = self.sourceCartas


        self.posCartas = []
        self.posCartas.append(POS_CARTA01)
        self.posCartas.append(POS_CARTA02)
        self.posCartas.append(POS_CARTA03)        
        self.toque['posCartas'] = self.posCartas

        
        self.canvas = appuifw.Canvas(event_callback = None,
                                     redraw_callback = self.handle_redraw)
        appuifw.app.body = self.canvas

        self.fundoMesa = util.cria_imagem('fundoMesa.png')
        
        rect_bot_sair = ((self.largura_tela-65, self.altura_tela-35),(self.largura_tela-5, self.altura_tela-5)) 
        self.fundoMesa.rectangle(rect_bot_sair, outline=RGB_BLUE, width=3, fill=RGB_BLUE)
        
        self.canvas.bind(key_codes.EButton1Up, self.quit, rect_bot_sair)
        
        
        self.telajogo.blit(self.fundoMesa)
        # mostra a imagem na tela
        
        

        

    def desenhaCartas(self):
        #72x100 - x16
        
        imgsCartas = []
        imgsCartas.append(Image.new((LARGU_CARTA,ALTUR_CARTA)))
        imgsCartas.append(Image.new((LARGU_CARTA,ALTUR_CARTA)))
        imgsCartas.append(Image.new((LARGU_CARTA,ALTUR_CARTA)))
        
        self.toque['imgCartas'] = imgsCartas 
        #self.camadaCartas = Image.new((self.largura_tela,self.altura_tela))
        #cartas.clear(0)
        self.matrizCartas = util.cria_imagem('cartasteste.png')
        
        for i in range(len(self.toque['imgCartas'])):
            self.carregaCarta(i)
            self.telajogo.blit(self.toque['imgCartas'][i], target = self.toque['posCartas'][i])
            self.canvas.bind(key_codes.EButton1Up, self.seleciona_carta, self.toque['rectCartas'][i] )
            self.canvas.bind(key_codes.EButton1Down, self.deseleciona_carta, self.toque['rectCartas'][i] )        

        
        espacoCartas = util.cria_imagem('espacoCartas.png')
        self.espacoCartas = Image.new(espacoCartas.size)
        
        self.espacoCartas.rectangle(SOURCE_CARTA01, outline=RGB_BLUE, width=3)
        self.maskCartas = Image.new(espacoCartas.size, 'L') #tons de cinza 8-bits
        self.maskCartas.blit(espacoCartas)
        
        self.canvas.blit(self.espacoCartas, mask=self.maskCartas)
        
        
        self.bordaSelecao = Image.new((LARGU_CARTA+4,ALTUR_CARTA+4))
        self.bordaSelecao.clear(RGB_BLUE)
        #self.bordaSelecao.rectangle(SOURCE_CARTA01, outline=RGB_BLUE, width=3)
        mask = util.cria_imagem('mascaraCartas.png')
        self.mask = Image.new(mask.size, 'L') #tons de cinza 8-bits
        self.mask.blit(mask)                  #converte a imagem para 8-bits

        
        self.canvas.blit(self.telajogo)
        
        #self.canvas.blit(self.bordaSelecao, mask=self.mask)


    def carregaCarta(self, indice):
        self.toque['imgCartas'][indice].blit(self.matrizCartas, target = (0, 0), source = self.toque['sourceCartas'][indice])

        
    def deseleciona_carta(self, pos):
        print "deselecionou: (%s, %s)" % pos
        self.bordaSelecao.clear()
        for i in range(len(self.toque['rectCartas'])):
            if self.tocou_na_carta(pos, self.toque['rectCartas'][i]):
                pass
            else:
                #self.telajogo.rectangle(self.toque['rectCartas'][i], outline=RGB_BLUE, width=3)
                #self.canvas.blit(self.telaSelecaoCartas, target = self.toque['posicao'][i])
                #self.toque['imgCartas'][i].clear()
                print "Deselect1"
                
                #self.canvas.blit(self.bordaSelecao, mask=self.mask, target = self.toque['posicao'][i])
                
                #self.canvas.blit(self.bordaSelecao, mask=self.mask)
                #self.canvas.blit(self.bordaSelecao)
                #break
        
        
        #self.telajogo.clear()

    def tocou_na_carta(self, pos, carta):
        if  pos[0] >= carta[0][0] and pos[0] <  carta[1][0]\
        and pos[1] >= carta[0][1] and pos[1] <  carta[1][1]:
            return True
        return False


    def seleciona_carta(self, pos):
        ''' Seleciona carta '''
        print "selecionou: (%s, %s)" % pos
        
        #self.telaSelecaoCartas = Image.new((72,100))
        self.bordaSelecao.clear()
        for i in range(len(self.toque['rectCartas'])):
            if self.tocou_na_carta(pos, self.toque['rectCartas'][i]):
                #self.telajogo.rectangle(self.toque['rectCartas'][i], outline=RGB_BLUE, width=3)
                #self.toque['imgCartas'][i].clear()
                #self.toque['imgCartas'][i].rectangle(self.toque['rectCartas'][i], outline=RGB_BLUE, width=3)
                #self.canvas.blit(self.toque['imgCartas'][i])
                print "Select1"
                
                #self.bordaSelecao.rectangle(self.toque['rectCartas'][i], outline=RGB_BLUE, width=3)
                
                self.canvas.blit(self.bordaSelecao, mask=self.mask, target = self.toque['posicao'][i])
                #break
            
        
        
        
        
        
        #appuifw.note(u"Blue Down")



    def handle_redraw(self, rect):
        if self.telajogo:
            self.canvas.blit(self.telajogo)




    def quit(self, pos=(0,0)):
        """Function called when the user requests exit"""
        global app_lock
        appuifw.app.exit_key_handler = None
        app_lock.signal()








app = Jogo()

app.desenhaCartas()



app_lock = e32.Ao_lock()
app_lock.wait()

