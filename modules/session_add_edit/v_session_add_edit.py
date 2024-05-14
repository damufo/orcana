# -*- coding: utf-8 -*-


import wx

from .w_session_add_edit import SessionAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_date import TxtDateIso
from classes.wxp.txt_time import TxtTimeShort

class View(SessionAddEdit):
    def __init__(self, parent):
        SessionAddEdit.__init__(self, parent=parent)
        self.SetName('session_add_edit')
        self.parent = parent
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.txt_date_plus = TxtDateIso(txt=self.txt_date)
        self.txt_time_plus = TxtTimeShort(txt=self.txt_time)


    def set_values(self, session):
        self.txt_date_plus.SetValue(session.date)
        self.txt_time_plus.SetValue(session.time)
        self.txt_date.SetFocus()

    def get_values(self):
        values = {}
        values['date'] = self.txt_date_plus.GetValue()
        self.txt_time_plus.SetValue(self.txt_time.GetValue())
        values['time'] = self.txt_time_plus.GetValue()
        return values


