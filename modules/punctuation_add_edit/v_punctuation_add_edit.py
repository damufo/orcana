# -*- coding: utf-8 -*-


import wx

from .w_punctuation_add_edit import PunctuationAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_integer import TxtInteger


class View(PunctuationAddEdit):
    def __init__(self, parent):
        PunctuationAddEdit.__init__(self, parent=parent)
        self.SetName('punctuation_add_edit')
        self.parent = parent
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.txt_entity_to_point_ind_plus = TxtInteger(txt=self.txt_entity_to_point_ind)
        self.txt_entity_to_point_rel_plus = TxtInteger(txt=self.txt_entity_to_point_rel)


    def set_values(self, punctuation):
        self.txt_name.SetValue(punctuation.name)
        self.txt_points_ind.SetValue(punctuation.points_ind)
        self.txt_points_rel.SetValue(punctuation.points_rel)
        self.txt_entity_to_point_ind_plus.SetValue(punctuation.entity_to_point_ind)
        self.txt_entity_to_point_rel_plus.SetValue(punctuation.entity_to_point_rel)
        self.txt_name.SetFocus()

    def get_values(self):
        values = {}
        values["name"] = self.txt_name.GetValue().strip().upper()
        values["points_ind"] = self.txt_points_ind.GetValue().strip().upper()
        values["points_rel"] = self.txt_points_rel.GetValue().strip().upper()
        values["entity_to_point_ind"] = self.txt_entity_to_point_ind.GetValue()
        values["entity_to_point_rel"] = self.txt_entity_to_point_rel.GetValue()
        return values

