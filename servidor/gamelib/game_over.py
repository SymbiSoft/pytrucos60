#-*- coding: utf-8 -*-


import cocos
from cocos.menu import *
from cocos.text import Label
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer import Layer
from cocos.layer.util_layers import ColorLayer
import game_audio
from cocos.director import director

import pyglet
from pyglet.gl import *

import menu_conexoes

class JanelaErroScene(Scene):
    def __init__(self):
        super(JanelaErroScene, self).__init__()

    def on_enter(self):
        game_audio.stop_music()
        super(JanelaErroScene, self).on_enter()

    def on_quit(self):
        director.pop()
        director.pop()

class JanelaMsgMenu(Layer):
    
    def __init__(self, msg):
        super( JanelaMsgMenu, self).__init__()
        
        self.msg_erro = Label("%s !!!" % msg) #, font_name='Segoe Print', font_size=23, x=30, y=600, anchor_x='left', anchor_y='top')
        
        
        self.add(self.msg_erro)
    
    
    
    

class JanelaErroMenu(Menu):
    """Pause menu"""
    def __init__(self):
        super(JanelaErroMenu, self).__init__('Erro!!')

        itens = []
        itens.append( MenuItem('Deseja jogar novamente?', self.on_main_menu))
        itens.append( MenuItem('Sair', self.on_quit))
        self.create_menu(itens)
        game_audio.stop_music()


    def on_main_menu(self):
        print "Obrigado por jogar!"
        director.replace(FadeTransition( menu_conexoes.get_scene(), duration = 0.4 ) )
        #director.pop()
        sounds.set_music('musicas/music_intro.ogg')

    def on_quit(self):
        print "Thanks for playing!"
        sys.exit()


def get_janela():
    w, h = director.window.width, director.window.height
    texture = pyglet.image.Texture.create_for_size(
                    GL_TEXTURE_2D, w, h, GL_RGBA)
    texture.blit_into(pyglet.image.get_buffer_manager().get_color_buffer(), 0,0,0)
    scene = JanelaErroScene()
    bg = Sprite(texture.get_region(0, 0, w, h))
    bg.x=w/2;
    bg.y=h/2;
    scene.add(bg,z=-999)
    overlay = ColorLayer(25,25,25,205)
    scene.add(overlay)
    #menu = JanelaErroMenu()
    msg = JanelaMsgMenu("Partida Termida")
    #scene.add(menu)
    scene.add(msg)
    return scene