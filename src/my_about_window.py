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

""" Module de gestion about de l'application """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import platform
import tkinter as tk_gui
from tkinter import Label, Button, Toplevel

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_widget_rich_text import MyRichTextWidget

# __name__ = "MyAboutWindow"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= About Dialogs Window =========================
class MyAboutWindow:
    """ Create the about Windows of the application """
    # pylint: disable=too-many-instance-attributes
    # number is reasonable in this case these are all the icons of the main windows and the application icons

    # ####################### __init__ ########################
    def __init__( self, c_the_main_window, list_application_info):
        """
            all this parameter are created in main()
            c_the_main_window : the parent windows
            list_application_info : all information about application
        """
        self.c_the_main_window = c_the_main_window
        self.a_list_application_info = list_application_info
        self.c_the_log = MyLogAnUsage( None)
        self.c_the_icons = MyIconPictures( None)
        self.s_platform = platform.system()
        self.w_about_window = None
        self.i_height = 0
        self.i_width = 0
        self.i_position_x = 0
        self.i_position_y = 0
        self.about_background = 'darkgray'

    # ####################### __aw_about_ok_button ########################
    def __aw_about_ok_button( self):
        """ Button ok of the about window """
        self.w_about_window.grab_release()
        self.w_about_window.destroy()
        self.c_the_log.add_string_to_log( 'Do about close')

    # ####################### __aw_about_cancel_button ########################
    def __aw_about_cancel_button( self):
        """ Button cancel of the about window """
        self.w_about_window.grab_release()
        self.w_about_window.destroy()

    # ####################### __aw_about_block ########################
    # URL : https://stackoverflow.com/questions/53827364/how-to-create-a-multiple-labels-dynamically-in-tkinter
    def __aw_about_block( self):
        """ Create a about dialog """
        # global s_device_information
        top_frame = tk_gui.Frame( self.w_about_window, relief='flat', background=self.about_background)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        button_frame = tk_gui.Frame( self.w_about_window, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR, width=self.i_width, height=336)
        button_frame.pack( side='bottom', fill='x', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        # #### TOP LEFT #####
        _a_about_photo = self.c_the_icons.get_about_photo()
        top_left_frame = tk_gui.Frame( top_frame, relief='flat', background=self.about_background, width=_a_about_photo.width(), height=_a_about_photo.height())   # darkgray or light grey
        top_left_frame.pack( side='left', fill='y', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        a_name_photo_label = Label( top_left_frame, image=_a_about_photo, background=self.about_background, anchor='center')  # background='darkgray' or 'light grey' == self.about_background
        a_name_photo_label.grid( row=1, column=1, padx=4, pady=4)

        _a_french_touch_photo = self.c_the_icons.get_french_photo()
        a_name_photo_label = Label( top_left_frame, image=_a_french_touch_photo, background=self.about_background, anchor='center')  # background='darkgray' or 'light grey' == self.about_background
        a_name_photo_label.grid( row=4, column=1, padx=4, pady=4)

        # #### TOP RIGHT #####
        __s_0_part = self.a_list_application_info[0] + '\n'
        __s_1_part = 'Version' + '\t' + self.a_list_application_info[5] + '\n' + \
            '\n' + \
            'Author' + '\t'
        __s_3_part = '\n' + \
            'Thanks to\n'
        __s_4_part = \
            '  ' + self.a_list_application_info[3][0] + ", " + self.a_list_application_info[3][1] + '\n' + \
            '  ' + self.a_list_application_info[3][2] + '\n' + \
            '  ' + self.a_list_application_info[3][3] + '\n' + \
            '  ' + self.a_list_application_info[3][4] + '\n'
        __s_7_part = '\n' + 'License' + '\n  ' + self.a_list_application_info[4] + '\n'
        __s_9_part = '  ' + self.a_list_application_info[2] + '\n  All rights reserved' + '\n' + \
            '\n' + \
            'eMail' + '\t' + self.a_list_application_info[7] + '\n'

        a_middle_text = MyRichTextWidget( top_left_frame, background=self.about_background, relief='sunken', tabs=('7c', '16c'), width=60, height=19)  # , exportselection=0, takefocus=0
        a_middle_text.insert( '2.0', __s_0_part, 'h1') # '1.0' -> line 1, character 0
        a_middle_text.insert( 'end', __s_1_part)
        a_middle_text.insert( 'end', self.a_list_application_info[1] + '\n', "bold-italic")
        a_middle_text.insert( 'end', __s_3_part)
        a_middle_text.insert( 'end', __s_4_part, "italic")
        a_middle_text.insert( 'end', __s_7_part)
        a_middle_text.insert( 'end', __s_9_part)
        a_middle_text.configure( state='disabled')
        a_middle_text.grid( row=1, rowspan=4, column=2, columnspan=3, padx=8, pady=8)

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 2 charracters
        if self.s_platform == "Darwin":
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound='center', command=self.__aw_about_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=2, pady=2 )
        else:
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound='center', command=self.__aw_about_ok_button, relief='raised', background=self.about_background)
            a_ok_btn.pack( side='right', padx=4, pady=4 )
        self.w_about_window.update()

    # ####################### __aw_set_window_size ########################
    def __aw_set_window_size( self):
        """ Set the size of the configuration windows (+16 for any line added in a_middle_text) """
        if self.s_platform == "Linux":
            self.i_width = 592
            self.i_height = 374
        elif self.s_platform == "Darwin":
            self.i_width = 552
            self.i_height = 306
        elif self.s_platform == "Windows":
            self.i_width = 592
            self.i_height = 356

        self.i_position_x = self.c_the_main_window.mw_get_main_window_pos_x() + int((self.c_the_main_window.mw_get_main_window_width() - self.i_width) / 2)
        self.i_position_y = self.c_the_main_window.mw_get_main_window_pos_y() + int((self.c_the_main_window.mw_get_main_window_height() - self.i_height) / 2)

        s_windows_size_and_position = ( str( self.i_width) + 'x' + str( self.i_height) + '+' + str( self.i_position_x) + '+' + str( self.i_position_y))
        self.w_about_window.geometry( s_windows_size_and_position)  # dimension + position x/y a l'ouverture

        # lock resize of main window
        self.w_about_window.minsize( self.i_width, self.i_height)
        self.w_about_window.maxsize( self.i_width, self.i_height)
        # no resize for both directions
        self.w_about_window.resizable( False, False)
        self.w_about_window.iconphoto( True, self.c_the_icons.get_app_photo())

        print( '\npw_set_window_size() : geometry  ' + s_windows_size_and_position + '\n')

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

    # ####################### aw_create_about_window ########################
    def aw_create_about_window( self):
        """ Design the about box dialog """
        print()
        print( 'aw_create_about_window() : ' )
        w_parent_window = self.c_the_main_window.mw_get_main_window()

        self.w_about_window = Toplevel( w_parent_window)
        self.w_about_window.lift( aboveThis=w_parent_window)
        # window dialog is on top of w_parent_window
        self.w_about_window.grab_set()
        self.w_about_window.focus_set()
        self.w_about_window.configure( background=self.about_background)

        # ####################### disable_event ########################
        # disable click on the X on top right of the window
        def disable_event():
            self.__aw_about_cancel_button()
            # pass

        self.w_about_window.protocol( "WM_DELETE_WINDOW", disable_event)
        self.w_about_window.title( ' About ')

        self.__aw_about_block()
        self.w_about_window.update()
        self.__aw_set_window_size()

        self.w_about_window.mainloop()
        # w_parent_window.focus_set()
        # print ('pw_create_preference_window() : exit' )

    # ####################### pw_close_preference_window ########################
    def aw_close_preference_window( self):
        """ Close the preference window """
        self.__aw_about_cancel_button()
        self.w_about_window.quit()
