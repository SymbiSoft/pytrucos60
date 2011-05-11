#-*- coding: utf-8 -*-
#!/usr/bin/env python

# para manter o jogo principal separado
import logging
log = logging.getLogger('run_cfg_game')

from cocos.director import  director 
from cocos.scene import Scene

import config
import constantes

def loadandrun(args):        
    
    if constants.DEBUG:
        nomejogo = config.arqjogo
    else:
        nomejogo = "jogo"

    log.info("Carregando :"+str(nomejogo))
    try:
        jogo = __import__(nomejogo)
        if args is not None:
            director.push(Scene (jogo.run(args)) )
        else:
            director.push(Scene (jogo.run()) ) # Dont push in the menu cause it will consume up and down key events
    except ImportError:
        print "Import error: "+nomejogo

