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

import platform
import os
import sys

from typing import Optional

from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk

import src.my_constants as constant

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
    app_photo: Optional[PhotoImage] = None
    about_photo: Optional[PhotoImage] = None
    open_photo: Optional[PhotoImage] = None
    save_photo: Optional[PhotoImage] = None
    color_palett_photo: Optional[PhotoImage] = None
    cursor_photo: Optional[PhotoImage] = None
    preferences_photo: Optional[PhotoImage] = None
    french_photo: Optional[PhotoImage] = None
    error_photo: Optional[PhotoImage] = None
    question_photo: Optional[PhotoImage] = None
    warning_photo: Optional[PhotoImage] = None
    right_arrow_photo: Optional[PhotoImage] = None
    left_arrow_photo: Optional[PhotoImage] = None
    up_arrow_photo: Optional[PhotoImage] = None
    down_arrow_photo: Optional[PhotoImage] = None

    # ####################### __new__ ########################
    def __new__( cls, w_windows_parent=None) -> "MyIconPictures":
        """ Instantiate a singleton class """
        if MyIconPictures._instance is None:
            MyIconPictures._instance = object.__new__( cls)
            MyIconPictures.w_windows_parent = w_windows_parent
            # Liste des paires (nom_de_variable, nom_de_fichier_image)
            MyIconPictures.images = [
                ("app_photo", "ScbEditorII_T_16x16.png"),
                ("about_photo", "ScbEditorII_b_T_81x81.png"),
                ("open_photo", "openfile_b_T_81x81.png"),
                ("save_photo", "savefile_b_T_81x81.png"),
                ("color_palett_photo", "color-pallet_b_T_81x81.png"),
                ("cursor_photo", "curseur_b_T_81x81.png"),
                ("preferences_photo", "preferences_b_T_81x81.png"),
                ("french_photo", "fr_France_T_81x81.png"),
                ("error_photo", "error_T_81x81.png"),
                ("question_photo", "question2_T_81x81.png"),
                ("warning_photo", "Warning_T_81x81.png")
            ]
            MyIconPictures.arrows = [
                ("right_arrow_photo", "Arrow_Right_T_16x16.png"),
                ("left_arrow_photo", "Arrow_Left_T_16x16.png"),
                ("up_arrow_photo", "Arrow_Up_T_16x16.png"),
                ("down_arrow_photo", "Arrow_Down_T_16x16.png")
            ]
            
            MyIconPictures.__init( MyIconPictures._instance)
        return MyIconPictures._instance

    # ####################### __test_format_image ########################
    # def __test_format_image( self, s_relative_path : str):
    #     """ check if picture have transparency """
    #     print( f"test image {s_relative_path}")
    #     img = Image.open( s_relative_path)
    #     if img.mode in ("RGBA", "LA"):
    #         alpha = img.getchannel("A")
    #         i_min, i_max = alpha.getextrema()
    #         print( f"i_min = {i_min}")
    #         print( f"i_max = {i_max}")
    #         print( f"a var = {alpha.getextrema()[0]}")
    #         if alpha.getextrema()[0] < 255:
    #             print( "\t✅ L’image a une transparence.")
    #         else:
    #             print( "\t🟠 L’image est en mode RGBA, mais complètement opaque.")
    #     else:
    #         print( "\t❌ L’image n’a pas de canal alpha (pas de transparence).")

    # ####################### __resource_path ########################
    def __resource_path( self, s_relative_path : str) -> str:
        """ Get absolute path to resource, works for dev and for PyInstaller """
        s_pictures_folder = None
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
			# PyInstaller creates a temp folder and stores path in _MEIPASS
            # pylint: disable=protected-access
            s_pictures_folder = os.path.join( sys._MEIPASS, os.path.basename( s_relative_path))
            # pylint: enable=protected-access
        else:
            s_pictures_folder = os.path.join( os.path.abspath("."), s_relative_path)

        if not os.path.exists( s_pictures_folder):
            messagebox.showerror( "Error : Internal icon missing", f"file {s_relative_path} not found")
            sys.exit( int( 2))

        return s_pictures_folder

    # ####################### __get_flat_icon ########################
    def __get_flat_icon( self, s_path_filename : str, background_color=constant.BACKGROUD_COLOR_UI_MAC) :
        """ Manage transparency for mac os version """
        img = Image.open( s_path_filename).convert("RGBA")
        background = Image.new("RGBA", img.size, background_color)
        blended = Image.alpha_composite(background, img)
        return ImageTk.PhotoImage( blended)

    # ####################### __init ########################
    def __init( self):
        """
            Create all the icons of the application
            The disk with degrade color from green to blue come form Reion <a href=https://www.flaticon.com/authors/reion</a>
            I add multiple images from Reion to create it.
        """
        s_pictures_folder = "images"
        s_platform = platform.system()
        for var_name, file_name in self.images:
            s_icon_path = self.__resource_path( os.path.join( s_pictures_folder, file_name))
            if s_platform == 'Darwin':
                photo = self.__get_flat_icon( s_icon_path)
            else:
                photo = PhotoImage( master=self.w_windows_parent, file=s_icon_path)
            setattr( self, var_name, photo)

        for var_name, file_name in self.arrows:
            s_icon_path = self.__resource_path( os.path.join( s_pictures_folder, file_name))
            photo = PhotoImage( master=self.w_windows_parent, file=s_icon_path)
            setattr( self, var_name, photo)

    # ####################### get_app_photo ########################
    def get_app_photo( self) -> PhotoImage:
        """Get app icon for the menu bar windows"""
        assert self.app_photo is not None
        return self.app_photo

    # ####################### get_about_photo ########################
    def get_about_photo( self) -> PhotoImage:
        """Get about icon for the main windows"""
        assert self.about_photo is not None
        return self.about_photo

    # ####################### get_open_photo ########################
    def get_open_photo( self) -> PhotoImage:
        """Get open icon for the main windows"""
        assert self.open_photo is not None
        return self.open_photo

    # ####################### get_save_photo ########################
    def get_save_photo( self) -> PhotoImage:
        """Get save icon for the main windows"""
        assert self.save_photo is not None
        return self.save_photo

    # ####################### get_color_pallet_photo ########################
    def get_color_pallet_photo( self) -> PhotoImage:
        """Get color pallet icon for the main windows"""
        assert self.color_palett_photo is not None
        return self.color_palett_photo

    # ####################### get_cursor_photo ########################
    def get_cursor_photo( self) -> PhotoImage:
        """Get cursor icon for the main windows"""
        assert self.cursor_photo is not None
        return self.cursor_photo

    # ####################### get_preferences_photo ########################
    def get_preferences_photo( self) -> PhotoImage:
        """Get preferences icon for the main windows"""
        assert self.preferences_photo is not None
        return self.preferences_photo

    # ####################### get_french_photo ########################
    def get_french_photo( self) -> PhotoImage:
        """Get french flag icon for the main windows"""
        assert self.french_photo is not None
        return self.french_photo

    # ####################### get_error_photo ########################
    def get_error_photo( self) -> PhotoImage:
        """Get error flag icon for the alert windows"""
        assert self.error_photo is not None
        return self.error_photo

    # ####################### get_question_photo ########################
    def get_question_photo( self) -> PhotoImage:
        """Get question flag icon for the alert windows"""
        assert self.question_photo is not None
        return self.question_photo

    # ####################### get_warning_photo ########################
    def get_warning_photo( self) -> PhotoImage:
        """Get warning flag icon for the alert windows"""
        assert self.warning_photo is not None
        return self.warning_photo

    # ####################### get_right_arrow_photo ########################
    def get_right_arrow_photo( self) -> PhotoImage:
        """Get right arrow icon for the alert windows"""
        assert self.right_arrow_photo is not None
        return self.right_arrow_photo

    # ####################### get_left_arrow_photo ########################
    def get_left_arrow_photo( self) -> PhotoImage:
        """Get left arrow icon for the alert windows"""
        assert self.left_arrow_photo is not None
        return self.left_arrow_photo

    # ####################### get_up_arrow_photo ########################
    def get_up_arrow_photo( self) -> PhotoImage:
        """Get up arrow icon for the alert windows"""
        assert self.up_arrow_photo is not None
        return self.up_arrow_photo

    # ####################### get_down_arrow_photo ########################
    def get_down_arrow_photo( self) -> PhotoImage:
        """Get down arrow icon for the alert windows"""
        assert self.down_arrow_photo is not None
        return self.down_arrow_photo

    # ####################### log_size_of_photo ########################
    # def log_size_of_photo( self, a_photo):
    #     """log the size of a photo"""
    #     if self.w_windows_parent is not None:
    #         # __s_dimensions = "Image size is\t%dx%d pixels\n" % (a_photo.width(), a_photo.height())
    #         # self.c_the_log.add_string_to_log( "log_size_of_photo() : " + __s_dimensions)
    #         self.c_the_log.add_string_to_log( "log_size_of_photo() : Image size is\t" + str( a_photo.width()) + 'x' + str( a_photo.height()) + " pixels\n" )
