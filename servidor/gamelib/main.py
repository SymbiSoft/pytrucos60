#-*- coding: utf-8 -*-
#!/usr/bin/env python
"""Módulo principal de partida.

The DEBUG constant can be safely assumed set by the time this module is
imported.

A constante DEBUG pode ser seguramente assumido definido pelo tempo que 
este módulo é importado.

"""

import random, math
import datetime

import logging
log = logging.getLogger('main')


import cocos
import cocos.scene
from cocos.scenes.transitions import *
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.director import director

import pyglet
import data
import config
from common import *
from constantes import *
import game_audio

from bg_layer import BGLayer
from menu_main import MainMenu

  
def run():
    
    director.init(caption=TITULO_JOGO, width=LARGURA_JANELA, height=ALTURA_JANELA, resizable=False )

 
    mainmenu = Scene(BGLayer("menu"), MainMenu())
    intro = Scene(BGLayer("splash"))
    #game_audio.play_song('music_intro.ogg')
    

    director.window.set_fullscreen(config.fullscreen)

    image = pyglet.image.load('data/imagens/mouse.png')
    cursor = pyglet.window.ImageMouseCursor(image, 16, 16)
    director.window.set_mouse_cursor(cursor)
    
    if config.playerseed == "": # first time this person has run the game
        print "First time run generating seed"
        config.playerseed = str(random.uniform(0, 99999999))+":"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        config.save_option("playerseed", config.playerseed)
        director.run( FadeTransition( mainmenu, 10, intro) )
    
    else:   
        director.run( FadeTransition( mainmenu, 5, intro) )
    

def main():
    log.info('Starting main...')  
    
    if config.profile:
        import os, profile
        print "printou profilleee"
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(SCRIPT_DIR, "profile-%s.log" % timestamp)
        profile.runctx("run()", globals(), None, filename)
        import pstats # http://docs.python.org/library/profile.html
        p = pstats.Stats(filename)
        stats = p.sort_stats('time').print_stats(10)#print_callers(10) 
        log.debug(stats)
    else:
        run()
    
    log.info('... DONE')  
    
