# -*- coding: utf-8 -*-


from .m_relay_members import Model
from .v_relay_members import View
from .i_relay_members import Interactor


def create(parent, relay_members):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(relay_members=relay_members),
            view=View(parent.parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.model.candidates.load_items_from_dbs()
        # Candidates, delete relay_members already in use
        # if self.model.relay_members:
            # for result_member in self.model.relay_members:
            #     self.model.candidates.remove_person(result_member.person.person_id)

        # Delete cadidate members in another relays in same phase
        max_relay_participation = 1
        member_count = {}
        current_relay_entity_id = self.model.relay_members.relay.entity.entity_id
        current_relay_event_id = self.model.relay_members.relay.event_id
        for relay, event in self.model.relay_members.champ.relays_events:
            if (relay.entity.entity_id == current_relay_entity_id and
                    event.event_id == current_relay_event_id):
                for relay_member in relay.relay_members:
                    person_id = relay_member.person_id
                    if person_id in member_count:
                        member_count[person_id] += 1
                    else:
                        member_count[person_id] = 1
                    # member_count
                    if member_count[person_id] >= max_relay_participation:
                        print(relay_member.person.full_name)
                        self.model.candidates.remove_person(relay_member.person.person_id)

        self.view.lsc_candidates_plus.values = self.model.candidates
        self.view.lsc_candidates_plus.load(custom_column_widths=True)
        
        self.view.lsc_members_plus.values = self.model.relay_members
        self.view.lsc_members_plus.load(custom_column_widths=True)
        if self.model.relay_members.num_members == len(self.model.relay_members):
            self.view.btn_new_person.Enable(False)
        self.view.set_values(self.model.relay_members)
        # If result is official disable changes
        if self.model.relay_members.relay.inscription.result.heat.official:
            # disable buttons
            self.view.btn_new_person.Enable(False)
            self.view.btn_select_candidates.Enable(False)
            self.view.btn_remove_members.Enable(False)
            self.view.btn_move_up.Enable(False)
            self.view.btn_move_down.Enable(False)
            self.view.lsc_candidates.Enable(False)
            self.view.lsc_members.Enable(False)

        # self.model.relay_members.load_items_from_dbs()
        # self.view.lsc_caplus.values = self.model.relay_members
        # self.view.lsc_plus.load(custom_column_widths=True)
        # self.view.set_values(prefs=self.model.prefs)
        # self.view.view_plus.start(modal=True)

    # def acept(self):
    #     self.view.get_values(prefs=self.model.prefs)p
    #     self.model.prefs.save()
    #     self.view.view_plus.stop()

    def go_back(self):
        self.view.close()
        if self.parent.name == "inscriptions":  # parent is presenter
            self.parent.parent.load_inscriptions()
        elif self.parent.name == "heats":
            self.parent.parent.load_heats()
        # if self.parent.name == "inscriptions":  # parent is presenter
        #     idx = self.parent.view.lsc_plus.get_sel_pos_item()
        #     self.parent.view.lsc_plus.update_item(idx)
        # elif self.parent.name == "heats":
        #     self.parent.parent.load_heats()

    def new_person(self):
        relay_members = self.model.relay_members
        # relay_members_view = {}
        # relay_members_view['candidates_pos'] = self.view.lsc_candidates_plus.get_sel_pos_item()
        # relay_members_view['members_pos'] = self.view.lsc_members_plus.get_sel_pos_item()
        # relay_members_view['relay_members'] = self.model.relay_members
        # self.model.candidates.config.views['relay_members'] = relay_members_view
        # self.view.lsc_candidates_plus.save_custom_column_width()
        # self.view.lsc_members_plus.save_custom_column_width()
        person = self.model.candidates.item_blank
        person.entity = self.model.relay_members.champ.entities.get_entity(self.model.candidates.entity_id)
        person.lock = []
        person.lock.append('entity_id')
        if self.model.candidates.gender_id != 'X':
            person.gender_id = self.model.candidates.gender_id
            person.lock.append('gender_id')
        from modules.person_add_edit import p_person_add_edit
        p_person_add_edit.create(parent=self, person=person)

        if person.person_id:  # foi engadida
            relay_members.add_member(person)
            self.view.lsc_members_plus.add_last_item()
            if relay_members.num_members == len(relay_members):
                    self.view.btn_new_person.Enable(False)

        # self.view.lsc_members_plus.update_item(idx=pos) 

    def select_candidates(self):
        idxs = self.view.lsc_candidates_plus.get_sel_pos_items()
        for idx in idxs:
            if idx not in self.view.candidates_selected:
                self.view.candidates_selected.append(idx)
        for selected in self.view.candidates_selected:
            if selected not in idxs:
                self.view.candidates_selected.remove(selected)
        
        current_selected = len(self.model.relay_members)
        current_candidates = len(self.view.candidates_selected)

        if (current_selected + current_candidates) > self.model.relay_members.num_members:
                self.view.msg.warning(_("No more members are allowed in this relay."))
                last_person_added = self.view.candidates_selected[-1]
                # deselect last person added
                self.view.lsc_candidates.Select(last_person_added, on=0)
        if self.view.candidates_selected:
            self.view.lsc_candidates.Focus(self.view.candidates_selected[-1])
        else:
            self.view.lsc_candidates.Focus(0)

        
        print(', '.join([self.model.candidates[i].name for i in self.view.candidates_selected]))
        print('...')

    def move_down(self):
        idx = self.view.lsc_members_plus.get_sel_pos_item()
        if idx is not None:
            if idx == (len(self.model.relay_members)-1):
                self.view.msg.warning(_("This is already the last element."))
            else:
                self.model.relay_members.move_down(idx)
                self.view.lsc_members_plus.update_item(idx)
                self.view.lsc_members_plus.update_item(idx + 1)
                self.view.lsc_members_plus.set_sel_pos_item(idx + 1)
                # print(self.view.lsc_members.GetFocusedItem())
                # print(idx + 1)

        else:
            self.view.msg.warning(message=_("No item selected."))

    def move_up(self):
        idx = self.view.lsc_members_plus.get_sel_pos_item()
        if idx is not None:
            if idx == 0:
                self.view.msg.warning(_("This is already the first element."))
            else:
                self.model.relay_members.move_up(idx)
                self.view.lsc_members_plus.update_item(idx)
                self.view.lsc_members_plus.update_item(idx - 1)
                self.view.lsc_members_plus.set_sel_pos_item(idx - 1)
                # print(self.view.lsc_members.GetFocusedItem())
                # print(idx - 1)
        else:
            self.view.msg.warning(message=_("No item selected."))

    def save_candidates(self):
        idxs = self.view.candidates_selected
        if idxs:
            candidates_selected = [self.model.candidates[idx] for idx in idxs]
            idxs = self.view.lsc_candidates_plus.get_sel_pos_items()
            for idx in idxs:
                self.view.lsc_candidates.Select(idx, on=0)  #deselect
                self.view.lsc_candidates.Focus(0)  #deselect
            update_list = False
            relay_members = self.model.relay_members
            for person in candidates_selected:
                if len(relay_members) >= relay_members.num_members:
                    self.view.msg.warning(_("No more members are allowed in this relay."))
                    break
                # check if already in members
                add_member = True
                for member in relay_members:
                    if member.person.person_id == person.person_id:
                        self.view.msg.warning(_("This person is already a member of the relay."))
                        add_member = False
                        break
                if add_member:
                    relay_members.add_member(person)
                    self.model.candidates.remove(person)
                    update_list = True
            if update_list:
                self.view.lsc_candidates_plus.load(custom_column_widths=True)
                self.view.lsc_members_plus.load(custom_column_widths=True)
                self.view.lsc_members_plus.set_sel_pos_item_last()
                if relay_members.num_members == len(relay_members):
                    self.view.btn_new_person.Enable(False)
        else:
            self.view.msg.warning(message=_("No item selected."))

    def remove_members(self):
        idxs = self.view.lsc_members_plus.get_sel_pos_items()
        if idxs:
            for idx in sorted(idxs, reverse=True):
                person = self.model.relay_members[idx].person
                self.model.candidates.append(person)
            self.model.candidates.sort()
            self.view.lsc_candidates_plus.load(custom_column_widths=True)        
            self.model.relay_members.delete_items(idxs)
            self.view.lsc_members_plus.load(custom_column_widths=True)
            self.view.btn_new_person.Enable(True)