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

""" Module de creation pour la fenetre principale de la partie image. """

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

from tkinter import font, Label, Button, Entry, Canvas, Scale, StringVar
from tkinter.ttk import Separator
from PIL import ImageTk

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_alert_window import MyAlertWindow
from .my_scb_window import MyScbPalletWindow
# from .my_main_window  import mv_entry_black_focus_out, mv_on_single_key, mw_print_widget_under_mouse
# from .my_main_window_pallet import mwp_entry_black_focus_out, mwp_select_color_rad_btn

# __name__ = "MyMainWindowImage"

# ###############################################################################################
# #######========================= constant private =========================

# ###############################################################################################
# #######=========================     GUI     =========================
# ####################### MyMainWindow ########################
class MyMainWindowImage:
    """ Create the main Windows Picture part of the application. """
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
        self.c_the_log = MyLogAnUsage( None)
        self.c_the_icons = MyIconPictures( self.w_tk_root)
        self.s_platform = platform.system()
        # Size of the main windows
        self.i_main_window_width = c_main_window.mw_get_main_window_width()
        self.i_main_window_height = c_main_window.mw_get_main_window_height()
        self.c_alert_windows = MyAlertWindow( c_main_window, c_main_window.mw_get_application_info())
        self.s_init_pathname = os.getcwd()
        self.c_main_icon_bar = None                # top icon menu bar : MyMainWindowIconsBar
        self.c_main_pallet = None                 # top icon menu bar : MyMainWindowPallet

        self.a_original_img = None
        self.a_work_img = None
        self.a_picture_lbl = None
        self.a_scb_cnvs = None
        self.a_scb_cnvs_rect_lst = []
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

        self.i_around_cursor = -1

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

    # ####################### __mwi_click_on_picture ########################
    def __mwi_click_on_picture( self, event):
        """ Show position of the mouse in the loaded picture and repair SCB to draw a rect """
        # print( "mw_click_on_picture()  ", event)
        self.c_main_pallet.mwp_entry_black_focus_out()
        if self.a_work_img:
            # print( "i_pos_x= " + str( event.x) + "   i_pos_y= " + str( event.y))
            i_pos_x = max( event.x, 0)
            i_pos_x = min( event.x, constant.PICTURE_WIDTH - 1)
            i_pos_y = max( event.y, 0)
            i_pos_y = min( event.y, constant.PICTURE_HEIGHT - 1)

            i_offset = self.a_work_img.getpixel( ( i_pos_x, i_pos_y))

            # Use only the pair values, click is done in the picture zoom x 2
            if i_pos_y & 1:
                i_pos_y -= 1
            if i_pos_x & 1:
                i_pos_x -= 1

            if self.i_around_cursor != -1:
                self.i_around_cursor = - 1

            self.a_mouse_pos_x_input_var.set( str( i_pos_x))
            self.a_mouse_pos_y_input_var.set( str( i_pos_y))
            self.a_pos_x_true_lbl.configure( text=str( int( ( i_pos_x & 1022) / 2)))
            self.a_pos_y_true_lbl.configure( text=str( int( ( i_pos_y & 1022) / 2)))

            self.a_color_lbl.configure( text=str( i_offset))
            self.a_scb_lbl.configure( text=str( int( i_offset / 16)))
            self.a_line_slider.set( int( i_offset / 16))

            # Select the radio button color in the pallet
            self.c_main_pallet.mwp_select_color_rad_btn( i_offset)

            # print( "mw_click_on_picture() i_offset = ", str( i_offset))
            self.c_main_pallet.mwp_color_btn_rad( i_offset)

            # Draw bar chart for colors in usage in a line
            self.mwi_draw_bar_chart( i_offset, i_pos_y)

            # Display zoom of a part of the picture
            self.c_main_pallet.mwp_draw_zoom_square( i_pos_x, i_pos_y)

            self.w_tk_root.update()
            print()

    # ####################### __mwi_less_x_value_clicked ########################
    def __mwi_less_x_value_clicked( self):
        """ Decrease value of X clicked """
        if self.a_work_img:
            i_current_val = int( self.a_mouse_pos_x_input_var.get())
            i_current_val = max( i_current_val-2, 0)
            self.a_mouse_pos_x_input_var.set( str( i_current_val))
            self.a_pos_x_true_lbl.configure( text=str( int( i_current_val / 2)))
            # goto self.__mwi_click_on_picture()
            self.a_picture_lbl.event_generate("<1>", x=i_current_val, y=self.a_mouse_pos_y_input_var.get())

    # ####################### __mwi_more_x_value_clicked ########################
    def __mwi_more_x_value_clicked( self):
        """ Increase value of X clicked """
        if self.a_work_img:
            i_current_val = int( self.a_mouse_pos_x_input_var.get())
            i_current_val = min( i_current_val+2, constant.PICTURE_WIDTH)
            self.a_mouse_pos_x_input_var.set( str( i_current_val))
            self.a_pos_x_true_lbl.configure( text=str( int( i_current_val / 2)))
            # goto self.__mwi_click_on_picture()
            self.a_picture_lbl.event_generate("<1>", x=i_current_val, y=self.a_mouse_pos_y_input_var.get())

    # ####################### __mwi_less_y_value_clicked ########################
    def __mwi_less_y_value_clicked( self):
        """ Decrease value of Y clicked """
        if self.a_work_img:
            i_current_val = int( self.a_mouse_pos_y_input_var.get())
            i_current_val = max( i_current_val-2, 0)
            self.a_mouse_pos_y_input_var.set( str( i_current_val))
            self.a_pos_y_true_lbl.configure( text=str( int( i_current_val / 2)))
            # goto self.__mwi_click_on_picture()
            self.a_picture_lbl.event_generate("<1>", x=self.a_mouse_pos_x_input_var.get(), y=i_current_val)

    # ####################### __mwi_more_y_value_clicked ########################
    def __mwi_more_y_value_clicked( self):
        """ Increase value of Y clicked """
        if self.a_work_img:
            i_current_val = int( self.a_mouse_pos_y_input_var.get())
            i_current_val = min( i_current_val+2, constant.PICTURE_HEIGHT)
            self.a_mouse_pos_y_input_var.set( str( i_current_val))
            self.a_pos_y_true_lbl.configure( text=str( int( i_current_val / 2)))
            # goto self.__mwi_click_on_picture()
            self.a_picture_lbl.event_generate("<1>", x=self.a_mouse_pos_x_input_var.get(), y=i_current_val)

    # ####################### __mv_entry_mouse_x_focus_in ########################
    def __mwi_entry_mouse_x_focus_in( self, _):
        """ entry mouse pos X take the focus """
        self.w_tk_root.unbind( "<Key>")
        print( "mv_entry_mouse_x_focus_in()")

    # ####################### __mv_entry_mouse_y_focus_in ########################
    def __mwi_entry_mouse_y_focus_in( self, _):
        """ entry mouse pos Y take the focus """
        self.w_tk_root.unbind( "<Key>")
        print( "mv_entry_mouse_y_focus_in()")

    # ####################### __mv_entry_mouse_x_y_focus_out ########################
    def __mwi_entry_mouse_x_y_focus_out( self, _):
        """ entry mouse pos X or Y loose the focus """
        self.w_tk_root.bind( "<Key>" , self.mwi_on_single_key)
        print( "mv_entry_mouse_x_y_focus_out()")

    # ####################### __mwi_set_max_len_to_four_chars_and_filter ########################
    def __mwi_set_max_len_to_four_chars_and_filter( self, i_action, s_string_apres, s_insert) -> bool:
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

        b_result = False
        if s_insert in '0123456789ABCDEF':
            # print( '__mwi_set_max_len_to_four_chars_and_filter() : __s_value len = ' + str( len( __s_value) + 1) )
            if int( i_action) == 0:     # deletion
                # print( '__mwi_set_max_len_to_four_chars_and_filter() : action = deletion' )
                if len( s_string_apres) + 1 > 8:
                    b_result = True
            elif int( i_action) == 1:   # insertion
                # print( '__mwi_set_max_len_to_four_chars_and_filter() : action = insertion' )
                if len( s_string_apres) + 1 < 16:
                    b_result = True
            else:
                # print( '__mwi_set_max_len_to_four_chars_and_filter() : autre')
                b_result = True
        else:
            print( '__mwi_set_max_len_to_four_chars_and_filter() : key= ' + str( s_insert) )

        return b_result

    # ####################### __mwi_change_scb_line ########################
    def __mwi_change_scb_line( self):
        """ Change the line pallet """
        if self.a_original_img:
            i_line_number = int( self.a_pos_y_true_lbl.cget( "text"))
            i_current_pallet_number = int( self.a_scb_lbl.cget( "text"))
            i_new_pallet_number = int( self.a_line_slider.get())
            if i_current_pallet_number != i_new_pallet_number:
                # print( " Convert the index." )
                if i_current_pallet_number > i_new_pallet_number:
                    i_delta = (i_new_pallet_number - i_current_pallet_number) * 16
                else:
                    i_delta = abs( (i_current_pallet_number - i_new_pallet_number) * 16)

                for i_index in range( 0, 319, 1):
                    i_current_index = self.a_original_img.getpixel( ( i_index, i_line_number))
                    i_current_index += i_delta
                    self.a_original_img.putpixel( ( i_index, i_line_number), i_current_index)

                # width, height = self.a_original_img.size
                # print( "width = " + str( width) + "  height = " + str( height) )
                # self.a_work_img.save( self.s_filename, 'BMP')
                # self.a_work_img = Image.open( self.s_filename)
                # s_filename = self.s_init_pathname + mt_get_path_separator( self.s_platform) + self.a_filename_lbl.cget( "text")
                self.c_main_windows.mw_update_main_window( self.c_main_icon_bar.mwib_get_get_path_filename() , self.a_original_img)
                self.mwi_click_in_picture_center( int( self.a_mouse_pos_x_input_var.get()), int( self.a_mouse_pos_y_input_var.get()))

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

    # ####################### mw_click_in_picture_center ########################
    def mwi_click_in_picture_center( self, pos_x=320, pos_y=200):
        """ Click on the center of the picture only after loaded it """
        # call method self.__mwi_click_on_picture()
        self.a_picture_lbl.event_generate("<1>", x=pos_x, y=pos_y)

    # ####################### mw_on_single_key ########################
    def mwi_on_single_key( self, event):
        """ Method manage arrow key press for the main windows """
        # print( "mw_on_single_key() ", event)
        # a_widget = event.widget
        # print( "mw_on_single_key() ", a_widget)
        # print( "mw_on_single_key() ", a_widget._name)
        # print( "mw_on_single_key() ", str( a_widget.winfo_id()))

        # print( "focus is:", root.focus_get())
        if event.keysym == "Left":
            self.a_less_x_btn.invoke()
        elif event.keysym == "Right":
            self.a_more_x_btn.invoke()
        elif event.keysym == "Up":
            self.a_less_y_btn.invoke()
        elif event.keysym == "Down":
            self.a_more_y_btn.invoke()
        # elif event.keysym == "Return":
        #     self.a_more_y_btn.invoke()
        # elif event.keysym == "Tab":
        #     self.a_more_y_btn.invoke()
        else:
            s_key = event.char
            print( 'mw_on_single_key() : key= ' + s_key )

    # ####################### get_original_image ########################
    def mwi_get_original_image( self):
        """ get original image the base bmp to the apple II GS resolution """
        return self.a_original_img

    # ####################### get_working_image ########################
    def mwi_get_working_image( self):
        """ get the resize and resised working image """
        return self.a_work_img

    # ####################### get_mouse_pos_x_var ########################
    def mwi_get_mouse_pos_x_var( self):
        """ get a_mouse_pos_x_input_var """
        return int( self.a_mouse_pos_x_input_var.get())

    # ####################### get_mouse_pos_y_var ########################
    def mwi_get_mouse_pos_y_var( self):
        """ get a_mouse_pos_y_input_var """
        return int( self.a_mouse_pos_y_input_var.get())

    # ####################### get_mouse_live_pos_x ########################
    # def get_mouse_live_pos_x( self):
    #     """ get value of the latest position of the mouse X """
    #     self.a_mouse_live_pos_x

    # ####################### get_mouse_live_pos_y ########################
    # def get_mouse_live_pos_y( self):
    #     """ get value of the latest position of the mouse Y """
    #     self.a_mouse_live_pos_y

    # ####################### set_mouse_live_pos_x ########################
    def mwi_set_mouse_live_pos_x( self, i_pos_x):
        """ set value of the latest position of the mouse X """
        self.a_mouse_live_pos_x.configure( text=str( i_pos_x))

    # ####################### set_mouse_live_pos_y ########################
    def mwi_set_mouse_live_pos_y( self, i_pos_y):
        """ set value of the latest position of the mouse Y """
        self.a_mouse_live_pos_y.configure( text=str( i_pos_y))

    # ####################### mwi_draw_bar_chart ########################
    def mwi_draw_bar_chart( self, i_offset, i_position_y):
        """ Draw bar chart for colors in usage in a line """
        # print( "mwi_draw_bar_chart : i_offset= " + str( i_offset) + " i_position_x= " + str( i_position_y))
        self.a_bar_chart_cnvs.delete( "all")
        a_usage_color_rry = array.array( 'i')
        a_usage_color_rry = [1] * 16
        a_result_color_rry = array.array( 'i')
        a_result_color_rry = [0] * 16
        i_pallet_number = int( i_offset / 16) * 16

        for i_loop in range( 0, constant.PICTURE_WIDTH, 2):
            i_offset = self.a_work_img.getpixel( ( i_loop, i_position_y))
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
                self.a_bar_chart_cnvs.create_rectangle( (i_colmun_x, 84-i_hauteur, i_colmun_x+20, 84), fill=self.c_main_pallet.get_from_pal_btn_lst_color(i_pallet_number+i_loop), outline='white')
                if a_usage_color_rry[i_loop] > 0 and a_usage_color_rry[i_loop] < 10:
                    self.a_bar_chart_cnvs.create_text( i_colmun_x+8, 84-64, text=str( a_usage_color_rry[i_loop]), fill="black")
            i_colmun_x += 24

    # ####################### mw_draw_scb_bar ########################
    def mwi_draw_scb_bar( self, i_color_offset):
        """ Draw the bar with rectangles to display all the SCB usage """
        i_pallet_number = int( i_color_offset / 16) * 16
        # print( " offset= " + str( i_color_offset) + "  pallet_number= " + str( i_pallet_number))
        self.a_scb_cnvs.delete( "all")
        self.a_scb_cnvs_rect_lst.clear()
        i_rect_begin = -1
        for i_loop in range( 0, constant.PICTURE_HEIGHT, 2):
            i_offset = self.a_work_img.getpixel( ( 0, i_loop))
            i_inter = int( i_offset / 16) * 16
            if i_inter == i_pallet_number:
                if i_rect_begin == -1:
                    i_rect_begin = i_loop   # te Y hight of the rectangle
            else:
                if i_rect_begin != -1:
                    self.a_scb_cnvs_rect_lst.append( self.a_scb_cnvs.create_rectangle( 0, i_rect_begin, 24, i_loop-1, fill='blue', outline='blue'))
                    i_rect_begin = -1
                i_inter = 0
        # print( "Number of rectangle created = " + str( len( self.a_scb_cnvs_rect_lst)))

    # ####################### mw_update_main_window ########################
    def mwi_update_main_window_image( self, s_filename, a_work_img):
        """ Load a picture and fill the interface """
        if s_filename and a_work_img:
            self.a_original_img = a_work_img.copy()
            self.a_work_img = a_work_img
            width, height = self.a_work_img.size
            self.a_work_img = self.a_work_img.resize( (width * 2, height * 2))

            # disabled its for debug
            # for i_loop in range( 0, 60, 1):
            #     i_pallet_offset = self.a_work_img.getpixel( (0,i_loop))
            #     print( str(i_loop) + " i_pallet_Offset = " + str(i_pallet_offset) + "  pal= " + str(int(i_pallet_offset/16)) + " ndx= " + str( i_pallet_offset - (int(i_pallet_offset/16)) * 16))

            self.a_render = ImageTk.PhotoImage( self.a_work_img)
            self.a_picture_lbl.config( image=self.a_render)
            self.a_picture_lbl.photo = self.a_render

            self.a_filename_lbl.config( text=os.path.basename( s_filename))

    # ####################### mwi_set_pallet ########################
    def mwi_set_pallet( self, c_pallet):
        """ Give access to method of c_pallet """
        self.c_main_pallet = c_pallet

    # ####################### mwi_change_pallet ########################
    def mwi_change_pallet( self, event):
        """ Click on the SCB """
        if self.a_original_img and self.a_work_img:
            print( "clicked at", event.x, event.y)
            print( "Number of rectangle created = " + str( len( self.a_scb_cnvs_rect_lst)))
            for i_loop in range( 0, len( self.a_scb_cnvs_rect_lst), 1):
                a_cnvs_rect = self.a_scb_cnvs_rect_lst[i_loop]
                x0, y0, x1, y1 = self.a_scb_cnvs.coords( a_cnvs_rect)
                print( f'#{i_loop} {x0:0.0f} {y0:0.0f} {x1:0.0f} {y1:0.0f}'.format(i_loop, x0, y0, x1, y1))
                if event.y >= y0 and event.y <= y1:
                    print( "C'est le bon at index= ", i_loop )
                    break

            print()
            # x0, y0, x1, y1 = w.coords(blue)
            # w.coords(blue, x0, y0, x1, y1)

            # self.c_the_log.add_string_to_log( 'Do scb editor pallet')
            # w_front_window = MyScbPalletWindow( self.c_main_windows, self.a_scb_cnvs_rect_lst[], event.y)
            # w_front_window.scbw_create_scb_window( None, self.a_work_img, 0)
            # w_front_window = None
            # self.c_main_windows.mw_update_main_window( self.c_main_icon_bar.mwib_get_get_path_filename(), self.a_work_img)
            # self.c_main_windows.update()
            # self.mwi_click_in_picture_center()

    # ####################### mw_picture_zone ########################
    def mwi_picture_zone( self, a_pic_frame, i_pic_frame_width, c_icon_bar):
        """ Frame with the picture to left, and details to right """
        s_platform = platform.system()
        self.c_main_icon_bar = c_icon_bar
        i_index_base_block = 0
        # print( a_pic_frame.get())
        a_pic_sep_h0 = Separator( a_pic_frame, orient='horizontal')
        a_pic_sep_h0.grid(row=i_index_base_block, column=0, columnspan=1, sticky='ew')
        a_pic_sep_lbl_h0 = Label( a_pic_frame, text="Picture", anchor="center", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h0.grid( row=i_index_base_block, column=0, columnspan=1)
        a_pic_sep_h1 = Separator( a_pic_frame, orient='horizontal')
        a_pic_sep_h1.grid( row=i_index_base_block, column=2, columnspan=1, sticky='ew')
        a_pic_sep_lbl_h1 = Label( a_pic_frame, text="SCB", anchor="center", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h1.grid( row=i_index_base_block, column=2, columnspan=1)
        a_pic_sep_h2 = Separator( a_pic_frame, orient='horizontal')
        a_pic_sep_h2.grid( row=i_index_base_block, column=4, columnspan=5, sticky='ew')
        a_pic_sep_lbl_h2 = Label( a_pic_frame, text="Details", anchor="center", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h2.grid( row=i_index_base_block, column=4, columnspan=5, padx=200)

        i_index_base_block += 1
        if s_platform == "Linux":
            self.a_picture_lbl = Label( a_pic_frame, padx=0, pady=0, image=None, width=constant.PICTURE_WIDTH, height=constant.PICTURE_HEIGHT, background=constant.BACKGROUD_COLOR_UI, cursor="circle", borderwidth=0, compound="center", highlightthickness=0)
        else:
            self.a_picture_lbl = Label( a_pic_frame, padx=0, pady=0, image=None, width=constant.PICTURE_WIDTH, height=constant.PICTURE_HEIGHT, background=constant.BACKGROUD_COLOR_UI, cursor="circle", borderwidth=0, compound="center", highlightthickness=0)
        self.a_picture_lbl.grid( row=i_index_base_block, column=0)
        self.a_picture_lbl.bind( '<Button>', self.__mwi_click_on_picture)
        self.a_picture_lbl.bind( '<Motion>', self.c_main_windows.mw_print_widget_under_mouse)

        # Create SCB frame to draw rectangle to present SCB
        a_scb_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_scb_frame.place( x=644, y=21, width=24, height=constant.PICTURE_HEIGHT)

        self.a_scb_cnvs = Canvas( a_scb_frame, width=24, height=constant.PICTURE_HEIGHT, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
        self.a_scb_cnvs.grid( row=0, column=0, sticky='ewns')
        self.a_scb_cnvs.bind("<Button-1>", self.mwi_change_pallet)

        self.w_tk_root.update()
        # Create details frame
        i_width = i_pic_frame_width
        i_width = i_width - ( 640 + 24 + 10)
        a_details_pic_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background=constant.BACKGROUD_COLOR_UI or'darkgray' or 'light grey'
        a_details_pic_frame.place( x=668, y=21, width=i_width, height=constant.PICTURE_HEIGHT)

        a_bar_chart_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_bar_chart_frame.place( x=668, y=21+(constant.PICTURE_HEIGHT-104), width=i_width, height=104)

        i_index_base_block = 0
        self.a_bar_chart_cnvs = Canvas( a_bar_chart_frame, width=i_width - 10, height=84, background=constant.BACKGROUD_COLOR_UI, highlightthickness=0) # constant.BACKGROUD_COLOR_UI
        self.a_bar_chart_cnvs.grid( row=i_index_base_block, column=0, padx=4, pady=2, sticky='ewns')
        i_index_base_block += 1
        i_index_base_column = 0
        a_font_label = font.Font( size=6)

        a_bar_chart_comment_frame = tk_gui.Frame( a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_bar_chart_comment_frame.place( x=667, y=30+(constant.PICTURE_HEIGHT-20), width=self.i_main_window_width - 438, height=15)
        for i_loop in range( 0, 16, 1):
            a_label = Label(a_bar_chart_comment_frame, text=str( i_loop), width=2, justify='left', background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            if s_platform == "Linux":
                a_label.grid( row=1, column=i_index_base_column, padx=5, pady=0, sticky='w')
            else:
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
        self.a_mouse_live_pos_x = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH-2, background='light grey', foreground='black')
        self.a_mouse_live_pos_x.grid( row=i_index_base_block, column=2, padx=4, pady=1, sticky='ew')
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="Y ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')
        self.a_mouse_live_pos_y = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH-2, background='light grey', foreground='black')
        self.a_mouse_live_pos_y.grid( row=i_index_base_block, column=4, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h3 = Label( a_details_pic_frame, text="Mouse click position", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h3.grid( row=i_index_base_block, column=1, columnspan=5, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h5 = Label( a_details_pic_frame, text="X ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h5.grid( row=i_index_base_block, column=1, padx=4, pady=1)
        # font='-weight bold'
        self.a_mouse_pos_x = Entry( a_details_pic_frame, textvariable=self.a_mouse_pos_x_input_var, width=constant.DEFAULT_BUTTON_WIDTH, validatecommand=( a_pic_frame.register( self.__mwi_set_max_len_to_four_chars_and_filter), '%d', '%s', '%S'), background='white', foreground='black')
        self.a_mouse_pos_x.grid( row=i_index_base_block, column=2, padx=4, pady=1)
        self.a_mouse_pos_x.bind( "<FocusIn>", self.__mwi_entry_mouse_x_focus_in)
        self.a_mouse_pos_x.bind( "<FocusOut>", self.__mwi_entry_mouse_x_y_focus_out)

        self.a_pos_x_true_lbl = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH-2, background='light grey', foreground='black')
        self.a_pos_x_true_lbl.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')

        if self.s_platform == "Darwin":
            self.a_less_y_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_up_arrow_photo(), command=self.__mwi_less_y_value_clicked, width=44, height=20, relief='raised', highlightbackground='light grey', repeatdelay=500, repeatinterval=100)
        else:
            self.a_less_y_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_up_arrow_photo(), command=self.__mwi_less_y_value_clicked, width=44, height=20, relief='raised', background=constant.BACKGROUD_COLOR_UI, repeatdelay=500, repeatinterval=100)
        self.a_less_y_btn.grid( row=i_index_base_block, column=6, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        if self.s_platform == "Darwin":
            self.a_less_x_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_left_arrow_photo(), command=self.__mwi_less_x_value_clicked, width=44, height=20, relief='raised', highlightbackground='light grey', repeatdelay=500, repeatinterval=100)
        else:
            self.a_less_x_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_left_arrow_photo(), command=self.__mwi_less_x_value_clicked, width=44, height=20, relief='raised', background=constant.BACKGROUD_COLOR_UI, repeatdelay=500, repeatinterval=100)
        self.a_less_x_btn.grid( row=i_index_base_block, column=5, padx=4, pady=1, sticky='ew')

        if self.s_platform == "Darwin":
            self.a_more_x_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_right_arrow_photo(), command=self.__mwi_more_x_value_clicked, width=44, height=20, relief='raised', highlightbackground='light grey', repeatdelay=500, repeatinterval=100)
        else:
            self.a_more_x_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_right_arrow_photo(), command=self.__mwi_more_x_value_clicked, width=44, height=20, relief='raised', background=constant.BACKGROUD_COLOR_UI, repeatdelay=500, repeatinterval=100)
        self.a_more_x_btn.grid( row=i_index_base_block, column=7, padx=4, pady=1, sticky='ew')

        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="Y ", width=4, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4, pady=1)
        self.a_mouse_pos_y = Entry( a_details_pic_frame, textvariable=self.a_mouse_pos_y_input_var, width=constant.DEFAULT_BUTTON_WIDTH, validatecommand=( a_pic_frame.register( self.__mwi_set_max_len_to_four_chars_and_filter), '%d', '%s', '%S'), background='white', foreground='black')
        self.a_mouse_pos_y.grid( row=i_index_base_block, column=2, padx=4, pady=1)
        self.a_mouse_pos_y.bind( "<FocusIn>", self.__mwi_entry_mouse_y_focus_in)
        self.a_mouse_pos_y.bind( "<FocusOut>", self.__mwi_entry_mouse_x_y_focus_out)

        self.a_pos_y_true_lbl = Label( a_details_pic_frame, text="   ", width=constant.DEFAULT_BUTTON_WIDTH-2, background='light grey', foreground='black')
        self.a_pos_y_true_lbl.grid( row=i_index_base_block, column=3, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h5 = Label( a_details_pic_frame, text="Color offset", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h5.grid( row=i_index_base_block, column=1, columnspan=2, padx=4, pady=1, sticky='ew')
        self.a_color_lbl = Label( a_details_pic_frame, text="   ", background='light grey', foreground='black')
        self.a_color_lbl.grid( row=i_index_base_block, column=3, columnspan=1, padx=4, pady=1, sticky='ew')

        if self.s_platform == "Darwin":
            self.a_more_y_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_down_arrow_photo(), command=self.__mwi_more_y_value_clicked, width=44, height=20, relief='raised', highlightbackground='light grey', repeatdelay=500, repeatinterval=100)
        else:
            self.a_more_y_btn = Button( a_details_pic_frame, image=self.c_the_icons.get_down_arrow_photo(), command=self.__mwi_more_y_value_clicked, width=44, height=20, relief='raised', background=constant.BACKGROUD_COLOR_UI, repeatdelay=500, repeatinterval=100)
        self.a_more_y_btn.grid( row=i_index_base_block, column=6, padx=4, pady=1, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h6 = Label( a_details_pic_frame, text="Pallet line", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h6.grid( row=i_index_base_block, column=1, columnspan=2, padx=4, pady=1, sticky='ew')
        self.a_scb_lbl = Label( a_details_pic_frame, text="   ", background='light grey', foreground='black')
        self.a_scb_lbl.grid( row=i_index_base_block, column=3, columnspan=1, padx=4, pady=1, sticky='ew')
        self.a_line_slider = Scale( a_details_pic_frame, from_=0, to=15, orient='horizontal', background=constant.BACKGROUD_COLOR_UI, highlightbackground='light grey', borderwidth=0, highlightthickness=0)
        self.a_line_slider.grid( row=i_index_base_block, rowspan=2, column=4, columnspan=6, padx=4, pady=2, sticky='ewns')

        i_index_base_block += 1
        if self.s_platform == "Darwin":
            a_change_scb_btn = Button( a_details_pic_frame, text='Change pallet line number', command=self.__mwi_change_scb_line, width=21, height=1, relief='raised', highlightbackground=constant.BACKGROUD_COLOR_UI)
            a_change_scb_btn.grid( row=i_index_base_block, column=1, columnspan=3, padx=2, pady=0, sticky='ew')
        else:
            a_change_scb_btn = Button( a_details_pic_frame, text='Change pallet line number', command=self.__mwi_change_scb_line, width=21, height=1, relief='raised', background=constant.BACKGROUD_COLOR_UI)
            a_change_scb_btn.grid( row=i_index_base_block, column=1, columnspan=3, padx=4, pady=1, sticky='ew')
