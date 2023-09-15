# -*- coding: utf-8 -*-


from .m_classification_add_edit import Model
from .v_classification_add_edit import View
from .i_classification_add_edit import Interactor


def create(parent, classification, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(classification=classification),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(classification=self.model.classification)
        self.view.view_plus.start(modal=True)

    def acept(self):
        classification = self.model.classification
        values = self.view.get_values()
        msg = None

        if not values['name']:
            msg = 'Set a name.'
            self.view.txt_name.SetFocus()
        # elif not values['gender_id']:
        #     msg = 'Set a gender.'
            # self.view.cho_gender_id.SetFocus()
        elif not values['categories']:
            msg = 'Set any category.'
            self.view.clb_categories.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            categories_dict = classification.champ.categories.dict
            classification_categories = []
            for i in values['categories']:
                category = categories_dict[i]
                classification_categories.append(category)
            classification.name = values['name']
            classification.gender_id = values['gender_id']
            classification.categories = classification_categories
            if not classification in classification.classifications:
                classification.classifications.append(classification)
            classification.save()
            self.view.view_plus.stop()

    def cancel(self):
        # self.view.view_plus.close()
        # self.model.classification.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

