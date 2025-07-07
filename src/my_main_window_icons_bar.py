#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This is an application to do modification of bmp file to prepare convertion to a AIIGS pic file.
#
# Copyright (C) 2023-2025 Renaud Malaval <renaud.malaval@free.fr>.
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

import os
import platform

from tkinter import Button
from PIL import Image

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_about_window import MyAboutWindow
from .my_import_window import MyImportPalletWindow
from .my_alert_window import MyAlertWindow
from .my_progress_bar_window import MyProgressBarWindow

from .my_tools import mt_open_file

# __name__ = "MyMainWindowIconsBar"

# ###############################################################################################
# #######========================= constant private =========================


# ###############################################################################################
# #######=========================     GUI     =========================
# ####################### MyMainWindowIconsBar ########################
class MyMainWindowIconsBar:
    """ Create the icon bar to the main Windows of the application. """

    # ####################### __init__ ########################
    def __init__( self, c_main_class, w_main_windows, list_application_info, a_top_frame_of_main_window):
        """
            All this parameters come from main()
            c_main_class : the class who manage w_main_windows
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
        self.c_alert_windows = MyAlertWindow( self.c_main_class, list_application_info)
        self.s_filename = None
        self.a_original_image = None
        self.c_mains_image = None
        self.imported_pallet_lst = []
        self.i_selected_pallet_in_main_windows = -1

    # ####################### __mwib_ensure_bmp_extension ########################
    def __mwib_ensure_bmp_extension(self, s_filename) -> str:
        if not s_filename.lower().endswith( '.bmp'):
            root, _ = os.path.splitext( s_filename)
            return root + ".bmp"
        return s_filename

    # ####################### __mwib_get_copy_of_image ########################
    def __mwib_get_copy_of_image( self, s_filename, a_image) -> Image:
        """ Create a copy of the image with additional attributes """
        a_new_image = a_image.copy()
        if hasattr( a_image, "BITFIELDS"):
            a_new_image.BITFIELDS = a_image.BITFIELDS  # Copy BITFIELD attribute from img to a_image
        if hasattr( a_image, "COMPRESSIONS"):
            a_new_image.COMPRESSIONS = a_image.COMPRESSIONS  # Copy COMPRESSION attribute from img to a_image
        a_new_image.pathname = s_filename  # Add custom attribute to the image object
        a_new_image.format = a_image.format  # Add format attribute from img to a_image
        a_new_image.format_description = a_image.format_description  # Add format description attribute from img to a_image

        return a_new_image

    # ####################### __mwib_convert_bmp ########################
    def __mwib_convert_bmp( self, s_filename, a_image, b_do_all) -> Image:
        """ Convert bmp 4 bpp to 8 bpp """
        # converted_bmp = Image.new( 'P', (320, 200), color=0)
        a_org_pal_list = a_image.getpalette()
        i_number_of_colors = len( a_org_pal_list)
        if a_org_pal_list and i_number_of_colors:
            converted_bmp = self.__mwib_get_copy_of_image( s_filename, a_image)
            a_image = None  # Free the memory of the original image
            a_conv_pal_list = converted_bmp.getpalette()

            if b_do_all:
                # Copy the 1st pallet at index 0 to all 1 .. 16
                for _ in range( 1, 16, 1):
                    for i_index in range( 0, i_number_of_colors, 1):
                        a_conv_pal_list.append( a_org_pal_list[i_index])
                converted_bmp.putpalette( a_conv_pal_list, rawmode='RGB')
                a_conv_pal_list = converted_bmp.getpalette()
            # print( "\na_org_pal_list= " + str( len( a_org_pal_list)) + "   a_conv_pal_list= " + str( len( a_conv_pal_list)))

            # Debug : use an another name to save it and using it
            # s_path = os.path.dirname( s_filename)
            # s_filename = s_path + os.sep + "beach1.bmp"

            s_bmp_filename = self.__mwib_ensure_bmp_extension( s_filename)
            old_file = s_bmp_filename + ".old"
            # If file exists, rename to .old
            if os.path.exists( s_bmp_filename):
                if os.path.exists( old_file):
                    os.remove( old_file)
                os.rename( s_bmp_filename, old_file)

            print( 'mwib_convert_bmp() : Saving : ' + s_bmp_filename)
            try:
                converted_bmp.save( s_bmp_filename, 'BMP')
                # Save succeeded, remove .old
                if os.path.exists( old_file):
                    os.remove( old_file)
                print( "mwib_convert_bmp() : File saved successfully.")
            # pylint: disable=broad-exception-caught
            except Exception as error:
                # pylint: enable=broad-exception-caught
                print( f"Error saving file: {error}")
                # Restore original file on any error during save
                if os.path.exists( old_file):
                    if os.path.exists( s_bmp_filename):
                        os.remove( s_bmp_filename)
                    os.rename( old_file, s_bmp_filename)
                print( "mwib_convert_bmp() : Original file restored.")

            # Open the image file
            with Image.open( s_bmp_filename) as a_img:
                a_image = self.__mwib_get_copy_of_image( s_bmp_filename, a_img)

            a_img = None
            print( 'mwib_convert_bmp() : Upgraded to 8 bpp : ' + s_bmp_filename)
        else:
            self.c_alert_windows.aw_create_alert_window( 1, "BMP file not compatible", "This bmp file don't have 256 colors (1 or 2 bpp).")

        return a_image

    # ####################### __mwib_select_load_bmp ########################
    def __mwib_select_load_bmp( self) -> str:
        """ Select the bmp file to use """
        return mt_open_file( self.w_main_windows, self.c_main_class)

    # ####################### __mwib_load_check_bmp ########################
    def __mwib_load_check_bmp( self, s_filename) -> tuple:
        """ Check size and number of color in bmp """
        a_image = None
        print( 'mwib_load_check_bmp() : Loading : ' + s_filename)
        # Open the image file
        with Image.open( s_filename) as a_img:
            a_image = self.__mwib_get_copy_of_image( s_filename, a_img)

        a_img = None  # Free the memory of the original image
        # Now the file is closed, but a_image is a full in-memory image
        if a_image and s_filename:
            i_width, i_height = a_image.size
            # resize the original bmp from 320x200 to 640x400
            if i_width != 320 or i_height != 200:
                # messagebox.showerror( "BMP file not compatible", "The size of bmp file must be 320 x 200, for Apple II GS.", parent=self.w_main_windows )
                self.c_alert_windows.aw_create_alert_window( 1, "BMP file not compatible", "The size of bmp file must be 320 x 200, for Apple II GS.")
                a_image = None
                s_filename = None
            else:
                a_pallet_list = a_image.getpalette()
                if len( a_pallet_list) < 768:      # Less than 256 colors 2, 4 bpp
                    i_result = self.c_alert_windows.aw_create_alert_window( 4, "Question", "This bmp file don't have 256 colors (4 bpp is 16 colors).\nDo you agree improvement it?\n- just 8 bpp (16 / 256 colors)\n- 8 bpp and copy pallet (256 colors)\nThis write it to update it.")
                    if i_result == 1:
                        a_image = self.__mwib_convert_bmp( s_filename, a_image, True)
                    elif i_result == 3:
                        a_image = self.__mwib_convert_bmp( s_filename, a_image, False)
                    else:
                        a_image = None
                        s_filename = None
                elif len( a_pallet_list) > 768:      # More than 256 colors 16, 24 or 32 bpp
                    self.c_alert_windows.aw_create_alert_window( 3, "BMP file not compatible", "The bmp file have to much colors.\nConvert it, please.")
                    a_image = None
                    s_filename = None

                if a_image and s_filename:
                    # Check if the image have a maximum of 16 colors per line
                    for y in range(i_height):
                        color_set = set()
                        for x in range(i_width):
                            color_index = a_image.getpixel((x, y))
                            color_set.add(color_index)
                        if len(color_set) > 16:
                            self.c_alert_windows.aw_create_alert_window( 3, "BMP file not compatible", f"Line {y} has more than 16 colors ({len(color_set)} colors).")
                            a_image = None
                            s_filename = None
                            break

        return s_filename, a_image

    # ####################### __mwib_dump_pallet_bmp ########################
    # def __mwib_dump_pallet_bmp( self):
    #     """ dump the pallet of the current image a_work_img """
    #     if self.a_original_image:
    #         a_pallet_list = self.a_original_image.getpalette()
    #         print( 'Pallet :')
    #         i_to = 0
    #         for i_loop in range( 0, 16, 1):
    #             i_from = i_to
    #             i_to = i_to + 48
    #             if i_loop < 10:
    #                 s_my_hex = "0" + str( i_loop) + " "
    #             else:
    #                 s_my_hex = str( i_loop) + " "

    #             for i_index in range( i_from, i_to, 3):
    #                 s_red = f'{a_pallet_list[ i_index]:02X}'
    #                 s_green = f'{a_pallet_list[ i_index + 1]:02X}'
    #                 s_blue = f'{a_pallet_list[ i_index + 2]:02X}'
    #                 s_my_hex = s_my_hex + "#" + s_red + s_green + s_blue + " "

    #             print( s_my_hex)

    # ####################### __mwib_validate_scb_in_bmp ########################
    def __mwib_validate_scb_in_bmp( self):
        """ Check bitmap to synchronize all lines to use right scb """

        self.w_front_window = MyProgressBarWindow( self.c_main_class, self.a_list_application_info)
        self.w_front_window.pbw_create_progres_bar_window( 200, "BMP pallet checking", "Check bitmap to synchronize all lines to use right SCB.")
        # print()
        # self.__dump_pallet_bmp()
        # print()
        # a_pallet_list = self.a_original_image.getpalette()

        self.w_front_window.pbw_progress_bar_start()
        for i_picture_line_y in range( 0, 200, 1):
            i_small_index = 255
            # i_small_pos_x = 255
            i_big_index = 0
            # i_big_pos_x = 0
            self.w_front_window.pbw_progress_bar_step()
            # - parse a line to get the bigger index of a pallet to compute the right line of color to use (SCB)
            for i_loop in range( 0, 320, 1):
                i_first_color_offset = self.a_original_image.getpixel( ( i_loop, i_picture_line_y))
                i_big_index = max(i_big_index, i_first_color_offset)
                i_small_index = min(i_small_index, i_first_color_offset)

            if int( i_big_index / 16) != int( i_small_index / 16):
                # - re-pare the line to upgrade each index to have the same SCB on all the line
                # print( "#" + f"{i_picture_line_y:03d}" + " i_big_index   = " + str( i_big_index) + " line  Y = " + str( int( i_big_index / 16)) + " index X = " + str( i_big_index - int( i_big_index / 16) * 16) + \
                #     " at pox X = " + str( i_big_pos_x) )
                # print( "    " + " i_small_index = " + str( i_small_index) + " line  Y = " + str( int( i_small_index / 16)) + " index X = " + str( i_small_index - int( i_small_index / 16) * 16) + \
                #     " at pox X = " + str( i_small_pos_x) )
                for i_index in range( 0, 320, 1):
                    i_current_index = self.a_original_image.getpixel( ( i_index, i_picture_line_y))
                    if int( i_current_index / 16) != int( i_big_index / 16):
                        # print( "    " + str( i_current_index) )
                        while int( i_current_index / 16) != int( i_big_index / 16):
                            i_current_index += 16
                        if int( i_current_index / 16) == int( i_big_index / 16):
                            # print( "    " + str( i_current_index) )
                            self.a_original_image.putpixel( ( i_index, i_picture_line_y), i_current_index)
                        else:
                            print( "BUG : index is after the big i_big_index")

        self.w_front_window.pbw_progress_bar_stop()
        self.w_front_window = None

    # ####################### __about_dialog_box ########################
    def __mwib_about_dialog_box( self):
        """ Button about of the main window """
        self.c_the_log.add_string_to_log( 'Do about')
        self.w_front_window = MyAboutWindow( self.c_main_class, self.a_list_application_info)
        self.w_front_window.aw_create_about_window()
        self.w_front_window = None

    # ####################### __mwib_save_box ########################
    def __mwib_save_box( self):
        """ Button save the picture modified """
        a_main_picture = self.c_mains_image.mwi_get_original_image()
        if a_main_picture:
            self.c_the_log.add_string_to_log( 'Do save picture')
            self.c_main_class.mw_save_picture()

    # ####################### __mwib_import_pallet_box ########################
    def __mwib_import_pallet_box( self):
        """ Button import pallet from an another picture """
        if self.s_filename and self.a_original_image:
            self.c_the_log.add_string_to_log( 'Do import pallet of picture')
            s_filename = self.__mwib_select_load_bmp()
            if s_filename:
                s_filename, a_image = self.__mwib_load_check_bmp( s_filename)
                if s_filename and a_image:
                    self.w_front_window = MyImportPalletWindow( self.c_main_class, self.c_mains_image, self.mwib_get_get_path_filename())
                    self.w_front_window.ipw_create_import_window( a_image, self.a_original_image, self.i_selected_pallet_in_main_windows)
                    self.w_front_window = None

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
    def mwib_create_top_bar_icons( self, i_row_line) -> int:
        """ Design the top row for the main windows """
        # print( "mwib_create_top_bar_icons() color : " + self.w_main_windows['background'])

        s_button_style = 'flat'
        i_column = 0
        if self.s_platform == "Darwin":
            a_button_about = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_about_photo(), compound='center', command=self.__mwib_about_dialog_box, relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_open = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_open_photo(), compound='center', command=self.mwib_open_box, relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_save = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_save_photo(), compound='center', command=self.__mwib_save_box, relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_pallet = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_color_pallet_photo(), compound='center', command=self.__mwib_import_pallet_box, relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_cursor = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_cursor_photo(), compound='center', command='', relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
        elif self.s_platform == "Linux":
            a_button_about = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_about_photo(), compound='center', command=self.__mwib_about_dialog_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_open = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_open_photo(), compound='center', command=self.mwib_open_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_save = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_save_photo(), compound='center', command=self.__mwib_save_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_pallet = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_color_pallet_photo(), compound='center', command=self.__mwib_import_pallet_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_cursor = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_cursor_photo(), compound='center', command='', relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
        else:
            a_button_about = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_about_photo(), compound='center', command=self.__mwib_about_dialog_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
            a_button_open = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_open_photo(), compound='center', command=self.mwib_open_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
            a_button_save = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_save_photo(), compound='center', command=self.__mwib_save_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
            a_button_pallet = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_color_pallet_photo(), compound='center', command=self.__mwib_import_pallet_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
            a_button_cursor = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_cursor_photo(), compound='center', command='', relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)

        a_button_about.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse' )
        i_column += 1
        a_button_open.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'
        i_column += 1
        a_button_save.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'
        i_column += 1
        a_button_pallet.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'
        i_column += 1
        a_button_cursor.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'

        i_row_line += 1
        return i_row_line

    # ####################### mwib_create_left_bar_icons ########################
    def mwib_create_left_bar_icons( self, i_row_line) -> int:
        """ Design the left row for the main windows """
        # print( "mwib_create_left_bar_icons() color : " + self.w_main_windows['background'])

        s_button_style = 'flat'
        i_column = 0
        i_row_line = 0
        if self.s_platform == "Darwin":
            a_button_about = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_about_photo(), compound='center', command=self.__mwib_about_dialog_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_open = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_open_photo(), compound='center', command=self.mwib_open_box, relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_save = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_save_photo(), compound='center', command=self.__mwib_save_box, relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_pallet = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_color_pallet_photo(), compound='center', command=self.__mwib_import_pallet_box, relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_cursor = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_cursor_photo(), compound='center', command='', relief=s_button_style, highlightbackground=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
        elif self.s_platform == "Linux":
            a_button_about = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_about_photo(), compound='center', command=self.__mwib_about_dialog_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_open = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_open_photo(), compound='center', command=self.mwib_open_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_save = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_save_photo(), compound='center', command=self.__mwib_save_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_pallet = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_color_pallet_photo(), compound='center', command=self.__mwib_import_pallet_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
            a_button_cursor = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_cursor_photo(), compound='center', command='', relief=s_button_style, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
        else:
            a_button_about = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_about_photo(), compound='center', command=self.__mwib_about_dialog_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
            a_button_open = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_open_photo(), compound='center', command=self.mwib_open_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
            a_button_save = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_save_photo(), compound='center', command=self.__mwib_save_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
            a_button_pallet = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_color_pallet_photo(), compound='center', command=self.__mwib_import_pallet_box, relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)
            a_button_cursor = Button( self.a_top_frame_of_main_window, width=85, height=85, image=self.c_the_icons.get_cursor_photo(), compound='center', command='', relief=s_button_style, background=constant.BACKGROUD_COLOR_UI)

        a_button_about.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse' )
        i_row_line += 1
        a_button_open.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'
        i_row_line += 1
        a_button_save.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'
        i_row_line += 1
        a_button_pallet.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'
        i_row_line += 1
        a_button_cursor.grid( row=i_row_line, column=i_column, padx=2, pady=2, sticky='nse')  # , sticky='nse'

        i_row_line += 1
        return i_row_line

    # ####################### mwib_open_box ########################
    def mwib_open_box( self, filepathname=None):
        """ Button load of the main window """
        self.c_the_log.add_string_to_log( 'Do load picture')
        if filepathname:
            self.s_filename, self.a_original_image = self.__mwib_load_check_bmp( filepathname)
        else:
            self.s_filename = self.__mwib_select_load_bmp()
            self.s_filename, self.a_original_image = self.__mwib_load_check_bmp( self.s_filename)

        if self.s_filename and self.a_original_image:
            # Display image already in 8 bpp or a converted to 8 bpp
            self.c_main_class.mw_update_main_window( self.s_filename, self.a_original_image)
            self.w_main_windows.update()
            self.c_mains_image.mwi_click_in_picture_center()
            # Increase valeur index to use the right line to be SCB ready
            self.__mwib_validate_scb_in_bmp()
            self.c_main_class.mw_update_main_window( self.s_filename, self.a_original_image)
            self.w_main_windows.update()
            self.c_mains_image.mwi_click_in_picture_center()

    # ####################### mwib_get_frame ########################
    def mwib_get_frame( self) -> object:
        """ Return frame to be able to add new elements """
        return self.a_top_frame_of_main_window

    # ####################### mwib_get_get_path_filename ########################
    def mwib_get_get_path_filename( self) -> str:
        """ Return thye complete file pathname of the last image loaded """
        return self.s_filename

    # ####################### mwib_get_get_pathname ########################
    def mwib_get_get_pathname( self) -> str:
        """ Return the complete pathname of the last image loaded """
        if self.s_filename:
            s_pathname = os.path.dirname( os.path.abspath(self.s_filename))
        else:
            s_pathname = os.getcwd()
            s_pathname, _ = os.path.split(s_pathname)
        return s_pathname

    # ####################### mwib_get_get_path_filename ########################
    def mwib_set_main_image( self, c_mains_image):
        """ Return thye complete file pathname of the last image loaded """
        self.c_mains_image = c_mains_image

    # ####################### mwib_set_selected_pallet_line ########################
    def mwib_set_selected_pallet_line( self, i_selected_pallet):
        """ Return thye complete file pathname of the last image loaded """
        self.i_selected_pallet_in_main_windows = i_selected_pallet
