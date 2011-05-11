#-*- coding: utf-8 -*-
import appuifw
import graphics
import e32
import sysinfo
import key_codes #import key_codes - required for touch event detection
import traceback
import sys, os

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
#        elif os.path.isfile(os.path.join(drive, PYTRUCOS60_PATH3, app_name)):
#            return os.path.join(drive, PYTRUCOS60_PATH3)
    return None


full_path = get_path('testeAplic.py') 
if full_path == None:
    full_path = get_path('testeAplic.py')
    if full_path == None:
        appuifw.note(u'Usando fallback path')
        full_path = u'C:\\' + u'Private' + u'\\' + PYTRUCOS60_UID + u'\\'


sys.path.append(os.path.join(full_path, "pytruco","libs"))

from btclient import BluetoothError
import btclient 


# define colour constants
RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)
RGB_PURPLE = (100,0,255)
RGB_BLACK = (0,0,0)

larg, alt = sysinfo.display_pixels()

# disable directional pad
appuifw.app.directional_pad = False
 
#prepare canvas for drawing
canvas = appuifw.Canvas()
appuifw.app.body = canvas
 
#obtaining canvas size (Total_x and Total_y)
Total_x, Total_y = canvas.size
larg, alt = canvas.size
y1 = Total_y/4

lado1 = larg/3
lado2 = alt/5


print "Largura: %s  -  Altura: %s " % (larg,alt)

print "Lado 1: %s  -  Lado 2: %s " % (lado1,lado2)


def blue_down(event):
    ''' Blue DOWN event handler '''
    print "evento blue_down: "
    print event
    appuifw.note(u"Blue Down")
 
def green_up(event):
    ''' Green UP event handler '''
    print "evento green_up: "
    print event
    appuifw.note(u"Green Up")
 
def red_drag(event):
    ''' Red DRAG event handler '''
    print "evento red_drag: "
    print event
    appuifw.note(u"Red Drag")
 
def purple_tap(event):
    ''' Purple TAP event handler '''
    print "evento purple_tap: "
    print event
    appuifw.note(u"Purple Tap")

btcliente = None

def conexoes(event): 
    global btcliente
    print "evento conexoes: "
    print event
    opcoes_conexoes = [u"Bluetooth", u"WI-FI", u"GPRS", u"Voltar"]
    conexao = appuifw.popup_menu(opcoes_conexoes, u"Tipo de conexão")
    if conexao == 0:
        try:
            btcliente = btclient.BluetoothClient()
            connectBT()
        except Exception, exc:
            open("E:\\Python\\errorTestAplic.log", "w").write(traceback.format_exc())
            raise
        #appuifw.note(u"Vou me conectar por Bluetooth" , "info")
        desenha_botoes()

        print "Falow, Abraço!!"
        #disconnect()


def desenha_botoes():
    global btcliente
    
    myscreen = graphics.Image.new((larg,alt))
    myscreen.clear((15,126,0))
    
    

    # Retangulo Lilas - TAP Event
    '''Desenha um retangulo lilaz e o texto'''
    myscreen.rectangle(((10+lado1,10+lado2), (10+2*lado1,(2*lado2)+10)), fill=RGB_PURPLE, width=5)
    myscreen.text((20+lado1,lado2+45), u"Mandar msg", fill = RGB_BLACK,font=(u'Nokia Hindi S60',10,appuifw.STYLE_BOLD))  
    '''Vincula a função TAP ao retangulo Lilas'''
    canvas.bind(key_codes.EButton1Up, enviaPosicao, ((10+lado1,10+lado2), (10+2*lado1,(2*lado2)+10)))

    # Retangulo Azul - Evento DOWN
    '''Desenha um retangulo azul e o texto'''
    myscreen.rectangle(((5,5), (5+lado1,5+lado2)), fill=RGB_BLUE, width=5)
    myscreen.text((20,40), u"Envia texto", fill = RGB_BLACK,font=(u'Nokia Hindi S60',10,appuifw.STYLE_BOLD)) 
    '''Vincula a função DOWN ao retangulo azul'''
    canvas.bind(key_codes.EButton1Down, enviaTexto, ((5,5), (lado1,lado2)))

    # Retangulo Vermelho - DRAG Event
    '''Desenha um retangulo vermelho e o texto'''
    myscreen.rectangle(((5,10+lado2), (5+lado1,(2*lado2)+10)), fill=RGB_RED, width=5)
    myscreen.text((20,lado2+45), u"Desconectar", fill = RGB_BLACK,font=(u'Nokia Hindi S60',10,appuifw.STYLE_BOLD))  
    '''Vincula a função DRAG ao retangulo vermelho'''
    canvas.bind(key_codes.EDrag, desconectar, ((5,10+lado2), (5+lado1,(2*lado2)+10)))
    
    canvas.blit(myscreen) # show the image on the screen
    while btcliente.is_connected():
        data = btcliente.recebe_comando()
        appuifw.note(u"%s" % data)
    

def enviaPosicao(event):
    global btcliente
    btcliente.send_command(str(event))


def desconectar(event):
    global btcliente
    txtDescon = "Vou desconectar! - %s e %s " % (event)
    btcliente.send_command(txtDescon)
    disconnect()

def enviaTexto(event):
    global btcliente
    txtEnviar = "s"
    btcliente.send_command(txtEnviar)


def connectBT():
    """Conecta ao servidor.
    """
    global btcliente
    try:
        btcliente.connect()
    except BluetoothError, e:
        appuifw.note(u"Erro na execução do Bluetooth %s"%e, "error")


def disconnect():
    """Disconnects from the server.
    """
    global btcliente
    try:
        btcliente.close()
    except BluetoothError, e:
        appuifw.note((e.msg), "error")


# Retangulo Azul - Evento DOWN
'''Desenha um retangulo azul e o texto'''
canvas.rectangle(((5,5), (5+lado1,5+lado2)), fill=RGB_BLUE, width=5)
canvas.text((25,40), u"Teste 1", fill = RGB_BLACK,font=(u'Nokia Hindi S60',30,appuifw.STYLE_BOLD)) 
'''Vincula a função DOWN ao retangulo azul'''
canvas.bind(key_codes.EButton1Down, blue_down, ((5,5), (lado1,lado2)))
 
# Retangulo verde - UP Event
'''Desenha um retangulo verde e o texto'''
canvas.rectangle(((10+lado1,5), (10+2*lado1, 5+lado2)), fill=RGB_GREEN, width=5)
canvas.text((30+lado1,40), u"Teste 2", fill = RGB_BLACK,font=(u'Nokia Hindi S60',30,appuifw.STYLE_BOLD))  
'''Vincula a função UP ao retangulo Verde'''
canvas.bind(key_codes.EButton1Up, conexoes, ((7+lado1,5), (7+2*lado1, lado2)))
 
# Retangulo Vermelho - DRAG Event
'''Desenha um retangulo vermelho e o texto'''
canvas.rectangle(((5,10+lado2), (5+lado1,(2*lado2)+10)), fill=RGB_RED, width=5)
canvas.text((25,lado2+45), u"Teste 3", fill = RGB_BLACK,font=(u'Nokia Hindi S60',30,appuifw.STYLE_BOLD))  
'''Vincula a função DRAG ao retangulo vermelho'''
canvas.bind(key_codes.EDrag, red_drag, ((5,10+lado2), (5+lado1,(2*lado2)+10)))
 
# Retangulo Lilas - TAP Event
'''Desenha um retangulo lilaz e o texto'''
canvas.rectangle(((10+lado1,10+lado2), (10+2*lado1,(2*lado2)+10)), fill=RGB_PURPLE, width=5)
canvas.text((30+lado1,lado2+45), u"Teste 4", fill = RGB_BLACK,font=(u'Nokia Hindi S60',30,appuifw.STYLE_BOLD))  
'''Vincula a função TAP ao retangulo Lilas'''
canvas.bind(key_codes.EButton1Up, purple_tap, ((10+lado1,10+lado2), (10+2*lado1,(2*lado2)+10)))
 
#wait for user to exit


app_lock = e32.Ao_lock()
app_lock.wait()

if btcliente:
    disconnect()

