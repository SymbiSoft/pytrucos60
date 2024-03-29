#-*- coding: utf-8 -*-
from cocos.director import director
from cocos.menu import *
from cocos.scene import Scene

from bg_layer import BGLayer

class BackMenu( Menu ):

    def __init__(self, name = 'Voltar'):
        super( BackMenu, self).__init__() 
        
        
        self.font_item['color'] = (75,135,73,255)
        self.font_item['font_name'] = 'Forte'
        
        self.font_item_selected['color'] = (75,135,73,255)
        self.font_item_selected['font_name'] = 'Forte'
        
        items = []
        
        items.append( MenuItem(name, self.on_back) )

        self.create_menu( items)
        
        # Spacing
        pos = 0
        for menuItem in items:
            menuItem.y -= 300
            pos += 1
        
    def on_back(self):
        director.scene.end()
        
    def on_quit(self):
        # called by esc
        director.scene.end()


def get_scene():
    scene = Scene(BGLayer("menu2"), BackMenu() )
    return scene