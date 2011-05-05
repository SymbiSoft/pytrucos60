#-*- coding: utf-8 -*-
import logging
log = logging.getLogger('ready_menu')


from cocos.director import director
from cocos.menu import *
from cocos.scene import Scene
#from lookup import BuildLookupTable, SortByName
import config
import constants

class ReadyMenu( Menu ):

    def __init__(self):
        super( ReadyMenu, self).__init__("Choose Level") 
        
        self.menu_valign = BOTTOM
        #self.font_item['color'] = (32,16,32,255)
        self.font_item['font_size'] = 16
        self.font_item['color'] = (189,190,190,255)
        self.font_item_selected['color'] = (128,16,32,255)
        self.font_item_selected['font_size'] = 24
       
        self.levels = {'Bluetooth': 'truco', 'Wireless':'meio pau', 'GPRS':'nove'} #SortByName(BuildLookupTable("levels", "defs/levels.def") )
        log.debug("levels:"+str(self.levels.keys()))
        
        self.level_choice = 0 
        log.info("level:"+str(self.level_choice))
        
        items = []
        items.append( MenuItem('PLAY', self.on_play) )

        items.append( MultipleMenuItem(
                        'Level : ', 
                        self.on_level,
                        self.levels.keys(),
                        self.level_choice )
                    )


        self.create_menu( items)
            
    def on_enter(self):
        super(ReadyMenu, self).on_enter() 
    def on_quit(self):
        # called by esc
        director.scene.end()

    def on_level( self, idx ):
        self.level_choice = idx
        log.info("on_level:"+str(self.level_choice)+" ->"+str(self.levels[self.levels.keys()[self.level_choice]]))

    def on_play( self ):
        log.info("on_play:"+str(self.levels[self.levels.keys()[self.level_choice]]))
        if constants.DEBUG:
            #import run_cfg_game
            #run_cfg_game.loadandrun(self.levels[self.levels.keys()[self.level_choice]])
            print self.levels[self.levels.keys()[self.level_choice]]
        else:
            #import game
            #director.push(Scene (game.run(self.levels[self.levels.keys()[self.level_choice]]))) 
            print self.levels[self.levels.keys()[self.level_choice]]
            
