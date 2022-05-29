# -*- coding: utf-8 -*-


from .m_persons import Model
from .v_persons import View
from .i_persons import Interactor


def create(parent, persons):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(persons=persons),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.persons.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.persons
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
        persons = self.model.persons
        person = persons.item_blank
        person.lock = []
        from modules.person_add_edit import p_person_add_edit
        p_person_add_edit.create(parent=self, person=person)
        if person.person_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(persons) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            person = self.model.persons[idx]
            person.lock = []
            if person.is_in_use_rel:
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
                    if self.model.persons[i].is_in_use:
                        message = '{} {} is in use.\nDelete first all inscriptions and results where it is being used.'.format(
                            self.model.persons[i].surname,
                            self.model.persons[i].name,
                        )
                        self.view.msg.warning(message=message)
                        break
                else:
                    self.model.persons.delete_items(idxs)
                    self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))