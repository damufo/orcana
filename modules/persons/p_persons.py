# -*- coding: utf-8 -*-


from .m_persons import Model
from .v_persons import View
from .i_persons import Interactor

from specific_classes.champ.inscriptions import Inscriptions


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
        self.view.lsc_persons_plus.values = self.model.persons
        self.view.lsc_persons_plus.load(custom_column_widths=True)

        # self.view.set_values(prefs=self.model.prefs)
        # self.view.view_plus.start(modal=True)
        if self.model.persons:
            self.view.lsc_persons.Focus(0)
            self.view.lsc_persons.Select(0)
        self.view.load_splitter()

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
            self.view.lsc_persons_plus.add_last_item()
            self.view.lsc_persons.EnsureVisible(len(persons) - 1)

    def edit(self):
        idxs = self.view.lsc_persons_plus.get_sel_pos_items()
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
            self.view.lsc_persons_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_persons_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected persons?")
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
                    self.view.lsc_persons_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))

    def select_person(self):
        idx = self.view.lsc_persons_plus.get_sel_pos_item()
        if idx is not None:
            person = self.model.persons[idx]
            self.model.person = person

            self.view.lsc_inscriptions_ind_plus.save_custom_column_width()
            person.inscriptions.load()
            self.view.lsc_inscriptions_ind_plus.values = person.inscriptions
            print(len(self.view.lsc_inscriptions_ind_plus.values))
            self.view.lsc_inscriptions_ind_plus.load(custom_column_widths=True)
        else:
            self.model.person = None
            self.view.lsc_inscriptions_ind.DeleteAllItems()

    def add_insc(self):
        inscriptions = self.model.person.inscriptions
        inscription = inscriptions.item_blank
        inscription.lock = []
        inscription.lock.append('person')
        from modules.insc_ind_add_edit import p_insc_ind_add_edit
        p_insc_ind_add_edit.create(parent=self, inscription=inscription)
        if inscription.inscription_id:  # foi engadida
            self.view.lsc_inscriptions_ind_plus.add_last_item()
            self.view.lsc_inscriptions_ind.EnsureVisible(len(self.model.person.inscriptions) - 1)

    def edit_insc(self):
        idxs = self.view.lsc_inscriptions_ind_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            inscription = self.model.person.inscriptions[idx]
            inscription.lock = []
            inscription.lock.append('person')
            from modules.insc_ind_add_edit import p_insc_ind_add_edit
            p_insc_ind_add_edit.create(parent=self, inscription=inscription)
            self.view.lsc_inscriptions_ind_plus.update_item(idx)

    def delete_insc(self):
        idxs = self.view.lsc_inscriptions_ind_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected inscriptions?\n"
                        "If has results, they are deleted.")
            if self.view.msg.question(message=message):
                msg = False
                for i in idxs:
                    inscription = self.model.person.inscriptions[i]
                    if inscription.result and inscription.result.official:
                        msg = _("Is not possible delete a official result.")
                        break
                if msg:
                    self.view.msg.warning(message=msg)
                else:
                        self.model.person.inscriptions.delete_items(idxs)
                        self.view.lsc_inscriptions_ind_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))



        # if idxs:
        #     message = _("Are you sure that delete selected inscriptions?")
        #     if self.view.msg.question(message=message):
        #         for i in idxs:
        #             if self.model.person.inscriptions[i].result:
        #                 message = '{} has result.\nDelete first all results and results where it is being used.'.format(
        #                     self.model.person.inscriptions[i].phase.full_name
        #                 )
        #                 self.view.msg.warning(message=message)
        #                 break
        #         else:
        #             self.model.persons.delete_items(idxs)
        #             self.view.lsc_persons_plus.delete_items(idxs)
        # else:
        #     self.view.msg.warning(message=_("No item selected."))