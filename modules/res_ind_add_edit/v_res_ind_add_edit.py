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

    def retrieve_focus(self):
        value = wx.FindWindowByName('res_ind_add_edit')
        if value:
            self.Hide()  # Isto é o que o fai funcionar
            self.Show()
            self.txt_person_full_name.SetFocus()
            print('retieve focus en view')


    def set_heat(self, heat):
        self.lbl_event_name.SetLabel(heat.event.name)
        self.lbl_heat.SetLabel(str(heat.pos))
    
    def set_lane(self, lane):
        self.lbl_lane.SetLabel(str(lane))

    def set_person(self, person):
        if person:
            self.txt_person_full_name.SetValue(person.full_name)
            self.lbl_license.SetLabel(person.license)
            self.lbl_entity_short_name.SetLabel(person.entity.short_name)
            self.lbl_entity_code.SetLabel(person.entity.entity_code)
        else:
            self.lbl_license.SetLabel('')
            self.txt_person_full_name.SetValue('')
            self.lbl_entity_short_name.SetLabel('')
            self.lbl_entity_code.SetLabel('')
