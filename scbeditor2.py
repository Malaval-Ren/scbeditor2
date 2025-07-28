#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# An application to do modification of bmp file to prepare convertion to a Apple IIGS pic file.
#
# Copyright (C) 2023-2025 Renaud Malaval <renaud.malaval@free.fr>.
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
import re

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
__softname__    = ""
__author__      = ""
__copyright__   = ""
__credits__     = ["Frédéric Mure",
                    "Patrice Afflatet",
                    "Reion: https://www.flaticon.com/authors/reion",
                    "Pixelmeetup: https://www.flaticon.com/authors/pixelmeetup",
                    "HJ Studio: https://www.flaticon.com/authors/hj-studio",
                    ]
__license__     = ""
__version__     = ""
__contact__     = ""
__status__      = "Production"
__buildDate__   = ""
__companyName__ = ""

LIST_APPLICATION_INFO = [ __softname__,
                        __author__,
                        __copyright__,
                        __credits__,
                        __license__,
                        __version__,
                        __contact__,
                        __status__,
                        __buildDate__,
                        __companyName__
                        ]

# ###############################################################################################
# #######========================= variable =========================
# ###############################################################################################
# ####################### print_application_info ########################
def __print_application_info( c_the_log, list_application_info):
    """ Print application info """
    if c_the_log:
        c_the_log.add_string_to_log( '\n ' + list_application_info[0] + '\t\t\t: v' + list_application_info[5])
        c_the_log.add_string_to_log( ' ' + list_application_info[0] + ' - Author\t\t: ' + list_application_info[1])
        c_the_log.add_string_to_log( '\n ' + list_application_info[0] + ' - Python\t\t: v' + str( sys.version))
        c_the_log.add_string_to_log( ' ' + list_application_info[0] + ' - tkinter\t: v' + str( tk_gui.TkVersion) + '\n')

        s_platform = platform.system()
        if s_platform == "Linux":
            c_the_log.add_string_to_log( ' ' + list_application_info[0] + '\t\t\t: ' + s_platform)
        elif s_platform == "Windows":
            c_the_log.add_string_to_log( ' ' + list_application_info[0] + '\t\t\t: ' + s_platform)
        elif s_platform == "Darwin":
            c_the_log.add_string_to_log( ' ' + list_application_info[0] + '\t\t\t: ' + s_platform)
        else:
            c_the_log.add_string_to_log( ' ' + list_application_info[0] + '\t\t\t: ' + s_platform + ' not supported.')
            mt_force_exit_application( 1)

        c_the_log.add_string_to_log( ' ' + list_application_info[0] + '\t\t\t: ' + platform.machine() )
        c_the_log.add_string_to_log( ' ' + list_application_info[0] + '\t\t\t: ' + platform.architecture()[0] )
        c_the_log.add_string_to_log( ' ' + list_application_info[0] + '\t\t\t: ' + platform.architecture()[1] )
        c_the_log.add_string_to_log( ' ' + list_application_info[0] + '\t\t\t: ' + platform.release() )
        c_the_log.add_string_to_log( '\n ' + list_application_info[0] + '\t\t\t: ' + os.getcwd() + '\n')

# ####################### print_font_info ########################
def __print_font_info( c_the_log, s_font_tkinter_name):
    """ Print application font info """
    if c_the_log:
        a_default_font = tkFont.nametofont( s_font_tkinter_name)
        a_actual_font = a_default_font.actual()
        i_loop = 0
        for key, value in a_actual_font.items():
            c_the_log.add_string_to_log( f'main() : {str( s_font_tkinter_name)} - {str( i_loop)} - {key} -> {value}')
            i_loop += 1
        c_the_log.add_string_to_log( '\n')

# ####################### __resource_path ########################
def __resource_path( s_relative_path) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    s_pictures_folder = None
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # pylint: disable=protected-access
        s_pictures_folder = os.path.join( sys._MEIPASS, os.path.basename( s_relative_path))
        # pylint: enable=protected-access
    else:
        s_pictures_folder = os.path.join( os.path.abspath("."), s_relative_path)

    return s_pictures_folder

# ####################### __get_app_version ########################
def __get_app_version( s_ligne) -> str:
    """ Get the version, verify format and convvert it if Linux platform"""
    s_version = ''
    match = re.search( r"u'(\d+\.\d+\.\d+\.\d+)'", s_ligne)
    if match:
        s_version = match.group(1)
        if platform.system() == 'Linux':
            parts = s_version.split('.')
            if len(parts) >= 4:
                # Remplacer le 3e point (entre 27 et 125) par un tiret, par exemple
                s_version = '.'.join(parts[:3]) + '-' + parts[3]
    else:
        print( "Version not found.")
        sys.exit( int( 1))

    return s_version

# ####################### __get_licence_copyright_owner ########################
def __get_licence_copyright_owner( s_ligne, list_application_info):
    """ Get from s_ligne licence, copyright, author"""
    s_match = re.search( r"StringStruct\(u'[^']+', u'([^']+)'\)", s_ligne)
    if s_match:
        s_valeur = s_match.group(1)
        # 1. Découper la valeur
        # a. Séparer à " Copyright"
        licence_part, rest = s_valeur.split( " Copyright", 1)
        list_application_info[4] = licence_part.strip()
        # 2. Le reste commence par "Copyright"
        # Séparer à la première virgule
        copyright_part, author_part = rest.split( ",", 1)
        list_application_info[2] = f"Copyright {copyright_part.strip()}"
        # 3. Le reste aprsè la virgule
        list_application_info[1] = author_part.strip()

        # valeur = match.group(1)  # Ex : 'GNU GPLv3 Copyright © 2023 … 2025, Renaud Malaval'

        # # 2. Découper la valeur
        # # a. Séparer à " Copyright"
        # licence_part, rest = valeur.split(" Copyright", 1)
        # s_licence = licence_part.strip()

        # # b. Le reste commence par "Copyright"
        # # Séparer à la première virgule
        # copyright_part, owner_part = rest.split(",", 1)
        # s_copyright = f"Copyright{copyright_part.strip()}"
        # s_owner = owner_part.strip()

    else:
        print( "Licence, Copyright and Author not found.")
        sys.exit( int( 1))

# ####################### __get_sentense ########################
def __get_sentense( s_ligne ) -> str:
    s_sentence = ''
    match = re.search( r"StringStruct\(u'[^']+', u'([^']+)'\)", s_ligne)
    if match:
        s_sentence = match.group(1)
    else:
        print( "Sentense not found.")
        sys.exit( int( 1))

    return s_sentence

# ####################### print_font_info ########################
def __get_app_informations( list_application_info):
    """
        __softname__,   # 0
        __author__,     # 1
        __copyright__,  # 2
        __credits__,    # 3
        __license__,    # 4
        __version__,    # 5
        __contact__,    # 6
        __status__,     # 7
        __buildDate__,  # 8
        __companyName__ # 9
    """
    s_version_file_name = __resource_path( "scbeditor2_version.txt")
    if os.path.exists( s_version_file_name):
        with open( s_version_file_name, 'r', encoding='utf-8') as the_file:
            for s_ligne in the_file:
                # nothing is done for 3 __credits__ and 7 __status__ fixed by constant
                if s_ligne.strip().startswith("StringStruct(u'CompanyName"):
                    # 9 __companyName__
                    list_application_info[9] = __get_sentense( s_ligne)
                elif s_ligne.strip().startswith("StringStruct(u'LegalCopyright"):
                    # 1 __author__, 2 __copyright__ and 4 __license__
                    __get_licence_copyright_owner( s_ligne, list_application_info)
                elif s_ligne.strip().startswith("StringStruct(u'ProductName"):
                    # 0 __softname__
                    list_application_info[0] = __get_sentense( s_ligne)
                elif s_ligne.strip().startswith("StringStruct(u'ProductVersion"):
                    # 5 __version__
                    list_application_info[5] = __get_app_version( s_ligne)
                elif s_ligne.strip().startswith("StringStruct(u'BuildDate"):
                    # 8 __buildDate__
                    list_application_info[8] = __get_sentense( s_ligne)
                elif s_ligne.strip().startswith("StringStruct(u'Maintainer"):
                    # 6 __contact__
                    list_application_info[6] = __get_sentense( s_ligne)
                    break

    else:
        print( f"Version file : {s_version_file_name} not found.")
        sys.exit( int( 1))

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
def main( a_list_argv):
    """ The entry function of the application """
    i_value_for_exit = 0

    __get_app_informations( LIST_APPLICATION_INFO)

    if getattr( sys, 'frozen', False) and hasattr( sys, '_MEIPASS'):
        c_the_log = MyLogAnUsage( LIST_APPLICATION_INFO, '')
    else:
        # c_the_log = MyLogAnUsage( LIST_APPLICATION_INFO, 'file')
        c_the_log = MyLogAnUsage( LIST_APPLICATION_INFO, 'console')

    c_the_log.add_date_to_log( ' ' + LIST_APPLICATION_INFO[0] + '\t\t\t: ')

    __print_application_info( c_the_log, LIST_APPLICATION_INFO)

    a_root_windows = tk_gui.Tk()

    a_root_windows.configure( bg=constant.BACKGROUD_COLOR_UI) # 'blue'
    # a_root_windows.withdraw()

    # Create the application main windows
    a_root_windows.update()
    a_root_windows.deiconify()
    c_my_main_window = MyMainWindow( a_root_windows, LIST_APPLICATION_INFO)
    mt_get_memory_used( c_my_main_window)
    c_my_main_window.mw_create_main_window()
    mt_get_memory_used( c_my_main_window)

    __print_font_info( c_the_log, 'TkDefaultFont')
#    __print_font_info( c_the_log, 'TkMenuFont')
#    __print_font_info( c_the_log, 'TkFixedFont')

    if len( a_list_argv) == 2:
        if os.path.exists(a_list_argv[1]) is True:
            s_filepathname = a_list_argv[1].lower()
            if s_filepathname[-4:] == ".bmp":
                c_my_main_window.mw_load_this_picture( s_filepathname)

    a_root_windows.mainloop()

    c_the_log.add_date_to_log()
    c_the_log.write_log()
    c_the_log.add_string_to_log( 'main() : end')

    return int( i_value_for_exit)

# ###############################################################################################
# ####################### Entry point ########################
# wrapper(main)
if __name__ == "__main__":
    sys.exit( int( main( sys.argv)) )
