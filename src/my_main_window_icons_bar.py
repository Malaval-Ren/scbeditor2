#!/usr/bin/python3
# -*- coding: utf-8 -*-
# script by  Renaud Malaval

""" Module de creation de la bare d'icon de la fenetre principale. """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# number is reasonable in this case these are all the icons of the main windows and the application icons
# pylint: disable=too-many-instance-attributes
# ###############################################################################################

import platform

from tkinter import Button

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_about_window import MyAboutWindow

# __name__ = "MyMainWindowIconsBar"

# ###############################################################################################
# #######========================= constant private =========================


# ###############################################################################################
# #######=========================     GUI     =========================
# ####################### MyMainWindow ########################
class MyMainWindowIconsBar:
    """ Create the icon bar to the main Windows of the application. """

    # ####################### __init__ ########################
    def __init__( self, c_main_class, w_main_windows, list_application_info, a_top_frame_of_main_window):
        """
            All this parameter comme from main()
            c_main_class :
            w_main_windows : the windows created by tk
            a_list_application_info : les inforamtions de l'application
            a_top_frame_of_main_window :
        """
        self.c_main_window = c_main_class
        self.w_main_windows = w_main_windows
        self.a_list_application_info = list_application_info
        self.a_top_frame_of_main_window = a_top_frame_of_main_window
        self.a_dico_mw_gui_element = None
        self.w_front_window = None
        self.c_the_log = MyLogAnUsage( None)
        self.c_the_icons = MyIconPictures( None)
        self.s_platform = platform.system()

    # ####################### __about_dialog_box ########################
    def __mwib_about_dialog_box( self):
        """ Button about of the main window """
        self.c_the_log.add_string_to_log( 'Do about')
        self.w_front_window = MyAboutWindow( self.c_main_window, self.a_list_application_info)
        self.w_front_window.aw_create_about_window()
        self.w_front_window = None

    # ####################### __mwib_open_box ########################
    def __mwib_open_box( self):
        """ Button preference of the main window """
        self.c_the_log.add_string_to_log( 'Do load picture')
        self.c_main_window.mw_load_main_window()

    # ####################### __mwib_save_box ########################
    def __mwib_save_box( self):
        """ Button configuration of the main window """
        self.c_the_log.add_string_to_log( 'Do save picture')
        self.c_main_window.bell()
        self.c_main_window.bell()
        # self.w_front_window = MyConfigurationWindow( self.c_main_window)
        # self.w_front_window.cw_create_configuration_window()
        # self.w_front_window = None

    # ##########################################################################################
    # #######################                                           ########################
    # #######################                   PUBLIC                  ########################
    # #######################                                           ########################
    # ##########################################################################################

    # ####################### mwib_create_top_bar_icons ########################
    def mwib_create_top_bar_icons( self, i_row_line):
        """ Design the top row for the main windows """
        # print( "mw_top_bar_icons_cmd() color : " + self.w_main_windows['background'])

        s_button_style = 'flat'
        i_column = 0
        if self.s_platform == "Darwin":
            a_button_about = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_about_photo(), compound="c", command=self.__mwib_about_dialog_box, relief=s_button_style, highlightbackground='light grey')
        else:
            a_button_about = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_about_photo(), compound="c", command=self.__mwib_about_dialog_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
        a_button_about.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse' )

        i_column += 1
        if self.s_platform == "Darwin":
            a_button_preference = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_open_photo(), compound="c", command=self.__mwib_open_box, relief=s_button_style, highlightbackground='light grey')
        else:
            a_button_preference = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_open_photo(), compound="c", command=self.__mwib_open_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
        a_button_preference.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'

        i_column += 1
        if self.s_platform == "Darwin":
            a_button_config = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_save_photo(), compound="c", command=self.__mwib_save_box, relief=s_button_style, highlightbackground='light grey')
        else:
            a_button_config = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_save_photo(), compound="c", command=self.__mwib_save_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
        a_button_config.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'

        i_row_line += 1
        return i_row_line

    # ####################### mwib_get_frame ########################
    def mwib_get_frame( self):
        """ return frame to be able to add new elements """
        return self.a_top_frame_of_main_window
