#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This is an application to do modification of bmp file to prepare convertion to a AIIGS pic file.
#
# from :
# https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter/65125558#65125558
#
# Copyright (C) 2023 astqx <https://stackoverflow.com/users/14094985/astqx>
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

"""Module de gestion of a sub class for create help display when flying on some widget"""

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# pylint: disable=too-few-public-methods
# ###############################################################################################

from tkinter import Label, Toplevel

# __name__ = "MyToolTip"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= Enhanced Text widget =========================
class MyToolTip:
    """It creates a tooltip for a given widget as the mouse goes on it."""

    def __init__( self, widget, text=None):

        self.tooltip = None
        self.label = None

        def on_enter( event):
            """Create a yellow label on enter in widget shape"""
            self.tooltip = Toplevel()
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f'+{event.x_root+15}+{event.y_root+10}')

            self.label = Label( self.tooltip, text=self.text, padx=5, pady=5, justify='left', background="Yellow")
            self.label.pack()

        def on_leave( event):
            """Delete a yellow label on leave in widget shape"""
            self.tooltip.destroy()
            if event:   # remove pylint error : W0613: Unused argument 'event' (unused-argument)
                pass    # do nothing

        self.widget=widget
        self.text=text

        self.widget.bind( '<Enter>', on_enter)
        self.widget.bind( '<Leave>', on_leave)
