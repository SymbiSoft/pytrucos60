#-*- coding: utf-8 -*-
'''
Criado em 24 de Novembro de 2010

@author: Wander Jrdim
'''
import logging
log = logging.getLogger('audio')

import pyglet.media
import data
import config

class Audio(object):
    def __init__(self):
        
        log.info("inicializando audio")
                 
        self.player = pyglet.media.Player()
        self.sounds = {}
        self.sfx_volume = config.sfxvolume/10.0
        self.enable_sound = True
        
    def carrega_som(self, name):
        
        log.info("carregando som:"+str(name))
                 
        if name not in self.sounds:
            self.sounds[name] = data.carrega_som(name)
        return self.sounds[name]

    def play_sound(self, name):
        if name not in self.sounds:
            self.carrega_som(name)  
        
        log.info("tocando som:"+str(name))
                 
        self.sounds[name].play().volume = self.sfx_volume

    def play_song(self, name):
        
        log.info("tocando som:"+str(name))
                 
        self.player.volume = config.musicvolume/10.0
        self.player.queue(data.carrega_musica(name))
        self.player.play()
        self.player.eos_action = 'loop'

    def next_song(self):       
        log.info("parando a musica:")
        self.player.next()

    def sound_volume(self, vol):       
        log.info("configurando volume do som:"+str(vol))
                 
        self.sfx_volume = vol 
    def music_volume(self, vol):       
        log.info("configurando volume da musica:"+str(vol))
                 
        self.player.volume = vol
    def pause_music(self):
        log.info("pausando a musica")
                 
        self.music.play()
    def start_music(self):        
        log.info("iniciando a musica")

    def stop_music(self):
        if(self.enable_sound):
            self.player.pause()
                 
    def pre_load_sfx(self, sfx_list):
        log.info("pre-cacheado efeitos de som: "+str(sfx_list))
                 
        for sfx in sfx_list:
            self.carrega_som(sfx)  
                 
_audio = None

def init_audio():
    global _audio
    
    if _audio is None:
        _audio = Audio()

def play_sound(name):
    global _audio

    if _audio is None:
        init_audio()
    
    _audio.play_sound(name)
    
def sound_volume(vol):
    global _audio

    if _audio is None:
        init_audio()
    
    _audio.sound_volume(vol)

def play_song(name):
    global _audio

    if _audio is None:
        init_audio()
    
    _audio.play_song(name)


def stop_music():
    global _audio

    if _audio is not None:
        _audio.stop_music()


def next_song():
    global _audio

    if _audio is None:
        init_audio()
    
    _audio.next_song()

def music_volume(vol):
    global _audio

    if _audio is None:
        init_audio()
    
    _audio.music_volume(vol)
    
def pre_load_sfx(sfx_list):
    global _audio

    if _audio is None:
        init_audio()
    
    _audio.pre_load_sfx(sfx_list)
    
    
