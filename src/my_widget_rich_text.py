#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This is an application to do modification of bmp file to prepare convertion to a AIIGS pic file.
#
# from : https://stackoverflow.com/questions/63099026/fomatted-text-in-tkinter
# Copyright (C) Jul 26, 2020 Bryan Oakley
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

"""Module de gestion of a sub class of Text widget"""

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# Disable R0901 = Too many ancestors (this error come from class Text )
# pylint: disable=line-too-long
# pylint: disable=too-many-ancestors
# ###############################################################################################

from tkinter import font as tkFont
from tkinter import Text

# __name__ = "MyRichTextWidget"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= Enhanced Text widget =========================
class MyRichTextWidget( Text):
    """
    Create a custom Text Widget to manage a size normal * 1.5, bold, italic and bold_italic modes
    """
    # ####################### __init__ ########################
    def __init__( self, *args, **kwargs):
        """ Sub class of Text widget to add simple option """
        super().__init__( *args, **kwargs)
        default_font = tkFont.nametofont( self.cget( "font"))

        i_size_of_char = default_font.measure( "m")
        i_default_size = default_font.cget( "size")
        bold_font = tkFont.Font( **default_font.configure())
        italic_font = tkFont.Font( **default_font.configure())
        bold_italic_font = tkFont.Font( **default_font.configure())

        h1_font = tkFont.Font( **default_font.configure())

        bold_font.configure( weight="bold")
        italic_font.configure( slant="italic")
        bold_italic_font.configure( weight="bold", slant="italic")
        h1_font.configure( size=int( i_default_size * 1.5), weight="bold")

        self.tag_configure( "bold", font=bold_font)
        self.tag_configure( "italic", font=italic_font)
        self.tag_configure( "bold-italic", font=bold_italic_font)
        self.tag_configure( "h1", font=h1_font, spacing3=i_default_size)

        lmargin2 = i_size_of_char + default_font.measure( "\u2022 ")
        self.tag_configure( "bullet", lmargin1=i_size_of_char, lmargin2=lmargin2)

    # ####################### insert_bullet ########################
    def insert_bullet( self, index, text):
        """ Create little bullet to enhance the style """
        self.insert( index, f"\u2022 {text}", "bullet")
