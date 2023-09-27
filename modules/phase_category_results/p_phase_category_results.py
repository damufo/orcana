# -*- coding: utf-8 -*-


from .m_phase_category_results import Model
from .v_phase_category_results import View
from .i_phase_category_results import Interactor



def create(parent, champ):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(champ=champ),
            view=View(parent.parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.name = "inscriptions"
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        if self.model.champ.phases:
            config_views = self.model.champ.config.views
            if ('phase_category_results' in config_views and
                    config_views['phase_category_results']['phase_id']):
                phase_id = config_views['phase_category_results']['phase_id']
                phase_category_id = config_views['phase_category_results']['phase_category_id']
            else:
                phase_id = self.model.champ.phases[0].phase_id
                phase_category_id = self.model.champ.phases[0].phase_categories[0]
            
            self.model.phase = self.model.champ.phases.get_phase(phase_id)
            self.model.phase_category = self.model.phase.phase_categories.get_phase_category(phase_category_id)
            self.view.set_phases(self.model.champ.phases)
            if self.model.phase != self.model.champ.phases[0]:
                self.view.view_plus.cho_set(
                        choice=self.view.cho_phase_id,
                        value=self.model.phase.phase_id)
            if self.model.phase_category != self.model.phase.phase_categories[0]:
                self.view.view_plus.cho_set(
                        choice=self.view.cho_phase_category,
                        value=self.model.phase_category.phase_category_id)
            self.load_phase_category_results()
        else:
            self.view.msg.error(_('No phases available.'))
            self.go_back()

    def phase_change(self):
        phase_id = self.view.get_phase_id()
        self.model.phase = self.model.champ.phases.get_phase(phase_id)
        phase_categories = self.model.phase.phase_categories
        self.model.phase_category = phase_categories[0]  # select fist
        self.view.set_phase_categories(phase_categories=phase_categories)
        self.load_phase_category_results()

    def phase_category_change(self):
        phase_category_id = self.view.get_phase_category_id()
        self.model.phase_category = self.model.phase.phase_categories.get_phase_category(phase_category_id)
        self.load_phase_category_results()
    
    def load_phase_category_results(self):
        phase = self.model.phase
        phase_category = self.model.phase_category
        phase_category_results = phase_category.phase_category_results

        # self.model.inscriptions.load_items_from_dbs()
        if phase.ind_rel == 'I':
            self.view.set_ind()
        elif phase.ind_rel == 'R':
            self.view.set_rel()
        phase_category_results.load_items_from_dbs()
        self.view.lsc_plus.values = phase_category_results
        self.view.lsc_plus.load(custom_column_widths=True)
        self.model.phase_category_results = phase_category_results

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            phase_category_result = self.model.phase_category_results[idx]
            phase_category_result.lock = []

            from modules.phase_category_result_edit import p_phase_category_result_edit
            p_phase_category_result_edit.create(parent=self, phase_category_result=phase_category_result)
            self.view.lsc_plus.update_item(idx)

    def go_back(self):
        self.view.close()
        self.parent.parent.load_heats()
