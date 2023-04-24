# -*- coding: utf-8 -*-


from .m_events import Model
from .v_events import View
from .i_events import Interactor


def create(parent, events):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(events=events),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.events.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.events
        self.view.lsc_plus.load(custom_column_widths=True)
        # self.view.set_values(prefs=self.model.prefs)
        # self.view.view_plus.start(modal=True)

    # def acept(self):
    #     self.view.get_values(prefs=self.model.prefs)
    #     self.model.prefs.save()
    #     self.view.view_plus.stop()

    def go_back(self):
        self.view.close()
        self.parent.load_me()

    def event_categories(self):
        print("set categories")
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            event = self.model.events[idx]

            event_categories = event.event_categories
            from modules.event_categories import p_event_categories
            p_event_categories.create(parent=self, event_categories=event_categories)
            self.view.lsc_plus.update_item(idx)

    def move_down(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            if idx == (len(self.model.events)-1):
                self.view.msg.warning(_("This is already the last element."))
            else:
                self.model.events.move_down(idx)
                self.view.lsc_plus.update_item(idx)
                self.view.lsc_plus.update_item(idx + 1)
                self.view.lsc_plus.set_sel_pos_item(idx + 1)

    def move_up(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            if idx == 0:
                self.view.msg.warning(_("This is already the first element."))
            else:
                self.model.events.move_up(idx)
                self.view.lsc_plus.update_item(idx)
                self.view.lsc_plus.update_item(idx - 1)
                self.view.lsc_plus.set_sel_pos_item(idx - 1)
                
    def add(self):
        events = self.model.events
        event = events.item_blank
        event.lock = []
        from modules.event_add_edit import p_event_add_edit
        p_event_add_edit.create(parent=self, event=event)
        if event.event_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(events) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            event = self.model.events[idx]
            event.lock = []
            # event.lock = ['code']
            # if event.official:
            #     message=_("Is not possible edit event when is official.")
            #     self.view.msg.warning(message=message)
            # else:
                # if len(event.heats):
                #     event.lock = ['event_id']
            from modules.event_add_edit import p_event_add_edit
            p_event_add_edit.create(parent=self, event=event)
            self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items? "
                        "\nAll event phases, event categories, event heats and "
                        "\nevent results are deleted.")
            if self.view.msg.question(message=message):
                for i in idxs:
                    self.model.events.delete_items(idxs)
                    self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))