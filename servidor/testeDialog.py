import os

import pyglet
import cocos
from cocos.director import director
from cocos import tiles

VERSION = 'TesteDialog 0.2.0'


class DialogNode(cocos.batch.BatchableNode):
    def __init__(self, dialog=None):
        super(DialogNode, self).__init__()
        self.dialog = dialog

    def set_batch(self, batch, group=None, z=0):
        super(DialogNode, self).set_batch(batch, group)
        if self.dialog is not None:
            self.dialog.batch = self.batch
            self.dialog.group = self.group

    def delete(self, dialog=None):
        self.dialog.teardown()
        super(DialogNode, self).on_exit()
        self.parent.remove(self)

    def draw(self):
        pass




class EditorScene(cocos.scene.Scene):
    def __init__(self):
        super(EditorScene, self).__init__()
        self.manager = tiles.ScrollingManager()
        self.add(self.manager)
        self.dialog_layer = DialogLayer()
        #self.scrollbar_layer = DialogLayer()
        #self.dialog_layer.add_dialog(DialogNode(kytten.Dialog(kytten.Frame(kytten.Scrollable(kytten.Spacer(100, 100), width=50, height=50)))))
        self.editor_layer = None
        self.tile_dialog = None
        self.add(self.dialog_layer)
        

    def open(self):
        pass

class DialogLayer(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self, dialog=None):
        super(DialogLayer, self).__init__()
        self.batchnode = cocos.batch.BatchNode()
        #self.batchnode.position = 50,100
        self.add(self.batchnode)
        #self.batch = pyglet.graphics.Batch()
        #self.group = pyglet.graphics.OrderedGroup(0)
        director.window.register_event_type('on_update')        
        def update(dt):
            director.window.dispatch_event('on_update', dt)
        self.schedule(update)

    def add_dialog(self, dialog_node):
        if dialog_node is not None:
            self.batchnode.add(dialog_node)

director.init(width=800, height=600, resizable=True, 
                  do_not_scale=True, caption=VERSION)

director.show_FPS = True
pyglet.gl.glClearColor(.3, .3, .3, 1)


e = EditorScene()


director.run(e)
