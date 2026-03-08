#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This is an application to do modification of bmp file to prepare convertion to a AIIGS pic file.
#
# Copyright (C) 2023-2026 Renaud Malaval <renaud.malaval@free.fr>.
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

""" Module de convertion Pil.Image () from BMP to PIC format. """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# number is reasonable in this case these are all the icons of the main windows and the application icons
# pylint: disable=too-many-instance-attributes
# ###############################################################################################

import ctypes

from PIL import Image

class MyFormatPic( ctypes.Structure):
    """
    convert a PIL image to a PIC format for Apple IIgs.

    typedef struct
    {
        unsigned char       MonImage[200][160];             // 32000 car 2 pixel par octets -> 200 * (320 / 2) = 32000
        unsigned char       SCB[200];                       // 200 SCB donnant le numero de palette de couleur pour chaque ligne 
        unsigned char       Libre[56];                      // espace libre utiliser pour indiquer quel logiciel... Par exemple en [25] == "816 Paint"
        unsigned short int  Couleur_Palette_0[16];          // une seule palette de 16 couleurs sur 2 octets A=0 R=x G=x B=x
        unsigned short int  Couleur_Palette_1a15[16 * 15];  // les autres 15 palettes restantes... 16 couleurs sur 2 octets * 15
    } FormatPIC;

    _fields_ is a class attribute that belongs to ctypes.Structure.
    It defines the fields of the structure, their names, and their types.
    """
    _fields_ = [
        ("MonImage", ctypes.c_ubyte * 160 * 200),
        ("SCB", ctypes.c_ubyte * 200),
        ("Libre", ctypes.c_ubyte * 56),
        ("Couleur_Palette_0", ctypes.c_uint16 * 16),
        ("Couleur_Palette_1a15", ctypes.c_uint16 * (16 * 15)),
    ]

    # ####################### __init__ ########################
    def __init__( self):
        """ Initialize the structure with default values """
        super().__init__()

    # ####################### __do_pixels_and_scb ########################
    def __do_pixels_and_scb( self, pixels):
        """ Convertit les pixels d'une image PIL en format PIC pour Apple IIgs. """
        for y in range(200):
            # On détermine la palette utilisée par la ligne
            first_pixel = pixels[y * 320]
            palette_line = first_pixel // 16

            self.SCB[y] = palette_line & 0x0F

            for x in range(160):
                p1 = pixels[y * 320 + (x * 2)]
                p2 = pixels[y * 320 + (x * 2 + 1)]

                # Convertit index 0–255 vers 0–15
                c1 = p1 % 16
                c2 = p2 % 16

                self.MonImage[y * 160 + x] = (c1 << 4) | c2

        used_blocks = {pixel // 16 for pixel in pixels[y*320:(y+1)*320]}
        if len( used_blocks) != 1:
            print(f"Ligne {y} mélange plusieurs palettes :", list(used_blocks))

    # ####################### __do_palette ########################
    def __do_palette( self, palette):
        """ Convertit la palette d'une image PIL en format PIC pour Apple IIgs. """
        for p1 in range(16):
            for p2 in range(16):

                idx = p1 * 16 + p2

                red = palette[idx * 3] >> 4
                green = palette[idx * 3 + 1] >> 4
                blue = palette[idx * 3 + 2] >> 4

                color12 = (red << 8) | (green << 4) | blue

                if p1 == 0:
                    self.Couleur_Palette_0[p2] = color12
                else:
                    self.Couleur_Palette_1a15[(p1 - 1) * 16 + p2] = color12

    # ####################### pil_to_format_pic ########################
    def pil_to_format_pic( self, img: Image.Image, filename: str):
        """
        Convertit une image PIL en format PIC pour Apple IIgs

        L'image doit être de 320x200 pixels et utiliser une palette de 16 couleurs (index 0-15)
        - MonImage : chaque pixel est codé sur 4 bits (16 couleurs), donc 2 pixels par octet
        - SCB : 200 octets, un par ligne, indiquant quelle palette de couleur est utilisée pour chaque ligne (0-15)
        - Libre : 56 octets, utilisé pour stocker des informations sur le logiciel qui a créé le fichier (ConvM (c) 2022..2026 Renaud Malaval & Frederic Mure)
        - Couleur_Palette_0 : 16 couleurs de la palette 0, chaque couleur codée sur 2 octets (A=0 R=xxx G=xxx B=xxx)
        - Couleur_Palette_1a15 : 15 palettes de 16 couleurs chacune, codées de la même manière que Couleur_Palette_0
        """

        pixels = list(img.getdata())

        # ==========================
        # 1) PIXELS + SCB
        # ==========================
        self.__do_pixels_and_scb( pixels)

        # ==========================
        # 2) SIGNATURE
        # ==========================
        texte = "ConvM (c) 2022..2026  Renaud Malaval & Frederic Mure"
        self.Libre[:] = texte.encode("ascii").ljust(56, b'\x00')

        # ==========================
        # 3) PALETTES IIGS
        # ==========================
        self.__do_palette( img.getpalette()) # 256 * 3 valeurs RGB

        with open(filename, "wb") as f:
            bytes_written = f.write( bytes( self))
            if bytes_written != 32768:
                print(f"Erreur d'écriture : {bytes_written} octets écrits au lieu de 32768 Ko")

    # ####################### is_valid ########################
    def is_valid( self) -> bool:
        """ Check if the structure has been properly initialized and contains valid data. """
        return len( bytes( self)) == 32768
