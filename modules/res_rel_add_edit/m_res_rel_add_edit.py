# -*- coding: utf-8 -*-


class Model(object):

    def __init__(self, heat, lane, result):
        self.heat = heat
        self.lane = lane
        self.result = result
        if result and result.relay:
            self.relay = result.relay
            self.entity_selected = self.relay.entity
        else:
            self.relay = None
            self.entity_selected = None


    @property
    def entity_change(self):
        return not (self.result.relay.entity == self.entity_selected)
