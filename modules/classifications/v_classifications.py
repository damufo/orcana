# -*- coding: utf-8 -*-


import wx

from .w_classifications import Classifications
# from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Classifications):
    def __init__(self, parent):
        Classifications.__init__(self, parent=parent)
        self.SetName('classifications')
        self.parent = parent
        self.parent.load_panel(self)
        # self.view_plus = ViewPlus(self)
        self.msg = Messages(self.parent)
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        self.lsc.SetName('classifications')

    def close(self):
        self.lsc_plus.save_custom_column_width()

        
