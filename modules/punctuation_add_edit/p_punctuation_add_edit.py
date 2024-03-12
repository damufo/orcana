# -*- coding: utf-8 -*-


from .m_punctuation_add_edit import Model
from .v_punctuation_add_edit import View
from .i_punctuation_add_edit import Interactor


def create(parent, punctuation, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(punctuation=punctuation),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(punctuation=self.model.punctuation)
        self.view.view_plus.start(modal=True)

    def acept(self):
        punctuation = self.model.punctuation
        values = self.view.get_values()
        msg = None
        points_ind = punctuation.validade_points_list(values['points_ind'])
        points_rel = punctuation.validade_points_list(values['points_rel'])
        if not values['name']:
            msg = 'Set a name.'
            self.view.txt_name.SetFocus()
        elif not points_ind:
            msg = 'Set points of individual result.'
            self.view.txt_points_ind.SetFocus()
        elif not points_rel:
            msg = 'Set points of relay result.'
            self.view.txt_points_rel.SetFocus()
        elif not values['entity_to_point_ind']:
            msg = 'Set number to point for individual results.'
            self.view.txt_entity_to_point_ind.SetFocus()
        elif not values['entity_to_point_rel']:
            msg = 'Set number to point for relay results.'
            self.view.txt_entity_to_point_rel.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            punctuation.name = values['name']
            punctuation.points_ind = points_ind
            punctuation.points_rel = points_rel
            punctuation.entity_to_point_ind = int(values['entity_to_point_ind'])
            punctuation.entity_to_point_rel = int(values['entity_to_point_rel'])
            punctuation.save()
            if not punctuation in punctuation.punctuations:
                punctuation.punctuations.append(punctuation)
            self.view.view_plus.stop()

    def cancel(self):
        # self.view.view_plus.close()
        # self.model.punctuation.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

