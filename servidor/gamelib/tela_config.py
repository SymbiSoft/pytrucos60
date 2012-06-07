#-*- coding: utf-8 -*-

from cocos.menu import *
from cocos.scene import Scene
from cocos.layer import Layer,ColorLayer
from cocos.director import director
from pyglet.window import key
import pyglet
import config
from cocos.sprite import Sprite
from cocos.text import Label


import game_audio
import constantes
from bg_layer import BGLayer


from cocos.cocosnode import CocosNode

class Rectangle(CocosNode):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )

class TextWidget(CocosNode):
    def __init__(self, text, x, y, width, batch):
        super(TextWidget, self).__init__()
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
            dict(color=(0, 0, 255, 255)))
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

    def draw(self):
      self.layout.draw()


class textInputLayer(Layer):
    # For the layer to receive events this variable must be set to 'True'
    is_event_handler = True

    def __init__(self, *args, **kwargs):
        super(textInputLayer, self).__init__()

        self.batch = pyglet.graphics.Batch()
        self.labels = [
            Label(u'Endereço Servidor', x=10, y=100, anchor_y='bottom', color=(0, 0, 0, 255)),
            Label(u'Porta', x=10, y=60, anchor_y='bottom', color=(0, 0, 0, 255)),
            Label(u'Nome', x=10, y=20, anchor_y='bottom', color=(0, 0, 0, 255)),]
        map(self.add, self.labels)

        self.width, self.height = director.get_window_size()
        self.widgets = [
             TextWidget('', 200, 100, self.width - 210, self.batch),
             TextWidget('', 200, 60, self.width - 210, self.batch),
             TextWidget('', 200, 20, self.width - 210, self.batch),
        ]
        self.text_cursor = director.window.get_system_mouse_cursor('text')
        map(self.add, self.widgets)

        self.focus = None
        self.set_focus(self.widgets[0])


    def draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        director.window.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                director.window.set_mouse_cursor(self.text_cursor)
                break
        else:
            director.window.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        
        print symbol
        print modifiers
        
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.widgets[(i + dir) % len(self.widgets)])

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)







class ConfigMenu( Menu ):
    def __init__(self):
        super( ConfigMenu, self).__init__() 
        self.font_item['font_size'] = 16
        self.font_item['color'] = (189,190,190,255)
        self.font_item_selected['font_size'] = 24
        self.font_item_selected['color'] = (128,16,32,255)

        self.playername = config.playername
        self.musicvolume = config.musicvolume
        self.sfxvolume = config.sfxvolume
        self.arqjogo = config.arqjogo
        
        items = []
                
     
        if constantes.DEBUG:
            items.append( EntryMenuItem('DBG Game:', self.on_game, self.arqjogo) )
         
        # No High scores - dont need this for now   
        #items.append( EntryMenuItem('Name:', self.on_name, self.playername) )
        
        self.volumes = [
                        '----------',
                        '|---------',
                        '-|--------',
                        '--|-------',
                        '---|------',
                        '----|-----',
                        '-----|----',
                        '------|---',
                        '-------|--',
                        '--------|-',
                        '---------|'
                        ]
        

        items.append( MultipleMenuItem(
                        'Efeitos de Som: ', 
                        self.on_sfx_volume,
                        self.volumes,
                        int(self.sfxvolume) )
                    )
        items.append( MultipleMenuItem(
                        'Musica de fundo : ', 
                        self.on_music_volume,
                        self.volumes,
                        int(self.musicvolume) )
                    )
        
        #items.append( ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS) )
        items.append( MenuItem('Tela Cheia', self.on_fullscreen) )
        
        
        items.append( MenuItem('Voltar', self.on_back) )
        

        self.create_menu( items)

    def on_back(self):
        config.playername = self.playername
        config.save_option("playername",config.playername)

        if constantes.DEBUG:
            config.arqjogo = self.arqjogo
        else:
            config.arqjogo = "jogo"
            
        config.save_option("arqjogo",config.arqjogo)

        config.save_option("musicvolume",self.musicvolume)
        config.save_option("sfxvolume",self.sfxvolume)
        
        config.save_option("fullscreen", director.window.fullscreen)
        
        director.scene.end()
        
    def on_quit(self):
        # called by esc
        director.scene.end()
        
    def on_fullscreen( self ):
        director.window.set_fullscreen( not director.window.fullscreen )

    def on_sfx_volume( self, idx ):
        vol = idx / 10.0
        self.sfxvolume = idx
        game_audio.sound_volume( vol )

    def on_music_volume( self, idx ):
        vol = idx / 10.0
        self.musicvolume = idx
        game_audio.music_volume( vol )
        
    def on_name( self, value ):
        self.playername = value

    def on_game( self, value ):
        self.arqjogo = value

def get_scene():
    scene = Scene(BGLayer("menu2"), ConfigMenu() )
    text_layer = textInputLayer()
    scene.add(text_layer)
    return scene
