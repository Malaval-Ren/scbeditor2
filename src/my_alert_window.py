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

""" Module de gestion alertes de l'application """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import platform

import tkinter as tk_gui
from tkinter import Label, Button, Toplevel, font

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures

# __name__ = "MyAlertWindow"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= About Dialogs Window =========================
class MyAlertWindow:
    """ Create the alert windows of the application """
    # pylint: disable=too-many-instance-attributes
    # number is reasonable in this case these are all the icons of the main windows and the application icons

    answer_cancel = 0
    answer_ok = 1
    answer_other = 2

    # ####################### __init__ ########################
    def __init__( self, c_the_main_window, list_application_info):
        """
            all this parameter are created in main()
            w_parent_windows : the parent windows
        """
        self.c_the_main_window = c_the_main_window
        self.a_list_application_info = list_application_info
        self.c_the_log = MyLogAnUsage( None)
        self.c_the_icons = MyIconPictures( None)
        self.s_platform = platform.system()
        self.w_alert_window = None
        self.i_height = 0
        self.i_width = 0
        self.i_position_x = 0
        self.i_position_y = 0
        self.alert_background = 'darkgray'
        self.answers = self.answer_cancel

    # ####################### __aw_alert_ok_button ########################
    def __aw_alert_ok_button( self):
        """ Button ok of the alert window """
        self.w_alert_window.grab_release()
        # self.w_alert_window.destroy()
        self.w_alert_window.quit()
        self.c_the_log.add_string_to_log( 'Do alert close with ok')
        self.answers = self.answer_ok

    # ####################### __aw_alert_cancel_button ########################
    def __aw_alert_cancel_button( self):
        """ Button cancel of the alert window """
        self.w_alert_window.grab_release()
        # self.w_alert_window.destroy()
        self.w_alert_window.quit()
        self.c_the_log.add_string_to_log( 'Do alert close with cancel')
        self.answers = self.answer_cancel

    # ####################### __aw_alert_block ########################
    # URL : https://stackoverflow.com/questions/53827364/how-to-create-a-multiple-labels-dynamically-in-tkinter
    def __aw_error_block( self, s_message):
        """ Create a error dialog """
        # global s_device_information
        top_frame = tk_gui.Frame( self.w_alert_window, relief='flat', background=self.alert_background)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        button_frame = tk_gui.Frame( self.w_alert_window, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR, width=self.i_width, height=336)
        button_frame.pack( side='bottom', fill='x', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        # #### TOP LEFT #####
        _a_error_photo = self.c_the_icons.get_error_photo()
        top_left_frame = tk_gui.Frame( top_frame, relief='flat', background=self.alert_background, width=_a_error_photo.width(), height=_a_error_photo.height())   # darkgray or light grey
        top_left_frame.pack( side='left', fill='y', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        a_name_photo_label = Label( top_left_frame, image=_a_error_photo, background=self.alert_background, anchor='center')  # background='darkgray' or 'light grey' == self.about_background
        a_name_photo_label.grid( row=1, column=1, padx=4, pady=4)

        # #### TOP RIGHT #####
        a_font_label = font.Font( size=18)
        a_alert_text_label = Label( top_left_frame, text=s_message, wraplength=320, justify='left', background=self.alert_background, foreground='white', anchor='w', font=a_font_label)  # background='darkgray' or 'light grey' == self.about_background
        a_alert_text_label.grid( row=1, column=2, padx=4, pady=4, sticky='w')

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 2 charracters
        Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_ok_button, background=self.alert_background).pack( side='right', padx=4, pady=4 )

        self.w_alert_window.update()

    # ####################### __aw_question_block ########################
    # URL : https://stackoverflow.com/questions/53827364/how-to-create-a-multiple-labels-dynamically-in-tkinter
    def __aw_question_block( self, s_message):
        """ Create a error dialog """
        # global s_device_information
        top_frame = tk_gui.Frame( self.w_alert_window, relief='flat', background=self.alert_background)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        button_frame = tk_gui.Frame( self.w_alert_window, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR, width=self.i_width, height=336)
        button_frame.pack( side='bottom', fill='x', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        # #### TOP LEFT #####
        _a_error_photo = self.c_the_icons.get_question_photo()
        top_left_frame = tk_gui.Frame( top_frame, relief='flat', background=self.alert_background, width=_a_error_photo.width(), height=_a_error_photo.height())   # darkgray or light grey
        top_left_frame.pack( side='left', fill='y', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        a_name_photo_label = Label( top_left_frame, image=_a_error_photo, background=self.alert_background, anchor='center')  # background='darkgray' or 'light grey' == self.about_background
        a_name_photo_label.grid( row=1, column=1, padx=4, pady=4)

        # #### TOP RIGHT #####
        a_font_label = font.Font( size=18)
        a_alert_text_label = Label( top_left_frame, text=s_message, wraplength=320, justify='left', background=self.alert_background, foreground='white', anchor='w', font=a_font_label)  # background='darkgray' or 'light grey' == self.about_background
        a_alert_text_label.grid( row=1, column=2, padx=4, pady=4, sticky='w')

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 2 charracters
        if self.s_platform == "Darwin":
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=2, pady=2 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_cancel_button, relief='raised', background=self.alert_background)
            a_cancel_btn.pack( side='right', padx=2, pady=2 )
        else:
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=4, pady=4 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_cancel_button, relief='raised', background=self.alert_background)
            a_cancel_btn.pack( side='right', padx=4, pady=4 )

        self.w_alert_window.update()

    # ####################### __aw_warning_block ########################
    # URL : https://stackoverflow.com/questions/53827364/how-to-create-a-multiple-labels-dynamically-in-tkinter
    def __aw_warning_block( self, s_message):
        """ Create a error dialog """
        # global s_device_information
        top_frame = tk_gui.Frame( self.w_alert_window, relief='flat', background=self.alert_background)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        button_frame = tk_gui.Frame( self.w_alert_window, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR, width=self.i_width, height=336)
        button_frame.pack( side='bottom', fill='x', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        # #### TOP LEFT #####
        _a_error_photo = self.c_the_icons.get_warning_photo()
        top_left_frame = tk_gui.Frame( top_frame, relief='flat', background=self.alert_background, width=_a_error_photo.width(), height=_a_error_photo.height())   # darkgray or light grey
        top_left_frame.pack( side='left', fill='y', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        a_name_photo_label = Label( top_left_frame, image=_a_error_photo, background=self.alert_background, anchor='center')  # background='darkgray' or 'light grey' == self.about_background
        a_name_photo_label.grid( row=1, column=1, padx=4, pady=4)

        # #### TOP RIGHT #####
        a_font_label = font.Font( size=18)
        a_alert_text_label = Label( top_left_frame, text=s_message, wraplength=320, justify='left', background=self.alert_background, foreground='white', anchor='w', font=a_font_label)  # background='darkgray' or 'light grey' == self.about_background
        a_alert_text_label.grid( row=1, column=2, padx=4, pady=4, sticky='w')

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 2 charracters
        if self.s_platform == "Darwin":
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=2, pady=2 )
        else:
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_ok_button, relief='raised', background=self.alert_background)
            a_ok_btn.pack( side='right', padx=4, pady=4 )

        self.w_alert_window.update()

    # ####################### __aw_alert_block ########################
    # URL : https://stackoverflow.com/questions/53827364/how-to-create-a-multiple-labels-dynamically-in-tkinter
    def __aw_alert_block( self, s_message):
        """ Create a alert dialog """
        # global s_device_information
        top_frame = tk_gui.Frame( self.w_alert_window, relief='flat', background=self.alert_background)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        button_frame = tk_gui.Frame( self.w_alert_window, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR, width=self.i_width, height=336)
        button_frame.pack( side='bottom', fill='x', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        # #### TOP LEFT #####
        _a_about_photo = self.c_the_icons.get_about_photo()
        top_left_frame = tk_gui.Frame( top_frame, relief='flat', background=self.alert_background, width=_a_about_photo.width(), height=_a_about_photo.height())   # darkgray or light grey
        top_left_frame.pack( side='left', fill='y', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        a_name_photo_label = Label( top_left_frame, image=_a_about_photo, background=self.alert_background, anchor='center')  # background='darkgray' or 'light grey' == self.about_background
        a_name_photo_label.grid( row=1, column=1, padx=4, pady=4)

        # #### TOP RIGHT #####
        a_alert_text_label = Label( top_left_frame, text=s_message, background='light grey', foreground='black', anchor='center')  # background='darkgray' or 'light grey' == self.about_background
        a_alert_text_label.grid( row=1, column=2, padx=4, pady=4, sticky='ewns')

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 2 charracters
        if self.s_platform == "Darwin":
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=2, pady=2 )
        else:
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__aw_alert_ok_button, relief='raised', background=self.alert_background)
            a_ok_btn.pack( side='right', padx=4, pady=4 )

        self.w_alert_window.update()

    # ####################### __aw_set_window_size ########################
    def __aw_set_window_size( self):
        """ Set the size of the configuration windows """
        self.i_width = 500
        self.i_height = 200
        self.i_position_x = self.c_the_main_window.mw_get_main_window_pos_x() + int((self.c_the_main_window.mw_get_main_window_width() - self.i_width) / 2)
        self.i_position_y = self.c_the_main_window.mw_get_main_window_pos_y() + int((self.c_the_main_window.mw_get_main_window_height() - self.i_height) / 2)

        s_windows_size_and_position = ( str( self.i_width) + 'x' + str( self.i_height) + '+' + str( self.i_position_x) + '+' + str( self.i_position_y))
        self.w_alert_window.geometry( s_windows_size_and_position)  # dimension + position x/y a l'ouverture

        # lock resize of main window
        self.w_alert_window.minsize( self.i_width, self.i_height)
        self.w_alert_window.maxsize( self.i_width, self.i_height)
        # no resize for both directions
        self.w_alert_window.resizable( False, False)
        self.w_alert_window.iconphoto( True, self.c_the_icons.get_app_photo())

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

    # ####################### aw_create_alert_window ########################
    def aw_create_alert_window( self, i_type, s_title, s_message):
        """ Design the about box dialog """
        w_parent_window = self.c_the_main_window.mw_get_main_window()
        self.w_alert_window = Toplevel( w_parent_window)
        self.w_alert_window.lift( aboveThis=w_parent_window)
        # window dialog is on top of w_parent_window
        self.w_alert_window.grab_set()
        self.w_alert_window.focus_set()
        self.w_alert_window.configure( background=self.alert_background)

        # ####################### disable_event ########################
        # disable click on the X on top right of the window
        def disable_event():
            self.__aw_alert_cancel_button()
            # pass

        self.w_alert_window.protocol( "WM_DELETE_WINDOW", disable_event)
        if s_title:
            self.w_alert_window.title( s_title)
        else:
            self.w_alert_window.title( ' Alert ')

        if i_type == 1:
            self.__aw_error_block( s_message)
        elif i_type == 2:
            self.__aw_question_block( s_message)
        elif i_type == 3:
            self.__aw_warning_block( s_message)
        else:
            self.__aw_alert_block( s_message)
        self.w_alert_window.update()
        self.__aw_set_window_size()

        self.w_alert_window.mainloop()
        self.w_alert_window.destroy()
        return self.answers

    # ####################### aw_close_alert_window ########################
    def aw_close_alert_window( self):
        """ Close the preference window """
        self.__aw_alert_cancel_button()
        self.w_alert_window.quit()
