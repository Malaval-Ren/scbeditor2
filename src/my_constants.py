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

"""Application constants declaration module"""

# FROM :
# https://qastack.fr/programming/6343330/importing-a-long-list-of-constants-to-a-python-file
#
# USAGE :
#
# import my_constants as constant
#
# constant.MAX_NUMBER_OF_DEVICE
#

# __name__ = "MyConstants"

# #######========================= constant =========================

MY_APPLICATION_NAME = 'SCB Editor II'

# size of a button is number of charracters here 15 charracters => 115 pixels
# size of a button is number of charracters here 3 charracters => 21 pixels
# size of a button is number of charracters here 5 charracters => 35 pixels
# size of a button is number of charracters here 6 charracters => 42 pixels
# size of a button is number of charracters here 7 charracters => 49 pixels
DEFAULT_BUTTON_WIDTH = 7

# Color informations
# https://matplotlib.org/stable/gallery/color/named_colors.html

COLOR_WINDOWS_MENU_BAR = '#0063B1'  # rgb(0, 99, 177)

# BACKGROUD_COLOR_UI = 'light grey' or 'darkgray' or 'gray'
# gray color for windows 211,211,211 -> '#D3D3D3'
BACKGROUD_COLOR_UI = 'dimgray'    #dimgray -> '#696969' or  #595959

DARK_COLOR_UI = '#000000' # 'black'
LIGHT_COLOR_UI = '#FFFFFF' # 'white'

COLOR_WINDOWS_MENU_BAR = '#0063B1'  # rgb(0, 99, 177)

PICTURE_WIDTH = 640
PICTURE_HEIGHT = 400
