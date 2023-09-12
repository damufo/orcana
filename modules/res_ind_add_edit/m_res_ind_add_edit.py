# -*- coding: utf-8 -*-


class Model(object):

    def __init__(self, heat, lane, result):
        self.heat = heat
        self.lane = lane
        self.result = result
        if result and result.person:
            self.person = result.person
        else:
            self.person = None
        self.person_full_name_change = False
