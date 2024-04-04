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

from tkinter import font, Label, Button, Toplevel, Radiobutton, IntVar
from tkinter.ttk import Combobox
from functools import partial
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

    answer_cancel = 0
    answer_ok = 1

    # ####################### __init__ ########################
    def __init__( self, c_the_main_window, a_scb_cnvs_rect_lst, i_click_y):
        """
            all this parameter are created in main()
            c_the_main_window : the parent windows
        """
        self.c_the_main_window = c_the_main_window
        self.c_the_log = MyLogAnUsage( None)
        self.c_the_icons = MyIconPictures( None)
        self.s_platform = platform.system()
        self.w_scb_window = None
        self.a_work_img = None

        self.a_scb_cnvs_rect_lst = a_scb_cnvs_rect_lst
        self.i_click_y = i_click_y
        self.a_scb_cnvs = None

        self.a_pallet_image = None
        self.a_list_device_combo = None
        self.i_index_in_a_scb_cnvs_rect_lst = 0

        self.i_height = 0
        self.i_width = 0
        self.i_position_x = 0
        self.i_position_y = 0
        self.import_background = 'darkgray'
        self.color_radio_button = IntVar()
        self.i_selected_pallet = -1                     # source of index pallet to copy
        self.i_selected_pallet_in_main_windows = -1     # target of destination index
        self.a_zoom_lbl = None
        self.a_zoom_work_img = None
        self.a_render_zoom = None

    # ####################### __scbw_import_ok_button ########################
    def __scbw_import_ok_button( self):
        """ Button ok of the import window """
        # a_work_pallet_list = self.a_work_img.getpalette()

        # self.imported_pallet_lst.clear()
        # i_first_color_conponent_to_copy = int( self.a_list_device_combo.get()) * 16 * 3
        # i_last_color_conponent_to_copy = i_first_color_conponent_to_copy + ( 16 * 3)

        # a_pallet_list = self.a_pallet_image.getpalette()
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

        self.w_scb_window.grab_release()
        self.w_scb_window.quit()
        self.c_the_log.add_string_to_log( 'Do SCB edit close with ok')

    # ####################### __scbw_import_cancel_button ########################
    def __scbw_import_cancel_button( self):
        """ Button cancel of the import window """
        # self.imported_pallet_lst = None
        # self.i_selected_pallet = -1
        self.w_scb_window.grab_release()
        self.w_scb_window.quit()
        self.c_the_log.add_string_to_log( 'Do SCB edit close with cancel')

    # ####################### __scbw_scb_block ########################
    def __scbw_scb_block( self, a_original_image):
        """ Create a about dialog """
        # global s_device_information
        top_frame = tk_gui.Frame( self.w_scb_window, relief='flat', background=constant.BACKGROUD_COLOR_UI)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_frame = tk_gui.Frame( self.w_scb_window, relief='flat', background=constant.BACKGROUD_COLOR_UI, width=self.i_width, height=214)
        middle_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        button_frame = tk_gui.Frame( self.w_scb_window, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR, width=self.i_width, height=23)
        button_frame.pack( side='bottom', fill='x', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        # #### TOP #####
        a_cnvs_rect = self.a_scb_cnvs_rect_lst[self.i_index_in_a_scb_cnvs_rect_lst]
        x0, y0, x1, y1 = self.a_scb_cnvs.coords( a_cnvs_rect)
        print( f'scbw_scb_block() {x0:0.0f} {y0:0.0f} {x1:0.0f} {y1:0.0f}'.format(x0, y0, x1, y1))

        i_box_top = (0, int(y0/2), 320, int(y1/2))
        a_part_image = a_original_image.crop( i_box_top)

        width, height = a_part_image.size
        self.a_zoom_work_img = a_part_image.resize( (width * 3, height * 3))     # Total of zoom is x 3
        self.a_render_zoom = ImageTk.PhotoImage( self.a_zoom_work_img)

        # the text is the cursor style on the middle of the label
        i_index_base_block = 0
        self.a_zoom_lbl = Label( top_frame, image=self.a_render_zoom, background=constant.BACKGROUD_COLOR_UI, width=width * 3, height=height * 3, borderwidth=0, compound="center", highlightthickness=0)
        if self.s_platform in [ "Darwin", "Linux" ]:
            self.a_zoom_lbl.grid( row=i_index_base_block, padx=2, pady=2, sticky='ewns')
        else:
            self.a_zoom_lbl.grid( row=i_index_base_block, padx=4, pady=2, sticky='ewns')
        self.a_zoom_lbl.photo = self.a_render_zoom

        # self.a_zoom_lbl.bind( '<Button>', self.__mwp_click_on_picture_zoom)
        self.w_scb_window.update()

        # #### MIDDLE #####
        i_index_base_block += 1
        # a_label = Label( top_frame, text="Select a color in the line to select copy of it:\n", height=2, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='white')
        # a_label.grid( row=i_index_base_block, column=i_index_base_column, columnspan=11, sticky='wns', padx=2, pady=0)

        # Table of color button for the pallet
        # a_pallet_list = a_image.getpalette()
        # i_index_base_block += 1
        # i_to = 0
        # i_index = 0
        # for i_loop in range( 0, 16, 1):
        #     i_from = i_to
        #     i_to = i_to + 48
        #     # First element of the line is its number
        #     a_label = Label( top_frame, text=str(i_loop), background=constant.BACKGROUD_COLOR_UI, foreground='white', font=font.Font( size=6))  # Creating a font object with little size for color buttons to reduce their size
        #     # if self.s_platform == "Darwin":
        #     #     a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
        #     # else:
        #     a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
        #     i_index_base_column += 1
        #     # create list of line of radio button and add it in a list to be accessible
        #     for i_value in range( i_from, i_to, 3):
        #         a_color_btn_rad = Radiobutton( top_frame, text='', indicatoron = 0, width=8, height=1, variable=self.color_radio_button, value=i_index, background=constant.BACKGROUD_COLOR_UI, font=font.Font( size=3))    # Creating a font object with little size for color buttons to reduce their size
        #         if self.s_platform in [ "Darwin", "Linux" ]:
        #             a_color_btn_rad.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=2)
        #         else:
        #             a_color_btn_rad.grid( row=i_index_base_block, column=i_index_base_column, padx=4, pady=2)
        #         a_color_btn_rad.configure( background="#" + f'{a_pallet_list[ i_index]:02X}' + f'{a_pallet_list[ i_index + 1]:02X}' + f'{a_pallet_list[ i_index + 2]:02X}')     # '# red green blue'
        #         a_color_btn_rad.configure( command=partial( self.__scbw_select_color_rad_btn, int( i_value / 3)))
        #         self.a_pallet_button_lst.append( a_color_btn_rad)
        #         i_index_base_column += 1
        #         i_index += 3

        #     i_index_base_column = 0
        #     i_index_base_block += 1

        # i_index_base_column = 0
        # self.a_selected_info_lbl = Label( top_frame, text="The selected line is 0. On click Ok it update pallet:", height=2, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='white')
        # self.a_selected_info_lbl.grid( row=i_index_base_block, column=i_index_base_column, columnspan=11, sticky='wns', padx=2, pady=0)

        # i_index_base_column += 11
        # # Création de la Combobox via la méthode ttk.Combobox()
        # self.a_list_device_combo = Combobox( top_frame, values=self.a_list_device_model, width=4, state="readonly")
        # self.a_list_device_combo.grid( row=i_index_base_block, column=i_index_base_column, columnspan=2, padx=2, pady=0)
        # # Choisir l'élément qui s'affiche par défaut
        # if self.i_selected_pallet_in_main_windows != -1:
        #     self.a_list_device_combo.current( self.i_selected_pallet_in_main_windows)
        # else:
        #     self.a_list_device_combo.current( 0)

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 2 charracters
        if self.s_platform == "Darwin":
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__scbw_import_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=2, pady=2 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__scbw_import_cancel_button, relief='raised', background=self.import_background)
            a_cancel_btn.pack( side='right', padx=2, pady=2 )
        else:
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__scbw_import_ok_button, relief='raised', background=self.import_background)
            a_ok_btn.pack( side='right', padx=4, pady=4 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__scbw_import_cancel_button, relief='raised', background=self.import_background)
            a_cancel_btn.pack( side='right', padx=4, pady=4 )

        self.w_scb_window.update()

    # ####################### __scbw_set_window_size ########################
    def __scbw_set_window_size( self):
        """ Set the size of the configuration windows (+16 for any line added in a_middle_text) """
        if self.s_platform == "Linux":
            self.i_width = 968
            self.i_height = 374
        elif self.s_platform == "Darwin":
            self.i_width = 968
            self.i_height = 306
        elif self.s_platform == "Windows":
            self.i_width = 968
            self.i_height = 376

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

            self.a_pallet_image = a_original_image
            self.a_scb_cnvs = a_scb_cnvs
            self.i_index_in_a_scb_cnvs_rect_lst = i_index_in_a_scb_cnvs_rect_lst

            self.w_scb_window = Toplevel( w_parent_window)
            self.w_scb_window.lift( aboveThis=w_parent_window)
            # window dialog is on top of w_parent_window
            self.w_scb_window.grab_set()
            self.w_scb_window.focus_set()
            self.w_scb_window.configure( background=constant.BACKGROUD_COLOR_UI)

            self.w_scb_window.title( ' SCB edit ')

            self.__scbw_scb_block( a_original_image)
            # self.w_scb_window.update()
            self.__scbw_set_window_size()

            self.w_scb_window.mainloop()
            self.w_scb_window.destroy()

    # ####################### scbw_close_scb_window ########################
    def scbw_close_scb_window( self):
        """ Close the preference window """
        self.__scbw_import_cancel_button()
        self.w_scb_window.quit()
