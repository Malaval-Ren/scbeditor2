#!/usr/bin/python3
# -*- coding: utf-8 -*-
# script by  Renaud Malaval

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

__name__ = "MyConstants"

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
