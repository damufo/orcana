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

    def set_heat(self, heat):
        self.lbl_event_name.SetLabel(heat.event.name)
        self.lbl_heat.SetLabel(str(heat.pos))
        category_choices = heat.phase.phase_categories.choices()
        category_default = None
        category_default = category_choices[0][1]
        self.view_plus.cho_load(choice=self.cho_category_id,
            values=heat.phase.phase_categories.choices(),
            default=category_default)
    
    def set_lane(self, lane):
        self.lbl_lane.SetLabel(str(lane))
    
    def set_entity(self, entity):
        if entity:
            self.txt_entity_name.SetValue(entity.short_name)
            self.lbl_entity_code.SetLabel(entity.entity_code)
        else:
            self.txt_entity_name.SetValue('')
            self.lbl_entity_code.SetLabel('')

    def set_relay(self, relay):
        if relay:
            # self.view_plus.cho_set(choice=self.cho_category_id,
                # value=relay.category.category_id)
            self.txt_relay_name.SetValue(relay.name)
        else:
            # self.view_plus.cho_set(choice=self.cho_category_id,
                # value=-1)
            self.txt_relay_name.SetValue('')

    def get_values(self):
        values = {}
        values['relay_name'] = self.txt_relay_name.GetValue().strip().upper()
        values['category_id'] = self.view_plus.cho_get(self.cho_category_id)
        return values