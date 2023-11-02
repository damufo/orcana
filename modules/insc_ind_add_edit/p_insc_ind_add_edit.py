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
        phase = self.model.phase
        if inscription.result:
            message = _("Is not possible edit a inscription with a result.")
            self.view.msg.warning(message=message)
        else:
            values = self.view.get_values()
            msg = None
            
            if not person:
                msg =_("Set a person.")
                self.view.txt_person_full_name.SetFocus()
            elif not phase:
                msg = _('Set a phase.')
                self.view.cho_phase_id.SetFocus()
            elif self.model.inscription.is_inscript(
                    person_id=person.person_id,
                    phase_id=phase.phase_id):
                msg = _('This person already inscript in this phase.')
            elif not values['mark_hundredth']:
                msg = _('Set a mark.')
                self.view.txt_mark.SetFocus()
            elif not values['chrono_type']:
                msg = _('Set a chrono type.')
                self.view.cho_chrono_type.SetFocus()
            elif not values['pool_length']:
                msg = _('Set a pool length.')
                self.view.cho_pool_length.SetFocus()
            if msg:
                self.view.msg.warning(msg)
            else:
                inscription.person = person
                # If change phase move to new phase
                if inscription.inscription_id and inscription.phase != phase:
                    inscription.inscriptions.remove(inscription)
                inscription.inscriptions = phase.inscriptions
                # inscription.phase = phase
                # inscription.person = person
                inscription.mark_hundredth = values['mark_hundredth']
                inscription.pool_length = values['pool_length']
                inscription.chrono_type = values['chrono_type']
                inscription.date = values['date']
                inscription.venue = values['venue']
                inscription.rejected = values['rejected']
                inscription.exchanged = values['exchanged']
                inscription.score = values['score']
                inscription.classify = values['classify']
                inscription.save()
                if inscription not in phase.inscriptions:
                    phase.inscriptions.append(inscription)  #sobrecargado para que engada tamén a inscrición á persoa
                    # person.inscriptions.append(inscription) # isto debería cascar o correcto sería a liña de abaixo
                    # person.inscriptions.load()
                self.view.view_plus.stop()

    def phase_id_change(self):
        # self.model.inscription.person.entity_code = ""
        phase_id = self.view.view_plus.cho_get(self.view.cho_phase_id)
        self.model.phase = self.model.inscription.champ.phases.get_phase(phase_id)

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

