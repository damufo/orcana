# -*- coding: utf-8 -*-


from .m_phase_add_edit import Model
from .v_phase_add_edit import View
from .i_phase_add_edit import Interactor


def create(parent, phase, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(phase=phase),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(phase=self.model.phase)
        if self.model.phase.official:
            # Disable acept button
            self.view.btn_acept.Enable(False)
        self.view.view_plus.start(modal=True)

    def acept(self):
        phase = self.model.phase
        values = self.view.get_values()
        msg = None
        pool_lanes_sort_validated = phase.champ.validade_pool_lanes_sort(values['pool_lanes_sort'])
        if not values['event_id']:
            msg = 'Set a event_id.'
            self.view.cho_event_id.SetFocus()
        elif not values['progression']:
            msg = 'Set a progression.'
            self.view.cho_progression.SetFocus()
        elif phase.already_exists(event_id=values["event_id"], progression=values['progression']):
            msg = 'Already exists.'
            self.view.cho_event_id.SetFocus()
        elif not pool_lanes_sort_validated:
            msg = 'Set a pool lanes sort.'
            self.view.txt_pool_lanes_sort.SetFocus()

        elif not values['session_id']:
            msg = 'Set a session.'
            self.view.cho_session_id.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            event = phase.champ.events.get_event(
                event_id=values['event_id'])
            session = phase.champ.sessions.get_session(
                session_id=values['session_id'])
            phase.event = event
            phase.pool_lanes_sort = pool_lanes_sort_validated
            phase.progression = values['progression']
            phase.num_clas_next_phase = values['num_clas_next_phase']
            phase.session = session
            phase.phases.append(phase)
            phase.save()
            self.view.view_plus.stop()

    def cancel(self):
        # self.view.view_plus.close()
        # self.model.category.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

