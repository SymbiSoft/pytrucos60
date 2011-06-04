#-*- coding: utf-8 -*-
# Author: Wander Jardim
# email: wanderjardim@gmail.com
#        Copyright 2011
# About: The main application class, will hold event processing
# code as also objects to represent windows.

'''
/*  Copyright (C) 2011  Wander Jardim <wanderjardim@gmail.com>
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; by version 2 of the License.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */
'''


class configure:
    #Todas as definições estão em um dicionario chamado pref
    pref = {}             # Configurações gerais
    userpref = {}         # Configurações livres para ser alteradas pelo usuário




    def __init__(self,path):
        # Local onde armazenaremos nossos dados e configurações
        self.set_value(self.userpref, 'base_dir', path)
        # Ajuste para "full" se quiser que seja usada toda a tela
        self.set_value(self.pref,'game_screen', 'large')    #
                          # 'large'   # softkeys fica visivel
                          # 'full'    # fica em tela cheia
        # Define o título
        self.set_value(self.pref,'titulo_jogo', "PyTruco4S60")



    def set_value(self,dict, key, value, type = None):
        """Essa função seta os pares  de key e value em um dicionário, se a chave ainda não existir.
           Se a chave já existir, não acontece nada, exceto se o tipo for específicado, aí
           então, ele tenta converter o valor para esse tipo.
        """
        if not dict.has_key(key):
            dict[key] = value

        # aqui, definitivamente a chave existe 
        if type == 'bool':
            if dict[key] == "False":
                dict[key] = False
            elif dict[key] == "True":
                dict[key] = True
            # atenção: nunca implemente um caso else aqui, porque
            # isto destruiria as configurações padrão
        elif type == 'int':
            try: dict[key] = int(dict[key])
            except:
                print "Não é possível converter %s para %s" % (key, type)
                sys.exit(-1)
        elif type == 'float':
            try: dict[key] = float(dict[key])
            except:
                print "Não é possível converter %s para %s" % (key, type)
                sys.exit(-1)

















