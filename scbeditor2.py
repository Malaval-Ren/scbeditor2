#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# An application to do modification of bmp file to prepare convertion to a Apple IIGS pic file.
#
# Copyright (C) 2023-2024 Renaud Malaval <renaud.malaval@free.fr>.
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Coding rule (added to PEP8) :

b_ this is a boolean
x_ this is bits
i_ this is an integer
f_ this is a float
s_ this is a string
w_ this is a windows widget
a_ this is a widget
t_ this is a thread

__method pour les méthodes ou variable privées
_method pour les méthodes ou variable protégées

"""

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = line-too-long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import os
import sys
import platform
from datetime import datetime

# GUI
import tkinter as tk_gui
import tkinter.font as tkFont

# Source code of the application
import src.my_constants as constant
from src.my_tools import mt_force_exit_application, mt_get_memory_used
from src.my_log_an_usage import MyLogAnUsage
from src.my_main_window import MyMainWindow

# ###############################################################################################
# #######========================= constant private =========================
# Owned
__softname__ = constant.MY_APPLICATION_NAME
__author__ = "Renaud Malaval"
__copyright__ = "Copyright © 2023-2024, Disk Crack Band"
__credits__ = ["Frédéric Mure",
               "Patrice Afflatet",
               "Reion: https://www.flaticon.com/authors/reion",
               "Pixelmeetup: https://www.flaticon.com/authors/pixelmeetup",
               "HJ Studio: https://www.flaticon.com/authors/hj-studio",
               ]
__license__ = "GNU GPLv3"
s_check_platform = platform.system()
if s_check_platform == 'Linux':
    __version__ = "2.2.9-27"
else:
    __version__ = "2.2.9.27"
__maintainer__ = "Renaud Malaval"
__contact__ = "renaud.malaval@free.fr"
__status__ = "Production"

LIST_APPLICATION_INFO = [ __softname__,
                        __author__,
                        __copyright__,
                        __credits__,
                        __license__,
                        __version__,
                        __maintainer__,
                        __contact__,
                        __status__,
                        ]

# ###############################################################################################
# #######========================= variable =========================
# ###############################################################################################
# ####################### print_application_info ########################
def __print_application_info():
    """ Print application info """
    print()
    print( ' ' + __softname__ + '\t\t\t: v' + __version__)
    print( ' ' + __softname__ + ' - Author\t\t: ' + __author__)
    print()
    print( ' ' + __softname__ + ' - Python\t\t: v' + str( sys.version))
    print( ' ' + __softname__ + ' - tkinter\t: v' + str( tk_gui.TkVersion))
    print()

    s_platform = platform.system()
    if s_platform == "Linux":
        print( ' ' + __softname__ + '\t\t\t: ' + s_platform)
    elif s_platform == "Windows":
        print( ' ' + __softname__ + '\t\t\t: ' + s_platform)
    elif s_platform == "Darwin":
        print( ' ' + __softname__ + '\t\t\t: ' + s_platform)
    else:
        print( ' ' + __softname__ + '\t\t\t: ' + s_platform + ' not supported.')
        mt_force_exit_application( 1)

    print( ' ' + __softname__ + '\t\t\t: ' + platform.machine() )
    print( ' ' + __softname__ + '\t\t\t: ' + platform.architecture()[0] )
    print( ' ' + __softname__ + '\t\t\t: ' + platform.architecture()[1] )
    print( ' ' + __softname__ + '\t\t\t: ' + platform.release() )
    print()
    print( ' ' + __softname__ + '\t\t\t: ' + os.getcwd() )
    print()

# ####################### print_font_info ########################
def __print_font_info( s_font_tkinter_name):
    """ Print application font info """
    a_default_font = tkFont.nametofont( s_font_tkinter_name)
    a_actual_font = a_default_font.actual()
    i_loop = 0
    for key, value in a_actual_font.items():
        print( f'main() : {str( s_font_tkinter_name)} - {str( i_loop)} - {key} -> {value}')
        i_loop += 1
    print()

    # ##########################################################################################
    # https://manytools.org/hacker-tools/ascii-banner/
    #
    # #    #   ##   ### #    #
    # ##  ##  #  #   #  ##   #
    # # ## # #    #  #  # #  #
    # #    # ######  #  #  # #
    # #    # #    #  #  #   ##
    # #    # #    # ### #    #
    #
    # ##########################################################################################

# ####################### main ########################
def main():
    """ The entry function of the application """
    _now = datetime.now()
    # dd/mm/YY H:M:S
    _s_dt_string = _now.strftime( "%d/%m/%Y %H:%M:%S")
    __print_application_info()

    c_the_log = MyLogAnUsage( LIST_APPLICATION_INFO, None)
    c_the_log.add_string_to_log( _s_dt_string)
    c_the_log.add_string_to_log( 'Starting ' + __softname__ + ' release : ' + __version__)

    a_root_windows = tk_gui.Tk()
    a_root_windows.configure( bg=constant.BACKGROUD_COLOR_UI) # 'blue'
    a_root_windows.withdraw()

    # Create the application main windows
    a_root_windows.update()
    a_root_windows.deiconify()
    c_my_main_window = MyMainWindow( a_root_windows, LIST_APPLICATION_INFO)
    mt_get_memory_used( c_my_main_window)
    c_my_main_window.mw_create_main_window()
    mt_get_memory_used( c_my_main_window)
    # c_my_main_window.mw_load_main_window()

    __print_font_info( 'TkDefaultFont')
#    __print_font_info( 'TkMenuFont')
#    __print_font_info( 'TkFixedFont')

    a_root_windows.mainloop()

    c_the_log.add_date_to_log()
    c_the_log.write_log()
    print( 'main() : end')

# ###############################################################################################
# ####################### Entry point ########################
# wrapper(main)
if __name__ == "__main__":
    main()
