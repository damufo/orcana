# -*- coding: utf-8 -*-


from .m_results import Model
from .v_results import View
from .i_results import Interactor


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
        # self.view.set_events(self.model.champ.events)
        # self.model.champ.heats.load_items_from_dbs()
        self.view.lsc_heats_plus.values = self.model.champ.heats
        self.view.lsc_heats_plus.load(custom_column_widths=True)
        self.view_refresh()

    def view_refresh(self):
        pass
        # event_id = self.view.get_event_id()
        # self.model.champ.heats.load_items_from_dbs()
        # event = self.model.inscriptions.event
        # if event and event.ind_rel == 'I':
        #     self.view.set_ind()
        #     self.view.lsc_ind_inscriptions_plus.values = self.model.inscriptions
        #     self.view.lsc_ind_inscriptions_plus.load(custom_column_widths=True)
        # elif event and event.ind_rel == 'R':
        #     self.view.set_rel()
        #     self.view.lsc_rel_inscriptions_plus.values = self.model.inscriptions
        #     self.view.lsc_rel_inscriptions_plus.load(custom_column_widths=True)
        

    # def acept(self):
    #     self.view.get_values(prefs=self.model.prefs)
    #     self.model.prefs.save()
    #     self.view.view_plus.stop()

    def go_back(self):
        self.view.close()
        self.parent.load_me()
