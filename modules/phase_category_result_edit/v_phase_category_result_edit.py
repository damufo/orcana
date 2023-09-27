# -*- coding: utf-8 -*-


import wx

from .w_phase_category_result_edit import PhaseCategoryResultEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_float import TxtFloat


class View(PhaseCategoryResultEdit):
    def __init__(self, parent):
        PhaseCategoryResultEdit.__init__(self, parent=parent)
        self.parent = parent
        self.SetName('phase_category_result_edit')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.txt_points_plus = TxtFloat(txt=self.txt_points)

    def set_values(self, phase_category_result):
        self.txt_points_plus.SetValue(phase_category_result.points)
        self.chb_clas_next_phase.SetValue(phase_category_result.clas_next_phase)
        self.txt_points.SetFocus()

    def get_values(self):
        values = {}
        values['points'] = self.txt_points_plus.GetValue()
        values['clas_next_phase'] = self.chb_clas_next_phase.GetValue()
        return values
