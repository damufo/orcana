# -*- coding: utf-8 -*-


import wx

from .w_res_rel_add_edit import ResRelAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(ResRelAddEdit):
    def __init__(self, parent):
        ResRelAddEdit.__init__(self, parent=parent)
        self.parent = parent
        self.SetName('res_rel_add_edit')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)

    def set_values(self, result):
        self.lbl_event_name.SetLabel(result.event.name)
        self.lbl_heat.SetLabel(str(result.heat.pos))
        self.lbl_lane.SetLabel(str(result.lane))
        if result.result_id:
            self.txt_entity_name.SetValue(result.relay.entity.short_name)
            self.lbl_entity_code.SetLabel(result.relay.entity.entity_code)
            self.txt_relay_name.SetValue(result.relay.name)
            self.view_plus.cho_load(choice=self.cho_category_id,
                                values=result.event.event_categories.choices(),
                                default=result.relay.category.category_id)
        else:
            self.txt_entity_name.SetValue('')
            self.lbl_entity_code.SetLabel('')
            category_choices = result.event.event_categories.choices()
            category_default = None
            if len(category_choices) == 1:
                category_default = category_choices[0][1]
            self.view_plus.cho_load(choice=self.cho_category_id,
                                values=result.event.event_categories.choices(),
                                default=category_default)
            self.txt_relay_name.SetLabel('')
        self.txt_entity_name.SetFocus()
    
    def set_entity_values(self, entity):
        if entity:
            self.txt_entity_name.SetValue(entity.short_name)
            self.lbl_entity_code.SetLabel(entity.entity_code)
        else:
            self.txt_entity_name.SetValue('')
            self.lbl_entity_code.SetLabel('')


    def get_values(self):
        values = {}
        values['relay_name'] = self.txt_relay_name.GetValue().strip().upper()
        values['category_id'] = self.view_plus.cho_get(self.cho_category_id)
        return values