#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This is an application to do modification of bmp file to prepare convertion to a AIIGS pic file.
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

"""Module de gestion des valeur de configuration."""

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import sys
import os

from tkinter import filedialog

# __name__ = "MyTools"

# #######========================= Exit and relaunch myself =========================
class MyExitWithRelaunch( ):
    """ Leave my application and re launch it """
    _instance = None

    # ####################### __new__ ########################
    def __new__( cls, argv=None, c_the_log=None):
        """ Instantiate a singleton class """
        if MyExitWithRelaunch._instance is None:
            MyExitWithRelaunch._instance = object.__new__( cls)
            if argv is not None:
                MyExitWithRelaunch.argv = []
                MyExitWithRelaunch.argv.append( argv[0])
            if c_the_log is not None:
                MyExitWithRelaunch.c_the_log = c_the_log
        return MyExitWithRelaunch._instance

    # ####################### mt_exit_end_relaunch ########################
    def mt_exit_end_relaunch( self):
        """ Close the log and relaunch myself """
        if self.c_the_log is not None:
            if '.exe' in self.argv[0]:
                self.c_the_log.add_string_to_log( "Relaunch : " + self.argv[0])
            else:
                self.c_the_log.add_string_to_log( "Relaunch script :")
                self.c_the_log.add_string_to_log( "argv[0] was        : " + self.argv[0])
                self.c_the_log.add_string_to_log( "sys.executable was : " + sys.executable)
            self.c_the_log.add_date_to_log()
            self.c_the_log.write_log()

        if '.exe' in self.argv[0]:
            os.execl( self.argv[0], *self.argv)
        else:
            # print( "argv was", sys.argv)
            # print( "sys.executable was", sys.executable)
            # print( "restart now")
            os.execv( sys.executable, ['python'] + self.argv)

# ###############################################################################################
# #######========================= constant private =========================

# ####################### mt_force_exit_application ########################
def mt_force_exit_application( i_error, c_the_log=None):
    """ Force exit of application """
    if c_the_log is not None:
        c_the_log.add_date_to_log()
        c_the_log.write_log()

    sys.exit( int( i_error))

# ####################### mt_get_path_separator ########################
def mt_get_path_separator( s_platform):
    """ Return the separator for pathname """
    if s_platform == "":
        s_separator = ""
    elif s_platform == "Linux":
        s_separator = "/"
    elif s_platform == "Windows":
        s_separator = "\\"
    elif s_platform == 'Darwin':
        s_separator = "/"
    else:
        s_separator = ""

    return s_separator

# ####################### mt_colored_string ########################
def mt_colored_string( red, green, blue, text):
    """ Do color print in bash shell and visual studio code """
    s_color = "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m"
    return s_color.format( red, green, blue, text)

# ####################### mt_get_memory_used ########################
def mt_get_memory_used( a_class):
    """ Compute size of in a class """
    print( 'get_memory_used() : self\t= ', str( sys.getsizeof( a_class)))

# ####################### mt_open_file ########################
def mt_open_file( w_main_windows, a_caller_class):
    """ Return the selected picture file or None """
    s_filename = None
    s_filename = filedialog.askopenfilename( parent=w_main_windows, initialdir=a_caller_class.mw_get_pathname(), title="Select BMP File", filetypes=[("BMP Files","*.bmp")])
    if s_filename and s_filename != "":
        a_caller_class.mw_set_pathname( os.path.dirname( s_filename))
    else:
        s_filename = None
        # return # user cancelled; stop this method

    return s_filename

# ####################### mt_save_file ########################
def mt_save_file( w_main_windows, a_caller_class, s_original_filename):
    """ Return the selected picture file or None """
    s_filename = None
    s_filename = filedialog.asksaveasfilename( parent=w_main_windows, initialfile=s_original_filename, initialdir=a_caller_class.mw_get_pathname(), title="Select BMP File", filetypes=[("BMP Files","*.bmp")])
    if s_filename and s_filename != "":
        a_caller_class.mw_set_pathname( os.path.dirname( s_filename))
    else:
        s_filename = None
        # return # user cancelled; stop this method

    return s_filename

# ####################### mt_hexlify_byte_string ########################
def mt_hexlify_byte_string( byte_string, delim="%") -> str:
    """ Very simple way to hexlify a byte string using delimiters 
        From :
        https://stackoverflow.com/questions/12214801/print-a-string-as-hexadecimal-bytes
        Big thank's to :
        https://stackoverflow.com/users/8265823/berndschmitt
        https://stackoverflow.com/users/63550/peter-mortensen
    """
    ret_val = ""
    for int_val in byte_string:
        ret_val += ('0123456789ABCDEF'[int( int_val / 16)])
        ret_val += ('0123456789ABCDEF'[int( int_val % 16)])
        ret_val += delim
    return ret_val[:-1]
