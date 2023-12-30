#!/usr/bin/python3
# -*- coding: utf-8 -*-
# script by  Renaud Malaval

"""Module de gestion d'émission des logs dans un mail."""

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# Disable E0401 = Unable to import 'win32com.client.dynamic' (import-error) on Linux
# pylint: disable=line-too-long
# pylint: disable=too-many-instance-attributes
# pylint: disable=import-error
# ###############################################################################################

import os
import platform

if platform.system().lower().startswith('win'):
    import win32com.client.dynamic

# __name__ = "MyLogMail"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# ####################### MyLogMail ########################
class MyLogMail:
    """
    Classe to create a log mail during usage of the application.
    first and last line are date and times
    This mail is sended at the end of the application
    """

    _instance = None

    # ####################### __new__ ########################
    def __new__( cls, list_application_info=None):
        """ Instantiate a singleton class """
        if MyLogMail._instance is None:
            # if list_application_info is not None:
            #     print( ' ' + list_application_info[9] + '\t\t: New class : MyLogMail')
            MyLogMail._instance = object.__new__( cls)
            MyLogMail._a_list_application_info = list_application_info
            MyLogMail._instance._b_sealed = False

        return MyLogMail._instance

    # ####################### __init__ ########################
    def __init__( self, list_application_info=None):
        """ Find and configure process available to send a log mail """
        if self._instance._b_sealed:
            return

        # if self._a_list_application_info is not None:
        #     print( ' ' + self._a_list_application_info[9] + '\t\t: Init class : MyLogMail')
        self.__s_email_body = ""
        self.__mail_by_outlook = None
        if self._a_list_application_info is not None:
            self.__softname = self._a_list_application_info[0]
            self.__version = self._a_list_application_info[5]
            self.__app_base_file_name = self._a_list_application_info[9]
        elif list_application_info is not None:
            self.__softname = list_application_info[0]
            self.__version = list_application_info[5]
            self.__app_base_file_name = list_application_info[9]
        else:
            self.__softname = ""
            self.__version = ""
            self.__app_base_file_name = ""

        self.s_platform = platform.system()
        if self.s_platform == "Windows":
            self.__b_email_is_enabled = True
            try:
                self.__mail_by_outlook = win32com.client.dynamic.Dispatch( 'outlook.application')
            except ValueError:
                # on Windows but outlook is not installed
                self.__mail_by_outlook = None
                self.__b_email_is_enabled = False
                print( ' ' + self.__app_base_file_name + '\t\t: log email windows is disabled')

                # Here use an other method to send a mail ie sntp
            else:
                print( ' ' + self.__app_base_file_name + '\t\t: log email windows outlook is enabled')
        elif self.s_platform == 'Linux':
            self.__b_email_is_enabled = False
        elif self.s_platform == 'Darwin':
            self.__b_email_is_enabled = False
        else:
            self.__b_email_is_enabled = False

        if self.__b_email_is_enabled is False:
            if self.s_platform != "Windows":
                print( ' ' + self.__app_base_file_name + '\t\t: log email is disabled')
        self._instance._b_sealed = True

    # ####################### add_log ########################
    def add_log( self, s_text):
        """ Concat an action done in application. This is the body of the mail """
        if s_text != "":
            self.__s_email_body = self.__s_email_body + s_text + '\n'

    # ####################### write_log ########################
    def write_log( self):
        """ write the string __s_log_Text to send a mail """
        if self.__b_email_is_enabled is True:
            if self.s_platform == "Windows":
                if self.__mail_by_outlook is not None:
                    self.__send_mail_by_outlook()
                else:
                    print( self.__s_email_body)
            elif self.s_platform == 'Linux':
                print( self.__s_email_body)
            elif self.s_platform == 'Darwin':
                print( self.__s_email_body)
            else:
                print( self.__s_email_body)

        self.__s_email_body = ""

    # ####################### __send_mail_by_outlook ########################
    def __send_mail_by_outlook( self):
        """ Send the string __s_email_body by email by the Outlook application """
        if self.s_platform == "Windows":
            try:
                # import win32com.client
                self.__mail_by_outlook = win32com.client.dynamic.Dispatch( 'outlook.application')
                self.__b_email_is_enabled = True
            except ValueError:
                self.__b_email_is_enabled = False
            else:
                __mail = self.__mail_by_outlook.CreateItem( 0)
                __mail.To = 'renaud.malaval@free.fr'   # mail du destinataire
                __mail.Subject = os.getlogin() + '  ' + self.__softname + '  v' + self.__version
                if self.__s_email_body == '':
                    self.__s_email_body = 'nothing was done.'
                __mail.Body = self.__s_email_body
                # mail.HTMLBody = '<h2>HTML Message body CASA</h2>'; #this field is optional
                __mail.Send()
