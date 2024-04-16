# -*- coding: utf-8 -*-


from email import message
from .m_res_ind_add_edit import Model
from .v_res_ind_add_edit import View
from .i_res_ind_add_edit import Interactor


def create(parent, heat, lane, result):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(heat=heat, lane=lane, result=result),
            view=View(parent.view),  # main_frame casca
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
            self.view.set_person(person=self.model.person)
        self.view.txt_person_full_name.SetFocus()
        self.view.view_plus.start(modal=True)

    def delete(self):
        current_result = self.model.result
        if current_result and current_result.result_id:  # Question if remove current result
            message = _("Are you sure you want to delete this result?")
            if self.view.msg.question(message):
                print('set inscription as rejected and delete current result')
                current_result.inscription.rejected = True
                current_result.inscription.result = None
                current_result.inscription.save()
                current_result.delete()
                self.view.view_plus.stop()
        else:
            self.view.msg.warning(_("There is no person to delete."))
            self.view.txt_person_full_name.SetFocus()
    
    def acept(self):
        # if self.model.person_full_name_change:
        #     print('foi modificado')
        #     self.person_full_name()
        # else:
        #     print('non foi modificado')
        current_heat = self.model.heat
        current_lane = self.model.lane
        current_result = self.model.result
        if current_result:
            current_person = current_result.person
        else:
            current_person = None
        new_person = self.model.person
        if new_person and new_person != current_person:
            match_inscription = new_person.get_phase_insc(phase_id=current_heat.phase.phase_id)
            if match_inscription:
                if match_inscription.result:
                    # Question if move
                    if self.view.msg.question(
                            _("This person already has another result.\n"
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
                                current_result.delete()
                        # Move another result to current heat and lane
                        match_inscription.result.heat = current_heat
                        match_inscription.result.lane = current_lane
                        match_inscription.result.save()
                        self.view.view_plus.stop()
                    else:  # Non fai nada
                        self.view.txt_person_full_name.SetFocus()
                else:  # If new inscription without result
                    # if self.view.msg.question(
                    #         _("This person already exists in inscriptions (without result).\n"
                    #         "Do you like move to this lane?")):
                    if current_result:
                        # hai resultado na actual estaxe
                        # marka a inscrición como exchanged
                        # borra o resultado previo
                        current_result.inscription.exchanged = True
                        current_result.inscription.result = None
                        current_result.inscription.save()
                        current_result.delete()
                    match_inscription.exchanged = False
                    match_inscription.rejected = False
                    match_inscription.save()
                    match_inscription.add_result(
                            heat=current_heat, lane=current_lane)
                    match_inscription.result.save()
                    self.view.view_plus.stop()
                    # else:
                    #     # Non fai nada
                    #     self.view.txt_person_full_name.SetFocus()
            else:  # Selected person not has inscription
                if current_result:  # If eself.model.person_full_name_changexists result in current lane
                    # Question if replace
                    if self.view.msg.question(
                            _("This lane has a result.\n"
                            "Do you like replace?\n"
                            "This result will be deleted.")):
                        # delete current result
                        current_result.inscription.exchanged = True
                        current_result.inscription.result = None
                        current_result.inscription.save()
                        current_result.delete()
                        # Create inscription and result
                        match_inscription = current_heat.phase.inscriptions.item_blank
                        match_inscription.person = new_person
                        match_inscription.save()
                        match_inscription.add_result(
                                heat=current_heat, lane=current_lane)
                        match_inscription.result.save()
                        current_heat.phase.inscriptions.append(match_inscription)  # sobrecargado para que acutalice as inscricións da persoa
                        # new_person.inscriptions.load()  # actualiza as inscricións da persoa
                        self.view.view_plus.stop()
                else:
                        # Create inscription and result
                        match_inscription = current_heat.phase.inscriptions.item_blank
                        match_inscription.person = new_person
                        match_inscription.save()
                        match_inscription.add_result(
                                heat=current_heat, lane=current_lane)
                        match_inscription.result.save()
                        current_heat.phase.inscriptions.append(match_inscription)  # sobrecargado para que acutalice as inscricións da persoa
                        # new_person.inscriptions.load()  # actualiza as inscricións da persoa
                        self.view.view_plus.stop()
        elif new_person == current_person:  # Same person selected
            self.view.msg.warning(_("Same person is in current lane.\nPlease, select a distinct person."))
            self.view.txt_person_full_name.SetFocus()
        elif not new_person:  # Not person selected
            self.view.msg.warning(_("Please, select a person."))
            self.view.txt_person_full_name.SetFocus()

    def person_full_name(self):           
        self.model.person = None
        person_name = self.view.txt_person_full_name.GetValue()
        if person_name:
            gender_id = None
            if self.model.heat.event.gender_id != 'X':
                gender_id = self.model.heat.event.gender_id
            persons = self.model.heat.champ.persons
            persons_match = persons.get_persons_with_name(
                criterias=person_name, gender_id=gender_id)
            if len(persons_match) == 1:
                self.model.person = persons_match[0]
            elif len(persons_match) > 1:
                choices = []
                for i in persons_match:
                    choices.append('{} {}'.format(i.full_name, i.license))
                choice = self.view.msg.choice(
                    _('Select person'),
                    _('Select person'), 
                    choices
                    )
                if choice is not None:
                    self.model.person = persons_match[choice[0]]
        self.view.set_person(self.model.person)
        print('change off')

    def add_person(self):
        event = self.model.heat.event
        persons = self.model.heat.champ.persons
        person = persons.item_blank
        person.lock = []
        if event.gender_id != 'X':
            person.gender_id = event.gender_id
            person.lock.append('gender_id')
        from modules.person_add_edit import p_person_add_edit
        p_person_add_edit.create(parent=self, person=person)
        if person.person_id:  # foi engadida
            self.model.person = person
            self.view.set_person(self.model.person)


    def cancel(self):
        print('cancelou')
        self.view.view_plus.stop()

