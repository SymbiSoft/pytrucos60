#-*- coding: utf-8 -*-
#!/usr/bin/env python
import logging
log = logging.getLogger('ready_menu')


from cocos.director import director
from cocos.menu import *
from cocos.scene import Scene
from cocos.scenes.transitions import *
#from lookup import BuildLookupTable, SortByName
import config
import constantes

#from aguarda_conexao import TelaConexoes
import aguarda_conexao
from bg_layer import BGLayer



class MenuConexao( Menu ):

    def __init__(self):
        super( MenuConexao, self).__init__(u"Escolha um Tipo de Conexão") 
        
        self.font_title = {
            'font_name':'Forte',
            'font_size':45,
            'color':(75,135,73,255),
            'bold':False,
            'italic':False,
            'anchor_y':'center',
            'anchor_x':'center',
            'x':500, 'y':300,
        }
              
        self.menu_valign = CENTER
        
        self.font_item = {
            'font_name':'Forte',
            'font_size':40,
            'color':(75,135,73,255),
        }
        
        self.font_item_selected = {
            'font_name':'Forte',
            'font_size':40,
            'color':(0,0,0,255),
        }
        
        
        #self.x = 35
        self.y = -150
        
        
       
        self.conexoes = {'3Bluetooth': 'bluetooth', '2Wireless':'wireless', '1GPRS':'gprs'} #SortByName(BuildLookupTable("levels", "defs/levels.def") )
        log.debug("conexoes:"+str(self.conexoes.keys()))
        
        self.conexao_escolhida = 0 
        log.info("conexao:"+str(self.conexao_escolhida))
        
        items = []
        items.append( MenuItem('Iniciar Partida', self.on_play) )

        items.append( MultipleMenuItem(
                        u'Conexão : ', 
                        self.na_conexao,
                        self.conexoes.keys(),
                        self.conexao_escolhida )
                    )


        self.create_menu( items)
            
    def on_enter(self):
        super(MenuConexao, self).on_enter() 
    def on_quit(self):
        # chamado ao precionar esc
        director.scene.end()

    def na_conexao( self, idx ):
        self.conexao_escolhida = idx
        log.info("na_conexao:"+str(self.conexao_escolhida)+" ->"+str(self.conexoes[self.conexoes.keys()[self.conexao_escolhida]]))

    def on_play( self ):
        log.info("on_play:"+str(self.conexoes[self.conexoes.keys()[self.conexao_escolhida]]))
        # Testando nova tela de Aguardando conexão em 11/05/11
        #director.push(Scene (jogo.run(self.conexoes[self.conexoes.keys()[self.conexao_escolhida]])))
        
        #director.push(Scene (BGLayer("menu"),  TelaConexoes(self.conexoes[self.conexoes.keys()[self.conexao_escolhida]])))
        tipo_conexao = self.conexoes[self.conexoes.keys()[self.conexao_escolhida]]
        s = aguarda_conexao.get_menu_conexao(tipo_conexao)
        director.replace(FadeTransition( s, 1 ) )
         
        #print self.conexoes[self.conexoes.keys()[self.conexao_escolhida]]
            

def get_scene():
    scene = Scene(BGLayer("menu2"), MenuConexao() )
    return scene

