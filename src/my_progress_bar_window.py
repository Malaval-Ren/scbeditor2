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

""" Module de gestion d'une progres bar de l'application """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import tkinter as tk_gui
from tkinter import Label, Button, Toplevel, font
from tkinter.ttk import Progressbar, Style

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures

# __name__ = "MyProgressBarWindow"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= Progress bar Dialogs Window =========================
class MyProgressBarWindow:
    """ Create the progres bar windows of the application """
    # pylint: disable=too-many-instance-attributes
    # number is reasonable in this case these are all the icons of the main windows and the application icons

    answer_cancel = 0
    answer_done = 1

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
        self.w_progres_bar_window = None
        self.i_height = 0
        self.i_width = 0
        self.i_position_x = 0
        self.i_position_y = 0
        self.progres_bar = None
        self.progres_bar_background = 'darkgray'
        self.value_lbl = None
        self.answers = self.answer_cancel
        self.i_number_of_step = 0
        self.f_value = 0.0

    # ####################### __pbw_alert_ok_button ########################
    def __pbw_alert_ok_button( self):
        """ Button ok of the alert window """
        self.w_progres_bar_window.grab_release()
        # self.w_progres_bar_window.destroy()
        self.w_progres_bar_window.quit()
        self.c_the_log.add_string_to_log( 'Do alert close with ok')
        self.answers = self.answer_done

    # ####################### __pbw_alert_cancel_button ########################
    def __pbw_progress_bar_cancel_button( self):
        """ Button cancel of the alert window """
        self.w_progres_bar_window.grab_release()
        # self.w_progres_bar_window.destroy()
        self.w_progres_bar_window.quit()
        self.c_the_log.add_string_to_log( 'Do alert close with cancel')
        self.answers = self.answer_cancel

    # ####################### pbw_create_progres_bar_window ########################
    def __pbw_update_progress_label( self):
        """ Uppdate progress label """
        return f"Current Progress: {self.progres_bar['value']:.2f}%"    # format 2 numbers after the '.'

    # ####################### pbw_create_progres_bar_window ########################
    def __pbw_progress( self):
        """ Do progression of the bar """
        if self.progres_bar['value'] < self.i_number_of_step:
            self.progres_bar['value'] = min( self.progres_bar['value'] + self.f_value, 200.00)
            self.value_lbl['text'] = self.__pbw_update_progress_label()
        # else:
        #     showinfo(message='The progress completed!')

    # ####################### __pbw_progres_bar_block ########################
    # URL : https://stackoverflow.com/questions/53827364/how-to-create-a-multiple-labels-dynamically-in-tkinter
    def __pbw_progres_bar_block( self, i_number_of_step, s_message):
        """ Create a progres bar dialog """

        # global s_device_information
        top_frame = tk_gui.Frame( self.w_progres_bar_window, relief='flat', background=self.progres_bar_background)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'
        button_frame = tk_gui.Frame( self.w_progres_bar_window, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR, width=self.i_width, height=336)
        button_frame.pack( side='bottom', fill='x', expand='no')   # fill :  must be 'none', 'x', 'y', or 'both'

        # #### TOP #####
        a_font_label = font.Font( size=12)
        a_alert_text_label = Label( top_frame, text=s_message, wraplength=480, justify='left', background=self.progres_bar_background, anchor='w', font=a_font_label)  # background='darkgray' or 'light grey' == self.about_background
        a_alert_text_label.grid( row=0, column=0, columnspan=2, padx=10, pady=8, sticky='we')

        self.i_number_of_step = float( i_number_of_step)
        self.f_value = float( (480 / i_number_of_step) / (i_number_of_step / 100) )

        s = Style()
        s.theme_use( 'clam')
        s.configure( "blue.Horizontal.TProgressbar", foreground=constant.COLOR_WINDOWS_MENU_BAR, background=constant.COLOR_WINDOWS_MENU_BAR)
        self.progres_bar = Progressbar( top_frame, style="blue.Horizontal.TProgressbar", orient='horizontal', mode='determinate', length=480, maximum=200)   # lightcolor=constant.COLOR_WINDOWS_MENU_BAR
        self.progres_bar.grid( row=1, column=0, columnspan=2, padx=10, pady=8, sticky='we')

        self.value_lbl = Label( top_frame, text=self.__pbw_update_progress_label(), background=self.progres_bar_background)
        self.value_lbl.grid( row=2, column=0, columnspan=2, pady=10)

        # #### BOTTOM #####
        # width size of a button is number of charracters 15 + 2 charracters
        w_button = Button( button_frame, text='Stop', width=constant.DEFAULT_BUTTON_WIDTH + 2, compound="c", command=self.__pbw_alert_ok_button, background=self.progres_bar_background)
        w_button.pack( side='right', padx=4, pady=4 )

        self.w_progres_bar_window.update()

    # ####################### __pbw_set_window_size ########################
    def __pbw_set_window_size( self):
        """ Set the size of the configuration windows """
        self.i_width = 500
        self.i_height = 150
        self.i_position_x = self.c_the_main_window.mw_get_main_window_pos_x() + int((self.c_the_main_window.mw_get_main_window_width() - self.i_width) / 2)
        self.i_position_y = self.c_the_main_window.mw_get_main_window_pos_y() + int((self.c_the_main_window.mw_get_main_window_height() - self.i_height) / 2)

        s_windows_size_and_position = ( str( self.i_width) + 'x' + str( self.i_height) + '+' + str( self.i_position_x) + '+' + str( self.i_position_y))
        self.w_progres_bar_window.geometry( s_windows_size_and_position)  # dimension + position x/y a l'ouverture

        # lock resize of main window
        self.w_progres_bar_window.minsize( self.i_width, self.i_height)
        self.w_progres_bar_window.maxsize( self.i_width, self.i_height)
        # no resize for both directions
        self.w_progres_bar_window.resizable( False, False)
        self.w_progres_bar_window.iconphoto( True, self.c_the_icons.get_app_photo())

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

    # ####################### pbw_create_progres_bar_window ########################
    def pbw_create_progres_bar_window( self, i_number_of_step, s_title, s_message):
        """ Design the about box dialog """
        w_parent_window = self.c_the_main_window.mw_get_main_window()
        self.w_progres_bar_window = Toplevel( w_parent_window)
        self.w_progres_bar_window.lift( aboveThis=w_parent_window)
        # window dialog is on top of w_parent_window
        self.w_progres_bar_window.grab_set()
        self.w_progres_bar_window.focus_set()
        self.w_progres_bar_window.configure( background=self.progres_bar_background)

        # ####################### disable_event ########################
        # disable click on the X on top right of the window
        def disable_event():
            self.__pbw_progress_bar_cancel_button()
            # pass

        self.w_progres_bar_window.protocol( "WM_DELETE_WINDOW", disable_event)
        if s_title:
            self.w_progres_bar_window.title( s_title)
        else:
            self.w_progres_bar_window.title( ' Progress Bar ')

        self.__pbw_set_window_size()
        self.__pbw_progres_bar_block( i_number_of_step, s_message)

        self.w_progres_bar_window.update()

        return self.answers

    # ####################### pbw_progres_bar_start ########################
    def pbw_progress_bar_start( self):
        """ start progres """
        self.__pbw_progress()

    # ####################### pbw_progres_bar_start ########################
    def pbw_progress_bar_step( self):
        """ go to to next value """
        if self.w_progres_bar_window:
            self.__pbw_progress()
            # self.progres_bar.step( i_step * self.f_value)
            self.w_progres_bar_window.update()

    # ####################### pbw_progres_bar_stop ########################
    def pbw_progress_bar_stop( self):
        """ Design the about box dialog """
        self.progres_bar.stop()
        self.value_lbl['text'] = self.__pbw_update_progress_label()
        # self.w_progres_bar_window.quit()
        self.w_progres_bar_window.destroy()
        self.w_progres_bar_window = None

    # ####################### pbw_close_progres_bar_window ########################
    def pbw_close_progress_bar_window( self):
        """ Close the preference window """
        self.__pbw_progress_bar_cancel_button()
        self.w_progres_bar_window.destroy()
        self.w_progres_bar_window = None
        # self.w_progres_bar_window.quit()
