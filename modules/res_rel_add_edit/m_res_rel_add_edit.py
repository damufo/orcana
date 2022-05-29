# -*- coding: utf-8 -*-


class Model(object):

    def __init__(self, result):
        self.result = result
        self.relay = result.relay
        self.entity = None
        self.entity_name_change = False
