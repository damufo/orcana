# -*- coding: utf-8 -*-


from .m_phase_categories_categories_add import Model
from .v_phase_categories_categories_add import View
from .i_phase_categories_categories_add import Interactor
import copy

def create(parent, phase_categories):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(phase_categories=phase_categories),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        champ_categories = copy.copy(self.model.phase_categories.champ.categories)
        phase = self.model.phase_categories.phase
        # Remove current categories from list
        idxs_to_remove = []
        for i in self.model.phase_categories:
            champ_categories.remove(i.category)
        # Remove incompatible categories
        gender_id = self.model.phase_categories.phase.event.gender_id
        if gender_id == "X" and phase.event.ind_rel == "R":
            for i in copy.copy(champ_categories):
                print((i.code, i.gender_id))
                if i.gender_id != "X":
                    champ_categories.remove(i)
        elif self.model.phase_categories.phase.event.gender_id != "X":
            for i in copy.copy(champ_categories):
                print((i.code, i.gender_id))
                if i.gender_id != gender_id:
                    champ_categories.remove(i)
        self.model.champ_categories = champ_categories
        self.view.lsc_plus.values = champ_categories
        self.view.lsc_plus.load(custom_column_widths=True)
        self.view.set_values()

        self.view.view_plus.start(modal=True)

    def acept(self):       
        if self.view.categories_selected:
            categories = [self.model.champ_categories[i] for i in self.view.categories_selected]
            action = self.view.get_values()
            self.model.phase_categories.add_items(
                categories=categories,
                action=action,
                )
            self.view.view_plus.stop()
        else:
            self.view.msg.warning(message=_("No item selected."))

    def select_categories(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        for idx in idxs:
            if idx not in self.view.categories_selected:
                self.view.categories_selected.append(idx)
        for selected in self.view.categories_selected:
            if selected not in idxs:
                self.view.categories_selected.remove(selected)
        
        # current_selected = len(self.model.result_members)
        # current_categories = len(self.view.categories_selected)
        print(', '.join([self.model.champ_categories[i].name for i in self.view.categories_selected]))

    def add_category(self):
        entities = self.model.person.champ.entities
        entity = entities.item_blank
        entity.lock = []
        from modules.entity_add_edit import p_entity_add_edit
        p_entity_add_edit.create(parent=self, entity=entity)
        if entity.entity_id:  # foi engadida
            self.model.entity = entity
            self.view.set_entity_values(self.model.entity)

    def cancel(self):
        # self.view.view_plus.close()
        # self.model.person.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

