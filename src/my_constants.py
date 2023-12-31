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

# Nombre de relais utiliser sur les devices
MAX_NUMBER_OF_DEVICE = 4

# size of a button is number of charracters here 15 charracters => 115 pixels
DEFAULT_BUTTON_WIDTH = 15

COLOR_WINDOWS_MENU_BAR = '#0063B1'  # rgb(0, 99, 177)

OUTPUT_TM221CE16_07 = 7     # 0 .. 6
OUTPUT_TM221CE24_10 = 10    # 0 .. 9
OUTPUT_TM221CE40_16 = 16    # 0 .. 15

INPUT_TM221CE16_09 = 9      # 0 .. 8
INPUT_TM221CE24_14 = 14     # 0 .. 13
INPUT_TM221CE40_24 = 24     # 0 .. 23

DISPLAY_MODE_HORIZONTAL = 'Z'
DISPLAY_MODE_VERTICAL = 'N'

# BACKGROUD_COLOR_UI = 'light grey'
# gray color for windows 211,211,211 -> '#D3D3D3'
BACKGROUD_COLOR_UI = '#D3D3D3' # 'light grey'

DARK_COLOR_UI = '#000000' # 'black'
LIGHT_COLOR_UI = '#FFFFFF' # 'white'

COLOR_WINDOWS_MENU_BAR = '#0063B1'  # rgb(0, 99, 177)
