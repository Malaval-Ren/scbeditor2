#!/usr/bin/python3
# -*- coding: utf-8 -*-
# script by  Bryan Oakley, Renaud Malaval
#
# from : https://stackoverflow.com/questions/63099026/fomatted-text-in-tkinter

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

        size_of_char = default_font.measure( "m")
        default_size = default_font.cget( "size")
        bold_font = tkFont.Font( **default_font.configure())
        italic_font = tkFont.Font( **default_font.configure())
        bold_italic_font = tkFont.Font( **default_font.configure())

        h1_font = tkFont.Font( **default_font.configure())

        bold_font.configure( weight="bold")
        italic_font.configure( slant="italic")
        bold_italic_font.configure( weight="bold", slant="italic")
        h1_font.configure( size=int( default_size * 1.5), weight="bold")

        self.tag_configure( "bold", font=bold_font)
        self.tag_configure( "italic", font=italic_font)
        self.tag_configure( "bold-italic", font=bold_italic_font)
        self.tag_configure( "h1", font=h1_font, spacing3=default_size)

        lmargin2 = size_of_char + default_font.measure( "\u2022 ")
        self.tag_configure( "bullet", lmargin1=size_of_char, lmargin2=lmargin2)

    # ####################### insert_bullet ########################
    def insert_bullet( self, index, text):
        """ Create little bullet to enhance the style """
        self.insert( index, f"\u2022 {text}", "bullet")
