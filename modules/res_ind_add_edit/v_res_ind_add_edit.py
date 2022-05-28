# -*- coding: utf-8 -*-


import wx

from .w_res_ind_add_edit import ResIndAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(ResIndAddEdit):
    def __init__(self, parent):
        ResIndAddEdit.__init__(self, parent=parent)
        self.parent = parent
        self.SetName('res_ind_add_edit')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)

    def set_values(self, result):
        self.lbl_event_name.SetLabel(result.event.name)
        self.lbl_heat.SetLabel(str(result.heat.pos))
        self.lbl_lane.SetLabel(str(result.lane))
        if result.result_id:
            self.txt_person_full_name.SetValue(result.person.full_name)
            self.lbl_license.SetLabel(result.person.license)
            self.lbl_entity_short_name.SetLabel(result.person.entity.short_name)
            self.lbl_entity_code.SetLabel(result.person.entity.entity_code)
        else:
            self.lbl_license.SetLabel('')
            self.txt_person_full_name.SetValue('')
            self.lbl_entity_short_name.SetLabel('')
            self.lbl_entity_code.SetLabel('')
        
        self.txt_person_full_name.SetFocus()
    
    def set_person_values(self, person):
        if person:
            self.txt_person_full_name.SetValue(person.full_name)
            self.lbl_license.SetLabel(person.license)
            self.lbl_entity_code.SetLabel(person.entity.entity_code)
            self.lbl_entity_short_name.SetLabel(person.entity.short_name)
        else:
            self.txt_person_full_name.SetValue("")
            self.lbl_license.SetLabel("")
            self.lbl_entity_code.SetLabel("")
            self.lbl_entity_short_name.SetLabel("")
