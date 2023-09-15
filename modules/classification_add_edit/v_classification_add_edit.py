# -*- coding: utf-8 -*-


import wx

from .w_classification_add_edit import ClassificationAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(ClassificationAddEdit):
    def __init__(self, parent):
        ClassificationAddEdit.__init__(self, parent=parent)
        self.SetName('classification_add_edit')
        self.parent = parent
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)


    def set_values(self, classification):
        self.txt_name.SetValue(classification.name)
        self.view_plus.cho_load(choice=self.cho_gender_id,
                                values=classification.config.genders.choices(),
                                default=classification.gender_id)
        choices_categories = classification.champ.categories.choices()
        selected_categories = [i.category_id for i in classification.categories]
        self.view_plus.clb_load(choice=self.clb_categories,
                                values=choices_categories,
                                default=selected_categories)
        self.txt_name.SetFocus()

    def get_values(self):
        values = {}
        values["name"] = self.txt_name.GetValue().strip().upper()
        values["gender_id"] = self.view_plus.cho_get(choice=self.cho_gender_id)
        values["categories"] = self.view_plus.clb_get(choice=self.clb_categories)
        return values

