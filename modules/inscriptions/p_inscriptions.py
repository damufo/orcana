# -*- coding: utf-8 -*-


from .m_inscriptions import Model
from .v_inscriptions import View
from .i_inscriptions import Interactor


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
        self.view.set_events(self.model.champ.events)
        self.view_refresh()

    def view_refresh(self):
        event_id = self.view.get_event_id()
        event = self.model.champ.events.get_event(event_id)
        self.model.inscriptions = event.inscriptions
        self.model.inscriptions.load_items_from_dbs()
        if event.ind_rel == 'I':
            self.view.set_ind()
            # self.view.lsc_ind_inscriptions_plus.values = event.inscriptions
            # self.view.lsc_ind_inscriptions_plus.load(custom_column_widths=True)
        elif event.ind_rel == 'R':
            self.view.set_rel()
            # self.view.lsc_rel_inscriptions_plus.values = event.inscriptions
            # self.view.lsc_rel_inscriptions_plus.load(custom_column_widths=True)
        self.view.lsc_plus.values = event.inscriptions
        self.view.lsc_plus.load(custom_column_widths=True)
        

    def add(self):
        inscriptions = self.model.inscriptions
        inscription = inscriptions.item_blank
        if inscriptions.ind_rel == 'I':
            from modules.insc_ind_add_edit import p_insc_ind_add_edit
            p_insc_ind_add_edit.create(parent=self, inscription=inscription)
            if inscription.inscription_id:  # foi engadida
                inscriptions.append(inscription)
                self.view.lsc_plus.add_last_item()
                self.view.lsc.EnsureVisible(len(inscriptions) - 1)
        elif inscriptions.ind_rel == 'R':
            from modules.insc_rel_add_edit import p_insc_rel_add_edit
            p_insc_rel_add_edit.create(parent=self, inscription=inscription)
            if inscription.inscription_id:  # foi engadida
                inscriptions.append(inscription)
                self.view.lsc_plus.add_last_item()
                self.view.lsc.EnsureVisible(len(inscriptions) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            inscription = self.model.inscriptions[idx]
            if self.model.inscriptions.ind_rel == 'I':
                from modules.insc_ind_add_edit import p_insc_ind_add_edit
                p_insc_ind_add_edit.create(parent=self, inscription=inscription)
                self.view.lsc_plus.update_item(idx)
            elif self.model.inscriptions.ind_rel == 'R':
                from modules.insc_rel_add_edit import p_insc_rel_add_edit
                p_insc_rel_add_edit.create(parent=self, inscription=inscription)
                self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items?")
            if self.view.msg.question(message=message):
                self.model.inscriptions.delete_items(idxs)
                self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))

    def go_back(self):
        self.view.close()
        self.parent.load_me()
