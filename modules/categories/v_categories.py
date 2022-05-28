# -*- coding: utf-8 -*-


import wx

from .w_categories import Categories
# from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Categories):
    def __init__(self, parent):
        Categories.__init__(self, parent=parent)
        self.SetName('categories')
        self.parent = parent
        self.parent.load_panel(self)
        self.msg = Messages(self.parent)
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        self.lsc.SetName('categories')

    def close(self):
        self.lsc_plus.save_custom_column_width()

        
