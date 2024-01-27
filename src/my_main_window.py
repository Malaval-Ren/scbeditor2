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
from tkinter import font, Label, Button, Entry, Canvas, Scale, StringVar, Radiobutton, IntVar
from tkinter.ttk import Separator
from functools import partial

# from ttkthemes              import ThemedTk, THEMES, ThemedStyle
from PIL import ImageTk

import src.my_constants as constant
# from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_main_window_icons_bar import MyMainWindowIconsBar
from .my_alert_window import MyAlertWindow
from .my_tools import mt_get_path_separator, mt_save_file

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
        # Position of the main windows
        self.i_main_window_x = 20
        self.i_main_window_y = 20
        self.w_main_windows.background = constant.BACKGROUD_COLOR_UI
        self.c_the_icons = MyIconPictures( self.w_main_windows)
        self.s_platform = platform.system()
        # Size of the main windows
        if self.s_platform == "Linux":
            self.i_main_window_width = 1080
            self.i_main_window_height = 830       
        elif self.s_platform == "Darwin":
            self.i_main_window_width = 1150
            self.i_main_window_height = 834
        elif self.s_platform == "Windows":
            self.i_main_window_width = 1060
            self.i_main_window_height = 824
        else:
            print( 'init() : H : Currently not managed')

        self.c_alert_windows = MyAlertWindow( w_main_windows, list_application_info)
        self.s_init_pathname = os.getcwd()
        self.c_mains_icon_bar = None
        self.a_palette_number_lst = []
        self.a_palette_button_lst = []
        self.a_original_img = None
        self.a_work_img = None
        self.a_bmp_image_file = None
        self.a_picture_lbl = None
        self.a_scb_cnvs = None
        self.a_render = None
        self.a_image = None
        self.a_filename_lbl = None
        self.a_mouse_live_pos_x = None
        self.a_mouse_live_pos_y = None
        self.a_mouse_pos_x = None
        self.a_mouse_pos_y = None
        self.a_mouse_pos_x_input_var = StringVar()
        self.a_mouse_pos_y_input_var = StringVar()
        self.a_pos_x_true_lbl = None
        self.a_pos_y_true_lbl = None
        self.a_color_lbl = None
        self.a_scb_lbl = None
        self.a_line_slider = None
        self.a_scb_start_lbl = None
        self.a_scb_start_true_lbl = None
        self.a_scb_end_lbl = None
        self.a_scb_end_true_lbl = None
        self.a_more_x_btn = None
        self.a_less_x_btn = None
        self.a_more_y_btn = None
        self.a_less_y_btn = None
        self.a_bar_chart_cnvs = None

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
        self.a_arround_cursor = None
        self.a_zoom_work_img = None
        self.a_render_zoom = None

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
        self.__mv_entry_black_focus_out()
        if self.a_work_img:
            # print( "i_pos_x= " + str( event.x) + "   i_pos_y= " + str( event.y))
            i_pos_x = max( event.x, 0)
            i_pos_x = min( event.x, constant.PICTURE_WIDTH - 1)
            i_pos_y = max( event.y, 0)
            i_pos_y = min( event.y, constant.PICTURE_HEIGHT - 1)

            i_offset = self.a_work_img.getpixel( ( i_pos_x, i_pos_y))

            # TODO : CHECK THIS CODE
            # Define r, g, b for the rgb colour space and fetch the RGB colour for each pixel
            # r, g, b = self.a_work_img.getpixel( ( i_pos_x, i_pos_y))

            # Use only the pair values, click is done in the picture zoom x 2
            if i_pos_y & 1:
                i_pos_y -= 1
            if i_pos_x & 1:
                i_pos_x -= 1

            self.a_mouse_pos_x_input_var.set( str( i_pos_x))
            self.a_mouse_pos_y_input_var.set( str( i_pos_y))
            self.a_pos_x_true_lbl.configure( text=str( int( ( i_pos_x & 1022) / 2)))
            self.a_pos_y_true_lbl.configure( text=str( int( ( i_pos_y & 1022) / 2)))

            self.a_color_lbl.configure( text=str( i_offset))
            self.a_scb_lbl.configure( text=str( int( i_offset / 16)))
            self.a_line_slider.set( int( i_offset / 16))

            # Select the radio button color in the palette
            self.a_palette_button_lst[i_offset].select()
            # print( "mw_click_on_picture() i_offset = ", str( i_offset))
            self.__mw_color_button( i_offset)

            # Draw bar chart for couleur in usage in a line
            self.a_bar_chart_cnvs.delete( "all")
            a_usage_color_rry = array.array( 'i')
            a_usage_color_rry = [1] * 16
            a_result_color_rry = array.array( 'i')
            a_result_color_rry = [0] * 16
            i_palette_number = int( i_offset / 16) * 16

            for i_loop in range( 0, constant.PICTURE_WIDTH, 2):
                i_offset = self.a_work_img.getpixel( ( i_loop, i_pos_y))
                i_offset = i_offset - (int( i_offset / 16) * 16)
                a_usage_color_rry[i_offset] +=1

            for i_loop in range( 0, 16, 1):
                if a_usage_color_rry[i_loop] == 1:
                    a_usage_color_rry[i_loop] = 0
                else:
                    if a_usage_color_rry[i_loop] < 4:
                        a_result_color_rry[i_loop] = int( (((a_usage_color_rry[i_loop] + 3) * 84) / 320) + 0.5)
                    else:
                        a_result_color_rry[i_loop] = int( ((a_usage_color_rry[i_loop] * 84) / 320) + 0.5)

            i_colmun_x = 0
            for i_loop in range( 0, 16, 1):
                i_hauteur = a_result_color_rry[i_loop]
                if a_result_color_rry[i_loop] > 0:
                    self.a_bar_chart_cnvs.create_rectangle( (i_colmun_x, 84-i_hauteur, i_colmun_x+20, 84), fill=self.a_palette_button_lst[i_palette_number+i_loop].cget( 'bg'), outline='white')
                    if a_usage_color_rry[i_loop] > 0 and a_usage_color_rry[i_loop] < 10:
                        self.a_bar_chart_cnvs.create_text( i_colmun_x+8, 84-64, text=str( a_usage_color_rry[i_loop]), fill="black")
                i_colmun_x += 24

            # Display zoom of a part of the picture
            i_contour = 26
            i_top_x = i_pos_x-i_contour
            if i_pos_x < i_contour:
                i_top_x = 0
            i_top_y = i_pos_y-i_contour
            if i_pos_y < i_contour:
                i_top_y = 0

            i_box_top = (i_top_x, i_top_y, i_pos_x+i_contour, i_pos_y+i_contour)
            a_zoom_work_tmp = self.a_work_img.crop( i_box_top)
            width, height = a_zoom_work_tmp.size
            self.a_zoom_work_img = a_zoom_work_tmp.resize( (width*4, height*4))     # Total of zoom is x 8
            self.a_render_zoom = ImageTk.PhotoImage( self.a_zoom_work_img)
            self.a_zoom_lbl.config( image=self.a_render_zoom)
            self.a_zoom_lbl.photo = self.a_render_zoom
            self.w_main_windows.update()
            print()

    # ####################### __mw_less_x_value_clicked ########################
    def __mw_less_x_value_clicked( self):
        """ Decrease value of X clicked """
        if self.a_work_img:
            i_current_val = int( self.a_mouse_pos_x_input_var.get())
            i_current_val = max( i_current_val-2, 0)
            self.a_mouse_pos_x_input_var.set( str( i_current_val))
            self.a_pos_x_true_lbl.configure( text=str( int( i_current_val / 2)))
            # goto self.__mw_click_on_picture()
            self.a_picture_lbl.event_generate("<1>", x=i_current_val, y=self.a_mouse_pos_y_input_var.get())

    # ####################### __mw_more_x_value_clicked ########################
    def __mw_more_x_value_clicked( self):
        """ Increase value of X clicked """
        if self.a_work_img:
            i_current_val = int( self.a_mouse_pos_x_input_var.get())
            i_current_val = min( i_current_val+2, constant.PICTURE_WIDTH)
            self.a_mouse_pos_x_input_var.set( str( i_current_val))
            self.a_pos_x_true_lbl.configure( text=str( int( i_current_val / 2)))
            # goto self.__mw_click_on_picture()
            self.a_picture_lbl.event_generate("<1>", x=i_current_val, y=self.a_mouse_pos_y_input_var.get())

    # ####################### __mw_less_y_value_clicked ########################
    def __mw_less_y_value_clicked( self):
        """ Decrease value of Y clicked """
        if self.a_work_img:
            i_current_val = int( self.a_mouse_pos_y_input_var.get())
            i_current_val = max( i_current_val-2, 0)
            self.a_mouse_pos_y_input_var.set( str( i_current_val))
            self.a_pos_y_true_lbl.configure( text=str( int( i_current_val / 2)))
            # goto self.__mw_click_on_picture()
            self.a_picture_lbl.event_generate("<1>", x=self.a_mouse_pos_x_input_var.get(), y=i_current_val)

    # ####################### __mw_more_y_value_clicked ########################
    def __mw_more_y_value_clicked( self):
        """ Increase value of Y clicked """
        if self.a_work_img:
            i_current_val = int( self.a_mouse_pos_y_input_var.get())
            i_current_val = min( i_current_val+2, constant.PICTURE_HEIGHT)
            self.a_mouse_pos_y_input_var.set( str( i_current_val))
            self.a_pos_y_true_lbl.configure( text=str( int( i_current_val / 2)))
            # goto self.__mw_click_on_picture()
            self.a_picture_lbl.event_generate("<1>", x=self.a_mouse_pos_x_input_var.get(), y=i_current_val)

    # ####################### __mv_entry_mouse_x_focus_in ########################
    def __mv_entry_mouse_x_focus_in( self, _):
        """ entry mouse pos X take the focus """
        self.w_main_windows.unbind( "<Key>")
        print( "mv_entry_mouse_x_focus_in()")

    # ####################### __mv_entry_mouse_y_focus_in ########################
    def __mv_entry_mouse_y_focus_in( self, _):
        """ entry mouse pos Y take the focus """
        self.w_main_windows.unbind( "<Key>")
        print( "mv_entry_mouse_y_focus_in()")

    # ####################### __mv_entry_mouse_x_y_focus_out ########################
    def __mv_entry_mouse_x_y_focus_out( self, _):
        """ entry mouse pos X or Y loose the focus """
        self.w_main_windows.bind( "<Key>" , self.__on_single_key)
        print( "mv_entry_mouse_x_y_focus_out()")

    # ####################### __mw_set_max_len_to_four_chars_and_filter ########################
    def __mw_set_max_len_to_four_chars_and_filter( self, i_action, s_string_apres, s_insert):
        """ Validates each character as it is entered in the entry for a color value
            parameter setup is '%d', '%s', '%S'
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
        print( " i_action       %d = ", str( i_action))
        # print( "i_position     %i = ", str( i_position))
        # print( "s_string_avant %P = ", s_string_avant)
        print( " s_string_apres %s = ", s_string_apres)
        print( " s_insert       %S = ", s_insert)
        # print( "a_name         %W = ", s_name)

        if 'a' <= s_insert <= 'f':
        # if s_insert >= 'a' and s_insert <= 'f':
            s_insert.upper()

        if s_insert in '0123456789ABCDEF':
        # if (s_insert != '') or (s_insert >= 'A' and s_insert <= 'F') or ( s_insert >= '0' and s_insert <= '9'):
            # print( 'mw_set_max_len_to_four_chars_and_filter() : __s_value len = ' + str( len( __s_value) + 1) )
            if int( i_action) == 0:     # deletion
                # print( 'mw_set_max_len_to_four_chars_and_filter() : action = deletion' )
                if len( s_string_apres) + 1 > 8:
                    b_result = True
                else:
                    # self.w_main_windows.bell()
                    b_result = False
            elif int( i_action) == 1:   # insertion
                # print( 'mw_set_max_len_to_four_chars_and_filter() : action = insertion' )
                if len( s_string_apres) + 1 > 15:
                    # self.w_main_windows.bell()
                    b_result = False
                else:
                    b_result = True
            else:
                # print( 'mw_set_max_len_to_four_chars_and_filter() : autre')
                b_result = True
        else:
            # print( 'mw_set_max_len_to_four_chars_and_filter() : character not managed')
            # self.w_main_windows.bell()
            b_result = False

        return b_result

    # ####################### __mw_change_scb_line ########################
    def __mw_change_scb_line( self):
        """ Change the line palette """
        if self.a_original_img:
            i_line_number = int( self.a_pos_y_true_lbl.cget( "text"))
            i_current_palette_number = int( self.a_scb_lbl.cget( "text"))
            i_new_palette_number = int( self.a_line_slider.get())
            if i_current_palette_number != i_new_palette_number:
                # print( " Convert the index." )
                if i_current_palette_number > i_new_palette_number:
                    i_delta = (i_new_palette_number - i_current_palette_number) * 16
                else:
                    i_delta = abs( (i_current_palette_number - i_new_palette_number) * 16)

                for i_index in range( 0, 319, 1):
                    i_current_index = self.a_original_img.getpixel( ( i_index, i_line_number))
                    i_current_index += i_delta
                    self.a_original_img.putpixel( ( i_index, i_line_number), i_current_index)

                # width, height = self.a_original_img.size
                # print( "width = " + str( width) + "  height = " + str( height) )
                # self.a_work_img.save( self.s_filename, 'BMP')
                # self.a_work_img = Image.open( self.s_filename)
                s_filename = self.s_init_pathname + mt_get_path_separator( self.s_platform) + self.a_filename_lbl.cget( "text")
                self.mw_update_main_window( s_filename , self.a_original_img)
                self.mw_click_in_picture_center( int( self.a_mouse_pos_x_input_var.get()), int( self.a_mouse_pos_y_input_var.get()))

    # ####################### __mw_picture_zone ########################
    def __mw_picture_zone( self, a_pic_frame):
        """ Frame with the picture to left, and details to right """
        i_index_base_block = 0
        a_pic_sep_h0 = Separator( a_pic_frame, orient='horizontal')
        a_pic_sep_h0.grid(row=i_index_base_block, column=0, columnspan=1, sticky='ew')
        a_pic_sep_lbl_h0 = Label( a_pic_frame, text="Picture", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h0.grid( row=i_index_base_block, column=0, padx=15)

        a_pic_sep_h0 = Separator( a_pic_frame, orient='horizontal')
        a_pic_sep_h0.grid( row=i_index_base_block, column=1, columnspan=9, sticky='ew')
        a_pic_sep_lbl_h0 = Label( a_pic_frame, text="Details", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h0.grid( row=i_index_base_block, column=1, columnspan=9, padx=170, sticky='ew')

        i_index_base_block += 1
        self.a_picture_lbl = Label( a_pic_frame, padx=0, pady=0, image=None, width=constant.PICTURE_WIDTH, height=constant.PICTURE_HEIGHT, background=constant.BACKGROUD_COLOR_UI, cursor='circle', borderwidth=0, compound="center", highlightthickness=0)
        self.a_picture_lbl.grid( row=i_index_base_block, column=0)
        self.a_picture_lbl.bind( '<Button>', self.__mw_click_on_picture)
        self.a_picture_lbl.bind( '<Motion>', self.__mw_print_widget_under_mouse)

        # Create SCB frame to draw rectangle to present SCB
        a_scb_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_scb_frame.place( x=644, y=21, width=20, height=constant.PICTURE_HEIGHT)

        self.a_scb_cnvs = Canvas( a_scb_frame, width=20, height=constant.PICTURE_HEIGHT, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
        self.a_scb_cnvs.grid( row=0, column=0, sticky='ewns')

        # Create details frame
        a_details_pic_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background=constant.BACKGROUD_COLOR_UI or'darkgray' or 'light grey'
        a_details_pic_frame.place( x=664, y=30, width=self.i_main_window_width - 664, height=constant.PICTURE_HEIGHT)

        a_bar_chart_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_bar_chart_frame.place( x=664, y=30+(constant.PICTURE_HEIGHT-104), width=self.i_main_window_width - 442, height=104)

        i_index_base_block = 0
        self.a_bar_chart_cnvs = Canvas( a_bar_chart_frame, width=self.i_main_window_width - (438+40), height=84, background=constant.BACKGROUD_COLOR_UI, highlightthickness=0)
        self.a_bar_chart_cnvs.grid( row=i_index_base_block, column=0, padx=4, sticky='ewns')
        i_index_base_block += 1
        i_index_base_column = 0
        a_font_label = font.Font( size=6)

        a_bar_chart_comment_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_bar_chart_comment_frame.place( x=667, y=30+(constant.PICTURE_HEIGHT-20), width=self.i_main_window_width - 438, height=15)
        for i_loop in range( 0, 16, 1):
            a_label = Label(a_bar_chart_comment_frame, text=str( i_loop), width=2, justify='left', background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            a_label.grid( row=1, column=i_index_base_column, padx=4, pady=0, sticky='w')
            i_index_base_column += 1

        i_index_base_block = 0
        a_pic_sep_lbl_h2 = Label( a_details_pic_frame, text="File name", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h2.grid( row=i_index_base_block, column=1, columnspan=7, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        self.a_filename_lbl = Label( a_details_pic_frame, text="   ", background='light grey', foreground='black')
        self.a_filename_lbl.grid( row=i_index_base_block, column=1, columnspan=7, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_space_lbl_h1 = Label( a_details_pic_frame, text="", background=constant.BACKGROUD_COLOR_UI)
        a_space_lbl_h1.grid( row=i_index_base_block, column=1, columnspan=7, padx=4, pady=1)

        i_index_base_block += 1
        a_pic_sep_lbl_h3 = Label( a_details_pic_frame, text="Mouse live position", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h3.grid( row=i_index_base_block, column=1, columnspan=4, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="X ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4, pady=1, sticky='ew')
        self.a_mouse_live_pos_x = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH-1, background='light grey', foreground='black')
        self.a_mouse_live_pos_x.grid( row=i_index_base_block, column=2, padx=4, pady=1, sticky='ew')
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="Y ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')
        self.a_mouse_live_pos_y = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH-1, background='light grey', foreground='black')
        self.a_mouse_live_pos_y.grid( row=i_index_base_block, column=4, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h3 = Label( a_details_pic_frame, text="Mouse click position", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h3.grid( row=i_index_base_block, column=1, columnspan=5, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="X ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4, pady=1)
        # font='-weight bold'
        self.a_mouse_pos_x = Entry( a_details_pic_frame, textvariable=self.a_mouse_pos_x_input_var, width=constant.DEFAULT_BUTTON_WIDTH, validatecommand=( a_pic_frame.register( self.__mw_set_max_len_to_four_chars_and_filter), '%d', '%s', '%S'), background='white', foreground='black')
        self.a_mouse_pos_x.grid( row=i_index_base_block, column=2, padx=4, pady=1)
        self.a_mouse_pos_x.bind( "<FocusIn>", self.__mv_entry_mouse_x_focus_in)
        self.a_mouse_pos_x.bind( "<FocusOut>", self.__mv_entry_mouse_x_y_focus_out)

        self.a_pos_x_true_lbl = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH-1, background='light grey', foreground='black')
        self.a_pos_x_true_lbl.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')

        if self.s_platform == "Darwin":
            self.a_less_y_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_up_arrow_photo(), command=self.__mw_less_y_value_clicked, width=44, height=20, relief='raised', highlightbackground='light grey', repeatdelay=500, repeatinterval=100)
        else:
            self.a_less_y_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_up_arrow_photo(), command=self.__mw_less_y_value_clicked, width=44, height=20, relief='raised', background=constant.BACKGROUD_COLOR_UI, repeatdelay=500, repeatinterval=100)
        self.a_less_y_btn.grid( row=i_index_base_block, column=6, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        if self.s_platform == "Darwin":
            self.a_less_x_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_left_arrow_photo(), command=self.__mw_less_x_value_clicked, width=44, height=20, relief='raised', highlightbackground='light grey', repeatdelay=500, repeatinterval=100)
        else:
            self.a_less_x_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_left_arrow_photo(), command=self.__mw_less_x_value_clicked, width=44, height=20, relief='raised', background=constant.BACKGROUD_COLOR_UI, repeatdelay=500, repeatinterval=100)
        self.a_less_x_btn.grid( row=i_index_base_block, column=5, padx=4, pady=1, sticky='ew')

        if self.s_platform == "Darwin":
            self.a_more_x_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_right_arrow_photo(), command=self.__mw_more_x_value_clicked, width=44, height=20, relief='raised', highlightbackground='light grey', repeatdelay=500, repeatinterval=100)
        else:
            self.a_more_x_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_right_arrow_photo(), command=self.__mw_more_x_value_clicked, width=44, height=20, relief='raised', background=constant.BACKGROUD_COLOR_UI, repeatdelay=500, repeatinterval=100)
        self.a_more_x_btn.grid( row=i_index_base_block, column=7, padx=4, pady=1, sticky='ew')

        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="Y ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4, pady=1)
        self.a_mouse_pos_y = Entry( a_details_pic_frame, textvariable=self.a_mouse_pos_y_input_var, width=constant.DEFAULT_BUTTON_WIDTH, validatecommand=( a_pic_frame.register( self.__mw_set_max_len_to_four_chars_and_filter), '%d', '%s', '%S'), background='white', foreground='black')
        self.a_mouse_pos_y.grid( row=i_index_base_block, column=2, padx=4, pady=1)
        self.a_mouse_pos_y.bind( "<FocusIn>", self.__mv_entry_mouse_y_focus_in)
        self.a_mouse_pos_y.bind( "<FocusOut>", self.__mv_entry_mouse_x_y_focus_out)

        self.a_pos_y_true_lbl = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH-1, background='light grey', foreground='black')
        self.a_pos_y_true_lbl.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h5 = Label( a_details_pic_frame, text="Color offset", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h5.grid( row=i_index_base_block, column=1, columnspan=2, padx=4, pady=1, sticky='ew')
        self.a_color_lbl = Label( a_details_pic_frame, text="   ", background='light grey', foreground='black')
        self.a_color_lbl.grid( row=i_index_base_block, column=3, columnspan=1, padx=4, pady=1, sticky='ew')

        if self.s_platform == "Darwin":
            self.a_more_y_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_down_arrow_photo(), command=self.__mw_more_y_value_clicked, width=44, height=20, relief='raised', highlightbackground='light grey', repeatdelay=500, repeatinterval=100)
        else:
            self.a_more_y_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_down_arrow_photo(), command=self.__mw_more_y_value_clicked, width=44, height=20, relief='raised', background=constant.BACKGROUD_COLOR_UI, repeatdelay=500, repeatinterval=100)
        self.a_more_y_btn.grid( row=i_index_base_block, column=6, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h6 = Label( a_details_pic_frame, text="Palette line", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h6.grid( row=i_index_base_block, column=1, columnspan=2, padx=4, pady=1, sticky='ew')
        self.a_scb_lbl = Label( a_details_pic_frame, text="   ", background='light grey', foreground='black')
        self.a_scb_lbl.grid( row=i_index_base_block, column=3, columnspan=1, padx=4, pady=1, sticky='ew')
        self.a_line_slider = Scale( a_details_pic_frame, from_=0, to=15, orient='horizontal', background=constant.BACKGROUD_COLOR_UI, highlightbackground='light grey', borderwidth=0, highlightthickness=0)
        self.a_line_slider.grid( row=i_index_base_block, rowspan=2, column=4, columnspan=6, padx=4, pady=2, sticky='ewns')

        i_index_base_block += 1
        if self.s_platform == "Darwin":
            a_change_scb_btn = Button( a_details_pic_frame, text='Change palette line number', command=self.__mw_change_scb_line, width=21, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            a_change_scb_btn.grid( row=i_index_base_block, column=1, columnspan=3, padx=2, pady=0, sticky='ew')
        else:
            a_change_scb_btn = Button( a_details_pic_frame, text='Change palette line number', command=self.__mw_change_scb_line, width=21, height=1, relief='raised', background=constant.BACKGROUD_COLOR_UI)
            a_change_scb_btn.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1, sticky='ew')

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
        i_number = int( self.a_btn_offset_lbl.cget( "text"))
        # print( "mw_restore_old_color() i_offset = ", str( i_number))
        self.__mw_color_button( i_number)

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
    def __mv_entry_red_focus_in( self, _):
        """ Select of red entry widget focus events prepare scale to move """
        self.a_color_slider.config( foreground='red')
        self.a_color_slider.set( int(self.a_red_ntr.get(), 16) )
        self.a_color_slider.config( command=self.__mv_update_red_entry )

    # ####################### __mv_entry_green_focus_in ########################
    def __mv_entry_green_focus_in( self, _):
        """ Select of green entry widget focus events prepare scale to move """
        self.a_color_slider.config( foreground='green')
        self.a_color_slider.set( int(self.a_green_ntr.get(), 16) )
        self.a_color_slider.config( command=self.__mv_update_green_entry )

    # ####################### __mv_entry_blue_focus_in ########################
    def __mv_entry_blue_focus_in( self, _):
        """ Select of blue entry widget focus events prepare scale to move """
        self.a_color_slider.config( foreground='blue')
        self.a_color_slider.set( int(self.a_blue_ntr.get(), 16) )
        self.a_color_slider.config( command=self.__mv_update_blue_entry )

    # ####################### __mv_entry_red_focus_out ########################
    def __mv_entry_black_focus_out( self):
        """ No selected entry widget focus events restore color to black """
        self.a_color_slider.config( foreground='black')

    # ####################### __mw_palette_zone ########################
    def __mw_palette_zone( self, a_bottom_frame):
        """ Frame with the palette button to left, and details to right """

        i_index_base_block = 0
        a_palette_sep_h1 = Separator( a_bottom_frame, orient='horizontal')
        a_palette_sep_h1.grid( row=i_index_base_block, column=0, columnspan=8, sticky='ew')
        a_palette_sep_lbl_h1 = Label( a_bottom_frame, text="Palette", background=constant.BACKGROUD_COLOR_UI)
        a_palette_sep_lbl_h1.grid( row=i_index_base_block, column=0, columnspan=2, padx=260)
        a_palette_sep_h1 = Separator( a_bottom_frame, orient='horizontal')
        a_palette_sep_h1.grid( row=i_index_base_block, column=9, columnspan=4, sticky='ew')
        a_palette_sep_lbl_h1 = Label( a_bottom_frame, text="Color", background=constant.BACKGROUD_COLOR_UI)
        a_palette_sep_lbl_h1.grid( row=i_index_base_block, column=9, columnspan=4, padx=120)
        a_palette_sep_h1 = Separator( a_bottom_frame, orient='horizontal')
        a_palette_sep_h1.grid( row=i_index_base_block, column=13, columnspan=4, sticky='ew')
        a_palette_sep_lbl_h1 = Label( a_bottom_frame, text="Zoom", background=constant.BACKGROUD_COLOR_UI)
        a_palette_sep_lbl_h1.grid( row=i_index_base_block, column=13, columnspan=4, padx=90)

        # Create palette button left frame
        a_palette_bottom_frame = tk_gui.Frame( a_bottom_frame, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        if self.s_platform == "Darwin":
            a_palette_bottom_frame.place( x=2, y=20, width=590, height=276 )
        else:
            a_palette_bottom_frame.place( x=2, y=20, width=570, height=276 )

        # Creating a font object with little size for color buttons to reduce their size
        a_font_label = font.Font( size=6)
        a_font_button = font.Font( size=3)

        # Create a line of number for the column
        i_index_base_column = 1
        for i_loop in range( 0, 16, 1):
            a_label = Label( a_palette_bottom_frame, text=str( i_loop), background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            self.a_palette_number_lst.append( a_label)
            i_index_base_column += 1

        # Table of color button for the palette
        i_index_base_block += 1
        i_index_base_column = 0
        i_to = 0
        i_index = 0
        for i_loop in range( 0, 16, 1):
            i_from = i_to
            i_to = i_to + 48
            # First element of the line is its number
            a_label = Label( a_palette_bottom_frame, text=str(i_loop), background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            if self.s_platform == "Darwin":
                a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            else:
                a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            i_index_base_column += 1
            # create list of line of radio button and add it in a list to be accessible
            for _ in range( i_from, i_to, 3):
                a_button_color = Radiobutton( a_palette_bottom_frame, text='', indicatoron = 0, width=8, height=1, variable=self.color_radio_button, value=i_index, background=constant.LIGHT_COLOR_UI, font=a_font_button)
                if self.s_platform == "Darwin":
                    a_button_color.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=2)
                else:
                    a_button_color.grid( row=i_index_base_block, column=i_index_base_column, padx=4, pady=2)
                self.a_palette_button_lst.append( a_button_color)
                i_index_base_column += 1
                i_index += 1

            i_index_base_column = 0
            i_index_base_block += 1

        self.w_main_windows.update()

        # Create color button right frame
        a_color_bottom_frame = tk_gui.Frame( a_bottom_frame, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        if self.s_platform == "Darwin":
            a_color_bottom_frame.place( x=592, y=20, width=self.i_main_window_width - 592, height=276 )
        else:
            a_color_bottom_frame.place( x=572, y=20, width=self.i_main_window_width - 572, height=276 )

        i_index_base_block = 0
        a_color_name_lbl = Label( a_color_bottom_frame, text="Red", background=constant.BACKGROUD_COLOR_UI, foreground='red')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1)
        a_color_name_lbl = Label( a_color_bottom_frame, text="RGB Color", background=constant.BACKGROUD_COLOR_UI)
        a_color_name_lbl.grid( row=i_index_base_block, column=2, columnspan=2, padx=4, pady=1)

        self.a_zoom_lbl = Label( a_color_bottom_frame, image=None, text="   _     _", background=constant.BACKGROUD_COLOR_UI, cursor='circle', borderwidth=2, compound="center", highlightthickness=2)
        self.a_zoom_lbl.grid( row=i_index_base_block, rowspan=10, column=4, columnspan=4, padx=4, pady=1, sticky='ewns')

        i_index_base_block += 1
        self.a_red_ntr = Entry( a_color_bottom_frame, textvariable=self.a_red_input_var, validate="key", validatecommand=( a_color_bottom_frame.register( self.__mw_set_max_len_to_fifteen_chars_and_filter), '%d', '%s', '%S'), width=constant.DEFAULT_BUTTON_WIDTH, background=constant.LIGHT_COLOR_UI, foreground='red')
        self.a_red_ntr.grid( row=i_index_base_block, column=0, columnspan=1, padx=4, sticky='w')
        self.a_red_ntr.bind( "<FocusIn>", self.__mv_entry_red_focus_in)
        self.a_red_ntr_dec_lbl = Label( a_color_bottom_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH - 1, background='light grey', foreground='red')
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
        if self.s_platform == "Darwin":
            self.a_color_old_btn = Button( a_color_bottom_frame, text='', command=self.__mw_restore_old_color, width=5, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            self.a_color_old_btn.grid( row=i_index_base_block, rowspan=4, column=3, columnspan=1, padx=2, pady=0, sticky='ewns')
        else:
            self.a_color_old_btn = Button( a_color_bottom_frame, text='', command=self.__mw_restore_old_color, width=7, height=1, relief='raised', background='light grey')
            self.a_color_old_btn.grid( row=i_index_base_block, rowspan=4, column=3, columnspan=1, padx=4, pady=1, sticky='ewns')
        i_index_base_block += 1
        self.a_green_ntr = Entry( a_color_bottom_frame, textvariable=self.a_green_input_var, validate="key", validatecommand=( a_color_bottom_frame.register( self.__mw_set_max_len_to_fifteen_chars_and_filter), '%d', '%s', '%S'), width=constant.DEFAULT_BUTTON_WIDTH, background=constant.LIGHT_COLOR_UI, foreground='green')
        self.a_green_ntr.grid( row=i_index_base_block, column=0, padx=4, sticky='w')
        self.a_green_ntr.bind( "<FocusIn>", self.__mv_entry_green_focus_in)
        self.a_green_ntr_dec_lbl = Label( a_color_bottom_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH - 1, background='light grey', foreground='green')
        self.a_green_ntr_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=4, sticky='ew')
        i_index_base_block += 1
        a_color_name_lbl = Label( a_color_bottom_frame, text="Blue", background=constant.BACKGROUD_COLOR_UI, foreground='blue')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=1)
        i_index_base_block += 1
        self.a_blue_ntr = Entry( a_color_bottom_frame, textvariable=self.a_blue_input_var, validate="key", validatecommand=( a_color_bottom_frame.register( self.__mw_set_max_len_to_fifteen_chars_and_filter), '%d', '%s', '%S'), width=constant.DEFAULT_BUTTON_WIDTH, background=constant.LIGHT_COLOR_UI, foreground='blue')
        self.a_blue_ntr.grid( row=i_index_base_block, column=0, padx=4, sticky='w')
        self.a_blue_ntr.bind( "<FocusIn>", self.__mv_entry_blue_focus_in)
        self.a_blue_ntr_dec_lbl = Label( a_color_bottom_frame, text="", width=constant.DEFAULT_BUTTON_WIDTH - 1, background='light grey', foreground='blue')
        self.a_blue_ntr_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=4, sticky='ew')

        i_index_base_block += 1
        # , borderwidth=0, compound="center", highlightthickness=0
        self.a_color_slider = Scale( a_color_bottom_frame, from_=0, to=255, orient='horizontal', background=constant.BACKGROUD_COLOR_UI, highlightbackground='light grey', borderwidth=0, highlightthickness=0)
        self.a_color_slider.grid( row=i_index_base_block, column=0, columnspan=4, padx=4, pady=4, sticky='ew')

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
        if self.s_platform == "Darwin":
            a_change_color_btn = Button( a_color_bottom_frame, text='Set color', command=self.__mw_set_color_in_palette, width=14, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            a_change_color_btn.grid( row=i_index_base_block, column=0, columnspan=2, padx=2, pady=0, sticky='ew')
            a_pen_color_btn = Button( a_color_bottom_frame, text='Pen color', command=self.__mw_set_pen_color, width=14, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            a_pen_color_btn.grid( row=i_index_base_block, column=2, columnspan=2, padx=2, pady=0, sticky='ew')
        else:
            a_change_color_btn = Button( a_color_bottom_frame, text='Set color', command=self.__mw_set_color_in_palette, width=14, height=1, relief='raised', background=constant.BACKGROUD_COLOR_UI)
            a_change_color_btn.grid( row=i_index_base_block, column=0, columnspan=2, padx=4, pady=6, sticky='ew')
            a_pen_color_btn = Button( a_color_bottom_frame, text='Pen color', command=self.__mw_set_pen_color, width=14, height=1, relief='raised', background=constant.BACKGROUD_COLOR_UI)
            a_pen_color_btn.grid( row=i_index_base_block, column=2, columnspan=2, padx=4, pady=6, sticky='ew')

        # self.w_main_windows.update()
        # i_col, i_row = self.a_red_ntr_dec_lbl.grid_size()
        # print( f'GRID : col= {i_col} row= {i_row}')
        # i_width = self.a_red_ntr_dec_lbl.winfo_width()
        # print( f'a_red_ntr_dec_lbl : width= {i_width}')

    # ####################### __mw_set_max_len_to_fifteen_chars_and_filter ########################
    def __mw_set_max_len_to_fifteen_chars_and_filter( self, i_action, s_string_apres, s_insert):
        """ Validates each character as it is entered in the entry for a color value
            parameter setup is '%d', '%s', '%S'
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
        print( "i_action       %d = ", str( i_action))
        # print( "i_position     %i = ", str( i_position))
        # print( "s_string_avant %P = ", s_string_avant)
        print( "s_string_apres %s = ", s_string_apres)
        print( "s_insert       %S = ", s_insert)
        # print( "a_name         %W = ", s_name)

        if s_insert != '':
            if 'a' <= s_insert <= 'f':
            # if s_insert >= 'a' and s_insert <= 'f':
                s_insert.upper()

            if 'A' <= s_insert <= 'F' or '0' <= s_insert <= '9':
            # if (s_insert >= 'A' and s_insert <= 'F') or ( s_insert >= '0' and s_insert <= '9'):
                # print( 'mw_set_max_len_to_fifteen_chars_and_filter() : __s_value len = ' + str( len( __s_value) + 1) )
                if int( i_action) == 0:     # deletion
                    # print( 'mw_set_max_len_to_fifteen_chars_and_filter() : action = deletion' )
                    if len( s_string_apres) + 1 > 8:
                        b_result = True
                    else:
                        # self.w_main_windows.bell()
                        b_result = False
                elif int( i_action) == 1:   # insertion
                    # print( 'mw_set_max_len_to_fifteen_chars_and_filter() : action = insertion' )
                    if len( s_string_apres) + 1 > 15:
                        # self.w_main_windows.bell()
                        b_result = False
                    else:
                        b_result = True
                else:
                    # print( 'mw_set_max_len_to_fifteen_chars_and_filter() : autre' )
                    b_result = True
            else:
                print( 'mw_set_max_len_to_fifteen_chars_and_filter() : key= ' + s_insert)
                # self.w_main_windows.bell()
                b_result = False
        else:
            b_result = False

        return b_result

    # ####################### __on_single_key ########################
    def __on_single_key( self, event):
        """ Method manage arrow key press for the main windows """
        if event.keysym == "Left":
            self.a_less_x_btn.invoke()
        elif event.keysym == "Right":
            self.a_more_x_btn.invoke()
        elif event.keysym == "Up":
            self.a_less_y_btn.invoke()
        elif event.keysym == "Down":
            self.a_more_y_btn.invoke()
        else:
            s_key = event.char
            print( 'on_single_key() : key= ' + s_key )

    # ####################### __mw_color_button ########################
    def __mw_color_button( self, i_number):
        """ Palette of color buttons. i_number is a value form 0 to 255 one of the palette radio button """
        # self.w_main_windows.bell()
        self.__mv_entry_black_focus_out()
        # print( "mw_color_button() i_number = ", str( i_number))
        a_palette_list = self.a_original_img.getpalette()
        i_tmp_number = i_number * 3
        i_red = a_palette_list[i_tmp_number]
        i_green = a_palette_list[i_tmp_number + 1]
        i_blue = a_palette_list[i_tmp_number + 2]
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
            self.a_btn_x_lbl.configure( text=str( __i_complete))    # label under Palette Y
        else:
            self.a_btn_x_lbl.configure( text="0")                   # label under Palette Y

        self.a_btn_y_lbl.configure( text=str( __i_rest))            # label under Offset X

        # Draw the SCB rectangle
        self.mw_draw_scb_bar( i_number)

    # ####################### __mw_set_color_in_palette ########################
    def __mw_set_color_in_palette( self):
        """ Set a new color value in palette  """
        s_red = self.a_red_input_var.get()
        s_green = self.a_green_input_var.get()
        s_blue = self.a_blue_input_var.get()
        i_index = int(self.a_btn_offset_lbl.cget( "text"))
        i_original_index = int( i_index/3)
        a_palette_button = self.a_palette_button_lst[i_original_index]
        # ready when color modification will be done
        a_palette_button.configure( background= "#" + s_red + s_green + s_blue)
        # Update the picture palette
        a_palette_list = self.a_original_img.getpalette()
        a_palette_list[ i_index] = int( self.a_red_ntr_dec_lbl.cget( "text"))
        a_palette_list[ i_index+1] = int( self.a_green_ntr_dec_lbl.cget( "text"))
        a_palette_list[ i_index+2] = int( self.a_blue_ntr_dec_lbl.cget( "text"))
        self.a_original_img.putpalette( a_palette_list, rawmode='RGB')
        self.mw_update_main_window( self.c_mains_icon_bar.mwib_get_get_path_filename(), self.a_original_img)
        self.__mw_color_button( i_index)

    # ####################### __mw_set_pen_color ########################
    def __mw_set_pen_color( self):
        """ Set a new color value in palette  """
        self.w_main_windows.bell()
        # s_red = self.a_red_input_var.get()
        # s_green = self.a_green_input_var.get()
        # s_blue = self.a_blue_input_var.get()
        # i_index = int(self.a_btn_offset_lbl.cget( "text"))
        # a_palette_button = self.a_palette_button_lst[i_index]
        # # ready when color modification will be done
        # a_palette_button.configure( background= "#" + s_red + s_green + s_blue)
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
    def __mw_print_widget_under_mouse( self, event):
        """ Show position of the mouse in the loaded picture """
        if self.a_work_img:
            self.__mv_entry_black_focus_out()
            i_pos_x = event.x
            i_pos_y = event.y
            # Use only the pair values, click is done in the picture zoomed x 2
            if i_pos_y & 1:
                i_pos_y -= 1
            if i_pos_x & 1:
                i_pos_x -= 1
            self.a_mouse_live_pos_x.configure( text=str( i_pos_x))
            self.a_mouse_live_pos_y.configure( text=str( i_pos_y))

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

        self.w_main_windows.title( self.a_list_application_info[0])

        # Create 1 line of action icons
        a_top_bar_frame = tk_gui.Frame( self.w_main_windows, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)    # background='darkgray'
        a_top_bar_frame.place( x=2, y=0, width=self.i_main_window_width-4, height=98 )   # fill :  must be 'none', 'x', 'y', or 'both'
        self.c_mains_icon_bar = MyMainWindowIconsBar( self, self.w_main_windows, self.a_list_application_info, a_top_bar_frame)
        self.c_mains_icon_bar.mwib_create_top_bar_icons( 1)
        self.w_main_windows.update()
        # print( "a_top_bar_frame     : width= " + str( a_top_bar_frame.winfo_width()) + " height= ", str( a_top_bar_frame.winfo_height()))

        # Create picture frame
        a_pic_frame = tk_gui.Frame( self.w_main_windows, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_pic_frame.place( x=2, y=98, width=self.i_main_window_width-4, height=constant.PICTURE_HEIGHT+20+8)  # fill :  must be 'none', 'x', 'y', or 'both'
        self.__mw_picture_zone( a_pic_frame)
        self.w_main_windows.update()
        # print( "a_pic_frame         : width= " + str( a_pic_frame.winfo_width()) + " height= ", str( a_pic_frame.winfo_height()))

        # Create palette frame
        a_palette_frame = tk_gui.Frame( self.w_main_windows, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_palette_frame.place( x=2, y=98+constant.PICTURE_HEIGHT+22+8, width=self.i_main_window_width-4, height=self.i_main_window_height - ( a_top_bar_frame.winfo_height() + a_pic_frame.winfo_height()) )
        self.__mw_palette_zone( a_palette_frame)
        self.w_main_windows.update()
        # print( "a_palette_frame     : width= " + str( a_palette_frame.winfo_width()) + " height= ", str( a_palette_frame.winfo_height()))
        # print( "Calcul height       : " + str( self.i_main_window_height - ( a_top_bar_frame.winfo_height() + a_pic_frame.winfo_height())))

        self.w_main_windows.bind( '<Button>', self.__mw_change_focus)
        self.w_main_windows.bind( "<Key>" , self.__on_single_key)

        # disabled during debug
        # if self.s_platform == "Windows":
        #     self.__mw_clock_in_window_bar()
            # if self.a_work_img:
            #     self.__mw_print_widget_under_mouse( self.w_main_windows)


    # ####################### mw_draw_scb_bar ########################
    def mw_draw_scb_bar( self, i_color_offset):
        """ Draw the bar how display all the same SCB """
        # Draw the SCB rectangle
        i_palette_number = int( i_color_offset / 16) * 16
        # print( " offset= " + str( i_color_offset) + "  palette_number= " + str( i_palette_number))

        self.a_scb_cnvs.delete( "all")
        for i_loop in range( 0, constant.PICTURE_HEIGHT, 2):
            i_offset = self.a_work_img.getpixel( ( 0, i_loop))
            i_inter = int( i_offset / 16) * 16
            if i_inter == i_palette_number:
                self.a_scb_cnvs.create_rectangle( 0, i_loop, 20, i_loop+1, fill='blue', outline='blue')
            else:
                i_inter = 0

    # ####################### mw_update_main_window ########################
    def mw_update_main_window( self, s_filename, a_work_img):
        """ Load a picture and fill the interface """
        if s_filename and a_work_img:
            self.a_original_img = a_work_img.copy()
            self.a_work_img = a_work_img
            width, height = self.a_work_img.size
            self.a_work_img = self.a_work_img.resize( (width * 2, height * 2))

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
                    s_red = f'{a_palette_list[ i_index]:02X}'
                    s_green = f'{a_palette_list[ i_index + 1]:02X}'
                    s_blue = f'{a_palette_list[ i_index + 2]:02X}'
                    # Disabled for debug
                    # s_my_hex = s_my_hex + "#" + s_red + s_green + s_blue + " "

                    a_button_color = self.a_palette_button_lst[i_element]
                    # print( "mw_update_main_window() i_index = ", str( i_index))
                    config_palette_bottom_with_arg = partial( self.__mw_color_button, i_index)  #  str( int( i_index / 3))
                    a_button_color.configure( command=config_palette_bottom_with_arg)
                    a_button_color.configure( background="#" + s_red + s_green + s_blue)
                    i_element += 1

                    if i_index == 0:
                        # print( "mw_update_main_window() i_index = ", str( i_index))
                        self.__mw_color_button( i_index)

                self.w_main_windows.update()
                # Disabled for debug
                # print( s_my_hex)

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

    # ####################### mw_get_pathname ########################
    def mw_get_pathname( self):
        """ Return default pathname """
        return self.s_init_pathname

    # ####################### mw_set_pathname ########################
    def mw_set_pathname( self, s_new_pathname):
        """ Set last used pathname """
        self.s_init_pathname = s_new_pathname

    # ####################### mw_click_in_picture_center ########################
    def mw_click_in_picture_center( self, pos_x=320, pos_y=200):
        """ Click on the center of the picture only after loaded it """
        self.a_picture_lbl.event_generate("<1>", x=pos_x, y=pos_y)

    # ####################### mw_save_picture ########################
    def mw_save_picture( self):
        """ Save the picture """
        s_original_filename = self.a_filename_lbl.cget( "text")
        s_new_file_name = mt_save_file( self.w_main_windows, self, s_original_filename)
        if s_new_file_name:
            s_new_file_name.lower()
            if s_new_file_name[-4:] != ".bmp":
                s_new_file_name = s_new_file_name + ".bmp"
            self.a_original_img.save( s_new_file_name, 'BMP')
