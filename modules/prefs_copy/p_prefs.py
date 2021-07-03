# -*- coding: utf-8 -*-


from .m_prefs import Model
from .v_prefs import View
from .i_prefs import Interactor


def create(parent, prefs):
    return Presenter(
            Model(prefs=prefs),
            View(parent.view),
            Interactor())

class Presenter(object):

    def __init__(self, model, view, interactor):
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(prefs=self.model.prefs)
        self.view.view_plus.start(modal=True)

    def acept(self):
        self.view.get_values(prefs=self.model.prefs)
        self.model.prefs.save()
        self.view.view_plus.stop()

    def close(self):
        self.view.view_plus.stop()
