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

""" Module de gestion import palette de l'application """

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

# __name__ = "MyImportPalletWindow"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= Import Pallet Dialogs Window =========================
class MyImportPalletWindow:
    """ Create the import pallet Windows of the application """
    # pylint: disable=too-many-instance-attributes
    # number is reasonable in this case these are all the icons of the main windows and the application icons

    answer_cancel = 0
    answer_ok = 1
    a_list_device_model = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']

    # ####################### __init__ ########################
    def __init__( self, a_the_main_window, a_main_window_image, file_path_name):
        """
            all this parameter are created in main()
            a_main_window : the parent windows
            a_main_window_image : the top right part class who manage the iamge
        """
        self.a_main_window = a_the_main_window
        self.a_main_window_image = a_main_window_image
        self.s_original_filename = file_path_name
        self.c_the_log = MyLogAnUsage( None)
        self.c_the_icons = MyIconPictures( None)
        self.s_platform = platform.system()
        self.w_import_window = None
        self.a_work_img = None

        self.a_pallet_button_lst = []
        self.a_selected_info_lbl = None
        self.a_pallet_image = None
        self.a_list_device_combo = None

        self.i_height = 0
        self.i_width = 0
        self.i_position_x = 0
        self.i_position_y = 0
        self.import_background = 'darkgray'
        self.color_radio_button = IntVar()
        self.i_selected_pallet = -1                     # source of index pallet to copy
        self.i_selected_pallet_in_main_windows = -1     # target of destination index
        self.imported_pallet_lst = []

    # ####################### __scbw_do_leave_import_dialog ########################
    def __scbw_do_leave_import_dialog( self):
        """ Do commun stuff when press button ok or cancel on the scb window """
        self.w_import_window.grab_release()
        self.w_import_window.quit()
 
    # ####################### __ipw_import_ok_button ########################
    def __ipw_import_ok_button( self):
        """ Button ok of the import window """
        a_work_pallet_list = self.a_work_img.getpalette()

        self.imported_pallet_lst.clear()
        i_first_color_conponent_to_copy = int( self.a_list_device_combo.get()) * 16 * 3
        i_last_color_conponent_to_copy = i_first_color_conponent_to_copy + ( 16 * 3)

        a_pallet_list = self.a_pallet_image.getpalette()
        i_index = self.i_selected_pallet * 16 * 3
        for i_loop in range( 0, len( a_work_pallet_list), 1):
            if i_loop in range( i_first_color_conponent_to_copy, i_last_color_conponent_to_copy):
                # Copy of 16 colors (3 integers per color)
                self.imported_pallet_lst.append( a_pallet_list[i_index])
                i_index += 1
            else:
                # Copy 768 colors - 48 (3 integers per color)
                self.imported_pallet_lst.append( a_work_pallet_list[i_loop])

        self.a_work_img.putpalette( self.imported_pallet_lst)

        self.__scbw_do_leave_import_dialog()
        self.c_the_log.add_string_to_log( 'Do import pallet close with ok')
        self.a_main_window.mw_update_main_window( self.s_original_filename, self.a_work_img)
        w_parent_window = self.a_main_window.mw_get_main_window()
        w_parent_window.update()
        self.a_main_window_image.mwi_click_in_picture_center()

    # ####################### __ipw_import_cancel_button ########################
    def __ipw_import_cancel_button( self):
        """ Button cancel of the import window """
        self.imported_pallet_lst = None
        self.i_selected_pallet = -1
        self.__scbw_do_leave_import_dialog()
        self.c_the_log.add_string_to_log( 'Do import pallet close with cancel')

    # ####################### __ipw_select_color_rad_btn ########################
    def __ipw_select_color_rad_btn( self, i_offset):
        """ Select the radio button color in the pallet """
        self.a_pallet_button_lst[i_offset].select()
        if i_offset > 15:
            self.i_selected_pallet = int( i_offset / 16)
            self.a_selected_info_lbl.configure( text="\nThe selected line is " + str( self.i_selected_pallet) + ". On click Ok it update pallet : ")
        else:
            self.i_selected_pallet = 0
            self.a_selected_info_lbl.configure( text="\nThe selected line is 0. On click Ok it update pallet : ")

    # ####################### __ipw_import_block ########################
    def __ipw_import_block( self, a_image):
        """ Create a about dialog """
        # global s_device_information
        top_frame = tk_gui.Frame( self.w_import_window, relief='flat', background=constant.BACKGROUD_COLOR_UI)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        button_frame = tk_gui.Frame( self.w_import_window, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR, width=self.i_width, height=336)
        button_frame.pack( side='bottom', fill='x', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        # #### TOP #####
        i_index_base_block = 0
        i_index_base_column = 0
        a_render = ImageTk.PhotoImage( a_image)
        if self.s_platform == "Linux":
            a_picture_lbl = Label( top_frame, padx=0, pady=0, image=a_render, height=200, anchor='center', background=constant.BACKGROUD_COLOR_UI, borderwidth=0, compound="center", highlightthickness=0)
        else:
            a_picture_lbl = Label( top_frame, padx=0, pady=0, image=a_render, height=200, anchor='center', background=constant.BACKGROUD_COLOR_UI, borderwidth=0, compound="center", highlightthickness=0)
        a_picture_lbl.grid( row=i_index_base_block, column=i_index_base_column, columnspan=16, sticky='ew')
        a_picture_lbl.photo = a_render

        i_index_base_block += 1
        a_label = Label( top_frame, text="Select a color in the line to select copy of it:\n", height=2, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='white')
        a_label.grid( row=i_index_base_block, column=i_index_base_column, columnspan=11, sticky='wns', padx=2, pady=0)

        # Table of color button for the pallet
        a_pallet_list = a_image.getpalette()
        i_index_base_block += 1
        i_to = 0
        i_index = 0
        for i_loop in range( 0, 16, 1):
            i_from = i_to
            i_to = i_to + 48
            # First element of the line is its number
            a_label = Label( top_frame, text=str(i_loop), background=constant.BACKGROUD_COLOR_UI, foreground='white', font=font.Font( size=6))  # Creating a font object with little size for color buttons to reduce their size
            # if self.s_platform == "Darwin":
            #     a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            # else:
            a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            i_index_base_column += 1
            # create list of line of radio button and add it in a list to be accessible
            for i_value in range( i_from, i_to, 3):
                a_color_btn_rad = Radiobutton( top_frame, text='', indicatoron = 0, width=8, height=1, variable=self.color_radio_button, value=i_index, background=constant.BACKGROUD_COLOR_UI, font=font.Font( size=3))    # Creating a font object with little size for color buttons to reduce their size
                if self.s_platform in [ "Darwin", "Linux" ]:
                    a_color_btn_rad.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=2)
                else:
                    a_color_btn_rad.grid( row=i_index_base_block, column=i_index_base_column, padx=4, pady=2)
                a_color_btn_rad.configure( background="#" + f'{a_pallet_list[ i_index]:02X}' + f'{a_pallet_list[ i_index + 1]:02X}' + f'{a_pallet_list[ i_index + 2]:02X}')     # '# red green blue'
                a_color_btn_rad.configure( command=partial( self.__ipw_select_color_rad_btn, int( i_value / 3)))
                self.a_pallet_button_lst.append( a_color_btn_rad)
                i_index_base_column += 1
                i_index += 3

            i_index_base_column = 0
            i_index_base_block += 1

        i_index_base_column = 0
        self.a_selected_info_lbl = Label( top_frame, text="The selected line is 0. On click Ok it update pallet:", height=2, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='white')
        self.a_selected_info_lbl.grid( row=i_index_base_block, column=i_index_base_column, columnspan=11, sticky='wns', padx=2, pady=0)

        i_index_base_column += 11
        # Création de la Combobox via la méthode ttk.Combobox()
        self.a_list_device_combo = Combobox( top_frame, values=self.a_list_device_model, width=4, state="readonly")
        self.a_list_device_combo.grid( row=i_index_base_block, column=i_index_base_column, columnspan=2, padx=2, pady=0)
        # Choisir l'élément qui s'affiche par défaut
        if self.i_selected_pallet_in_main_windows != -1:
            self.a_list_device_combo.current( self.i_selected_pallet_in_main_windows)
        else:
            self.a_list_device_combo.current( 0)

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 2 charracters
        if self.s_platform == "Darwin":
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__ipw_import_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=2, pady=2 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__ipw_import_cancel_button, relief='raised', background=self.import_background)
            a_cancel_btn.pack( side='right', padx=2, pady=2 )
        else:
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__ipw_import_ok_button, relief='raised', background=self.import_background)
            a_ok_btn.pack( side='right', padx=4, pady=4 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__ipw_import_cancel_button, relief='raised', background=self.import_background)
            a_cancel_btn.pack( side='right', padx=4, pady=4 )

        self.w_import_window.update()
        self.__ipw_select_color_rad_btn( 0)

    # ####################### __ipw_set_window_size ########################
    def __ipw_set_window_size( self):
        """ Set the size of the configuration windows (+16 for any line added in a_middle_text) """
        if self.s_platform == "Linux":
            self.i_width = 592
            self.i_height = 574
        elif self.s_platform == "Darwin":
            self.i_width = 552
            self.i_height = 506
        elif self.s_platform == "Windows":
            self.i_width = 592
            self.i_height = 556

        self.i_position_x = self.a_main_window.mw_get_main_window_pos_x() + int((self.a_main_window.mw_get_main_window_width() - self.i_width) / 2)
        self.i_position_y = self.a_main_window.mw_get_main_window_pos_y() + int((self.a_main_window.mw_get_main_window_height() - self.i_height) / 2)

        s_windows_size_and_position = ( str( self.i_width) + 'x' + str( self.i_height) + '+' + str( self.i_position_x) + '+' + str( self.i_position_y))
        self.w_import_window.geometry( s_windows_size_and_position)  # dimension + position x/y a l'ouverture

        # lock resize of main window
        self.w_import_window.minsize( self.i_width, self.i_height)
        self.w_import_window.maxsize( self.i_width, self.i_height)
        # no resize for both directions
        self.w_import_window.resizable( False, False)
        self.w_import_window.iconphoto( True, self.c_the_icons.get_app_photo())

        print( '\nipw_set_window_size() : geometry  ' + s_windows_size_and_position + '\n')

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

    # ####################### ipw_create_import_window ########################
    def ipw_create_import_window( self, a_pallet_image, a_work_img, i_selected_pallet_in_main_windows):
        """ Design the import pallet box dialog """
        if a_pallet_image and a_work_img:
            self.c_the_log.add_string_to_log( 'ipw_create_import_window()')
            w_parent_window = self.a_main_window.mw_get_main_window()
            self.a_pallet_image = a_pallet_image
            self.a_work_img = a_work_img
            self.i_selected_pallet_in_main_windows = i_selected_pallet_in_main_windows

            self.w_import_window = Toplevel( w_parent_window)
            self.w_import_window.lift( aboveThis=w_parent_window)
            # window dialog is on top of w_parent_window
            self.w_import_window.grab_set()
            self.w_import_window.focus_set()
            self.w_import_window.configure( background=constant.BACKGROUD_COLOR_UI)
            self.w_import_window.title( ' Import pallet ')

            self.__ipw_import_block( a_pallet_image)
            self.w_import_window.update()
            self.__ipw_set_window_size()

            self.w_import_window.mainloop()
            self.w_import_window.destroy()

    # ####################### ipw_close_import_window ########################
    def ipw_close_import_window( self):
        """ Close the preference window """
        self.__ipw_import_cancel_button()
