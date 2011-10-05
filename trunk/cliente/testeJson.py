#-*- coding: utf-8 -*-
# Author: Wander Jardim
# email: wanderjardim@gmail.com
#        Copyright 2011
# About: The main application class, will hold event processing
# code as also objects to represent windows.

import appuifw
import e32
import sys
import os



PYTRUCOS60_UID = u"ef080808"

TESTE_PATH1 = "\\Python\\"
TESTE_PATH2 = "\\Data\\python\\"

"""
# the initial timer is triggered, follow up the keys in the pressablekeys
# contribution by Makoto Sugano
def pressablekeys_followup():
    escancode_isdown = app.pressablekeys_isdown()
    if (escancode_isdown):
        timer.cancel()
        app.pressablekeys_process(escancode_isdown)
        timer.after(0.1, pressablekeys_followup)
    else:
        timer.cancel()
"""


def get_path(app_name):
    drives_list = e32.drive_list()
    #Gives preference to load from drive 'E:'
    drives_list.reverse()
    for drive in [str(x) for x in drives_list]:
        if os.path.isfile(os.path.join(drive, TESTE_PATH1, app_name)):
            return os.path.join(drive, TESTE_PATH1)
        elif os.path.isfile(os.path.join(drive, TESTE_PATH2, app_name)):
            return os.path.join(drive, TESTE_PATH2)
    return None


full_path = get_path('testeJson.py') 


sys.path.append(full_path)


import simplejson

print dir(simplejson)

print "OK!! Funcionando!!!"




