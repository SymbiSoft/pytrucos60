#-*- coding: utf-8 -*-
#!/usr/bin/env python

import random, datetime, math

from cocos.director import director
from cocos.layer import Layer,ColorLayer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.scenes.transitions import *
from cocos.actions import *
from cocos.scenes.transitions import FadeTransition

from cocos.menu import *
from cocos.text import *

#import pygame
import config

from screen_config import ConfigMenu
from menu_back import BackMenu

import menu_conexoes

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
        director.push(FadeTransition( menu_conexoes.get_scene(), duration = 0.4 ) )
        
    def on_scores( self ):
        pass #director.push(Scene (BGLayer("scores"), ScoresLayer(), BackMenu()) )
        
    def on_settings( self ):
        director.push(Scene (BGLayer("menu"),  ConfigMenu()))
        
        
    def on_credits( self ):
        director.push(Scene (BGLayer("creditos"), BackMenu()) )

    def on_quit(self):
        pyglet.app.exit()
        








class PauseMenu(Menu):
    """Pause menu"""
    def __init__(self):
        super(PauseMenu, self).__init__('Paused')

        l = []
        l.append( MenuItem('Continue', self.on_continue))
        l.append( MenuItem('Quit to Main Menu', self.on_main_menu))
        l.append( MenuItem('Exit', self.on_quit))
        self.create_menu(l)
        sounds.stop_music()

    def on_continue(self):
        sounds.play_music()
        director.pop()

    def on_main_menu(self):
        print "Thanks for playing!"
        director.pop()
        director.pop()
        sounds.set_music('music/intro.ogg')

    def on_quit(self):
        print "Thanks for playing!"
        sys.exit()




class PauseMenuScene(Scene):
    def __init__(self):
        super(PauseMenuScene, self).__init__()
        self.add(DisableEscapeKeyLayer())

    def on_enter(self):
        sounds.stop_music()
        super(PauseMenuScene, self).on_enter()



def pause_menu():
    w, h = director.window.width, director.window.height
    texture = pyglet.image.Texture.create_for_size(
                    GL_TEXTURE_2D, w, h, GL_RGBA)
    texture.blit_into(pyglet.image.get_buffer_manager().get_color_buffer(), 0,0,0)
    scene = PauseMenuScene()
    bg = Sprite(texture.get_region(0, 0, w, h))
    bg.x=w/2;
    bg.y=h/2;
    scene.add(bg,z=-999)
    overlay = ColorLayer(25,25,25,205)
    scene.add(overlay)
    menu = PauseMenu()
    scene.add(menu)
    return scene