#-*- coding: utf-8 -*-

from pyglet.window import key 

from cocos.layer import ColorLayer
from cocos.director import director
from cocos.sprite import Sprite
#from cocos.layer import Layer,ColorLayer

class BGLayer( ColorLayer ):
    def __init__(self, file):
        ColorLayer.__init__(self, 0,0,0,0)
        w,h = director.get_window_size()
        bg = Sprite("data/backgrounds/"+file+".png")
        bg.position = w/2,h/2
        self.add(bg)
        

