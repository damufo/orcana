# -*- coding: utf-8 -*-


from .m_punctuations import Model
from .v_punctuations import View
from .i_punctuations import Interactor


def create(parent, punctuations):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(punctuations=punctuations),
            view=View(parent.parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.punctuations.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.punctuations
        self.view.lsc_plus.load(custom_column_widths=True)

    def go_back(self):
        self.view.close()
        self.parent.parent.load_properties()

    def add(self):
        punctuations = self.model.punctuations
        punctuation = punctuations.item_blank
        punctuation.lock = []
        from modules.punctuation_add_edit import p_punctuation_add_edit
        p_punctuation_add_edit.create(parent=self, punctuation=punctuation)
        if punctuation.punctuation_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(punctuations) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            punctuation = self.model.punctuations[idx]
            punctuation.lock = []
            # punctuation.lock = ['code']
            from modules.punctuation_add_edit import p_punctuation_add_edit
            p_punctuation_add_edit.create(parent=self, punctuation=punctuation)
            self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items?")
            if self.view.msg.question(message=message):
                self.model.punctuations.delete_items(idxs)
                self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))