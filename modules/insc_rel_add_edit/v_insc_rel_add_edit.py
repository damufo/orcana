# -*- coding: utf-8 -*-


import wx

from .w_insc_rel_add_edit import InscRelAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_date import TxtDateIso
from classes.wxp.txt_mark import TxtMark


class View(InscRelAddEdit):
    def __init__(self, parent):
        InscRelAddEdit.__init__(self, parent=parent)
        self.parent = parent
        self.SetName('insc_rel_add_edit')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.txt_date_plus = TxtDateIso(txt=self.txt_date)
        self.txt_mark_plus = TxtMark(txt=self.txt_mark)
        
    def set_values(self, inscription):
        self.lbl_event_name.SetLabel(inscription.event.name)
        if inscription.relay.relay_id:
            self.txt_entity_name.SetValue(inscription.relay.entity.short_name)
            self.lbl_entity_code.SetLabel(inscription.relay.entity.entity_code)
            self.txt_relay_name.SetValue(inscription.relay.name)
            self.view_plus.cho_load(choice=self.cho_category_id,
                                values=inscription.phase.phase_categories.choices(),
                                default=inscription.relay.category.category_id)
        else:
            self.txt_entity_name.SetValue('')
            self.lbl_entity_code.SetLabel('')
            self.txt_relay_name.SetLabel('')
            category_choices = inscription.phase.phase_categories.choices()
            category_default = None
            if len(category_choices) == 1:
                category_default = category_choices[0][1]
            self.view_plus.cho_load(choice=self.cho_category_id,
                                values=inscription.phase.phase_categories.choices(),
                                default=category_default)
        if inscription.mark_hundredth:
            self.txt_mark.SetValue(inscription.mark_time)
        else:
            self.txt_mark.SetValue('59:59.99')
        
        self.view_plus.cho_load(choice=self.cho_chrono_type,
                                values=inscription.config.chrono_type.choices(),
                                default=inscription.chrono_type or inscription.champ.params['champ_chrono_type'])
        self.view_plus.cho_load(choice=self.cho_pool_length,
                                values=inscription.config.pool_length.choices(),
                                default=inscription.pool_length or inscription.champ.params['champ_pool_length'])
        self.txt_date_plus.SetValue(inscription.date)
        self.txt_venue.SetValue(inscription.venue)
        self.chb_rejected.SetValue(inscription.rejected)
        self.chb_exchanged.SetValue(inscription.exchanged)
        self.chb_score.SetValue(inscription.score)
        self.chb_classify.SetValue(inscription.classify)
        self.txt_entity_name.SetFocus()
        self.set_classify()

    def get_values(self):
        values = {}
        values['relay_name'] = self.txt_relay_name.GetValue().strip().upper()
        values['category_id'] = self.view_plus.cho_get(self.cho_category_id)
        values['mark_hundredth'] = self.txt_mark_plus.GetValue()
        values['pool_length'] = self.view_plus.cho_get(self.cho_pool_length)
        values['chrono_type'] = self.view_plus.cho_get(self.cho_chrono_type)
        values['date'] = self.txt_date_plus.GetValue()
        values['venue'] = self.txt_venue.GetValue().strip().upper()
        values['rejected'] = self.chb_rejected.GetValue()
        values['exchanged'] = self.chb_exchanged.GetValue()
        values['score'] = self.chb_score.GetValue()
        values['classify'] = self.chb_classify.GetValue()
        return values

    def set_entity_values(self, entity):
        if entity:
            self.txt_entity_name.SetValue(entity.short_name)
            self.lbl_entity_code.SetLabel(entity.entity_code)
        else:
            self.txt_entity_name.SetValue('')
            self.lbl_entity_code.SetLabel('')

    def set_classify(self):
        if self.chb_classify.GetValue():
            self.chb_score.Enable(True)
        else:
            self.chb_score.SetValue(0)
            self.chb_score.Enable(False)