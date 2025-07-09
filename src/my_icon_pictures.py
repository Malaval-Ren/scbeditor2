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
#
# Special thank's to Reion for the icons : url: https://www.flaticon.com/authors/reion

""" Module to content all icons used in application """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# Number is reasonable in this case these are all the icons of the main windows and the application icons
# ###############################################################################################

import os
import sys
from tkinter import PhotoImage

# __name__ = "MyIconPictures"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# ####################### MyIconPictures ########################
class MyIconPictures:
    """ Content the pictures for human interface graphic """
    # pylint: disable=too-many-instance-attributes
    # nine is reasonable in this case these are all the icons of the main windows and the application icons

    _instance = None

    # ####################### __new__ ########################
    def __new__( cls, w_windows_parent=None) -> "MyIconPictures":
        """ Instantiate a singleton class """
        if MyIconPictures._instance is None:
            MyIconPictures._instance = object.__new__( cls)
            MyIconPictures.w_windows_parent = w_windows_parent
            MyIconPictures.app_photo = None
            MyIconPictures.about_photo = None
            MyIconPictures.open_photo = None
            MyIconPictures.save_photo = None
            MyIconPictures.color_palett_photo = None
            MyIconPictures.cursor_photo = None
            MyIconPictures.preferences_photo = None
            MyIconPictures.french_photo = None
            MyIconPictures.error_photo = None
            MyIconPictures.question_photo = None
            MyIconPictures.warning_photo = None
            MyIconPictures.right_arrow_photo = None
            MyIconPictures.left_arrow_photo = None
            MyIconPictures.up_arrow_photo = None
            MyIconPictures.down_arrow_photo = None
            MyIconPictures.__init( MyIconPictures._instance)
        return MyIconPictures._instance

    # ####################### _resource_path ########################
    def _resource_path( self, s_relative_path) -> str:
        """ Get absolute path to resource, works for dev and for PyInstaller """
        s_pictures_folder = None
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
			# PyInstaller creates a temp folder and stores path in _MEIPASS
            # pylint: disable=protected-access
            s_pictures_folder = os.path.join( sys._MEIPASS, os.path.basename( s_relative_path))
            # pylint: enable=protected-access
        else:
            s_pictures_folder = os.path.join( os.path.abspath("."), s_relative_path)

        return s_pictures_folder

    # ####################### __init ########################
    def __init( self):
        """
            Create all the icons of the application
            The disk with degrade color from green to blue come form Reion <a href=https://www.flaticon.com/authors/reion</a>
            I add multiple images from Reion to create it.
        """
        s_pictures_folder = "images"

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "ScbEditorII_T_16x16.png"))
        self.app_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "ScbEditorII_b_T_81x81.png"))
        self.about_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "openfile_b_T_81x81.png"))
        self.open_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "savefile_b_T_81x81.png"))
        self.save_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "color-pallet_b_T_81x81.png"))
        self.color_palett_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "curseur_b_T_81x81.png"))
        self.cursor_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "preferences_b_T_81x81.png"))
        self.preferences_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "fr_France_T_81x81.png"))
        self.french_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "error_T_81x81.png"))
        MyIconPictures.error_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "question2_T_81x81.png"))
        MyIconPictures.question_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "Warning_T_81x81.png"))
        MyIconPictures.warning_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "Arrow_Right_T_16x16.png"))
        self.right_arrow_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "Arrow_Left_T_16x16.png"))
        self.left_arrow_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "Arrow_Up_T_16x16.png"))
        self.up_arrow_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

        icon_path = self._resource_path( os.path.join( s_pictures_folder, "Arrow_Down_T_16x16.png"))
        self.down_arrow_photo = PhotoImage( master=self.w_windows_parent, file=icon_path)

    # ####################### log_size_of_photo ########################
    # def log_size_of_photo( self, a_photo):
    #     """log the size of a photo"""
    #     if self.w_windows_parent is not None:
    #         # __s_dimensions = "Image size is\t%dx%d pixels\n" % (a_photo.width(), a_photo.height())
    #         # self.c_the_log.add_string_to_log( "log_size_of_photo() : " + __s_dimensions)
    #         self.c_the_log.add_string_to_log( "log_size_of_photo() : Image size is\t" + str( a_photo.width()) + 'x' + str( a_photo.height()) + " pixels\n" )

    # ####################### get_app_photo ########################
    def get_app_photo( self) -> PhotoImage:
        """Get app icon for the menu bar windows"""
        return self.app_photo

    # ####################### get_about_photo ########################
    def get_about_photo( self) -> PhotoImage:
        """Get about icon for the main windows"""
        return self.about_photo

    # ####################### get_open_photo ########################
    def get_open_photo( self) -> PhotoImage:
        """Get open icon for the main windows"""
        return self.open_photo

    # ####################### get_save_photo ########################
    def get_save_photo( self) -> PhotoImage:
        """Get save icon for the main windows"""
        return self.save_photo

    # ####################### get_color_pallet_photo ########################
    def get_color_pallet_photo( self) -> PhotoImage:
        """Get color pallet icon for the main windows"""
        return self.color_palett_photo

    # ####################### get_cursor_photo ########################
    def get_cursor_photo( self) -> PhotoImage:
        """Get cursor icon for the main windows"""
        return self.cursor_photo

    # ####################### get_preferences_photo ########################
    def get_preferences_photo( self) -> PhotoImage:
        """Get preferences icon for the main windows"""
        return self.preferences_photo

    # ####################### get_french_photo ########################
    def get_french_photo( self) -> PhotoImage:
        """Get french flag icon for the main windows"""
        return self.french_photo

    # ####################### get_error_photo ########################
    def get_error_photo( self) -> PhotoImage:
        """Get error flag icon for the alert windows"""
        return self.error_photo

    # ####################### get_question_photo ########################
    def get_question_photo( self) -> PhotoImage:
        """Get question flag icon for the alert windows"""
        return self.question_photo

    # ####################### get_warning_photo ########################
    def get_warning_photo( self) -> PhotoImage:
        """Get warning flag icon for the alert windows"""
        return self.warning_photo

    # ####################### get_right_arrow_photo ########################
    def get_right_arrow_photo( self) -> PhotoImage:
        """Get right arrow icon for the alert windows"""
        return self.right_arrow_photo

    # ####################### get_left_arrow_photo ########################
    def get_left_arrow_photo( self) -> PhotoImage:
        """Get left arrow icon for the alert windows"""
        return self.left_arrow_photo

    # ####################### get_up_arrow_photo ########################
    def get_up_arrow_photo( self) -> PhotoImage:
        """Get up arrow icon for the alert windows"""
        return self.up_arrow_photo

    # ####################### get_down_arrow_photo ########################
    def get_down_arrow_photo( self) -> PhotoImage:
        """Get down arrow icon for the alert windows"""
        return self.down_arrow_photo
