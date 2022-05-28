# -*- coding: utf-8 -*-


import wx

from .w_person_add_edit import PersonAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_date import TxtDateIso

class View(PersonAddEdit):
    def __init__(self, parent):
        PersonAddEdit.__init__(self, parent=parent)
        self.SetLabel('Person add edit')
        self.SetName('person_add_edit')
        self.parent = parent
        # self.parent.load_panel(self)
        # self.view_plus = self.parent.view_plus
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.txt_birth_date_plus = TxtDateIso(txt=self.txt_birth_date)
        # self.SetWindowStyle(wx.STAY_ON_TOP)
        # button_image = (
        #     (self.btn_close, 'close.png'),
        #     )
        # self.parent.view_plus.set_button_image(button_image)

# class View2(Prefs):

#     def __init__(self, parent):
#         Prefs.__init__(self, parent)
#         self.SetName('prefs')
#         self.view_plus = ViewPlus(self)
#         self.msg = Messages(self)
        
    def set_values(self, person):
        self.txt_license.SetValue(person.license)
        self.txt_surname.SetValue(person.surname)
        self.txt_name.SetValue(person.name)
        self.view_plus.cho_load(choice=self.cho_gender_id,
                                values=person.config.gender.choices(),
                                default=person.gender_id)
        self.txt_birth_date_plus.SetValue(person.birth_date)
        if person.entity:
            self.txt_entity_name.SetValue(person.entity.short_name)
            self.lbl_entity_code.SetLabel(person.entity.entity_code or '')
        if 'entity_id' in person.lock:
            self.txt_entity_name.Enable(False)
            self.btn_add_entity.Enable(False)
        if 'gender_id' in person.lock:
            self.cho_gender_id.Enable(False)
        self.txt_license.SetFocus()

    def get_values(self):
        values = {}
        values["license"] = self.txt_license.GetValue().strip()
        values["surname"] = self.txt_surname.GetValue().strip().upper()
        values["name"] = self.txt_name.GetValue().strip().upper()
        values["gender_id"] = self.view_plus.cho_get(choice=self.cho_gender_id)
        values["birth_date"] = self.txt_birth_date_plus.GetValue()
        values["entity_code"] = self.lbl_entity_code.GetLabel()
        return values

    def set_entity_values(self, entity):
        if entity:
            self.txt_entity_name.SetValue(entity.short_name)
            self.lbl_entity_code.SetLabel(entity.entity_code)

        else:
            self.txt_entity_name.SetValue('')
            self.lbl_entity_code.SetLabel('')