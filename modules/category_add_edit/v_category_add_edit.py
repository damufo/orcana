# -*- coding: utf-8 -*-


import wx

from .w_category_add_edit import CategoryAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_integer import TxtInteger


class View(CategoryAddEdit):
    def __init__(self, parent):
        CategoryAddEdit.__init__(self, parent=parent)
        self.SetName('category_add_edit')
        self.parent = parent
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.txt_from_age_plus = TxtInteger(txt=self.txt_from_age)
        self.txt_to_age_plus = TxtInteger(txt=self.txt_to_age)

    def set_values(self, category):

        self.txt_code.SetValue(category.code)
        self.view_plus.cho_load(choice=self.cho_gender_id,
                                values=category.config.genders.choices(),
                                default=category.gender_id)               
        self.txt_name.SetValue(category.name)
        self.txt_from_age_plus.SetValue(category.from_age)
        self.txt_to_age_plus.SetValue(category.to_age)
        self.txt_code.SetFocus()

    def get_values(self):
        values = {}
        values["code"] = self.txt_code.GetValue().strip().upper()
        values["gender_id"] = self.view_plus.cho_get(choice=self.cho_gender_id)
        values["name"] = self.txt_name.GetValue().strip().upper()
        values["from_age"] = self.txt_from_age_plus.GetValue()
        values["to_age"] = self.txt_to_age_plus.GetValue()
        return values

    def calculate_category_name(self):
        if not self.txt_name.GetValue().strip().upper():
            code = self.txt_code.GetValue().strip().upper()
            gender_id = self.view_plus.cho_get(choice=self.cho_gender_id)
            if (code and gender_id):
                self.txt_name.SetValue('{} {}'.format(code, gender_id))
