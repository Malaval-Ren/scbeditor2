#!/usr/bin/python3
# -*- coding: utf-8 -*-
# script by  Renaud Malaval

""" Module de creation de la fenetre principale. """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# number is reasonable in this case these are all the icons of the main windows and the application icons
# pylint: disable=too-many-instance-attributes
# ###############################################################################################

import platform
import os
import tkinter as tk_gui

from datetime import datetime
from enum import IntEnum
from tkinter import Label, Button, Canvas, Entry
from tkinter.ttk import Separator
from functools import partial

import tkinter.font as tkFont

# from ttkthemes              import ThemedTk, THEMES, ThemedStyle
from PIL import Image, ImageTk
# import matplotlib as tkMapPlot
# import matplotlib.pyplot as plt

import src.my_constants as constant
# from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_main_window_icons_bar import MyMainWindowIconsBar
from .my_tools import open_file

# __name__ = "MyMainWindow"

# ###############################################################################################
# #######========================= constant private =========================

MAIN_WINDOWS_WIDTH = 840
MAIN_WINDOWS_HEIGHT = 806
WAIT_TIME_COM = 0.05

# ###############################################################################################
# #######=========================     GUI     =========================
# ####################### MyMainWindow ########################
class MyMainWindow:
    """ Create the main Windows of the application. """
    # Optimizing memory usage with slots
    # __slots__ = ["w_main_windows", "a_list_application_info", "a_dico_mw_gui_element" ]

    # ####################### __init__ ########################
    def __init__( self, w_main_windows, list_application_info):
        """
            All this parameter are created in main()
            w_main_windows : the windows created by tk
            a_list_application_info : les inforamtions de l'application
        """
        print()
        self.w_main_windows = w_main_windows
        self.a_list_application_info = list_application_info
        # Size of the main windows
        self.i_main_window_width = MAIN_WINDOWS_WIDTH
        self.i_main_window_height = MAIN_WINDOWS_HEIGHT
        # Position of the main windows
        self.i_main_window_x = 20
        self.i_main_window_y = 20       
        self.w_main_windows.background = constant.BACKGROUD_COLOR_UI
        self.c_the_icons = MyIconPictures( w_main_windows)
        self.s_platform = platform.system()
        self.a_palette_button_lst = []
        self.a_work_img = None
        self.a_bmp_image_file = None
        self.a_canvas = None
        self.a_render = None
        self.a_image = None
        self.a_mouse_pos_x = None
        self.a_mouse_pos_Y = None
        self.a_color_lbl = None
        self.a_scb_lbl = None
        self.a_pic_color_lbl = None
        self.a_red = None
        self.a_green = None
        self.a_blue = None
        self.a_red_dec_lbl = None
        self.a_green_dec_lbl = None
        self.a_blue_dec_lbl = None        
        self.a_btn_x_lbl = None
        self.a_btn_y_lbl = None
        self.a_the_color_lbl = None
        
        self.__mw_print_widget_under_mouse( w_main_windows)

    # ####################### __repr__ ########################
    def __repr__( self):
        """ A dundle method for description """
        return f"{type(self).__name__}({self.w_main_windows}, {self.a_list_application_info})"

    # ####################### __getattribute__ ########################
    # def __getattribute__( self, name):
    #     """ A dundle method for description """
    #     cls = type( self)
    #     # if hasattr( cls, "__slots__"):
    #     #     if name in cls.__slots__:
    #     #         index = cls.__slots__.index( name)
    #     #         return self.slot_array( index)
    #     if name in vars( self):
    #         return vars( self)[ name]
    #     if hasattr( cls, name):
    #         return getattr( cls, name)
    #     if hasattr( cls, "__getattr__"):
    #         return cls.__getattr__( self, name)
    #     return AttributeError( f"{cls.name} object has no attribute {name}")


    # ####################### __mw_picture_zone ########################
    def __mw_picture_zone(self):
        """ Frame with the picture to left, and details to right """        
        i_index_base_block = 0
        a_pic_frame = tk_gui.Frame(self.w_main_windows, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_pic_frame.place(x=2, y=98, width=self.i_main_window_width-4, height=400+15)  # fill :  must be 'none', 'x', 'y', or 'both'

        a_pic_sep_h1 = Separator(a_pic_frame, orient='horizontal')
        a_pic_sep_h1.grid(row=i_index_base_block, column=0, columnspan=1, sticky='ew')
        a_pic_sep_lbl_h1 = Label(a_pic_frame, text="Picture", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h1.grid(row=i_index_base_block, column=0, padx=15)
        a_pic_sep_h2 = Separator(a_pic_frame, orient='horizontal')
        a_pic_sep_h2.grid(row=i_index_base_block, column=1, columnspan=1, sticky='ew')
        a_pic_sep_lbl_h2 = Label(a_pic_frame, text="Details", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h2.grid(row=i_index_base_block, column=1, columnspan=1, padx=81, sticky='ew')

        i_index_base_block += 1
        self.a_canvas = Canvas(a_pic_frame, width=640, height=404, background='darkgray')
        self.a_canvas.grid(row=i_index_base_block, column=0, sticky='e')

        # Create SCB frame
        a_scb_frame = tk_gui.Frame(a_pic_frame, padx=0, pady=0, background='white')     # background='darkgray' or 'light grey'
        a_scb_frame.place(x=648, y=20, width=20, height=399)

        # Create details frame
        a_details_pic_frame = tk_gui.Frame(a_pic_frame, padx=0, pady=0, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_details_pic_frame.place(x=668, y=15, width=self.i_main_window_width - 668, height=404)

        i_index_base_block = 0
        a_pic_sep_lbl_h3 = Label(a_details_pic_frame, text="Mouse position", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h3.grid(row=i_index_base_block, column=1, columnspan=2, padx=4)

        i_index_base_block += 1
        a_pic_sep_lbl_h4 = Label(a_details_pic_frame, text="X: ", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid(row=i_index_base_block, column=1, padx=4)
        self.a_mouse_pos_x = Entry(a_details_pic_frame, textvariable="", background='white', foreground='black')
        self.a_mouse_pos_x.grid(row=i_index_base_block, column=2, padx=4)

        i_index_base_block += 1
        a_pic_sep_lbl_h4 = Label( a_details_pic_frame, text="Y: ", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h4.grid( row=i_index_base_block, column=1, padx=4)
        self.a_mouse_pos_y = Entry( a_details_pic_frame, textvariable="", background='white', foreground='black')
        self.a_mouse_pos_y.grid( row=i_index_base_block, column=2, padx=4)

        i_index_base_block += 1
        a_pic_sep_lbl_h5 = Label( a_details_pic_frame, text="Color offset", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h5.grid( row=i_index_base_block, column=1, columnspan=2, padx=4)

        i_index_base_block += 1
        self.a_color_lbl = Label( a_details_pic_frame, text="   ", background='white', foreground='black')
        self.a_color_lbl.grid( row=i_index_base_block, column=1, columnspan=2, padx=4, sticky='ew')

        i_index_base_block += 1
        a_pic_sep_lbl_h6 = Label( a_details_pic_frame, text="Palette number / SCB", background=constant.BACKGROUD_COLOR_UI)
        a_pic_sep_lbl_h6.grid( row=i_index_base_block, column=1, columnspan=2, padx=4)

        i_index_base_block += 1
        self.a_scb_lbl = Label( a_details_pic_frame, text="   ", background='white', foreground='black')
        self.a_scb_lbl.grid( row=i_index_base_block, column=1, columnspan=2, padx=4, sticky='ew')

        i_index_base_block += 1
        a_color_name_lbl = Label( a_details_pic_frame, text="RGB Color", background=constant.BACKGROUD_COLOR_UI)
        a_color_name_lbl.grid( row=i_index_base_block, column=1, columnspan=2, padx=4)

        i_index_base_block += 1
        self.a_pic_color_lbl = Label( a_details_pic_frame, text="", background='white', foreground='black')
        self.a_pic_color_lbl.grid( row=i_index_base_block, column=1, columnspan=2, padx=4, sticky='ew')

    # ####################### __mw_palette_zone ########################
    def __mw_palette_zone(self):
        """ Frame with the palette button to left, and details to right """
        i_index_base_block = 0
        a_bottom_frame = tk_gui.Frame( self.w_main_windows, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_bottom_frame.place( x=2, y=98+400+14, width=self.i_main_window_width-4, height=294 )
        
        a_palette_sep_h2 = Separator( a_bottom_frame, orient='horizontal')
        a_palette_sep_h2.grid( row=i_index_base_block, column=0, columnspan=8, sticky='ew')
        a_palette_sep_lbl_h2 = Label( a_bottom_frame, text="Palette", background=constant.BACKGROUD_COLOR_UI)
        a_palette_sep_lbl_h2.grid( row=i_index_base_block, column=0, columnspan=2, padx=260)

        a_palette_sep_h3 = Separator( a_bottom_frame, orient='horizontal')
        a_palette_sep_h3.grid( row=i_index_base_block, column=9, columnspan=4, sticky='ew')
        a_palette_sep_lbl_h3 = Label( a_bottom_frame, text="Color", background=constant.BACKGROUD_COLOR_UI)
        a_palette_sep_lbl_h3.grid( row=i_index_base_block, column=9, columnspan=4, padx=120)

        # Create palette button left frame
        a_palette_bottom_frame = tk_gui.Frame( a_bottom_frame, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_palette_bottom_frame.place( x=2, y=15, width=600, height=276 )

        # Create color buton right frame
        a_color_bottom_frame = tk_gui.Frame( a_bottom_frame, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)     # background='darkgray' or 'light grey'
        a_color_bottom_frame.place( x=602, y=15, width=self.i_main_window_width - 602, height=276 )

        i_index_base_block = 0
        a_color_name_lbl = Label( a_color_bottom_frame, text="Red", background=constant.BACKGROUD_COLOR_UI, foreground='red')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=7)
        i_index_base_block += 1
        self.a_red = Entry( a_color_bottom_frame, textvariable="", background='white', foreground='red')
        self.a_red.grid( row=i_index_base_block, column=0, padx=7)
        self.a_red_dec_lbl = Label( a_color_bottom_frame, text="   ", background='white', foreground='red')
        self.a_red_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=2, padx=7, sticky='ew')       
        i_index_base_block += 1
        a_color_name_lbl = Label( a_color_bottom_frame, text="Green", background=constant.BACKGROUD_COLOR_UI, foreground='green')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=7)
        i_index_base_block += 1
        self.a_green = Entry( a_color_bottom_frame, textvariable="", background='white', foreground='green')
        self.a_green.grid( row=i_index_base_block, column=0, padx=7)
        self.a_green_dec_lbl = Label( a_color_bottom_frame, text="   ", background='white', foreground='green')
        self.a_green_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=2, padx=7, sticky='ew')
        i_index_base_block += 1
        a_color_name_lbl = Label( a_color_bottom_frame, text="Blue", background=constant.BACKGROUD_COLOR_UI, foreground='blue')
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=7)
        i_index_base_block += 1
        self.a_blue = Entry( a_color_bottom_frame, textvariable="", background='white', foreground='blue')
        self.a_blue.grid( row=i_index_base_block, column=0, padx=7)
        self.a_blue_dec_lbl = Label( a_color_bottom_frame, text="   ", background='white', foreground='blue')
        self.a_blue_dec_lbl.grid( row=i_index_base_block, column=1, columnspan=2, padx=7, sticky='ew')

        i_index_base_block += 1
        a_color_name_lbl = Label( a_color_bottom_frame, text="RGB Color", background=constant.BACKGROUD_COLOR_UI)
        a_color_name_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=7)
        i_index_base_block += 1
        self.a_the_color_lbl = Label( a_color_bottom_frame, text="", background='white', foreground='black')
        self.a_the_color_lbl.grid( row=i_index_base_block, column=0, columnspan=2, padx=7, sticky='ew')

        i_index_base_block += 1
        a_offset_lbl = Label( a_color_bottom_frame, text="Palette Y", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=0, columnspan=1, padx=7)
        a_offset_lbl = Label( a_color_bottom_frame, text="Offset X", background=constant.BACKGROUD_COLOR_UI)
        a_offset_lbl.grid( row=i_index_base_block, column=1, columnspan=1, padx=7)
        i_index_base_block += 1
        self.a_btn_x_lbl = Label( a_color_bottom_frame, text="   ", background='white', foreground='black')
        self.a_btn_x_lbl.grid( row=i_index_base_block, column=0, padx=7, sticky='ew')
        self.a_btn_y_lbl = Label( a_color_bottom_frame, text="   ", background='white', foreground='black')
        self.a_btn_y_lbl.grid( row=i_index_base_block, column=1, padx=7, sticky='ew')
        i_index_base_block += 1
        a_zButton = Button( a_color_bottom_frame, text='Set color', width=14, height=1)
        a_zButton.grid( row=i_index_base_block, column=0, columnspan=2, padx=7, pady=8, sticky='ew')

        # creating a font object with little size for color buttons
        a_font_label = tkFont.Font(size=6)
        a_font_button = tkFont.Font(size=5)

        i_index_base_block += 1
        i_index_base_column = 1
        for i_loop in range( 0, 16, 1):
            a_label = Label(a_palette_bottom_frame, text=str(i_loop), background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            i_index_base_column += 1

        i_index_base_block += 1
        i_index_base_column = 0
        i_to = 0
        for i_loop in range( 0, 16, 1):
            i_from = i_to
            i_to = i_to + 48
            a_label = Label(a_palette_bottom_frame, text=str(i_loop), background=constant.BACKGROUD_COLOR_UI, font=a_font_label)
            a_label.grid( row=i_index_base_block, column=i_index_base_column, padx=2, pady=0)
            i_index_base_column += 1
            for i_index in range( i_from, i_to, 3):
                a_button_color = Button( a_palette_bottom_frame, text='', width=4, height=1, background="#FFFFFF", font=a_font_button)
                a_button_color.grid( row=i_index_base_block, column=i_index_base_column, padx=4, pady=2)
                self.a_palette_button_lst.append(a_button_color)
                i_index_base_column += 1

            self.w_main_windows.update()
            i_index_base_column = 0
            i_index_base_block += 1

    # ####################### __mw_color_button ########################
    def __mw_color_button(self, i_number, s_red, s_green, s_blue):
        """ Button de couleur """
        # self.w_main_windows.bell()
        self.a_red.delete( 0, 10)
        __s_red_true=s_red.replace("#","")
        self.a_red.insert( "end", __s_red_true)
        self.a_red_dec_lbl.configure( text=str(int(__s_red_true, 16)))
        self.a_green.delete( 0, 10)
        self.a_green.insert( "end", s_green)
        self.a_green_dec_lbl.configure( text=str(int(s_green, 16)))
        self.a_blue.delete( 0, 10)
        self.a_blue.insert( "end", s_blue)
        self.a_blue_dec_lbl.configure( text=str(int(s_blue, 16)))
        self.a_the_color_lbl.configure( background= s_red + s_green + s_blue)
        __i_complete = int(i_number / 16)
        __i_rest = i_number - (__i_complete * 16)
        # print( f'number= {i_number} -> complete= {__i_complete} rest= {__i_rest}')
        if i_number > 15:
            self.a_btn_x_lbl.configure( text=str(__i_complete))
        else:
            self.a_btn_x_lbl.configure( text="0")

        self.a_btn_y_lbl.configure( text=str(__i_rest))

    # ####################### __mw_clock_in_window_bar ########################
    def __mw_clock_in_window_bar( self):
        """ Print the date and times in menu bar of the main windows """
        __now = datetime.now()
        # dd/mm/YY H:M:S
        __s_date_time = __now.strftime( "%d/%m/%Y %H:%M:%S")
        __s_windows_title = ' ' + self.a_list_application_info[0] + '                                           ' + __s_date_time
        self.w_main_windows.title( __s_windows_title)
        self.w_main_windows.after( 1000, self.__mw_clock_in_window_bar)

    # ####################### __mw_print_widget_under_mouse ########################
    def __mw_print_widget_under_mouse(self, root):
        """ Print the widget type """
        __i_pos_x,__i_pos_y = root.winfo_pointerxy()
        __a_widget = root.winfo_containing(__i_pos_x,__i_pos_y)
        if __a_widget:
            if "canvas" in str( __a_widget):
                # x,y = a_widget.winfo_pointerxy()
                # print('{}, {}'.format(x, y))
                __i_pos_x = __i_pos_x - (root.winfo_rootx() + 4)
                if (__i_pos_x < 0):
                    __i_pos_x = 0
                if (__i_pos_x > 640):
                    __i_pos_x = 640
                __i_pos_y = __i_pos_y - (root.winfo_rooty() + 98 + 15 + 8)  # 98 = top bar; 15 = separator; 8 = ???
                if (__i_pos_y < 0):
                    __i_pos_y = 0
                if (__i_pos_y > 400):
                    __i_pos_y = 400
                self.a_mouse_pos_x.delete( 0, 10)
                self.a_mouse_pos_x.insert( "end", str(__i_pos_x))
                self.a_mouse_pos_y.delete( 0, 10)
                self.a_mouse_pos_y.insert( "end", str(__i_pos_y))
                if self.a_work_img:
                    i_offset = self.a_work_img.getpixel((__i_pos_x/2, __i_pos_y/2))
                    self.a_color_lbl.configure( text=str(i_offset))
                    self.a_scb_lbl.configure( text=str(int(i_offset/16)))
                    # self.a_pic_color_lbl.configure(background= s_red + s_green + s_blue)
                    # self.a_image
                # if self.a_bmp_image_file:
                #     a_pixel = self.a_bmp_image_file.map.read_byte(__i_pos_x, __i_pos_y)
                #     __i_pos_x = __i_pos_x
            else:
                self.a_mouse_pos_x.delete( 0, 10)
                self.a_mouse_pos_y.delete( 0, 10)

        root.after(500, self.__mw_print_widget_under_mouse, root)

    # ##########################################################################################
    # #######################                                           ########################
    # #######################                   PUBLIC                  ########################
    # #######################                                           ########################
    # ##########################################################################################

    # ####################### mw_create_main_window ########################
    def mw_create_main_window( self):
        """ Design the main windows """

        __s_windows_size_and_position = ( str( self.i_main_window_width) + 'x' + str( self.i_main_window_height) + '+' + str( self.i_main_window_x) + '+' + str( self.i_main_window_y) )
        self.w_main_windows.geometry( __s_windows_size_and_position)  # dimension + position x/y a l'ouverture
        self.w_main_windows.update()

        # Create 2 lines : icons, empty
        a_top_bar_frame = tk_gui.Frame( self.w_main_windows, padx=0, pady=2, background=constant.BACKGROUD_COLOR_UI)    # background='darkgray'
        a_top_bar_frame.place(x=2, y=0, width=self.i_main_window_width-4, height=98 )   # fill :  must be 'none', 'x', 'y', or 'both'

        self.c_mains_icon_bar = MyMainWindowIconsBar( self, self.w_main_windows, self.a_list_application_info, a_top_bar_frame)
        self.c_mains_icon_bar.mwib_create_top_bar_icons( 1)

        # Create picture frame
        self.__mw_picture_zone()

        # Create palette frame
        self.__mw_palette_zone()

        if self.s_platform == "Windows":
            self.__mw_clock_in_window_bar()

    # ####################### mw_load_main_window ########################
    def mw_load_main_window(self):
        """ load a picture and fill the interface """
        s_filename = open_file(self)
        if s_filename:
            print( '\nLoading : ' + s_filename)
            # resize the original bmp from 320x200 to 640x400
            self.a_work_img = Image.open(s_filename)
            width, height = self.a_work_img.size
            if width != 320 and height != 200:
                return False

            width = width * 2
            height = height * 2
            self.a_work_img = self.a_work_img.resize((width,height))
            self.a_work_img.save(s_filename + ".bmp")

            self.a_bmp_image_file = Image.open(s_filename + ".bmp")
            w, h = self.a_bmp_image_file.size
            
            if self.a_image is not None:          # if an image was already loaded
                self.a_canvas.delete(self.a_image)  # remove the previous image

            # a_photo_image = plt.imread( 'G:\Collector\_Apple IIgs\_DiskCrackBand_\Iron_Lord\dessin.bmp\medite.ch.bmp')
            # a_label_picture = Label( None, text='', width=320, image=a_photo_image)  # add , background='darkgray' to show where is the cell

            self.a_render = ImageTk.PhotoImage(self.a_bmp_image_file) #must keep a reference to this
            self.a_image = self.a_canvas.create_image(((w/2), (h/2)), image=self.a_render)

            a_palette_list = self.a_work_img.getpalette()
            print( 'Palette :')

            i_element = 0
            i_to = 0
            for i_loop in range( 0, 16, 1):
                i_from = i_to
                i_to = i_to + 48
                if i_loop < 10:
                    s_my_hex = "0" + str(i_loop) + " "
                else:
                    s_my_hex = str(i_loop) + " "

                for i_index in range( i_from, i_to, 3):
                    if (a_palette_list[ i_index] > 15):
                        s_red = f'#{a_palette_list[ i_index]:X}'
                    else:
                        s_red = f'#0{a_palette_list[ i_index]:X}'
                    if (a_palette_list[ i_index + 1] > 15):
                        s_green = f'{a_palette_list[ i_index + 1]:X}'
                    else:
                        s_green = f'0{a_palette_list[ i_index + 1]:X}'
                    if (a_palette_list[ i_index + 2] > 15):
                        s_blue = f'{a_palette_list[ i_index + 2]:X}'
                    else:
                        s_blue = f'0{a_palette_list[ i_index + 2]:X}'
                    s_my_hex = s_my_hex + s_red + s_green + s_blue + " "

                    a_button_color = self.a_palette_button_lst[i_element]
                    config_palette_bottom_with_arg = partial( self.__mw_color_button, int(i_index / 3), s_red, s_green, s_blue)
                    a_button_color.configure( command=config_palette_bottom_with_arg)
                    a_button_color.configure( background=s_red + s_green + s_blue)
                    i_element += 1

                    if i_index == 0:
                        self.__mw_color_button( i_index, s_red, s_green, s_blue)

                self.w_main_windows.update()
                print( s_my_hex)

            self.w_main_windows.update()
        else:
            return False
        print()

        return True

    # ####################### mw_get_main_window ########################
    def mw_get_main_window( self):
        """ Return the window widget of the main window """
        return self.w_main_windows

    # ####################### mw_get_main_window_height ########################
    def mw_get_main_window_height( self):
        """ Return height of the main window """
        self.i_main_window_height = self.w_main_windows.winfo_height()
        return int( self.i_main_window_height)

    # ####################### mw_get_main_window_width ########################
    def mw_get_main_window_width( self):
        """ Return width of the main window """
        self.i_main_window_width = self.w_main_windows.winfo_width()
        return int( self.i_main_window_width)

    # ####################### mw_get_main_window_pos_x ########################
    def mw_get_main_window_pos_x( self):
        """ Return position X of the main window """
        self.i_main_window_x = self.w_main_windows.winfo_x()
        return int( self.i_main_window_x)

    # ####################### mw_get_main_window_pos_y ########################
    def mw_get_main_window_pos_y( self):
        """ Return position Y of the main window """
        self.i_main_window_y = self.w_main_windows.winfo_y()
        return int( self.i_main_window_y)
