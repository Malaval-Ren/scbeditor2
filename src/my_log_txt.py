#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This is an application to do modification of bmp file to prepare convertion to a AIIGS pic file.
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

""" Module to wrtie logs in a text file """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import os
import platform
import io

from datetime import datetime

from .my_tools import get_path_separator

# __name__ = "MyLogText"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# ####################### MyLogText ########################
class MyLogText:
    """
    Classe to create a log usage during life of the application.
    2 capabilities mail or text file, (think if its could be beter in .rtf or .md format)
    mail:
        Content is created during usage of the application. and send on application exist
    file:
        File is created with mame of the month user name and application name (without space)
        Content is created during usage of the application. and write on application exist
    windows :
        mail or file
    linux :
        file
    Mac OS :
        file
    """
    # pylint: disable=too-many-instance-attributes

    _instance = None

    # ####################### __new__ ########################
    def __new__( cls, list_application_info=None):
        """ Instantiate a singleton class """
        if MyLogText._instance is None:
            MyLogText._instance = object.__new__( cls)
            MyLogText._a_list_application_info = list_application_info
            MyLogText.s_platform = ''
            MyLogText.s_separator = ''
            MyLogText._s_log_file_pathname = ''
            MyLogText._s_log_file_name = list_application_info[0]
            MyLogText._instance._b_sealed = False

        return MyLogText._instance

    # ####################### __init__ ########################
    def __init__( self, list_application_info=None):
        """ Find and configure process available to write a log text file """
        if self._instance._b_sealed:
            return

        self._a_list_application_info = list_application_info
        self.__s_log_text = ""
        self.s_platform = platform.system()
        self.s_separator = get_path_separator( self.s_platform)

        # Replace ' ' by character '_'
        self._s_log_file_name = self._s_log_file_name.replace( ' ', '_', 2)
        # print( '__init__() : _s_log_file_name     = ' + self._s_log_file_name + '\n')

        if self.set_log_pathname() is False:
            # print( '__init__() : _s_log_file_pathname = ' + self._s_log_file_pathname + '\n')
            pass
        else:
            print( '__init__() : Failed to create pathname')

        if self.set_log_filename() is False:
            # print( '__init__() : _s_log_file_name     = ' + self._s_log_file_name + '\n')
            pass
        else:
            print( '__init__() : Failed to create filename')
        self._instance._b_sealed = True

    # ####################### add_log ########################
    def add_log( self, s_text):
        """ add log text string to __s_log_text """
        if s_text != "":
            self.__s_log_text = self.__s_log_text + s_text + '\n'

    # ####################### write_log ########################
    def write_log( self):
        """ write the string __s_log_text to text file """
        if self.s_platform == "Windows":
            self.__write_file_win()
        elif self.s_platform == 'Linux':
            self.__write_file_linux()
        elif self.s_platform == 'Darwin':
            self.__write_file_mac_os()
        else:
            print( self.__s_log_text)
        self.__s_log_text = ""

    # ####################### set_log_pathname ########################
    def set_log_pathname( self):
        """ Set the pathname to store the text file """
        b_error = True
        if self.s_platform == "Windows":
            self.__set_pathname_hidden_win()
            # print( 'set_log_pathname() : folder pathname = ' + self._s_log_file_pathname + '\n')
            self.__set_pathname_win()
            # print( 'set_log_pathname() : folder pathname = ' + self._s_log_file_pathname + '\n')
        elif self.s_platform == 'Linux':
            self.__set_pathname_linux()
        elif self.s_platform == 'Darwin':
            self.__set_pathname_mac_os()

        if self._s_log_file_pathname == '':
            # print( "set_log_pathname() : Failed")
            pass
        else:
            if os.path.exists( self._s_log_file_pathname) is False:
                os.mkdir( self._s_log_file_pathname)
            if os.path.exists( self._s_log_file_pathname) is True & os.path.isdir( self._s_log_file_pathname) is True:
                b_error = False

        return b_error

    # ####################### set_log_filename ########################
    def set_log_filename( self):
        """ Set the file name of the text file """
        # date and time object containing current date and time
        a_now = datetime.now()
        # YYYY-mm
        _s_dt_string = str( a_now.year) + '-' + str( a_now.month).zfill( 2) + '_'
        self._s_log_file_name = _s_dt_string + 'log_' + self._s_log_file_name + '.txt'

        return False

    # ####################### __set_pathname_win ########################
    def __set_pathname_win( self):
        """ Set pathname for Windows platform """
        self._s_log_file_pathname = os.getcwd() + self.s_separator

    # ####################### __set_pathname_hidden_win ########################
    def __set_pathname_hidden_win( self):
        """ Set pathname for Windows platform """
        self._s_log_file_pathname = os.path.join( os.path.expanduser('~'), self.s_separator, 'AppData', self.s_separator, 'Local', self.s_separator, "Schneider Electric", self.s_separator)

    # ####################### __set_pathname_mac_os ########################
    def __set_pathname_mac_os( self):
        """ Set pathname for Mac OS platform """
        self._s_log_file_pathname = os.path.join( os.path.expanduser('~'), self.s_separator, 'Documents', self.s_separator)

    # ####################### __set_pathname_linux ########################
    def __set_pathname_linux( self):
        """ Set pathname for Linux platform """
        self._s_log_file_pathname = os.getcwd() + self.s_separator

    # ####################### __write_file_win ########################
    def __write_file_win( self):
        """ Write log file for Windows platform """
        # Display the log on shell
        # print( '\n' + self.__s_log_text + '\n')
        s_complete_path = self._s_log_file_pathname + self._s_log_file_name
        if os.path.exists( s_complete_path) is True:
            s_open_mode = 'a'
        else:
            s_open_mode = 'w'

        with io.open( s_complete_path, s_open_mode, encoding='utf8') as log_file:
            if s_open_mode == 'a':
                log_file.write( '\n')
            log_file.write( self.__s_log_text)

        log_file.close()  # not needed done by usage of with

    # ####################### __write_file_mac_os ########################
    def __write_file_mac_os( self):
        """ Write log file for Mac OS platform """
        print( self.__s_log_text)

    # ####################### __write_file_linux ########################
    def __write_file_linux( self):
        """ Write log file for Linux platform """
        print( self.__s_log_text)
