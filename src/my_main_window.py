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
import array

from datetime import datetime
from tkinter import font, Label, Button, Entry, Canvas, Scale, StringVar
from tkinter.ttk import Separator
from functools import partial

# from ttkthemes              import ThemedTk, THEMES, ThemedStyle
from PIL import Image, ImageTk

import src.my_constants as constant
# from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_main_window_icons_bar import MyMainWindowIconsBar
from .my_tools import open_file

# __name__ = "MyMainWindow"

# ###############################################################################################
# #######========================= constant private =========================

MAIN_WINDOWS_WIDTH = 1060
MAIN_WINDOWS_HEIGHT = 824
WAIT_TIME_COM = 0.05

# ###############################################################################################
# #######=========================     GUI     =========================
# ####################### MyMainWindow ########################
class MyMainWindow:
    """ Create the main Windows of the application. """
    # Optimizing memory usage with slots
    # __slots__ = ["w_main_windows", "a_list_application_info", "a_dico_mw_gui_element" ]

    # ####################### __init__ ########################
    def __init__( self, w_main_windows, list_application_info):
        """
            All this parameter are created in main()
            w_main_windows : the windows created by tk
            a_list_application_info : les inforamtions de l'application
        """
        print()
        self.w_main_windows = w_main_windows
        self.a_list_application_info = list_application_info
        # Size of the main windows
        self.i_main_window_width = MAIN_WINDOWS_WIDTH
        self.i_main_window_height = MAIN_WINDOWS_HEIGHT
        # Position of the main windows
        self.i_main_window_x = 20
        self.i_main_window_y = 20
        self.w_main_windows.background = constant.BACKGROUD_COLOR_UI
        self.c_the_icons = MyIconPictures( w_main_windows)
        self.c_mains_icon_bar = None
        self.s_platform = platform.system()
        self.a_palette_button_lst = []
        self.a_work_img = None
        self.a_bmp_image_file = None
        self.a_picture_lbl = None
        self.a_scb_cnvs = None
        self.a_render = None
        self.a_image = None
        self.a_filename_lbl = None
        self.a_mouse_pos_x = None
        self.a_mouse_pos_y = None
        self.a_mouse_pos_x_input_var= StringVar()
        self.a_mouse_pos_y_input_var = StringVar()
        self.a_pos_x_true_lbl = None
        self.a_pos_y_true_lbl = None
        self.a_color_lbl = None
        self.a_scb_lbl = None
        self.a_scb_start_lbl = None
        self.a_scb_start_true_lbl = None
        self.a_scb_end_lbl = None
        self.a_scb_end_true_lbl = None        
        self.a_pic_color_lbl = None
        self.a_bar_chart_cnvs = None
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

    # ####################### __repr__ ########################
    def __repr__( self):
        """ A dundle method for description """
        return f"{type(self).__name__}({self.w_main_windows}, {self.a_list_application_info})"

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

    # ####################### __mw_click_on_picture ########################
    def __mw_click_on_picture( self, event):
        """ Show position of the mouse in the loaded picture and repair SCB to draw a rect """
        self.__mv_entry_black_focus_out( None)
        if self.a_work_img:
            # print( "i_pos_x= " + str( event.x) + "   i_pos_y= " + str( event.y))
            i_pos_x = max( event.x, 0)
            i_pos_x = min( event.x, 640)
            i_pos_y = max( event.y, 0)
            i_pos_y = min( event.y, 400)

            self.a_mouse_pos_x_input_var.set( str( i_pos_x))
            self.a_mouse_pos_y_input_var.set( str( i_pos_y))
            self.a_pos_x_true_lbl.configure( text=str( int( ( i_pos_x & 1022) / 2)))
            self.a_pos_y_true_lbl.configure( text=str( int( ( i_pos_y & 1022) / 2)))

            i_offset = self.a_work_img.getpixel( ( i_pos_x, i_pos_y))
            self.a_color_lbl.configure( text=str( i_offset))
            self.a_scb_lbl.configure( text=str( int( i_offset/16)))
            self.a_pic_color_lbl.configure( background=self.a_palette_button_lst[i_offset].cget( 'bg'))

            # Draw the SCB rectangle
            i_palette_number = int( i_offset/16) * 16
            print( r"/  i_pos_x= " + str( i_pos_x) + "   i_pos_y= " + str( i_pos_y)+ "   i_offset= " + str( i_offset) + "   i_palette_number= " + str( i_palette_number))
            if i_pos_y & 1:
                i_pos_y -= 1
            if i_pos_x & 1:
                i_pos_x -= 1

            self.a_scb_cnvs.delete("all")
            for i_loop in range( 0, 398, 2):
                i_offset = self.a_work_img.getpixel( ( i_pos_x, i_loop))
                i_inter = int( i_offset/16) * 16
                if (i_inter == i_palette_number):
                    self.a_scb_cnvs.create_rectangle( 0, i_loop, 20, i_loop+1, fill='blue', outline='blue')
                else:
                    i_inter = 0

            # Draw bar chart for couleur in usage in a line 
            self.a_bar_chart_cnvs.delete( "all")
            a_usage_color_rry = array.array( 'i')
            a_usage_color_rry = [1] * 16

            for i_loop in range( 0, 638, 2):
                i_offset = self.a_work_img.getpixel( ( i_loop, i_pos_y))
                i_offset = i_offset - (int( i_offset / 16) * 16)
                a_usage_color_rry[i_offset] +=1

            for i_loop in range( 0, 16, 1):
                a_usage_color_rry[i_loop] = int( ((a_usage_color_rry[i_loop] * 74) / 320) + 0.5)
                print( str(i_loop) + "  "+ str( a_usage_color_rry[i_loop]))

            i_colmun_x = 0
            for i_loop in range( 0, 16, 1):
                i_hauteur = a_usage_color_rry[i_loop]
                self.a_bar_chart_cnvs.create_rectangle( i_colmun_x, 74-i_hauteur, i_colmun_x+20, 74, fill=self.a_palette_button_lst[i_palette_number+i_loop].cget( 'bg'), outline='white')
                i_colmun_x += 24

            self.w_main_windows.update()
            print()

    # ####################### __mw_picture_zone ########################
    def __mw_picture_zone( self, a_pic_frame):
        """ Frame with the picture to left, and details to right """

        i_index_base_block = 0
        a_pic_sep_h0 = Separator( a_pic_frame, orient='horizontal')
        a_pic_sep_h0.grid(row=i_index_base_block, column=0, columnspan=1, sticky='ew')
        a_pic_sep_lbl_h0 = Label( a_pic_frame, text="Picture", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h0.grid( row=i_index_base_block, column=0, padx=15)
        a_pic_sep_h0 = Separator( a_pic_frame, orient='horizontal')
        a_pic_sep_h0.grid( row=i_index_base_block, column=1, columnspan=1, sticky='ew')
        a_pic_sep_lbl_h0 = Label( a_pic_frame, text="Details", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h0.grid( row=i_index_base_block, column=1, columnspan=1, padx=81, sticky='ew')

        i_index_base_block += 1
        self.a_picture_lbl = Label( a_pic_frame, padx=0, pady=0, image=None, width=640, height=410, background=constant.BACKGROUD_COLOR_UI)
        self.a_picture_lbl.grid( row=i_index_base_block, column=0, sticky='nw')
        self.a_picture_lbl.bind( '<Button>', self.__mw_click_on_picture)

        # Create SCB frame to fraw rectangle to present SCB
        a_scb_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_scb_frame.place( x=644, y=28, width=20, height=400)

        self.a_scb_cnvs = Canvas( a_scb_frame, width=20, height=400, background='green', highlightthickness=0)
        self.a_scb_cnvs.grid( row=0, column=0, sticky='ewns')

        # Create details frame
        a_details_pic_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_details_pic_frame.place( x=664, y=30, width=self.i_main_window_width - 664, height=400)

        a_bar_chart_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_bar_chart_frame.place( x=664, y=30+(400-74), width=self.i_main_window_width - 438, height=74)

        self.a_bar_chart_cnvs = Canvas( a_bar_chart_frame, width=self.i_main_window_width - (438+8), height=74, background=constant.BACKGROUD_COLOR_UI, highlightthickness=0)
        self.a_bar_chart_cnvs.grid( row=0, column=0, padx=4, sticky='ewns')

        i_index_base_block = 0
        a_pic_sep_lbl_h2 = Label( a_details_pic_frame, text="File name", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h2.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1)

        i_index_base_block += 1
        self.a_filename_lbl = Label( a_details_pic_frame, text="   ", background='white', foreground='black')
        self.a_filename_lbl.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_space_lbl_h1 = Label( a_details_pic_frame, text="", background=constant.BACKGROUD_COLOR_UI)
        a_space_lbl_h1.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1)

        i_index_base_block += 1
        a_pic_sep_lbl_h3 = Label( a_details_pic_frame, text="Mouse position", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h3.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1)

        i_index_base_block += 1
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="X ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4, pady=1)
        self.a_mouse_pos_x = Entry( a_details_pic_frame, textvariable=self.a_mouse_pos_x_input_var, width=constant.DEFAULT_BUTTON_WIDTH, background='white', foreground='black')
        self.a_mouse_pos_x.grid( row=i_index_base_block, column=2, padx=4, pady=1)
        self.a_pos_x_true_lbl = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH, background='light grey', foreground='black')
        self.a_pos_x_true_lbl.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="Y ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4, pady=1)
        self.a_mouse_pos_y = Entry( a_details_pic_frame, textvariable=self.a_mouse_pos_y_input_var, width=constant.DEFAULT_BUTTON_WIDTH, background='white', foreground='black')
        self.a_mouse_pos_y.grid( row=i_index_base_block, column=2, padx=4, pady=1)
        self.a_pos_y_true_lbl = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH, background='light grey', foreground='black')
        self.a_pos_y_true_lbl.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h5 = Label( a_details_pic_frame, text="Color offset", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h5.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1)

        i_index_base_block += 1
        self.a_color_lbl = Label( a_details_pic_frame, text="   ", background='white', foreground='black')
        self.a_color_lbl.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h6 = Label( a_details_pic_frame, text="Palette number / SCB", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h6.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1)

        i_index_base_block += 1
        self.a_scb_lbl = Label( a_details_pic_frame, text="   ", background='white', foreground='black')
        self.a_scb_lbl.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="From", width=5, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4, pady=1)
        self.a_scb_start_lbl = Label( a_details_pic_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH, background='light grey', foreground='black')
        self.a_scb_start_lbl.grid( row=i_index_base_block, column=2, padx=4, pady=1, sticky='ew')
        self.a_scb_start_true_lbl = Label( a_details_pic_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH, background='light grey', foreground='black')
        self.a_scb_start_true_lbl.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="To", width=5, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4, pady=1)
        self.a_scb_end_lbl = Label( a_details_pic_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH, background='light grey', foreground='black')
        self.a_scb_end_lbl.grid( row=i_index_base_block, column=2, padx=4, pady=1, sticky='ew')
        self.a_scb_end_true_lbl = Label( a_details_pic_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH, background='light grey', foreground='black')
        self.a_scb_end_true_lbl.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_color_name_lbl = Label( a_details_pic_frame, text="RGB Color", background=constant.BACKGROUD_COLOR_UI)
        a_color_name_lbl.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1)

        i_index_base_block += 1
        self.a_pic_color_lbl = Label( a_details_pic_frame, text=None, background='white', foreground='black')
        self.a_pic_color_lbl.grid( row=i_index_base_block, rowspan=2, column=1, columnspan=3, padx=4, pady=1, sticky='nsew')
        # self.a_the_color_new_lbl = Label( a_color_bottom_frame, text="", width=8, background=constant.LIGHT_COLOR_UI, foreground='black')
        # self.a_the_color_new_lbl.grid( row=i_index_base_block, rowspan=4, column=2, columnspan=1, padx=4, pady=1, sticky='ewns')

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

    # ####################### __mw_restore_old_color ########################
    def __mw_restore_old_color( self):
        """ This button restore the old color same as the pallette button clicked """
        s_old_color_of_button = self.a_color_old_btn.cget( 'bg')
        __s_color_true=s_old_color_of_button.replace( "#","")
        s_red = __s_color_true[0:0+2]
        s_green = __s_color_true[2:2+2]
        s_blue = __s_color_true[4:4+2]
        i_number = int(self.a_btn_offset_lbl.cget( "text"))
        self.__mw_color_button( i_number, "#" + s_red, s_green, s_blue)

    # ####################### __mv_update_red_entry ########################
    def __mv_update_red_entry( self, i_value):
        """" Scale is moving update red : entry in hex, label in dec and color of new color label """
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

    # ####################### __mv_update_green_entry ########################
    def __mv_update_green_entry( self, i_value):
        """" Scale is moving update green : entry in hex, label in dec and color of new color label """
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

    # ####################### __mv_update_blue_entry ########################
    def __mv_update_blue_entry( self, i_value):
        """" Scale is moving update blue : entry in hex, label in dec and color of new color label """
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

    # ####################### __mv_entry_red_focus_in ########################
    def __mv_entry_red_focus_in( self, event):
        """ Select of red entry widget focus events prepare scale to move """
        self.a_color_slider.config( foreground='red')
        self.a_color_slider.set( int(self.a_red_ntr.get(), 16) )
        self.a_color_slider.config( command=self.__mv_update_red_entry )

    # ####################### __mv_entry_green_focus_in ########################
    def __mv_entry_green_focus_in( self, event):
        """ Select of green entry widget focus events prepare scale to move """
        self.a_color_slider.config( foreground='green')
        self.a_color_slider.set( int(self.a_green_ntr.get(), 16) )
        self.a_color_slider.config( command=self.__mv_update_green_entry )

    # ####################### __mv_entry_blue_focus_in ########################
    def __mv_entry_blue_focus_in( self, event):
        """ Select of blue entry widget focus events prepare scale to move """
        self.a_color_slider.config( foreground='blue')
        self.a_color_slider.set( int(self.a_blue_ntr.get(), 16) )
        self.a_color_slider.config( command=self.__mv_update_blue_entry )

    # ####################### __mv_entry_red_focus_out ########################
    def __mv_entry_black_focus_out( self, event):
        """ no selected entry widget focus events restore color to black """
        self.a_color_slider.config( foreground='black')

    # ####################### __mw_palette_zone ########################
    def __mw_palette_zone(self, a_bottom_frame):
        """ Frame with the palette button to left, and details to right """

        i_index_base_block = 0
        a_palette_sep_h2 = Separator( a_bottom_frame, orient='horizontal')
        a_palette_sep_h2.grid( row=i_index_base_block, column=0, columnspan=8, sticky='ew')
        a_palette_sep_lbl_h2 = Label( a_bottom_frame, text="Palette", background=constant.BACKGROUD_COLOR_UI)
        a_palette_sep_lbl_h2.grid( row=i_index_base_block, column=0, columnspan=2, padx=260)

        a_palette_sep_h3 = Separator( a_bottom_frame, orient='horizontal')
        a_palette_sep_h3.grid( row=i_index_base_block, column=9, columnspan=4, sticky='ew')
        a_palette_sep_lbl_h3 = Label( a_bottom_frame, text="Color", background=constant.BACKGROUD_COLOR_UI)
        a_palette_sep_lbl_h3.grid( row=i_index_base_block, column=9, columnspan=4, padx=120)

        # Create palette button left frame
        a_palette_bottom_frame = tk_gui.Frame( a_bottom_frame, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_palette_bottom_frame.place( x=2, y=20, width=570, height=276 )

        # creating a font object with little size for color buttons to reduce their size
        a_font_label = font.Font(size=6)
        a_font_button = font.Font(size=5)

        i_index_base_block = 0
        i_index_base_column = 1
        for i_loop in range( 0, 16, 1):
            a_label = Label(a_palette_bottom_frame, text=str(i_loop), background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            i_index_base_column += 1

        i_index_base_block += 1
        i_index_base_column = 0
        i_to = 0
        for i_loop in range( 0, 16, 1):
            i_from = i_to
            i_to = i_to + 48
            a_label = Label(a_palette_bottom_frame, text=str(i_loop), background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            i_index_base_column += 1
            for _ in range( i_from, i_to, 3):
                a_button_color = Button( a_palette_bottom_frame, text='', width=4, height=1, background=constant.LIGHT_COLOR_UI, font=a_font_button)
                a_button_color.grid( row=i_index_base_block, column=i_index_base_column, padx=4, pady=2)
                self.a_palette_button_lst.append( a_button_color)
                i_index_base_column += 1

            self.w_main_windows.update()
            i_index_base_column = 0
            i_index_base_block += 1

        # Create color button right frame
        a_color_bottom_frame = tk_gui.Frame( a_bottom_frame, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_color_bottom_frame.place( x=572, y=20, width=self.i_main_window_width - 572, height=276 )

        i_index_base_block = 0
        a_color_name_lbl = Label( a_color_bottom_frame, text="Red", background=constant.BACKGROUD_COLOR_UI, foreground='red')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1)
        a_color_name_lbl = Label( a_color_bottom_frame, text="RGB Color", background=constant.BACKGROUD_COLOR_UI)
        a_color_name_lbl.grid( row=i_index_base_block, column=2, columnspan=2, padx=4, pady=1)

        i_index_base_block += 1
        self.a_red_ntr = Entry( a_color_bottom_frame, textvariable=self.a_red_input_var, validate="key", validatecommand=( a_color_bottom_frame.register( self.__mw_set_max_len_to_fifteen_chars_and_filter), '%d', '%s', '%S'), width=constant.DEFAULT_BUTTON_WIDTH, background=constant.LIGHT_COLOR_UI, foreground='red')
        self.a_red_ntr.grid( row=i_index_base_block, column=0, columnspan=1, padx=4, sticky='w')
        self.a_red_ntr.bind( "<FocusIn>", self.__mv_entry_red_focus_in)
        self.a_red_ntr_dec_lbl = Label( a_color_bottom_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH, background='light grey', foreground='red')
        self.a_red_ntr_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=4, sticky='ew')

        a_offset_lbl = Label( a_color_bottom_frame, text="New", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=2, columnspan=1, padx=4, pady=1, sticky='ew')
        a_offset_lbl = Label( a_color_bottom_frame, text="Old", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=3, columnspan=1, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_color_name_lbl = Label( a_color_bottom_frame, text="Green", background=constant.BACKGROUD_COLOR_UI, foreground='green')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1)
        self.a_the_color_new_lbl = Label( a_color_bottom_frame, text="", width=8, background=constant.LIGHT_COLOR_UI, foreground='black')
        self.a_the_color_new_lbl.grid( row=i_index_base_block, rowspan=4, column=2, columnspan=1, padx=4, pady=1, sticky='ewns')
        self.a_color_old_btn = Button( a_color_bottom_frame, text='', command=self.__mw_restore_old_color, width=7, height=1, background='light grey')
        self.a_color_old_btn.grid( row=i_index_base_block, rowspan=4, column=3, columnspan=1, padx=4, pady=1, sticky='ewns')

        i_index_base_block += 1
        self.a_green_ntr = Entry( a_color_bottom_frame, textvariable=self.a_green_input_var, validate="key", validatecommand=( a_color_bottom_frame.register( self.__mw_set_max_len_to_fifteen_chars_and_filter), '%d', '%s', '%S'), width=constant.DEFAULT_BUTTON_WIDTH, background=constant.LIGHT_COLOR_UI, foreground='green')
        self.a_green_ntr.grid( row=i_index_base_block, column=0, padx=4, sticky='w')
        self.a_green_ntr.bind( "<FocusIn>", self.__mv_entry_green_focus_in)
        self.a_green_ntr_dec_lbl = Label( a_color_bottom_frame, text="   ", background='light grey', foreground='green')
        self.a_green_ntr_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=4, sticky='ew')
        i_index_base_block += 1
        a_color_name_lbl = Label( a_color_bottom_frame, text="Blue", background=constant.BACKGROUD_COLOR_UI, foreground='blue')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1)
        i_index_base_block += 1
        self.a_blue_ntr = Entry( a_color_bottom_frame, textvariable=self.a_blue_input_var, validate="key", validatecommand=( a_color_bottom_frame.register( self.__mw_set_max_len_to_fifteen_chars_and_filter), '%d', '%s', '%S'), width=constant.DEFAULT_BUTTON_WIDTH, background=constant.LIGHT_COLOR_UI, foreground='blue')
        self.a_blue_ntr.grid( row=i_index_base_block, column=0, padx=4, sticky='w')
        self.a_blue_ntr.bind( "<FocusIn>", self.__mv_entry_blue_focus_in)
        self.a_blue_ntr_dec_lbl = Label( a_color_bottom_frame, text="   ", background='light grey', foreground='blue')
        self.a_blue_ntr_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=4, sticky='ew')

        i_index_base_block += 1
        self.a_color_slider = Scale( a_color_bottom_frame, from_=0, to=255, orient='horizontal', background=constant.BACKGROUD_COLOR_UI, highlightbackground='darkgray')
        self.a_color_slider.grid( row=i_index_base_block, column=0, columnspan=4, padx=1, pady=4, sticky='ew')

        i_index_base_block += 1
        a_offset_lbl = Label( a_color_bottom_frame, text="Offset", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1, sticky='ew')
        a_offset_lbl = Label( a_color_bottom_frame, text="Palette Y", background=constant.BACKGROUD_COLOR_UI)
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
        a_change_color_btn = Button( a_color_bottom_frame, text='Set color', command=self.__mw_set_color_in_palette, width=14, height=1, background=constant.BACKGROUD_COLOR_UI)
        a_change_color_btn.grid( row=i_index_base_block, column=0, columnspan=4, padx=4, pady=6, sticky='ew')

        # self.w_main_windows.update()
        # i_col, i_row = self.a_red_ntr_dec_lbl.grid_size()
        # print( f'GRID : col= {i_col} row= {i_row}')
        # i_width = self.a_red_ntr_dec_lbl.winfo_width()
        # print( f'a_red_ntr_dec_lbl : width= {i_width}')

    # ####################### __mw_set_max_len_to_fifteen_chars_and_filter ########################
    def __mw_set_max_len_to_fifteen_chars_and_filter( self, i_action, s_string_apres, s_insert):
        """ Validates each character as it is entered in the entry for a color value """
        # print( "i_action       %d = ", str( i_action))
        # print( "i_position     %i = ", str( i_position))
        # print( "s_string_avant %P = ", s_string_avant)
        # print( "s_string_apres %s = ", s_string_apres)
        # print( "s_insert       %S = ", s_insert)
        # print( "a_name         %W = ", s_name)

        if (s_insert >= 'a') & (s_insert <= 'f'):
            s_insert.upper()

        if (s_insert == '') | ((s_insert >= 'A') & (s_insert <= 'F')) | ( (s_insert >= '0') & (s_insert <= '9')):
            # print( '__mw_set_max_len_to_fifteen_chars_and_filter() : __s_value len = ' + str( len( __s_value) + 1) )
            if int( i_action) == 0:     # deletion
                # print( '__mw_set_max_len_to_fifteen_chars_and_filter() : action = deletion' )
                if len( s_string_apres) + 1 > 8:
                    b_result = True
                else:
                    self.w_main_windows.bell()
                    b_result = False
            elif int( i_action) == 1:   # insertion
                # print( '__mw_set_max_len_to_fifteen_chars_and_filter() : action = insertion' )
                if len( s_string_apres) + 1 > 15:
                    self.w_main_windows.bell()
                    b_result = False
                else:
                    b_result = True
            else:
                # print( '__mw_set_max_len_to_fifteen_chars_and_filter() : autre' )
                b_result = True
        else:
            self.w_main_windows.bell()
            b_result = False

        return b_result

    # ####################### __mw_color_button ########################
    def __mw_color_button(self, i_number, s_red, s_green, s_blue):
        """ Palette of color buttons. note: s_red start by char '#' """
        # self.w_main_windows.bell()
        self.__mv_entry_black_focus_out( None)
        s_red_true=s_red.replace( "#","")
        self.a_red_input_var.set( s_red_true)
        self.a_red_ntr_dec_lbl.configure( text=str( int( s_red_true, 16)))
        self.a_green_input_var.set( s_green)
        self.a_green_ntr_dec_lbl.configure( text=str( int( s_green, 16)))
        self.a_blue_input_var.set( s_blue)
        self.a_blue_ntr_dec_lbl.configure( text=str(int(s_blue, 16)))
        self.a_the_color_new_lbl.configure( background= s_red + s_green + s_blue)
        self.a_color_old_btn.configure( background= s_red + s_green + s_blue)
        __i_complete = int( i_number / 16)
        __i_rest = i_number - ( __i_complete * 16)
        # print( f'number= {i_number} -> complete= {__i_complete} rest= {__i_rest}')
        self.a_btn_offset_lbl.configure( text=str( i_number))         # label under Offset
        if i_number > 15:
            self.a_btn_x_lbl.configure( text=str( __i_complete))      # label under Palette Y
        else:
            self.a_btn_x_lbl.configure( text="0")                     # label under Palette Y

        self.a_btn_y_lbl.configure( text=str(__i_rest))               # label under Offset X

    # ####################### __mw_set_color_in_palette ########################
    def __mw_set_color_in_palette(self):
        """ Set a new color value in palette  """
        self.w_main_windows.bell()
        s_red = self.a_red_input_var.get()
        s_green = self.a_green_input_var.get()
        s_blue = self.a_blue_input_var.get()
        i_index = int(self.a_btn_offset_lbl.cget( "text"))
        a_palette_button = self.a_palette_button_lst[i_index]
        # ready when color modification will be done
        a_palette_button.configure( background= "#" + s_red + s_green + s_blue)
        #
        # to do : Modify the picture palette

    # ####################### __mw_clock_in_window_bar ########################
    def __mw_clock_in_window_bar( self):
        """ Show the date and times in menu bar of the main windows """
        __now = datetime.now()
        # dd/mm/YY H:M:S
        __s_date_time = __now.strftime( "%d/%m/%Y %H:%M:%S")
        __s_windows_title = ' ' + self.a_list_application_info[0] + '                                           ' + __s_date_time
        self.w_main_windows.title( __s_windows_title)
        self.w_main_windows.after( 1000, self.__mw_clock_in_window_bar)

    # ####################### __mw_print_widget_under_mouse ########################
    def __mw_print_widget_under_mouse( self, root):
        """ Show position of the mouse in the loaded picture """
        if self.a_work_img:
            self.__mv_entry_black_focus_out( None)
            # i_pos_x = root.winfo_x()
            # i_pos_y = root.winfo_y()
            # print( "-> i_pos_x= " + str( i_pos_x) + "   i_pos_y= " + str( i_pos_y))
        #     i_pos_x = max( event.x, 0)
        #     i_pos_x = min( event.x, 640)
        #     i_pos_y = max( event.y, 0)
        #     i_pos_y = min( event.y, 400)

        #     self.a_mouse_pos_x_input_var.set( str( i_pos_x))
        #     self.a_mouse_pos_y_input_var.set( str( i_pos_y))
        #     self.a_pos_x_true_lbl.configure( text=str( int( ( i_pos_x and 1022)/2)))
        #     self.a_pos_y_true_lbl.configure( text=str( int( ( i_pos_y and 1022/2))))

        # __i_pos_x, __i_pos_y = root.winfo_pointerxy()
        # a_widget = root.winfo_containing( __i_pos_x,__i_pos_y)
        # if a_widget:
        #     if "label3" in str( a_widget):
        #         # print( r"\ i_pos_x= " + str(__i_pos_x) + "   i_pos_y= " + str(__i_pos_y))
        #         # x,y = a_widget.winfo_pointerxy()
        #         # print('{}, {}'.format(x, y))
        #         __i_pos_x = __i_pos_x - ( root.winfo_rootx() + 4)
        #         __i_pos_x = max( __i_pos_x, 0)
        #         __i_pos_x = min( __i_pos_x, 640)
        #         __i_pos_y = __i_pos_y - ( root.winfo_rooty() + 98 + 15 + 8)  # 98 = top bar; 15 = separator; 8 = ???
        #         # print( "/ i_pos_x= " + str(__i_pos_x) + "   i_pos_y= " + str(__i_pos_y))
        #         __i_pos_y = max( __i_pos_y, 0)
        #         __i_pos_y = min( __i_pos_y, 400)
        #         self.a_mouse_pos_x_input_var.set( str( __i_pos_x))
        #         self.a_mouse_pos_y_input_var.set( str( __i_pos_y))

        #         # Disabled during debug, evolution of feature is necessary
        #         # if self.a_work_img:
        #         #     i_offset = self.a_work_img.getpixel( (__i_pos_x/2, __i_pos_y/2))
        #         #     self.a_color_lbl.configure( text=str( i_offset))
        #         #     self.a_scb_lbl.configure( text=str( int( i_offset/16)))
        #         #     self.a_pic_color_lbl.configure( background=self.a_palette_button_lst[i_offset].cget( 'bg'))
        #     # else:
        #     #     self.a_mouse_pos_x.delete( 0, 10)
        #     #     self.a_mouse_pos_y.delete( 0, 10)

            root.after( 500, self.__mw_print_widget_under_mouse, root)

    # ####################### __mw_change_focus ########################
    def __mw_change_focus( self, event):
        """ De selected an entry widget, when a button is clicked ie the palette button """
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
        # set windows attribute
        __s_windows_size_and_position = ( str( self.i_main_window_width) + 'x' + str( self.i_main_window_height) + '+' + str( self.i_main_window_x) + '+' + str( self.i_main_window_y) )
        self.w_main_windows.geometry( __s_windows_size_and_position)  # dimension + position x/y a l'ouverture
        self.w_main_windows.update()
        # lock resize of main window
        self.w_main_windows.minsize( self.i_main_window_width, self.i_main_window_height)
        self.w_main_windows.maxsize( self.i_main_window_width, self.i_main_window_height)
        # no resize for both directions
        self.w_main_windows.resizable( False, False)
        self.w_main_windows.iconphoto( True, self.c_the_icons.get_app_photo())

        # Create 1 line of action icons
        a_top_bar_frame = tk_gui.Frame( self.w_main_windows, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)    # background='darkgray'
        a_top_bar_frame.place(x=2, y=0, width=self.i_main_window_width-4, height=98 )   # fill :  must be 'none', 'x', 'y', or 'both'
        self.c_mains_icon_bar = MyMainWindowIconsBar( self, self.w_main_windows, self.a_list_application_info, a_top_bar_frame)
        self.c_mains_icon_bar.mwib_create_top_bar_icons( 1)

        # Create picture frame
        a_pic_frame = tk_gui.Frame( self.w_main_windows, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_pic_frame.place( x=2, y=98, width=self.i_main_window_width-4, height=400+20+8)  # fill :  must be 'none', 'x', 'y', or 'both'
        self.__mw_picture_zone( a_pic_frame)

        # Create palette frame
        a_palette_frame = tk_gui.Frame( self.w_main_windows, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_palette_frame.place( x=2, y=98+400+22+8, width=self.i_main_window_width-4, height=294 )
        self.__mw_palette_zone( a_palette_frame)
        self.w_main_windows.update()

        self.w_main_windows.bind( '<Button>', self.__mw_change_focus)

        # disabled during debug
        # if self.s_platform == "Windows":
        #     self.__mw_clock_in_window_bar()
            # if self.a_work_img:
            #     self.__mw_print_widget_under_mouse( self.w_main_windows)

    # ####################### mw_load_main_window ########################
    def mw_load_main_window(self):
        """ load a picture and fill the interface """
        s_filename = open_file( self.w_main_windows)
        if s_filename:
            print( '\nLoading : ' + s_filename)
            # resize the original bmp from 320x200 to 640x400
            self.a_work_img = Image.open( s_filename)
            width, height = self.a_work_img.size
            if width != 320 and height != 200:
                return False

            self.a_work_img = self.a_work_img.resize( (width*2,height*2))
            width, height = self.a_work_img.size
            if width != 640 and height != 400:
                return False

            # disabled its for debug
            # for i_loop in range( 0, 60, 1):
            #     i_palette_offset = self.a_work_img.getpixel( (0,i_loop))
            #     print( str(i_loop) + " i_palette_Offset = " + str(i_palette_offset) + "  pal= " + str(int(i_palette_offset/16)) + " ndx= " + str( i_palette_offset - (int(i_palette_offset/16)) * 16))

            self.a_render = ImageTk.PhotoImage( self.a_work_img)
            self.a_picture_lbl.config( image=self.a_render)
            self.a_picture_lbl.photo = self.a_render

            self.a_filename_lbl.config( text=os.path.basename( s_filename))

            a_palette_list = self.a_work_img.getpalette()
            # Disabled for debug
            # print( 'Palette :')
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
                    if a_palette_list[ i_index] > 15:
                        s_red = f'#{a_palette_list[ i_index]:X}'
                    else:
                        s_red = f'#0{a_palette_list[ i_index]:X}'
                    if a_palette_list[ i_index + 1] > 15:
                        s_green = f'{a_palette_list[ i_index + 1]:X}'
                    else:
                        s_green = f'0{a_palette_list[ i_index + 1]:X}'
                    if a_palette_list[ i_index + 2] > 15:
                        s_blue = f'{a_palette_list[ i_index + 2]:X}'
                    else:
                        s_blue = f'0{a_palette_list[ i_index + 2]:X}'
                    # Disabled for debug
                    # s_my_hex = s_my_hex + s_red + s_green + s_blue + " "

                    a_button_color = self.a_palette_button_lst[i_element]
                    config_palette_bottom_with_arg = partial( self.__mw_color_button, int(i_index / 3), s_red, s_green, s_blue)
                    a_button_color.configure( command=config_palette_bottom_with_arg)
                    a_button_color.configure( background=s_red + s_green + s_blue)
                    i_element += 1

                    if i_index == 0:
                        self.__mw_color_button( i_index, s_red, s_green, s_blue)

                self.w_main_windows.update()
                # Disabled for debug
                # print( s_my_hex)
                if self.a_work_img:
                    self.__mw_print_widget_under_mouse( self.a_picture_lbl)

            self.w_main_windows.update()
        else:
            return False
        print()

        return True

    # ####################### mw_get_main_window ########################
    def mw_get_main_window( self):
        """ Return the window widget of the main window """
        return self.w_main_windows

    # ####################### mw_get_main_window_height ########################
    def mw_get_main_window_height( self):
        """ Return height of the main window """
        self.i_main_window_height = self.w_main_windows.winfo_height()
        return int( self.i_main_window_height)

    # ####################### mw_get_main_window_width ########################
    def mw_get_main_window_width( self):
        """ Return width of the main window """
        self.i_main_window_width = self.w_main_windows.winfo_width()
        return int( self.i_main_window_width)

    # ####################### mw_get_main_window_pos_x ########################
    def mw_get_main_window_pos_x( self):
        """ Return position X of the main window """
        self.i_main_window_x = self.w_main_windows.winfo_x()
        return int( self.i_main_window_x)

    # ####################### mw_get_main_window_pos_y ########################
    def mw_get_main_window_pos_y( self):
        """ Return position Y of the main window """
        self.i_main_window_y = self.w_main_windows.winfo_y()
        return int( self.i_main_window_y)
