#-*- coding: utf-8 -*-

from cocos.menu import *
from cocos.layer import Layer,ColorLayer
from cocos.director import director
from pyglet.window import key
import config
from cocos.sprite import Sprite

import game_audio
import constantes
      
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
            config.arqjogo = "game"
            
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

