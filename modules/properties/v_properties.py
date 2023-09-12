# -*- coding: utf-8 -*-


import wx

from .w_properties import Properties
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_date import TxtDateIso


class View(Properties):
    def __init__(self, parent):
        Properties.__init__(self, parent=parent)
        self.SetName('properties')
        self.parent = parent
        self.parent.load_panel(self)
        self.msg = Messages(self.parent)
        self.view_plus = self.parent.view_plus
        self.txt_date_age_calculation_plus = TxtDateIso(txt=self.txt_date_age_calculation)

    def set_values(self, champ):
        self.txt_champ_name.SetValue(champ.params['champ_name'])
        self.view_plus.cho_load(choice=self.cho_pool_length,
                                values=champ.config.pool_length.choices(),
                                default=champ.params['champ_pool_length'])
        self.txt_pool_lanes_sort.SetValue(champ.params['champ_pool_lanes_sort'])
        self.view_plus.cho_load(choice=self.cho_chrono_type,
                                values=champ.config.chrono_type.choices(),
                                default=champ.params['champ_chrono_type'])
        self.view_plus.cho_load(choice=self.cho_estament_id,
                                values=champ.config.estament.choices(),
                                default=champ.params['champ_estament_id']) 
        self.txt_date_age_calculation_plus.SetValue(champ.params['champ_date_age_calculation'])
        self.txt_venue.SetValue(champ.params['champ_venue'])
        self.txt_dbs_path.SetValue(champ.config.prefs['last_path_dbs'] or '')
    
    def get_values(self):
        values = {}
        values['champ_name'] = self.txt_champ_name.GetValue().strip()
        values['champ_pool_length'] = self.view_plus.cho_get(choice=self.cho_pool_length)
        values['champ_chrono_type'] = self.view_plus.cho_get(choice=self.cho_chrono_type)
        values['champ_estament_id'] = self.view_plus.cho_get(choice=self.cho_estament_id)
        values['champ_date_age_calculation'] = self.txt_date_age_calculation_plus.GetValue()
        values['champ_venue'] = self.txt_venue.GetValue().strip()
        values["champ_pool_lanes_sort"] = self.txt_pool_lanes_sort.GetValue().strip()
        return values
