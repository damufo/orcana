# -*- coding: utf-8 -*-


import wx

from .w_results import Results
from classes.wxp.view_plus import ViewPlus
# from classes.wxp.messages import Messages


class View(Results):
    def __init__(self, parent):
        Results.__init__(self, parent=parent)
        self.SetName('results')
        self.parent = parent
        self.parent.load_panel(self)
        self.lsc_heats_plus = self.parent.get_lsc_plus(
            lsc=self.lsc_heats, parent=self)
        self.lsc_heats.SetName('heats')
        self.lsc_heat_plus = self.parent.get_lsc_plus(
            lsc=self.lsc_heat, parent=self)
        self.lsc_heat.SetName('heat')
        self.view_plus = ViewPlus(self)

        button_image = (
            (self.btn_move_down, 'move_down.png'),
            (self.btn_move_up, 'move_up.png'),
            (self.btn_delete, 'delete.png'),
            (self.btn_edit, 'edit.png'),
            (self.btn_add, 'add.png'),
            (self.btn_import, 'import.png'),
            (self.btn_close, 'close.png'),
            )
        self.parent.view_plus.set_button_image(button_image)

    def set_events(self, events):
        self.view_plus.cho_load(choice=self.cho_event_id,
                                values=events.choices(add_empty=False),
                                default=events[0].event_id)

    def set_ind(self):
        self.lsc_ind_inscriptions.Show()
        self.lsc_rel_inscriptions.Hide()
        self.Layout()

    def set_rel(self):
        self.lsc_rel_inscriptions.Show()
        self.lsc_ind_inscriptions.Hide()
        self.Layout()

    def get_event_id(self):
        event_id = self.view_plus.cho_get(self.cho_event_id)
        return event_id

    def close(self):
        self.lsc_heats_plus.save_custom_column_width()
        self.lsc_heat_plus.save_custom_column_width()
