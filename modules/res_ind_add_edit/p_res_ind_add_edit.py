# -*- coding: utf-8 -*-


from email import message
from .m_res_ind_add_edit import Model
from .v_res_ind_add_edit import View
from .i_res_ind_add_edit import Interactor


def create(parent, result):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(result=result),
            view=View(parent.view),  # main_frame casca
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(result=self.model.result)
        self.view.view_plus.start(modal=True)

    def acept(self):
        person = self.model.person
        result = self.model.result
        if person:
            if result.is_inscript(person_id=person.person_id):
                self.view.msg.warning("This person is already inscripted")
                self.view.txt_person_full_name.SetFocus()
            else:
                result.person = person
                result.save()
                self.view.view_plus.stop()
        else:
            if result.result_id:
                message = "Are you sure you want to delete this person and results?"
                if self.view.msg.question(message):
                    print('delete person and results')
                    result.delete()
                    self.view.view_plus.stop()
            else:
                self.view.msg.warning("No person selected.")
                self.view.txt_person_full_name.SetFocus()

    def person_full_name(self):
        # self.model.result.person.entity_code = ""
        if self.model.person_full_name_change:
            self.model.person = None
            person_name = self.view.txt_person_full_name.GetValue()
            if person_name:
                gender_id = None
                if self.model.result.event.gender_id != 'X':
                    gender_id = self.model.result.event.gender_id
                persons = self.model.result.champ.persons
                persons_match = persons.get_persons_with_name(
                    criterias=person_name, gender_id=gender_id)
                if len(persons_match) == 1:
                    self.model.person = persons_match[0]
                elif len(persons_match) > 1:
                    choices = []
                    for i in persons_match:
                        choices.append('{} {}'.format(i.full_name, i.license))
                    choice = self.view.msg.choice(
                        _('Select entity'),
                        _('Select entity'), 
                        choices
                        )
                    if choice is not None:
                        self.model.person = persons_match[choice[0]]
            self.view.set_person_values(self.model.person)
            self.model.person_full_name_change = False
            print('change off')
        # FIXME recuperar foco cando hai varias opcións

    def add_person(self):
        event = self.model.result.event
        persons = self.model.result.champ.persons
        person = persons.item_blank
        person.lock = []
        if event.gender_id != 'X':
            person.gender_id = event.gender_id
            person.lock.append('gender_id')
        from modules.person_add_edit import p_person_add_edit
        p_person_add_edit.create(parent=self, person=person)
        if person.person_id:  # foi engadida
            self.model.person = person
            self.view.set_person_values(self.model.person)


    def cancel(self):
        self.view.view_plus.stop()

