if __name__ == "__main__":
    import sys,os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import cocos
from cocos import sprite
from cocos.director import director

from PIL import Image
from PIL import TgaImagePlugin
from PIL import PngImagePlugin

import config
from common import *
from constantes import *
from data import carrega_arquivo

#import anims
#from tiledtmxloader import ImageLoaderPyglet


try:
    import psycho
    psyco.full()
    BASEOBJ =  psyco.compact
    
    print "Imported psycho!"
except ImportError:
    print "Import psycho failed."
    BASEOBJ = object


import logging
log = logging.getLogger('tiles')
log.debug("imported")

# TODO: move to defn file
PLAYER_START = 16

def load_level_from_image( filename):
        log.info("Loading tile layer from: "+filename)
        file = load_file(filename, "rb")
        log.debug("Image file open:"+str(file))
        #import PIL.TgaImagePlugin.TgaImageFile
        #PIL.TgaImagePlugin.TgaImageFile 
        im = Image.open(file)#source_tiles)
        
        log.debug("Loading Image file:"+str(im))

        pix = im.load()
        log.debug("Closing Image file:"+str(pix))
        file.close()
        
        width , height = im.size
        log.info("level size:"+str( im.size))
        
        packed_data = []
        
        
            
        for y in xrange(height):
            row = []
            for x in xrange(width):
                row.append(pix[x,height-1-y])
             
            packed_data.append(row)
        
        return   width , height, packed_data

class TileHandeler(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self, initial_offset = (0,0)):
        super(TileHandeler, self).__init__()
        self.position = initial_offset
        
        self.scroller = cocos.layer.ScrollingManager()

        self.add(self.scroller)
        
    def add_scrolling_layer(self, layer, offset = [0,0]):
        self.scroller.add(layer)

class TileSprite(cocos.sprite.Sprite):
    def __init__(self, img):
        super(TileSprite, self).__init__(img)
        self.properties = {
                           "top":True,
                            "left": True,
                            "bottom": True,
                            "right": True,
                            }
        
class TileLayer(cocos.tiles.RectMapLayer): 
    is_event_handler = True
    def __init__(self, source_tiles, background_tile_images = None, std_dim = None, isBack = False, parallax = 1):
        global _opened_files
        log.debug("TileLayer.__init__"+str((source_tiles, background_tile_images, std_dim)))
        
        if std_dim is None:
            std_dim = (32,32)

        self.groundcells = []
        
        width , height, tile_data = source_tiles
        
        properties = None
        self.tileset = []
        tileset = []
        
        tileset = []# cocos.tiles.TileSet("moo", None)
        
        if background_tile_images is not None:

            self.tileset = anims.OpenFile(background_tile_images, std_dim)
            cnt = 0
            for img in self.tileset:
                sp = TileSprite(img)
                tileset.append(sp)
                #tileset.add(img, None, cnt)
                cnt += 1
        
        
            
        log.info( "Got "+str(len(tileset))+" tiles")
        tile_width, tile_height  = std_dim
        blanktile = cocos.tiles.RectCell(-1,-1, tile_width, tile_height, (-1,0,0), tileset[0])
        for x in xrange(width):
            row = []
            for y in xrange(height):            
                fg_tile, bg_tile, action = tile_data[y][x]
                properties = (fg_tile, bg_tile, action)

                # handle forground
                #fg_tile = fg_tile# % len(tileset)
                #bg_tile = bg_tile# % len(tileset)
                
                     
                if isBack: 
                    tile_choice = bg_tile
                else:
                    tile_choice = fg_tile
                    
                tile = tileset[tile_choice]     
                
                if tile_choice == 0 :
                    newtile = cocos.tiles.RectCell(-1,-1, tile.width, tile.height, properties, tile)
                else:
                    newtile = cocos.tiles.RectCell(x,y, tile.width, tile.height, properties, tile)

                row.append(newtile)

                # Handle background tiles
                
                # Handle action tiles
                    
            self.groundcells.append(row)
            
        log.info( "Map cells: "+str(len(self.groundcells)))
        log.info( "Map w,h: "+str(width*tile_width)+","+str(height*tile_height))
                
        #super(TileLayer, self).__init__( "moo", tile_width, tile_height, tileset, (0,0,0), parallax)
        super(TileLayer, self).__init__( "moo", tile_width, tile_height, self.groundcells, (0,0,0), parallax)

        self.set_dirty()
        
        
    def remove(self, child):
        super(TileLayer, self).remove(child)

    def check_collide(self, obj):
        pass
    
def run():
    import pyglet   
    
    
    leveldata = load_level_from_image("data/level/9.tga")
    tiles = TileLayer(leveldata, 
                               std_dim=[32,32], 
                               background_tile_images = "data/images/dngn.png", 
                               creature_tile_images = "data/images/nethackcreaturetiles32x32.png")
    manager = TileHandeler()
    manager.add_scrolling_layer(tiles)
    main_scene = cocos.scene.Scene(manager.scroller)
    manager.scroller.set_focus(100,100)
    manager.scroller.scale =  0.09
    
    def on_key_press(key, modifier):
        from cocos.actions import ScaleTo
        low = 0.1
        if key == pyglet.window.key.Z:
            if manager.scroller.scale == low:
                manager.scroller.do(ScaleTo(1, 2))
            else:
                manager.scroller.do(ScaleTo(low, 2))
                
    director.window.push_handlers(on_key_press)
    return main_scene

if __name__ == '__main__':



    director.init(width=640, height=480, do_not_scale=True)    
    director.run(run())
  
    
