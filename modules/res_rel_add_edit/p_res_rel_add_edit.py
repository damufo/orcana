# -*- coding: utf-8 -*-


from email import message
from xml.dom.minidom import Entity
from .m_res_rel_add_edit import Model
from .v_res_rel_add_edit import View
from .i_res_rel_add_edit import Interactor


def create(parent, heat, lane, result):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(heat=heat, lane=lane, result=result),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view 
        interactor.install(self, view)
        self.view.set_heat(heat=self.model.heat)
        self.view.set_lane(lane=self.model.lane)
        if self.model.result:
            self.view.set_entity(entity=self.model.relay.entity)
            self.view.set_relay(relay=self.model.relay)
        self.view.txt_entity_name.SetFocus()
        self.view.view_plus.start(modal=True)

    def delete(self):
        current_result = self.model.result
        if current_result.result_id:  # Question if remove current result
            message = "Are you sure you want to delete this result?"
            if self.view.msg.question(message):
                print('set inscription as rejected and delete current result')
                current_result.inscription.rejected = True
                current_result.inscription.result = None
                current_result.inscription.save()
                current_result.delete()
                self.view.view_plus.stop()
        else:
            self.view.msg.warning("There was no longer a relay to delete.")
            self.view.tx_entity_name.SetFocus()
            
    def acept(self):
        current_heat = self.model.heat
        current_lane = self.model.lane
        current_result = self.model.result
        new_entity = self.model.entity_selected
        msg = None
        values = self.view.get_values()
        if not self.model.entity_selected:
            msg = 'Set a entity.'
            self.view.txt_entity_name.SetFocus()
        elif not values["relay_name"]:
            msg = 'Set a relay name.'
            self.view.txt_relay_name.SetFocus()
        elif not values["category_id"]:
            msg = 'Set a relay category.'
            self.view.txt_relay_category.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            categories = self.model.heat.champ.categories.dict
            relay_entity = self.model.entity_selected
            relay_category = categories[values["category_id"]]
            relay_name = values["relay_name"]
            phase = current_heat.phase
            # Mira se xa existe a entidade, categoría e nome de remuda
            match_inscription = phase.inscriptions.search_relay(entity=relay_entity, category=relay_category, name=relay_name)  
            # Se existe, pregunta se quero movela a esta estaxe
                # se nesta estaxe xa hai outra remuda pregunta se quere intercambiar
                # caso de non querer intercambiar borra o resultado á actual inscrición
            if match_inscription and (not current_result or (match_inscription != current_result.inscription)):  # é distinta
                if match_inscription.result:  # ten resultado, está noutra estaxe
                    # Question if move
                    if self.view.msg.question(
                            _("This relay already has another result.\n"
                            "Do you like move to this lane?")):
                        if current_result:  # If exists result in current lane
                            # Question if exchange, otherside move and replace
                            if self.view.msg.question(
                                _("This lane has a result.\n"
                                "Do you like exchange?")):
                                # exchange
                                # Move current result to another heat and lane
                                current_result.lane, match_inscription.result.lane = match_inscription.result.lane, current_result.lane
                                current_result.heat, match_inscription.result.heat = match_inscription.result.heat, current_result.heat
                                current_result.save()
                                # match_inscription.result.save()
                            else:  # remove current_result in heat and lane
                                current_result.inscription.exchanged = True
                                current_result.inscription.result = None
                                current_result.inscription.save()
                                current_result.delete()
                        # Move another result to current heat and lane
                        match_inscription.result.heat = current_heat
                        match_inscription.result.lane = current_lane
                        match_inscription.result.save()
                        self.view.view_plus.stop()
                    else: # non fai nada xa que non quere mover
                        pass
                else:  # non ten resultado é unha inscrición sen resultado
                    # Pregunta se quere recuperar esta inscrición
                    # Question if move
                    if self.view.msg.question(
                            _("This relay already exists in inscriptions (without result).\n"
                            "Do you like move to this lane?")):                
                        if current_result:  # hai resultado na actual estaxe
                            # marka a inscrición como exchanged
                            # borra o resultado previo
                            current_result.inscription.exchanged = True
                            current_result.inscription.save()
                            current_result.inscription.result = None
                            current_result.delete()
                        match_inscription.exchanged = False
                        match_inscription.rejected = False
                        match_inscription.save()
                        match_inscription.add_result(
                                heat=current_heat, lane=current_lane)
                        match_inscription.result.save()
                        self.view.view_plus.stop()
                    else:
                        # Non fai nada
                        self.view.txt_relay_name.SetFocus()
            else:  # non atopou inscrición ou é a mesma remuda
                # se existe o resultado actualízao
                if current_result:  # If exists result in current lane
                    clear_relayers = False
                    if current_result.inscription.relay.entity != relay_entity:
                        current_result.inscription.relay.entity = relay_entity
                        clear_relayers = True
                    if current_result.inscription.relay.category != relay_category:
                        current_result.inscription.relay.category = relay_category
                        current_result.inscription.relay.gender_id = relay_category.gender_id
                        clear_relayers = True
                    if clear_relayers:
                        current_result.inscription.relay.relay_members.delete_all_items()
                    current_result.inscription.relay.name = relay_name
                    # revisar que borra os remudistas se cambia de club
                    current_result.inscription.relay.save()
                    # current_result.inscription.save()
                # se non existe engade a inscrición e o resultado
                else:  # Create inscription and result
                    new_inscription = self.model.heat.phase.inscriptions.item_blank
                    new_inscription.relay.entity = relay_entity
                    new_inscription.relay.category = relay_category
                    new_inscription.relay.name = relay_name
                    new_inscription.relay.gender_id = relay_category.gender_id

                    new_inscription.relay.save()
                    new_inscription.save()
                    new_inscription.add_result(
                            heat=current_heat, lane=current_lane)
                    new_inscription.result.save()
                self.view.view_plus.stop()

    def entity_name(self):
        entity_name = self.view.txt_entity_name.GetValue()
        # trata de establecer a entidade
        if entity_name:
            entities = self.model.heat.champ.entities
            entities_match = entities.get_entities_with_name(
                name=entity_name)
            entity_selected = None
            if len(entities_match) == 1:
                entity_selected = entities_match[0]
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
                    entity_selected = entities_match[choice[0]]
            else:
                # pon en branco todo, borrará o resultado se existir
                self.view.set_entity(entity=None)
                self.view.set_relay(relay=None)
                self.model.entity_selected = None
            if entity_selected:
                # establece a entidade na vista
                self.view.set_entity(entity=entity_selected)
                # mira se cambiou respecto do que había seleccionado
                if entity_selected != self.model.entity_selected:
                    if self.model.relay:
                        if entity_selected == self.model.relay.entity:
                            # Se a entidade é a mesma que a inicial,
                            # restitue os valores da remuda inicial
                            self.view.set_relay(relay=self.model.relay)
                        else:
                            # Borra os datos da remuda
                            self.view.set_relay(relay=None)
                    else:
                        # Borra os datos da remuda
                        self.view.set_relay(relay=None)
                    self.model.entity_selected = entity_selected
                else:
                    # No caso contrario é que non cambiou nada
                    #  polo tanto non se fai nada nada
                    pass
            else:
                # pon en branco todo, borrará o resultado se existir
                self.view.set_relay(relay=None)
                self.view.set_entity(entity=None)
                self.model.entity_selected = None
        
        
        
        # if  self.model.entity.name == entity_name:
        #     self.model.entity_name_change = False
        #     if self.model.entity_selected != self.model.entity.name:
        #         # Restitúe a remuda inicial
        #         self.model.entity_selected = self.model.entity
        #         # Restitúe o nome e categoría da remuda
        #         print("poñer aquí o código para restituir o nóme e categoría")
        # elif self.model.entity.name != entity_name:
        #    self.model.entity_name_change = True
        #     # self.model.entity = None
        # if entity_name:
        #         if ((self.model.entity_selected and (entity_name != 
        #         self.model.entity_selected.short_name)) or not self.model.entity_selected):
        #             entities = self.model.result.champ.entities
        #             entities_match = entities.get_entities_with_name(
        #                 name=entity_name)
        #             if len(entities_match) == 1:
        #                 self.model.entity_selected = entities_match[0]
        #             elif len(entities_match) > 1:
        #                 choices = []
        #                 for i in entities_match:
        #                     choices.append('{} {}'.format(i.short_name, i.entity_code))
        #                 choice = self.view.msg.choice(
        #                     _('Select entity'),
        #                     _('Select entity'), 
        #                     choices
        #                     )
        #                 if choice is not None:
        #                     self.model.entity_selected = entities_match[choice[0]]
        #         if (self.model.entity_selected and
        #             (self.model.entity_selected.entity_id != old_entity_id or 
        #                 not self.view.txt_relay_name.GetValue())):
        #             self.set_relay_name()
        #         elif not self.model.entity_selected:
        #             self.view.txt_relay_name.SetValue('')
        #     else:
        #         self.model.entity_selected = None
        #         self.view.txt_relay_name.SetValue('')
        #     self.view.set_entity(entity=self.model.entity_selected)
        #     self.model.entity_name_change = False
        #     print('change off')
        # # FIXME recuperar foco cando hai varias opcións

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
        entities = self.model.heat.champ.entities
        entity = entities.item_blank
        entity.lock = []
        from modules.entity_add_edit import p_entity_add_edit
        p_entity_add_edit.create(parent=self, entity=entity)
        if entity.entity_id:  # foi engadida
            self.model.entity_selected = entity
            self.view.set_entity(entity=self.model.entity_selected)
            self.set_relay_name()


    def cancel(self):
        self.view.view_plus.stop()

