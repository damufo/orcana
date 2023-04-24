# -*- coding: utf-8 -*-


import wx

from .w_event_categories import EventCategories
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_date import TxtDateIso

class View(EventCategories):
    def __init__(self, parent):
        EventCategories.__init__(self, parent=parent)
        self.SetLabel('Event categories')
        self.SetName('event_categories')
        self.parent = parent
        self.lsc_plus = self.parent.parent.get_lsc_plus(lsc=self.lsc, parent=self)
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

# class View2(Prefs):

#     def __init__(self, parent):
#         Prefs.__init__(self, parent)
#         self.SetName('prefs')
#         self.view_plus = ViewPlus(self)
#         self.msg = Messages(self)
        
    def set_values(self, categories):
        # self.lst_categories.Set(categories)
        values = [
            "PUNC", "Punctuate"
            "CLAS", "Clasificate"
            "", ""
        ]
        self.view_plus.cho_load(choice=self.cho_action,
                                values=values,
                                default="")

    def select_categories(self, categories_selected):
        for i in categories_selected:
            idx = self.lst_categories.FindString(i)
            self.lst_categories.Select(idx)

    def get_selections(self):
        selections = self.lst_categories.GetSelections()
        return selections

