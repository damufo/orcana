# -*- coding: utf-8 -*-


from .m_person_add_edit import Model
from .v_person_add_edit import View
from .i_person_add_edit import Interactor


def create(parent, person, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(person=person),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(person=self.model.person)
        self.view.view_plus.start(modal=True)

    def acept(self):
        person = self.model.person
        values = self.view.get_values()
        msg = None
        if not values['surname']:
            msg = 'Set a surname.'
            self.view.txt_surname.SetFocus()
        elif not values['name']:
            msg = 'Set a name.'
            self.view.txt_name.SetFocus()
        elif not values['gender_id']:
            msg = 'Set a gender.'
            self.view.cho_gender_id.SetFocus()
        elif not values['birth_date']:
            msg = 'Set a birth date.'
            self.view.txt_birth_date.SetFocus()
        elif not self.model.entity:
            msg = 'Set a entity.'
            self.view.txt_entity_name.SetFocus()
        elif person.persons.check_exists_license(person, values['license']):
            msg = 'This license already exists.'
            self.view.txt_license.SetFocus()

        if msg:
            self.view.msg.warning(msg)
        else:
            person.license = values['license']
            person.surname = values['surname']
            person.name = values['name']
            person.gender_id = values['gender_id']
            person.birth_date = values['birth_date']
            person.entity = self.model.entity
            self.model.person.save()
            if not person in person.persons:
                person.persons.append(person)
            self.view.view_plus.stop()

    def entity_name(self):
        if self.model.entity_name_change:
            self.model.entity = None
            entity_name = self.view.txt_entity_name.GetValue()
            if entity_name:
                entities = self.model.person.champ.entities
                entities_match = entities.get_entities_with_name(entity_name)
                if len(entities_match) == 1:
                    self.model.entity = self.model.person.champ.entities.get_entity_by_code(entities_match[0].entity_code)
                elif len(entities_match) > 1:
                    choices = []
                    for i in entities_match:
                        choices.append(i.medium_name)
                    choice = self.view.msg.choice(
                        _('Select entity'),
                        _('Select entity'), 
                        choices
                        )
                    if choice is not None:
                        self.model.entity = self.model.person.champ.entities.get_entity_by_code(entities_match[0].entity_code)
            self.view.set_entity_values(self.model.entity)
            self.model.entity_name_change = False
        # FIXME recuperar foco cando hai varias opcións
        # self.view.txt_entity_short_name.SetFocus()
        # print(self.view.HasFocus())
        # # self.view.Show()
        # self.view.SetFocus()
        # self.view.panel.SetFocus()
        # self.view.panel.SetFocusIgnoringChildren()
        # print(self.view.panel.HasFocus())
        # print('pasou')

    def add_entity(self):
        entities = self.model.person.champ.entities
        entity = entities.item_blank
        entity.lock = []
        from modules.entity_add_edit import p_entity_add_edit
        p_entity_add_edit.create(parent=self, entity=entity)
        if entity.entity_id:  # foi engadida
            self.model.entity = entity
            self.view.set_entity_values(self.model.entity)

    def cancel(self):
        # self.view.view_plus.close()
        # self.model.person.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

