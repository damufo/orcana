# -*- coding: utf-8 -*-


import wx

from .w_event_categories_categories_add import EventCategoriesCategoriesAdd
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_date import TxtDateIso

class View(EventCategoriesCategoriesAdd):
    def __init__(self, parent):
        EventCategoriesCategoriesAdd.__init__(self, parent=parent)
        self.SetLabel('Event categories categories add')
        self.SetName('event_categories_categories_add')
        self.parent = parent
        self.lsc_plus = self.parent.parent.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.categories_selected = []

