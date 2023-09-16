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
        self.name = "inscriptions"
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_phases(self.model.champ.phases)
        config_views = self.model.champ.config.views
        if 'inscriptions' in config_views:
            phase_id = config_views['inscriptions']['phase_id']
            inscription_pos = config_views['inscriptions']['inscription_pos']
            self.view.view_plus.cho_set(choice=self.view.cho_phase_id, value=phase_id)
            self.load_inscriptions(phase_id=phase_id)
            self.view.lsc_plus.set_sel_pos_item(inscription_pos)
            self.view.lsc.SetFocus()
        else:
            self.view.lsc_plus.set_sel_pos_item(0)

        self.view_refresh()

    def view_refresh(self):
        phase_id = self.view.get_phase_id()
        self.load_inscriptions(phase_id=phase_id)
    
    def load_inscriptions(self, phase_id):
        phase = self.model.champ.phases.get_phase(phase_id)
        self.model.inscriptions = phase.inscriptions
        # self.model.inscriptions.load_items_from_dbs()
        if phase.ind_rel == 'I':
            self.view.set_ind()
            # self.view.lsc_ind_inscriptions_plus.values = event.inscriptions
            # self.view.lsc_ind_inscriptions_plus.load(custom_column_widths=True)
            self.view.btn_members.Enable(False)
        elif phase.ind_rel == 'R':
            self.view.set_rel()
            # self.view.lsc_rel_inscriptions_plus.values = event.inscriptions
            # self.view.lsc_rel_inscriptions_plus.load(custom_column_widths=True)
            self.view.btn_members.Enable(True)
        self.view.lsc_plus.values = phase.inscriptions
        self.view.lsc_plus.load(custom_column_widths=True)
        

    def import_from_file(self):
        msg = self.view.msg
        champ = self.model.inscriptions.champ
        file_path = self.view.msg.open_file(
            suffixes=[".csv"],
            )
        if not file_path:
            msg.error(_("No file was selected."))
        else:
            if not file_path.exists() or file_path.is_dir():
                msg.error(_("The file not exists."))
            else:
                file_valid = champ.import_insc_from_file(file_path=file_path)
                if not file_valid:
                    msg.error(_("This file haven't a format correct."))
                else:
                    self.view_refresh()

    def load_members(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            relay_members = self.model.inscriptions[idx].relay.relay_members
            inscriptions_view = {}
            inscriptions_view['phase_id'] = self.view.view_plus.cho_get(choice=self.view.cho_phase_id)
            inscriptions_view['inscription_pos'] = self.view.lsc_plus.get_sel_pos_item()
            self.model.inscriptions.config.views['inscriptions'] = inscriptions_view
            self.view.lsc_plus.save_custom_column_width()
            from modules.relay_members import p_relay_members
            p_relay_members.create(parent=self, relay_members=relay_members)

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
            msg = False
            for i in idxs:
                if self.model.inscriptions[i].result and self.model.inscriptions[i].result.official:
                    msg = _("Is not possible delete a official result.")
                    break
            if msg:
                self.view.msg.warning(message=msg)
            else:
                message = _("Are you sure that delete selected items?\n"
                    "If has results, they are deleted.")
                if self.view.msg.question(message=message):
                    self.model.inscriptions.delete_items(idxs)
                    self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))

    def go_back(self):
        self.view.close()
        self.parent.load_me()
