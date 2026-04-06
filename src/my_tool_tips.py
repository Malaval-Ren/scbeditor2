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
# Copyright (C) 2023 .. 2026 Renaud Malaval <renaud.malaval@free.fr>.
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

import platform
from typing import Optional
from tkinter import Label, Toplevel, Canvas
from tkinter import font as tkFont

# __name__ = "MyToolTip"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= Enhanced Text widget =========================
class MyToolTip:
    """It creates a tooltip for a given widget as the mouse goes on it."""

    def __init__( self, widget, text="no string given"):

        self.tooltip: Optional[Toplevel] = None
        self.label = None
        self.s_platform = platform.system()
        self.text = text

        # ####################### create_rounded_canvas ########################
        def create_rounded_canvas( parent, text, radius=10):
            """Create a canvas with rounded rectangle for Windows"""
            # Measure actual text width and height using font
            font = tkFont.Font( family="Arial", size=10)

            # Calculate height and width based on lines
            lines = text.split('\n')

            # Find the width of the longest line
            if lines:
                max_line_width = max(font.measure(line) for line in lines)
            else:
                max_line_width = 0

            height = len(lines) * 15 + 10       # 15 is Height per line, 10 is Padding top and bottom
            width = max_line_width + (15 * 2)   # 15 is Equal padding on left and right

            canvas = Canvas( parent, width=width, height=height, bg="white", highlightthickness=0, bd=0)

            # Draw rounded rectangle (using 4 arcs and 2 rectangles)
            x1, y1, x2, y2 = 0, 0, width - 1, height - 1
            canvas.create_arc( (x1, y1), (x1+radius*2, y1+radius*2), start=90, extent=90, fill="Yellow", outline="Yellow")
            canvas.create_arc( (x2-radius*2, y1), (x2, y1+radius*2), start=0, extent=90, fill="Yellow", outline="Yellow")
            canvas.create_arc( (x2-radius*2, y2-radius*2), (x2, y2), start=270, extent=90, fill="Yellow", outline="Yellow")
            canvas.create_arc( (x1, y2-radius*2), (x1+radius*2, y2), start=180, extent=90, fill="Yellow", outline="Yellow")
            canvas.create_rectangle( (x1+radius, y1), (x2-radius, y2), fill="Yellow", outline="Yellow")
            canvas.create_rectangle( (x1, y1+radius), (x2, y2-radius), fill="Yellow", outline="Yellow")

            # Set justify based on number of lines
            if len( lines) > 1:
                justify = "left"
            else:
                justify = "center"
            canvas.create_text(width // 2, height // 2, text=text, font=("Arial", 10), fill="Black", justify=justify)
            return canvas

        # ####################### on_enter ########################
        def on_enter( event):
            """Create a yellow label on enter in widget shape"""
            self.tooltip = Toplevel()
            self.tooltip.overrideredirect(True)
            if self.s_platform == "Windows":
                self.tooltip.attributes('-transparentcolor', 'white')
            self.tooltip.geometry(f'+{event.x_root+15}+{event.y_root+10}')

            if self.s_platform == "Linux":
                self.label = Label( self.tooltip, text=self.text, padx=5, pady=5, justify='left', background="Yellow", borderwidth=2, relief="solid")
            elif self.s_platform == "Darwin":
                self.label = Label( self.tooltip, text=self.text, padx=5, pady=5, justify='left', background="Yellow", foreground="Black")
            else:
                # Windows: use Canvas with rounded corners
                self.label = create_rounded_canvas(self.tooltip, self.text)

            self.label.pack()

        # ####################### on_leave ########################
        def on_leave( event):
            """Delete a yellow label on leave in widget shape"""
            if self.tooltip:
                self.tooltip.destroy()
            if event:   # remove pylint error : W0613: Unused argument 'event' (unused-argument)
                pass    # do nothing

        self.widget=widget
        self.text=text

        self.widget.bind( '<Enter>', on_enter)
        self.widget.bind( '<Leave>', on_leave)
