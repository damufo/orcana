# -*- coding: utf-8 -*-


import wx

from .w_phase_categories_categories_add import PhaseCategoriesCategoriesAdd
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_date import TxtDateIso

class View(PhaseCategoriesCategoriesAdd):
    def __init__(self, parent):
        PhaseCategoriesCategoriesAdd.__init__(self, parent=parent)
        self.SetLabel('Phase categories categories add')
        self.SetName('phase_categories_categories_add')
        self.parent = parent
        self.lsc_plus = self.parent.parent.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        # self.parent.load_panel(self)
        # self.view_plus = self.parent.view_plus
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        # self.txt_birth_date_plus = TxtDateIso(txt=self.txt_birth_date)
        # self.SetWindowStyle(wx.STAY_ON_TOP)
        # button_image = (
        #     (self.btn_close, 'close.png'),
        #     )
        # self.parent.view_plus.set_button_image(button_image)
        self.categories_selected = []

    def set_values(self):
        # self.lst_categories.Set(categories)
        values = [
            (_("Punctuate"), "PUNC"),
            (_("Classify"), "CLAS"),
            ("", ""),
        ]
        self.view_plus.cho_load(choice=self.cho_action,
                                values=values,
                                default="")
    def get_values(self):
        return self.view_plus.cho_get(choice=self.cho_action)
