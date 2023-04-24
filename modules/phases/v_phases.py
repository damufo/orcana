# -*- coding: utf-8 -*-


import wx

from .w_phases import Phases
# from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Phases):
    def __init__(self, parent):
        Phases.__init__(self, parent=parent)
        self.SetName('phases')
        self.parent = parent
        self.parent.load_panel(self)
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        self.lsc.SetName('phases')
        # self.view_plus = ViewPlus(self)
        self.msg = Messages(self.parent)

    def close(self):
        self.lsc_plus.save_custom_column_width()