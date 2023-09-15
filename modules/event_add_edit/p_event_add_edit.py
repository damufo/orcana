# -*- coding: utf-8 -*-


from .m_event_add_edit import Model
from .v_event_add_edit import View
from .i_event_add_edit import Interactor


def create(parent, event, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(event=event),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(event=self.model.event)
        self.view.view_plus.start(modal=True)

    def acept(self):
        event = self.model.event
        values = self.view.get_values()
        msg = None
        if not values['code']:
            msg = 'Set a event code.'
            self.view.cho_code.SetFocus()
        elif not values['gender_id']:
            msg = 'Set a gender.'
            self.view.cho_gender_id.SetFocus()
        elif not values['name']:
            msg = 'Set a event name.'
            self.view.txt_name.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            event.code = values['code']
            event.gender_id = values['gender_id']
            event.name = values['name']
            if not event in event.events:
                event.events.append(event)
            event.save()
            self.view.view_plus.stop()

    def cancel(self):
        self.view.view_plus.stop()

    def generate_name(self):
        self.view.generate_name(self.model.event)
