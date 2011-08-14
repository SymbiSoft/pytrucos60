



import cocos
from cocos.director import director
from cocos.layer import *
from cocos.scene import Scene

import constantes

FONT_NAME_TITLE = FONTE_JOGO
FONT_NAME_MENU = FONTE_JOGO



class CamadaServidor( ColorLayer):

    FONT_SIZE=22

    is_event_handler = True #: enable pyglet's events

    def __init__(self):

        w,h = director.get_window_size()
        super( CamadaServidor,self).__init__( 32,32,32,16, width=w, height=h-97)

        self.font_title = {}

        # you can override the font that will be used for the title and the items
        self.font_title['font_name'] = FONTE_JOGO
        self.font_title['font_size'] = 36
#        self.font_title['color'] = (204,164,164,255)
        self.font_title['color'] = COLOR_WHITE
        self.font_title['anchor_y'] ='top'
        self.font_title['anchor_x'] ='center'

        title = Label('GAS MAN', **self.font_title )

        title.position=(w/2.0,h-5)

        self.add(title,z=1)

        self.table = None

    def on_enter( self ):
        super(ScoresLayer,self).on_enter()

        scores = hiscore.hiscore.get()

        if self.table:
            self.remove_old()

        self.table =[]
        for idx,s in enumerate(scores):

            pos= Label( '%d:' % (idx+1), font_name=FONT_NAME_MENU,
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='left',
                        color=(255,255,255,255) )

            name = Label( s[1], font_name=FONT_NAME_MENU,
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='left',
                        color=(255,255,255,255) )

            score = Label( str(s[0]), font_name=FONT_NAME_MENU,
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='right',
                        color=(255,255,255,255) )

            lvl = Label( str(s[2]), font_name=FONT_NAME_MENU,
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='right',
                        color=(255,255,255,255) )

            self.table.append( (pos,name,score,lvl) )

        self.process_table()

    def remove_old( self ):
        for item in self.table:
            pos,name,score,lvl = item
            self.remove(pos)
            self.remove(name)
            self.remove(score)
            self.remove(lvl)
        self.table = None

    def process_table( self ):
        w,h = director.get_window_size()

        for idx,item in enumerate(self.table):
            pos,name,score,lvl = item

            posy = h - 100 - ( (self.FONT_SIZE+15) * idx )

            pos.position=( 5, posy)
            name.position=( 48, posy)
            score.position=( w-150, posy )
            lvl.position=( w-10, posy)

            self.add( pos, z=2 )
            self.add( name, z=2 )
            self.add( score, z=2 )
            self.add( lvl, z=2 )

    def on_key_press( self, k, m ):
        if k in (key.ENTER, key.ESCAPE, key.SPACE):
            self.parent.switch_to( 0 )
            return True

    def on_mouse_release( self, x, y, b, m ):
        self.parent.switch_to( 0 )
        return True




def get_servidor_scene():

    scene = Scene()
    scene.add(CamadaServidor(), z=2 )

    return scene
