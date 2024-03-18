#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This application to do modification of bmp file to prepare convertion to a Apple IIGS pic file.
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

""" Module de creation pour la fenetre principale de la partie pallet. """

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

from tkinter import font, Label, Button, Entry, Scale, StringVar, Radiobutton, IntVar
from tkinter.ttk import Separator
from functools import partial

# from ttkthemes              import ThemedTk, THEMES, ThemedStyle
from PIL import ImageTk


import src.my_constants as constant
# from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_alert_window import MyAlertWindow
from .my_tools import mt_hexlify_byte_string

# __name__ = "MyMainWindowPallet"

# ###############################################################################################
# #######========================= constant private =========================

# ###############################################################################################
# #######=========================     GUI     =========================
# ####################### MyMainWindowPallet ########################
class MyMainWindowPallet:
    """ Create the main Windows Pallet part of the application. """
    # Optimizing memory usage with slots
    # __slots__ = ["w_root_windows", "a_list_application_info" ]

    # ####################### __init__ ########################
    def __init__( self, w_root_windows, c_main_window):
        """
            All this parameter are created in main()
            w_root_windows : the windows created by tk
            c_main_window : the main window
        """
        self.w_tk_root = w_root_windows        # root window the first window created
        self.c_main_windows = c_main_window
        # Position of the main windows
        self.i_main_window_x = 20
        self.i_main_window_y = 20
        self.w_tk_root.background = constant.BACKGROUD_COLOR_UI
        self.c_the_icons = MyIconPictures( self.w_tk_root)
        self.s_platform = platform.system()
        # Size of the main windows
        self.i_main_window_width = c_main_window.mw_get_main_window_width()
        self.i_main_window_height = c_main_window.mw_get_main_window_height()
        self.c_alert_windows = MyAlertWindow( c_main_window, c_main_window.mw_get_application_info())
        self.s_init_pathname = os.getcwd()
        self.c_main_icon_bar = None                # top icon menu bar : MyMainWindowIconsBar
        self.c_main_image = None                   # top icon menu bar : MyMainWindowPicture
        self.c_main_pallet = None                  # top icon menu bar : MyMainWindowPallet

        self.a_pallet_number_lst = []
        self.a_pallet_button_lst = []

        self.color_radio_button = IntVar()
        self.a_red_ntr = None
        self.a_green_ntr = None
        self.a_blue_ntr = None
        self.a_red_input_var= StringVar()
        self.a_green_input_var = StringVar()
        self.a_blue_input_var = StringVar()
        self.a_red_ntr_dec_lbl = None
        self.a_green_ntr_dec_lbl = None
        self.a_blue_ntr_dec_lbl = None
        self.a_btn_offset_lbl = None
        self.a_btn_x_lbl = None
        self.a_btn_y_lbl = None
        self.a_the_color_new_lbl = None
        self.a_color_old_btn = None
        self.a_color_slider = None
        self.a_zoom_lbl = None
        self.i_around_cursor = -1
        self.a_zoom_work_img = None
        self.a_render_zoom = None
        self.i_color_to_copy_offset = -1
        self.i_color_line_to_copy_offset = -1

    # ##########################################################################################
    # https://manytools.org/hacker-tools/ascii-banner/
    #
    # ######
    # #     #  ####  ##### #####  ####  #    #    #####    ##   #       #      ###### #####    #####    ##   #####  #####
    # #     # #    #   #     #   #    # ##  ##    #    #  #  #  #       #      #        #      #    #  #  #  #    #   #
    # ######  #    #   #     #   #    # # ## #    #    # #    # #       #      #####    #      #    # #    # #    #   #
    # #     # #    #   #     #   #    # #    #    #####  ###### #       #      #        #      #####  ###### #####    #
    # #     # #    #   #     #   #    # #    #    #      #    # #       #      #        #      #      #    # #   #    #
    # ######   ####    #     #    ####  #    #    #      #    # ######  ###### ######   #      #      #    # #    #   #
    #
    # ##########################################################################################

    # ####################### __mwp_restore_old_color ########################
    def __mwp_restore_old_color( self):
        """ This button restore the old color same as the pallette button clicked """
        i_number = int( self.a_btn_offset_lbl.cget( "text"))
        # print( "mw_restore_old_color() i_offset = ", str( i_number))
        self.mwp_color_btn_rad( i_number)

    # ####################### __mwp_update_red_entry ########################
    def __mwp_update_red_entry( self, i_value):
        """" Scale is moving update red : entry in hex, label in dec and color of new color label """
        # print( "mv_update_red_entry()")
        if int( i_value) > 15:
            s_red = f'{int( i_value):X}'
        else:
            s_red = f'0{int( i_value):X}'
        self.a_red_input_var.set( s_red)
        self.a_red_ntr_dec_lbl.configure( text=i_value)
        s_green = self.a_green_input_var.get()
        if len( s_green) != 2:
            s_green = "0" + s_green
        s_blue = self.a_blue_input_var.get()
        if len( s_blue) != 2:
            s_blue = "0" + s_blue
        self.a_the_color_new_lbl.configure( background= "#" + s_red + s_green + s_blue)

    # ####################### __mwp_update_green_entry ########################
    def __mwp_update_green_entry( self, i_value):
        """" Scale is moving update green : entry in hex, label in dec and color of new color label """
        # print( "mv_update_green_entry()")
        if int( i_value) > 15:
            s_green = f'{ int(i_value):X}'
        else:
            s_green = f'0{ int(i_value):X}'
        self.a_green_input_var.set( s_green)
        self.a_green_ntr_dec_lbl.configure( text=i_value)
        s_red = self.a_red_input_var.get()
        if len( s_red) != 2:
            s_red = "0" + s_red
        s_blue = self.a_blue_input_var.get()
        if len( s_blue) != 2:
            s_blue = "0" + s_blue
        self.a_the_color_new_lbl.configure( background= "#" + s_red + s_green + s_blue)

    # ####################### __mwp_update_blue_entry ########################
    def __mwp_update_blue_entry( self, i_value):
        """" Scale is moving update blue : entry in hex, label in dec and color of new color label """
        # print( "mv_update_blue_entry()")
        if int( i_value) > 15:
            s_blue= f'{int( i_value):X}'
        else:
            s_blue= f'0{int( i_value):X}'
        self.a_blue_input_var.set( s_blue)
        self.a_blue_ntr_dec_lbl.configure( text=i_value)
        s_red = self.a_red_input_var.get()
        if len( s_red) != 2:
            s_red = "0" + s_red
        s_green = self.a_green_input_var.get()
        if len( s_green) != 2:
            s_green = "0" + s_green
        self.a_the_color_new_lbl.configure( background= "#" + s_red + s_green + s_blue)

    # ####################### __mwp_entry_red_focus_in ########################
    def __mwp_entry_red_focus_in( self, _):
        """ Select of red entry widget focus events prepare scale to move """
        self.a_color_slider.config( troughcolor='red')
        i_red_color = int(self.a_red_ntr.get(), 16)
        self.a_color_slider.set( i_red_color )
        self.a_red_ntr_dec_lbl.configure( text=str( i_red_color))
        self.a_color_slider.config( command=self.__mwp_update_red_entry )

    # ####################### __mwp_entry_green_focus_in ########################
    def __mwp_entry_green_focus_in( self, _):
        """ Select of green entry widget focus events prepare scale to move """
        self.a_color_slider.config( troughcolor='green')
        i_green_color = int(self.a_green_ntr.get(), 16)
        self.a_color_slider.set( i_green_color )
        self.a_green_ntr_dec_lbl.configure( text=str( i_green_color))
        self.a_color_slider.config( command=self.__mwp_update_green_entry )

    # ####################### __mwp_entry_blue_focus_in ########################
    def __mwp_entry_blue_focus_in( self, _):
        """ Select of blue entry widget focus events prepare scale to move """
        self.a_color_slider.config( troughcolor='blue')
        i_blue_color = int(self.a_blue_ntr.get(), 16)
        self.a_color_slider.set( i_blue_color )
        self.a_blue_ntr_dec_lbl.configure( text=str( i_blue_color))
        self.a_color_slider.config( command=self.__mwp_update_blue_entry )

    # ####################### __mwp_click_on_picture_zoom ########################
    def __mwp_click_on_picture_zoom( self, _):
        """ Show position of the mouse in the loaded picture and repair SCB to draw a rect """
        # print( "mw_click_on_picture()  ", event)
        self.mwp_entry_black_focus_out()
        a_original_img = self.c_main_image.mwi_get_original_image()
        a_work_img= self.c_main_image.mwi_get_working_image()
        if a_original_img and a_work_img:
            if self.i_around_cursor != -1:
                i_pox_x = self.c_main_image.mwi_get_mouse_pos_x_var()
                i_pox_y = self.c_main_image.mwi_get_mouse_pos_y_var()
                i_true_x = int( (( i_pox_x & 1022) / 2))
                i_true_y = int( (( i_pox_y & 1022) / 2))
                self.c_main_windows.mw_replace_color( i_true_x, i_true_y)
                self.c_main_windows.mw_update_main_window( self.c_main_icon_bar.mwib_get_get_path_filename(), a_original_img)
                # Display zoom of a part of the picture
                self.mwp_draw_zoom_square( i_pox_x, i_pox_y)


    # ####################### __mwp_set_pen_color ########################
    def __mwp_set_pen_color( self):
        """ Set a new color value in pallet  """

        self.i_around_cursor = int( self.a_btn_offset_lbl.cget( "text"))
        # s_red = self.a_red_input_var.get()
        # s_green = self.a_green_input_var.get()
        # s_blue = self.a_blue_input_var.get()
        # i_index = int(self.a_btn_offset_lbl.cget( "text"))
        # a_pallet_button = self.a_pallet_button_lst[i_index]
        # # ready when color modification will be done
        # a_pallet_button.configure( background= "#" + s_red + s_green + s_blue)
        #
        # to do : Modify the picture pallet

    # ####################### __mwp_copy_a_color ########################
    def __mwp_copy_a_color( self):
        """ copy the selected color to the next click on a pallet color """
        if self.i_color_to_copy_offset == -1:
            self.i_color_to_copy_offset = int( self.a_btn_offset_lbl.cget( "text"))

    # ####################### __mwp_copy_line_color ########################
    def __mwp_copy_line_color( self):
        """ copy the line selected color to the next click on a pallet color """
        if self.i_color_line_to_copy_offset == -1:
            self.i_color_line_to_copy_offset = int( self.a_btn_x_lbl.cget( "text"))

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

    # ####################### get_from_pal_btn_lst_color ########################
    def get_from_pal_btn_lst_color(self, i_offset):
        """ Frame with the pallet button to left, and details to right """
        return self.a_pallet_button_lst[i_offset].cget( 'bg')

    # ####################### mwp_pallet_zone ########################
    def mwp_pallet_zone( self, a_bottom_frame, c_main_image, c_main_icon_bar):
        """ Frame with the pallet button to left, and details to right """
        self.c_main_image = c_main_image
        self.c_main_icon_bar = c_main_icon_bar
        i_index_base_block = 0
        a_pallet_sep_h0 = Separator( a_bottom_frame, orient='horizontal')
        a_pallet_sep_h0.grid( row=i_index_base_block, column=0, columnspan=8, sticky='ew')
        a_pallet_sep_lbl_h0 = Label( a_bottom_frame, text="Pallet", background=constant.BACKGROUD_COLOR_UI)
        a_pallet_sep_lbl_h0.grid( row=i_index_base_block, column=0, columnspan=2, padx=260)
        a_pallet_sep_h1 = Separator( a_bottom_frame, orient='horizontal')
        a_pallet_sep_h1.grid( row=i_index_base_block, column=9, columnspan=4, sticky='ew')
        a_pallet_sep_lbl_h1 = Label( a_bottom_frame, text="Color", background=constant.BACKGROUD_COLOR_UI)
        if self.s_platform in [ "Darwin", "Linux" ]:
            a_pallet_sep_lbl_h1.grid( row=i_index_base_block, column=9, columnspan=4, padx=130)
        else:
            a_pallet_sep_lbl_h1.grid( row=i_index_base_block, column=9, columnspan=4, padx=120)
        a_pallet_sep_h2 = Separator( a_bottom_frame, orient='horizontal')
        a_pallet_sep_h2.grid( row=i_index_base_block, column=13, columnspan=4, sticky='ew')
        a_pallet_sep_lbl_h2 = Label( a_bottom_frame, text="Zoom", background=constant.BACKGROUD_COLOR_UI)
        if self.s_platform in [ "Darwin", "Linux" ]:
            a_pallet_sep_lbl_h2.grid( row=i_index_base_block, column=13, columnspan=4, padx=120)
        else:
            a_pallet_sep_lbl_h2.grid( row=i_index_base_block, column=13, columnspan=4, padx=100)

        # Create pallet button left frame
        a_pallet_bottom_frame = tk_gui.Frame( a_bottom_frame, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        if self.s_platform == "Darwin":
            a_pallet_bottom_frame.place( x=2, y=20, width=590, height=276 )
        else:
            a_pallet_bottom_frame.place( x=2, y=20, width=570, height=276 )

        # Creating a font object with little size for color buttons to reduce their size
        a_font_label = font.Font( size=6)
        a_font_button = font.Font( size=3)

        # Create a line of number for the column
        i_index_base_column = 1
        for i_loop in range( 0, 16, 1):
            a_label = Label( a_pallet_bottom_frame, text=str( i_loop), background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            self.a_pallet_number_lst.append( a_label)
            i_index_base_column += 1

        # Table of color button for the pallet
        i_index_base_block += 1
        i_index_base_column = 0
        i_to = 0
        i_index = 0
        for i_loop in range( 0, 16, 1):
            i_from = i_to
            i_to = i_to + 48
            # First element of the line is its number
            a_label = Label( a_pallet_bottom_frame, text=str(i_loop), background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            if self.s_platform == "Darwin":
                a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            else:
                a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            i_index_base_column += 1
            # create list of line of radio button and add it in a list to be accessible
            for _ in range( i_from, i_to, 3):
                a_button_color = Radiobutton( a_pallet_bottom_frame, text='', indicatoron = 0, width=8, height=1, variable=self.color_radio_button, value=i_index, background=constant.LIGHT_COLOR_UI, font=a_font_button)
                if self.s_platform in [ "Darwin", "Linux" ]:
                    a_button_color.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=2)
                else:
                    a_button_color.grid( row=i_index_base_block, column=i_index_base_column, padx=4, pady=2)
                self.a_pallet_button_lst.append( a_button_color)
                i_index_base_column += 1
                i_index += 1

            i_index_base_column = 0
            i_index_base_block += 1

        self.w_tk_root.update()

        # Create color button right frame
        a_color_bottom_frame = tk_gui.Frame( a_bottom_frame, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        if self.s_platform == "Darwin":
            a_color_bottom_frame.place( x=592, y=20, width=self.i_main_window_width - 592, height=276 )
        else:
            a_color_bottom_frame.place( x=572, y=20, width=self.i_main_window_width - 572, height=276 )

        i_index_base_block = 0
        a_color_name_lbl = Label( a_color_bottom_frame, text="Red", background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1)
        a_color_name_lbl = Label( a_color_bottom_frame, text="RGB Color", background=constant.BACKGROUD_COLOR_UI)
        a_color_name_lbl.grid( row=i_index_base_block, column=2, columnspan=2, padx=4, pady=1)
        # the text is the cursor style on the middle of the label
        self.a_zoom_lbl = Label( a_color_bottom_frame, image=None, text="   _     _", background=constant.BACKGROUD_COLOR_UI, cursor='circle', borderwidth=2, compound="center", highlightthickness=2)
        if self.s_platform in [ "Darwin", "Linux" ]:
            self.a_zoom_lbl.grid( row=i_index_base_block, rowspan=9, column=4, columnspan=4, padx=4, pady=1, sticky='ewns')
        else:
            self.a_zoom_lbl.grid( row=i_index_base_block, rowspan=9, column=4, columnspan=4, padx=8, pady=1, sticky='ewns')
        self.a_zoom_lbl.bind( '<Button>', self.__mwp_click_on_picture_zoom)

        i_index_base_block += 1
        red_okay_command = self.w_tk_root.register( self.mwp_red_max_of_two_chars_and_filter)
        # all parameter available for self.mwp_red_max_of_two_chars_and_filter are '%P', '%s', '%S', '%v', '%V'
        self.a_red_ntr = Entry( a_color_bottom_frame, textvariable=self.a_red_input_var, width=constant.DEFAULT_BUTTON_WIDTH,
                               validate='all', validatecommand=( red_okay_command, '%P', '%S', '%V'), background=constant.LIGHT_COLOR_UI, foreground='red')
        self.a_red_ntr.grid( row=i_index_base_block, column=0, columnspan=1, padx=4, sticky='w')
        self.a_red_ntr_dec_lbl = Label( a_color_bottom_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH - 1, background='light grey', foreground='red')
        self.a_red_ntr_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=4, sticky='ew')
        a_offset_lbl = Label( a_color_bottom_frame, text="New", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=2, columnspan=1, padx=4, pady=1, sticky='ew')
        a_offset_lbl = Label( a_color_bottom_frame, text="Old", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=3, columnspan=1, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        i_index_base_block_for_old_button = i_index_base_block
        a_color_name_lbl = Label( a_color_bottom_frame, text="Green", background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1)
        self.a_the_color_new_lbl = Label( a_color_bottom_frame, text="", width=8, background=constant.LIGHT_COLOR_UI, foreground='black')
        self.a_the_color_new_lbl.grid( row=i_index_base_block, rowspan=3, column=2, columnspan=1, padx=4, pady=1, sticky='ewns')

        i_index_base_block += 1
        green_okay_command = self.w_tk_root.register( self.mwp_green_max_of_two_chars_and_filter)
        # all parameter available for self.mwp_green_max_of_two_chars_and_filter are '%P', '%s', '%S', '%v', '%V'
        self.a_green_ntr = Entry( a_color_bottom_frame, textvariable=self.a_green_input_var, width=constant.DEFAULT_BUTTON_WIDTH,
                                validate="all", validatecommand=( green_okay_command, '%P', '%S', '%V'), background=constant.LIGHT_COLOR_UI, foreground='green')
        self.a_green_ntr.grid( row=i_index_base_block, column=0, padx=4, sticky='w')
        self.a_green_ntr_dec_lbl = Label( a_color_bottom_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH - 1, background='light grey', foreground='green')
        self.a_green_ntr_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=4, sticky='ew')

        i_index_base_block += 1
        a_color_name_lbl = Label( a_color_bottom_frame, text="Blue", background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1)

        i_index_base_block += 1
        blue_okay_command = self.w_tk_root.register( self.mwp_blue_max_of_two_chars_and_filter)
        # all parameter available for self.mwp_blue_max_of_two_chars_and_filter are '%P', '%s', '%S', '%v', '%V'
        self.a_blue_ntr = Entry( a_color_bottom_frame, textvariable=self.a_blue_input_var, width=constant.DEFAULT_BUTTON_WIDTH,
                                validate="all", validatecommand=( blue_okay_command, '%P', '%S', '%V'), background=constant.LIGHT_COLOR_UI, foreground='blue')
        self.a_blue_ntr.grid( row=i_index_base_block, column=0, padx=4, sticky='w')
        self.a_blue_ntr_dec_lbl = Label( a_color_bottom_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH - 1, background='light grey', foreground='blue')
        self.a_blue_ntr_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=4, sticky='ew')

        # move declaration of old button to be able to focus color entry in a loop with the key 'tab'
        if self.s_platform == "Darwin":
            set_color_in_pallet_with_arg = partial( self.__mwp_set_color_in_pallet, -1)
            a_change_color_btn = Button( a_color_bottom_frame, text='Set color', command=set_color_in_pallet_with_arg, width=14, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            a_change_color_btn.grid( row=i_index_base_block, column=2, columnspan=2, padx=2, pady=1, sticky='ew')
            self.a_color_old_btn = Button( a_color_bottom_frame, text='', command=self.__mwp_restore_old_color, width=5, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            self.a_color_old_btn.grid( row=i_index_base_block_for_old_button, rowspan=3, column=3, columnspan=1, padx=2, pady=0, sticky='ewns')
        else:
            set_color_in_pallet_with_arg = partial( self.__mwp_set_color_in_pallet, -1)
            a_change_color_btn = Button( a_color_bottom_frame, text='Set color', command=set_color_in_pallet_with_arg, width=14, height=1, relief='raised', background=constant.BACKGROUD_COLOR_UI)
            a_change_color_btn.grid( row=i_index_base_block, column=2, columnspan=2, padx=4, pady=1, sticky='ew')
            self.a_color_old_btn = Button( a_color_bottom_frame, text='', command=self.__mwp_restore_old_color, width=7, height=1, relief='raised', background='light grey')
            self.a_color_old_btn.grid( row=i_index_base_block_for_old_button, rowspan=3, column=3, columnspan=1, padx=4, pady=1, sticky='ewns')

        i_index_base_block += 1
        # , borderwidth=0, compound="center", highlightthickness=0
        self.a_color_slider = Scale( a_color_bottom_frame, from_=0, to=255, orient='horizontal', background=constant.BACKGROUD_COLOR_UI, highlightbackground='light grey', borderwidth=0, highlightthickness=0, troughcolor=constant.BACKGROUD_COLOR_UI)
        self.a_color_slider.grid( row=i_index_base_block, column=0, columnspan=4, padx=4, pady=4, sticky='ew')

        i_index_base_block += 1
        a_offset_lbl = Label( a_color_bottom_frame, text="Offset", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1, sticky='ew')
        a_offset_lbl = Label( a_color_bottom_frame, text="Pallet Y", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=2, columnspan=1, padx=4, pady=1, sticky='ew')
        a_offset_lbl = Label( a_color_bottom_frame, text="Offset X", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=3, columnspan=1, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        self.a_btn_offset_lbl = Label( a_color_bottom_frame, text="   ", background='light grey', foreground='black')
        self.a_btn_offset_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, sticky='ew')
        self.a_btn_x_lbl = Label( a_color_bottom_frame, text="   ", background='light grey', foreground='black')
        self.a_btn_x_lbl.grid( row=i_index_base_block, column=2, padx=4, sticky='ew')
        self.a_btn_y_lbl = Label( a_color_bottom_frame, text="   ", background='light grey', foreground='black')
        self.a_btn_y_lbl.grid( row=i_index_base_block, column=3, padx=4, sticky='ew')

        i_index_base_block += 1
        if self.s_platform == "Darwin":
            a_change_color_btn = Button( a_color_bottom_frame, text='Copy color', command=self.__mwp_copy_a_color, width=14, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            a_change_color_btn.grid( row=i_index_base_block, column=0, columnspan=2, padx=2, pady=0, sticky='ew')
            a_copy_line_color_btn = Button( a_color_bottom_frame, text='Copy line color', command=self.__mwp_copy_line_color, width=14, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            a_copy_line_color_btn.grid( row=i_index_base_block, column=2, columnspan=2, padx=2, pady=0, sticky='ew')
            a_pen_color_btn = Button( a_color_bottom_frame, text='Pen color', command=self.__mwp_set_pen_color, width=14, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            a_pen_color_btn.grid( row=i_index_base_block, column=4, columnspan=2, padx=2, pady=0, sticky='ew')
        else:
            a_change_color_btn = Button( a_color_bottom_frame, text='Copy color', command=self.__mwp_copy_a_color, width=14, height=1, relief='raised', background=constant.BACKGROUD_COLOR_UI)
            a_change_color_btn.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=6, sticky='ew')
            a_copy_line_color_btn = Button( a_color_bottom_frame, text='Copy line color', command=self.__mwp_copy_line_color, width=14, height=1, relief='raised', background=constant.BACKGROUD_COLOR_UI)
            a_copy_line_color_btn.grid( row=i_index_base_block, column=2, columnspan=2, padx=4, pady=6, sticky='ew')
            a_pen_color_btn = Button( a_color_bottom_frame, text='Pen color', command=self.__mwp_set_pen_color, width=14, height=1, relief='raised', background=constant.BACKGROUD_COLOR_UI)
            a_pen_color_btn.grid( row=i_index_base_block, column=4, columnspan=2, padx=4, pady=6, sticky='ew')

        # self.w_tk_root.update()

    # ####################### mwp_red_max_of_two_chars_and_filter ########################
    def mwp_red_max_of_two_chars_and_filter( self, s_before, s_call, s_reason) -> bool:
    # def mwp_red_max_of_two_chars_and_filter( self, s_before, s_after, s_call, s_value, s_reason) -> bool:
        """ Validates each character as it is entered in the entry for a color value
            parameter setup is '%P', '%s', '%S', '%v', '%V'
            no used : '%d', '%W'
            posibility are
            '%d'	Action code: 0 for an attempted deletion, 1 for an attempted insertion, or -1 if the callback was called for focus in, focus out, or a change to the textvariable.
            '%i'	When the user attempts to insert or delete text, this argument will be the index of the beginning of the insertion or deletion. If the callback was due to focus in, focus out, or a change to the textvariable, the argument will be -1.
            '%P'	The value that the text will have if the change is allowed.
            '%s'	The text in the entry before the change.
            '%S'	If the call was due to an insertion or deletion, this argument will be the text being inserted or deleted.
            '%v'	The current value of the widget's validate option.
            '%V'	The reason for this callback: one of 'focusin', 'focusout', 'key', or 'forced' if the textvariable was changed.
            '%W'	The name of the widget.
        """
        # print( "mwp_red_max_of_two_chars_and_filter() ")
        # print( f"i_action  d : {i_action}")
        # print( f"s_before  P : {s_before}")
        # print( f"s_after   s : {s_after}")
        # print( f"s_call    S : {s_call}")
        # print( f"s_value   v : {s_value}")
        # print( f"s_reason  V : {s_reason}")
        # print( f"s_name    W : {s_name}")
        # a_widget = self.w_tk_root.nametowidget( s_name)
        # print( "widget      = ", a_widget)

        b_result = False
        if s_reason == "focusin":
            # print( "focusin set value to Slider, new label and old button")
            self.__mwp_entry_red_focus_in( None)
            b_result = True
        elif s_reason == "focusout":
            # print( "focusout set value to Slider, new label and old button")
            self.__mwp_entry_red_focus_in( None)
            b_result = True
        elif s_reason == "key":
            # print( "key")
            if 'a' <= s_call <= 'f' or 'A' <= s_call <= 'F' or '0' <= s_call <= '9':
                if len( s_before) > 2:
                    b_result = False
                else:
                    b_result = True
            else:
                # print( "manage value")
                if s_call.isprintable() or s_call.isspace():
                    b_result = False
                else:
                    print( mt_hexlify_byte_string( b's_call', ":"))
                    b_result = True
        else:
            # print( "does nothing")
            b_result = True

        return b_result

    # ####################### mwp_green_max_of_two_chars_and_filter ########################
    def mwp_green_max_of_two_chars_and_filter( self, s_before, s_call, s_reason) -> bool:
    # def mwp_green_max_of_two_chars_and_filter( self, s_before, s_after, s_call, s_value, s_reason) -> bool:
        """ Validates each character as it is entered in the entry for a color value
            parameter setup is '%P', '%s', '%S', '%v', '%V'
            no used : '%d', '%W'
            posibility are
            '%d'	Action code: 0 for an attempted deletion, 1 for an attempted insertion, or -1 if the callback was called for focus in, focus out, or a change to the textvariable.
            '%i'	When the user attempts to insert or delete text, this argument will be the index of the beginning of the insertion or deletion. If the callback was due to focus in, focus out, or a change to the textvariable, the argument will be -1.
            '%P'	The value that the text will have if the change is allowed.
            '%s'	The text in the entry before the change.
            '%S'	If the call was due to an insertion or deletion, this argument will be the text being inserted or deleted.
            '%v'	The current value of the widget's validate option.
            '%V'	The reason for this callback: one of 'focusin', 'focusout', 'key', or 'forced' if the textvariable was changed.
            '%W'	The name of the widget.
        """
        # print( "mwp_green_max_of_two_chars_and_filter() ")
        # print( f"i_action  d : {i_action}")
        # print( f"s_before  P : {s_before}")
        # print( f"s_after   s : {s_after}")
        # print( f"s_call    S : {s_call}")
        # print( f"s_value   v : {s_value}")
        # print( f"s_reason  V : {s_reason}")
        # print( f"s_name    W : {s_name}")
        # a_widget = self.w_tk_root.nametowidget( s_name)
        # print( "widget      = ", a_widget)

        b_result = False
        if s_reason == "focusin":
            # print( "focusin set value to Slider, new label and old button")
            self.__mwp_entry_green_focus_in( None)
            b_result = True
        elif s_reason == "focusout":
            # print( "focusout set value to Slider, new label and old button")
            self.__mwp_entry_green_focus_in( None)
            b_result = True
        elif s_reason == "key":
            # print( "key")
            if 'a' <= s_call <= 'f' or 'A' <= s_call <= 'F' or '0' <= s_call <= '9':
                if len( s_before) > 2:
                    b_result = False
                else:
                    b_result = True
            else:
                # print( "manage value")
                if s_call.isprintable() or s_call.isspace():
                    b_result = False
                else:
                    print( mt_hexlify_byte_string( b's_call', ":"))
                    b_result = True
        else:
            # print( "does nothing")
            b_result = True

        return b_result

    # ####################### mwp_blue_max_of_two_chars_and_filter ########################
    def mwp_blue_max_of_two_chars_and_filter( self, s_before, s_call, s_reason) -> bool:
    # def mwp_blue_max_of_two_chars_and_filter( self, s_before, s_after, s_call, s_value, s_reason) -> bool:
        """ Validates each character as it is entered in the entry for a color value
            parameter setup is '%P', '%s', '%S', '%v', '%V'
            no used : '%d', '%W'
            posibility are
            '%d'	Action code: 0 for an attempted deletion, 1 for an attempted insertion, or -1 if the callback was called for focus in, focus out, or a change to the textvariable.
            '%i'	When the user attempts to insert or delete text, this argument will be the index of the beginning of the insertion or deletion. If the callback was due to focus in, focus out, or a change to the textvariable, the argument will be -1.
            '%P'	The value that the text will have if the change is allowed.
            '%s'	The text in the entry before the change.
            '%S'	If the call was due to an insertion or deletion, this argument will be the text being inserted or deleted.
            '%v'	The current value of the widget's validate option.
            '%V'	The reason for this callback: one of 'focusin', 'focusout', 'key', or 'forced' if the textvariable was changed.
            '%W'	The name of the widget.
        """
        # print( "mwp_blue_max_of_two_chars_and_filter() ")
        # print( f"i_action  d : {i_action}")
        # print( f"s_before  P : {s_before}")
        # print( f"s_after   s : {s_after}")
        # print( f"s_call    S : {s_call}")
        # print( f"s_value   v : {s_value}")
        # print( f"s_reason  V : {s_reason}")
        # print( f"s_name    W : {s_name}")
        # a_widget = self.w_tk_root.nametowidget( s_name)
        # print( "widget      = ", a_widget)

        b_result = False
        if s_reason == "focusin":
            # print( "focusin set value to Slider, new label and old button")
            self.__mwp_entry_blue_focus_in( None)
            b_result = True
        elif s_reason == "focusout":
            # print( "focusout set value to Slider, new label and old button")
            self.__mwp_entry_blue_focus_in( None)
            b_result = True
        elif s_reason == "key":
            # print( "key")
            if 'a' <= s_call <= 'f' or 'A' <= s_call <= 'F' or '0' <= s_call <= '9':
                if len( s_before) > 2:
                    b_result = False
                else:
                    b_result = True
            else:
                # print( "manage value")
                if s_call.isprintable() or s_call.isspace():
                    b_result = False
                else:
                    print( mt_hexlify_byte_string( b's_call', ":"))
                    b_result = True
        else:
            # print( "does nothing")
            b_result = True

        return b_result

    # ####################### mwp_select_color_rad_btn ########################
    def mwp_select_color_rad_btn( self, i_offset):
        """ Select the radio button color in the pallet """
        self.a_pallet_button_lst[i_offset].select()

    # ####################### mwp_color_btn_rad ########################
    def mwp_color_btn_rad( self, i_number):
        """ Pallet of color buttons. i_number is a value form 0 to 255 one of the pallet radio button """
        if self.i_color_to_copy_offset != -1:
            i_result = self.c_alert_windows.aw_create_alert_window( 2, "Question",
                "Confirm copy of the color at index " + str( self.i_color_to_copy_offset) + " to the index " + str( i_number) + " ?")
            self.i_color_to_copy_offset = -1
            if i_result == 1:
                self.__mwp_set_color_in_pallet( i_number)
        elif self.i_color_line_to_copy_offset != -1:
            __i_complete = int( i_number / 16)
            i_result = self.c_alert_windows.aw_create_alert_window( 2, "Question",
                "Confirm copy of the line " + str( self.i_color_line_to_copy_offset) + " to the line " + str( __i_complete) + " ?")
            self.i_color_line_to_copy_offset = -1
            if i_result == 1:
                self.__mwp_set_line_in_pallet( i_number, __i_complete)
        else:
            self.mwp_entry_black_focus_out()
            #print( "mwp_color_btn_rad() i_number       = ", str( i_number))
            a_original_img = self.c_main_image.mwi_get_original_image()
            a_pallet_list = a_original_img.getpalette()
            #print( "mwp_color_btn_rad() a_pallet_list = ", str( len( a_pallet_list)))
            if (i_number * 3) > len( a_pallet_list):
                print( "mwp_color_btn_rad() i_number       = ", str( i_number))
                print( "mwp_color_btn_rad() a_pallet_list = ", str( len( a_pallet_list)))
                print( "mwp_color_btn_rad() FAILED")

            i_tmp_number = i_number * 3
            i_red = a_pallet_list[i_tmp_number]
            i_green = a_pallet_list[i_tmp_number + 1]
            i_blue = a_pallet_list[i_tmp_number + 2]
            if int( i_red) > 15:
                s_red = f'{int( i_red):X}'
            else:
                s_red = f'0{int( i_red):X}'
            if int( i_green) > 15:
                s_green = f'{int( i_green):X}'
            else:
                s_green = f'0{int( i_green):X}'
            if int( i_blue) > 15:
                s_blue = f'{int( i_blue):X}'
            else:
                s_blue = f'0{int( i_blue):X}'

            self.a_red_input_var.set( s_red)                            # hex string
            self.a_red_ntr_dec_lbl.configure( text=str( i_red))         # int to string
            self.a_green_input_var.set( s_green)
            self.a_green_ntr_dec_lbl.configure( text=str( i_green))
            self.a_blue_input_var.set( s_blue)
            self.a_blue_ntr_dec_lbl.configure( text=str( i_blue))
            self.a_the_color_new_lbl.configure( background= "#" + s_red + s_green + s_blue)
            self.a_color_old_btn.configure( background= "#" + s_red + s_green + s_blue)
            __i_complete = int( i_number / 16)
            __i_rest = i_number - ( __i_complete * 16)
            # print( f'number= {i_number} -> complete= {__i_complete} rest= {__i_rest}')
            self.a_btn_offset_lbl.configure( text=str( i_number))       # label under Offset
            if i_number > 15:
                self.a_btn_x_lbl.configure( text=str( __i_complete))    # label under Pallet Y
            else:
                self.a_btn_x_lbl.configure( text="0")                   # label under Pallet Y

            self.a_btn_y_lbl.configure( text=str( __i_rest))            # label under Offset X

            # Draw the SCB rectangle
            self.c_main_image.mwi_draw_scb_bar( i_number)

             #set value for import a pallet from an another windows
            self.c_main_icon_bar.mwib_set_selected_pallet_line( __i_complete)

    # ####################### __mwp_set_color_in_pallet ########################
    def __mwp_set_color_in_pallet( self, i_new_index):
        """ Set a new color value in pallet  """
        s_red   = self.a_red_input_var.get().upper()
        s_green = self.a_green_input_var.get().upper()
        s_blue  = self.a_blue_input_var.get().upper()
        if i_new_index == -1:
            i_index = int( self.a_btn_offset_lbl.cget( "text"))
        else:
            i_index = i_new_index
        # print( "i_index    = ", str( i_index))
        a_pallet_button = self.a_pallet_button_lst[i_index]
        # ready when color modification will be done
        # print( "btn: red   = ", s_red, "  green = ", s_green, "  blue  = ", s_blue)
        a_pallet_button.configure( background= "#" + s_red + s_green + s_blue)
        # Update the picture pallet
        a_original_img = self.c_main_image.mwi_get_original_image()
        a_pallet_list = a_original_img.getpalette()
        # s_red   = self.a_red_ntr_dec_lbl.cget( "text")
        # s_green = self.a_green_ntr_dec_lbl.cget( "text")
        # s_blue  = self.a_blue_ntr_dec_lbl.cget( "text")
        # print( "btn: red   = ", s_red, "  green = ", s_green, "  blue  = ", s_blue)
        # i_index is a number of radio button and the pallete is 3 int for RGB so I do a * 3
        i_pallet_index = i_index * 3
        # print( "pal: red   = ", str( a_pallet_list[ i_pallet_index]), "  green = ", str( a_pallet_list[ i_pallet_index+1]), "  blue  = ", str( a_pallet_list[ i_pallet_index+2]))
        a_pallet_list[ i_pallet_index] = int( self.a_red_ntr_dec_lbl.cget( "text"))
        a_pallet_list[ i_pallet_index+1] = int( self.a_green_ntr_dec_lbl.cget( "text"))
        a_pallet_list[ i_pallet_index+2] = int( self.a_blue_ntr_dec_lbl.cget( "text"))
        # print( "pal: red   = ", str( a_pallet_list[ i_pallet_index]), "  green = ", str( a_pallet_list[ i_pallet_index]+1), "  blue  = ", str( a_pallet_list[ i_pallet_index+2]))
        a_original_img.putpalette( a_pallet_list, rawmode='RGB')
        self.c_main_windows.mw_update_main_window( self.c_main_icon_bar.mwib_get_get_path_filename(), a_original_img)
        self.mwp_color_btn_rad( i_index)

        i_click_pos_x = self.c_main_image.mwi_get_mouse_pos_x_var()
        i_click_pos_y = self.c_main_image.mwi_get_mouse_pos_y_var()
        a_work_img = self.c_main_image.mwi_get_working_image()
        i_offset = a_work_img.getpixel( (i_click_pos_x, i_click_pos_y))

        # Draw bar chart for colors in usage in a line
        self.c_main_image.mwi_draw_bar_chart( i_offset, i_click_pos_y)

        # Display zoom of a part of the picture
        self.mwp_draw_zoom_square( i_click_pos_x, i_click_pos_y)

        self.w_tk_root.update()

    # ####################### __mwp_set_line_in_pallet ########################
    def __mwp_set_line_in_pallet( self, i_new_index, i_line_number):
        """ Set a new color value in pallet  """
        # Update the picture pallet
        a_original_img = self.c_main_image.mwi_get_original_image()
        a_pallet_list = a_original_img.getpalette()

        i_destination = (i_line_number - 1) * 16 * 3
        for i_loop in range( self.i_color_line_to_copy_offset * 16 * 3, 16*3, 1):
            a_pallet_list[i_destination] = a_pallet_list[ i_loop]
            i_destination += 1

        a_original_img.putpalette( a_pallet_list, rawmode='RGB')

        self.__mwp_set_color_in_pallet( i_new_index)

    # ####################### mwp_change_focus ########################
    def mwp_change_focus( self, event):
        """ De selected an entry widget, when a button is clicked ie the pallet button """
        event.widget.focus_set()

    # ####################### mwp_draw_zoom_square ########################
    def mwp_draw_zoom_square( self, i_position_x, i_position_y):
        """ Draw the zoom square part * 8 of the picture """
        # print( "mwp_draw_zoom_square : i_position_x= " + str( i_position_x) + " i_position_x= " + str( i_position_y))
        i_contour = 26

        i_box_top = (i_position_x - i_contour, i_position_y - i_contour, i_position_x + i_contour, i_position_y + i_contour)
        a_work_img = self.c_main_image.mwi_get_working_image()
        a_part_image = a_work_img.crop( i_box_top)
        width, height = a_part_image.size
        # a_part_image.show()

        self.a_zoom_work_img = a_part_image.resize( (width * 4, height * 4))     # Total of zoom is x 8
        self.a_render_zoom = ImageTk.PhotoImage( self.a_zoom_work_img)
        self.a_zoom_lbl.config( image=self.a_render_zoom)
        self.a_zoom_lbl.photo = self.a_render_zoom

        # Adapt color of the label text "   _     _"
        i_result = 0
        i_red   = int( self.a_red_ntr_dec_lbl.cget( "text"))
        i_green = int( self.a_green_ntr_dec_lbl.cget( "text"))
        i_blue  = int( self.a_blue_ntr_dec_lbl.cget( "text"))
        if i_red > 128:
            i_result +=1
        if i_green > 128:
            i_result +=1
        if i_blue > 128:
            i_result +=1
        if i_result >= 2:
            self.a_zoom_lbl.config( fg='black')
        else:
            self.a_zoom_lbl.config( fg='white')

    # ####################### mwp_get_around_cursor ########################
    def mwp_get_around_cursor( self) -> int:
        """ the state for cursor """
        return self.i_around_cursor

    # ####################### mwp_get_pallet_btn ########################
    def mwp_get_pallet_btn( self, i_element) -> Radiobutton:
        """ Return the color of the button radio """
        return self.a_pallet_button_lst[i_element]

    # ####################### mwp_reset_around_cursor ########################
    def mwp_reset_around_cursor( self):
        """ the state for cursor """
        self.i_around_cursor = -1

    # ####################### __mv_entry_red_focus_out ########################
    def mwp_entry_black_focus_out( self):
        """ No selected entry widget focus events restore color to black """
        self.a_color_slider.config( troughcolor='light grey')
