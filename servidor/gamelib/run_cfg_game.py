# to keep the main game seperate
import logging
log = logging.getLogger('run_cfg_game')

from cocos.director import  director 
from cocos.scene import Scene

import config
import constants

def loadandrun(args = None):        
    
    if constants.DEBUG:
        gamename = config.gamefile
    else:
        gamename = "game"

    log.info("Loading :"+str(gamename))
    try:
        game = __import__(gamename)
        if args is not None:
            director.push(Scene (game.run(args)) )
        else:
            director.push(Scene (game.run()) ) # Dont push in the menu cause it will consume up and down key events
    except ImportError:
        print "Import error: "+gamename
        
