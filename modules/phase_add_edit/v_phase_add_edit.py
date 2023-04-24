# -*- coding: utf-8 -*-


import wx

from .w_phase_add_edit import PhaseAddEdit
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.txt_integer import TxtInteger


class View(PhaseAddEdit):
    def __init__(self, parent):
        PhaseAddEdit.__init__(self, parent=parent)
        self.SetName('phase_add_edit')
        self.parent = parent
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.txt_pool_lanes_plus = TxtInteger(txt=self.txt_pool_lanes)

    def set_values(self, phase):

        # self.txt_code.SetValue(phase.code)
        event_id = phase.event and phase.event.event_id or None
        self.view_plus.cho_load(choice=self.cho_event_id,
                                values=phase.champ.events.choices(),
                                default=event_id)               
        self.txt_pool_lanes.SetValue(str(phase.pool_lanes))
        self.view_plus.cho_load(choice=self.cho_progression,
                                values=phase.champ.config.progressions.choices(),
                                default=phase.progression) 
        session_id = phase.session and phase.session.session_id or None
        self.view_plus.cho_load(choice=self.cho_session_id,
                                values=phase.champ.sessions.choices(),
                                default=session_id)  
        if 'event_id' in phase.lock:
            self.cho_event_id.Enable(False)
            self.txt_pool_lanes.SetFocus()
        else:
            self.cho_event_id.SetFocus()

    def get_values(self):
        values = {}
        # values["code"] = self.txt_code.GetValue().strip().upper()
        values["event_id"] = self.view_plus.cho_get(choice=self.cho_event_id)
        values["pool_lanes"] = int(self.txt_pool_lanes.GetValue().strip())
        values["progression"] = self.view_plus.cho_get(choice=self.cho_progression)
        values["session_id"] = self.view_plus.cho_get(choice=self.cho_session_id)
        return values
