# -*- coding: utf-8 -*-


import wx

from .w_inscriptions import Inscriptions
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Inscriptions):
    def __init__(self, parent):
        Inscriptions.__init__(self, parent=parent)
        self.SetName('inscriptions')
        self.parent = parent
        self.parent.load_panel(self)
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        # self.lsc.SetName('')
        # self.lsc_rel_inscriptions_plus = self.parent.get_lsc_plus(
        #     lsc=self.lsc_rel_inscriptions, parent=self)
        # self.lsc_rel_inscriptions.SetName('rel_inscriptions')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self.parent)

        # button_image = (
        #     (self.btn_move_down, 'move_down.png'),
        #     (self.btn_move_up, 'move_up.png'),
        #     (self.btn_delete, 'delete.png'),
        #     (self.btn_edit, 'edit.png'),
        #     (self.btn_add, 'add.png'),
        #     (self.btn_import, 'import.png'),
        #     (self.btn_close, 'close.png'),
        #     )
        # self.parent.view_plus.set_button_image(button_image)

    def set_phases(self, phases):
        self.view_plus.cho_load(choice=self.cho_phase_id,
                                values=phases.choices(add_empty=False),
                                default=phases[0].phase_id)

    def set_ind(self):
        # self.lsc_ind_inscriptions.Show()
        # self.lsc_rel_inscriptions.Hide()
        self.lsc.SetName('ind_inscriptions')
        # self.Layout()

    def set_rel(self):
        # self.lsc_rel_inscriptions.Show()
        # self.lsc_ind_inscriptions.Hide()
        self.lsc.SetName('rel_inscriptions')
        # self.Layout()

    def get_phase_id(self):
        phase_id = self.view_plus.cho_get(self.cho_phase_id)
        return phase_id

    def close(self):
        # self.lsc_ind_inscriptions_plus.save_custom_column_width()
        # self.lsc_rel_inscriptions_plus.save_custom_column_width()
        self.lsc_plus.save_custom_column_width()
