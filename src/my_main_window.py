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

""" Module de creation de la fenetre principale. """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# number is reasonable in this case these are all the icons of the main windows and the application icons
# pylint: disable=too-many-instance-attributes
# ###############################################################################################

import platform
import os
import tkinter as tk_gui

from datetime import datetime
from functools import partial

import src.my_constants as constant
# from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_main_window_icons_bar import MyMainWindowIconsBar
from .my_main_window_image import MyMainWindowImage
from .my_main_window_pallet import MyMainWindowPallet
from .my_alert_window import MyAlertWindow
from .my_tools import mt_save_file

# __name__ = "MyMainWindow"

# ###############################################################################################
# #######========================= constant private =========================

WAIT_TIME_COM = 0.05

# ###############################################################################################
# #######=========================     GUI     =========================
# ####################### MyMainWindow ########################
class MyMainWindow:
    """ Create the main Windows of the application. """
    # Optimizing memory usage with slots
    # __slots__ = ["w_root_windows", "a_list_application_info" ]

    # ####################### __init__ ########################
    def __init__( self, w_root_windows, list_application_info):
        """
            All this parameter are created in main()
            w_root_windows : the windows created by tk
            a_list_application_info : les inforamtions de l'application
        """
        print()
        self.w_tk_root = w_root_windows        # root window the first window created
        self.a_list_application_info = list_application_info
        # Position of the main windows
        self.i_main_window_x = 20
        self.i_main_window_y = 20
        self.w_tk_root.background = constant.BACKGROUD_COLOR_UI
        self.c_the_icons = MyIconPictures( self.w_tk_root)
        self.s_platform = platform.system()
        # Size of the main windows
        if self.s_platform == "Linux":
            self.i_main_window_width = 1120
            self.i_main_window_height = 830
        elif self.s_platform == "Darwin":
            self.i_main_window_width = 1150
            self.i_main_window_height = 834
        elif self.s_platform == "Windows":
            self.i_main_window_width = 1070
            self.i_main_window_height = 824

        self.c_alert_windows = MyAlertWindow( self, list_application_info)
        self.s_init_pathname = os.getcwd()
        self.c_main_icon_bar = None             # top icon menu bar : MyMainWindowIconsBar
        self.c_main_image = None                # top icon menu bar : MyMainWindowImage
        self.c_main_pallet = None               # top icon menu bar : MyMainWindowPallet

    # ####################### __repr__ ########################
    def __repr__( self) -> str:
        """ A dundle method for description """
        return f"{type(self).__name__}({self.w_tk_root}, {self.a_list_application_info})"

    # ####################### __getattribute__ ########################
    # def __getattribute__( self, name):
    #     """ A dundle method for description """
    #     cls = type( self)
    #     # if hasattr( cls, "__slots__"):
    #     #     if name in cls.__slots__:
    #     #         index = cls.__slots__.index( name)
    #     #         return self.slot_array( index)
    #     if name in vars( self):
    #         return vars( self)[ name]
    #     if hasattr( cls, name):
    #         return getattr( cls, name)
    #     if hasattr( cls, "__getattr__"):
    #         return cls.__getattr__( self, name)
    #     return AttributeError( f"{cls.name} object has no attribute {name}")

    # ##########################################################################################
    # https://manytools.org/hacker-tools/ascii-banner/
    #
    # #     #                                  ######
    # ##   ## # #####  #####  #      ######    #     # #  ####  ##### #    # #####  ######    #####    ##   #####  #####
    # # # # # # #    # #    # #      #         #     # # #    #   #   #    # #    # #         #    #  #  #  #    #   #
    # #  #  # # #    # #    # #      #####     ######  # #        #   #    # #    # #####     #    # #    # #    #   #
    # #     # # #    # #    # #      #         #       # #        #   #    # #####  #         #####  ###### #####    #
    # #     # # #    # #    # #      #         #       # #    #   #   #    # #   #  #         #      #    # #   #    #
    # #     # # #####  #####  ###### ######    #       #  ####    #    ####  #    # ######    #      #    # #    #   #
    #
    # ##########################################################################################

    # ####################### __mw_paint_left_and_right ########################
    def __mw_paint_left_and_right( self, i_offset, i_true_x, i_true_y):
        """  Replace color from middle point to left and right """
        a_original_img = self.c_main_image.mwi_get_original_image()
        # same line for origin to left
        i_run_to_left = i_true_x
        i_run_offset = i_offset
        i_around_cursor = self.c_main_pallet.mwp_get_around_cursor()
        while i_run_to_left >= 0:
            if (i_offset == i_run_offset) and (i_offset != i_around_cursor):
                a_original_img.putpixel( (i_run_to_left, i_true_y), i_around_cursor)
                i_run_to_left -= 1
                i_run_offset = a_original_img.getpixel( ( i_run_to_left, i_true_y))
            else:
                break

        # same line for origin to right
        i_run_to_rigth = i_true_x
        i_run_offset = i_offset
        while i_run_to_rigth <= 320:
            if (i_offset == i_run_offset) and (i_offset != i_around_cursor):
                a_original_img.putpixel( (i_run_to_rigth, i_true_y), i_around_cursor)
                i_run_to_rigth += 1
                i_run_offset = a_original_img.getpixel( ( i_run_to_rigth, i_true_y))
            else:
                break

    # ####################### mw_replace_color ########################
    def mw_replace_color( self, i_true_x, i_true_y):
        """ Replace a color for line with the same SCB """
        a_original_img = self.c_main_image.mwi_get_original_image()
        if a_original_img:
            i_around_cursor = self.c_main_pallet.mwp_get_around_cursor()
            i_offset = a_original_img.getpixel( ( i_true_x, i_true_y))
            print( "offset to change = " + str( i_offset) + " by = " + str( i_around_cursor))

            i_run_offset = i_offset
            i_up = i_true_y
            while (i_offset == i_run_offset) and (i_offset != i_around_cursor):
                if i_up >= 0:
                    self.__mw_paint_left_and_right( i_offset, i_true_x, i_up)
                    i_up -= 1
                    i_run_offset = a_original_img.getpixel( ( i_true_x, i_up))
                else:
                    break

            i_down = i_true_y + 1
            if i_down <= 199:
                i_run_offset = a_original_img.getpixel( ( i_true_x, i_down))
                while (i_offset == i_run_offset) and (i_offset != i_around_cursor):
                    if i_down <= 199:
                        self.__mw_paint_left_and_right( i_offset, i_true_x, i_down)
                        i_down += 1
                        i_run_offset = a_original_img.getpixel( ( i_true_x, i_down))
                    else:
                        break

            self.c_main_pallet.mwp_reset_around_cursor()

    # ##########################################################################################
    # https://manytools.org/hacker-tools/ascii-banner/
    #
    # ######
    # #     #  ####  ##### #####  ####  #    #    #####    ##   #      ###### ##### ##### ######    #####    ##   #####  #####
    # #     # #    #   #     #   #    # ##  ##    #    #  #  #  #      #        #     #   #         #    #  #  #  #    #   #
    # ######  #    #   #     #   #    # # ## #    #    # #    # #      #####    #     #   #####     #    # #    # #    #   #
    # #     # #    #   #     #   #    # #    #    #####  ###### #      #        #     #   #         #####  ###### #####    #
    # #     # #    #   #     #   #    # #    #    #      #    # #      #        #     #   #         #      #    # #   #    #
    # ######   ####    #     #    ####  #    #    #      #    # ###### ######   #     #   ######    #      #    # #    #   #
    #
    # ##########################################################################################

    # ####################### __mw_clock_in_window_bar ########################
    def __mw_clock_in_window_bar( self):
        """ Show the date and times in menu bar of the main windows """
        __now = datetime.now()
        # dd/mm/YY H:M:S
        __s_date_time = __now.strftime( "%d/%m/%Y %H:%M:%S")
        __s_windows_title = ' ' + self.a_list_application_info[0] + '                                           ' + __s_date_time
        self.w_tk_root.title( __s_windows_title)
        # self.w_tk_root.after( 1000, self.__mw_clock_in_window_bar)

    # ####################### __mw_change_focus ########################
    def __mw_change_focus( self, event):
        """ De selected an entry widget, when a button is clicked ie the pallet button """
        event.widget.focus_set()

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

    # ####################### mw_create_main_window ########################
    def mw_create_main_window( self):
        """ Design the main windows """
        b_vertical = True        # or False for futur feature with a preference dialog to chose the prefered mode
        if b_vertical is True:
            self.i_main_window_width += 100
            if self.s_platform == "Linux":
                self.i_main_window_height -= 100
            elif self.s_platform == "Darwin":
                self.i_main_window_height -= 100
            elif self.s_platform == "Windows":
                self.i_main_window_height -= 98
            i_rect_x = 2
            i_rect_y = 0
            i_rect_width = 98
            i_rect_height = self.i_main_window_height-4
        else:
            i_rect_x = 2
            i_rect_y = 0
            i_rect_width = self.i_main_window_width-4
            i_rect_height = 98

        # Set windows attribute
        __s_windows_size_and_position = ( str( self.i_main_window_width) + 'x' + str( self.i_main_window_height) + '+' + str( self.i_main_window_x) + '+' + str( self.i_main_window_y) )
        self.w_tk_root.geometry( __s_windows_size_and_position)  # dimension + position x/y a l'ouverture
        self.w_tk_root.update()
        # Lock resize of main window
        self.w_tk_root.minsize( self.i_main_window_width, self.i_main_window_height)
        self.w_tk_root.maxsize( self.i_main_window_width, self.i_main_window_height)
        # No resize for both directions
        self.w_tk_root.resizable( False, False)
        self.w_tk_root.iconphoto( True, self.c_the_icons.get_app_photo())
        self.w_tk_root.title( self.a_list_application_info[0])
        self.w_tk_root.update()

        # Create icons frame
        a_top_bar_frame = tk_gui.Frame( self.w_tk_root, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)    # background='darkgray'
        a_top_bar_frame.place( x=i_rect_x, y=i_rect_y, width=i_rect_width, height=i_rect_height )   # fill :  must be 'none', 'x', 'y', or 'both'
        # Create picture frame
        a_pic_frame = tk_gui.Frame( self.w_tk_root, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        if b_vertical is True:
            a_pic_frame.place( x=100, y=2, width=self.i_main_window_width-104, height=constant.PICTURE_HEIGHT+20+8)  # fill :  must be 'none', 'x', 'y', or 'both'
        else:
            a_pic_frame.place( x=2, y=98, width=self.i_main_window_width-4, height=constant.PICTURE_HEIGHT+20+8)  # fill :  must be 'none', 'x', 'y', or 'both'
        # Create pallet frame
        a_pallet_frame = tk_gui.Frame( self.w_tk_root, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        if b_vertical is True:
            a_pallet_frame.place( x=100, y=2+constant.PICTURE_HEIGHT+22+8, width=self.i_main_window_width-104, height=self.i_main_window_height - ( constant.PICTURE_HEIGHT+20+8), anchor="nw" )
        else:
            a_pallet_frame.place( x=2, y=98+constant.PICTURE_HEIGHT+22+8, width=self.i_main_window_width-4, height=self.i_main_window_height - ( constant.PICTURE_HEIGHT+20+8), anchor="nw" )
        self.w_tk_root.update()
        print( "w_tk_root           : width= " + str( self.w_tk_root.winfo_width()) + " height= ", str( self.w_tk_root.winfo_height()))
        print( "a_top_bar_frame     : width= " + str( a_top_bar_frame.winfo_width()) + " height= ", str( a_top_bar_frame.winfo_height()))
        print( "a_pic_frame         : width= " + str( a_pic_frame.winfo_width()) + " height= ", str( a_pic_frame.winfo_height()))
        print( "a_pallet_frame      : width= " + str( a_pallet_frame.winfo_width()) + " height= ", str( a_pallet_frame.winfo_height()))

        # Create line or column 1 for action icons
        self.c_main_icon_bar = MyMainWindowIconsBar( self, self.w_tk_root, self.a_list_application_info, a_top_bar_frame)
        if b_vertical is True:
            self.c_main_icon_bar.mwib_create_left_bar_icons( 1)     # vertical on left
        else:
            self.c_main_icon_bar.mwib_create_top_bar_icons( 1)      # horizontal on top
        # Create line 2 for picture
        self.c_main_image = MyMainWindowImage( self.w_tk_root, self)
        self.c_main_image.mwi_picture_zone( a_pic_frame, a_pic_frame.winfo_width(), self.c_main_icon_bar)
        self.c_main_icon_bar.mwib_set_main_image( self.c_main_image)
        # Create line 3 for pallet
        self.c_main_pallet = MyMainWindowPallet( self.w_tk_root, self)
        self.c_main_pallet.mwp_pallet_zone( a_pallet_frame, self.c_main_image, self.c_main_icon_bar)
        self.c_main_image.mwi_set_pallet( self.c_main_pallet)

        self.w_tk_root.update()
        # print( "Calcul height       : " + str( self.i_main_window_height - ( a_top_bar_frame.winfo_height() + a_pic_frame.winfo_height())))

        self.w_tk_root.bind( '<Button>', self.__mw_change_focus)
        # Manage arrow keys pressed like click on arrow button
        self.w_tk_root.bind( "<Up>" , self.c_main_image.mwi_on_single_key)
        self.w_tk_root.bind( "<Down>" , self.c_main_image.mwi_on_single_key)
        self.w_tk_root.bind( "<Left>" , self.c_main_image.mwi_on_single_key)
        self.w_tk_root.bind( "<Right>" , self.c_main_image.mwi_on_single_key)

        # disabled during debug
        if self.s_platform == "Windows":
            self.__mw_clock_in_window_bar()
            # if self.a_work_img:
            #     self.__mw_print_widget_under_mouse( self.w_tk_root)


    # ####################### mw_update_main_window ########################
    def mw_update_main_window( self, s_filename, a_work_img) -> bool:
        """ Load a picture and fill the interface """
        if s_filename and a_work_img:
            self.c_main_image.mwi_update_main_window_image( s_filename, a_work_img)

            # Update pallet radio buttons
            a_work_img = self.c_main_image.mwi_get_working_image()
            a_pallet_list = a_work_img.getpalette()
            # Disabled for debug
            # print( 'Pallet :')
            i_element = 0
            i_to = 0
            # Disabled for debug
            # for i_loop in range( 0, 16, 1):
            for _ in range( 0, 16, 1):
                i_from = i_to
                i_to = i_to + 48
                # Disabled for debug
                # if i_loop < 10:
                #     s_my_hex = "0" + str( i_loop) + " "
                # else:
                #     s_my_hex = str( i_loop) + " "

                for i_index in range( i_from, i_to, 3):
                    s_red = f'{a_pallet_list[ i_index]:02X}'
                    s_green = f'{a_pallet_list[ i_index + 1]:02X}'
                    s_blue = f'{a_pallet_list[ i_index + 2]:02X}'
                    # Disabled for debug
                    # s_my_hex = s_my_hex + "#" + s_red + s_green + s_blue + " "

                    a_color_btn_rad = self.c_main_pallet.mwp_get_pallet_btn( i_element)
                    # print( "mw_update_main_window() i_index = ", str( i_index))
                    config_pallet_bottom_with_arg = partial( self.c_main_pallet.mwp_color_btn_rad, int( i_index / 3))
                    a_color_btn_rad.configure( command=config_pallet_bottom_with_arg)
                    a_color_btn_rad.configure( background="#" + s_red + s_green + s_blue)
                    i_element += 1

                # Disabled for debug
                # self.w_tk_root.update()
                # print( s_my_hex)

            self.c_main_pallet.mwp_update_color_number_vertical_used()
            self.w_tk_root.update()
            b_return = True
        else:
            b_return = False

        return b_return

    # ####################### mw_get_main_window ########################
    def mw_get_main_window( self):
        """ Return the window widget of the main window """
        return self.w_tk_root

    # ####################### mw_get_main_window_height ########################
    def mw_get_main_window_height( self) -> int:
        """ Return height of the main window """
        self.i_main_window_height = self.w_tk_root.winfo_height()
        return int( self.i_main_window_height)

    # ####################### mw_get_main_window_width ########################
    def mw_get_main_window_width( self) -> int:
        """ Return width of the main window """
        self.i_main_window_width = self.w_tk_root.winfo_width()
        return int( self.i_main_window_width)

    # ####################### mw_get_main_window_pos_x ########################
    def mw_get_main_window_pos_x( self) -> int:
        """ Return position X of the main window """
        self.i_main_window_x = self.w_tk_root.winfo_x()
        return int( self.i_main_window_x)

    # ####################### mw_get_main_window_pos_y ########################
    def mw_get_main_window_pos_y( self) -> int:
        """ Return position Y of the main window """
        self.i_main_window_y = self.w_tk_root.winfo_y()
        return int( self.i_main_window_y)

    # ####################### mw_get_pathname ########################
    def mw_get_pathname( self) -> str:
        """ Return default pathname """
        return self.c_main_icon_bar.mwib_get_get_pathname()

    # ####################### mw_get_application_info ########################
    def mw_get_application_info( self):
        """ Return about of app """
        return self.a_list_application_info

    # ####################### mw_set_pathname ########################
    def mw_set_pathname( self, s_new_pathname) -> str:
        """ Set last used pathname """
        self.s_init_pathname = s_new_pathname

    # ####################### mw_set_pathname ########################
    def mw_load_this_picture(self, filepathname):
        """ load the picture from first arg parameter """
        self.c_main_icon_bar.mwib_open_box( filepathname)

    # ####################### mw_save_picture ########################
    def mw_save_picture( self):
        """ Save the picture """
        s_new_file_name = mt_save_file( self.w_tk_root, self, os.path.basename( self.c_main_icon_bar.mwib_get_get_path_filename()))
        if s_new_file_name:
            s_new_file_name.lower()
            if s_new_file_name[-4:] != ".bmp":
                s_new_file_name = s_new_file_name + ".bmp"

            a_original_img = self.c_main_image.mwi_get_original_image()
            print( '\nSaving : ' + s_new_file_name)
            a_original_img.save( s_new_file_name, 'BMP')

    # ####################### mw_print_widget_under_mouse ########################
    def mw_print_widget_under_mouse( self, event):
        """ Show live position of the mouse in the loaded picture """
        a_original_img = self.c_main_image.mwi_get_original_image()
        if a_original_img:              #  and self.c_main_pallet:
            self.c_main_pallet.mwp_entry_black_focus_out()
            i_pos_x = event.x
            i_pos_y = event.y
            # Use only the pair values, click is done in the picture zoomed x 2
            if i_pos_y & 1:
                i_pos_y -= 1
            if i_pos_x & 1:
                i_pos_x -= 1

            self.c_main_image.mwi_set_mouse_live_pos_x( i_pos_x)
            self.c_main_image.mwi_set_mouse_live_pos_y( i_pos_y)
