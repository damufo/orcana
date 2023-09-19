# -*- coding: utf-8 -*-


from .m_classifications import Model
from .v_classifications import View
from .i_classifications import Interactor


def create(parent, classifications):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(classifications=classifications),
            view=View(parent.parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.classifications.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.classifications
        self.view.lsc_plus.load(custom_column_widths=True)

    def go_back(self):
        self.view.close()
        self.parent.parent.load_properties()

    def move_down(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            if idx == (len(self.model.classifications) - 1):
                self.view.msg.warning(_("This is already the last element."))
            else:
                self.model.classifications.move_down(idx)
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
                self.model.classifications.move_up(idx)
                self.view.lsc_plus.update_item(idx)
                self.view.lsc_plus.update_item(idx - 1)
                self.view.lsc_plus.set_sel_pos_item(idx - 1)
 
    def add(self):
        classifications = self.model.classifications
        classification = classifications.item_blank
        classification.lock = []
        from modules.classification_add_edit import p_classification_add_edit
        p_classification_add_edit.create(parent=self, classification=classification)
        if classification.classification_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(classifications) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            classification = self.model.classifications[idx]
            classification.lock = []
            # classification.lock = ['code']
            from modules.classification_add_edit import p_classification_add_edit
            p_classification_add_edit.create(parent=self, classification=classification)
            self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items?")
            if self.view.msg.question(message=message):
                self.model.classifications.delete_items(idxs)
                self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))