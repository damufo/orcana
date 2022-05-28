# -*- coding: utf-8 -*-


from .m_relays import Model
from .v_relays import View
from .i_relays import Interactor


def create(parent, relays):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(relays=relays),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.relays.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.relays
        self.view.lsc_plus.load(custom_column_widths=True)
        # self.view.set_values(prefs=self.model.prefs)
        # self.view.view_plus.start(modal=True)

    # def acept(self):
    #     self.view.get_values(prefs=self.model.prefs)
    #     self.model.prefs.save()
    #     self.view.view_plus.stop()

    def go_back(self):
        self.view.close()
        self.parent.load_me()

    def add(self):
        relays = self.model.relays
        person = relays.item_blank
        from modules.person_add_edit import p_person_add_edit
        p_person_add_edit.create(parent=self, person=person)
        if person.person_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(relays) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            person = self.model.relays[idx]
            person.lock = []
            person.lock.append('entity_id')
            from modules.person_add_edit import p_person_add_edit
            p_person_add_edit.create(parent=self, person=person)
            self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items?")
            if self.view.msg.question(message=message):
                for i in idxs:
                    if self.model.relays[i].is_in_use:
                        message = '{} {} is in use.\nDelete first all inscriptions and results where it is being used.'.format(
                            self.model.relays[i].surname,
                            self.model.relays[i].name,
                        )
                        self.view.msg.warning(message=message)
                        break
                else:
                    self.model.relays.delete_items(idxs)
                    self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))