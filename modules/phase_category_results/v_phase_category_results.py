# -*- coding: utf-8 -*-


import wx

from .w_phase_category_results import PhaseCategoryResults
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(PhaseCategoryResults):
    def __init__(self, parent):
        PhaseCategoryResults.__init__(self, parent=parent)
        self.SetName('phase_category_results')
        self.parent = parent
        self.parent.load_panel(self)
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        # self.lsc.SetName('') isto cambia en función de se é resultado individual ou de remuda
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self.parent)

    def set_phases(self, phases):
        self.view_plus.cho_load(choice=self.cho_phase_id,
                                values=phases.choices(add_empty=False),
                                default=phases[0].phase_id)
        self.set_phase_categories(phase_categories=phases[0].phase_categories)
    
    def set_phase_categories(self, phase_categories):
        self.view_plus.cho_load(choice=self.cho_phase_category_id,
                                values=phase_categories.choices(add_empty=False),
                                default=phase_categories[0].phase_category_id)
    def set_ind(self):
        self.lsc.SetName('phase_category_results_ind')

    def set_rel(self):
        self.lsc.SetName('phase_category_results_rel')


    def get_phase_id(self):
        phase_id = self.view_plus.cho_get(self.cho_phase_id)
        return phase_id

    def get_phase_category_id(self):
        phase_category_id = self.view_plus.cho_get(self.cho_phase_category_id)
        return phase_category_id

    def close(self):
        self.lsc_plus.save_custom_column_width()
