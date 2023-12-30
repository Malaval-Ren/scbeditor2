#!/usr/bin/python3
# -*- coding: utf-8 -*-
# script by  Renaud Malaval

"""
This script is an application to simplify modification of bmp file to prepare convertion to a AIIGS pic file.

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
# import base64
# Python mega widgets (module to add to Python 3.7.9)
# import Pmw
# from setuptools import setup, find_packages
# packages = find_packages(where='.', exclude=('.vscode', '__pycache__', '_Exemples', '_Help', '_Images', '_OLD_', '_old_version', '=SE= M221CE16R', 'build', 'dist', 'Fonts', 'Livraisons', 'Mail', 'rsc'))

# GUI
import tkinter as tk_gui
import tkinter.font as tkFont
from tkinter import messagebox

# Normal Tkinter.* widgets are not themed!   # Frame, Scale, LabelFrame,
# from tkinter import Label, Button, Entry, Checkbutton, IntVar, BooleanVar, Toplevel, messagebox, StringVar
# from tkinter.ttk import Separator, Combobox
# from ttkthemes              import ThemedTk, THEMES, ThemedStyle

#from PIL import Image
#from pillow import Image

# Source code of the application
import src.my_constants as constant
from src.my_tools import MyExitWithRelaunch, force_exit_application, get_memory_used
from src.my_log_an_usage import MyLogAnUsage
#from src.my_configuration_data import MyConfigurationData
#from src.my_configuration_data_gui import MyConfigurationDataGui
from src.my_main_window import MyMainWindow

# ###############################################################################################
# #######========================= constant private =========================
# Owned
__softname__ = constant.MY_APPLICATION_NAME
__author__ = "Renaud Malaval"
__copyright__ = "Copyright © 2023-2024, Disk Crack Band"
__credits__ = ["Frédéric Mure","Patrice Afflatet","Brutal Deluxe","Antoine Vignau","Olivier ZARDINI","https://www.flaticon.com/authors/reion"]
__license__ = "GNU GPLv3"
s_check_platform = platform.system()
if s_check_platform == 'Linux':
    __version__ = "2.0.1-07"
else:
    __version__ = "2.0.1.07"
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
    print( ' ' + __softname__ + '\t\t: v' + __version__)
    print( ' ' + __softname__ + ' - From\t: ' + __author__)
    print()
    print( ' ' + __softname__ + ' - Python\t: v' + str( sys.version))
    print( ' ' + __softname__ + ' - tkinter\t: v' + str( tk_gui.TkVersion))
    print()

    s_platform = platform.system()
    if s_platform == 'Linux':
        print( ' ' + __softname__ + '\t\t: ' + s_platform)
    elif s_platform == 'Windows':
        print( ' ' + __softname__ + '\t\t: ' + s_platform)
    elif s_platform == 'Darwin':
        print( ' ' + __softname__ + '\t\t: ' + s_platform)
    else:
        print( ' ' + __softname__ + '\t\t: ' + s_platform + ' not supported.')
        force_exit_application( 1)

    print( ' ' + __softname__ + '\t\t: ' + platform.machine() )
    print( ' ' + __softname__ + '\t\t: ' + platform.architecture()[0] )
    print( ' ' + __softname__ + '\t\t: ' + platform.architecture()[1] )
    print( ' ' + __softname__ + '\t\t: ' + platform.release() )
    print()
    print( ' ' + __softname__ + '\t\t: ' + os.getcwd() )
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

# #######========================= tkinter =========================
# ####################### main ########################
def main( argv):
    """ The entry function of the application """
    _now = datetime.now()
    # dd/mm/YY H:M:S
    _s_dt_string = _now.strftime( "%d/%m/%Y %H:%M:%S")

    __print_application_info()
    
    a_main_windows = tk_gui.Tk()
    a_main_windows.configure(bg=constant.BACKGROUD_COLOR_UI) # 'blue'
    a_main_windows.withdraw()

    # Create the application main windows
    a_main_windows.update()
    a_main_windows.deiconify()
    c_my_main_window = MyMainWindow( a_main_windows, LIST_APPLICATION_INFO)
    get_memory_used( c_my_main_window)
    c_my_main_window.mw_create_main_window()
    get_memory_used( c_my_main_window)
    # c_my_main_window.mw_load_main_window()

    __print_font_info( 'TkDefaultFont')
#    __print_font_info( 'TkMenuFont')
#    __print_font_info( 'TkFixedFont')

#    c_the_log = MyLogAnUsage( LIST_APPLICATION_INFO, None)
#    c_the_log.add_string_to_log( _s_dt_string)
#    c_the_log.add_string_to_log( 'Starting ' + __softname__ + ' release : ' + __version__)

    # s_log_text = 'main() : argv : '
    # for i_index in range( 0, len( argv), 1):
    #     s_log_text = s_log_text + argv[i_index] + " "
    # print( 'main() : s_display_mode\t\t= ' + s_log_text)
#    MyExitWithRelaunch( argv, c_the_log)

#    c_the_configuration_data = do_the_configuration( a_main_windows, c_the_log)
#    if c_the_configuration_data is not None:
#        c_the_log.set_log_mode( c_the_configuration_data.get_preference( 'WhereLog'))

#        print( 'main() : s_display_mode\t\t= ' + c_the_configuration_data.get_preference( 'DisplayMode'))
#        print( 'main() : s_temperature\t\t= ' + c_the_configuration_data.get_preference( 'Temperature'))
#        print( '\nmain() : number_of_device\t\t= ' + str( c_the_configuration_data.get_number_of_devices() ))
#        print( 'main() : the_big_number_of_ouput\t= ' + str( c_the_configuration_data.get_big_number_of_outputs() ))
#        print( 'main() : ListConfigurationLen\t\t= ' + str( c_the_configuration_data.get_list_configuration_len() ))
#        print()

        # #######=================================================
        # a_main_windows = Tk()
        # from tkinter import ttk # Normal Tkinter.* widgets are not themed!
        # from ttkthemes import ThemedTk
        # window = ThemedTk( theme="black")
        # window = ThemedTk( theme="blue")
        # a_main_windows = ThemedTk( theme="black")
        # if (platform.system() == "Linux"):
        #     aTheme = 'arc'
        #     a_main_windows = ThemedTk( theme = aTheme)
        #     style = ThemedStyle( a_main_windows)
        #     a_main_windows.update()
        #     a_main_windows.get_themes()
        #     a_main_windows.set_theme( aTheme)
        #     style.theme_use( aTheme)
        # elif (platform.system() == "Windows"):
        #     aTheme = 'winxpblue'
        #     a_main_windows = ThemedTk( theme = aTheme)
        #     style = ThemedStyle( a_main_windows)
        #     a_main_windows.update()
        #     a_main_windows.get_themes()
        #     a_main_windows.set_theme( aTheme)
        #     style.theme_use( aTheme)
        # else:
        #     print( "main() : Curently not managed")
        #
        # a_main_windows.update()

        # Create the application main windows
#        a_main_windows.update()
#        a_main_windows.deiconify()

#        c_my_main_window = MyMainWindow( a_main_windows, LIST_APPLICATION_INFO)
#        get_memory_used( c_my_main_window)
#        c_my_main_window.mw_create_main_window()
#        get_memory_used( c_my_main_window)

        # Debug info
        # for theme in THEMES:
        #     print( f'themes available : {theme}')
        # print ()

        # Gets both half the screen width/height and window width/height
#        i_screen_width = a_main_windows.winfo_screenwidth()
#        i_screen_height = a_main_windows.winfo_screenheight()
        # positionRight = int( (i_screen_width / 2) - (windowWidth / 2) )
        # positionDown = int( (i_screen_height / 2) - (windowHeight / 2) )
#        print( "main() : screen Width        : ", i_screen_width, "\tscreen Height : ", i_screen_height)

#        c_my_main_window.mw_display_debug_un()

#        c_the_configuration_data.cd_display_debug()
        #
        #  FONT MANAGEMENT OVER PLATFORM
        #
        # To add to set same font on any platform
        #
        # from tkinter import font
        # size = default_font.cget( "size")
        # default_font.configure( family='Segoe UI')
        # default_font.configure( weight='normal')
        # default_font.configure( slant='roman')
        # default_font.configure( underline=0)
        # default_font.configure( overstrike=0)
        # print( tkFont.families())
        # print( tkFont.names())
        # print( 'main() : families :')
        # i_loop = 0
        # for value in tkFont.families():
        #     print( f'main() : #{str( i_loop)} name - {value}')
        #     i_loop += 1
        # print( 'main() : names :')
        # i_loop = 0
        # for value in tkFont.names():
        #     print( f'main() : #{str( i_loop)} name - {value}')
        #     i_loop += 1
        # print()
        # Set the same font on any platform
#        print_font_info( 'TkDefaultFont')
#        print_font_info( 'TkMenuFont')
#        print_font_info( 'TkFixedFont')
        # if platform.system() == "Linux":
        #     a_default_font.configure( family='Segoe UI')
        #     a_default_font.configure( size=9)
        # elif platform.system() == 'Darwin':
        #     a_default_font.configure( family='Segoe UI')
        #     a_default_font.configure( size=9)
        # else:
        #     a_text_font ∑= tkFont.nametofont( 'TkTextFont')
        #     a_text_font_attribut = a_text_font.actual()
        #     i_loop = 0
        #     for key, value in a_text_font_attribut.items():
        #         print( f'main() : TkTextFont - {str( i_loop)} - {key} -> {value}')
        #         i_loop += 1
        #     print()

#        get_memory_used( c_my_main_window)

        # c_my_main_window.__getattribute__( w_main_windows)
        # print()
        # c_my_main_window.__class__()
        # print()
        # c_my_main_window.__dict__()

        # default for WINDOWS 10
        # main() : TkDefaultFont - 0 - family -> Segoe UI
        # main() : TkDefaultFont - 1 - size -> 9
        # main() : TkDefaultFont - 2 - weight -> normal
        # main() : TkDefaultFont - 3 - slant -> roman
        # main() : TkDefaultFont - 4 - underline -> 0
        # main() : TkDefaultFont - 5 - overstrike -> 0
        # default for LINUX MINT
        # main() : TkDefaultFont - 0 - family -> DejaVu Sans
        # main() : TkDefaultFont - 1 - size -> 10
        # main() : TkDefaultFont - 2 - weight -> normal
        # main() : TkDefaultFont - 3 - slant -> roman
        # main() : TkDefaultFont - 4 - underline -> 0
        # main() : TkDefaultFont - 5 - overstrike -> 0

    a_main_windows.mainloop()

#        c_my_main_window.mw_close_all_socket_client()

#    c_the_log.add_date_to_log()
#    c_the_log.write_log()
#    print( 'main() : end')

# ###############################################################################################
# ####################### Entry point ########################
# wrapper(main)
if __name__ == "__main__":
    main( sys.argv)
