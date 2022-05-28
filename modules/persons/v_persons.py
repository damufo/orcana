# -*- coding: utf-8 -*-


import wx

from .w_persons import Persons
# from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Persons):
    def __init__(self, parent):
        Persons.__init__(self, parent=parent)
        self.SetName('persons')
        self.parent = parent
        self.parent.load_panel(self)
        self.msg = Messages(self.parent)
        self.lsc.SetName('persons')
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)

    def close(self):
        self.lsc_plus.save_custom_column_width()

        
