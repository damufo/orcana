# -*- coding: utf-8 -*-


import wx

from .w_ind_inscriptions import IndInscriptions
from classes.wxp.view_plus import ViewPlus
# from classes.wxp.messages import Messages


class View(IndInscriptions):
    def __init__(self, parent):
        IndInscriptions.__init__(self, parent=parent)
        self.SetName('ind_inscriptions')
        self.parent = parent
        self.parent.load_panel(self)
        self.lsc_plus = self.parent.get_lsc_plus(lsc=self.lsc, parent=self)
        self.lsc.SetName('ind_inscriptions')
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
                                values=events.choices(add_empty=True),
                                default=events[0].event_id)

    def get_event_id(self):
        event_id = self.view_plus.cho_get(self.cho_event_id)
        return event_id
        
# class View2(Prefs):

#     def __init__(self, parent):
#         Prefs.__init__(self, parent)
#         self.SetName('prefs')
#         self.view_plus = ViewPlus(self)
#         self.msg = Messages(self)
        
    # def set_values(self, prefs):
    #     jpg_quality = prefs.get_value('prefs.jpg.quality')
    #     jpg_optimize = prefs.get_value('prefs.jpg.optimize')
    #     jpg_progresissve = prefs.get_value('prefs.jpg.progressive')
    #     max_width = prefs.get_value('prefs.autoresize.max_width')
    #     max_height = prefs.get_value('prefs.autoresize.max_height')
    #     pr_ratio = prefs.get_value('prefs.autoresize.pr_ratio')
    #     auto_save = prefs.get_value('prefs.autoresize.auto_save')

    #     self.spn_jpg_quality.SetValue(jpg_quality)
    #     self.chb_jpg_optimize.SetValue(jpg_optimize)
    #     self.chb_jpg_progressive.SetValue(jpg_progresissve)
    #     self.spn_width_px.SetValue(max_width)
    #     self.spn_height_px.SetValue(max_height)
    #     self.chb_preserve_aspect_ratio.SetValue(pr_ratio)
    #     self.chb_save_when_autoresize.SetValue(auto_save)
    
    # def get_values(self, prefs):
    #     jpg_quality = self.spn_jpg_quality.GetValue()
    #     jpg_optimize = self.chb_jpg_optimize.GetValue()
    #     jpg_progresissve = self.chb_jpg_progressive.GetValue()
    #     max_width = self.spn_width_px.GetValue()
    #     max_height = self.spn_height_px.GetValue()
    #     pr_ratio = self.chb_preserve_aspect_ratio.GetValue()
    #     auto_save = self.chb_save_when_autoresize.GetValue()

    #     prefs.set_value('prefs.jpg.quality', jpg_quality)
    #     prefs.set_value('prefs.jpg.optimize', jpg_optimize)
    #     prefs.set_value('prefs.jpg.progressive', jpg_progresissve)
    #     prefs.set_value('prefs.autoresize.max_width', max_width)
    #     prefs.set_value('prefs.autoresize.max_height', max_height)
    #     prefs.set_value('prefs.autoresize.pr_ratio', pr_ratio)
    #     prefs.set_value('prefs.autoresize.auto_save', auto_save)

    def close(self):
        self.lsc_plus.save_custom_column_width()

        
