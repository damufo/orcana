# -*- coding: utf-8 -*-


from .m_category_add_edit import Model
from .v_category_add_edit import View
from .i_category_add_edit import Interactor


def create(parent, category, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(category=category),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(category=self.model.category)
        self.view.view_plus.start(modal=True)

    def acept(self):
        category = self.model.category
        values = self.view.get_values()
        msg = None
        if category.already_exists(code=values["code"], gender_id=values['gender_id']):
            msg = 'Already exists.'
            self.view.txt_code.SetFocus()
        elif not values['code']:
            msg = 'Set a code.'
            self.view.txt_code.SetFocus()
        elif not values['gender_id']:
            msg = 'Set a gender.'
            self.view.cho_gender_id.SetFocus()
        elif not values['name']:
            msg = 'Set a name.'
            self.view.txt_name.SetFocus()
        elif not values['from_age']:
            msg = 'Set from age.'
            self.view.txt_from_age.SetFocus()
        elif not values['to_age']:
            msg = 'Set to age.'
            self.view.txt_to_age.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            # category.pos = person
            category.code = values['code']
            category.gender_id = values['gender_id']
            category.name = values['name']
            category.from_age = values['from_age']
            category.to_age = values['to_age']
            category.save()
            self.view.view_plus.stop()

    def cancel(self):
        # self.view.view_plus.close()
        # self.model.category.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

