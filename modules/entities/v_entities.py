# -*- coding: utf-8 -*-


import wx

from .w_entities import Entities
# from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Entities):
    def __init__(self, parent):
        Entities.__init__(self, parent=parent)
        self.SetName('entities')
        self.parent = parent
        self.parent.load_panel(self)
        self.msg = Messages(self.parent)
        self.lsc.SetName('entities')
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)

    def close(self):
        self.lsc_plus.save_custom_column_width()

        
