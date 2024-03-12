# -*- coding: utf-8 -*-


from .m_session_add_edit import Model
from .v_session_add_edit import View
from .i_session_add_edit import Interactor


def create(parent, session, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(session=session),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(session=self.model.session)
        self.view.view_plus.start(modal=True)

    def acept(self):
        session = self.model.session
        values = self.view.get_values()
        msg = None
        if not values['date']:
            msg = 'Set a date.'
            self.view.txt_date.SetFocus()
        elif not values['time']:
            msg = 'Set a time.'
            self.view.txt_time.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            session.date = values['date']
            session.time = values['time']
            session.save()
            if not session in session.sessions:
                session.sessions.append(session)
            self.view.view_plus.stop()

    def cancel(self):
        # self.view.view_plus.close()
        # self.model.session.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

