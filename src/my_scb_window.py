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

""" Module de gestion SCB editor """

# ###############################################################################################
#                                   PYLINT
# Disable C0301 = Line too long (80 chars by line is not enough)
# pylint: disable=line-too-long
# ###############################################################################################

import platform
import tkinter as tk_gui
import inspect
from typing import TYPE_CHECKING

from tkinter import Label, Button, Toplevel, Scale, Radiobutton, IntVar, font, Canvas, Checkbutton
from tkinter.ttk import Combobox
from PIL import ImageTk

import src.my_constants as constant
from .my_log_an_usage import MyLogAnUsage
from .my_icon_pictures import MyIconPictures
from .my_alert_window import MyAlertWindow

if TYPE_CHECKING:
    from .my_main_window import MyMainWindow

# __name__ = "MyScbPalletWindow"

# ###############################################################################################
# #######========================= constant private =========================
# ###############################################################################################
# #######========================= SSB Pallet Dialogs Window =========================
class MyScbPalletWindow:
    """ Create the scb pallet Windows of the application """
    # pylint: disable=too-many-instance-attributes
    # number is reasonable in this case these are all the icons of the main windows and the application icons

    # ANSWER_CANCEL = 0
    # ANSWER_OK = 1
    SCB_NUMBER_LST = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
    MIDDLE_FRAME_HEIGHT = 40
    UP_MIDDLE_FRAME_HEIGHT =  30 + MIDDLE_FRAME_HEIGHT + MIDDLE_FRAME_HEIGHT
    DOWN_MIDDLE_FRAME_HEIGHT =  30 + MIDDLE_FRAME_HEIGHT
    BOTTOM_FRAME_HEIGHT = 34

    # ####################### __init__ ########################
    def __init__( self, a_main_window_image, a_the_main_window: "MyMainWindow", a_scb_cnvs_rect_lst, i_selected_pallet_line):
        """
            all this parameter are created in main()
            a_main_window : the parent windows
        """
        self.a_main_window: "MyMainWindow"  = a_the_main_window
        self.a_main_window_image            = a_main_window_image
        self.a_scb_cnvs_rect_lst            : list = a_scb_cnvs_rect_lst
        self.i_selected_pallet_line         = i_selected_pallet_line

        self.c_the_log: "MyLogAnUsage"      = MyLogAnUsage( None)
        self.c_the_icons: "MyIconPictures"  = MyIconPictures( None)
        self.s_platform                     = platform.system()
        self.w_scb_window                   = None
        self.a_work_img                     = None

        self.a_original_part_image          = None
        self.s_original_filename            = ''
        self.a_list_device_combo            : list = None
        self.i_index_in_a_scb_cnvs_rect_lst = 0

        self.a_mouse_live_pos_y_lbl         : Label = None
        self.i_height = 0
        self.i_width = 0
        self.i_position_x = 0
        self.i_position_y = 0
        self.scb_background = 'darkgray'
        self.i_selected_pallet = -1                     # source of index pallet to copy
        self.i_selected_pallet_in_main_windows = -1     # target of destination index
        self.a_zoom_cnv                     : Canvas = None
        self.a_zoom_work_img                : ImageTk.PhotoImage = None
        self.a_zoom_work_img_original       : ImageTk.PhotoImage = None
        self.a_render_zoom                  : ImageTk.PhotoImage = None
        self.var_rdx_btn                    : IntVar = IntVar()
        self.a_scb_cnvs                     : list = None
        self.a_the_color_new_lbl            : Label = None
        self.a_frontier_scale               : Scale = None
        self.a_show_var                     : IntVar = IntVar( value = 0)
        self.a_show_chk                     : Checkbutton = None
        self.a_pallet_to_begin_combo        : Combobox = None
        self.a_pallet_to_end_combo          : Combobox = None
        self.a_down_begin_lbl               : Label = None
        self.a_pallet_to_all_combo          : Combobox = None

    # ####################### __scbw_do_leave_scb_dialog ########################
    def __scbw_do_leave_scb_dialog( self):
        """ Do commun stuff when press button ok or cancel on the scb window """
        self.a_zoom_cnv.unbind( '<Motion>')
        self.a_zoom_cnv.unbind( '<Button>')
        self.w_scb_window.grab_release()
        self.w_scb_window.destroy()

    # ####################### __scbw_change_pallet_for_lines ########################
    def __scbw_change_pallet_for_lines( self, i_new_pallet_to_use, i_from, i_to):
        """ Change the pallet used by a scb to another one """
        self.c_the_log.add_string_to_log( 'scbw_change_pallet_for_lines(): i_new_pallet_to_use= ' + str(i_new_pallet_to_use) + ' from line: ' + str(i_from) + ' to line: ' + str(i_to))
        for i_picture_line_y in range( i_from, i_to, 1):
            for i_loop in range( 0, 320, 1):
                i_first_color_offset = self.a_original_part_image.getpixel( ( i_loop, i_picture_line_y))
                i_first_color_offset = i_first_color_offset - (self.i_selected_pallet_line * 16)
                i_first_color_offset = i_first_color_offset + (i_new_pallet_to_use * 16)
                self.a_original_part_image.putpixel( ( i_loop, i_picture_line_y), i_first_color_offset)

    # ####################### __scbw_scb_ok_button ########################
    def __scbw_scb_ok_button( self):
        """ Button ok of the scb window """
        b_result = False
        # self.c_the_log.add_string_to_log( f'scbw_scb_ok_button() i_selected_pallet_line= {self.i_selected_pallet_line}')
        a_cnvs_rect = self.a_scb_cnvs_rect_lst[self.i_index_in_a_scb_cnvs_rect_lst]
        _, f_y0, _, f_y1 = self.a_scb_cnvs.coords( a_cnvs_rect)
        f_y0 = (f_y0 + 0.5) / 2
        f_y1 = (f_y1 + 0.5) / 2
        # self.c_the_log.add_string_to_log( f'scbw_scb_ok_button() from line: {f_y0:0.0f} to {f_y1:0.0f}'.format(f_y0, f_y1))
        if self.var_rdx_btn.get() == 1:
            i_top_selected_pallet_line = int( self.a_pallet_to_begin_combo.get())
            i_bottom_selected_pallet_line = int( self.a_pallet_to_end_combo.get())
            # self.c_the_log.add_string_to_log( f'scbw_scb_ok_button() combo up= {i_top_selected_pallet_line} down= {i_bottom_selected_pallet_line}')
            if self.i_selected_pallet_line != i_top_selected_pallet_line:
                # Change the pallet on top part of the image band
                self.__scbw_change_pallet_for_lines( i_top_selected_pallet_line, int(f_y0), int(f_y0) + int(self.a_frontier_scale.get())+1)
                self.__scbw_do_leave_scb_dialog()
                b_result = True
            if self.i_selected_pallet_line != i_bottom_selected_pallet_line:
                # Change the pallet on bottom part of the image band
                self.__scbw_change_pallet_for_lines( i_bottom_selected_pallet_line, int(f_y0) + int(self.a_frontier_scale.get() + 1), int(f_y1)+1)
                self.__scbw_do_leave_scb_dialog()
                b_result = True
        else:
            i_top_selected_pallet_line = int( self.a_pallet_to_all_combo.get())
            # self.c_the_log.add_string_to_log( f'scbw_scb_ok_button() combo = {i_top_selected_pallet_line}')
            if self.i_selected_pallet_line != i_top_selected_pallet_line:
                self.__scbw_change_pallet_for_lines( i_top_selected_pallet_line, int(f_y0), int(f_y1)+1)
                self.__scbw_do_leave_scb_dialog()
                b_result = True

        if b_result is True:
            self.c_the_log.add_string_to_log( 'Do change scb close with ok')
            self.a_main_window.mw_update_main_window( self.s_original_filename, self.a_original_part_image)
            w_parent_window = self.a_main_window.mw_get_main_window()
            w_parent_window.update()
            self.a_main_window_image.mwi_click_in_picture_center()

    # ####################### __scbw_scb_cancel_button ########################
    def __scbw_scb_cancel_button( self):
        """ Button cancel of the scb window """
        self.__scbw_do_leave_scb_dialog()
        self.c_the_log.add_string_to_log( 'Do SCB edit close with cancel')

    # ####################### __invert_rectangle_on_canvas ########################
    def __invert_rectangle_on_canvas( self):
        """ Invert the color indices in the selected rectangle for Apple II GS SCB format """
        i_height = int(self.a_frontier_scale.get()) * 3
        i_width = self.a_zoom_work_img.width
        # self.c_the_log.add_string_to_log( 'invert_rectangle_on_canvas zoom: height= ' + str( self.a_zoom_work_img.height) + '  width= ' + str( self.a_zoom_work_img.width))
        # self.c_the_log.add_string_to_log( 'invert_rectangle_on_canvas i_height= ' + str( i_height) + '  i_width= ' + str( i_width))

        # For each line in the rectangle
        for y in range(i_height):
            # Determine which palette line is used for this line
            # Example: palette_line = self.i_selected_pallet_line
            palette_line = self.i_selected_pallet_line
            base_index = palette_line * 16
            for x in range(i_width):
                idx = self.a_zoom_work_img.getpixel((x, y))
                # Only invert if index is in the current palette line
                if base_index <= idx < base_index + 16:
                    # Invert index within palette line
                    new_idx = base_index + (15 - (idx - base_index))
                    self.a_zoom_work_img.putpixel((x, y), new_idx)

        # Update the PhotoImage
        self.a_render_zoom = ImageTk.PhotoImage(self.a_zoom_work_img)
        self.a_zoom_cnv.create_image(0, 0, anchor='nw', image=self.a_render_zoom)
        self.a_zoom_cnv.image = self.a_render_zoom

    # ####################### __scbw_print_coord_under_mouse ########################
    def __scbw_print_coord_under_mouse( self, event):
        """ Show live position of the mouse in the loaded picture """
        i_pos_x = event.x
        i_pos_y = event.y
        # Use only the pair values, click is done in the picture zoomed x 2
        if i_pos_y & 3:
            i_pos_y -= 3
        if i_pos_x & 3:
            i_pos_x -= 3

        self.a_mouse_live_pos_y_lbl.configure( text=str( int(event.y / 3)))

        a_pallet_list = self.a_zoom_work_img.getpalette()
        # 3 * is to avoid to do 2 multiplications later
        palette_index = 3 * self.a_zoom_work_img.getpixel((i_pos_x, i_pos_y))
        # without the 3 * we would have: 3*palette_index:3*palette_index+3
        i_red, i_green, i_blue = a_pallet_list[palette_index:palette_index+3]
        self.a_the_color_new_lbl.configure( background= f"#{i_red:02x}{i_green:02x}{i_blue:02x}")

    # ####################### __scbw_show_chk_toggled ########################
    def __scbw_show_chk_toggled( self):
        """ Toggle the visibility of the rectangle on the canvas """
        self.a_zoom_work_img = self.a_zoom_work_img_original.copy()
        if self.a_show_var.get() == 1:
            self.__invert_rectangle_on_canvas()
        else:
            self.a_render_zoom = ImageTk.PhotoImage( self.a_zoom_work_img)
            self.a_zoom_cnv.create_image( 0, 0, anchor='nw', image=self.a_render_zoom)
            self.a_zoom_cnv.image = self.a_render_zoom

    # ####################### __scbw_update_begin ########################
    def __scbw_update_begin( self, s_value):
        """Called when the scale is moved. Update the label, Invert rectangle if checkbox is set."""
        i_value = int( s_value)
        if len( s_value) == 1 and i_value < 9:
            self.a_down_begin_lbl.configure( text="  " + str( i_value + 1))
        else:
            self.a_down_begin_lbl.configure( text=str( i_value + 1))

        # Always restore the original before inverting
        self.a_zoom_work_img = self.a_zoom_work_img_original.copy()
        if self.a_show_var.get() == 1:   # Checkbox is checked
            self.__invert_rectangle_on_canvas()
        else:
            # Just redraw the original image
            self.a_render_zoom = ImageTk.PhotoImage(self.a_zoom_work_img)
            self.a_zoom_cnv.create_image(0, 0, anchor='nw', image=self.a_render_zoom)
            self.a_zoom_cnv.image = self.a_render_zoom

    # ####################### __scbw_click_on_picture ########################
    def __scbw_click_on_picture( self, event):
        """ Show position of the mouse in the loaded picture and repair SCB to draw a rect """
        self.a_frontier_scale.set( int( event.y / 3) )
        self.a_down_begin_lbl.configure( text=str( int( event.y / 3) + 1))

    # ####################### __scbw_selection_rdx_btn ########################
    def __scbw_selection_rdx_btn( self):
        """ Change the state of the comboboxes and scale when the radio button is selected """
        if self.var_rdx_btn.get() == 1:
            self.a_pallet_to_all_combo.config( state="disabled")
            self.a_frontier_scale.config( state="normal")
            self.a_pallet_to_begin_combo.config( state="normal")
            self.a_pallet_to_end_combo.config( state="normal")
        else:
            self.a_pallet_to_all_combo.config( state="normal")
            self.a_frontier_scale.config( state="disabled")
            self.a_pallet_to_begin_combo.config( state="disabled")
            self.a_pallet_to_end_combo.config( state="disabled")

    # ####################### __scbw_scb_block_top ########################
    def __scbw_scb_block_top( self, top_frame, i_part_width, i_part_height):
        """ Create a SCB top dialog """
        self.a_zoom_cnv = Canvas( top_frame, width=i_part_width * 3, height=i_part_height * 3, background=constant.BACKGROUD_COLOR_UI, borderwidth=0, highlightthickness=0)
        self.a_zoom_cnv.create_image( 0, 0, anchor='nw', image=self.a_render_zoom)
        # if self.s_platform in [ "Darwin", "Linux" ]:
        #     self.a_zoom_lbl.pack( side='left', padx=4)
        # else:
        self.a_zoom_cnv.pack( side='left', padx=4)

        self.a_zoom_cnv.bind( '<Motion>', self.__scbw_print_coord_under_mouse)
        self.a_zoom_cnv.bind( '<Button>', self.__scbw_click_on_picture)

    # ####################### __scbw_scb_block_middle_up ########################
    def __scbw_scb_block_middle_up( self, middle_up_frame, up_middle_middle_frame, middle_middle_frame, i_part_height):
        """ Create a SCB middle up dialog """
        if self.s_platform == "Darwin":
            a_split_rdx_btn = Radiobutton( up_middle_middle_frame, text="Split this scb to two scb :", variable=self.var_rdx_btn, value=1, command=self.__scbw_selection_rdx_btn, background=constant.BACKGROUD_COLOR_UI, font=font.Font( size=10))
        elif self.s_platform == "Linux":
            a_split_rdx_btn = Radiobutton( up_middle_middle_frame, text="Split this scb to two scb :", variable=self.var_rdx_btn, value=1, command=self.__scbw_selection_rdx_btn, borderwidth=0, background=constant.BACKGROUD_COLOR_UI, font=font.Font( size=10))
        else:
            a_split_rdx_btn = Radiobutton( up_middle_middle_frame, text="Split this scb to two scb :", variable=self.var_rdx_btn, value=1, command=self.__scbw_selection_rdx_btn, background=constant.BACKGROUD_COLOR_UI, font=font.Font( size=10))
        a_split_rdx_btn.pack( side='left', padx=4 )
        self.var_rdx_btn.set(1)     # initializing the choice, to the Split

        a_label = Label( middle_up_frame, text="The pallet used for this SCB is " + str(self.i_selected_pallet_line) + ".", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black', font=font.Font( size=10))
        a_label.pack( side='left', padx=4)
        a_label = Label( middle_up_frame, text="Mouse live position on Y :", height=1, justify='right', background=constant.BACKGROUD_COLOR_UI, foreground='black', font=font.Font( size=10))
        a_label.pack( side='left', padx=4)
        self.a_mouse_live_pos_y_lbl = Label( middle_up_frame, text="   ", width=3, justify="left", background=constant.BACKGROUD_COLOR_UI, foreground='black', font=font.Font( size=10))
        self.a_mouse_live_pos_y_lbl.pack( side='left', padx=4)
        a_label = Label( middle_up_frame, text="Color under the cursor is ", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black', font=font.Font( size=10))
        a_label.pack( side='left', padx=4)
        self.a_the_color_new_lbl = Label( middle_up_frame, text=None, width=8, borderwidth=2, background='black', foreground='black', font=font.Font( size=10))
        self.a_the_color_new_lbl.pack( side='left', padx=4)

        a_label = Label( middle_middle_frame, text="The UPPER part, from 0 to", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='left', padx=2)
        if self.s_platform == "Linux":
            self.a_frontier_scale = Scale( middle_middle_frame, from_=0, to=i_part_height-2, length=480, command=self.__scbw_update_begin, orient='horizontal', background=constant.BACKGROUD_COLOR_UI, highlightbackground='light grey', borderwidth=0, highlightthickness=0, troughcolor='light grey')
        else:
            self.a_frontier_scale = Scale( middle_middle_frame, from_=0, to=i_part_height-2, length=500, command=self.__scbw_update_begin, orient='horizontal', background=constant.BACKGROUD_COLOR_UI, highlightbackground='light grey', borderwidth=0, highlightthickness=0, troughcolor='light grey')
        self.a_frontier_scale.pack( side='left', padx=2)
        self.a_frontier_scale.set(int(i_part_height/3))
        a_label = Label( middle_middle_frame, text="use the pallet line (scb number)", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='left', padx=2)
        self.a_pallet_to_begin_combo = Combobox( middle_middle_frame, values=self.SCB_NUMBER_LST, width=3, state="readonly")
        self.a_pallet_to_begin_combo.pack( side='left', padx=4)
        self.a_pallet_to_begin_combo.current( self.i_selected_pallet_line)
        self.a_show_chk = Checkbutton( middle_middle_frame, text = "Show", variable = self.a_show_var, onvalue = 1, offvalue = 0, height=1, width=5, background=constant.BACKGROUD_COLOR_UI, foreground='black', command=self.__scbw_show_chk_toggled )
        self.a_show_chk.pack( side='left', padx=2)

    # ####################### __scbw_scb_block_middle_down ########################
    def __scbw_scb_block_middle_down( self, middle_down_frame, up_middle_down_frame, down_middle_down_frame, i_part_height):
        """ Create a SCB middle down dialog """
        self.a_pallet_to_end_combo = Combobox( middle_down_frame, values=self.SCB_NUMBER_LST, width=3, state="readonly")
        self.a_pallet_to_end_combo.pack( side='right', padx=4)
        self.a_pallet_to_end_combo.current( self.i_selected_pallet_line)
        a_label = Label( middle_down_frame, text=" to " + str(i_part_height-1) + " will use the pallet line (scb number)", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='right', padx=2)
        self.a_down_begin_lbl = Label( middle_down_frame, text=str(int(i_part_height/3)+1), height=1, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        self.a_down_begin_lbl.pack( side='right')
        a_label = Label( middle_down_frame, text="The LOWER part, from ", height=1, anchor="e", background=constant.BACKGROUD_COLOR_UI)
        a_label.pack( side='right', padx=2)
        if self.s_platform == "Darwin":
            a_pallet_rdx_btn = Radiobutton( up_middle_down_frame, text="Change the pallet used by this scb :", variable=self.var_rdx_btn, value=2, command=self.__scbw_selection_rdx_btn, background=constant.BACKGROUD_COLOR_UI, font=font.Font( size=10))
        elif self.s_platform == "Linux":
            a_pallet_rdx_btn = Radiobutton( up_middle_down_frame, text="Change the pallet used by this scb :", variable=self.var_rdx_btn, value=2, command=self.__scbw_selection_rdx_btn, borderwidth=0, background=constant.BACKGROUD_COLOR_UI, font=font.Font( size=10))
        else:
            a_pallet_rdx_btn = Radiobutton( up_middle_down_frame, text="Change the pallet used by this scb :", variable=self.var_rdx_btn, value=2, command=self.__scbw_selection_rdx_btn, background=constant.BACKGROUD_COLOR_UI, font=font.Font( size=10))
        a_pallet_rdx_btn.pack( side='left', padx=4 )
        a_label = Label( down_middle_down_frame, text="Selected the new pallet instead of " + str(self.i_selected_pallet_line) + " use :", height=1, anchor='center', background=constant.BACKGROUD_COLOR_UI, foreground='black')
        a_label.pack( side='left', padx=4)
        self.a_pallet_to_all_combo = Combobox( down_middle_down_frame, values=self.SCB_NUMBER_LST, width=3, state="readonly")
        self.a_pallet_to_all_combo.pack( side='left', padx=4)
        self.a_pallet_to_all_combo.current( self.i_selected_pallet_line)
        self.a_pallet_to_all_combo.config( state="disabled")

    # ####################### __scbw_scb_block_bottom ########################
    def __scbw_scb_block_bottom( self, button_frame):
        """ Create a SCB bottom dialog """
        # width size of a button is number of charracters 15 + 4 charracters
        if self.s_platform == "Darwin":
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 4, compound='center', command=self.__scbw_scb_ok_button, relief='raised', highlightbackground=constant.COLOR_WINDOWS_MENU_BAR)
            a_ok_btn.pack( side='right', padx=2, pady=2 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 4, compound='center', command=self.__scbw_scb_cancel_button, relief='raised', background=self.scb_background)
            a_cancel_btn.pack( side='right', padx=2, pady=2 )
        else:
            a_ok_btn = Button( button_frame, text='Ok', width=constant.DEFAULT_BUTTON_WIDTH + 4, compound='center', command=self.__scbw_scb_ok_button, relief='raised', background=self.scb_background)
            a_ok_btn.pack( side='right', padx=4, pady=4 )
            a_cancel_btn = Button( button_frame, text='Cancel', width=constant.DEFAULT_BUTTON_WIDTH + 4, compound='center', command=self.__scbw_scb_cancel_button, relief='raised', background=self.scb_background)
            a_cancel_btn.pack( side='right', padx=4, pady=4 )

    # ####################### __scbw_scb_block ########################
    def __scbw_scb_block( self, i_part_width, i_part_height):
        """ Create a SCB dialog """
        # Define the GUI
        top_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.i_height, relief='flat', background=constant.BACKGROUD_COLOR_UI)   # darkgray or light grey
        top_frame.pack( side='top', fill='both', expand=False)   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_up_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        middle_up_frame.pack( side='top', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_up_frame.pack_propagate( False)

        up_middle_middle_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.UP_MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        up_middle_middle_frame.pack( side='top', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        up_middle_middle_frame.pack_propagate( False)
        middle_down_frame = tk_gui.Frame( up_middle_middle_frame, width=self.i_width, height=self.MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        middle_down_frame.pack( side='bottom', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_down_frame.pack_propagate( False)
        middle_middle_frame = tk_gui.Frame( up_middle_middle_frame, width=self.i_width, height=self.MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        middle_middle_frame.pack( side='bottom', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_middle_frame.pack_propagate( False)

        up_middle_down_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.DOWN_MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        up_middle_down_frame.pack( side='top', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        up_middle_down_frame.pack_propagate( False)
        down_middle_down_frame = tk_gui.Frame( up_middle_down_frame, width=self.i_width, height=self.MIDDLE_FRAME_HEIGHT, relief='flat', background=constant.BACKGROUD_COLOR_UI)
        down_middle_down_frame.pack( side='bottom', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        down_middle_down_frame.pack_propagate( False)

        button_frame = tk_gui.Frame( self.w_scb_window, width=self.i_width, height=self.BOTTOM_FRAME_HEIGHT, relief='flat', background=constant.COLOR_WINDOWS_MENU_BAR)
        button_frame.pack( side='bottom', fill='both')   # fill :  must be 'none', 'x', 'y', or 'both'
        middle_down_frame.pack_propagate( False)

        # #### TOP #####
        self.__scbw_scb_block_top( top_frame, i_part_width, i_part_height)

        # #### MIDDLE #####
        self.__scbw_scb_block_middle_up( middle_up_frame, up_middle_middle_frame, middle_middle_frame, i_part_height)

        self.__scbw_scb_block_middle_down( middle_down_frame, up_middle_down_frame, down_middle_down_frame, i_part_height)

        # #### BOTTOM #####
        self.__scbw_scb_block_bottom( button_frame)

    # ####################### __scbw_set_window_size ########################
    def __scbw_set_window_size( self):
        """ Set the size of the configuration windows (+16 for any line added in a_middle_text) """
        # self.c_the_log.add_string_to_log( "computer height =" + str( 30 + self.i_height + (self.MIDDLE_FRAME_HEIGHT * 3) + self.BOTTOM_FRAME_HEIGHT))
        # i_height of the picture part + 30 windows title + 3 frames for action widgets + 1 frame for cancel and ok button
        # self.i_height += 30 +  (self.MIDDLE_FRAME_HEIGHT * 3) + self.BOTTOM_FRAME_HEIGHT
        self.i_height += 30 + self.MIDDLE_FRAME_HEIGHT + self.UP_MIDDLE_FRAME_HEIGHT + self.DOWN_MIDDLE_FRAME_HEIGHT

        if self.s_platform == "Linux":
            self.i_width = 968
            self.i_height += 10  #374
        elif self.s_platform == "Darwin":
            self.i_width = 968
            self.i_height += 0  #306
        elif self.s_platform == "Windows":
            self.i_width = 968
            self.i_height += 0  #376

        self.i_position_x = self.a_main_window.mw_get_main_window_pos_x() + int((self.a_main_window.mw_get_main_window_width() - self.i_width) / 2)
        self.i_position_y = self.a_main_window.mw_get_main_window_pos_y() + int((self.a_main_window.mw_get_main_window_height() - self.i_height) / 2)
        self.i_position_y = max(self.i_position_y, 0)

        s_windows_size_and_position = ( str( self.i_width) + 'x' + str( self.i_height) + '+' + str( self.i_position_x) + '+' + str( self.i_position_y))
        self.w_scb_window.geometry( s_windows_size_and_position)  # dimension + position x/y a l'ouverture

        # lock resize of main window
        self.w_scb_window.minsize( self.i_width, self.i_height)
        self.w_scb_window.maxsize( self.i_width, self.i_height)
        # no resize for both directions
        self.w_scb_window.resizable( False, False)
        self.w_scb_window.iconphoto( True, self.c_the_icons.get_app_photo())

        self.c_the_log.add_string_to_log( '\nscbw_set_window_size() : geometry  ' + s_windows_size_and_position + '\n')

    # ##########################################################################################
    # https://manytools.org/hacker-tools/ascii-banner/
    #
    #  ######  #     # ######  #       ###  #####
    #  #     # #     # #     # #        #  #     #
    #  #     # #     # #     # #        #  #
    #  ######  #     # ######  #        #  #
    #  #       #     # #     # #        #  #
    #  #       #     # #     # #        #  #     #
    #  #        #####  ######  ####### ###  #####
    #
    # ##########################################################################################

    # ####################### scbw_create_scb_window ########################
    def scbw_create_scb_window( self, s_filename, a_original_image, a_scb_cnvs, i_index_in_a_scb_cnvs_rect_lst):
        """ Design the scb box dialog """
        self.c_the_log.add_string_to_log( f"{inspect.currentframe().f_code.co_name}")
        if a_original_image and a_scb_cnvs:
            self.s_original_filename = s_filename
            self.a_original_part_image = a_original_image
            self.a_scb_cnvs = a_scb_cnvs
            self.i_index_in_a_scb_cnvs_rect_lst = i_index_in_a_scb_cnvs_rect_lst

            # Prepare the picture band
            # a_cnvs_rect = self.a_scb_cnvs_rect_lst[self.i_index_in_a_scb_cnvs_rect_lst]
            # self.c_the_log.add_string_to_log( f' a_cnvs_rect= {a_cnvs_rect}')
            _f_x0, f_y0, _f_x1, f_y1 = self.a_scb_cnvs.coords( self.a_scb_cnvs_rect_lst[self.i_index_in_a_scb_cnvs_rect_lst])

            if f_y0 == f_y1:
                c_alert_windows = MyAlertWindow( self.a_main_window, self.a_main_window.mw_get_application_info())
                c_alert_windows.aw_create_alert_window( 3, "SCB on one line", "Can't use SCB Edit dialog.\n\nUse the scroller and\nvalidate with the button\n'Change pallet line number'.")
                return

            w_parent_window = self.a_main_window.mw_get_main_window()
            self.w_scb_window = Toplevel( w_parent_window)
            self.w_scb_window.lift( aboveThis=w_parent_window)
            # window dialog is on top of self.a_main_window.mw_get_main_window()
            self.w_scb_window.grab_set()
            self.w_scb_window.focus_set()
            self.w_scb_window.configure( background=constant.BACKGROUD_COLOR_UI)

            # ####################### disable_event ########################
            # disable click on the X on top right of the window
            def disable_event():
                self.__scbw_scb_cancel_button()
                # pass

            self.w_scb_window.protocol( "WM_DELETE_WINDOW", disable_event)
            self.w_scb_window.title( ' SCB edit ')

            # self.c_the_log.add_string_to_log(f' rect       size is: ({f_x0:0.1f} {f_y0:0.1f}) ({f_x1:0.1f} {f_y1:0.1f}) {int(f_y1 - f_y0 + 1):d} lines')
            # width, height = a_original_image.size
            # self.c_the_log.add_string_to_log( f' org  image size is: {width:d} {height:d}'.format(width, height))

            f_y0 = f_y0  / 2
            f_y1 = (f_y1  / 2) + 1
            # self.c_the_log.add_string_to_log(f' rect round size is: ({int(f_x0):d} {int(f_y0):d}) ({int(f_x1):d} {int(f_y1):d}) {int(f_y1 - f_y0 + 1):d} lines')

            # i_box_top = (0, int(f_y0), 320, int(f_y1)) # left, upper, width, height
            a_part_image = a_original_image.crop( (0, int(f_y0), 320, int(f_y1)) )   # left, upper, width, height
            # width, height = a_original_image.size
            # self.c_the_log.add_string_to_log( f' org  image size is: {width:d} {height:d}'.format(width, height))

            width, height = a_part_image.size
            # self.c_the_log.add_string_to_log( f' part image size is: {width:d} {height:d}'.format(width, height))
            self.a_zoom_work_img = a_part_image.resize( (width * 3, height * 3))     # Total of zoom is x 3
            self.a_render_zoom = ImageTk.PhotoImage( self.a_zoom_work_img)
            # self.c_the_log.add_string_to_log( ' a_zoom_work_img: height= ' + str( self.a_zoom_work_img.height) + '  width= ' + str( self.a_zoom_work_img.width))
            # self.c_the_log.add_string_to_log( '   a_render_zoom: height= ' + str( self.a_render_zoom.height()) + '  width= ' + str( self.a_render_zoom.width()))

            # After creating self.a_zoom_work_img
            self.a_zoom_work_img_original = self.a_zoom_work_img.copy()

            self.i_width = width * 3
            self.i_height = height * 3

            self.__scbw_scb_block( width, height)
            self.__scbw_set_window_size()
            # self.c_the_log.add_string_to_log( "")

            self.w_scb_window.bind("<Escape>", lambda event: self.__scbw_scb_cancel_button())
            self.w_scb_window.bind("<Return>", lambda event: self.__scbw_scb_ok_button())

            self.w_scb_window.mainloop()

            self.w_scb_window.unbind("<Escape>")
            self.w_scb_window.unbind("<Return>")

            # self.w_scb_window.destroy()

    # ####################### scbw_close_scb_window ########################
    def scbw_close_scb_window( self):
        """ Close the scb window """
        self.__scbw_scb_cancel_button()
