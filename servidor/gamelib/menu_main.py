#-*- coding: utf-8 -*-
#!/usr/bin/env python

import random, datetime, math

from cocos.director import director
from cocos.layer import Layer,ColorLayer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.scenes.transitions import *
from cocos.actions import *

from cocos.menu import *
from cocos.text import *

#import pygame
import config
from bg_layer import BGLayer
from screen_config import ConfigMenu
from menu_back import BackMenu
from menu_game_conexoes import MenuConexao

class MainMenu( Menu ):

    def __init__(self):
        super( MainMenu, self).__init__() 
        
        self.menu_valign = BOTTOM
        #self.font_item['color'] = (32,16,32,255)
        self.font_item['font_size'] = 16
        self.font_item['color'] = (189,190,190,255)
        self.font_item_selected['color'] = (128,16,32,255)
        self.font_item_selected['font_size'] = 24
       
        items = []

        items.append( MenuItem(u'Iniciar Servidor', self.on_play) )
        items.append( MenuItem(u'Opções', self.on_settings) )
        items.append( MenuItem(u'Créditos', self.on_credits) )
        items.append( MenuItem(u'Sair', self.on_quit) )

        self.create_menu(items)

    def on_enter(self):
        super(MainMenu, self).on_enter() 
               
    def on_play( self ):
        director.push(Scene (BGLayer("menu"),  MenuConexao()))
        
    def on_scores( self ):
        pass #director.push(Scene (BGLayer("scores"), ScoresLayer(), BackMenu()) )
        
    def on_settings( self ):
        director.push(Scene (BGLayer("menu"),  ConfigMenu()))
        
        
    def on_credits( self ):
        director.push(Scene (BGLayer("creditos"), BackMenu()) )

    def on_quit(self):
        pyglet.app.exit()
        
