# -*- coding: utf-8 -*-


from .m_insc_ind_add_edit import Model
from .v_insc_ind_add_edit import View
from .i_insc_ind_add_edit import Interactor


def create(parent, inscription, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(inscription=inscription),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(inscription=self.model.inscription)
        self.view.view_plus.start(modal=True)

    def acept(self):
        person = self.model.person
        inscription = self.model.inscription
        if person:
            if inscription.is_inscript(person):
                self.view.msg.warning("This person is already inscripted")
                self.view.txt_person_full_name.SetFocus()
            else:

                values = self.view.get_values()
                msg = None
                if not values['mark_hundredth']:
                    msg = 'Set a mark.'
                    self.view.txt_mark.SetFocus()
                elif not values['chrono_type']:
                    msg = 'Set a chrono type.'
                    self.view.cho_chrono_type.SetFocus()
                elif not values['pool_length']:
                    msg = 'Set a pool length.'
                    self.view.cho_pool_length.SetFocus()
                if msg:
                    self.view.msg.warning(msg)
                else:
                    inscription.person = person
                    inscription.mark_hundredth = values['mark_hundredth']
                    inscription.pool_length = values['pool_length']
                    inscription.chrono_type = values['chrono_type']
                    inscription.date = values['date']
                    inscription.venue = values['venue']
                    inscription.rejected = values['rejected']
                    inscription.exchanged = values['exchanged']
                    inscription.score = values['score']
                    inscription.classify = values['classify']
                    self.model.inscription.save()
                    self.view.view_plus.stop()
        else:
            self.view.msg.warning("No person selected.")
            self.view.txt_person_full_name.SetFocus()

    def person_full_name(self):
        # self.model.inscription.person.entity_code = ""
        person_name = self.view.txt_person_full_name.GetValue()
        if self.model.person_full_name_change:
            self.model.person = None
            person_name = self.view.txt_person_full_name.GetValue()
            if person_name:
                gender_id = None
                if self.model.inscription.event.gender_id != 'X':
                    gender_id = self.model.inscription.event.gender_id
                persons = self.model.inscription.champ.persons
                persons_match = persons.get_persons_with_name(
                    criterias=person_name, gender_id=gender_id)
                if len(persons_match) == 1:
                    self.view.txt_person_full_name.SetValue(persons_match[0].full_name)
                    self.view.lbl_license.SetLabel(persons_match[0].license)
                    self.view.lbl_entity_code.SetLabel(persons_match[0].entity.entity_code)
                    self.view.lbl_entity_short_name.SetLabel(persons_match[0].entity.short_name)
                    self.model.person = persons_match[0]
                elif len(persons_match) > 1:
                    choices = []
                    for i in persons_match:
                        choices.append(i.full_name)
                    choice = self.view.msg.choice(
                        _('Select entity'),
                        _('Select entity'), 
                        choices
                        )
                    if choice is not None:
                        self.view.txt_person_full_name.SetValue(persons_match[choice[0]].full_name)
                        self.view.lbl_license.SetLabel(persons_match[choice[0]].license)
                        self.view.lbl_entity_code.SetLabel(persons_match[choice[0]].entity.entity_code)
                        self.view.lbl_entity_short_name.SetLabel(persons_match[choice[0]].entity.short_name)
                        self.model.person = persons_match[choice[0]]
        # FIXME recuperar foco cando hai varias opcións
            self.view.set_person_values(self.model.person)
            self.model.person_full_name_change = False
            print('change off')

    def add_person(self):
        event = self.model.inscription.event
        persons = self.model.inscription.champ.persons
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
        # self.view.view_plus.close()
        # self.model.person.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

