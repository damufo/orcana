# -*- coding: utf-8 -*-


from .m_properties import Model
from .v_properties import View
from .i_properties import Interactor


def create(parent, champ):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(champ=champ),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(champ=self.model.champ)
        # self.view.view_plus.start(modal=True)

    # def acept(self):
    #     self.view.get_values(prefs=self.model.prefs)
    #     self.model.prefs.save()
    #     self.view.view_plus.stop()

    def go_back(self):
        self.view.get_values(champ=self.model.champ)
        self.parent.load_me()
