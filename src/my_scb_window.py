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

""" Module de gestion SCB pallet editor """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import platform
import tkinter as tk_gui

from tkinter import Label, Button, Toplevel, Scale
from tkinter.ttk import Combobox
from PIL import ImageTk

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures

# __name__ = "MyScbPalletWindow"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= SSB Pallet Dialogs Window =========================
class MyScbPalletWindow:
    """ Create the scb pallet Windows of the application """
    # pylint: disable=too-many-instance-attributes
    # number is reasonable in this case these are all the icons of the main windows and the application icons

    # ANSWER_CANCEL = 0
    # ANSWER_OK = 1
    SCB_NUMBER_LST = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
    MIDDLE_FRAME_HEIGHT = 40
    BOTTOM_FRAME_HEIGHT = 34

    # ####################### __init__ ########################
    def __init__( self, c_the_main_window, a_scb_cnvs_rect_lst, i_click_y, i_selected_pallet_line):
        """
            all this parameter are created in main()
            c_the_main_window : the parent windows
        """
        self.c_the_main_window = c_the_main_window
        self.a_scb_cnvs_rect_lst            : list = a_scb_cnvs_rect_lst
        self.i_click_y = i_click_y
        self.i_selected_pallet_line = i_selected_pallet_line

        self.c_the_log = MyLogAnUsage( None)
        self.c_the_icons = MyIconPictures( None)
        self.s_platform = platform.system()
        self.w_scb_window = None
        self.a_work_img = None

        self.a_original_part_image = None
        self.a_list_device_combo            : list = None
        self.i_index_in_a_scb_cnvs_rect_lst = 0

        self.a_mouse_live_pos_y_lbl         : Label = None
        self.i_height = 0
        self.i_width = 0
        self.i_position_x = 0
        self.i_position_y = 0
        self.scb_background = 'darkgray'
        self.i_selected_pallet = -1                     # source of index pallet to copy
        self.i_selected_pallet_in_main_windows = -1     # target of destination index
        self.a_zoom_lbl                     : Label = None
        self.a_zoom_work_img                : ImageTk.PhotoImage = None
        self.a_render_zoom                  : ImageTk.PhotoImage = None
        self.a_scb_cnvs                     : list = None
        self.a_the_color_new_lbl            : Label = None
        self.a_frontier_scale               : Scale = None
        self.a_list_pallet_to_begin_combo   : Combobox = None
        self.a_list_pallet_to_end_combo     : Combobox = None
        self.a_down_begin_lbl               : Label = None

    # ####################### __scbw_do_stuff_to_leave_this_dialog ########################
    def __scbw_do_stuff_to_leave_this_dialog( self):
        """ Do commun stuff when press button ok or cancel on the scb window """
        self.a_zoom_lbl.unbind( '<Motion>')
        self.a_zoom_lbl.unbind( '<Button>')
        self.w_scb_window.grab_release()
        self.w_scb_window.quit()

    # ####################### __scbw_import_ok_button ########################
    def __scbw_import_ok_button( self):
        """ Button ok of the scb window """
        # a_work_pallet_list = self.a_work_img.getpalette()

        # self.imported_pallet_lst.clear()
        # i_first_color_conponent_to_copy = int( self.a_list_device_combo.get()) * 16 * 3
        # i_last_color_conponent_to_copy = i_first_color_conponent_to_copy + ( 16 * 3)

        # a_pallet_list = self.a_original_part_image.getpalette()
        # i_index = self.i_selected_pallet * 16 * 3
        # for i_loop in range( 0, len( a_work_pallet_list), 1):
        #     if i_loop in range( i_first_color_conponent_to_copy, i_last_color_conponent_to_copy):
        #         # Copy of 16 colors (3 integers per color)
        #         self.imported_pallet_lst.append( a_pallet_list[i_index])
        #         i_index += 1
        #     else:
        #         # Copy 768 colors - 48 (3 integers per color)
        #         self.imported_pallet_lst.append( a_work_pallet_list[i_loop])

        # self.a_work_img.putpalette( self.imported_pallet_lst)

        self.__scbw_do_stuff_to_leave_this_dialog()
        self.c_the_log.add_string_to_log( 'Do SCB edit close with ok')

    # ####################### __scbw_import_cancel_button ########################
    def __scbw_import_cancel_button( self):
        """ Button cancel of the scb window """
        # self.imported_pallet_lst = None
        # self.i_selected_pallet = -1

        self.__scbw_do_stuff_to_leave_this_dialog()
        self.c_the_log.add_string_to_log( 'Do SCB edit close with cancel')

    # ####################### __scbw_print_coord_under_mouse ########################
    def __scbw_print_coord_under_mouse( self, event):
        """ Show live position of the mouse in the loaded picture """
        i_pos_x = event.x
        i_pos_y = event.y
        # Use only the pair values, click is done in the picture zoomed x 2
        if i_pos_y & 3:
            i_pos_y -= 3
        if i_pos_x & 3:
            i_pos_x -= 3

        self.a_mouse_live_pos_y_lbl.configure( text=str( int(event.y / 3)))

        a_pallet_list = self.a_zoom_work_img.getpalette()
        i_base = 3 * self.a_zoom_work_img.getpixel((i_pos_x, i_pos_y))
        i_red, i_green, i_blue = a_pallet_list[i_base:i_base+3]
        self.a_the_color_new_lbl.configure( background= f"#{i_red:02x}{i_green:02x}{i_blue:02x}")

    # ####################### __scbw_update_begin ########################
    def __scbw_update_begin( self, s_value):
        """" Scale is moving update the label """
        i_value = int( s_value)
        if len( s_value) == 1 and i_value < 9:
            self.a_down_begin_lbl.configure( text="  " + str( i_value + 1))
        else:
            self.a_down_begin_lbl.configure( text=str( i_value + 1))

    # ####################### __scbw_click_on_picture ########################
    def __scbw_click_on_picture( self, event):
        """ Show position of the mouse in the loaded picture and repair SCB to draw a rect """
        self.a_frontier_scale.set( int( event.y / 3) )
        self.a_down_begin_lbl.configure( text=str( int( event.y / 3) + 1))

    # ####################### __scbw_scb_block ########################
    def __scbw_scb_block( self, i_part_width, i_part_height):
        """ Create a about dialog """
        # Define the GUI
        top_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.i_height, relief='flat', background=constant.BACKGROUD_COLOR_UI)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_up_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        middle_up_frame.pack( side='top', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_up_frame.pack_propagate( False)
        middle_middle_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        middle_middle_frame.pack( side='top', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_middle_frame.pack_propagate( False)
        middle_down_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        middle_down_frame.pack( side='top', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_down_frame.pack_propagate( False)
        button_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.BOTTOM_FRAME_HEIGHT, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR)
        button_frame.pack( side='bottom', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_down_frame.pack_propagate( False)

        # #### TOP #####
        self.a_zoom_lbl = Label( top_frame, image=self.a_render_zoom, background=constant.BACKGROUD_COLOR_UI, width=i_part_width * 3, height=i_part_height * 3, borderwidth=0, compound="center", highlightthickness=0)
        # if self.s_platform in [ "Darwin", "Linux" ]:
        #     self.a_zoom_lbl.pack( side='left', padx=4)
        # else:
        self.a_zoom_lbl.pack( side='left', padx=4)
        self.a_zoom_lbl.photo = self.a_render_zoom
        self.a_zoom_lbl.bind( '<Motion>', self.__scbw_print_coord_under_mouse)
        self.a_zoom_lbl.bind( '<Button>', self.__scbw_click_on_picture)

        # #### MIDDLE #####
        a_label = Label( middle_up_frame, text="The Pallet used for this SCB is " + str(self.i_selected_pallet_line) + ".", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='left', padx=4)
        a_label = Label( middle_up_frame, text="Mouse live position on Y:", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='left', padx=4)
        self.a_mouse_live_pos_y_lbl = Label( middle_up_frame, text="   ", width=3, background=constant.BACKGROUD_COLOR_UI, foreground='black')
        self.a_mouse_live_pos_y_lbl.pack( side='left', padx=4)
        a_label = Label( middle_up_frame, text="Color under the cursor is ", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='left', padx=4)
        self.a_the_color_new_lbl = Label( middle_up_frame, text=None, width=8, borderwidth=2, background='black', foreground='black')
        self.a_the_color_new_lbl.pack( side='left', padx=4)

        a_label = Label( middle_middle_frame, text="The UPPER part, from 0 to", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='left', padx=2)
        self.a_frontier_scale = Scale( middle_middle_frame, from_=0, to=i_part_height-2, length=500, command=self.__scbw_update_begin, orient='horizontal', background=constant.BACKGROUD_COLOR_UI, highlightbackground='light grey', borderwidth=0, highlightthickness=0, troughcolor='light grey')
        self.a_frontier_scale.pack( side='left', padx=2)
        self.a_frontier_scale.set(int(i_part_height/3))
        a_label = Label( middle_middle_frame, text="use the pallet line (SCB number)", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='left', padx=2)
        self.a_list_pallet_to_begin_combo = Combobox( middle_middle_frame, values=self.SCB_NUMBER_LST, width=3, state="readonly")
        self.a_list_pallet_to_begin_combo.pack( side='left', padx=4)
        self.a_list_pallet_to_begin_combo.current( self.i_selected_pallet_line)

        self.a_list_pallet_to_end_combo = Combobox( middle_down_frame, values=self.SCB_NUMBER_LST, width=3, state="readonly")
        self.a_list_pallet_to_end_combo.pack( side='right', padx=4)
        self.a_list_pallet_to_end_combo.current( self.i_selected_pallet_line)
        a_label = Label( middle_down_frame, text=" to " + str(i_part_height-1) + " will use the pallet line (SCB number)", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='right', padx=2)
        self.a_down_begin_lbl = Label( middle_down_frame, text=str(int(i_part_height/3)+1), height=1, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        self.a_down_begin_lbl.pack( side='right')
        a_label = Label( middle_down_frame, text="The LOWER part, from ", height=1, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_label.pack( side='right', padx=2)

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 4 charracters
        if self.s_platform == "Darwin":
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 4, compound="c", command=self.__scbw_import_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=2, pady=2 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 4, compound="c", command=self.__scbw_import_cancel_button, relief='raised', background=self.scb_background)
            a_cancel_btn.pack( side='right', padx=2, pady=2 )
        else:
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 4, compound="c", command=self.__scbw_import_ok_button, relief='raised', background=self.scb_background)
            a_ok_btn.pack( side='right', padx=4, pady=4 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 4, compound="c", command=self.__scbw_import_cancel_button, relief='raised', background=self.scb_background)
            a_cancel_btn.pack( side='right', padx=4, pady=4 )

    # ####################### __scbw_set_window_size ########################
    def __scbw_set_window_size( self):
        """ Set the size of the configuration windows (+16 for any line added in a_middle_text) """
        # print( "computer height =" + str( 30 + self.i_height + (self.MIDDLE_FRAME_HEIGHT * 3) + self.BOTTOM_FRAME_HEIGHT))
        self.i_height += 30 +  (self.MIDDLE_FRAME_HEIGHT * 3) + self.BOTTOM_FRAME_HEIGHT
        if self.s_platform == "Linux":
            self.i_width = 968
            self.i_height += 0  #374
        elif self.s_platform == "Darwin":
            self.i_width = 968
            self.i_height += 0  #306
        elif self.s_platform == "Windows":
            self.i_width = 968
            self.i_height += 0  #376

        self.i_position_x = self.c_the_main_window.mw_get_main_window_pos_x() + int((self.c_the_main_window.mw_get_main_window_width() - self.i_width) / 2)
        self.i_position_y = self.c_the_main_window.mw_get_main_window_pos_y() + int((self.c_the_main_window.mw_get_main_window_height() - self.i_height) / 2)

        s_windows_size_and_position = ( str( self.i_width) + 'x' + str( self.i_height) + '+' + str( self.i_position_x) + '+' + str( self.i_position_y))
        self.w_scb_window.geometry( s_windows_size_and_position)  # dimension + position x/y a l'ouverture

        # lock resize of main window
        self.w_scb_window.minsize( self.i_width, self.i_height)
        self.w_scb_window.maxsize( self.i_width, self.i_height)
        # no resize for both directions
        self.w_scb_window.resizable( False, False)
        self.w_scb_window.iconphoto( True, self.c_the_icons.get_app_photo())

        print( '\nscbw_set_window_size() : geometry  ' + s_windows_size_and_position + '\n')

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

    # ####################### scbw_create_scb_window ########################
    def scbw_create_scb_window( self, a_original_image, a_scb_cnvs, i_index_in_a_scb_cnvs_rect_lst):
        """ Design the import pallet box dialog """
        if a_original_image and a_scb_cnvs:
            self.c_the_log.add_string_to_log( 'scbw_create_scb_window()')
            w_parent_window = self.c_the_main_window.mw_get_main_window()

            # for i_loop in range( 0, len( self.a_scb_cnvs_rect_lst), 1):
            #     a_cnvs_rect = self.a_scb_cnvs_rect_lst[i_loop]
            #     x0, y0, x1, y1 = self.a_scb_cnvs.coords( a_cnvs_rect)
            #     print( f'#{i_loop} {x0:0.0f} {y0:0.0f} {x1:0.0f} {y1:0.0f}'.format(i_loop, x0, y0, x1, y1))
            #     if self.i_click_y >= y0 and self.i_click_y <= y1:
            #         print( "C'est le bon at index= ", i_loop )
            #         break

            self.a_original_part_image = a_original_image
            self.a_scb_cnvs = a_scb_cnvs
            self.i_index_in_a_scb_cnvs_rect_lst = i_index_in_a_scb_cnvs_rect_lst

            self.w_scb_window = Toplevel( w_parent_window)
            self.w_scb_window.lift( aboveThis=w_parent_window)
            # window dialog is on top of w_parent_window
            self.w_scb_window.grab_set()
            self.w_scb_window.focus_set()
            self.w_scb_window.configure( background=constant.BACKGROUD_COLOR_UI)

            self.w_scb_window.title( ' SCB edit ')

            # Prepare the picture band
            a_cnvs_rect = self.a_scb_cnvs_rect_lst[self.i_index_in_a_scb_cnvs_rect_lst]
            x0, y0, x1, y1 = self.a_scb_cnvs.coords( a_cnvs_rect)
            print( f'scbw_scb_block() rect       size is: {x0:0.0f} {y0:0.0f} {x1:0.0f} {y1:0.0f}'.format(x0, y0, x1, y1))
            width, height = a_original_image.size
            print( f'scbw_scb_block() org  image size is: {width:d} {height:d}'.format(width, height))

            i_box_top = (0, int(y0/2), 320, int(y1/2))
            a_part_image = a_original_image.crop( i_box_top)
            width, height = a_part_image.size
            print( f'scbw_scb_block() part image size is: {width:d} {height:d}'.format(width, height))
            self.a_zoom_work_img = a_part_image.resize( (width * 3, height * 3))     # Total of zoom is x 3
            self.a_render_zoom = ImageTk.PhotoImage( self.a_zoom_work_img)
            self.i_width = width * 3
            self.i_height = height * 3

            self.__scbw_scb_block( width, height)
            # self.w_scb_window.update()
            self.__scbw_set_window_size()

            self.w_scb_window.mainloop()
            self.w_scb_window.destroy()

    # ####################### scbw_close_scb_window ########################
    def scbw_close_scb_window( self):
        """ Close the preference window """
        self.__scbw_import_cancel_button()
        self.w_scb_window.quit()
