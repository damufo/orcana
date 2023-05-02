# -*- coding: utf-8 -*-


from email import message
from xml.dom.minidom import Entity
from .m_res_rel_add_edit import Model
from .v_res_rel_add_edit import View
from .i_res_rel_add_edit import Interactor


def create(parent, result):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(result=result),
            view=View(parent.view),
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
        result = self.model.result
        
        entity_selected = self.model.entity_selected
        if entity_selected:
            msg = None
            values = self.view.get_values()
            if not values["relay_name"]:
                msg = 'Set a relay name.'
                self.view.txt_relay_name.SetFocus()
            elif not values["category_id"]:
                msg = 'Set a relay category.'
                self.view.txt_relay_category.SetFocus()
            if msg:
                self.view.msg.warning(msg)
            else:
                # Has entity change
                if self.model.entity_change and result.result_members:
                    message = "Members will be deleted, do you want to continue?"
                    if self.view.msg.question(message):
                        result.result_members.delete_all_items()
                    else:
                        return
                category = result.champ.categories.get_category(category_id=values['category_id'])
                result.relay.name = values["relay_name"]
                result.relay.gender_id = category.gender_id
                result.relay.category = category
                result.relay.entity = entity_selected
                result.save()
                self.view.view_plus.stop()
        else:
            if result.result_id:
                message = "Are you sure you want to delete this relay and results?"
                if self.view.msg.question(message):
                    print('delete relay and results')
                    result.delete()
                    self.view.view_plus.stop()
            else:
                self.view.msg.warning("No entity selected.")
                self.view.txt_entity_name.SetFocus()

    def entity_name(self):
        entity_name = self.view.txt_entity_name.GetValue()
        if self.model.entity_name_change:
            if self.model.entity_selected:
                old_entity_id = self.model.entity_selected.entity_id
            else:
                old_entity_id = None
            # self.model.entity = None
            if entity_name:
                if ((self.model.entity_selected and (entity_name != 
                self.model.entity_selected.short_name)) or not self.model.entity_selected):
                    entities = self.model.result.champ.entities
                    entities_match = entities.get_entities_with_name(
                        name=entity_name)
                    if len(entities_match) == 1:
                        self.model.entity_selected = entities_match[0]
                    elif len(entities_match) > 1:
                        choices = []
                        for i in entities_match:
                            choices.append('{} {}'.format(i.short_name, i.entity_code))
                        choice = self.view.msg.choice(
                            _('Select entity'),
                            _('Select entity'), 
                            choices
                            )
                        if choice is not None:
                            self.model.entity_selected = entities_match[choice[0]]
                if (self.model.entity_selected and
                    (self.model.entity_selected.entity_id != old_entity_id or 
                        not self.view.txt_relay_name.GetValue())):
                    self.set_relay_name()
                elif not self.model.entity_selected:
                    self.view.txt_relay_name.SetValue('')
            else:
                self.model.entity_selected = None
                self.view.txt_relay_name.SetValue('')
            self.view.set_entity_values(entity=self.model.entity_selected)
            self.model.entity_name_change = False
            print('change off')
        # FIXME recuperar foco cando hai varias opcións

    def set_relay_name(self):
        # Conta as remudas que hai desa entidade e propón o total +1 como nome
        count = 1
        for i in self.model.result.heat.phase.results:
            if (i.relay.entity.entity_code == self.model.entity_selected.entity_code
                and i.relay != self.model.result.relay):
                count += 1
        self.view.txt_relay_name.SetValue('{} {}'.format(self.model.entity_selected.short_name, str(count).zfill(2)))
        self.view.txt_relay_name.SetFocus()

    def add_entity(self):
        entities = self.model.result.champ.entities
        entity = entities.item_blank
        entity.lock = []
        from modules.entity_add_edit import p_entity_add_edit
        p_entity_add_edit.create(parent=self, entity=entity)
        if entity.entity_id:  # foi engadida
            self.model.entity = entity
            self.view.set_entity_values(self.model.entity)
            self.set_relay_name()


    def cancel(self):
        self.view.view_plus.stop()

