#-*- coding: utf-8 -*-

"""Definição das constantes.

Este arquivo é carregado durante a inicialização do programa antes de o módulo 
principal ser importado. Por conseguinte, este arquivo não deve importar qualquer 
outro módulo, ou os módulos serão inicializados antes do módulo principal, o 
que significa que o valor DEBUG pode não ter sido configurado corretamente.

Este módulo destina-se a ser importado com a semântica 'from ... import *', mas
ele não fornece uma especificação __all__.

"""

#: Ativa o de depuração. Nunca deve ser alterada manualmente, mas é definida 
#: como True automaticamente quando estiver executando o `test_game.py».
DEBUG = False

#: String da Versão  Ela pode ser representado em algum lugar no jogo. Ela 
#: também é lido pelo 'setup.py' como parte de suas características de versionamento.
VERSION = u"V. 0.1"

#: O diretório (em relação ao nível superior) em que todos os recursos para o 
#: jogo serão armazenados, provavelmente, subdivididas em tipos de recursos. 
#: Veja `data.py».
DATA_DIR = "data"

#: O nome do jogo utilizado na localização do diretório de configurações salvas.
#: É bom não ter nenhum espaço neste nome.
CONFIG_NAME = "PyTruco4S60"

#: A legenda que aparece no topo da janela. Obviamente isto é apenas visível 
#: no modo de janela.
CAPTION = u"PyTruco4S60 - Server"
TITULO_JOGO = u"PyTruco4S60 - Server"

#: Definição da dimensões da janela do jogo
LARGURA_JANELA, ALTURA_JANELA = 800, 600

#: Definição do nome da fonte usada no jogo
FONTE_JOGO = 'Mail Ray Stuff'

#: Definição do volume dos sons
MUSIC_VOLUME = 0.25



TMP_LOC = "/tmp/"
from pyglet.lib import loader
if loader.platform == "win32":
    TMP_LOC = ""
   
LOGFILE = TMP_LOC+CONFIG_NAME+".log"
 
SCRIPT_DIR =  TMP_LOC    
    
