# -*- coding: utf-8 -*-


import wx

from .w_prefs import Prefs
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Prefs):

    def __init__(self, parent):
        Prefs.__init__(self, parent)
        self.SetName('prefs')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        
    def set_values(self, prefs):
        jpg_quality = prefs.get_value('prefs.jpg.quality')
        jpg_optimize = prefs.get_value('prefs.jpg.optimize')
        jpg_progresissve = prefs.get_value('prefs.jpg.progressive')
        max_width = prefs.get_value('prefs.autoresize.max_width')
        max_height = prefs.get_value('prefs.autoresize.max_height')
        pr_ratio = prefs.get_value('prefs.autoresize.pr_ratio')
        auto_save = prefs.get_value('prefs.autoresize.auto_save')

        self.spn_jpg_quality.SetValue(jpg_quality)
        self.chb_jpg_optimize.SetValue(jpg_optimize)
        self.chb_jpg_progressive.SetValue(jpg_progresissve)
        self.spn_width_px.SetValue(max_width)
        self.spn_height_px.SetValue(max_height)
        self.chb_preserve_aspect_ratio.SetValue(pr_ratio)
        self.chb_save_when_autoresize.SetValue(auto_save)
    
    def get_values(self, prefs):
        jpg_quality = self.spn_jpg_quality.GetValue()
        jpg_optimize = self.chb_jpg_optimize.GetValue()
        jpg_progresissve = self.chb_jpg_progressive.GetValue()
        max_width = self.spn_width_px.GetValue()
        max_height = self.spn_height_px.GetValue()
        pr_ratio = self.chb_preserve_aspect_ratio.GetValue()
        auto_save = self.chb_save_when_autoresize.GetValue()

        prefs.set_value('prefs.jpg.quality', jpg_quality)
        prefs.set_value('prefs.jpg.optimize', jpg_optimize)
        prefs.set_value('prefs.jpg.progressive', jpg_progresissve)
        prefs.set_value('prefs.autoresize.max_width', max_width)
        prefs.set_value('prefs.autoresize.max_height', max_height)
        prefs.set_value('prefs.autoresize.pr_ratio', pr_ratio)
        prefs.set_value('prefs.autoresize.auto_save', auto_save)
