#-*- coding: utf-8 -*-

'''
Created on 21/06/2011

@author: wander
'''

from graphics import Image
import e32
import os
import sysinfo


IMG_PATH1 = "\\Python\\img\\"
IMG_PATH2 = "\\Data\\python\\img\\"
IMG_PATH3 = "\\Private\\ef0b4099\\img\\"



def cria_imagem(arquivoImagem):
    """Carrega imagem referente ao parametro passado. Se a imagem não existir no
    diretório, retorna vazio.
    """
    
    caminho = get_caminho(arquivoImagem)
    
    try:
        img = Image.open(caminho+arquivoImagem)
        return img
    except:
        print "Imagem não encontrada!"
        return None



def get_caminho(arquivo):
    drives_list = e32.drive_list()
    drives_list.reverse()
    for drive in [str(x) for x in drives_list]:
        if os.path.isfile(os.path.join(drive, IMG_PATH1, arquivo)):
            return os.path.join(drive, IMG_PATH1)
        elif os.path.isfile(os.path.join(drive, IMG_PATH2, arquivo)):
            return os.path.join(drive, IMG_PATH2)
        elif os.path.isfile(os.path.join(drive, IMG_PATH3, arquivo)):
            return os.path.join(drive, IMG_PATH3)
    return None



def getTamanho_tela():
    return sysinfo.display_pixels()