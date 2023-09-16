# -*- coding: utf-8 -*-


from .m_sessions import Model
from .v_sessions import View
from .i_sessions import Interactor


def create(parent, sessions):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(sessions=sessions),
            view=View(parent.parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.sessions.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.sessions
        self.view.lsc_plus.load(custom_column_widths=True)

    def go_back(self):
        self.view.close()
        self.parent.parent.load_properties()

    def add(self):
        sessions = self.model.sessions
        session = sessions.item_blank
        session.lock = []
        from modules.session_add_edit import p_session_add_edit
        p_session_add_edit.create(parent=self, session=session)
        if session.session_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(sessions) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            session = self.model.sessions[idx]
            session.lock = []
            # session.lock = ['code']
            from modules.session_add_edit import p_session_add_edit
            p_session_add_edit.create(parent=self, session=session)
            self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items?")
            if self.view.msg.question(message=message):
                self.model.sessions.delete_items(idxs)
                self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))