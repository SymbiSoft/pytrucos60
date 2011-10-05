#-*- coding: utf-8 -*-

"""Definição das constantes.

Este arquivo é carregado durante a inicialização do programa antes de o módulo 
principal ser importado. Por conseguinte, este arquivo não deve importar qualquer 
outro módulo, ou os módulos serão inicializados antes do módulo principal, o 
que significa que o valor DEBUG pode não ter sido configurado corretamente.

Este módulo destina-se a ser importado com a semântica 'from ... import *', mas
ele não fornece uma especificação __all__.

"""

#Definições das constantes de cores
RGB_LIGHT_BLUE = (65, 156, 241)

RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)
RGB_PURPLE = (100,0,255)
RGB_BLACK = (0,0,0)
RGB_VERDE = (37,135,40)

COR_FD_INFOS = (217,218,222)


LARGU_CARTA = 146
ALTUR_CARTA = 212

POS_CARTA01 = (9,134)
POS_CARTA02 = (169,134)
POS_CARTA03 = (327,134)

POS_ESPAC_CARTAS = (5,130)

RECT_CARTA01 = ( POS_CARTA01, (POS_CARTA01[0]+LARGU_CARTA, POS_CARTA01[1]+ALTUR_CARTA) )
RECT_CARTA02 = ( POS_CARTA02, (POS_CARTA02[0]+LARGU_CARTA, POS_CARTA02[1]+ALTUR_CARTA) )
RECT_CARTA03 = ( POS_CARTA03, (POS_CARTA03[0]+LARGU_CARTA, POS_CARTA03[1]+ALTUR_CARTA) )

SOURCE_CARTA01 = ((0,0), (LARGU_CARTA, ALTUR_CARTA))
SOURCE_CARTA02 = ((LARGU_CARTA,0), (2*LARGU_CARTA, ALTUR_CARTA))
SOURCE_CARTA03 = ((2*LARGU_CARTA,0), (3*LARGU_CARTA, ALTUR_CARTA))

POS_CARTA01_SELEC = ((0,0),(LARGU_CARTA+10,ALTUR_CARTA+10))
POS_CARTA02_SELEC = ((LARGU_CARTA+12,0),(2*LARGU_CARTA+23,ALTUR_CARTA+10))
POS_CARTA03_SELEC = ((2*LARGU_CARTA+26,0),(3*LARGU_CARTA+35,ALTUR_CARTA+10))


posCartas = [POS_CARTA01, POS_CARTA02, POS_CARTA03]
posCartasSelec = [POS_CARTA01_SELEC, POS_CARTA02_SELEC, POS_CARTA03_SELEC]

listBotoes = {"truco":((0,0),(140,34)), "meiopau":((0,34),(140,68)), "nove":((0,68),(140,104)), "doze":((0,135),(140,169))}

#Dicionario para definir os valores do posicionamento no arquivos das cartas:
LC = LARGU_CARTA
AC = ALTUR_CARTA
dictCartas = {'ae':((0,0),(LC, AC)), 
              '2e':((LC,0), (2*LC, AC)), 
              '3e':((2*LC,0), (3*LC, AC)), 
              '4e':((3*LC,0), (4*LC, AC)), 
              '5e':((4*LC,0), (5*LC, AC)),
              '6e':((5*LC,0), (6*LC, AC)), 
              '7e':((6*LC,0), (7*LC, AC)), 
              'de':((7*LC,0), (8*LC, AC)), 
              've':((8*LC,0), (9*LC, AC)), 
              're':((9*LC,0), (10*LC, AC)),
              
              'ap':((0,AC),(LC, 2*AC)),
              '2p':((LC,AC),(2*LC, 2*AC)),
              '3p':((2*LC,AC),(3*LC, 2*AC)),
              '4p':((3*LC,AC),(4*LC, 2*AC)),
              '5p':((4*LC,AC),(5*LC, 2*AC)),
              '6p':((5*LC,AC),(6*LC, 2*AC)),
              '7p':((6*LC,AC),(7*LC, 2*AC)),
              'dp':((7*LC,AC),(8*LC, 2*AC)),
              'vp':((8*LC,AC),(9*LC, 2*AC)),
              'rp':((9*LC,AC),(10*LC, 2*AC)),
              
              'ac':((0,2*AC),(LC, 3*AC)),
              '2c':((LC,2*AC),(2*LC, 3*AC)),
              '3c':((2*LC,2*AC),(3*LC, 3*AC)),
              '4c':((3*LC,2*AC),(4*LC, 3*AC)),
              '5c':((4*LC,2*AC),(5*LC, 3*AC)),
              '6c':((5*LC,2*AC),(6*LC, 3*AC)),
              '7c':((6*LC,2*AC),(7*LC, 3*AC)),
              'dc':((7*LC,2*AC),(8*LC, 3*AC)),
              'vc':((8*LC,2*AC),(9*LC, 3*AC)),
              'rc':((9*LC,2*AC),(10*LC, 3*AC)),
                            
              'ao':((0,3*AC),(LC, 4*AC)),
              '2o':((LC,3*AC),(2*LC, 4*AC)),
              '3o':((2*LC,3*AC),(3*LC, 4*AC)),
              '4o':((3*LC,3*AC),(4*LC, 4*AC)),
              '5o':((4*LC,3*AC),(5*LC, 4*AC)),
              '6o':((5*LC,3*AC),(6*LC, 4*AC)),
              '7o':((6*LC,3*AC),(7*LC, 4*AC)),
              'do':((7*LC,3*AC),(8*LC, 4*AC)),
              'vo':((8*LC,3*AC),(9*LC, 4*AC)),
              'ro':((9*LC,3*AC),(10*LC, 4*AC)),
              }














































