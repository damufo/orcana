# -*- coding: utf-8 -*-


import wx

from .w_properties import Properties
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Properties):
    def __init__(self, parent):
        Properties.__init__(self, parent=parent)
        self.parent = parent
        self.parent.load_panel(self)
        self.view_plus = self.parent.view_plus

        button_image = (
            (self.btn_close, 'close.png'),
            )
        self.parent.view_plus.set_button_image(button_image)

# class View2(Prefs):

#     def __init__(self, parent):
#         Prefs.__init__(self, parent)
#         self.SetName('prefs')
#         self.view_plus = ViewPlus(self)
#         self.msg = Messages(self)
        
    def set_values(self, champ):
        self.txt_champ_name.SetValue(champ.name)
        self.view_plus.cho_load(choice=self.cho_pool_length,
                                values=champ.config.pool_lengths.choices(),
                                default=champ.pool_length)
        self.view_plus.cho_load(choice=self.cho_pool_lanes,
                                values=champ.config.pool_lanes.choices(),
                                default=champ.pool_lanes)
        self.view_plus.cho_load(choice=self.cho_chrono_type,
                                values=champ.config.chrono_types.choices(),
                                default=champ.chrono_type)                

    
    def get_values(self, champ):
        champ.name = self.txt_champ_name.GetValue().strip()
        champ.pool_length = self.view_plus.cho_get(choice=self.cho_pool_length)
        champ.pool_lanes = self.view_plus.cho_get(choice=self.cho_pool_lanes)
        champ.chrono_type = self.view_plus.cho_get(choice=self.cho_chrono_type)
        champ.save()
