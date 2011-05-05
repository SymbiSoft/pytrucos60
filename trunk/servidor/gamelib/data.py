#-*- coding: utf-8 -*-

"""Carregadores de Dados.

Adicione funções aqui para carregar tipos específicos de recursos.

"""

from __future__ import division

import os

from pyglet import font
from pyglet import media

import config
from common import *
from constantes import *

import os
import pyglet

import logging
log = logging.getLogger('data')

path = os.path.abspath(os.path.join(os.getcwd(), DATA_DIR)) 

log.info("Caminho do aquivos de dados: ["+path+"]")

font.add_directory(os.path.join(path, "fonts"))
    
pyglet.resource.path.append(path)
pyglet.resource.reindex()


def carrega_arquivo(path, mode="rb"):
    """Abrir um arquivo.

    :Parametros:
        `path` : str
            O caminho relativo do diretório de dados para o arquivo.
        `mode` : str
            O modo a ser usado quando abrir um arquivo (padrão: "rb").

    """
    file_path = os.path.join(DATA_DIR, path)
    return open(file_path, mode)


def carrega_musica(path):
    """Carrega um stream de musica a partir do diretório música.

    :Parametros:
        `path` : str
            O caminho relativo do diretório de músicas para o arquivo.

    """
    song_path = os.path.join(DATA_DIR, "musicas", path)
    return media.load(song_path, streaming=True)


def carrega_som(path):
    """Carrega uma fonte estática de som a partir do diretório sons.

    :Parametros:
        `path` : str
             O caminho relativo do diretório sons para o arquivo.

    """
    sound_path = os.path.join(DATA_DIR, "sons", path)
    return media.load(sound_path, streaming=False)
