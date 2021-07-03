# -*- coding: utf-8 -*-


import wx

from .w_resize import Resize
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Resize):

    def __init__(self, parent):
        Resize.__init__(self, parent)
        self.SetName('resize')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.picture = None
        
    def set_values(self):
        self.spn_width_px.SetValue(self.picture.width)
        self.spn_height_px.SetValue(self.picture.height)
    
    def get_values(self):
        if self.cho_units.GetSelection() == 0:  # pixels
            width = self.spn_width_px.GetValue()
            height = self.spn_height_px.GetValue()
        else:  # percentage
            width_percent = self.spn_width_percent.GetValue() / 100
            width = self.picture.width * width_percent
            height_percent = self.spn_width_percent.GetValue() / 100
            height = self.picture.height * height_percent
        return width, height
            
    def update_height(self):
        
        if self.chb_preserve_aspect_ratio.GetValue():
            if self.cho_units.GetSelection() == 0:  # pixels
                if self.spn_width_px.GetValue() > 0:
                    factor = self.spn_width_px.GetValue() / self.picture.width
                    self.spn_height_px.SetValue(
                        int(self.picture.height * factor))
            else:  # percentage
                if self.spn_width_px.GetValue() > 0:
                    self.spn_height_percent.SetValue(
                        self.spn_width_percent.GetValue())

    def update_width(self):
        if self.chb_preserve_aspect_ratio.GetValue():
            if self.cho_units.GetSelection() == 0:  # pixels
                if self.spn_height_px.GetValue() > 0:
                    factor = self.spn_height_px.GetValue() / self.picture.height
                    self.spn_width_px.SetValue(int(self.picture.width * factor))
            else:  # percentage
                if self.spn_height_percent.GetValue() > 0:
                    self.spn_width_percent.SetValue(
                        self.spn_height_percent.GetValue())

    def change_units(self):
        self.spn_width_px.Show(not self.spn_width_px.IsShown())
        self.spn_height_px.Show(not self.spn_height_px.IsShown())
        self.spn_height_percent.Show(not self.spn_height_percent.IsShown())
        self.spn_width_percent.Show(not self.spn_width_percent.IsShown())
        self.Layout()
