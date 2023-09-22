# -*- coding: utf-8 -*-


import wx

from .w_insc_ind_add_edit import InscIndAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_date import TxtDateIso
from classes.wxp.txt_mark import TxtMark


class View(InscIndAddEdit):
    def __init__(self, parent):
        InscIndAddEdit.__init__(self, parent=parent)
        self.parent = parent
        self.SetName('insc_ind_add_edit')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.txt_date_plus = TxtDateIso(txt=self.txt_date)
        self.txt_mark_plus = TxtMark(txt=self.txt_mark)

    def set_values(self, inscription):

        if inscription.person:
            self.txt_person_full_name.SetValue(inscription.person.full_name)
            self.lbl_license.SetLabel(inscription.person.license)
            self.lbl_entity_short_name.SetLabel(inscription.person.entity.short_name)
            self.lbl_entity_code.SetLabel(inscription.person.entity.entity_code)
        else:
            self.lbl_license.SetLabel('')
            self.txt_person_full_name.SetValue('')
            self.lbl_entity_short_name.SetLabel('')
            self.lbl_entity_code.SetLabel('')
        if inscription.mark_hundredth:
            self.txt_mark.SetValue(inscription.mark_time)
        else:
            self.txt_mark.SetValue('59:59.99')
        
        self.view_plus.cho_load(choice=self.cho_chrono_type,
                                values=inscription.config.chrono_type.choices(),
                                default=inscription.chrono_type)
        self.view_plus.cho_load(choice=self.cho_pool_length,
                                values=inscription.config.pool_length.choices(),
                                default=inscription.pool_length)
        self.txt_date_plus.SetValue(inscription.date)
        self.txt_venue.SetValue(inscription.venue)
        self.chb_rejected.SetValue(inscription.rejected)
        self.chb_exchanged.SetValue(inscription.exchanged)
        self.chb_score.SetValue(inscription.score)
        self.chb_classify.SetValue(inscription.classify)
        self.set_classify()

        if 'person' in inscription.lock:
            self.lbl_phase_name.Hide()
            self.txt_person_full_name.Hide()
            self.btn_add_person.Hide()
            # self.btn_add_person.Enable(False)
            self.lbl_person_full_name.SetLabel(inscription.person.full_name)
            phases = inscription.person.champ.phases
            if inscription.phase:
                phase_id = inscription.phase.phase_id
            else:
                phase_id = None
            choices = phases.choices(add_empty=False, gender_id=inscription.person.gender_id, ind_rel='I')
            self.view_plus.cho_load(choice=self.cho_phase_id,
                    values=choices,
                    default=phase_id)
            self.cho_phase_id.SetFocus()
        else:
            self.cho_phase_id.Hide()
            self.lbl_person_full_name.Hide()
            self.txt_person_full_name.SetFocus()


    def get_values(self):
        values = {}
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

    def set_person_values(self, person):
        if person:
            self.txt_person_full_name.SetValue(person.full_name)
            self.lbl_license.SetLabel(person.license)
            self.lbl_entity_code.SetLabel(person.entity.entity_code)
            self.lbl_entity_short_name.SetLabel(person.entity.short_name)
        else:
            self.txt_person_full_name.SetValue("")
            self.lbl_license.SetLabel("")
            self.lbl_entity_code.SetLabel("")
            self.lbl_entity_short_name.SetLabel("")

    def set_classify(self):
        if self.chb_classify.GetValue():
            self.chb_score.Enable(True)
        else:
            self.chb_score.SetValue(0)
            self.chb_score.Enable(False)