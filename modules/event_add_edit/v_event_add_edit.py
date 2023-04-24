# -*- coding: utf-8 -*-


import wx

from .w_event_add_edit import EventAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(EventAddEdit):
    def __init__(self, parent):
        EventAddEdit.__init__(self, parent=parent)
        self.SetName('event_add_edit')
        self.parent = parent
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)


    def set_values(self, event):
        self.view_plus.cho_load(choice=self.cho_code,
                                values=event.config.event_code.choices(),
                                default=event.code)  
        self.view_plus.cho_load(choice=self.cho_gender_id,
                                values=event.config.gender.choices(),
                                default=event.gender_id) 
        self.txt_name.SetValue(str(event.name))
        
        self.cho_code.SetFocus()

    def get_values(self):
        values = {}
        values["code"] = self.view_plus.cho_get(choice=self.cho_code)
        values["gender_id"] = self.view_plus.cho_get(choice=self.cho_gender_id)
        values["name"] = self.txt_name.GetValue().strip()
        return values

    def generate_name(self, event):
        code = self.view_plus.cho_get(choice=self.cho_code)
        gender_id = self.view_plus.cho_get(choice=self.cho_gender_id)
        self.txt_name.SetValue(event.generate_name(code=code, gender_id=gender_id))