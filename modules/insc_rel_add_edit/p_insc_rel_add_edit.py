# -*- coding: utf-8 -*-


from .m_insc_rel_add_edit import Model
from .v_insc_rel_add_edit import View
from .i_insc_rel_add_edit import Interactor


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
        entity = self.model.entity
        inscription = self.model.inscription     
        values  = self.view.get_values()
        msg = None
        if not entity: 
            msg = _('Set a entity.')
            self.view.txt_entity_name.SetFocus()
        elif not values['relay_name']:
            msg = _('Set a relay name.')
            self.view.txt_relay_name.SetFocus()
        elif not values['category_id']:
            msg = _('Set a relay category.')
            self.view.cho_category_id.SetFocus()
        elif not values['mark_hundredth']:
            msg = _('Set a mark.')
            self.view.txt_mark.SetFocus()
        elif not values['pool_length']:
            msg = _('Set a pool length.')
            self.view.cho_pool_length.SetFocus()
        elif not values['chrono_type']:
            msg = _('Set a chrono type.')
            self.view.cho_chrono_type.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            phase = inscription.phase
            phase_categories = phase.phase_categories.dict
            relay_category = phase_categories[values["category_id"]].category
            name = values['relay_name']
            match_inscription = inscription.inscriptions.search_relay(entity=entity, category=relay_category, name=name)
            if match_inscription and (match_inscription != inscription):  # é distinta
                msg = _('This relay already exists.')
                self.view.msg.warning(msg)
            else:
                if inscription.inscription_id:  # If exists inscription (edit mode)
                    clear_relayers = False
                    if inscription.relay.entity != entity:
                        clear_relayers = True
                    if inscription.relay.category != relay_category:
                        if inscription.relay.relay_members and self.view.msg.question(_('Delete members?')):
                            clear_relayers = True
                    if clear_relayers:
                        inscription.relay.relay_members.delete_all_items()

                inscription.relay.entity = entity
                # FIXME: o de abaixo seguramente debería borrarse xa que o sexo ten que obterse da categoría.
                # ou non, ver o caso no que sexa proba mixta de remudas e clasificacións por sexo.
                # pensándoo penso que non hai problema se se usa o sexo da categoría
                inscription.relay.gender_id = self.model.inscription.event.gender_id
                inscription.relay.name = name
                inscription.relay.category = relay_category
                inscription.relay.gender_id = relay_category.gender_id
                inscription.relay.save()
                if inscription.relay not in inscription.relay.relays:
                    inscription.relay.relays.append(inscription.relay)
                inscription.mark_hundredth = values['mark_hundredth']
                inscription.chrono_type = values['chrono_type']
                inscription.pool_length = values['pool_length']
                inscription.date = values['date']
                inscription.venue = values['venue']
                inscription.rejected = values['rejected']
                inscription.exchanged = values['exchanged']
                inscription.score = values['score']
                inscription.classify = values['classify']
                inscription.save()
                if inscription not in phase.inscriptions:
                    phase.inscriptions.append(inscription)
                self.view.view_plus.stop()

    def entity_name(self):
        entity_name = self.view.txt_entity_name.GetValue()
        if self.model.entity_name_change:
            if self.model.entity:
                old_entity_id = self.model.entity.entity_id
            else:
                old_entity_id = None
            self.model.entity = None
            if entity_name:
                if ((self.model.entity and (entity_name != 
                self.model.entity.short_name)) or not self.model.entity):
                    entities = self.model.inscription.champ.entities
                    entities_match = entities.get_entities_with_name(
                        name=entity_name)
                    if len(entities_match) == 1:
                        self.view.txt_entity_name.SetValue(entities_match[0].short_name)
                        self.view.lbl_entity_code.SetLabel(entities_match[0].entity_code)
                        self.model.entity = entities_match[0]
                    elif len(entities_match) > 1:
                        choices = []
                        for i in entities_match:
                            choices.append(i.short_name)
                        choice = self.view.msg.choice(
                            _('Select entity'),
                            _('Select entity'), 
                            choices
                            )
                        if choice is not None:
                            self.view.txt_entity_name.SetValue(entities_match[choice[0]].short_name)
                            self.view.lbl_entity_code.SetLabel(entities_match[choice[0]].entity_code)
                            self.view.txt_relay_name.SetValue('{} 01'.format(entities_match[choice[0]].short_name))
                            self.model.entity = entities_match[choice[0]]
            if self.model.entity and self.model.entity.entity_id != old_entity_id:
                self.set_relay_name()
            else:
                self.view.txt_relay_name.SetValue('')
            self.view.set_entity_values(self.model.entity)
            self.model.entity_name_change = False
            print('change off')

        # FIXME recuperar foco cando hai varias opcións

    def set_relay_name(self):
        count = 1
        for i in self.model.inscription.inscriptions:
            if i.relay.entity.entity_code == self.model.entity.entity_code:
                count += 1
        self.view.txt_relay_name.SetValue('{} {}'.format(self.model.entity.short_name, str(count).zfill(2)))
        self.view.txt_relay_name.SetFocus()

    def add_entity(self):
        entities = self.model.inscription.champ.entities
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

