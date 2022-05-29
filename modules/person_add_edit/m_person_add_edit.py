# -*- coding: utf-8 -*-


class Model(object):

    def __init__(self, person):
        self.person = person
        self.entity = person.entity
        self.entity_name_change = False
