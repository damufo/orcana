# -*- coding: utf-8 -*-


from .m_phases import Model
from .v_phases import View
from .i_phases import Interactor


def create(parent, phases):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(phases=phases),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.lsc_plus.values = self.model.phases
        self.view.lsc_plus.load(custom_column_widths=True)

    def phase_categories(self):
        print("set categories")
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            phase = self.model.phases[idx]
            phase_categories = phase.phase_categories
            from modules.phase_categories import p_phase_categories
            p_phase_categories.create(parent=self, phase_categories=phase_categories)
            self.view.lsc_plus.update_item(idx)

    def move_down(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            if idx == (len(self.model.phases)-1):
                self.view.msg.warning(_("This is already the last element."))
            else:
                self.model.phases.move_down(idx)
                self.view.lsc_plus.update_item(idx)
                self.view.lsc_plus.update_item(idx + 1)
                self.view.lsc_plus.set_sel_pos_item(idx + 1)

    def move_up(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            if idx == 0:
                self.view.msg.warning(_("This is already the first element."))
            else:
                self.model.phases.move_up(idx)
                self.view.lsc_plus.update_item(idx)
                self.view.lsc_plus.update_item(idx - 1)
                self.view.lsc_plus.set_sel_pos_item(idx - 1)

    def copy_phase_categories(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            self.model.phase_categories_clipboard = self.model.phases[idx].phase_categories



    def paste_phase_categories(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        # elif len(idxs) > 1:
        #     self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            if self.model.phase_categories_clipboard is None:
                self.view.msg.warning(message=_("Phase categories clipboard is void."))
            else:
                # check if official
                has_official = False
                for idx in idxs:
                    phase = self.model.phases[idx]
                    if phase.official:
                        message=_("Selection invalid, the phase {} {} is official.").format(
                            phase.pos, phase.event.long_name)
                        self.view.msg.warning(message=message)
                        has_official = True
                        break

                if not has_official:
                    for idx in idxs:

                        self.model.phases[idx].phase_categories.delete_all_items()
                        self.model.phases[idx].phase_categories.paste_phase_categories(self.model.phase_categories_clipboard)

                        print(self.model.phases[idx].phase_id)
                        print(self.model.phases[idx].phase_categories.phase.phase_id)

                    self.view.lsc_plus.update_items(idxs)

    def go_back(self):
        self.view.close()
        self.parent.load_me()

    def sort(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            phase = self.model.phases[idx]
            if phase.official:
                message=_("Is not possible sort phase when is official.")
                self.view.msg.warning(message=message)
            else:
                sort = True
                message = _(
                    "This phase has heats."
                    "\nAre you sure that sort and delete current heats and results?")
                if not self.view.msg.question(message=message):
                    sort = False
                if sort:
                    phase.gen_heats()
                    self.view.lsc_plus.update_item(idx)

    def start_list(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        else:
            for idx in idxs:
                phase = self.model.phases[idx]
                phase.report_start_list_pdf()

    def add(self):
        phases = self.model.phases
        phase = phases.item_blank
        phase.lock = []
        from modules.phase_add_edit import p_phase_add_edit
        p_phase_add_edit.create(parent=self, phase=phase)
        if phase.phase_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(phases) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            phase = self.model.phases[idx]
            phase.lock = []
            # phase.lock = ['code']
            if phase.official:
                message=_("Is not possible edit phase when is official.")
                self.view.msg.warning(message=message)
            if len(phase.heats):
                phase.lock = ['event_id']
            from modules.phase_add_edit import p_phase_add_edit
            p_phase_add_edit.create(parent=self, phase=phase)
            self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items? "
                        "\nAll phase categories, phase heats and "
                        "\nphase results are deleted.")
            if self.view.msg.question(message=message):
                for i in idxs:
                    self.model.phases.delete_items(idxs)
                    self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))