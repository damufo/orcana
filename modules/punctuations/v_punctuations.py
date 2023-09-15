# -*- coding: utf-8 -*-


import wx

from .w_punctuations import Punctuations
# from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Punctuations):
    def __init__(self, parent):
        Punctuations.__init__(self, parent=parent)
        self.SetName('punctuations')
        self.parent = parent
        self.parent.load_panel(self)
        # self.view_plus = ViewPlus(self)
        self.msg = Messages(self.parent)
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        self.lsc.SetName('punctuations')

    def close(self):
        self.lsc_plus.save_custom_column_width()

        
