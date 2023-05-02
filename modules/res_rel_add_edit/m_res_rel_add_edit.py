# -*- coding: utf-8 -*-


class Model(object):

    def __init__(self, result):
        self.result = result
        self.entity_selected = result.relay.entity
        self.entity_name_change = False

    @property
    def entity_change(self):
        return not (self.result.relay.entity == self.entity_selected)
