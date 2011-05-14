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

import appuifw
import e32
import sys
import os

#PYTRUCOS60_UID = u"ef080808"

PYTRUCOS60_PATH1 = "\\Python\\"
PYTRUCOS60_PATH2 = "\\Data\\python\\"
PYTRUCOS60_PATH3 = "\\Private\\ef0b4099\\"
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
        if os.path.isfile(os.path.join(drive, PYTRUCOS60_PATH1, app_name)):
            return os.path.join(drive, PYTRUCOS60_PATH1)
        elif os.path.isfile(os.path.join(drive, PYTRUCOS60_PATH2, app_name)):
            return os.path.join(drive, PYTRUCOS60_PATH2)
#        elif os.path.isfile(os.path.join(drive, PYTRUCOS60_PATH3, app_name)):
#            return os.path.join(drive, PYTRUCOS60_PATH3)
    return None


full_path = get_path('default.py') 
if full_path == None:
    full_path = get_path('default.py')
    if full_path == None:
        appuifw.note(u'Usando fallback path')
        full_path = u'C:\\' + u'Private' + u'\\' + PYTRUCOS60_UID + u'\\'


sys.path.append(os.path.join(full_path, "pytruco","libs"))



from game import *


app = Game(os.path.join(full_path, "pytruco"))


timer = e32.Ao_timer()

flag = 1
while flag:
    if (app.running == 1):
        escancode_pressed = app.pressablekeys_pressed()
        if (escancode_pressed):
            timer.cancel()
            app.pressablekeys_process(escancode_pressed)
            timer.after(1.5, pressablekeys_followup)
        else:
            app.otherkeys_process()
    elif app.running == -1:
        flag = 0
    e32.ao_yield()

