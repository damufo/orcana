# -*- coding: utf-8 -*-


import wx

from .w_phase_categories import PhaseCategories
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(PhaseCategories):
    def __init__(self, parent):
        PhaseCategories.__init__(self, parent=parent)
        self.SetLabel('Phase categories')
        self.SetName('phase_categories')
        self.parent = parent
        self.lsc_plus = self.parent.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)

    def disable_buttons(self):
        self.btn_add.Enable(False)
        self.btn_delete.Enable(False)
        self.btn_move_up.Enable(False)
        self.btn_move_down.Enable(False)

    # def set_values(self, categories):
    #     # self.lst_categories.Set(categories)
    #     values = [
    #         "PUNC", _("Punctuate"),
    #         "CLAS", _("Classify"),
    #         "", "",
    #     ]
    #     self.view_plus.cho_load(choice=self.cho_action,
    #                             values=values,
    #                             default="")

    def select_categories(self, categories_selected):
        for i in categories_selected:
            idx = self.lst_categories.FindString(i)
            self.lst_categories.Select(idx)

    def get_selections(self):
        selections = self.lst_categories.GetSelections()
        return selections
