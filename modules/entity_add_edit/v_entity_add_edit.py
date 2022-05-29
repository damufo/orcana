# -*- coding: utf-8 -*-


import wx

from .w_entity_add_edit import EntityAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages

class View(EntityAddEdit):
    def __init__(self, parent):
        EntityAddEdit.__init__(self, parent=parent)
        self.SetName('entity_add_edit')
        self.parent = parent
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)

    def set_values(self, entity):
        self.txt_entity_code.SetValue(entity.entity_code)
        self.txt_short_name.SetValue(entity.short_name)
        self.txt_medium_name.SetValue(entity.medium_name)
        self.txt_long_name.SetValue(entity.long_name)
        if 'entity_code' in entity.lock:
            self.txt_entity_code.Enable(False)
            self.txt_short_name.SetFocus()
        else:
            self.txt_entity_code.SetFocus()


    def get_values(self, entity):
        entity.entity_code = self.txt_entity_code.GetValue().strip()
        entity.short_name = self.txt_short_name.GetValue().strip().upper()
        entity.medium_name = self.txt_medium_name.GetValue().strip().upper()
        entity.long_name = self.txt_long_name.GetValue().strip().upper()

