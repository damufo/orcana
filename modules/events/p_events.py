# -*- coding: utf-8 -*-


from .m_events import Model
from .v_events import View
from .i_events import Interactor


def create(parent, events):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(events=events),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.events.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.events
        self.view.lsc_plus.load(custom_column_widths=True)
        # self.view.set_values(prefs=self.model.prefs)
        # self.view.view_plus.start(modal=True)

    # def acept(self):
    #     self.view.get_values(prefs=self.model.prefs)
    #     self.model.prefs.save()
    #     self.view.view_plus.stop()

    def go_back(self):
        self.view.close()
        self.parent.load_me()
