# -*- coding: utf-8 -*-


from .m_phase_categories import Model
from .v_phase_categories import View
from .i_phase_categories import Interactor


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
        self.view.lsc_plus.values = self.model.phase_categories
        self.view.lsc_plus.load(custom_column_widths=True)
        self.view.view_plus.start(modal=True)

    def edit(self):
        pass

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items?")
            if self.view.msg.question(message=message):
                for idx in sorted(idxs, reverse=True):
                    phase = self.model.phase_categories.phase
                    if phase.official:
                        message = '{} {} is official.\nIs not possible delte this phase.'
                        message = message.format(
                            phase.pos,
                            phase.event.name,
                            )
                        self.view.msg.warning(message=message)
                        continue
                    else:
                        self.model.phase_categories.delete_item(idx)
                        self.view.lsc_plus.delete_item(idx)
        else:
            self.view.msg.warning(message=_("No item selected."))

    def add(self):
        print("add categories")
        phase_categories = self.model.phase_categories
        categories_count = len(phase_categories)
        from modules.phase_categories_categories_add import p_phase_categories_categories_add
        p_phase_categories_categories_add.create(parent=self, phase_categories=phase_categories)
        if categories_count < len(phase_categories):
            # for idx in range(start=categories_count-1, stop=len(phase_categories)-1):
            #     self.view.lsc_plus._item(idx)
            self.view.lsc_plus.load()

    def move_down(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            if idx == (len(self.model.phase_categories)-1):
                self.view.msg.warning(_("This is already the last element."))
            else:
                self.model.phase_categories.move_down(idx)
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
                self.model.phase_categories.move_up(idx)
                self.view.lsc_plus.update_item(idx)
                self.view.lsc_plus.update_item(idx - 1)
                self.view.lsc_plus.set_sel_pos_item(idx - 1)
    
    def go_back(self):
        # self.view.view_plus.close()
        # self.model.person.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

