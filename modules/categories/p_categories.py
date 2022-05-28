# -*- coding: utf-8 -*-


from .m_categories import Model
from .v_categories import View
from .i_categories import Interactor


def create(parent, categories):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(categories=categories),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.categories.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.categories
        self.view.lsc_plus.load(custom_column_widths=True)

    def go_back(self):
        self.view.close()
        self.parent.load_me()

    def add(self):
        categories = self.model.categories
        category = categories.item_blank
        category.lock = []
        from modules.category_add_edit import p_category_add_edit
        p_category_add_edit.create(parent=self, category=category)
        if category.category_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(categories) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            category = self.model.categories[idx]
            category.lock = []
            # category.lock = ['code']
            from modules.category_add_edit import p_category_add_edit
            p_category_add_edit.create(parent=self, category=category)
            self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items?")
            if self.view.msg.question(message=message):
                for i in idxs:
                    if self.model.categories[i].is_in_use:
                        message = ('{} {} is in use.\nDelete first all '
                            'events where it is being used.').format(
                                self.model.categories[i].name,
                                self.model.categories[i].code,
                                )
                        self.view.msg.warning(message=message)
                        break
                else:
                    self.model.categories.delete_items(idxs)
                    self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))