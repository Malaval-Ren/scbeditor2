#!/usr/bin/python3
# -*- coding: utf-8 -*-
# script by  Renaud Malaval

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

    # ####################### exit_end_relaunch ########################
    def exit_end_relaunch( self):
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

# ####################### force_exit_application ########################
def force_exit_application( i_error, c_the_log=None):
    """ Force exit of application """
    if c_the_log is not None:
        c_the_log.add_date_to_log()
        c_the_log.write_log()

    sys.exit( int( i_error))

# ####################### get_path_separator ########################
def get_path_separator( s_platform):
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

# ####################### colored ########################
def colored_string( red, green, blue, text):
    """ Do color print in bash shell and visual studio code """
    s_color = "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m"
    return s_color.format(red, green, blue, text)

# ####################### get_memory_used ########################
def get_memory_used( a_class):
    """ Compute size of in a class """
    print( 'get_memory_used() : self                  = ', str( sys.getsizeof( a_class)))

# ####################### open_file ########################
def open_file(self):
    """ Return the selected picture file or None """
    s_filename = None
    s_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select BMP File", filetypes=[("BMP Files","*.bmp")])
    # if not filename:
        # return # user cancelled; stop this method

    return s_filename
