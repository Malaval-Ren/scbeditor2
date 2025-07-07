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

""" Module to manage write log text to a storage """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# pylint: disable=too-many-instance-attributes
# ###############################################################################################

import platform

from datetime import datetime

# from .my_log_mail import MyLogMail
from .my_log_txt import MyLogText

# __name__ = "MyLogAnUsage"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# ####################### MyLogAnUsage ########################
class MyLogAnUsage:
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

    _instance = None

    # ####################### __new__ ########################
    def __new__( cls, list_application_info=None, s_storage=None) -> 'MyLogAnUsage':
        """ Instantiate a singleton class """
        if MyLogAnUsage._instance is None:
            MyLogAnUsage._instance = object.__new__( cls)
            MyLogAnUsage._a_list_application_info = list_application_info
            MyLogAnUsage._s_storage = s_storage
            MyLogAnUsage.__b_log_is_enabled = False
            MyLogAnUsage.s_log_text = ""
            MyLogAnUsage.s_log_latest_text = ""
            MyLogAnUsage._instance._b_sealed = False
            MyLogAnUsage.c_the_log = None

        return MyLogAnUsage._instance

    # ####################### __init__ ########################
    def __init__( self, list_application_info=None, s_storage=None):
        """ Find and configure process available to send a log mail """
        if not self._instance._b_sealed:
            self.s_log_text = ""
            self.s_log_latest_text = ""
            self.s_platform = platform.system()
            self.list_application_info = list_application_info
            self.set_log_mode( s_storage)
            self._instance._b_sealed = True

    # ####################### __add_log ########################
    def __add_log( self, s_text):
        """ Add log private text string to __s_log_text """
        if s_text != "":
            self.s_log_text = self.s_log_text + s_text + '\n'

    # ####################### set_log_mode ########################
    def get_last_log( self) -> str:
        """ Return last log added """
        return self.s_log_latest_text

    # ####################### set_log_mode ########################
    def set_log_mode( self, s_storage):
        """ Changing mode of log ie before and after configuration load """
        if s_storage is None :
            self._s_storage = 'private'
            self.__b_log_is_enabled = False
        else:
            if s_storage is None:
                self._s_storage = 'private'
                self.__b_log_is_enabled = False
            elif self._s_storage != s_storage:
                if s_storage == 'mail':
                    # feature removed
                    self.__b_log_is_enabled = False
                elif s_storage == 'file':
                    self.c_the_log = MyLogText( self._a_list_application_info)
                    self.s_log_text = self.s_log_text[:-1]  # remove the last char : '\n'
                    self.c_the_log.add_log( self.s_log_text)
                    self.s_log_text = ""
                    self.__b_log_is_enabled = True

    # ####################### send_log_enabled ########################
    def send_log_enabled( self):
        """ Send the string __s_email_body by email by the Outlook application """
        self.__b_log_is_enabled = True

    # ####################### send_log_disabled ########################
    def send_log_disabled( self):
        """ Send the string __s_email_body by email by the Outlook application """
        self.__b_log_is_enabled = False

    # ####################### add_string_to_log ########################
    def add_string_to_log( self, s_body_line):
        """ Concat an action done in application. This is the log string """
        self.s_log_latest_text = s_body_line
        if self.__b_log_is_enabled is True:
            self.c_the_log.add_log( s_body_line)
        else:
            self.__add_log( s_body_line)

    # ####################### add_date_to_log ########################
    def add_date_to_log( self):
        """ Concat date string. This is first and last string line of the log string """
        # datetime object containing current date and time
        __now = datetime.now()
        # dd/mm/YY H:M:S
        __s_dt_string = __now.strftime( "%d/%m/%Y %H:%M:%S")
        # print("date and time =", dt_string)
        if self.__b_log_is_enabled is True:
            self.c_the_log.add_log( __s_dt_string)
        else:
            self.__add_log( __s_dt_string)

    # ####################### write_log ########################
    def write_log( self):
        """ Select and use the available method to write log """
        if self.__b_log_is_enabled is True:
            self.c_the_log.write_log()
        else:
            self.s_log_text = ""
