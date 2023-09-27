# -*- coding: utf-8 -*-


from .m_phase_category_result_edit import Model
from .v_phase_category_result_edit import View
from .i_phase_category_result_edit import Interactor


def create(parent, phase_category_result, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(phase_category_result=phase_category_result),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(phase_category_result=self.model.phase_category_result)
        self.view.view_plus.start(modal=True)

    def acept(self):
        phase_category_result = self.model.phase_category_result
        values = self.view.get_values()
        phase_category_result.points = values['points']
        phase_category_result.clas_next_phase = values['clas_next_phase']
        phase_category_result.save()
        self.view.view_plus.stop()

    def cancel(self):
        # self.view.view_plus.close()
        # self.model.person.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

