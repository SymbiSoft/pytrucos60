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


LARGU_CARTA = 146
ALTUR_CARTA = 210

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


#Dicionario para definir os valores do posicionamento no arquivos das cartas:
dictCartas = {'3e':((0,0),(LARGU_CARTA, ALTUR_CARTA)), '2e':((LARGU_CARTA,0), (2*LARGU_CARTA, ALTUR_CARTA)), 'ac':((2*LARGU_CARTA,0), (3*LARGU_CARTA, ALTUR_CARTA))}
