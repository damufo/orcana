# -*- coding: utf-8 -*-


class Model(object):

    def __init__(self, inscription):
        self.inscription = inscription
        self.person = inscription.person
        self.phase = inscription.phase
        self.person_full_name_change = None
