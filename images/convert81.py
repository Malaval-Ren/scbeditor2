#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Create a python file with png file converted in base 64
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

"""
Coding rule (added to PEP8) :

b_ this is a boolean
x_ this is bits
i_ this is an integer
f_ this is a float
s_ this is a string
w_ this is a windows widget
a_ this is a widget
t_ this is a thread

__method pour les méthodes ou variable privées
_method pour les méthodes ou variable protégées

"""

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = line-too-long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import os
import io
import base64

# ##########################################################################################
# https://manytools.org/hacker-tools/ascii-banner/
#
# #    #   ##   ### #    #
# ##  ##  #  #   #  ##   #
# # ## # #    #  #  # #  #
# #    # ######  #  #  # #
# #    # #    #  #  #   ##
# #    # #    # ### #    #
#
# ##########################################################################################

# ####################### write_header ########################
def write_header( output_file):
    """ Add a fake header to simplify merge """
    s_texte = "#!/usr/bin/python3\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte = "# -*- coding: utf-8 -*-\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte = "#\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte = "\"\"\" Module to content all icons used in application \"\"\"\n\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    to_write = str.encode( s_texte)
    s_texte = "# ###############################################################################################\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte = "#                                   PYLINT\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte = "# Disable C0301 = Line too long (80 chars by line is not enough)\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte = "# pylint: disable=line-too-long\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte = "# ###############################################################################################\n\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte =  "# ####################### MyIconPictures ########################\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte =  "class MyIconPictures:\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte =  "\t\"\"\" Content the pictures for human interface graphic \"\"\"\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte =  "\t# ####################### __init__ ########################\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte =  "\tdef __init( self):\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)
    s_texte =  "\t\t\"\"\" A TEXT \"\"\"\n"
    to_write = str.encode( s_texte)
    output_file.write( to_write)

# ####################### main ########################
def main():
    """ The entry function of the application """

    images_lst=[]
    s_target_folder="./"
    s_target_code="./my_images.py"

    if not os.path.isfile( "./catalog.txt"):
        print( "./catalog.txt does not exist")
        return

    # create a list of picture found
    with io.open( "./catalog.txt", 'r', encoding='utf8') as config_file:
        s_line_readed = config_file.readline()
        while s_line_readed != "":
            s_texte = s_line_readed.strip()
            images_lst.append( s_texte)
            s_line_readed = config_file.readline()

    config_file.close()

    # writing result Python file
    with io.open( s_target_code, 'wb' ) as output_file:
        write_header( output_file)
        for i_index in range( 0, len(images_lst), 1):
            iconfile = open( images_lst[i_index], "rb")
            icondata = iconfile.read()
            icondata = base64.b64encode( icondata)
            # write the header 1 line
            s_texte = "\t\t# Image file = " + images_lst[i_index] + "\n"
            to_write = str.encode( s_texte)
            output_file.write( to_write)

            # write the header 2 line
            s_texte = images_lst[i_index]
            s_texte = s_texte[:-11]
            s_texte = "\t\t__app_" + s_texte.lower() + "base_64 = \"\"\"" + "\n"
            to_write = str.encode( s_texte)
            output_file.write( to_write)

            # write the data
            i_lendata = len( icondata)
            v_buffer = memoryview( icondata)
            i_loop = 0
            # print( "i_lendata = " + str( i_lendata))
            while i_lendata > 0:
                # print( "i_loop = " + str( i_loop) + " to = " + str( i_loop+min( i_lendata, 255)))
                s_texte = "\t\t"
                to_write = str.encode( s_texte)
                output_file.write( to_write)
                tempo=bytes(v_buffer[i_loop:i_loop+min( i_lendata, 255)])
                output_file.write( tempo)
                if i_lendata < 255:
                    s_texte = '\n'
                else:
                    # This line does not work !!!
                    s_texte = "\\\n"
                to_write = str.encode( s_texte)
                output_file.write( to_write)
                i_lendata = i_lendata - min( i_lendata, 255)
                i_loop += 255

            # print( "i_loop = " + str( i_loop))
            s_texte = "\t\t\"\"\"\n"
            to_write = str.encode( s_texte)
            output_file.write( to_write)

    output_file.close()
    print( "Done")

# ###############################################################################################
# ####################### Entry point ########################
# wrapper(main)
if __name__ == "__main__":
    main()
