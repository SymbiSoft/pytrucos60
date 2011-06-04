#-*- coding: utf-8 -*-
#######################################################
# 
# splash.py
# Python implementation of the Class Splash
# Generated by Enterprise Architect
# Created on:      30-mai-2011 14:15:33
# Original author: Wander Jardim
# 
#######################################################


from graphics import Image
import e32
import os
import sysinfo

IMG_PATH1 = "\\Python\\img\\"
IMG_PATH2 = "\\Data\\python\\img\\"
IMG_PATH3 = "\\Private\\ef0b4099\\img\\"

class Splash:
    
    def __init__ (self):
        self.largura_tela, self.altura_tela = self.__getTamanho_tela()
        
        self.__caregar_imagens()
    
    def __caregar_imagens(self):
        caminho_img = self.__get_caminho('splash.png')
        
        self.fundoSplash=self.__cria_imagem(caminho_img + 'splash.png')
        

    def __cria_imagem(self, caminho):
        """Carrega imagem referente ao parametro passado. Se a imagem não existir no
        diretório, retorna vazio.
        """
        try:
            img = Image.open(caminho)
            return img
        except:
            print "Imagem não encontrada!"
            return None


    def desenha_splash(self, canvas):
        tela_splash = Image.new((self.largura_tela, self.altura_tela))
        mascaraSplash = Image.new((self.largura_tela, self.altura_tela), 'L')
        for i in range(0,26):
            fond=0
            texte=(10*i)
            mascaraSplash.clear((texte,texte,texte))
            tela_splash.clear((fond,fond,fond))
            tela_splash.blit(self.fundoSplash,mask=mascaraSplash)
            canvas.blit(tela_splash) # mostra a imagem na tela
            #e32.ao_sleep(0.06)
        #e32.ao_sleep(0.5)



    def __get_caminho(self, arquivo):
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

    def __getTamanho_tela(self):
        return sysinfo.display_pixels()