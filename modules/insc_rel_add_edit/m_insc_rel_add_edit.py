# -*- coding: utf-8 -*-


class Model(object):

    def __init__(self, inscription):
        self.inscription = inscription
        self.entity = inscription.relay.entity
        self.choice = None
        self.entity_name_change = None
