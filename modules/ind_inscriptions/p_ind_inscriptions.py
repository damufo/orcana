# -*- coding: utf-8 -*-


from .m_ind_inscriptions import Model
from .v_ind_inscriptions import View
from .i_ind_inscriptions import Interactor


def create(parent, ind_inscriptions):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(ind_inscriptions=ind_inscriptions),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_events(self.model.ind_inscriptions.champ.events)
        self.model.ind_inscriptions.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.ind_inscriptions
        self.view.lsc_plus.load(custom_column_widths=True)
        # self.view.set_values(prefs=self.model.prefs)
        self.view_refresh()
        # self.view.view_plus.start(modal=True)

    def view_refresh(self):
        event_id = self.view.get_event_id()
        self.model.ind_inscriptions.load_items_from_dbs(event_id=event_id)
        self.view.lsc_plus.load()

    # def acept(self):
    #     self.view.get_values(prefs=self.model.prefs)
    #     self.model.prefs.save()
    #     self.view.view_plus.stop()

    def go_back(self):
        self.view.close()
        self.parent.load_me()
