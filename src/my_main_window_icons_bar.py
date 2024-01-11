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
from PIL import Image

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_about_window import MyAboutWindow
from .my_alert_window import MyAlertWindow
# from .my_tools import mt_open_file, mt_get_path_separator
from .my_tools import mt_open_file

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
            All this parameters come from main()
            c_main_class : the lass who manage w_main_windows
            w_main_windows : the windows created by tk
            a_list_application_info : about information of this software
            a_top_frame_of_main_window :  the top frame
        """
        self.c_main_class = c_main_class
        self.w_main_windows = w_main_windows
        self.a_list_application_info = list_application_info
        self.a_top_frame_of_main_window = a_top_frame_of_main_window
        self.a_dico_mw_gui_element = None
        self.w_front_window = None
        self.c_the_log = MyLogAnUsage( None)
        self.c_the_icons = MyIconPictures( None)
        self.s_platform = platform.system()
        self.s_filename = None
        self.a_work_img = None

    # ####################### __mwib_convert_bmp ########################
    def __mwib_convert_bmp( self):
        """ Convert bmp 4 bpp to 8 bpp """
        # converted_bmp = Image.new( 'P', (320, 200), color=0)
        a_org_pal_list = self.a_work_img.getpalette()
        if a_org_pal_list and len( a_org_pal_list) == 48:
            converted_bmp = self.a_work_img.copy()
            a_conv_pal_list = converted_bmp.getpalette()

            # Copy the palettes
            for _ in range( 1, 16, 1):
                for i_index in range( 0, 48, 1):
                    a_conv_pal_list.append( a_org_pal_list[i_index])

            converted_bmp.putpalette( a_conv_pal_list, rawmode='RGB')
            a_conv_pal_list = converted_bmp.getpalette()
            # print( "\na_org_pal_list= " + str( len( a_org_pal_list)) + "   a_conv_pal_list= " + str( len( a_conv_pal_list)))

            # Debug : use an another name to save it and using it
            # s_path = os.path.dirname( self.s_filename)
            # self.s_filename = s_path + mt_get_path_separator( self.s_platform) + "beach1.bmp"

            converted_bmp.save( self.s_filename, 'BMP')
            self.a_work_img = Image.open( self.s_filename)
            print( 'Upgraded to 8 bpp : ' + self.s_filename)
        else:
            self.w_front_window = MyAlertWindow( self.c_main_class, self.a_list_application_info)
            self.w_front_window.aw_create_alert_window( 1, "BMP file not compatible", "This bmp file don't have 256 colors (1 or 2 bpp).")
            self.w_front_window = None
            self.a_work_img = None

    # ####################### __mwib_load_and_check_bmp ########################
    def __mwib_load_and_check_bmp( self):
        """ Check size and number of color in bmp """

        self.s_filename = mt_open_file( self.w_main_windows, self.c_main_class)
        if self.s_filename:
            print( '\nLoading : ' + self.s_filename)
            # resize the original bmp from 320x200 to 640x400
            self.a_work_img = Image.open( self.s_filename)
            width, height = self.a_work_img.size
            if width != 320 or height != 200:
                self.a_work_img = None
                # messagebox.showerror( "BMP file not compatible", "The size of bmp file must be 320 x 200, for Apple II GS.", parent=self.w_main_windows )
                self.w_front_window = MyAlertWindow( self.c_main_class, self.a_list_application_info)
                self.w_front_window.aw_create_alert_window( 1, "BMP file not compatible", "The size of bmp file must be 320 x 200, for Apple II GS.")
                self.w_front_window = None
            else:
                a_palette_list = self.a_work_img.getpalette()
                if len( a_palette_list) < 768:      # Less than 256 colors 2, 4 bpp
                    self.w_front_window = MyAlertWindow( self.c_main_class, self.a_list_application_info)
                    i_result = self.w_front_window.aw_create_alert_window( 2, "Question", "This bmp file don't have 256 colors (4 bpp).\nDo you agree improvement to 256 colors (8 bpp) and replace it?")
                    self.w_front_window = None
                    if i_result == 1:
                        self.__mwib_convert_bmp()
                elif len( a_palette_list) > 768:      # More than 256 colors 16, 24 or 32 bpp
                    self.w_front_window = MyAlertWindow( self.c_main_class, self.a_list_application_info)
                    i_result = self.w_front_window.aw_create_alert_window( 3, "BMP file not compatible", "The bmp file have to much colors.\nConvert it, please.")
                    self.w_front_window = None
                    self.a_work_img = None

    # ####################### __about_dialog_box ########################
    def __mwib_about_dialog_box( self):
        """ Button about of the main window """
        self.c_the_log.add_string_to_log( 'Do about')
        self.w_front_window = MyAboutWindow( self.c_main_class, self.a_list_application_info)
        self.w_front_window.aw_create_about_window()
        self.w_front_window = None

    # ####################### __mwib_open_box ########################
    def __mwib_open_box( self):
        """ Button preference of the main window """
        self.c_the_log.add_string_to_log( 'Do load picture')
        self.__mwib_load_and_check_bmp()
        if self.a_work_img:
            self.c_main_class.mw_update_main_window( self.s_filename, self.a_work_img)

    # ####################### __mwib_save_box ########################
    def __mwib_save_box( self):
        """ Button configuration of the main window """
        self.c_the_log.add_string_to_log( 'Do save picture')
        self.c_main_class.bell()
        self.c_main_class.bell()
        # self.w_front_window = MyConfigurationWindow( self.c_main_window)
        # self.w_front_window.cw_create_configuration_window()
        # self.w_front_window = None

    # ##########################################################################################
    # https://manytools.org/hacker-tools/ascii-banner/
    #
    #   ######  #     # ######  #       ###  #####
    #   #     # #     # #     # #        #  #     #
    #   #     # #     # #     # #        #  #
    #   ######  #     # ######  #        #  #
    #   #       #     # #     # #        #  #
    #   #       #     # #     # #        #  #     #
    #   #        #####  ######  ####### ###  #####
    #
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
        """ Return frame to be able to add new elements """
        return self.a_top_frame_of_main_window
